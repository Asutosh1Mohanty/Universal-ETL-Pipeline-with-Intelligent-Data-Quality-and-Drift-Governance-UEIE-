import pandas as pd
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "processed")
QUALITY_TXT = os.path.join(PROCESSED_DIR, "quality_report.txt")
QUALITY_JSON = os.path.join(PROCESSED_DIR, "quality_report.json")

def run_checks(df: pd.DataFrame) -> dict:
    rows = len(df)
    cols = list(df.columns)
    report = {
        "total_rows": rows,
        "columns": cols,
        "null_counts": {},
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_checks": {},
        "date_parsing_issues": {},
    }

    # null counts
    nulls = df.isnull().sum().to_dict()
    report["null_counts"] = {k: int(v) for k, v in nulls.items()}

    # numeric checks for any numeric-like columns
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            non_numeric = 0  # already numeric dtype so non-numeric should be 0
            neg_count = int((df[col] < 0).sum())
            report["numeric_checks"][col] = {"negative_count": neg_count, "non_numeric_count": int(non_numeric)}

    # date parsing issues for datetime dtypes
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            unparsable = int(df[col].isna().sum())
            report["date_parsing_issues"][col] = unparsable

    report["verdict"] = "PASS"
    # simple failure rules
    if report["duplicate_rows"] > 0:
        report["verdict"] = "FAIL"
    for col, stats in report["numeric_checks"].items():
        if stats["non_numeric_count"] > 0 or stats["negative_count"] > 0:
            report["verdict"] = "FAIL"
    for col, cnt in report["date_parsing_issues"].items():
        if cnt > 0:
            report["verdict"] = "FAIL"

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(QUALITY_TXT, "w", encoding="utf-8") as f:
        f.write("DATA QUALITY REPORT\n\n")
        f.write(json.dumps(report, indent=2, default=int))

    with open(QUALITY_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=int)

    report["report_txt"] = QUALITY_TXT
    report["report_json"] = QUALITY_JSON
    return report