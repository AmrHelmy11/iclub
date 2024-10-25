import streamlit as st
import sqlite3
import pandas as pd
import os

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('data.db')  # Create or connect to the database
    return conn

# Function to create the table if it doesn't exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(name, email, age):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', (name, email, age))
    conn.commit()
    conn.close()

# Function to save data to a CSV file
def save_to_csv(data):
    # Check if the CSV file exists
    if os.path.exists('data.csv'):
        # If it exists, append the new data
        existing_data = pd.read_csv('data.csv')
        updated_data = pd.concat([existing_data, data], ignore_index=True)
        updated_data.to_csv('data.csv', index=False)
    else:
        # If it doesn't exist, create a new one
        data.to_csv('data.csv', index=False)

# Create the table
create_table()

# Streamlit form
st.title("Simple Data Entry Form")

with st.form(key='data_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Insert the data into the database
        insert_data(name, email, age)

        # Create a DataFrame from the input data
        data = pd.DataFrame({
            'Name': [name],
            'Email': [email],
            'Age': [age]
        })

        # Save the data to CSV
        save_to_csv(data)

        st.success("Data saved successfully!")
