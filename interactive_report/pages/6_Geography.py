import streamlit as st
import matplotlib.pyplot as plt

from utils.data_loader import load_data
from utils.theme import PASTEL, apply_theme

# Apply Global Dashboard theme
apply_theme()


# -------------------------
# LOAD DATA
# -------------------------

df = load_data()


# -------------------------
# PAGE TITLE
# -------------------------

st.title("🌍 Geographic Insights")

st.markdown(
    """
    Explore global hiring trends and salary distribution across countries.
    """
)

st.write("---")


# -------------------------
# FILTERS
# -------------------------

col1, col2 = st.columns(2)


with col1:
    selected_year = st.selectbox(
        "Select Year",
        ["All"] + sorted(df["work_year"].unique().tolist())
    )


with col2:
    selected_category = st.selectbox(
        "Select Job Category",
        ["All"] + sorted(df["job_category"].unique().tolist())
    )


# -------------------------
# APPLY FILTERS
# -------------------------

filtered_df = df.copy()


if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["work_year"] == selected_year
    ]


if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["job_category"] == selected_category
    ]


st.write("---")


# =================================================
# SECTION 1: TOP HIRING COUNTRIES
# =================================================

st.subheader("📊 Top 10 Countries by Job Opportunities")


top_countries = (
    filtered_df["company_location"]
    .value_counts()
    .head(10)
)


fig, ax = plt.subplots(figsize=(10, 5))


ax.bar(
    top_countries.index,
    top_countries.values,
    color=PASTEL["primary"],
    edgecolor="black"
)


ax.set_title("Top Countries by Data Job Availability")
ax.set_xlabel("Country")
ax.set_ylabel("Number of Job Listings")

plt.xticks(rotation=25)


st.pyplot(fig)


st.info(
    """
    Countries such as the USA and Canada dominate global data job opportunities.
    """
)


st.write("---")


# =================================================
# SECTION 2: TOP COUNTRIES BY MEDIAN SALARY
# =================================================

st.subheader("💰 Top 10 Countries by Median Salary")


country_salary = (
    filtered_df
    .groupby("company_location")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
    .head(10)
)


fig, ax = plt.subplots(figsize=(10, 5))


ax.bar(
    country_salary.index,
    country_salary.values,
    color=PASTEL["light"],
    edgecolor="black"
)


ax.set_title("Top Countries by Median Salary")
ax.set_xlabel("Country")
ax.set_ylabel("Median Salary (USD)")

plt.xticks(rotation=25)


st.pyplot(fig)


st.info(
    """
    Some countries offer exceptionally high salaries, though the number of job listings may be lower.
    """
)


st.write("---")


# =================================================
# SECTION 3: GEOGRAPHIC SUMMARY METRICS
# =================================================

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Top Hiring Country",
        filtered_df["company_location"].mode()[0]
    )


with col2:
    st.metric(
        "Highest Median Salary",
        f"${int(country_salary.max()):,}"
    )


with col3:
    st.metric(
        "Countries Covered",
        filtered_df["company_location"].nunique()
    )


st.success(
    """
    The global data job market shows strong concentration in a few countries,
    while high-paying opportunities can appear across different regions.
    """
)