# =====================================================
# IMPORT LIBRARIES
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Data Job Market Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# LOAD AND CLEAN DATA
# =====================================================

@st.cache_data
def load_data():

    # Load dataset
    df = pd.read_csv("data_science_salaries.csv")


    # -------------------------------------------------
    # Data Cleaning
    # -------------------------------------------------

    # Remove salary outliers
    df = df[df["salary_in_usd"] < 600000]


    # Standardize job titles
    job_title_mapping = {
        "Data Scientist (Lead)": "Lead Data Scientist",
        "Data Analyst (Senior)": "Senior Data Analyst",
        "Machine Learning Engineer (Lead)": 
            "Lead Machine Learning Engineer",
    }

    df["job_title"] = (
        df["job_title"]
        .replace(job_title_mapping)
    )


    # -------------------------------------------------
    # Create Job Category
    # -------------------------------------------------

    def categorize_job(title):

        title = title.lower()

        if "data analyst" in title:
            return "Data Analytics"

        elif "data engineer" in title:
            return "Data Engineering"

        elif (
            "machine learning" in title
            or "ai" in title
        ):
            return "Machine Learning & AI"

        elif (
            "business intelligence" in title
            or "bi" in title
        ):
            return "Business Intelligence"

        elif "data scientist" in title:
            return "Data Science"

        else:
            return "Other"


    df["job_category"] = df["job_title"].apply(
        categorize_job
    )

    return df


df = load_data()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "🏠 Home",
        "📈 Job Market Analysis",
        "💰 Salary Insights",
        "👨‍💻 Career & Work Insights",
        "🌍 Geographic Insights",
        "📌 Key Findings"
    ]
)


# =====================================================
# HOME PAGE
# =====================================================

if page == "🏠 Home":

    st.title("📊 Data Job Market Analysis Dashboard")

    st.markdown("""
    Explore global trends in the data industry including:

    - Job demand across domains
    - Salary trends
    - Experience level requirements
    - Work models
    - Company hiring patterns
    - Geographic salary insights
    """)


    st.header("📌 Dataset Overview")


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "Total Jobs",
        f"{len(df):,}"
    )


    col2.metric(
        "Job Roles",
        df["job_title"].nunique()
    )


    col3.metric(
        "Countries",
        df["company_location"].nunique()
    )


    col4.metric(
        "Median Salary",
        f"${df['salary_in_usd'].median():,.0f}"
    )


    col5.metric(
        "Years Covered",
        f"{df['work_year'].min()} - "
        f"{df['work_year'].max()}"
    )


    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


    st.subheader("Dataset Shape")

    st.write(
        f"""
        Rows: {df.shape[0]:,}  
        Columns: {df.shape[1]}
        """
    )

# =====================================================
# JOB MARKET ANALYSIS
# =====================================================

