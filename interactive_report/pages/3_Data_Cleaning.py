import streamlit as st

from utils.charts import box_chart
from utils.data_loader import (
    groupwise_salary_outliers,
    load_clean_data,
    load_raw_data,
    prepare_data_like_notebook,
)
from utils.formatting import format_currency, format_number, insight_box


st.title("Data Cleaning & Quality Checks")
st.write(
    "This page preserves the notebook's cleaning workflow: copying raw data, standardizing job titles, "
    "creating the job_category feature, detecting salary outliers by experience level, and removing only "
    "unrealistic extreme salaries."
)

raw_df = load_raw_data()
clean_df = load_clean_data()

if clean_df.empty:
    st.warning("Clean dataset not found.")
    st.stop()

if raw_df.empty:
    st.info("Raw dataset not found. Showing available cleaned dataset details.")
    prepared_df = clean_df
else:
    prepared_df = prepare_data_like_notebook(raw_df)

cols = st.columns(4)
cols[0].metric("Clean Rows", format_number(len(clean_df)))
cols[1].metric("Clean Columns", format_number(clean_df.shape[1]))
cols[2].metric("Max Clean Salary", format_currency(clean_df["salary_in_usd"].max()))
cols[3].metric("Median Clean Salary", format_currency(clean_df["salary_in_usd"].median()))

st.subheader("Job Title Standardization")
st.write(
    "The notebook replaced abbreviations and inconsistent labels such as ML Engineer, BI Analyst, "
    "Data Modeller, and ETL Developer with standardized full-form titles."
)

st.subheader("Feature Engineering: job_category")
st.write(
    "A new job_category column was inserted after job_title. Titles were grouped into meaningful "
    "domains using exact title matches first, then keyword-based rules."
)
st.dataframe(
    clean_df[["job_title", "job_category"]].drop_duplicates().sort_values(["job_category", "job_title"]),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Salary Outlier Handling")
if not raw_df.empty:
    bounds, outliers = groupwise_salary_outliers(prepared_df)
    st.write(
        "Outliers were detected within each experience level using the IQR method. The notebook found "
        "that not every high salary was invalid, so only unrealistic extreme salaries were removed."
    )
    st.dataframe(bounds, use_container_width=True, hide_index=True)
    st.metric("Group-wise IQR Outliers Detected", format_number(len(outliers)))

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            box_chart(prepared_df, y="salary_in_usd", title="Salary Distribution Before Final Filtering"),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            box_chart(clean_df, y="salary_in_usd", title="Salary Distribution After Final Filtering"),
            use_container_width=True,
        )

insight_box(
    "Cleaning Insights Preserved",
    [
        "Salary distribution was right-skewed.",
        "High salaries can be valid for senior and executive roles, so outliers were checked within experience levels.",
        "Extreme unrealistic salaries above the notebook threshold were removed using salary_in_usd < 600000.",
        "The final clean dataset is more realistic and ready for EDA.",
    ],
)
