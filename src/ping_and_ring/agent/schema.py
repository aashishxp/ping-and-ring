from typing import Optional

from pydantic import BaseModel, Field, model_validator
from enum import Enum


class Intent(str, Enum):
    PRODUCT: str = "product"
    ORDER: str = "order"
    RETURNS: str = "returns"
    POLICY: str = "policy"
    ESCALATION: str = "escalation"
    GENERAL: str = "general"


class IntentClassification(BaseModel):
    """
    Represents the classification of a customer's intent in a customer support interaction.
    """
    intent: Intent = Field(
        description="The primary customer support category."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )
    reasoning: str = Field(
        description="Brief explanation for the classification."
    )