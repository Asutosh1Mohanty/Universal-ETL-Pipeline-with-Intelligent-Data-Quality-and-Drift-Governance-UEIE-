"""
etl/transform.py
- Robust transforms that work for arbitrary columns
- Standardizes column names
- Fills missing values based on dtype
- Tries to parse date-like columns (column name contains 'date' or 'time')
- Returns cleaned dataframe
"""
import pandas as pd
import numpy as np
from typing import List

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df

def detect_date_columns(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if "date" in c or "time" in c or c.endswith("_dt")]

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    # Drop exact duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Try to parse date-like columns
    date_cols = detect_date_columns(df)
    for c in date_cols:
        try:
            df[c] = pd.to_datetime(df[c], errors="coerce")
        except Exception:
            # keep as-is if parse fails
            pass

    # Fill missing values conservatively
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # numeric: fill with 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            # datetime: leave NaT (or could fill with a sentinel)
            # we keep NaT to allow quality checks to detect bad dates
            pass
        else:
            # other/object: convert to string and fill unknown
            df[col] = df[col].astype(object).fillna("unknown")
    return df
