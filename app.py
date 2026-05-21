import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Air Fare Home", layout="centered")

# Background color
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)
# Local images (ensure these files exist in your app directory)
image_files = ["Pic1.jpg", "Pic2.jpg", "Pic3.jpg"]

existing_images = [img for img in image_files if os.path.exists(img)]
if not existing_images:
    st.error("No images found! Please check your image file names and ensure they are in the same folder as app.py")
else:
    # Auto refresh every 3 seconds (3000 milliseconds)
    count = st_autorefresh(interval=3000, limit=None, key="auto_refresh")

    # Cycle through images using count % number_of_images
    img_index = count % len(existing_images)

    st.image(existing_images[img_index], use_column_width=True)

# Animated welcome message (same as before)
st.markdown("""
    <h2 style="text-align:center; margin-top: 30px;">
        <span style="color:green; font-size: 36px;">
         Welcome to the AIR FARE!
        </span><br>
        <span style="color:#ff4b4b; font-size: 36px;">
         Customize your travel!
        </span>
    </h2>

    <style>
    h2 span {
        animation: fadeIn 2s ease-in-out infinite alternate;
    }

    # @keyframes fadeIn {
    #     from { opacity: 0.4; }
    #     to { opacity: 1; }
    # }
    </style>
""", unsafe_allow_html=True)

st.markdown("---")

# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Check Prices"):
        st.experimental_set_query_params(page="./pages/Journey_Fare")
        st.experimental_rerun()

with col2:
    if st.button("Routes and Price trends"):
        st.experimental_set_query_params(page="./pages/Ai_Route and Analysis")
        st.experimental_rerun()

st.markdown("---")

# st.write("Use the buttons above to navigate between pages. Sidebar is no longer required!")


