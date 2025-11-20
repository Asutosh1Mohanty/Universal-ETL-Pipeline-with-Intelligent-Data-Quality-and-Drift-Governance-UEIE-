import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "processed")
OUTPUT_CSV = os.path.join(PROCESSED_DIR, "cleaned_sales.csv")
OUTPUT_PARQUET = os.path.join(PROCESSED_DIR, "cleaned_sales.parquet")

def ensure_processed_dir():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def save_dataframe(df, as_parquet: bool = False) -> str:
    ensure_processed_dir()
    if as_parquet:
        df.to_parquet(OUTPUT_PARQUET, index=False)
        return OUTPUT_PARQUET
    else:
        df.to_csv(OUTPUT_CSV, index=False)
        return OUTPUT_CSV