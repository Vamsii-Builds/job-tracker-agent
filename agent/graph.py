from langgraph.graph import StateGraph, END
from agent.state import JobState
from agent.nodes import fetch_jd, extract_requirements, store_to_db

def build_graph():
    graph = StateGraph(JobState)
    graph.add_node("fetch_jd", fetch_jd)
    graph.add_node("extract_requirements", extract_requirements)
    graph.add_node("store_to_db", store_to_db)
    graph.set_entry_point("fetch_jd")
    graph.add_edge("fetch_jd", "extract_requirements")
    graph.add_edge("extract_requirements", "store_to_db")
    graph.add_edge("store_to_db", END)
    return graph.compile()
