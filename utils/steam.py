import streamlit as st
import re
import os
import requests

def extract_app_id(url):
    match = re.search(r'/app/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def get_game_details(app_id):
    base_url = "http://store.steampowered.com/api/appdetails/"
    params = {"appids": app_id}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get(str(app_id)):
        return data[str(app_id)]["data"]
    
    return None

def download_and_save_image(url, folder, filename):
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(folder, filename + '.jpg')
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    return None

def fetch_game_details(url: str):
    app_id = extract_app_id(url)

    if app_id:
        image_filepath = None
        description = None
        name = None

        game_info = get_game_details(app_id)
        if game_info == None:
            st.warning("Game details not found.")
            return None, None, None
        
        name = game_info['name']
        description = game_info['short_description']
        cover_url = game_info['header_image']
        if cover_url:
            uploads_folder = './uploads'
            os.makedirs(uploads_folder, exist_ok=True)
            image_filepath = download_and_save_image(cover_url, uploads_folder, app_id)

            if image_filepath:
                st.warning(f"The cover image has been saved to: {image_filepath}")
            else:
                st.warning("Failed to save the cover image.")

        else:
            st.warning("Cover image not found.")

        return name, description, image_filepath
    else:
        st.warning("App ID not found in the URL.")
