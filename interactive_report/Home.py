import streamlit as st
from utils.theme import PASTEL

# Configure Streamlit page settings (title, layout, browser tab name)
st.set_page_config(
    page_title="Data Job Market Dashboard",
    layout="wide"
)

# Display main dashboard title
st.title("📊 Data Job Market Analysis Dashboard")

# Display a styled instruction message using custom theme colors
st.markdown(
    f"<p style='color:{PASTEL['text']}'>Use sidebar to navigate pages</p>",
    unsafe_allow_html=True
)