import streamlit as st
import json
import os
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user data from a JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.load(file)
    else:
        users = {}
    return users

# Save user data to a JSON file
def save_user(username, password):
    users = load_users()
    users[username] = hash_password(password)  # Save hashed password
    with open('users.json', 'w') as file:
        json.dump(users, file)

# Check if username exists and password matches
def login_user(username, password):
    users = load_users()
    hashed_password = hash_password(password)
    if username in users and users[username] == hashed_password:
        return True
    return False

# Streamlit registration page
def registration_page():
    st.title("Register")

    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        elif new_username in load_users():
            st.error("Username already exists!")
        else:
            save_user(new_username, new_password)
            st.success("User registered successfully! Please go to the login page.")

# Streamlit login page
def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password.")

# Main function
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Login", "Register"])

    if choice == "Register":
        registration_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
