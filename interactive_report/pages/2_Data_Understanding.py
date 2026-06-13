import streamlit as st

from utils.data_loader import load_clean_data, load_raw_data
from utils.formatting import format_number


st.title("Data Understanding")
st.write(
    "This page recreates the notebook's dataset inspection step: shape, columns, data types, "
    "missing values, duplicate rows, unique counts, and categorical frequencies."
)

raw_df = load_raw_data()
clean_df = load_clean_data()
df = raw_df if not raw_df.empty else clean_df

if df.empty:
    st.warning("Dataset not found.")
    st.stop()

if raw_df.empty:
    st.info("Raw dataset not found, so this page is showing the cleaned dataset.")

cols = st.columns(4)
cols[0].metric("Rows", format_number(df.shape[0]))
cols[1].metric("Columns", format_number(df.shape[1]))
cols[2].metric("Duplicate Rows", format_number(df.duplicated().sum()))
cols[3].metric("Missing Values", format_number(df.isna().sum().sum()))

tab1, tab2, tab3, tab4 = st.tabs(["Preview", "Schema", "Quality Checks", "Categorical Frequencies"])

with tab1:
    st.dataframe(df.head(), use_container_width=True, hide_index=True)

with tab2:
    schema = df.dtypes.astype(str).reset_index()
    schema.columns = ["column", "data_type"]
    st.dataframe(schema, use_container_width=True, hide_index=True)
    st.subheader("Numeric Summary")
    st.dataframe(df.describe(), use_container_width=True)

with tab3:
    missing = df.isna().sum().reset_index()
    missing.columns = ["column", "missing_values"]
    st.dataframe(missing, use_container_width=True, hide_index=True)

with tab4:
    columns = [
        col
        for col in [
            "job_title",
            "job_category",
            "experience_level",
            "employment_type",
            "work_models",
            "work_year",
            "company_size",
        ]
        if col in df.columns
    ]
    selected = st.selectbox("Choose a categorical column", columns)
    freq = df[selected].value_counts().reset_index()
    freq.columns = [selected, "count"]
    st.dataframe(freq, use_container_width=True, hide_index=True)
