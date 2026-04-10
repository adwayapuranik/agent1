def _extract_text(item):
    if isinstance(item, str):
        return item
    elif isinstance(item, dict):
        return item.get("text", "")
    return ""

def summarize_sentiment(feedback):
    neg_keywords = ["crash", "bug", "slow", "fail"]

    texts = [_extract_text(f).lower() for f in feedback]

    neg = [t for t in texts if any(k in t for k in neg_keywords)]
    pos = [t for t in texts if t not in neg]

    return {"positive": len(pos), "negative": len(neg)}

def extract_common_issues(feedback):
    issues = set()

    for f in feedback:
        t = _extract_text(f).lower()
        if "crash" in t:
            issues.add("crashes")
        if "slow" in t:
            issues.add("performance")
        if "payment" in t:
            issues.add("payments")

    return list(issues)