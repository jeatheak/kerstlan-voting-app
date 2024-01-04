import streamlit as st

st.set_page_config(
        page_title="Access - Kerstlan",
        page_icon="🎅",
    )

from database.database import add_riddle_answer, add_riddle_hint, get_riddles
from utils.login import getUsername, login
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
    riddles = get_riddles()
    st.header(f"Access Riddle{'s' if len(riddles) > 1 else ''}")

    count = 0
    for riddle in riddles:
        if str.lower(riddle[6]) == getUsername():
            count += 1
            st.subheader(f'{count}. {riddle[1]}')
            if riddle[7] == 0:
                st.write(riddle[2])
                if riddle[5] == 0 and st.button("Show Hint", key=f"{riddle[0]}_hint_btn"):
                    add_riddle_hint(riddle[0], riddle[5])
                    st.rerun()
                if riddle[5] > 0:
                    st.code(riddle[3])
                answer = st.text_input('Answer', key=f'{riddle[0]}_answer')
                if st.button('Send', key=f'{riddle[0]}_send'):
                    if str.lower(riddle[4]) in str.lower(answer):
                        add_riddle_answer(riddle[0])
                        st.rerun()
                    else:
                        if riddle[5] > 0:
                            st.error('Wrong Answer even after a HINT 🔥💀🔥')
                        else:
                            st.error('Wrong Answer try again!!! 🔥')
            else:
                st.success(f"Solved: {riddle[1]}")
    
    if count == 0:
        st.subheader('No riddles to solve!')
            
   
if __name__ == "__main__":
    if login():
        generate_subment_extras()
        page()