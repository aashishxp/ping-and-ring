from typing import Annotated, Literal, NotRequired, Required
from uuid import UUID

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import Doc, TypedDict


class PingAndRingAgentState(TypedDict, total=False):
    """
    Represents the state of a customer support interaction with BareONN's ping-and-ring Agent.
    """
    # 1. Conversation
    conversation_id: Required[
        Annotated[
            UUID,
            Doc("Unique identifier for the conversation, used to track and retrieve the interaction history."),
        ]
    ]
    messages: Required[
            Annotated[
                list[AnyMessage],
                add_messages,
                Doc(
                    "Complete conversation history between the customer and BareONN AI, "
                    "reduced to recent + summary when chat grows long."
                ),
            ]
        ]
    channel: NotRequired[
        Annotated[
            Literal["chat", "voice"],
            Doc("Channel through which the customer is interacting with BareONN."),
        ]
    ]

    # 2. Intent classification
    intent: NotRequired[
        Annotated[
            str,
            Doc("Primary customer support intent. One of: product, order, returns, policy, escalation, general."),
        ]
    ]
    sub_intent: NotRequired[
        Annotated[
            str,
            Doc("Specific customer request belonging to the selected primary intent."),
        ]
    ]
    intent_confidence: NotRequired[
        Annotated[
            float,
            Doc("LLM confidence score for the intent classification, between 0 and 1."),
        ]
    ]
    classification_reason: NotRequired[
        Annotated[
            str,
            Doc("Brief explanation of why the intent and sub-intent were selected."),
        ]
    ]
