import streamlit as st
import yaml
import os
import shutil
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
from config import AppName, config_path
from database.database import create_tables, add_game, get_games, delete_game, update_game, add_user_rating, get_ratings_for_game, update_user_rating, has_user_voted, get_rated_users_for_game
from utils.image_utils import save_uploaded_image
from utils.email_utils import email_forgot_password, email_forgot_username
from utils.steam import fetch_game_details, extract_app_id

if not os.path.exists(config_path):
    path = shutil.copy("./config.example.yaml", config_path)
    st.success("Config file created. Please modify config.yaml with your settings.")

with open(config_path) as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def write_auth():
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def main():
    create_tables()

    st.title(AppName)
    

    if 'forgot_pwd' not in st.session_state:
        st.session_state.forgot_pwd = False

    if 'forgot_user' not in st.session_state:
        st.session_state.forgot_user = False

    if 'register_user' not in st.session_state:
        st.session_state.register_user = False

    if 'choice' not in st.session_state:
        st.session_state.choice = 'List Games'

    authenticator.login('Login', 'main') 
    isLoggedIn = st.session_state.authentication_status
    if isLoggedIn is None or isLoggedIn is False:
        if isLoggedIn is False:
            st.error('Username/password is incorrect')

        if not st.session_state.forgot_pwd and not st.session_state.forgot_user and not st.session_state.register_user:
            if st.session_state.authentication_status:
                st.rerun()
            forgot_col1, forgot_col2, forgot_col3 = st.columns([1,1,2])
            with forgot_col1:
                if st.button('Forgot password'):
                    st.session_state.forgot_pwd = True
                    st.rerun()
            with forgot_col2:
                if st.button('Forgot username'):
                    st.session_state.forgot_user = True
                    st.rerun()
            with forgot_col3:
                if st.button('Register'):
                    st.session_state.register_user = True
                    st.rerun()
        elif st.session_state.forgot_pwd:
            try:
                username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
                if username_of_forgotten_password:
                    email_forgot_password(email_of_forgotten_password, new_random_password, username_of_forgotten_password)
                    write_auth()
                    st.success(f"Send newly generated password to email of {username_of_forgotten_password}")
                elif username_of_forgotten_password == False:
                    st.error('Username not found')
                if st.button('Back','forgot_pwd_btn_back'):
                    st.session_state.forgot_pwd = False
                    st.rerun()
            except Exception as e:
                st.error(e)     
        elif st.session_state.register_user:
            try:
                if authenticator.register_user('Register user', preauthorization=False):
                    write_auth()
                    st.success('User registered successfully')
                if st.button('Back','register_user_btn_back'):
                    st.session_state.register_user = False
                    st.rerun()
            except Exception as e:
                st.error(e)  
        elif st.session_state.forgot_user:
            try:
                username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
                if username_of_forgotten_username:
                    email_forgot_username(email_of_forgotten_username, username_of_forgotten_username)
                    write_auth()
                    st.success(f"Send username to: {email_of_forgotten_username}")
                elif username_of_forgotten_username == False:
                    st.error('Email not found')
                if st.button('Back','forgot_user_btn_back'):
                    st.session_state.forgot_user = False
                    st.rerun()
            except Exception as e:
                st.error(e)
    
    elif isLoggedIn:
        isAdmin = st.session_state["username"] == 'dkin'
        st.sidebar.write(f'Welcome *{str.capitalize(st.session_state["name"])}*')
        st.sidebar.divider()
        if st.sidebar.button('List Games 🎮', type='primary' if st.session_state.choice == 'List Games' else 'secondary', use_container_width=True):
            st.session_state.choice = 'List Games'
            st.rerun()
        if st.sidebar.button('Vote 🗳️', type='primary' if st.session_state.choice == 'Vote' else 'secondary', use_container_width=True):
            st.session_state.choice = 'Vote'
            st.rerun()
        if st.sidebar.button('Account 😁', type='primary' if st.session_state.choice == 'Account' else 'secondary', use_container_width=True):
            st.session_state.choice = 'Account'
            st.rerun()
        if st.sidebar.button('Manage 👑', type='primary' if st.session_state.choice == 'Manage' else 'secondary', use_container_width=True):
            st.session_state.choice = 'Manage'
            st.rerun()
        st.sidebar.divider()
        authenticator.logout('Logout', key='unique_key', location="sidebar")
        
        choice = st.session_state.choice

        if choice == "Account":
            try:
                if authenticator.reset_password(st.session_state["username"], 'Change password'):
                    st.success('Password modified successfully')
                    write_auth()
            except Exception as e:
                st.error(e)

            try:
                if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
                    st.success('Entries updated successfully')
                    write_auth()
            except Exception as e:
                st.error(e)
            
        elif choice == "Manage":
            st.header("Manage Games")
            actions = [ "Add Steam Game","Add Custom Game", "Delete", "Update"] if isAdmin else ["Add Steam Game","Add Custom Game"]
            action = st.selectbox("Select action", actions)

            if action == "Add Custom Game":
                st.subheader("Add a Custom New Game")
                name = st.text_input("Name")
                description = st.text_area("Description")
                link = st.text_input("Link")
                image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
                add_button_key = f"add_button_{name}"

                if st.button("Add Game", key=add_button_key):
                    image_path = save_uploaded_image(image)
                    add_game(name, description, link, image_path)
                    st.success("Game added successfully!")

            if action == "Add Steam Game":
                st.subheader("Add a Steam New Game")
                st.write('Provide a valid steam store url: Example: https://store.steampowered.com/app/892970/Valheim/')
                steam_link = st.text_input("Steam Url")
                add_button_key = f"add_button_steam_game"

                if st.button("Add Game", key=add_button_key):
                    name, description, image_path = fetch_game_details(steam_link)
                    if name and description and image_path:
                        add_game(name, description, steam_link, image_path)
                        st.success("Game added successfully!")
                    else:
                        st.error('Failed to retrieve')
                        st.rerun()

            elif action == "Delete":
                st.subheader("Delete a Game")
                games = get_games()
                game_names = [game[1] for game in games]
                selected_game = st.selectbox("Select a game to delete", game_names)

                if st.button("Delete Game"):
                    delete_game(selected_game)
                    st.success(f"{selected_game} deleted successfully!")
                    st.rerun()

            elif action == "Update":
                st.subheader("Update Game Information")
                games = get_games()
                game_names = [game[1] for game in games]
                selected_game = st.selectbox("Select a game to update", game_names)
                selected_game_details = [game for game in games if game[1] == selected_game][0]
                new_name = st.text_input("New Name", value=selected_game_details[1])
                new_description = st.text_area("New Description", value=selected_game_details[2])
                new_link = st.text_input("New Link", value=selected_game_details[3])
                new_image = st.file_uploader("Choose a new image", type=["jpg", "jpeg", "png"])
                update_button_key = f"update_button_{selected_game}"

                if st.button("Update Game", key=update_button_key):
                    new_image_path = save_uploaded_image(new_image)

                    update_game(selected_game, new_name, new_description, new_link, new_image_path)
                    st.success(f"{selected_game} updated successfully!")

        elif choice == "Vote":
            st.header("Vote for Games")

            games = get_games()

            username = st.session_state["username"]
            for game in games:
                st.subheader(game[1])  

                image_path = game[4]  
                if image_path:
                    st.image(image_path, use_column_width=False, width=300)

                st.write(game[2])
                app_id = extract_app_id(game[3])
                st.markdown(f"Store: [Steam Website]({game[3]}) | [Steam Desktop](steam://store/{app_id})")

                rating_slider_key = f"{game[0]}_rating_slider"
                vote_button_key = f"vote_button_{game[0]}"

                has_voted, votes = has_user_voted(username, game[0])

                if has_voted:
                    st.info("You have already voted for this game. You can update your vote.")
                    rating = st.slider("Update your rating", 1, 10, key=rating_slider_key, value=votes)
                else:
                    st.warning("You haven't voted for this game yet. Please vote.")
                    rating = st.slider("Rate this game", 1, 10, key=rating_slider_key)

                if st.button("Vote", key=vote_button_key):
                    game_id = game[0]
                    if has_voted:
                        update_user_rating(username, game_id, rating)
                        st.success(f"Your vote for {game[1]} has been updated!")
                    else:
                        add_user_rating(username, game_id, rating)
                        st.success(f"Your vote for {game[1]} has been recorded!")

                    total_rating = calculate_total_rating_for_game(game_id)
                    st.write(f"Total Rating for {game[1]}: {total_rating}")
                    st.rerun()

        elif choice == "List Games":
            list_games()

