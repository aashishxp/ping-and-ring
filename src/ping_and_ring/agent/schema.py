from pydantic import BaseModel, Field, model_validator
from enum import Enum


class Intent(str, Enum):
    PRODUCT = "product"
    ORDER = "order"
    RETURNS = "returns"
    POLICY = "policy"
    ESCALATION = "escalation"
    GENERAL = "general"


class SubIntent(str, Enum):

    # Product
    PRODUCT_RECOMMENDATION = "product_recommendation"
    PRODUCT_INFORMATION = "product_information"
    PRODUCT_USAGE = "product_usage"
    PRODUCT_COMPATIBILITY = "product_compatibility"
    PRODUCT_SHELF_LIFE = "product_shelf_life"

    # Order
    ORDER_STATUS = "order_status"
    ORDER_TRACKING = "order_tracking"
    ORDER_CANCELLATION = "order_cancellation"
    ORDER_MODIFICATION = "order_modification"
    ORDER_DELIVERY_ISSUE = "order_delivery_issue"

    # Returns
    RETURN_ELIGIBILITY = "return_eligibility"
    RETURN_REQUEST = "return_request"
    REPLACEMENT_REQUEST = "replacement_request"
    REFUND_QUERY = "refund_query"
    STORE_CREDIT_QUERY = "store_credit_query"

    # Policy
    SHIPPING_POLICY = "shipping_policy"
    PAYMENT_POLICY = "payment_policy"
    OFFERS_POLICY = "offers_policy"
    BUNDLE_POLICY = "bundle_policy"
    GENERAL_RETURN_POLICY = "general_return_policy"

    # Escalation
    HUMAN_AGENT_REQUEST = "human_agent_request"
    PRODUCT_SAFETY_ISSUE = "product_safety_issue"
    PAYMENT_DISPUTE = "payment_dispute"
    DELIVERY_DISPUTE = "delivery_dispute"
    FORMAL_COMPLAINT = "formal_complaint"

    # General
    GREETING = "greeting"
    GOODBYE = "goodbye"
    BRAND_INFORMATION = "brand_information"
    CONTACT_INFORMATION = "contact_information"
    UNCLEAR_REQUEST = "unclear_request"

class IntentClassification(BaseModel):

    intent: Intent = Field(
        description="The primary customer support category."
    )

    sub_intent: SubIntent = Field(
        description="The specific customer request. Must belong to the selected intent."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )

    reasoning: str = Field(
        description="Brief explanation for the classification."
    )

    @model_validator(mode="after")
    def validate_sub_intent(self):

        mapping = {
            Intent.PRODUCT: {
                SubIntent.PRODUCT_RECOMMENDATION,
                SubIntent.PRODUCT_INFORMATION,
                SubIntent.PRODUCT_USAGE,
                SubIntent.PRODUCT_COMPATIBILITY,
                SubIntent.PRODUCT_SHELF_LIFE,
            },
            Intent.ORDER: {
                SubIntent.ORDER_STATUS,
                SubIntent.ORDER_TRACKING,
                SubIntent.ORDER_CANCELLATION,
                SubIntent.ORDER_MODIFICATION,
                SubIntent.ORDER_DELIVERY_ISSUE,
            },
            Intent.RETURNS: {
                SubIntent.RETURN_ELIGIBILITY,
                SubIntent.RETURN_REQUEST,
                SubIntent.REPLACEMENT_REQUEST,
                SubIntent.REFUND_QUERY,
                SubIntent.STORE_CREDIT_QUERY,
            },
            Intent.POLICY: {
                SubIntent.SHIPPING_POLICY,
                SubIntent.PAYMENT_POLICY,
                SubIntent.OFFERS_POLICY,
                SubIntent.BUNDLE_POLICY,
                SubIntent.GENERAL_RETURN_POLICY,
            },
            Intent.ESCALATION: {
                SubIntent.HUMAN_AGENT_REQUEST,
                SubIntent.PRODUCT_SAFETY_ISSUE,
                SubIntent.PAYMENT_DISPUTE,
                SubIntent.DELIVERY_DISPUTE,
                SubIntent.FORMAL_COMPLAINT,
            },
            Intent.GENERAL: {
                SubIntent.GREETING,
                SubIntent.GOODBYE,
                SubIntent.BRAND_INFORMATION,
                SubIntent.CONTACT_INFORMATION,
                SubIntent.UNCLEAR_REQUEST,
            },
        }

        if self.sub_intent not in mapping[self.intent]:
            raise ValueError(
                f"{self.sub_intent.value} is not valid for {self.intent.value}"
            )

        return self