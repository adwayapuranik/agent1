import numpy as np

def _extract_numeric_series(series):
    if isinstance(series, (int, float)):
        return [series]

    if not isinstance(series, list):
        return []

    cleaned = []

    for item in series:
        if isinstance(item, (int, float)):
            cleaned.append(item)
        elif isinstance(item, dict):
            try:
                cleaned.append(float(item.get("value")))
            except:
                continue

    return cleaned


def analyze_trends(metrics):
    trends = {}
    for k, v in metrics.items():
        series = _extract_numeric_series(v)
        if len(series) >= 2:
            trends[k] = series[-1] - series[0]
    return trends


def detect_anomalies(metrics):
    anomalies = {}
    for k, v in metrics.items():
        series = _extract_numeric_series(v)
        if len(series) < 2:
            continue
        mean = np.mean(series)
        std = np.std(series)
        anomalies[k] = [x for x in series if abs(x - mean) > 2 * std]
    return anomalies