import streamlit as st

st.set_page_config(
        page_title="Manage - Kerstlan",
        page_icon="🎅",
    )

from database.database import add_game, add_riddle, delete_riddle, get_games, delete_game, get_riddles, get_users, update_game, update_riddle
from utils.image_utils import save_uploaded_image
from utils.steam import fetch_game_details
from utils.login import isAdmin, login
from utils.submenu import generate_subment_extras
from utils.login import config
from streamlit_authenticator import Authenticate

authenticate = Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )

st.session_state.authenticate = authenticate

def page():
    st.header("Manage Games")
    actions = [ "Add Steam Game","Add Custom Game", "Delete", "Update", "Add Riddle", "Update Riddle", "Delete Riddle"] if isAdmin() else ["Add Steam Game","Add Custom Game"]
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

    elif action == "Add Riddle":
        st.subheader("Add new Riddle")
        name = st.text_input("Name")
        riddle = st.text_area("Riddle")
        hint = st.text_input("Hint")
        answer = st.text_input("Answer")
        users = [user[0] for user in get_users()]
        username = st.selectbox("Select a User", users)
        add_button_key = f"add_button_{name}"

        if st.button("Add Riddle", key=add_button_key):
            add_riddle(name, riddle, hint, answer, username)
            st.success("Riddle added successfully!")
            
    elif action == 'Delete Riddle':
        st.subheader("Delete a Game")
        riddles = get_riddles()        
        selected_riddle = st.selectbox("Select a riddle to update",riddles, format_func=lambda riddle: f'{riddle[1]}: {riddle[6]}')

        if st.button("Delete riddle"):
            delete_riddle(selected_riddle[0])
            st.success(f"{selected_riddle[1]} deleted successfully!")
            st.rerun()

    elif action == "Update Riddle":
        riddles = get_riddles()
        if len(riddles) == 0: 
            st.subheader('0 riddles in DB!')
            return
        st.subheader("Update Riddle Information")
        selected_riddle = st.selectbox("Select a riddle to update",riddles, format_func=lambda riddle: f'{riddle[1]}: {riddle[6]}')
        new_name = st.text_input("Name", value=selected_riddle[1])
        new_riddle = st.text_area("Riddle", value=selected_riddle[2])
        new_hint = st.text_input("Hint", value=selected_riddle[3])
        new_answer = st.text_input("Answer", value=selected_riddle[4])
        used_hints = st.number_input("Used Hints", value=selected_riddle[5], min_value=0)
        
        # users = [user[0] for user in get_users()]
        # selected_user_index = users.index(selected_riddle[6])
        new_username = selected_riddle[6]
        new_solved = 1 if st.checkbox("Solved", value=selected_riddle[7] == 1) else 0
        update_button_key = f"update_button_{selected_riddle}"

        if st.button("Update Riddle", key=update_button_key):
            update_riddle(selected_riddle[0], new_name, new_riddle, new_hint, new_answer, used_hints, new_username, new_solved)
            st.success(f"{selected_riddle[1]} updated successfully!")
            
if __name__ == "__main__":
    if login():
        generate_subment_extras()
        page()