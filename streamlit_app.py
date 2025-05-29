import streamlit as st
import requests
from datetime import datetime

# ------------------ Tajuk & Selamat Datang ------------------ #
st.title('My First Bismillah !!')
st.write('Welcome to mobile legend!')

# Input mesej pengguna
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('Customized Message:', widgetuser_input)

# ------------------ Kadar Tukaran Mata Wang ------------------ #
st.subheader("💱 Currency Exchange Rate (MYR)")

response = requests.get('https://api.vatcomply.com/rates?base=MYR')
if response.status_code == 200:
    data = response.json()
    rates = data.get('rates', {})
    currency_list = sorted(rates.keys())
    selected_currency = st.selectbox('Choose target currency:', currency_list)
    exchange_rate = rates.get(selected_currency)
    st.write(f"1 MYR = {exchange_rate} {selected_currency}")

    if st.checkbox("Show all rates (JSON format)"):
        st.json(data)
else:
    st.error(f"API call failed with status code: {response.status_code}")

# ------------------ Waktu Azan Mengikut Negeri ------------------ #
st.subheader("🕌 Waktu Azan Mengikut Negeri di Malaysia")

# Senarai negeri & koordinat (lat, lon)
negeri_coords = {
    "Johor": (1.4854, 103.7615),
    "Kedah": (6.1184, 100.3685),
    "Kelantan": (6.1254, 102.2381),
    "Melaka": (2.1896, 102.2501),
    "Negeri Sembilan": (2.7258, 101.9424),
    "Pahang": (3.8126, 103.3256),
    "Perak": (4.5998, 101.0901),
    "Perlis": (6.4441, 100.2043),
    "Pulau Pinang": (5.4164, 100.3327),
    "Sabah": (5.9804, 116.0735),
    "Sarawak": (1.5533, 110.3592),
    "Selangor": (3.0738, 101.5183),
    "Terengganu": (5.3117, 103.1324),
    "Kuala Lumpur": (3.1390, 101.6869),
    "Labuan": (5.2831, 115.2308),
    "Putrajaya": (2.9264, 101.6964),
}

# Pilih negeri
selected_negeri = st.selectbox("Pilih negeri untuk waktu azan:", list(negeri_coords.keys()))
lat, lon = negeri_coords[selected_negeri]

# Dapatkan tarikh hari ini
today = datetime.now().strftime('%Y-%m-%d')

# Panggil API waktu solat
azan_api_url = f'https://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=9'
azan_response = requests.get(azan_api_url)

if azan_response.status_code == 200:
    azan_data = azan_response.json()
    timings = azan_data['data']['timings']
    st.write(f"**Waktu Azan ({selected_negeri}) - {today}**")
    for prayer, time in timings.items():
        st.write(f"{prayer}: {time}")
else:
    st.error("Gagal dapatkan waktu azan.")

