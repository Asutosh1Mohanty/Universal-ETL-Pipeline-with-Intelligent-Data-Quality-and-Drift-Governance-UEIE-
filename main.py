import os
import logging
from etl import extract, transform, load, quality
import pandas as pd

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
        logging.info(f"Processing chunk {i+1}")
        cleaned_chunk = transform.clean_dataframe(chunk)
        parts.append(cleaned_chunk)
    combined = pd.concat(parts, ignore_index=True)
    return process_full_df(combined)

def main():
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

    # If descriptor indicates chunking, handle separately
    if df is None and info.get("type") == "csv_chunked":
        cleaned, q = process_csv_in_chunks(info["path"], chunksize=info.get("chunksize", 100_000))
    else:
        cleaned, q = process_full_df(df)

    logging.info("Pipeline finished")

if __name__ == "__main__":
    main()