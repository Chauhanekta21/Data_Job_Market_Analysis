import streamlit as st
from utils.theme import PASTEL

st.set_page_config(
    page_title="Data Job Market Dashboard",
    layout="wide"
)

st.title("📊 Data Job Market Analysis Dashboard")

st.markdown(
    f"<p style='color:{PASTEL['text']}'>Use sidebar to navigate pages</p>",
    unsafe_allow_html=True
)