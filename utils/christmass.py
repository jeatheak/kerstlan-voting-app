import streamlit as st
from datetime import datetime

year = 2024
day = 5
month = 1

hour = 12

def kerstlan_countdown(location='sidebar'):
    today = datetime.now()
    kerstlan_day = datetime(year, month, day, hour)

    days_left = (kerstlan_day - today).days

    if days_left == 0:
        hours_left = (kerstlan_day - today).seconds / 3600
        if hours_left < 1:
            hours_left = 0
        left_text = f"Hours Left: {round(hours_left)} 🎄🎅"

    else:
        if days_left < 0:
            days_left = 0
        left_text = f"Days Left: {days_left} 🎄🎅"

    if location == 'sidebar':
        st.sidebar.header(left_text)
    else:
        st.header(left_text)