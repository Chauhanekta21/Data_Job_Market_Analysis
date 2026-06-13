import streamlit as st

from utils.charts import bar_chart
from utils.data_loader import load_clean_data
from utils.formatting import insight_box


st.title("Domain Demand Analysis")
st.write(
    "This page recreates EDA sections 01 and 02: overall job demand across data domains "
    "and the top job roles within each domain."
)

df = load_clean_data()
if df.empty:
    st.warning("Clean dataset not found.")
    st.stop()

st.subheader("EDA Section 01: Job Listings Across Data Domains")
domain_counts = df["job_category"].value_counts().reset_index()
domain_counts.columns = ["job_category", "job_listing_count"]

fig = bar_chart(
    domain_counts,
    x="job_category",
    y="job_listing_count",
    text="job_listing_count",
    title="Job Listings Across Data Domains (Highest to Lowest)",
    labels={"job_category": "Data Domain", "job_listing_count": "Number of Job Listings"},
)
fig.update_traces(
    hovertemplate="Data Domain: %{x}<br>Job Listings: %{y:,}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 01",
    [
        "Data Science domain has the highest number of job listings, followed by Data Engineering and Data Analysis.",
        "This shows that Data Science dominates the job market in this dataset compared to other data domains.",
    ],
)

st.subheader("EDA Section 02: Top Job Roles Within Each Data Domain")
job_role_count = df.groupby(["job_category", "job_title"]).size().reset_index(name="count")
domains = [
    "Data Science",
    "Data Engineering",
    "Data Analysis",
    "Machine Learning & AI",
    "Business Intelligence",
    "Data Architecture",
    "Leadership & Management",
    "Other",
]
selected_domains = st.multiselect("Domains to display", domains, default=domains)

for domain in selected_domains:
    temp = (
        job_role_count[job_role_count["job_category"] == domain]
        .sort_values("count", ascending=False)
        .head(5)
    )
    fig = bar_chart(
        temp,
        x="job_title",
        y="count",
        text="count",
        title=f"Top {domain} Job Roles by Job Listings",
        labels={"job_title": "Job Role", "count": "Number of Job Listings"},
        height=470,
    )
    fig.update_traces(
        hovertemplate="Job Role: %{x}<br>Job Listings: %{y:,}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 02",
    [
        "Each domain is dominated by one primary role.",
        "There is a sharp drop after the top role, showing highly concentrated demand.",
        "Data Analyst shows the highest entry-level demand.",
        "ML roles are more niche.",
        "The market favors standard roles over specialized ones.",
    ],
)
