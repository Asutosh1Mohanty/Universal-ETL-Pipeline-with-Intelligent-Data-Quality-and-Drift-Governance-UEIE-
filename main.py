import os
import logging
import pandas as pd
from datetime import datetime
import uuid
from etl import extract, transform, load, quality
# UEIE Imports
from ueie.detector import detect_file_info
from ueie.profiler import profile_dataframe
from ueie.rule_engine import decide_rules
from ueie.scorer import calculate_quality_score
from ueie.metadata import save_run_metadata, load_previous_profile,save_current_profile
from ueie.quality_gate import apply_quality_gate
from ueie.drift import detect_drift
from ueie.drift_gate import evaluate_drift_severity

# create logs folder first
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

def process_full_df(df: pd.DataFrame):
    cleaned = transform.clean_dataframe(df)
    path = load.save_dataframe(cleaned, as_parquet=False)
    q = quality.run_checks(cleaned)
    logging.info(f"Saved cleaned data to {path}")
    logging.info(f"Quality verdict: {q['verdict']}. Reports: {q['report_txt']}, {q['report_json']}")
    return cleaned, q

def process_csv_in_chunks(path: str, chunksize: int = 100_000):
    logging.info(f"Processing CSV in chunks from {path} with chunksize={chunksize}")
    reader = pd.read_csv(path, chunksize=chunksize)
    parts = []
    for i, chunk in enumerate(reader):
        logging.info(f"Processing chunk {i + 1}")
        cleaned_chunk = transform.clean_dataframe(chunk)
        parts.append(cleaned_chunk)
    combined = pd.concat(parts, ignore_index=True)
    return process_full_df(combined)

# Main Pipeline
def main():
    # Start Time Metrics
    run_id = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    start_time = datetime.utcnow()
    end_time = None
    duration_sec = None
    logging.info(f"Run started | run_id={run_id}")

    logging.info("Pipeline started")

    # decide: chunked=True for very large CSVs to avoid OOM; default False
    try:
        df_or_descriptor = extract.load_latest(chunked=False)
    except FileNotFoundError as e:
        logging.error(str(e))
        raise

    # load_latest returns (df, info) or (None, descriptor) depending on extension and chunked flag
    if isinstance(df_or_descriptor, tuple):
        df, info = df_or_descriptor
    else:
        # backwards compat: some callers may return df directly
        df, info = df_or_descriptor, {"path": None}

    # UEIE file detection
    if info.get("path"):
        file_info = detect_file_info(info["path"])
        logging.info(f"UEIE detected file info: {file_info}")
    else:
        file_info = {}

    # Profiling + Rule Decision
    try:
        ueie_profile = profile_dataframe(df) if df is not None else {}
        ueie_rules = decide_rules(ueie_profile)
        logging.info(f"UEIE generated rules: {ueie_rules}")
    except Exception as e:
        logging.warning(f"UEIE profiling failed, continuing without it: {e}")
        ueie_profile = {}
        ueie_rules = {}

    # Data Drift Detection
    try:
        previous_profile = load_previous_profile()
        drift_report = detect_drift(previous_profile, ueie_profile)

        if drift_report:
            logging.warning(f"UEIE data drift detected: {drift_report}")
        else:
            logging.info("UEIE data drift check: no drift detected")

    except Exception as e:
        logging.warning(f"UEIE drift detection failed: {e}")
        drift_report = {}

    # Drift Severity
    drift_severity = evaluate_drift_severity(drift_report)
    logging.info(
        f"UEIE drift severity: {drift_severity['status']} | "
        f"{drift_severity['reason']}"
    )

    # Transform / Load / Quality
    # If descriptor indicates chunking, handle separately
    if df is None and info.get("type") == "csv_chunked":
        cleaned, q = process_csv_in_chunks(info["path"], chunksize=info.get("chunksize", 100_000))
    else:
        cleaned, q = process_full_df(df)

    rows_processed = len(cleaned) if cleaned is not None else 0
    logging.info(f"Rows processed: {rows_processed}")

    # Quality Score + Quality Gate
    quality_score = calculate_quality_score(ueie_profile)
    gate_result = apply_quality_gate(quality_score)

    logging.info(f"UEIE quality score: {quality_score}")
    logging.info(f"UEIE quality gate status: {gate_result['status']} |" f"{gate_result['reason']}")

    # Metadata + Profile Persistence
    metadata_path = save_run_metadata(
        file_info=file_info,
        quality_score=quality_score,
        extra_metadata={
            "run_id": run_id,
            "rows_processed": rows_processed,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat() if end_time else None,
            "duration_sec": duration_sec,
            "quality_gate_status": gate_result["status"],
            "quality_gate_reason": gate_result["reason"],
            "drift_detected": bool(drift_report),
            "drift_columns": list(drift_report.keys()),
            "drift_severity": drift_severity["status"],
            "drift_reason": drift_severity["reason"]

        }
    )

    save_current_profile(ueie_profile)
    logging.info(f"UEIE metadata written to: {metadata_path}")

    # Enforce Quality Gate
    if gate_result["status"] == "FAIL":
        raise RuntimeError(
            f"UEIE QUALITY GATE FAILED → {gate_result['reason']}. "
            f"Pipeline stopped to protect downstream systems."
        )

    if gate_result["status"] == "WARN":
        logging.warning(
            f"UEIE QUALITY GATE WARNING → {gate_result['reason']}. "
            f"Pipeline continues with caution."
        )

    # Enforce Drift Gate
    if drift_severity["status"] == "CRITICAL":
        raise RuntimeError(
            "UEIE DRIFT GATE FAILED → Critical data drift detected. "
            "Pipeline stopped to prevent corrupted downstream data."
        )

    if drift_severity["status"] == "MAJOR":
        logging.warning(
            "UEIE DRIFT GATE WARNING → Major drift detected. "
            "Pipeline continues with caution."
        )

    # Runtime Duration
    end_time = datetime.utcnow()
    duration_sec = round((end_time - start_time).total_seconds(), 2)
    logging.info(f"Run completed in {duration_sec} seconds")

    logging.info("Pipeline finished")

if __name__ == "__main__":
    main()