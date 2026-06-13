import streamlit as st

from utils.data_loader import load_clean_data
from utils.formatting import format_currency, format_number, insight_box


st.title("Project Overview")

df = load_clean_data()
if df.empty:
    st.warning("Clean dataset not found.")
    st.stop()

st.write(
    "This dashboard presents an end-to-end exploratory data analysis of the data job market. "
    "It follows the same analytical flow as the original notebook: data understanding, cleaning, "
    "feature engineering, visual analysis, trend discovery, and final recommendations."
)

st.subheader("Objectives")
st.write(
    "Recruiters, learners, and job seekers need a clear view of where demand and salary opportunities "
    "exist across the modern data job market. This project identifies high-demand domains, high-paying "
    "roles, experience-level effects, work model patterns, company-size trends, and global salary hubs."
)

st.info(
    "Disclaimer: This dataset is sourced from Kaggle and used only for portfolio project purposes. "
    "Please do not make career, hiring, salary, or business decisions based only on this analysis."
)

cols = st.columns(5)
cols[0].metric("Listings", format_number(len(df)))
cols[1].metric("Roles", format_number(df["job_title"].nunique()))
cols[2].metric("Domains", format_number(df["job_category"].nunique()))
cols[3].metric("Locations", format_number(df["company_location"].nunique()))
cols[4].metric("Median Salary", format_currency(df["salary_in_usd"].median()))

st.subheader("Dataset Summary")
st.dataframe(
    {
        "Feature": [
            "Time period",
            "Salary field used",
            "Primary grouping feature",
            "Experience levels",
            "Employment types",
            "Work models",
        ],
        "Value": [
            f"{df['work_year'].min()}-{df['work_year'].max()}",
            "salary_in_usd",
            "job_category",
            ", ".join(sorted(df["experience_level"].unique())),
            ", ".join(sorted(df["employment_type"].unique())),
            ", ".join(sorted(df["work_models"].unique())),
        ],
    },
    use_container_width=True,
    hide_index=True,
)

insight_box(
    "Navigation Guide",
    [
        "Data Understanding reviews shape, columns, missing values, duplicates, and category frequencies.",
        "Data Cleaning explains title standardization, job category creation, and salary outlier treatment.",
        "Domain Demand, Salary Analysis, Trends, and Work/Company pages recreate all notebook EDA charts.",
        "Final Insights preserves the original conclusion narrative from the notebook.",
    ],
)
