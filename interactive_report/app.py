import streamlit as st

from utils.data_loader import load_clean_data
from utils.formatting import format_currency, format_number


st.set_page_config(
    page_title="Data Job Market Analysis",
    page_icon="📊",
    layout="wide",
)


st.title("Data Job Market Analysis")
st.caption("An interactive Streamlit dashboard built from the original EDA notebook.")

df = load_clean_data()

if df.empty:
    st.warning("Dataset not found. Please place the cleaned CSV inside the data folder.")
    st.stop()

st.subheader("Project Overview")
st.write(
    "This dashboard explores data job market trends across roles, domains, "
    "salary levels, experience levels, work models, company sizes, and locations."
)

metric_cols = st.columns(4)
metric_cols[0].metric("Job Listings", format_number(len(df)))
metric_cols[1].metric("Job Roles", format_number(df["job_title"].nunique()))
metric_cols[2].metric("Data Domains", format_number(df["job_category"].nunique()))
metric_cols[3].metric("Median Salary", format_currency(df["salary_in_usd"].median()))

st.subheader("Navigation Guide")
st.write(
    "Use the sidebar pages to move through the full analytical journey: "
    "data understanding, cleaning, EDA, trends, insights, and conclusions."
)

st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)
