import streamlit as st
from streamlit_authenticator import Authenticate

st.set_page_config(
        page_title="Account - Kerstlan",
        page_icon="🎅",
    )

from utils.login import write_auth, login
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
    authenticate:Authenticate = st.session_state.authenticate
    try:
        if authenticate.reset_password(st.session_state["username"], 'Change password'):
            st.success('Password modified successfully')
            write_auth()
    except Exception as e:
        st.error(e)

    try:
        if authenticate.update_user_details(st.session_state["username"], 'Update user details'):
            st.success('Entries updated successfully')
            write_auth()
    except Exception as e:
        st.error(e)

if __name__ == "__main__":
    if login():
        generate_subment_extras()
        page()