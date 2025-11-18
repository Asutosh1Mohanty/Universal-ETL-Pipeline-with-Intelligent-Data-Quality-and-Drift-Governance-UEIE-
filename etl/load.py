import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "processed")
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "cleaned_sales.csv")

def ensure_processed_dir():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def save_dataframe(df):
    ensure_processed_dir()
    df.to_csv(OUTPUT_FILE, index=False)
    return OUTPUT_FILE
