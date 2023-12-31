import streamlit as st
from config import AppName
from streamlit_authenticator import Authenticate
from utils.calc import calculate_total_rating_for_game
from utils.login import config, init_auth
from database.database import create_tables, get_games
import pandas as pd
import numpy as np

st.set_page_config(
        page_title="Home - Kertlan",
        page_icon="🎅",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "# 🎅 Made by [Jeatheak](https://github.com/jeatheak)\nA simple voting app to choose a game to play on our (kerst)Lan party!\n ## Happy Christmass 🎄"
        }
    )

from utils.login import login
from utils.christmass import kerstlan_countdown
from utils.submenu import generate_subment_extras

authenticate = Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )

st.session_state.authenticate = authenticate

def page():
    kerstlan_countdown(location='main')
    st.write('HoHo Welcome to the Kerstlan voting app!')
    st.write('To Vote, see Game details, Add new games or Manage your account use the sidebar on the left.')
    st.subheader('Current Ranking:')
    print_game_table()

def game_sort(e):
    return e[5]

def get_rank(game, games):
    ranking = games.index(game) + 1
    ranking_icons = {1: '👑', 2: '🥈', 3: '🥉'}
    return ranking_icons.get(ranking, f'{ranking}')

def get_game_name(game):
    # return f'[{game[1]}]({game[3]})'
    # return f'<a href="{game[3]}">{game[1]}</a>'
    return game[1]

def print_game_table():
    games = get_games()
    new_games = list()

    for game in games:
        game = list(game)
        game.append(calculate_total_rating_for_game(game[0]))
        new_games.append(game)
        
    new_games.sort(key=game_sort,reverse=True)
        
    chart_data = pd.DataFrame([[get_rank(game,new_games),get_game_name(game),round(game[5],1)] for game in new_games], columns=["Rank","Name", "Rating"])
    st.dataframe(chart_data, hide_index=True, height=(len(new_games) + 1) * 35 + 3,column_config={
        "Rating": st.column_config.NumberColumn(
            "Rating", help="Shows total Rating of the game"
        ),
        "Name": st.column_config.TextColumn('Steam Link')
    })

if __name__ == "__main__":    
    create_tables()

    if login():        
        generate_subment_extras()
        page()
