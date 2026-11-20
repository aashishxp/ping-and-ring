# llm_factory.py
import sys
from abc import ABC, abstractmethod

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from ping_and_ring.utils.exception import CustomException
from ping_and_ring.utils.logger import get_logger


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, provider_name: str, model_id: str):
        self.provider_name: str = provider_name
        self.model_id: str = model_id

    @abstractmethod
    def get_chat_model(self, **kwargs) -> BaseChatModel:
        """Instantiates and returns the configured LangChain chat model wrapper."""
        raise NotImplementedError("Subclasses must implement this method.")

    def __repr__(self) -> str:
        return f"<LLMProvider(provider_name={self.provider_name}, model_id={self.model_id})>"


class GoogleLLMProvider(LLMProvider):
    """Concrete implementation for Google LLM provider."""

    def __init__(self, provider_name: str, model_id: str):
        super().__init__(provider_name, model_id)
        self.logger = get_logger(name="model_garden/llm_factory: GoogleLLMProvider")

    def get_chat_model(self, **kwargs) -> ChatGoogleGenerativeAI:
        try:
            llm = ChatGoogleGenerativeAI(model=self.model_id, **kwargs)
            return llm
        except Exception as e:
            self.logger.error("Failed to instantiate a LLM from Google!")
            raise CustomException(e, sys) from e


class OpenAILLMProvider(LLMProvider):
    """Concrete implementation for OpenAI LLM provider."""

    def __init__(self, provider_name: str, model_id: str):
        super().__init__(provider_name, model_id)
        self.logger = get_logger(name="model_garden/llm_factory: OpenAILLMProvider")

    def get_chat_model(self, **kwargs) -> BaseChatModel:
        try:
            llm = ChatOpenAI(model=self.model_id, **kwargs)
            return llm
        except Exception as e:
            self.logger.error("Failed to instantiate a LLM from OpenAI!")
            raise CustomException(e, sys) from e


class GroqLLMProvider(LLMProvider):
    """Concrete implementation for Groq LLM provider."""
    def __init__(self, provider_name: str, model_id: str):
        super().__init__(provider_name, model_id)
        self.logger = get_logger(name="model_garden/llm_factory: GroqLLMProvider")

    def get_chat_model(self, **kwargs) -> BaseChatModel:
        try:
            llm = ChatGroq(model=self.model_id, **kwargs)
            return llm
        except Exception as e:
            self.logger.error("Failed to instantiate a LLM from Groq!")
            raise CustomException(e, sys) from e