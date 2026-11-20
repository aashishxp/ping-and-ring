import uuid
from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from ping_and_ring.config import settings

from ping_and_ring.agent.schema import IntentClassification
from ping_and_ring.agent.state import PingAndRingAgentState


def _resolve_conversation_id(state: PingAndRingAgentState) -> UUID:
    """Resolve the conversation ID from the agent state."""
    conversation_id = state.get("conversation_id", None)
    if not conversation_id:
        conversation_id = uuid.uuid4()
        return conversation_id
    return conversation_id

def classify_intent(
    state: PingAndRingAgentState,
) -> dict[str, str | float]:
    """Classify the latest customer message and update the agent state."""

    # Resolve conversation ID and Update state
    conversation_id = _resolve_conversation_id(state)
    state["conversation_id"] = conversation_id

    latest_message = state["messages"][-1]
    if latest_message is None:
        raise ValueError("Cannot classify intent without a human message.")

    # llm
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
=======
import uuid
from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from ping_and_ring.config import settings

from ping_and_ring.agent.schema import IntentClassification
from ping_and_ring.agent.state import PingAndRingAgentState


def _resolve_conversation_id(state: PingAndRingAgentState) -> UUID:
    """Resolve the conversation ID from the agent state."""
    conversation_id = state.get("conversation_id", None)
    if not conversation_id:
        conversation_id = uuid.uuid4()
        return conversation_id
    return conversation_id

def classify_intent(
    state: PingAndRingAgentState,
) -> dict[str, str | float]:
    """Classify the latest customer message and update the agent state."""

    # Resolve conversation ID and Update state
    conversation_id = _resolve_conversation_id(state)
    state["conversation_id"] = conversation_id

    latest_message = state["messages"][-1]
    if latest_message is None:
        raise ValueError("Cannot classify intent without a human message.")

    # llm
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
