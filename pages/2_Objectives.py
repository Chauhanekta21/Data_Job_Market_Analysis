import streamlit as st
from utils.theme import PASTEL


# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("🎯 Project Objectives")

st.markdown(
    "Understand the key goals behind this Data Job Market Analysis project."
)

st.write("---")


# -----------------------------
# OBJECTIVES DATA
# -----------------------------

objectives = [
    "📊 Analyze job distribution across different data domains",
    "💰 Compare salary trends across roles and experience levels",
    "🌍 Explore global hiring patterns and locations",
    "🏢 Study company size and employment trends",
    "🏠 Understand remote, hybrid, and on-site work models",
    "📈 Identify the relationship between job demand and salary"
]


# -----------------------------
# DISPLAY OBJECTIVES AS CARDS
# -----------------------------

col1, col2 = st.columns(2)

for i, obj in enumerate(objectives):

    with [col1, col2][i % 2]:
        st.markdown(
            f"""
            <div style="
                background-color: {PASTEL['very_light']};
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 15px;
                color: {PASTEL['text']};
                font-size: 16px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            ">
                {obj}
            </div>
            """,
            unsafe_allow_html=True
        )