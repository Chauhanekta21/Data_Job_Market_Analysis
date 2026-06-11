import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils.data_loader import load_data
from utils.theme import PASTEL


# -------------------------
# LOAD DATA
# -------------------------

df = load_data()


# -------------------------
# PAGE TITLE
# -------------------------

st.title("💰 Salary Analysis")

st.markdown(
    """
    Explore salary patterns across data domains and job roles.
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


# -------------------------
# SECTION 1:
# MEDIAN SALARY BY DOMAIN
# -------------------------

st.subheader("📊 Median Salary Across Data Domains")


salary_by_domain = (
    filtered_df
    .groupby("job_category")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
)


fig, ax = plt.subplots(figsize=(10, 5))


ax.bar(
    salary_by_domain.index,
    salary_by_domain.values,
    color=PASTEL["primary"],
    edgecolor="black"
)


ax.set_xlabel("Job Category")
ax.set_ylabel("Median Salary (USD)")
ax.set_title("Median Salary by Data Domain")

plt.xticks(rotation=25)


st.pyplot(fig)


st.info(
    """
    AI/ML and leadership-focused domains generally offer higher salary potential compared to other data fields.
    """
)




st.write("---")


# -------------------------
# SECTION 2:
# TOP 10 HIGHEST PAYING ROLES
# -------------------------

st.subheader("🏆 Top 10 Highest Paying Job Roles")


top_roles = (
    filtered_df
    .groupby("job_title")["salary_in_usd"]
    .median()
    .sort_values(ascending=False)
    .head(10)
)


fig, ax = plt.subplots(figsize=(10, 6))


ax.barh(
    top_roles.index,
    top_roles.values,
    color=PASTEL["light"],
    edgecolor="black"
)


ax.set_xlabel("Median Salary (USD)")
ax.set_ylabel("Job Role")
ax.set_title("Top 10 Highest Paying Data Job Roles")


# Highest salary at the top
ax.invert_yaxis()


st.pyplot(fig)


# -------------------------
# KEY INSIGHT
# -------------------------

st.info(
    """
    Leadership, AI/ML, and architecture-focused positions dominate the highest-paying roles in the data industry.
    """
)


st.write("---")


# -------------------------
# SALARY SUMMARY METRICS
# -------------------------

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Highest Median Salary",
        f"${int(top_roles.max()):,}"
    )


with col2:
    st.metric(
        "Overall Median Salary",
        f"${int(filtered_df['salary_in_usd'].median()):,}"
    )


with col3:
    st.metric(
        "Total Roles",
        filtered_df["job_title"].nunique()
    )


st.success(
    "Salary analysis highlights the most valuable domains and roles in the global data job market."
)