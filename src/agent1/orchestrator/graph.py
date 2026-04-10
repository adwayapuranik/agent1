from langgraph.graph import StateGraph
from src.agent1.orchestrator.state import WarRoomState

from src.agent1.agents.data_agent import data_node
from src.agent1.agents.pm_agent import pm_node, pm_revision_node
from src.agent1.agents.marketing_agent import marketing_node
from src.agent1.agents.risk_agent import risk_node
from src.agent1.agents.coordinator_agent import coordinator_node


def build_graph():
    builder = StateGraph(WarRoomState)

    builder.add_node("data", data_node)
    builder.add_node("pm", pm_node)
    builder.add_node("marketing", marketing_node)
    builder.add_node("risk", risk_node)
    builder.add_node("pm_revision", pm_revision_node)
    builder.add_node("coordinator", coordinator_node)

    builder.set_entry_point("data")

    builder.add_edge("data", "pm")
    builder.add_edge("pm", "marketing")
    builder.add_edge("marketing", "risk")
    builder.add_edge("risk", "pm_revision")
    builder.add_edge("pm_revision", "coordinator")

    return builder.compile()