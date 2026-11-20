# config.py
from ping_and_ring.agent.model_garden.llm_factory import (
    GoogleLLMProvider,
    OpenAILLMProvider,
    GroqLLMProvider
)
from ping_and_ring.constants import APP_CONFIG_FILE_PATH
from ping_and_ring.schema import AppDetails, SecretSettings
from ping_and_ring.utils.common import CommonUtils

# Registry for LLM providers
_PROVIDER_REGISTRY = {
    "google": GoogleLLMProvider,
    "openai": OpenAILLMProvider,
    "groq": GroqLLMProvider,
}


class AppSettings:
    def __init__(self):
        # 1. Load data into stateful instance variables so other methods can access them
        self._raw_config = CommonUtils().read_file(APP_CONFIG_FILE_PATH)
        self._secret_settings = SecretSettings()

        # 2. Extract base components
        self.app_details = AppDetails(**self._raw_config["app"])
        self._llm_defaults = self._raw_config["llm"]["defaults"]
        self._performance_tiers = self._raw_config["llm"]["performance_tiers"]

        # 3. Instantiate the configured LLMs
        self.fast_llm = self._init_llm_by_tier(performance_tier="fast")
        self.balanced_llm = self._init_llm_by_tier(performance_tier="balanced")
        self.expert_llm = self._init_llm_by_tier(performance_tier="expert")

        # 4. Map tasks to LLMs based on the configuration
        self.task_llm_mapping = {}
        for task, config in self._raw_config.get("task_llm_mapping", {}).items():
            tier = config.get("tier")
            if tier not in self._performance_tiers:
                raise ValueError(f"Unknown performance tier '{tier}' for task '{task}'")
            self.task_llm_mapping[task] = getattr(self, f"{tier}_llm")

    def _init_llm_by_tier(self, performance_tier: str):
        """Merges defaults with tier overrides, fetches API keys safely, and initializes the provider."""
        if performance_tier not in self._performance_tiers:
            raise ValueError(f"Unknown performance tier: {performance_tier}")

        tier_data = self._performance_tiers[performance_tier]

        # 1. Extract provider and model info
        provider_name, model_id = tier_data["model"].split(":")

        # 2. Look up the provider class dynamically from the registry
        provider_class = _PROVIDER_REGISTRY.get(provider_name)
        if not provider_class:
            supported = ", ".join(_PROVIDER_REGISTRY.keys())
            raise ValueError(f"Unsupported provider: {provider_name}. Supported are: {supported}")

        # 3. Safely look up the API key attribute
        secret_key_attr = f"{provider_name}_api_key"
        secret_field = getattr(self._secret_settings, secret_key_attr, None)

        if not secret_field:
            raise AttributeError(f"SecretSettings is missing the required field: {secret_key_attr}")

        api_key = secret_field.get_secret_value()

        # 4. Dynamically instantiate and initialize the model
        return provider_class(provider_name=provider_name, model_id=model_id).get_chat_model(api_key=api_key)

    def __repr__(self) -> str:
        return (
            f"<AppSettings("
            f"app_name={self.app_details.name}, "
            f"version={self.app_details.version}, "
            f"llm_tiers={self._performance_tiers}"
            f")>"
        )


# Single instantiation to prevent multi-read disk overhead
settings = AppSettings()
