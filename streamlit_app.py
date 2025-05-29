import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set app title
st.title('🕌 Prayer Times by Location')

# Input fields
city = st.text_input('Enter City:', 'Kuala Lumpur')
country = st.text_input('Enter Country:', 'Malaysia')
date_input = st.date_input('Select a Date (optional):', datetime.now())

# Convert date to required format
date_str = date_input.strftime('%d-%m-%Y')

# API call
url = f'https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=3&date={date_str}'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    timings = data['data']['timings']
    
    st.subheader('🕰️ Prayer Times')
    
    # Filter only the 5 daily prayers
    prayer_times = {key: timings[key] for key in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']}
    st.table(prayer_times)

    # Convert times to datetime for duration calculation
    prayer_times_dt = {
        k: datetime.strptime(v.split(' ')[0], '%H:%M') for k, v in prayer_times.items()
    }
    
    # Calculate gaps between prayers
    prayer_names = list(prayer_times_dt.keys())
    gaps = []
    for i in range(len(prayer_names) - 1):
        delta = (prayer_times_dt[prayer_names[i+1]] - prayer_times_dt[prayer_names[i]]).seconds / 3600
        gaps.append(delta)
    gaps.append(24 - sum(gaps))  # Time from Isha to next Fajr

    # Pie chart
    st.subheader('⏱️ Time Gaps Between Prayers')
    fig = px.pie(
        values=gaps,
        names=[f"{prayer_names[i]} ➝ {prayer_names[i+1]}" if i < len(prayer_names)-1 else f"Isha ➝ Fajr (next day)"
               for i in range(len(prayer_names))],
        title='Time Gaps Between Each Prayer (in hours)'
    )
    st.plotly_chart(fig)

else:
    st.error(f"Failed to get data. Status code: {response.status_code}")

else:
    st.error(f"API call failed with status code: {response.status_code}")



