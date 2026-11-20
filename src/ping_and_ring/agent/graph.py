import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from ping_and_ring.agent.nodes import IntentClassifier
from ping_and_ring.agent.state import PingAndRingAgentState


class PingAndRingAgentGraph:
    def __init__(self):
        self.graph_builder = StateGraph(PingAndRingAgentState)
        self.checkpointer = InMemorySaver()
        self.add_nodes()
        self.add_edges()
        self.graph = self.compile_graph()

    def add_nodes(self):
        self.graph_builder.add_node("intent_classification", IntentClassifier().classify_intent)

    def add_edges(self):
        self.graph_builder.add_edge(START, "intent_classification")
        self.graph_builder.add_edge("intent_classification", END)

    def compile_graph(self):
        return self.graph_builder.compile(checkpointer=self.checkpointer)
