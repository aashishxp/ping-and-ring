# schema.py
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from ping_and_ring.constants import ENV_FILE_PATH


# ::::::: App ::::::::
class AppDetails(BaseModel):
    name: str
    version: str
    description: str


# ::::: Secrets ::::::::
class SecretSettings(BaseSettings):
    """Loads and validates keys strictly from the local environment or .env file."""
    # API Keys
    google_api_key: SecretStr
    openai_api_key: SecretStr
    groq_api_key: SecretStr

    # Instructs Pydantic to look for the file path provided by constants.py
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",  # Keeps system environment noise isolated
    )