elif page == "📈 Job Market Analysis":

    st.title("📈 Job Market Analysis")

    st.markdown("""
    Explore hiring trends, job demand across categories,
    popular roles, and market growth over time.
    """)


    # -------------------------------------------------
    # Job Category Demand
    # -------------------------------------------------

    st.subheader("🔥 Most In-Demand Data Categories")


    category_count = (
        df["job_category"]
        .value_counts()
        .reset_index()
    )

    category_count.columns = [
        "Job Category",
        "Job Count"
    ]


    fig = px.bar(
        category_count,
        x="Job Category",
        y="Job Count",
        text="Job Count",
        title="Data Job Demand by Category"
    )


    fig.update_layout(
        xaxis_title="Job Category",
        yaxis_title="Number of Job Listings"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -------------------------------------------------
    # Top Roles within Each Category
    # -------------------------------------------------

    st.subheader("👨‍💻 Top Roles by Job Category")


    selected_category = st.selectbox(
        "Select a Job Category",
        sorted(df["job_category"].unique())
    )


    top_roles = (
        df[df["job_category"] == selected_category]
        ["job_title"]
        .value_counts()
        .head(10)
        .reset_index()
    )


    top_roles.columns = [
        "Job Title",
        "Number of Jobs"
    ]


    fig = px.bar(
        top_roles,
        x="Number of Jobs",
        y="Job Title",
        orientation="h",
        text="Number of Jobs",
        title=f"Top Roles in {selected_category}"
    )


    fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -------------------------------------------------
    # Demand vs Salary Relationship
    # -------------------------------------------------

    st.subheader("💰 Demand vs Salary Comparison")


    demand_salary = (
        df.groupby("job_title")
        .agg(
            Job_Demand=("job_title", "count"),
            Median_Salary=("salary_in_usd", "median")
        )
        .reset_index()
    )


    # Filter roles with sufficient data
    demand_salary = demand_salary[
        demand_salary["Job_Demand"] >= 20
    ]


    fig = px.scatter(
        demand_salary,
        x="Job_Demand",
        y="Median_Salary",
        size="Job_Demand",
        hover_name="job_title",
        title="Popularity vs Salary"
    )


    fig.update_layout(
        xaxis_title="Number of Job Listings",
        yaxis_title="Median Salary (USD)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -------------------------------------------------
    # Job Market Growth Trend
    # -------------------------------------------------

    st.subheader("📅 Data Job Market Trend Over Years")


    yearly_jobs = (
        df.groupby("work_year")
        .size()
        .reset_index(name="Total Jobs")
    )


    fig = px.line(
        yearly_jobs,
        x="work_year",
        y="Total Jobs",
        markers=True,
        title="Data Job Demand Trend (2020–2024)"
    )


    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Job Listings"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# SALARY INSIGHTS
# =====================================================

elif page == "💰 Salary Insights":

    st.title("💰 Salary Insights")

    st.markdown("""
    Explore how salaries vary based on job categories,
    roles, experience levels, work models, and company size.
    """)


    # -------------------------------------------------
    # Salary by Job Category
    # -------------------------------------------------

    st.subheader("📊 Median Salary by Job Category")


    category_salary = (
        df.groupby("job_category")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )


    fig = px.bar(
        category_salary,
        x="job_category",
        y="salary_in_usd",
        text="salary_in_usd",
        title="Median Salary Across Data Categories"
    )


    fig.update_layout(
        xaxis_title="Job Category",
        yaxis_title="Median Salary (USD)"
    )


    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Highest Paying Roles
    # -------------------------------------------------

    st.subheader("🏆 Top 10 Highest Paying Roles")


    top_roles_salary = (
        df.groupby("job_title")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )


    fig = px.bar(
        top_roles_salary,
        x="salary_in_usd",
        y="job_title",
        orientation="h",
        text="salary_in_usd",
        title="Top Paying Data Roles"
    )


    fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        xaxis_title="Median Salary (USD)",
        yaxis_title="Job Title"
    )


    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Salary Trend Over Years
    # -------------------------------------------------

    st.subheader("📈 Salary Growth Trend")


    yearly_salary = (
        df.groupby("work_year")["salary_in_usd"]
        .median()
        .reset_index()
    )


    fig = px.line(
        yearly_salary,
        x="work_year",
        y="salary_in_usd",
        markers=True,
        title="Median Salary Trend (2020–2024)"
    )


    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Median Salary (USD)"
    )


    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Salary by Experience Level
    # -------------------------------------------------

    st.subheader("🎓 Salary by Experience Level")


    exp_salary = (
        df.groupby("experience_level")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )


    fig = px.bar(
        exp_salary,
        x="experience_level",
        y="salary_in_usd",
        text="salary_in_usd"
    )


    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Median Salary (USD)"
    )


    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Salary by Work Model
    # -------------------------------------------------

    st.subheader("🏠 Salary by Work Model")


    work_salary = (
        df.groupby("work_models")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )


    fig = px.bar(
        work_salary,
        x="work_models",
        y="salary_in_usd",
        text="salary_in_usd"
    )


    fig.update_layout(
        xaxis_title="Work Model",
        yaxis_title="Median Salary (USD)"
    )


    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Salary by Company Size
    # -------------------------------------------------

    st.subheader("🏢 Salary by Company Size")


    company_salary = (
        df.groupby("company_size")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )


    fig = px.bar(
        company_salary,
        x="company_size",
        y="salary_in_usd",
        text="salary_in_usd"
    )


    fig.update_layout(
        xaxis_title="Company Size",
        yaxis_title="Median Salary (USD)"
    )


    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# CAREER & WORK INSIGHTS
