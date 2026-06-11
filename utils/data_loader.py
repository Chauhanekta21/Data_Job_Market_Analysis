import pandas as pd
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data_science_salaries.csv")

    df = pd.read_csv(file_path)

    # clean column names (prevents KeyError issues)
    df.columns = df.columns.str.strip()

    return df