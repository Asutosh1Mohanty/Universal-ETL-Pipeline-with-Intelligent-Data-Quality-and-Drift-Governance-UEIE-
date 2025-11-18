import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "processed")
QUALITY_REPORT = os.path.join(PROCESSED_DIR, "quality_report.txt")

def run_checks(df):
    rows = len(df)
    cols = list(df.columns)
    report_lines = []
    report_lines.append("DATA QUALITY REPORT\n")
    report_lines.append(f"Total rows: {rows}")
    report_lines.append(f"Columns: {cols}\n")
    report_lines.append("NULL VALUE COUNTS (per column):")
    nulls = df.isnull().sum()
    for col, cnt in nulls.items():
        report_lines.append(f"  {col}: {int(cnt)}")
    report_lines.append("")
    dup_count = int(df.duplicated().sum())
    report_lines.append(f"Duplicate rows: {dup_count}\n")
    # numeric checks
    if "unit_price" in df.columns:
        df["unit_price_num"] = pd.to_numeric(df["unit_price"], errors="coerce")
        report_lines.append(f"unit_price: negative_count={(df['unit_price_num']<0).sum()}, non_numeric_count={df['unit_price_num'].isna().sum()}")
    if "quantity" in df.columns:
        df["quantity_num"] = pd.to_numeric(df["quantity"], errors="coerce")
        report_lines.append(f"quantity: negative_count={(df['quantity_num']<0).sum()}, non_numeric_count={df['quantity_num'].isna().sum()}")
    if "order_date" in df.columns:
        parsed = pd.to_datetime(df["order_date"], errors="coerce")
        report_lines.append(f"order_date: unparsable_count={parsed.isna().sum()}")
    if "order_id" in df.columns:
        report_lines.append(f"order_id uniqueness: unique_count={int(df['order_id'].nunique())}, total_rows={rows}")
    # write
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(QUALITY_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    return {
        "rows": rows,
        "duplicates": dup_count,
        "verdict": "PASS" if dup_count==0 else "FAIL",
        "report_path": QUALITY_REPORT
    }