# =====================================================

elif page == "👨‍💻 Career & Work Insights":

    st.title("👨‍💻 Career & Work Insights")

    st.markdown("""
    Understand hiring preferences based on experience,
    work models, employment types, and company sizes.
    """)


    # -------------------------------------------------
    # Job Demand by Experience Level
    # -------------------------------------------------

    st.subheader("🎓 Hiring Demand by Experience Level")

    exp_demand = (
        df["experience_level"]
        .value_counts()
        .reset_index()
    )

    exp_demand.columns = [
        "Experience Level",
        "Number of Jobs"
    ]

    fig = px.bar(
        exp_demand,
        x="Experience Level",
        y="Number of Jobs",
        text="Number of Jobs",
        title="Job Opportunities by Experience Level"
    )

    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Work Model Distribution
    # -------------------------------------------------

    st.subheader("🏠 Work Model Distribution")

    work_distribution = (
        df["work_models"]
        .value_counts()
        .reset_index()
    )

    work_distribution.columns = [
        "Work Model",
        "Number of Jobs"
    ]

    fig = px.pie(
        work_distribution,
        names="Work Model",
        values="Number of Jobs",
        title="Remote vs Hybrid vs On-site Jobs"
    )

    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Employment Type Distribution
    # -------------------------------------------------

    st.subheader("📄 Employment Type Distribution")

    employment = (
        df["employment_type"]
        .value_counts()
        .reset_index()
    )

    employment.columns = [
        "Employment Type",
        "Number of Jobs"
    ]

    fig = px.bar(
        employment,
        x="Employment Type",
        y="Number of Jobs",
        text="Number of Jobs",
        title="Hiring by Employment Type"
    )

    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------------------------
    # Company Size Hiring Trend
    # -------------------------------------------------

    st.subheader("🏢 Hiring by Company Size")

    company_jobs = (
        df["company_size"]
        .value_counts()
        .reset_index()
    )

    company_jobs.columns = [
        "Company Size",
        "Number of Jobs"
    ]

    fig = px.bar(
        company_jobs,
        x="Company Size",
        y="Number of Jobs",
        text="Number of Jobs"
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# GEOGRAPHIC INSIGHTS
# =====================================================

elif page == "🌍 Geographic Insights":

    st.title("🌍 Geographic Insights")

    st.markdown("""
    Explore how salaries vary across different countries.
    """)


    # -------------------------------------------------
    # Highest Paying Countries
    # -------------------------------------------------

    st.subheader("💵 Top 10 Highest Paying Countries")

    country_salary = (
        df.groupby("company_location")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        country_salary,
        x="company_location",
        y="salary_in_usd",
        text="salary_in_usd",
        title="Top Paying Countries"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Median Salary (USD)"
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# KEY FINDINGS
# =====================================================

elif page == "📌 Key Findings":

    st.title("📌 Key Insights & Future Scope")


    st.success("""
    🔹 The data industry has experienced significant growth over recent years.

    🔹 Data Engineering, Data Science, and Machine Learning roles
    are among the most valuable areas in the market.

    🔹 Salary strongly increases with seniority and expertise.

    🔹 On-site and remote jobs dominate the market, while hybrid
    opportunities remain comparatively lower.

    🔹 Company size and location influence compensation patterns.

    🔹 The data job market continues to evolve with increasing
    demand for specialized skills.
    """)


    st.header("🚀 Future Scope")

    st.info("""
    📊 Build a Power BI dashboard with advanced business KPIs,
    storytelling, and executive-level reporting.

    🤖 Apply Machine Learning models to predict future job
    demand and salary trends.
    """)