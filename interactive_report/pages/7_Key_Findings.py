import streamlit as st

from utils.theme import PASTEL, apply_theme

# Apply Global Dashboard theme
apply_theme()



# -------------------------
# PAGE TITLE
# -------------------------

st.title("📌 Key Findings & Summary")

st.markdown(
    """
    Final insights from the Data Job Market Analysis (2020–2024).
    """
)

st.write("---")


# -------------------------
# KEY FINDINGS
# -------------------------

findings = [
    "Data Science, Data Engineering, and Data Analysis dominate overall job demand.",

    "AI & Machine Learning roles offer high salary potential despite relatively moderate demand.",

    "Leadership and architecture positions provide premium compensation but have fewer openings.",

    "Data Analysis and BI roles have strong demand with comparatively lower salary levels.",

    "The USA, Canada, and several European regions lead global hiring opportunities.",

    "Medium and large companies generally provide competitive salaries and better career opportunities.",

    "On-site work remains the dominant model, while remote work continues to hold a significant share.",

    "Senior professionals are most frequently hired, whereas executive positions achieve the highest pay.",

    "Full-time employment dominates the market compared with contract and freelance roles.",

    "AI/ML growth and increasing data adoption indicate strong future demand for data professionals."
]


# -------------------------
# DISPLAY FINDINGS
# -------------------------

col1, col2 = st.columns(2)


for index, finding in enumerate(findings):

    with col1 if index % 2 == 0 else col2:
        st.info(finding)


st.write("---")


# -------------------------
# FINAL PROJECT MESSAGE
# -------------------------

st.success(
    """
    🚀 This dashboard provides a complete overview of global data job trends, 
    salary patterns, demand distribution, and workforce behavior from 2020 to 2024.
    """
)