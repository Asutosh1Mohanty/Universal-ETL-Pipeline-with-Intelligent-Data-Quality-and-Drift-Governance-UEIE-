import pandas as pd

def standardize_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    return df

def clean_dataframe(df):
    df = standardize_columns(df)
    before = len(df)
    df = df.drop_duplicates()
    # conservative fill
    fill_map = {}
    for col in df.columns:
        if df[col].dtype == object:
            fill_map[col] = "unknown"
        else:
            fill_map[col] = 0
    if fill_map:
        df = df.fillna(fill_map)
    return df
