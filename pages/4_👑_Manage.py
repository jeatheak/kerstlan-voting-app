import streamlit as st
from database.database import add_game, get_games, delete_game, update_game
from utils.image_utils import save_uploaded_image
from utils.steam import fetch_game_details
from utils.login import isAdmin, login


def page():
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
            
if __name__ == "__main__":
    if login():
        page()