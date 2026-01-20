def profile_dataframe(df):
    profile = {}
    for col in df.columns:
        profile[col] = {
            "dtype": str(df[col].dtype),
            "null_pct": round(df[col].isna().mean() * 100, 2),
            "unique_pct": round(df[col].nunique() / len(df) * 100, 2)
        }
    return profile