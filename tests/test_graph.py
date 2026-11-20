from ping_and_ring.agent.graph import PingAndRingAgentGraph


def test_graph_can_be_compiled_more_than_once():
    agent_graph = PingAndRingAgentGraph()

    first_graph = agent_graph.graph
    second_graph = agent_graph.compile_graph()

    assert first_graph is not None
    assert second_graph is not None
