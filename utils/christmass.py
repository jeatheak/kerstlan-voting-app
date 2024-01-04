import streamlit as st
from datetime import datetime

year = 2024
day = 5
month = 1

hour = 12

def kerstlan_countdown(location='sidebar'):
    today = datetime.now()
    kerstlan_day = datetime(year, month, day, hour-1)

    days_left = (kerstlan_day - today).days

    if days_left == 0:
        time_left = kerstlan_day - today
        hours_left = time_left.total_seconds() // 3600
        minutes_left = (time_left.total_seconds() // 60) % 60
        seconds_left = time_left.total_seconds() % 60

        if hours_left < 1:
            hours_left = 0
        left_text = f"Time Left: {int(hours_left):02d}h {int(minutes_left):02d}m {int(seconds_left):02d}s 🎄🎅"

    else:
        if days_left < 0:
            days_left = 0
        left_text = f"Days Left: {days_left} 🎄🎅"

    if location == 'sidebar':
        st.sidebar.header(left_text)
    else:
        st.header(left_text)