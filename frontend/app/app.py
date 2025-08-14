import streamlit as st
from PIL import Image
import os
import base64  


def get_base64_image(image_file):
    with open(image_file, "rb") as img:
        return base64.b64encode(img.read()).decode()


# --- Page config ---
st.set_page_config(
    page_title="Med Bytes Prescription Checker",
    page_icon="💊",
    layout="centered"
)


# --- Custom CSS for nicer styling ---
bg_image = get_base64_image("bg.jpg")  # Make sure bg.jpeg is in the same folder as app.py

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                          url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .css-18e3th9 {{
        background: transparent;
    }}
    .stTextInput>div>div>input {{
        height: 40px;
        font-size: 20px;
    }}
    .stButton>button {{
        background-color: #A3C1F7;
        color: white;
        font-size: 16px;
        height: 40px;
        width: 100%;
        border-radius: 8px;
    }}
    .stFileUploader>div>div {{
        border: 2px dashed #d1d5db;
        border-radius: 8px;
        padding: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)











# --- Title & Subtitle ---
st.markdown("## 👤 Patient Information")
st.markdown("Provide patient details for age-appropriate dosage verification")

# --- Patient Age Input ---
age = st.text_input("Patient Age *", placeholder="Enter age")

# --- Prescription Text Input or Manual Entry ---
input_mode = st.radio("", ["Text Input", "Manual Entry"], horizontal=True)
if input_mode == "Text Input":
    prescription_text = st.text_area(
        "Prescription Text",
        placeholder="Paste prescription text here or upload an image/document..."
    )
else:
    prescription_text = ""  # Manual entry logic can be added here

# --- File uploader for prescription images ---
uploaded_file = st.file_uploader(
    "Drag and drop prescription image or click to upload",
    type=["png", "jpg", "jpeg", "pdf"]
)

# --- Analyze button ---
st.button("Analyze Prescription")
