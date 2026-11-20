import uuid
from uuid import UUID

from langchain_core.messages import SystemMessage
from ping_and_ring.config import settings
from ping_and_ring.agent.prompts.system_prompts import INTENT_CLASSIFIER

from ping_and_ring.agent.schema import IntentClassification
from ping_and_ring.agent.state import PingAndRingAgentState


class IntentClassifier:
    def __init__(self):
        self.llm = settings.task_llm_mapping.get("classify_intent", settings.fast_llm)

    def classify_intent(
        self,
        state: PingAndRingAgentState,
    ) -> PingAndRingAgentState:
        """Classify the latest customer message and update the agent state."""
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
            "intent": classification.intent.value,
            "intent_confidence": classification.confidence,
            "classification_reason": classification.reasoning,
        }
