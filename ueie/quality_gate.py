def apply_quality_gate(quality_score, pass_threshold=80, warn_threshold=60):
    if quality_score is None:
        return {
            "status": "FAIL",
            "reason": "Quality score is None"
        }
    if quality_score >= pass_threshold:
        return {
            "status": "PASS",
            "reason": f"Quality score {quality_score} >=  {pass_threshold}"
        }
    if quality_score >= warn_threshold:
        return {
            "status": "WARN",
            "reason": f"Quality score {quality_score} between {warn_threshold}–{pass_threshold}"
        }
    return {
        "status": "FAIL",
        "reason": f"Quality score {quality_score} < {warn_threshold}"
    }