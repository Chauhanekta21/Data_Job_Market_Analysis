from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATHS = [
    DATA_DIR / "data_science_salaries.csv",
    ROOT_DIR / "data_science_salaries.csv",
    ROOT_DIR.parent / "data_science_salaries.csv",
]
CLEAN_DATA_PATHS = [
    DATA_DIR / "data_science_salaries_clean.csv",
    ROOT_DIR / "data_science_salaries_clean.csv",
]


@st.cache_data(show_spinner=False)
def load_clean_data() -> pd.DataFrame:
    for path in CLEAN_DATA_PATHS:
        if path.exists():
            return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_raw_data() -> pd.DataFrame:
    for path in RAW_DATA_PATHS:
        if path.exists():
            return pd.read_csv(path)
    return pd.DataFrame()


def standardize_job_titles(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["job_title"] = df["job_title"].replace(
        {
            "ML Engineer": "Machine Learning Engineer",
            "BI Developer": "Business Intelligence Developer",
            "BI Analyst": "Business Intelligence Analyst",
            "BI Data Analyst": "Business Intelligence Data Analyst",
            "Data Science": "Data Scientist",
            "Data Modeller": "Data Modeler",
            "ETL Developer": "ETL Engineer",
        }
    )
    return df


def get_category(title: str) -> str:
    t = title.lower()
    exact_map = {
        "data engineer": "Data Engineering",
        "etl engineer": "Data Engineering",
        "big data engineer": "Data Engineering",
        "cloud data engineer": "Data Engineering",
        "azure data engineer": "Data Engineering",
        "software data engineer": "Data Engineering",
        "data developer": "Data Engineering",
        "data scientist": "Data Science",
        "data analyst": "Data Analysis",
        "machine learning engineer": "Machine Learning & AI",
        "ai engineer": "Machine Learning & AI",
        "business intelligence analyst": "Business Intelligence",
        "data architect": "Data Architecture",
        "big data architect": "Data Architecture",
        "data science manager": "Leadership & Management",
        "head of data science": "Leadership & Management",
        "director of data science": "Leadership & Management",
    }

    if t in exact_map:
        return exact_map[t]
    if any(k in t for k in ["lead", "head", "director", "manager", "principal", "staff"]):
        return "Leadership & Management"
    if any(k in t for k in ["etl", "data engineer", "infrastructure", "integration", "pipeline", "devops"]):
        return "Data Engineering"
    if any(k in t for k in ["scientist", "research scientist", "applied scientist"]):
        return "Data Science"
    if any(k in t for k in ["machine learning", "ml", "ai", "deep learning", "nlp", "computer vision"]):
        return "Machine Learning & AI"
    if any(k in t for k in ["analyst", "analytics", "visualization", "insight"]):
        return "Data Analysis"
    if any(k in t for k in ["business intelligence", "bi", "power bi"]):
        return "Business Intelligence"
    if any(k in t for k in ["architect", "modeler", "data architect"]):
        return "Data Architecture"
    return "Other"


def prepare_data_like_notebook(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty:
        return pd.DataFrame()
    df = standardize_job_titles(raw_df)
    categories = df["job_title"].apply(get_category)
    df.insert(loc=1, column="job_category", value=categories)
    return df


def groupwise_salary_outliers(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    outliers = []
    for group in df["experience_level"].unique():
        subset = df[df["experience_level"] == group]
        q1 = subset["salary_in_usd"].quantile(0.25)
        q3 = subset["salary_in_usd"].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        rows.append({"experience_level": group, "lower_bound": lower, "upper_bound": upper})
        outliers.append(
            subset[(subset["salary_in_usd"] < lower) | (subset["salary_in_usd"] > upper)]
        )
    return pd.DataFrame(rows), pd.concat(outliers, ignore_index=True)
