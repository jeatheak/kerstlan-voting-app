import streamlit as st
from datetime import datetime

year = 2024
day = 8
month = 1

def kerstlan_countdown(location='sidebar'):
    today = datetime.now()
    kerstlan_day = datetime(year, month, day)

    days_left = (kerstlan_day - today).days

    if location == 'sidebar':
        st.sidebar.header(f"Days Left: {days_left} 🎄🎅")
    else:
        st.header(f"Days Left: {days_left} 🎄🎅")