import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json
import os

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["gcp_service_account"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("Milk Records").sheet1  # Replace with your Google Sheet name

# Convert the sheet to a DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit app
st.title("Daily Milk Records")
st.write("Manage your daily milk records:")

# Input field for milk quantity (default value: 3Kg)
default_milk_quantity = st.number_input("Milk (Kg)", value=3.0)

# Get current date, month, and year
now = datetime.now()
date, month, year = now.day, now.month, now.year

# Display current date, month, and year
st.write(f"Date: {date}, Month: {month}, Year: {year}")

# Submit button to add a new record
if st.button("Submit"):
    df = df.append({"Date": date, "Month": month, "Year": year, "Milk (Kg)": default_milk_quantity}, ignore_index=True)
    sheet.append_row([date, month, year, default_milk_quantity])
    st.success("Record added successfully!")

# Display the records
st.write("Existing Records:")
st.dataframe(df)

# Additional functionalities like Search, Update, Delete, etc.
# You can add these functionalities following the example provided above
