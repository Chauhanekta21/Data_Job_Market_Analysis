import streamlit as st

from utils.data_loader import load_clean_data
from utils.formatting import format_currency, format_number


st.set_page_config(
    page_title="Data Job Market Analysis",
    page_icon=":bar_chart:",
    layout="wide",
)

st.sidebar.success("Choose a page above to explore the analysis.")

st.title("Data Job Market Analysis")
st.caption("A portfolio-level Streamlit dashboard transformed from the original EDA notebook.")

df = load_clean_data()

if df.empty:
    st.warning("Dataset not found. Please place data_science_salaries_clean.csv inside the data folder.")
    st.stop()

st.write(
    "This project analyzes the data job market from 2020 to 2024 across job domains, "
    "salary levels, experience levels, work models, company sizes, and company locations."
)

metric_cols = st.columns(4)
metric_cols[0].metric("Job Listings", format_number(len(df)))
metric_cols[1].metric("Job Roles", format_number(df["job_title"].nunique()))
metric_cols[2].metric("Data Domains", format_number(df["job_category"].nunique()))
metric_cols[3].metric("Median Salary", format_currency(df["salary_in_usd"].median()))

st.divider()

left, right = st.columns([1.1, 0.9])

with left:
    st.subheader("Objectives")
    st.write(
        "Understand which data domains, job roles, experience levels, work models, "
        "company sizes, and locations offer the strongest opportunities in terms of "
        "job demand and compensation."
    )

    st.info(
        "Disclaimer: This dataset is sourced from Kaggle and used only for portfolio "
        "project purposes. Please do not make career, hiring, salary, or business "
        "decisions based only on this analysis."
    )

    st.subheader("Analytical Journey")
    st.markdown(
        """
        1. Understand the dataset structure and quality.
        2. Review cleaning, job title standardization, and feature engineering.
        3. Analyze demand across data domains and roles.
        4. Compare salary patterns across domains, roles, experience, work model, and company size.
        5. Study demand and salary trends from 2020 to 2024.
        6. Summarize key findings and final recommendations.
        """
    )

with right:
    st.subheader("Dataset Summary")
    summary = {
        "Rows": format_number(len(df)),
        "Columns": format_number(df.shape[1]),
        "Years Covered": f"{df['work_year'].min()}-{df['work_year'].max()}",
        "Company Locations": format_number(df["company_location"].nunique()),
        "Work Models": format_number(df["work_models"].nunique()),
        "Experience Levels": format_number(df["experience_level"].nunique()),
    }
    st.dataframe(summary, use_container_width=True)

st.subheader("Preview")
st.dataframe(df.head(10), use_container_width=True, hide_index=True)
