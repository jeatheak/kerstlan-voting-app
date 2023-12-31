import streamlit as st

st.set_page_config(
        page_title="Vote - Kertlan",
        page_icon="🎅",
    )

from database.database import get_games, add_user_rating, update_user_rating, has_user_voted
from utils.calc import calculate_total_rating_for_game
from utils.login import login
from utils.steam import extract_app_id
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

if __name__ == "__main__":
    if login():
        generate_subment_extras()
        page()