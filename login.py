from auth import login_page, register_page, logout
import streamlit as st

# Handle authentication state
query_params = st.query_params()
current_page = query_params.get("page", ["login"])[0]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""

if not st.session_state.logged_in:
    if current_page == "register":
        register_page()
    else:
        login_page()
    st.stop()

# Set background (same as your original)
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

set_background("https://img.freepik.com/free-photo/veggie-quinoa-bowl-cooking-recipe_53876-110662.jpg?semt=ais_hybrid")

# Logout button
st.sidebar.button("Logout", on_click=logout)
