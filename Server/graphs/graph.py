from langgraph.graph import StateGraph, END
from graphs.nodes.interview import interview_node
from graphs.state import AgentState
from graphs.nodes.research import research_node


def build_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("research", research_node)
    graph.add_node("interview", interview_node)


    graph.set_entry_point("research")

    
    graph.add_edge("research", "interview")
    graph.add_edge("interview", END)

    return graph.compile()