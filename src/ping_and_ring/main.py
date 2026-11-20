import uuid
from ping_and_ring.agent.state import PingAndRingAgentState
from ping_and_ring.agent.graph import PingAndRingAgentGraph

def main(
    conversation_id: str,
    graph: PingAndRingAgentGraph,
):
    config = {
        "configurable": {
            "thread_id": conversation_id,
        }
    }

    while True:
        user_input = input("Enter a message (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        initial_state = PingAndRingAgentState(
            conversation_id=conversation_id,
            messages=[{"role": "human", "content": user_input}],
        )
        final_state = graph.invoke(initial_state, config=config)

        print("Final State:", final_state)
        print("\n---\n")


if __name__ == "__main__":
    conversation_id = str(uuid.uuid4())
    graph = PingAndRingAgentGraph().graph
    main(conversation_id, graph)