"""
etl/extract.py
- Find the latest file in raw/
- Support csv, xls, xlsx, parquet, json
- For large CSVs, optionally read in chunks and return a generator flag (handled in main)
"""
import os
import pandas as pd
from typing import Tuple, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "raw")

ALLOWED_EXTS = (".csv", ".xls", ".xlsx", ".parquet", ".json")

def ensure_raw_dir():
    os.makedirs(RAW_DIR, exist_ok=True)

def latest_raw_file() -> Optional[str]:
    ensure_raw_dir()
    files = [os.path.join(RAW_DIR, f) for f in os.listdir(RAW_DIR)]
    files = [f for f in files if os.path.isfile(f) and os.path.splitext(f)[1].lower() in ALLOWED_EXTS]
    if not files:
        return None
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files[0]

def load_file(path: str, chunked: bool = False, chunk_size: int = 100_000) -> Tuple[pd.DataFrame, dict]:
    """
    Load file into a dataframe.
    If chunked=True and file is CSV, returns (None, {"type":"csv_chunked", "path":path, "chunksize":chunk_size})
    Caller must handle chunked case.
    """
    ext = os.path.splitext(path)[1].lower()
    info = {"path": path, "ext": ext}
    if ext == ".csv":
        if chunked:
            return None, {"type": "csv_chunked", "path": path, "chunksize": chunk_size}
        df = pd.read_csv(path)
        return df, info
    if ext in (".xls", ".xlsx"):
        df = pd.read_excel(path)
        return df, info
    if ext == ".parquet":
        df = pd.read_parquet(path)
        return df, info
    if ext == ".json":
        df = pd.read_json(path, lines=True)
        return df, info
    raise ValueError(f"Unsupported file type: {ext}")

def load_latest(chunked: bool = False, chunk_size: int = 100_000):
    """
    Find latest raw file and return either a DataFrame or a chunk-descriptor.
    """
    path = latest_raw_file()
    if not path:
        raise FileNotFoundError(f"No input files found in raw/ (allowed: {ALLOWED_EXTS}). Please upload one file.")
    return load_file(path, chunked=chunked, chunk_size=chunk_size)
