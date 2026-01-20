import json
import os
from datetime import datetime


def save_run_metadata(file_info, quality_score, extra_metadata=None, output_dir="processed"):
    os.makedirs(output_dir, exist_ok=True)

    metadata = {
        "run_time": datetime.utcnow().isoformat(),
        "file_info": file_info,
        "quality_score": quality_score
    }

    if extra_metadata:
        metadata.update(extra_metadata)

    output_path = os.path.join(output_dir, "run_metadata.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return output_path

def load_previous_profile(path="processed/last_profile.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_current_profile(profile, path="processed/last_profile.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
