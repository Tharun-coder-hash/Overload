import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw
from auth import login_page, register_page, logout



# Handle Authentication
query_params = st.experimental_get_query_params()
current_page = query_params.get("page", ["login"])[0]
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if not st.session_state.logged_in:
    if current_page == "register":
        register_page()
    else:
        login_page()
    st.stop()

# Logout button
st.sidebar.button("Logout", on_click=logout)

# Set background image function
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

# Set background for the main page
set_background("https://static.vecteezy.com/system/resources/thumbnails/029/754/480/small/yellow-plastic-concrete-mixer-truck-toy-isolated-on-ink-background-construction-vechicle-truck-with-copy-space-for-banner-of-toy-store-photo.jpg")
def infer_image(image):
    api_url = "https://detect.roboflow.com/overloaded-detection/2"
    api_key = "AUriIUOQuEbHt8npqPyt"
    
    image = image.convert("RGB")
    image_np = np.array(image)
    _, img_encoded = cv2.imencode(".jpg", cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    response = requests.post(
        f"{api_url}?api_key={api_key}",
        files={"file": img_encoded.tobytes()}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("Detection Result:", result)  # Print detection result
        return result
    else:
        print("API Error", response.status_code, response.text)
        return None

def draw_boxes(image, detections):
    draw = ImageDraw.Draw(image)
    for detection in detections.get("predictions", []):
        x, y, width, height = detection["x"], detection["y"], detection["width"], detection["height"]
        score = detection["confidence"]
        label = detection["class"]
        
        x1, y1 = int(x - width / 2), int(y - height / 2)
        x2, y2 = int(x + width / 2), int(y + height / 2)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 10), f"{label}: {score:.2f}", fill="red")
    return image

def main():
    st.title("Object Detection with Bounding Boxes")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Detect Objects"):
            detections = infer_image(image)
            if detections:
                st.write("Detected Objects:")
                for detection in detections.get("predictions", []):
                    st.write(f"- {detection['class']} (Confidence: {detection['confidence']*100:.2f}%)")
                image_with_boxes = draw_boxes(image.copy(), detections)
                st.image(image_with_boxes, caption="Detection Results", use_column_width=True)
            else:
                st.error("Detection failed. Please try again.")

if __name__ == "__main__":
    main()