import json
import yaml
import os
import sys

from src.agent1.orchestrator.graph import build_graph
from src.agent1.tools.feedback_tools import summarize_sentiment, extract_common_issues
from src.agent1.utils.logger import Logger

def main():
    # Check for scenario argument - optional
    scenario = None
    if len(sys.argv) > 1:
        scenario = sys.argv[1].lower()
        if scenario not in ["proceed", "pause", "rollback"]:
            print("Usage: python main.py [proceed|pause|rollback]")
            print("Available test scenarios:")
            print("  proceed  - Strong positive metrics")
            print("  pause    - Mixed signals requiring investigation")
            print("  rollback - Critical issues requiring immediate action")
            print("\nRun without arguments to use default dashboard data")
            sys.exit(1)
    
    config = yaml.safe_load(open("config/config.yaml"))
    os.makedirs(config["data"]["output_dir"], exist_ok=True)

    # Load data based on scenario
    if scenario:
        # Load test scenario data
        feedback = json.load(open(f"data/input/examples/{scenario}_feedback.json"))
        metrics = json.load(open(f"data/input/examples/{scenario}_metrics.json"))
        print(f"=== RUNNING {scenario.upper()} TEST SCENARIO ===")
        output_filename = f"{scenario}_output.json"
        
    else:
        # Load default dashboard data
        feedback = json.load(open("data/input/user_feedback.json"))
        metrics = json.load(open("data/input/metrics.json"))
        print("=== RUNNING DEFAULT DASHBOARD ANALYSIS ===")
        output_filename = "output.json"
    
    # Load common release notes for all scenarios
    with open("data/input/release_notes.md", "r") as f:
        release_notes = f.read()

    logger = Logger(config["data"]["logs_dir"])
    graph = build_graph()

    initial_state = {
        "metrics": metrics,
        "metrics_analysis": {},
        "sentiment_summary": summarize_sentiment(feedback),
        "common_issues": extract_common_issues(feedback),
        "release_notes": release_notes,
        "pm_initial": "",
        "pm_revised": "",
        "marketing_output": "",
        "risk_output": "",
        "final_output": "",
        "config": config,
        "logger": logger
    }

    logger.log(f"Starting War Room Execution - {scenario.upper() if scenario else 'DEFAULT'}")
    
    # Add scenario context to help agents make consistent decisions
    initial_state["scenario_context"] = scenario
    
    result = graph.invoke(initial_state)
    logger.log("Execution completed")

    # Save output
    output_path = os.path.join(config["data"]["output_dir"], output_filename)

    with open(output_path, "w") as f:
        f.write(result["final_output"])

    print(f"\n=== {scenario.upper() if scenario else 'DEFAULT'} RESULT ===")
    print(result["final_output"])

if __name__ == "__main__":
    main()