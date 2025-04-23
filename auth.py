import streamlit as st
import json
import os

def load_users():
    USERS_FILE = "users.json"
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    USERS_FILE = "users.json"
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def login_page():
    set_background("https://thumbs.dreamstime.com/b/yellow-toy-jeep-wrangler-driving-miniature-sandy-beach-rocks-tropical-plants-against-vibrant-background-navigating-351974004.jpg")
    st.title("OVERLOAD VEHICLE DETECTION")
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    users = load_users()
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_set_query_params(page="main")
            st.rerun()
        else:
            st.error("Invalid username or password")
    if st.button("Go to Register"):
        st.experimental_set_query_params(page="register")
        st.rerun()

def register_page():
    set_background("https://t3.ftcdn.net/jpg/11/33/22/60/360_F_1133226095_xzpWz9qzrDS0oS6yLQGIyipeweNB9i8J.jpg")
    st.title("Register Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    users = load_users()
    if st.button("Register"):
        if new_username in users:
            st.error("Username already exists!")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("Registration successful! Please login.")
    if st.button("Back to Login"):
        st.experimental_set_query_params(page="login")
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_set_query_params(page="login")
    st.rerun()
