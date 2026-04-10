from src.agent1.tools.metrics_tools import analyze_trends, detect_anomalies

def data_node(state):
    logger = state["logger"]
    logger.log("[DataAgent] Running...")

    metrics = state["metrics"]
    state["metrics_analysis"] = {
        "trends": analyze_trends(metrics),
        "anomalies": detect_anomalies(metrics)
    }
    return state