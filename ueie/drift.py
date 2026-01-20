def detect_drift(previous_profile, current_profile, minor_null_threshold=5.0, major_null_threshold=20.0, unique_threshold=20.0):
    # Detect column-level drift with severity classification.
    drift_report = {}

    for col, curr_meta in current_profile.items():
        prev_meta = previous_profile.get(col)

        # New column → MAJOR
        if not prev_meta:
            drift_report[col] = {
                "severity": "MAJOR",
                "type": "NEW_COLUMN",
                "message": "Column not present in previous run"
            }
            continue

        issues = []
        severity = "MINOR"

        # Null % drift
        null_diff = abs(curr_meta["null_pct"] - prev_meta["null_pct"])
        if null_diff > major_null_threshold:
            severity = "MAJOR"
            issues.append(
                f"Null % changed from {prev_meta['null_pct']} to {curr_meta['null_pct']}"
            )
        elif null_diff > minor_null_threshold:
            issues.append(
                f"Null % changed from {prev_meta['null_pct']} to {curr_meta['null_pct']}"
            )

        # Uniqueness drift
        unique_diff = abs(curr_meta["unique_pct"] - prev_meta["unique_pct"])
        if unique_diff > unique_threshold:
            severity = max(severity, "MAJOR")
            issues.append(
                f"Uniqueness % changed from {prev_meta['unique_pct']} to {curr_meta['unique_pct']}"
            )

        # Type drift → CRITICAL
        if curr_meta["dtype"] != prev_meta["dtype"]:
            drift_report[col] = {
                "severity": "CRITICAL",
                "type": "TYPE_CHANGE",
                "message": f"Dtype changed from {prev_meta['dtype']} to {curr_meta['dtype']}"
            }
            continue

        if issues:
            drift_report[col] = {
                "severity": severity,
                "type": "DRIFT",
                "issues": issues
            }

    # Removed columns → CRITICAL
    for col in previous_profile:
        if col not in current_profile:
            drift_report[col] = {
                "severity": "CRITICAL",
                "type": "REMOVED_COLUMN",
                "message": "Column missing in current run"
            }
    return drift_report