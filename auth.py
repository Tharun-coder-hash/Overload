import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.exceptions import FirebaseError

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

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
    st.subheader("Login Page")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Input validation
        if not email or "@" not in email:
            st.warning("⚠️ Please enter a valid email address")
            return
        if len(password) < 6:
            st.warning("⚠️ Password must be at least 6 characters")
            return
            
        try:
            user = auth.get_user_by_email(email)
            st.session_state.logged_in = True
            st.session_state.email = email
            st.query_params.update({"page": "main"})
            st.rerun()
            
        except FirebaseError as e:
            error_msg = str(e).lower()
            if "user not found" in error_msg:
                st.error("❌ Email not registered. Please register first.")
            elif "invalid password" in error_msg:
                st.error("❌ Incorrect password. Please try again.")
            else:
                st.error(f"🔒 Login failed: {str(e)}")

def register_page():
    set_background("https://t3.ftcdn.net/jpg/11/33/22/60/360_F_1133226095_xzpWz9qzrDS0oS6yLQGIyipeweNB9i8J.jpg")
    st.title("Register Page")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        # Input validation
        if not email or "@" not in email:
            st.warning("⚠️ Please enter a valid email address")
            return
        if len(password) < 6:
            st.warning("⚠️ Password must be at least 6 characters")
            return
            
        try:
            auth.create_user(email=email, password=password)
            st.success("✅ Registration successful! Please login.")
            st.query_params.update({"page": "login"})
            st.rerun()
            
        except FirebaseError as e:
            error_msg = str(e).lower()
            if "email already exists" in error_msg:
                st.error("❌ Email already registered. Please login instead.")
            else:
                st.error(f"🚫 Registration failed: {str(e)}")

def logout():
    st.session_state.clear()
    st.query_params.update({"page": "login"})
    st.rerun()
