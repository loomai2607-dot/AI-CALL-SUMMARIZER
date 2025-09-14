from langgraph.graph import StateGraph
from agents.nodes import get_agent_nodes

from typing import TypedDict

from dotenv import load_dotenv

load_dotenv()

class CallState(TypedDict, total=False):
    audio_path: str
    transcript: str
    entities: dict
    summary: str
    recommendations: str



def create_call_graph():
    builder = StateGraph(state_schema=CallState)

    agents = get_agent_nodes()

    for name, node in agents.items():
        builder.add_node(name, node)

    builder.set_entry_point("transcription")
    builder.add_edge("transcription", "entity_extraction")
    builder.add_edge("entity_extraction", "summarization")
    builder.add_edge("summarization", "recommendation")
    builder.set_finish_point("recommendation")

    return builder.compile()