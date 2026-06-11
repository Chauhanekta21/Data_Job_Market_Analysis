import streamlit as st
import matplotlib.pyplot as plt
import textwrap

from utils.data_loader import load_data
from utils.theme import PASTEL


# -----------------------------
# LOAD DATA
# -----------------------------

df = load_data()


# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("📊 Job Market Analysis")

st.markdown(
    "Explore job demand across different data domains and popular roles."
)

st.write("---")


# -----------------------------
# FILTERS
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    year = st.selectbox(
        "Select Year",
        ["All"] + sorted(df["work_year"].unique().tolist())
    )

with col2:
    category = st.selectbox(
        "Select Job Category",
        ["All"] + sorted(df["job_category"].unique().tolist())
    )


# Apply filters

data = df.copy()

if year != "All":
    data = data[data["work_year"] == year]

if category != "All":
    data = data[data["job_category"] == category]


# -----------------------------
# SECTION 1: JOB CATEGORY DEMAND
# -----------------------------

st.subheader("📌 Job Listings Across Data Domains")

category_count = data["job_category"].value_counts()

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    category_count.index,
    category_count.values,
    color=PASTEL["primary"],
    edgecolor="black"
)

ax.set_xlabel("Job Category")
ax.set_ylabel("Number of Jobs")
ax.set_title("Job Demand by Data Domain")

plt.xticks(rotation=25)

st.pyplot(fig)


st.info(
    """
    Data Science and Data Engineering show strong hiring demand
    across the global data job market.
    """
)

st.write("---")


# -----------------------------
# SECTION 2: TOP ROLES IN DOMAIN
# -----------------------------

st.subheader("📌 Top Job Roles Within Each Domain")


role_count = (
    data.groupby(["job_category", "job_title"])
    .size()
    .reset_index(name="job_count")
)


selected_domain = st.selectbox(
    "Choose Domain",
    sorted(data["job_category"].unique().tolist())
)


top_roles = (
    role_count[role_count["job_category"] == selected_domain]
    .sort_values("job_count", ascending=False)
    .head(5)
)


# Wrap long job titles
labels = [
    textwrap.fill(title, 15)
    for title in top_roles["job_title"]
]


fig2, ax2 = plt.subplots(figsize=(10, 5))


ax2.bar(
    labels,
    top_roles["job_count"],
    color=PASTEL["light"],
    edgecolor="black"
)

ax2.set_title(f"Top 5 Roles in {selected_domain}")
ax2.set_xlabel("Job Title")
ax2.set_ylabel("Number of Jobs")


st.pyplot(fig2)


st.info(
    """
    Each data domain is dominated by a few specialized roles,
    showing clear hiring concentration.
    """
)