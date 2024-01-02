import streamlit as st

st.set_page_config(
        page_title="List Games - Kerstlan",
        page_icon="🎅",
    )

from database.database import get_games, get_user_ratings_for_game
from utils.calc import calculate_total_rating_for_game, get_voted_users
from utils.login import login
from utils.steam import extract_app_id
from utils.submenu import generate_subment_extras
import pandas as pd
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
        st.subheader(f'{icon} {game[1]}',anchor=f'{game[0]}')

        image_path = game[4]
        if image_path:
            st.image(image_path, use_column_width=False, width=300)

        st.write(game[2])
        app_id = extract_app_id(game[3])
        st.markdown(f"Store: [Steam Website]({game[3]}) | [Steam Desktop](steam://store/{app_id})")

        total_rating = game[5]
        st.subheader(f"Total Rating: {total_rating}")
        users_voted = get_user_ratings_for_game(game[0])
        st.write('Users voted: ' + (','.join([vote[0] for vote in users_voted]) if len(users_voted) > 0 else '0'))
        with st.expander("Votes per User"):
            ratings = users_voted
            chart_data = pd.DataFrame([rating[1] for rating in ratings],[rating[0] for rating in ratings] , columns=["rating"])
            st.bar_chart(chart_data)
        st.divider()
        ranking += 1

def game_sort(e):
    return e[5]

if __name__ == "__main__":
    if login():
        generate_subment_extras()
        page()