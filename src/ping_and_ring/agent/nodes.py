import uuid
from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from ping_and_ring.config import settings
from ping_and_ring.agent.prompts.system_prompts import INTENT_CLASSIFIER

from ping_and_ring.agent.schema import IntentClassification
from ping_and_ring.agent.state import PingAndRingAgentState


class IntentClassifier:
    def __init__(self):
        self.llm = settings.task_llm_mapping.get("classify_intent", settings.fast_llm)

    def _resolve_conversation_id(self, state: PingAndRingAgentState) -> UUID:
        """Resolve the conversation ID from the agent state."""
        conversation_id = state.get("conversation_id", None)
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            return conversation_id
        return conversation_id

    def classify_intent(
        self,
        state: PingAndRingAgentState,
    ) -> PingAndRingAgentState:
        """Classify the latest customer message and update the agent state."""

        # Resolve conversation ID and Update state
        conversation_id = self._resolve_conversation_id(state)

        # Get the latest human message from the agent state
        latest_message = state["messages"][-1]
        if latest_message is None:
            raise ValueError("Cannot classify intent without a human message.")

        # llm with structured output for intent classification
        structured_llm = self.llm.with_structured_output(IntentClassification)
        
        # Classify the intent of the latest message using the structured LLM
        classification = structured_llm.invoke(
            [
                SystemMessage(
                    content=INTENT_CLASSIFIER
                ),
                latest_message,
            ]
        )

        if not isinstance(classification, IntentClassification):
            raise TypeError("The intent classifier returned an unexpected output type.")

        return {
            "conversation_id": conversation_id,
            "messages": state["messages"],
            "intent": classification.intent.value,
            "intent_confidence": classification.confidence,
            "classification_reason": classification.reasoning,
        }
