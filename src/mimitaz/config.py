from pathlib import Path
from typing import Optional
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application Configuration.
    - Loads from environment variables (MIMITAZ_*)
    - Loads from .env file
    - Validates strict types
    """
    
    # Core
    debug: bool = Field(default=False, description="Enable debug logging")
    
    # Model Provider Config
    provider: str = Field(default="openai", description="Active LLM provider (openai, anthropic)")
    model: str = Field(default="gpt-4-turbo-preview", description="Model identifier to use")
    
    # Secrets (Environment only recommended)
    openai_api_key: Optional[SecretStr] = Field(default=None, alias="MIMITAZ_OPENAI_KEY")
    anthropic_api_key: Optional[SecretStr] = Field(default=None, alias="MIMITAZ_ANTHROPIC_KEY")
    
    # Application Paths
    config_dir: Path = Field(default=Path.home() / ".config" / "mimitaz")
    
    model_config = SettingsConfigDict(
        env_prefix="MIMITAZ_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_api_key(self) -> SecretStr:
        """Helper to get the key for the active provider."""
        if self.provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OpenAI Provider selected but MIMITAZ_OPENAI_KEY not found.")
            return self.openai_api_key
        elif self.provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("Anthropic Provider selected but MIMITAZ_ANTHROPIC_KEY not found.")
            return self.anthropic_api_key
        raise ValueError(f"Unknown provider: {self.provider}")

# Global settings singleton
settings = Settings()
