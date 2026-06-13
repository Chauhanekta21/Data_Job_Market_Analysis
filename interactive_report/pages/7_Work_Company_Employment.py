import streamlit as st

from utils.charts import bar_chart, grouped_bar_chart, pie_chart
from utils.data_loader import load_clean_data
from utils.formatting import insight_box


st.title("Work, Company & Employment Analysis")
st.write(
    "This page recreates EDA sections 08 to 16: experience-level demand and salary, "
    "work models, company locations, company size, and employment type."
)

df = load_clean_data()
if df.empty:
    st.warning("Clean dataset not found.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Experience", "Work Models", "Company & Location", "Employment Type"]
)

with tab1:
    st.subheader("EDA Section 08: Job Demand Across Experience Levels")
    demand = (
        df.groupby("experience_level")
        .size()
        .reset_index(name="job_listing_count")
        .sort_values("job_listing_count", ascending=False)
    )
    fig = bar_chart(
        demand,
        x="experience_level",
        y="job_listing_count",
        text="job_listing_count",
        title="Job Demand Across Experience Levels",
        labels={"experience_level": "Experience Level", "job_listing_count": "Number of Job Listings"},
    )
    fig.update_traces(
        hovertemplate="Experience Level: %{x}<br>Job Listings: %{y:,}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Key Insights of EDA Section 08",
        [
            "Senior-level roles dominate job demand with 4103 listings.",
            "Mid-level roles follow with 1668 listings.",
            "Entry-level and Executive-level roles have much lower demand.",
        ],
    )

    st.subheader("EDA Section 09: Salary Distribution Across Experience Levels")
    salary = (
        df.groupby("experience_level")["salary_in_usd"]
        .median()
        .reset_index(name="median_salary")
        .sort_values("median_salary", ascending=False)
    )
    fig = bar_chart(
        salary,
        x="experience_level",
        y="median_salary",
        text="median_salary",
        title="Median Salary Across Experience Levels",
        labels={"experience_level": "Experience Level", "median_salary": "Median Salary (USD)"},
    )
    fig.update_traces(
        texttemplate="$%{y:,.0f}",
        hovertemplate="Experience Level: %{x}<br>Median Salary: $%{y:,.0f}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Relationship Insights: EDA Sections 08 & 09",
        [
            "Senior-level roles show the highest job demand along with strong salary levels.",
            "Executive-level roles have the highest salaries but the lowest demand.",
            "Mid-level roles maintain steady demand and salary growth.",
            "Entry-level roles have lower demand and the lowest salaries.",
            "Higher experience levels are associated with higher salaries, but not always with higher job demand.",
        ],
    )

