from langgraph.graph import StateGraph
from app.agents.fetch_agent import fetch_agent
from app.agents.parse_agent import parse_agent
from app.agents.filter_agent import filter_agent
from app.agents.rank_agent import rank_agent


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("fetch", fetch_agent)
    graph.add_node("parse", parse_agent)
    graph.add_node("filter", filter_agent)
    graph.add_node("rank", rank_agent)

    graph.set_entry_point("fetch")

    graph.add_edge("fetch", "parse")
    graph.add_edge("parse", "filter")
    graph.add_edge("filter", "rank")

    return graph.compile()
