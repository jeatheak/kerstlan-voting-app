import streamlit as st
import yaml
import os
import shutil
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
from config import AppName, config_path, admin_user
from database.database import get_games
from utils.calc import calculate_total_rating_for_game, get_voted_users
from utils.christmass import christmas_countdown
from utils.login import login
from utils.steam import extract_app_id


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

def generate_subment_extras():
    christmas_countdown()
    st.sidebar.write(f'Welcome *{str.capitalize(st.session_state["name"])}*')
    st.sidebar.divider()
    authenticator.logout('Logout', key='unique_key', location="sidebar")

def page():
    games = get_games()
    st.header(f"{len(games)} Games Total 🕹️🎮", divider='rainbow')
    new_games = list()

    for game in games:
        game = list(game)
        game.append(calculate_total_rating_for_game(game[0]))
        new_games.append(game)
        
    new_games.sort(key=game_sort,reverse=True)
    ranking = 1
    for game in new_games:
        ranking_icons = {1: '👑', 2: '🥈', 3: '🥉'}
        icon = ranking_icons.get(ranking, f'{ranking}.')
        st.subheader(f'{icon} {game[1]}')

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

def game_sort(e):
    return e[5]

if __name__ == "__main__":
    if login():
        generate_subment_extras()
        page()