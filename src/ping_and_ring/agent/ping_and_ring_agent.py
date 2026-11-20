from ping_and_ring.agent.graph import PingAndRingAgentGraph


def agent(
    conversation_id: str,
    user_input: str,
) -> dict:
    """Run the Ping and Ring agent with the given conversation ID and user input."""
    graph = PingAndRingAgentGraph().graph

    initial_state = {
        "conversation_id": conversation_id,
        "messages": [{"role": "human", "content": user_input}],
    }
    config = {
        "configurable": {
            "thread_id": conversation_id,
        }
    }

    final_state = graph.invoke(initial_state, config=config)
    
    return final_state