import streamlit as st
import requests

# Set the app title 
st.title('My First Doa Ibu !!')

# Add a welcome message 
st.write('Welcome to Dunia!')

# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')

# Display the customized message 
st.write('Customized Message:', widgetuser_input)

# API call to get exchange rates with MYR as base
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

if response.status_code == 200:
    data = response.json()
    rates = data.get('rates', {})
    
    # Create a dropdown to select target currency
    currency_list = sorted(rates.keys())  # Sort for nicer dropdown
    selected_currency = st.selectbox('Choose target currency:', currency_list)
    
    # Display the selected exchange rate
    exchange_rate = rates.get(selected_currency)
    st.write(f"1 MYR = {exchange_rate} {selected_currency}")
    
    # Optionally show the full JSON (toggle)
    if st.checkbox("Show all rates (JSON format)"):
        st.json(data)
else:
    st.error(f"API call failed with status code: {response.status_code}")



