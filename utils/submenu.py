import streamlit as st
from utils.christmass import kerstlan_countdown
from streamlit_authenticator import Authenticate

def generate_subment_extras():
    authenticate:Authenticate = st.session_state.authenticate
    kerstlan_countdown()
    st.sidebar.write(f'Welcome *{str.capitalize(st.session_state["name"])}*')
    st.sidebar.divider()
    authenticate.logout('Logout', key='unique_key', location="sidebar")