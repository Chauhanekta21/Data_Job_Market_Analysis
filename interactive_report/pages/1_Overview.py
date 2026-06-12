import streamlit as st
from utils.data_loader import load_data
from utils.theme import PASTEL, apply_theme


st.set_page_config(page_title="Home", layout="wide")

# Apply Global Dashboard theme
apply_theme()


df = load_data()

st.markdown(
    f"<h1 style='text-align:center;color:{PASTEL['text']}'>📊 Data Job Market Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("---")

# safe column check
required = ["work_year", "job_category", "experience_level", "salary_in_usd"]

if not all(col in df.columns for col in required):
    st.error("CSV columns mismatch. Fix dataset.")
    st.stop()

# filters
year = st.selectbox("Year", ["All"] + sorted(df["work_year"].unique()))
category = st.selectbox("Category", ["All"] + sorted(df["job_category"].unique()))
exp = st.selectbox("Experience", ["All"] + sorted(df["experience_level"].unique()))

data = df.copy()

if year != "All":
    data = data[data["work_year"] == year]

if category != "All":
    data = data[data["job_category"] == category]

if exp != "All":
    data = data[data["experience_level"] == exp]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Jobs", len(data))
col2.metric("Median Salary", int(data["salary_in_usd"].median()))
col3.metric("Countries", data["company_location"].nunique())

st.write("---")
st.dataframe(data.head(10))