import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Directly use the secret dictionary
creds_dict = st.secrets["gcp_service_account"]
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
    # Append the entry to the DataFrame and Google Sheets
    df = df.append({"Date": date, "Month": month, "Year": year, "Milk (Kg)": default_milk_quantity}, ignore_index=True)
    sheet.append_row([date, month, year, default_milk_quantity])
    st.success("Record added successfully!")

# Display the records
st.write("Existing Records:")
st.dataframe(df)

# Search functionality
st.write("Search Records")
search_date = st.number_input("Search by Date (optional)", min_value=1, max_value=31, step=1)
search_month = st.number_input("Search by Month (optional)", min_value=1, max_value=12, step=1)
search_year = st.number_input("Search by Year (optional)", min_value=2000, max_value=2100, step=1)

# Filter the DataFrame based on search criteria
filtered_df = df.copy()

if search_date:
    filtered_df = filtered_df[filtered_df['Date'] == search_date]
if search_month:
    filtered_df = filtered_df[filtered_df['Month'] == search_month]
if search_year:
    filtered_df = filtered_df[filtered_df['Year'] == search_year]

st.write("Filtered Records:")
st.dataframe(filtered_df)

# Select a record to update
if not filtered_df.empty:
    st.write("Update or Delete a Record")
    selected_index = st.selectbox("Select Record to Update/Delete:", filtered_df.index)
    selected_record = filtered_df.loc[selected_index]

    # Display selected record details
    st.write("Selected Record:")
    st.write(f"Date: {selected_record['Date']}, Month: {selected_record['Month']}, Year: {selected_record['Year']}, Milk (Kg): {selected_record['Milk (Kg)']}")

    # Update fields
    updated_milk_quantity = st.number_input("Update Milk (Kg)", value=selected_record['Milk (Kg)'])

    # Buttons to update or delete the selected record
    if st.button("Update Record"):
        df.at[selected_index, 'Milk (Kg)'] = updated_milk_quantity
        sheet.update_cell(selected_index + 2, 4, updated_milk_quantity)  # Google Sheets rows are 1-indexed
        st.success("Record updated successfully!")

    if st.button("Delete Record"):
        df = df.drop(selected_index).reset_index(drop=True)
        sheet.delete_row(selected_index + 2)  # Google Sheets rows are 1-indexed
        st.success("Record deleted successfully!")

# Display all existing records
st.write("All Existing Records:")
st.dataframe(df)
