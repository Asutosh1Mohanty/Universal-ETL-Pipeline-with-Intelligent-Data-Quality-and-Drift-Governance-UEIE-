from etl import extract, transform, load, quality
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

def main():
    logging.info("Pipeline started")
    raw_df = extract.load_raw()
    logging.info(f"Loaded raw dataframe with {len(raw_df)} rows")
    cleaned = transform.clean_dataframe(raw_df)
    out_path = load.save_dataframe(cleaned)
    logging.info(f"Saved cleaned data to {out_path}")
    q = quality.run_checks(cleaned)
    logging.info(f"Quality verdict: {q['verdict']}, report: {q['report_path']}")
    logging.info("Pipeline finished")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    main()