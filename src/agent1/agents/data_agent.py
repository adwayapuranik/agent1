from src.agent1.tools.metrics_tools import analyze_trends, detect_anomalies

def data_node(state):
    logger = state["logger"]
    logger.log("[DataAgent] Running...")

    metrics = state["metrics"]
    metrics_data = metrics.get("metrics", {})
    
    state["metrics_analysis"] = {
        "trends": analyze_trends(metrics_data),
        "anomalies": detect_anomalies(metrics_data),
        "raw_metrics": metrics_data
    }
    return state