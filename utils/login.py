import streamlit as st
import yaml
import os
import shutil
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
from config import AppName, config_path, admin_user
from database.database import create_tables
from utils.email_utils import email_forgot_password, email_forgot_username

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

def write_auth():
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def login() -> bool:
    create_tables()

    st.title(AppName)
    

    if 'forgot_pwd' not in st.session_state:
        st.session_state.forgot_pwd = False

    if 'forgot_user' not in st.session_state:
        st.session_state.forgot_user = False

    if 'register_user' not in st.session_state:
        st.session_state.register_user = False

    if 'choice' not in st.session_state:
        st.session_state.choice = 'List Games'

    authenticator.login('Login', 'main') 
    isLoggedIn = st.session_state.authentication_status
    if isLoggedIn is None or isLoggedIn is False:
        if isLoggedIn is False:
            st.error('Username/password is incorrect')

        if not st.session_state.forgot_pwd and not st.session_state.forgot_user and not st.session_state.register_user:
            if st.session_state.authentication_status:
                st.rerun()
            forgot_col1, forgot_col2, forgot_col3 = st.columns([1,1,2])
            with forgot_col1:
                if st.button('Forgot password'):
                    st.session_state.forgot_pwd = True
                    st.rerun()
            with forgot_col2:
                if st.button('Forgot username'):
                    st.session_state.forgot_user = True
                    st.rerun()
            with forgot_col3:
                if st.button('Register'):
                    st.session_state.register_user = True
                    st.rerun()
        elif st.session_state.forgot_pwd:
            try:
                username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
                if username_of_forgotten_password:
                    email_forgot_password(email_of_forgotten_password, new_random_password, username_of_forgotten_password)
                    write_auth()
                    st.success(f"Send newly generated password to email of {username_of_forgotten_password}")
                elif username_of_forgotten_password == False:
                    st.error('Username not found')
                if st.button('Back','forgot_pwd_btn_back'):
                    st.session_state.forgot_pwd = False
                    st.rerun()
            except Exception as e:
                st.error(e)     
        elif st.session_state.register_user:
            try:
                if authenticator.register_user('Register user', preauthorization=False):
                    write_auth()
                    st.success('User registered successfully')
                if st.button('Back','register_user_btn_back'):
                    st.session_state.register_user = False
                    st.rerun()
            except Exception as e:
                st.error(e)  
        elif st.session_state.forgot_user:
            try:
                username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
                if username_of_forgotten_username:
                    email_forgot_username(email_of_forgotten_username, username_of_forgotten_username)
                    write_auth()
                    st.success(f"Send username to: {email_of_forgotten_username}")
                elif username_of_forgotten_username == False:
                    st.error('Email not found')
                if st.button('Back','forgot_user_btn_back'):
                    st.session_state.forgot_user = False
                    st.rerun()
            except Exception as e:
                st.error(e)
        return False
    else:
        return True