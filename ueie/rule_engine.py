def decide_rules(profile):
    rules = {}
    for col, meta in profile.items():
        if meta["null_pct"] > 40:
            rules[col] = "drop_column"
        elif meta["dtype"].startswith("object"):
            rules[col] = "fill_unknown"
        else:
            rules[col] = "fill_zero"
    return rules