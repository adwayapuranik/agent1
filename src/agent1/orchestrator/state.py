from typing import TypedDict, Dict, Any

class WarRoomState(TypedDict):
    metrics: Dict[str, Any]
    metrics_analysis: Dict[str, Any]
    sentiment_summary: Dict[str, Any]
    common_issues: list
    pm_initial: str
    pm_revised: str
    marketing_output: str
    risk_output: str
    final_output: str
    config: Dict[str, Any]  
    logger: Any     