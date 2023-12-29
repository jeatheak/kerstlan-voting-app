import yaml
import os
import shutil
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
from config import AppName, config_path, admin_user
import streamlit as st
from config import admin_user
from database.database import add_game, get_games, delete_game, update_game, add_user_rating, update_user_rating, has_user_voted, get_rated_users_for_game
from utils.calc import calculate_total_rating_for_game
from utils.christmass import christmas_countdown
from utils.image_utils import save_uploaded_image
from utils.steam import fetch_game_details, extract_app_id
from utils.login import authenticator, write_auth, login

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

isAdmin = st.session_state["username"] == admin_user

def main():    
    if login():
        christmas_countdown()
        isAdmin = st.session_state["username"] == admin_user
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

        

def save_uploaded_image(uploaded_image):
    if uploaded_image:
        image_path = f"uploads/{uploaded_image.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())
        return image_path

if __name__ == "__main__":
    main()
