import streamlit as st

from utils.charts import bar_chart, horizontal_bar_chart, scatter_chart
from utils.data_loader import load_clean_data
from utils.formatting import insight_box


st.title("Salary Analysis")
st.write(
    "This page recreates EDA sections 03, 04, and 05: domain salary comparison, "
    "highest-paying roles, and demand versus salary."
)

df = load_clean_data()
if df.empty:
    st.warning("Clean dataset not found.")
    st.stop()

st.subheader("EDA Section 03: Salary Comparison Across Data Domains")
salary_by_domain = (
    df.groupby("job_category")["salary_in_usd"]
    .median()
    .reset_index(name="median_salary_usd")
    .sort_values("median_salary_usd", ascending=False)
)
fig = bar_chart(
    salary_by_domain,
    x="job_category",
    y="median_salary_usd",
    text="median_salary_usd",
    title="Median Salary (USD) Across Data Domains",
    labels={"job_category": "Data Domain", "median_salary_usd": "Median Salary (USD)"},
)
fig.update_traces(
    texttemplate="$%{y:,.0f}",
    hovertemplate="Data Domain: %{x}<br>Median Salary: $%{y:,.0f}<extra></extra>",
)
st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 03",
    [
        "Machine Learning & AI offers the highest median salary, making it the highest-paying domain.",
        "Leadership & Management and Data Architecture also offer high salaries, showing strong pay for senior and specialized roles.",
        "Data Analysis and Business Intelligence have the lowest salaries despite high demand, showing that demand does not always mean high pay.",
    ],
)

st.subheader("EDA Section 04: Top 10 Highest-Paying Job Roles")
top_n = st.slider("Number of roles", min_value=5, max_value=20, value=10)
top_roles = (
    df.groupby("job_title")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index(name="median_salary")
)
fig = horizontal_bar_chart(
    top_roles,
    x="median_salary",
    y="job_title",
    text="median_salary",
    title=f"Top {top_n} Highest Paying Job Roles by Median Salary",
    labels={"job_title": "Job Role", "median_salary": "Median Salary (USD)"},
)
fig.update_traces(
    texttemplate="$%{x:,.0f}",
    hovertemplate="Job Role: %{y}<br>Median Salary: $%{x:,.0f}<extra></extra>",
)
st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 04",
    [
        "Highest salaries are concentrated in senior leadership roles such as Managers, Directors, and Heads.",
        "Specialized architecture roles including AI, Cloud, AWS, and Data Architect also pay very high salaries.",
        "Entry-level and general roles are not present in the top 10, showing salary is driven by experience and specialization.",
    ],
)

st.subheader("EDA Section 05: Demand vs Salary Across Data Domains")
domain_analysis = (
    df.groupby("job_category")
    .agg(median_salary_usd=("salary_in_usd", "median"), job_listing_count=("salary_in_usd", "count"))
    .reset_index()
    .sort_values("median_salary_usd", ascending=False)
)
fig = scatter_chart(
    domain_analysis,
    x="job_listing_count",
    y="median_salary_usd",
    text="job_category",
    title="Demand vs Salary Across Data Domains",
    labels={"job_listing_count": "Number of Job Listings", "median_salary_usd": "Median Salary (USD)"},
)
fig.update_traces(
    hovertemplate="Data Domain: %{text}<br>Job Listings: %{x:,}<br>Median Salary: $%{y:,.0f}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 05",
    [
        "Machine Learning & AI offers the highest salary despite moderate job demand, making it a high-value niche domain.",
        "Data Science and Data Engineering have high demand but moderate salaries.",
        "Data Analysis and Business Intelligence have high demand but the lowest salaries.",
        "Leadership & Management and Data Architecture show lower demand but strong salaries.",
        "The best opportunities exist in domains that balance specialization with experience-driven roles.",
    ],
)
