import os
import pandas as pd

def detect_file_info(file_path):
    return {
        "file_name": os.path.basename(file_path),
        "file_size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
        "extension": os.path.splitext(file_path)[1].lower()
    }