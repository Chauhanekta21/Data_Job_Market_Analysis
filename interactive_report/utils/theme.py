import streamlit as st


# -----------------------------
# DASHBOARD COLOR THEME
# -----------------------------

PASTEL = {
    # Main brand colors
    "primary": "#52799C",
    "dark_blue": "#2F5D7C",
    "light": "#A9C4D9",
    "very_light": "#DCEAF5",

    # Backgrounds
    "background": "#EAF6FF",
    "card_bg": "#FFFFFF",

    # Text
    "text": "#2B2B2B",
    "text_secondary": "#666666",

    # Effects
    "shadow": "rgba(0,0,0,0.08)"
}


# -----------------------------
# APPLY GLOBAL DASHBOARD THEME
# -----------------------------

def apply_theme():
    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background-color: #EAF6FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )