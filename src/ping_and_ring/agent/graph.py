import json

from langgraph.graph import END, START, StateGraph

from ping_and_ring.agent.nodes import classify_intent
from ping_and_ring.agent.state import PingAndRingAgentState

graph_builder = StateGraph(PingAndRingAgentState)
graph_builder.add_node("intent_classification", classify_intent)
graph_builder.add_edge(START, "intent_classification")
graph_builder.add_edge("intent_classification", END)

graph = graph_builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "messages": ["the product is causing irritation on my skin, i wish i could get it returned."]
        }
    )
    print(json.dumps(result, indent=2))