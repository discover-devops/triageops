"""Configuration: every value comes from the environment. Nothing is hardcoded."""
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "dev"
    log_level: str = "INFO"
    ai_api_url: str = "http://localhost:9000/classify"
    ai_timeout_seconds: float = 3.0
    ai_api_key: SecretStr          # no default: the service refuses to start without it


settings = Settings()
