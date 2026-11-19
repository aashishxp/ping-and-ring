from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from ping_and_ring.agent.schema import IntentClassification
from ping_and_ring.agent.state import PingAndRingAgentState


def intent_classification_node(
    state: PingAndRingAgentState,
    llm: BaseChatModel | None = None,
) -> dict[str, str | float]:
    """Classify the latest customer message and update the agent state."""
    latest_message = next(
        (message for message in reversed(state["messages"]) if isinstance(message, HumanMessage)),
        None,
    )
    if latest_message is None:
        raise ValueError("Cannot classify intent without a human message.")

    if llm is None:
        from ping_and_ring.config import settings

        llm = settings.fast_llm

    structured_llm = llm.with_structured_output(IntentClassification)
    classification = structured_llm.invoke(
        [
            SystemMessage(
                content=(
                    "Classify the customer's latest message for a customer support agent. "
                    "Select one primary intent and the sub-intent that belongs to it."
                )
            ),
            latest_message,
        ]
    )

    if not isinstance(classification, IntentClassification):
        raise TypeError("The intent classifier returned an unexpected output type.")

    return {
        "intent": classification.intent.value,
        "sub_intent": classification.sub_intent.value,
        "intent_confidence": classification.confidence,
        "classification_reason": classification.reasoning,
    }
