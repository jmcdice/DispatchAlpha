from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    """

    # Load settings from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Ollama settings
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    OLLAMA_MODEL: str = "gemma:3b"

    # Database settings
    DATABASE_URL: str


# Create a single instance of the settings to be used throughout the application
settings = Settings()
