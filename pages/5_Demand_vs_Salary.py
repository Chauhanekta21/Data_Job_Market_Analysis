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

st.title("📈 Demand vs Salary Analysis")

st.markdown(
    """
    Compare job demand with salary potential across different data domains.
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
    selected_experience = st.selectbox(
        "Select Experience Level",
        ["All"] + sorted(df["experience_level"].unique().tolist())
    )


# -------------------------
# APPLY FILTERS
# -------------------------

filtered_df = df.copy()


if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["work_year"] == selected_year
    ]


if selected_experience != "All":
    filtered_df = filtered_df[
        filtered_df["experience_level"] == selected_experience
    ]


# -------------------------
# AGGREGATE DATA
# -------------------------

domain_analysis = (
    filtered_df
    .groupby("job_category")
    .agg(
        job_count=("salary_in_usd", "count"),
        median_salary=("salary_in_usd", "median")
    )
    .reset_index()
)


st.write("---")

# -------------------------
# DEMAND VS SALARY SCATTER PLOT
# -------------------------

st.subheader("📊 Relationship Between Job Demand and Salary")

fig, ax = plt.subplots(figsize=(10, 6))


ax.scatter(
    domain_analysis["job_count"],
    domain_analysis["median_salary"],
    s=250,
    color=PASTEL["primary"],
    edgecolor="black",
    alpha=0.8
)


# Add labels to each point
for _, row in domain_analysis.iterrows():
    ax.text(
        row["job_count"],
        row["median_salary"],
        row["job_category"],
        fontsize=9,
        ha="left",
        va="bottom"
    )


ax.set_title("Demand vs Salary Across Data Domains")
ax.set_xlabel("Number of Job Listings")
ax.set_ylabel("Median Salary (USD)")

ax.grid(
    linestyle="--",
    alpha=0.4
)


st.pyplot(fig)


# -------------------------
# KEY INSIGHTS
# -------------------------

st.info(
    """
    • Machine Learning & AI offers high salary with moderate demand.

    • Data Science and Data Engineering show strong demand with competitive salaries.

    • Data Analysis and BI roles have high demand but comparatively lower salary levels.

    • Leadership roles are fewer in number but provide premium compensation.
    """
)


# -------------------------
# SUMMARY METRICS
# -------------------------

st.write("---")

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Highest Demand Domain",
        domain_analysis.loc[
            domain_analysis["job_count"].idxmax(),
            "job_category"
        ]
    )


with col2:
    st.metric(
        "Highest Median Salary",
        f"${int(domain_analysis['median_salary'].max()):,}"
    )


with col3:
    st.metric(
        "Total Domains",
        domain_analysis["job_category"].nunique()
    )


st.success(
    "This analysis reveals how market demand aligns with salary potential across different data domains."
)