import json
import yaml
import os

from src.agent1.orchestrator.graph import build_graph
from src.agent1.tools.feedback_tools import summarize_sentiment, extract_common_issues

def main():
    config = yaml.safe_load(open("config/config.yaml"))

    os.makedirs(config["data"]["output_dir"], exist_ok=True)

    feedback = json.load(open(config["data"]["feedback_path"]))
    metrics = json.load(open(config["data"]["metrics_path"]))

    print("Sample feedback:", feedback[0])
    print("Sample metric:", list(metrics.items())[0])

    graph = build_graph()

    initial_state = {
        "metrics": metrics,
        "metrics_analysis": {},
        "sentiment_summary": summarize_sentiment(feedback),
        "common_issues": extract_common_issues(feedback),
        "pm_initial": "",
        "pm_revised": "",
        "marketing_output": "",
        "risk_output": "",
        "final_output": "",
        "config": config,
    }


    result = graph.invoke(initial_state)
    output_path = os.path.join(config["data"]["output_dir"], "final_output.json")

    with open(output_path, "w") as f:
        f.write(result["final_output"])

    print("\n=== FINAL OUTPUT ===")
    print(result["final_output"])


if __name__ == "__main__":
    main()