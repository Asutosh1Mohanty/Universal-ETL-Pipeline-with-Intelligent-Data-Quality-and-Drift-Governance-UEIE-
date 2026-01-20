def evaluate_drift_severity(drift_report):
    # Decide overall drift severity from column-level drift.
    if not drift_report:
        return {
            "status": "NO_DRIFT",
            "reason": "No drift detected"
        }
    severities = {v["severity"] for v in drift_report.values()}

    if "CRITICAL" in severities:
        return {
            "status": "CRITICAL",
            "reason": "Critical drift detected (schema/type change)"
        }
    if "MAJOR" in severities:
        return {
            "status": "MAJOR",
            "reason": "Major drift detected"
        }
    return {
        "status": "MINOR",
        "reason": "Only minor drift detected"
    }