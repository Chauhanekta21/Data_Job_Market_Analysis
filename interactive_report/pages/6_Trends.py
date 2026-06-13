import streamlit as st

from utils.charts import line_chart
from utils.data_loader import load_clean_data
from utils.formatting import insight_box


st.title("Trend Analysis")
st.write(
    "This page recreates EDA sections 06 and 07: demand trends and median salary trends "
    "across data domains from 2020 to 2024."
)

df = load_clean_data()
if df.empty:
    st.warning("Clean dataset not found.")
    st.stop()

domains = sorted(df["job_category"].unique())
selected_domains = st.multiselect("Data domains", domains, default=domains)
filtered = df[df["job_category"].isin(selected_domains)]

st.subheader("EDA Section 06: Demand Trend Across Data Domains")
domain_demand_trend = (
    filtered.groupby(["work_year", "job_category"])
    .size()
    .reset_index(name="job_listing_count")
)
domain_demand_trend["work_year"] = domain_demand_trend["work_year"].astype(str)

fig = line_chart(
    domain_demand_trend,
    x="work_year",
    y="job_listing_count",
    color="job_category",
    title="Demand Growth Across Data Domains (2020-2024)",
    labels={"work_year": "Year", "job_listing_count": "Number of Job Listings", "job_category": "Data Domain"},
)
fig.update_traces(
    hovertemplate="Year: %{x}<br>Job Listings: %{y:,}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 06",
    [
        "Job demand across all data domains grew consistently from 2020 to 2023.",
        "Data Science recorded the highest job demand throughout the period and experienced the sharpest growth by 2023.",
        "Data Engineering and Data Analysis also experienced significant demand growth.",
        "Machine Learning & AI demand increased rapidly after 2022, reflecting growing industry adoption of AI technologies.",
        "Leadership & Management, Business Intelligence, and Data Architecture maintained comparatively lower but stable demand levels.",
        "Most domains showed a noticeable drop in 2024, which may indicate incomplete yearly data or changing market conditions.",
    ],
)

st.subheader("EDA Section 07: Salary Trend Across Data Domains")
domain_salary_trend = (
    filtered.groupby(["work_year", "job_category"])["salary_in_usd"]
    .median()
    .reset_index(name="median_salary")
)
domain_salary_trend["work_year"] = domain_salary_trend["work_year"].astype(str)

fig = line_chart(
    domain_salary_trend,
    x="work_year",
    y="median_salary",
    color="job_category",
    title="Median Salary Trends Across Data Domains (2020-2024)",
    labels={"work_year": "Year", "median_salary": "Median Salary (USD)", "job_category": "Data Domain"},
    height=620,
)
fig.update_traces(
    hovertemplate="Year: %{x}<br>Median Salary: $%{y:,.0f}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

insight_box(
    "Key Insights of EDA Section 07",
    [
        "ML & AI shows strongest growth, moving from about 100K to about 185K.",
        "Data Science grows until 2023, then shows a slight dip in 2024.",
        "Data Engineering shows steady growth, stabilizing around 137K-140K.",
        "Data Analysis remains flatter with slower salary growth.",
        "Leadership & Management peaks in 2024, reflecting high-value roles.",
        "Data Architecture slightly declines after its peak but remains a stable niche role.",
        "Business Intelligence grows until 2023 and declines in 2024.",
        "Overall, AI/ML leads salary growth while traditional roles are plateauing.",
    ],
)

insight_box(
    "Common Relationship Insights",
    [
        "ML & AI shows strongest growth in both demand and salary.",
        "Data Engineering shows steady demand and salary growth.",
        "Data Science has high demand but slightly weaker salary growth in 2024, suggesting early saturation.",
        "Data Analysis shows moderate demand but low salary growth, reflecting entry-level dominance.",
        "Leadership & Management shows strong salary performance with stable demand.",
        "BI and Data Architecture show stable to declining trends, indicating mature or shifting domains.",
    ],
)