with tab2:
    st.subheader("EDA Section 10: Distribution of Work Models")
    work_model_distribution = (
        (df["work_models"].value_counts(normalize=True) * 100)
        .round(2)
        .reset_index()
    )
    work_model_distribution.columns = ["work_model", "percentage"]
    fig = pie_chart(
        work_model_distribution,
        names="work_model",
        values="percentage",
        title="Distribution of Work Models in Data Jobs",
        labels={"work_model": "Work Model", "percentage": "Percentage"},
    )
    fig.update_traces(
        hovertemplate="Work Model: %{label}<br>Share: %{value:.2f}%<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Key Insights of EDA Section 10",
        [
            "On-site roles dominate the market at 57.75%.",
            "Remote roles are also strong at 38.83%.",
            "Hybrid roles are minimal at 3.41%, making it the least adopted work model.",
        ],
    )

    st.subheader("EDA Section 11: Work Model Preferences Across Data Domains")
    preferences = (
        df.groupby(["job_category", "work_models"])
        .size()
        .reset_index(name="work_model_count")
        .sort_values(["job_category", "work_model_count"], ascending=[True, False])
    )
    fig = grouped_bar_chart(
        preferences,
        x="job_category",
        y="work_model_count",
        color="work_models",
        title="Work Model Preferences Across Data Domains",
        labels={"job_category": "Data Domain", "work_model_count": "Number of Job Postings", "work_models": "Work Model"},
    )
    fig.update_traces(
        hovertemplate="Data Domain: %{x}<br>Job Postings: %{y:,}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("EDA Section 12: Median Salary by Work Model")
    work_salary = (
        df.groupby("work_models")["salary_in_usd"]
        .median()
        .reset_index(name="median_salary")
        .sort_values("median_salary", ascending=False)
    )
    fig = bar_chart(
        work_salary,
        x="work_models",
        y="median_salary",
        text="median_salary",
        title="Median Salary Across Work Models",
        labels={"work_models": "Work Model", "median_salary": "Median Salary (USD)"},
    )
    fig.update_traces(
        texttemplate="$%{y:,.0f}",
        hovertemplate="Work Model: %{x}<br>Median Salary: $%{y:,.0f}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Key Insights of EDA Sections 11 & 12",
        [
            "On-site work dominates across all data domains.",
            "Remote work is the second most common option and remains well-paid.",
            "Hybrid work is both the least adopted and lowest paying.",
        ],
    )

with tab3:
    st.subheader("EDA Section 13: Top Company Locations by Median Salary")
    top_locations = (
        df.groupby("company_location")["salary_in_usd"]
        .median()
        .reset_index(name="median_salary")
        .sort_values("median_salary", ascending=False)
        .head(10)
    )
    fig = bar_chart(
        top_locations,
        x="company_location",
        y="median_salary",
        text="median_salary",
        title="Top 10 Company Locations by Median Salary",
        labels={"company_location": "Company Location", "median_salary": "Median Salary (USD)"},
    )
    fig.update_traces(
        texttemplate="$%{y:,.0f}",
        hovertemplate="Company Location: %{x}<br>Median Salary: $%{y:,.0f}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Key Insights of EDA Section 13",
        [
            "Qatar has the highest median salary among all locations.",
            "Puerto Rico, United States, Saudi Arabia, and Canada also offer high-paying data job opportunities.",
            "High salaries are spread across different countries, not limited to one region.",
        ],
    )

    st.subheader("EDA Section 14: Company Size Hiring Across Data Domains")
    company_size_hiring = (
        df.groupby(["job_category", "company_size"])
        .size()
        .reset_index(name="job_count")
        .sort_values(["job_category", "job_count"], ascending=[True, False])
    )
    fig = grouped_bar_chart(
        company_size_hiring,
        x="job_category",
        y="job_count",
        color="company_size",
        title="Company Size Hiring Across Data Domains",
        labels={"job_category": "Data Domain", "job_count": "Number of Job Postings", "company_size": "Company Size"},
    )
    fig.update_traces(
        hovertemplate="Data Domain: %{x}<br>Job Count: %{y:,}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("EDA Section 15: Median Salary by Company Size")
    company_salary = (
        df.groupby("company_size")["salary_in_usd"]
        .median()
        .reset_index(name="median_salary")
        .sort_values("median_salary", ascending=False)
    )
    fig = bar_chart(
        company_salary,
        x="company_size",
        y="median_salary",
        text="median_salary",
        title="Median Salary Across Company Sizes",
        labels={"company_size": "Company Size", "median_salary": "Median Salary (USD)"},
    )
    fig.update_traces(
        texttemplate="$%{y:,.0f}",
        hovertemplate="Company Size: %{x}<br>Median Salary: $%{y:,.0f}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Key Insights of EDA Sections 14 & 15",
        [
            "Medium-sized companies hire the most across all data domains.",
            "Large companies hire second most, while small companies have the least hiring.",
            "Medium-sized companies also offer the highest median salary.",
            "Small companies have both the lowest hiring and lowest median salary.",
        ],
    )

with tab4:
    st.subheader("EDA Section 16: Employment Type Distribution")
    employment = (
        df.groupby("employment_type")
        .size()
        .reset_index(name="job_count")
        .sort_values("job_count", ascending=False)
    )
    fig = bar_chart(
        employment,
        x="employment_type",
        y="job_count",
        text="job_count",
        title="Employment Type Distribution in Data Jobs",
        labels={"employment_type": "Employment Type", "job_count": "Number of Job Postings"},
    )
    fig.update_traces(
        hovertemplate="Employment Type: %{x}<br>Job Postings: %{y:,}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Key Insights of EDA Section 16",
        [
            "Full-time jobs dominate the data job market.",
            "Contract, Part-time, and Freelance roles are very limited compared to Full-time jobs.",
            "The data industry strongly prefers stable long-term employment over flexible work types.",
        ],
    )
