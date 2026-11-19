from langgraph.graph import END, START, StateGraph

from ping_and_ring.agent.nodes import intent_classification_node
from ping_and_ring.agent.state import PingAndRingAgentState

graph_builder = StateGraph(PingAndRingAgentState)
graph_builder.add_node("intent_classification", intent_classification_node)
graph_builder.add_edge(START, "intent_classification")
graph_builder.add_edge("intent_classification", END)

graph = graph_builder.compile()


if __name__ == "__main__":
    graph.invoke("i want to return my order because it arrived damaged.")