def game_sort(e):
    return e[5]

def list_games():
    st.header("List of Games with Total Ratings")
    games = get_games()
    st.divider()
    new_games = list()

    for game in games:
        game = list(game)
        game.append(calculate_total_rating_for_game(game[0]))
        new_games.append(game)
        
    new_games.sort(key=game_sort,reverse=True)
    ranking = 1
    for game in new_games:
        st.subheader(f'{ranking}. {game[1]}')

        image_path = game[4]
        if image_path:
            st.image(image_path, use_column_width=False, width=300)

        st.write(game[2])
        app_id = extract_app_id(game[3])
        st.markdown(f"Store: [Steam Website]({game[3]}) | [Steam Desktop](steam://store/{app_id})")

        total_rating = game[5]
        st.subheader(f"Total Rating: {total_rating}")
        users_voted = get_voted_users(game[0])
        st.write('Users voted: ' + (','.join(users_voted) if len(users_voted) > 0 else '0'))
        st.divider()
        ranking += 1

def calculate_total_rating_for_game(game_id):
    ratings = get_ratings_for_game(game_id)
    
    if ratings:
        total_sum = sum(ratings)
        total_count = len(ratings)
        return total_sum / total_count

    return 0

def get_voted_users(game_id):
    users = get_rated_users_for_game(game_id)
    if users:
        return users

    return []

def save_uploaded_image(uploaded_image):
    if uploaded_image:
        image_path = f"uploads/{uploaded_image.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())
        return image_path

if __name__ == "__main__":
    main()
