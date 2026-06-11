import streamlit as st
import matplotlib.pyplot as plt

from utils.data_loader import load_data
from utils.theme import PASTEL


# -------------------------
# LOAD DATA
# -------------------------

df = load_data()


# -------------------------
# PAGE TITLE
# -------------------------

st.title("🧑‍💼 Career & Work Insights")

st.markdown(
    """
    Analyze experience levels, employment types, and company size trends.
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
# SECTION 1: EXPERIENCE LEVEL DEMAND
# =================================================

st.subheader("📊 Job Demand by Experience Level")


experience_demand = (
    filtered_df["experience_level"]
    .value_counts()
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    experience_demand.index,
    experience_demand.values,
    color=PASTEL["primary"],
    edgecolor="black"
)

ax.set_title("Demand Across Experience Levels")
ax.set_xlabel("Experience Level")
ax.set_ylabel("Number of Jobs")

st.pyplot(fig)


st.info(
    """
    Senior-level professionals dominate hiring demand, showing strong market preference for experienced talent.
    """
)


st.write("---")


# =================================================
# SECTION 2: SALARY BY EXPERIENCE LEVEL
# =================================================

st.subheader("💰 Median Salary by Experience Level")


experience_salary = (
    filtered_df
    .groupby("experience_level")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    experience_salary.index,
    experience_salary.values,
    color=PASTEL["light"],
    edgecolor="black"
)

ax.set_title("Median Salary Across Experience Levels")
ax.set_xlabel("Experience Level")
ax.set_ylabel("Median Salary (USD)")

st.pyplot(fig)


st.info(
    """
    Executive-level roles receive the highest salaries, while entry-level positions have lower compensation.
    """
)

st.write("---")


# =================================================
# SECTION 3: EMPLOYMENT TYPE DISTRIBUTION
# =================================================

st.subheader("📦 Employment Type Distribution")


employment_count = (
    filtered_df["employment_type"]
    .value_counts()
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    employment_count.index,
    employment_count.values,
    color=PASTEL["blue"],
    edgecolor="black"
)

ax.set_title("Distribution of Employment Types")
ax.set_xlabel("Employment Type")
ax.set_ylabel("Number of Jobs")

st.pyplot(fig)


st.info(
    """
    Full-time roles dominate the data job market, while contract and freelance opportunities are less common.
    """
)

st.write("---")


# =================================================
# SECTION 4: COMPANY SIZE VS SALARY
# =================================================

st.subheader("🏢 Salary Across Company Sizes")


company_salary = (
    filtered_df
    .groupby("company_size")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    company_salary.index,
    company_salary.values,
    color=PASTEL["primary"],
    edgecolor="black"
)

ax.set_title("Median Salary by Company Size")
ax.set_xlabel("Company Size")
ax.set_ylabel("Median Salary (USD)")

st.pyplot(fig)


st.info(
    """
    Medium and large organizations generally offer competitive salaries, while smaller companies may have wider salary variation.
    """
)


# =================================================
# SUMMARY METRICS
# =================================================

st.write("---")

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Most Common Experience",
        filtered_df["experience_level"].mode()[0]
    )


with col2:
    st.metric(
        "Most Common Employment",
        filtered_df["employment_type"].mode()[0]
    )


with col3:
    st.metric(
        "Company Sizes",
        filtered_df["company_size"].nunique()
    )


st.success(
    "Career insights reveal how experience, job type, and company scale influence opportunities in the data industry."
)