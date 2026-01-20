def calculate_quality_score(profile):
    score = 100
    for col, meta in profile.items():
        score -= meta["null_pct"] * 0.2
    return max(0, round(score, 2))
