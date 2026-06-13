from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ROOT_DIR = Path(__file__).resolve().parents[1]
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
