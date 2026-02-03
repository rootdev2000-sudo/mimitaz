from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import json

# GLM-style config persistence
CONFIG_FILE = Path.home() / ".mimitaz_config.json"

def load_json_config() -> Dict[str, Any]:
    """
    Load settings from the ~/.mimitaz_config.json file.
    Maps keys like "openai.api_key" to "openai_api_key".
    """
    if not CONFIG_FILE.exists():
        return {}
    
    try:
        data = json.loads(CONFIG_FILE.read_text())
        # Normalize keys: "openai.api_key" -> "openai_api_key" for Pydantic
        normalized = {}
        for k, v in data.items():
            if k == "provider": normalized["provider"] = v
            if k == "model": normalized["model"] = v
            if k == "openai.api_key": normalized["openai_api_key"] = v
            if k == "anthropic.api_key": normalized["anthropic_api_key"] = v
            if k == "zhipu.api_key": normalized["zhipu_api_key"] = v
        return normalized
    except Exception:
        return {} # Fail silently for CLI resilience

class Settings(BaseSettings):
    """
    Application Configuration.
    Priority: Env Vars > JSON Config File > Defaults
    """
    
    debug: bool = Field(default=False)
    
    # Model Provider Config
    provider: str = Field(default="openai") # Default to openai
    model: str = Field(default="gpt-4o")
    
    # API Keys
    openai_api_key: Optional[SecretStr] = Field(default=None, alias="MIMITAZ_OPENAI_KEY")
    anthropic_api_key: Optional[SecretStr] = Field(default=None, alias="MIMITAZ_ANTHROPIC_KEY")
    zhipu_api_key: Optional[SecretStr] = Field(default=None, alias="MIMITAZ_ZHIPU_KEY")
    
    model_config = SettingsConfigDict(
        env_prefix="MIMITAZ_",
        env_file=".env",
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Any,
        init_settings: Any,
        env_settings: Any,
        dotenv_settings: Any,
        file_secret_settings: Any,
    ) -> tuple:
        # Inject our JSON loader into the Pydantic source chain
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            load_json_config, 
            file_secret_settings,
        )

    def get_api_key(self) -> SecretStr:
        """Helper to get the key for the active provider."""
        if self.provider == "mock":
             return SecretStr("mock")

        if self.provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OpenAI Key missing. Run: mim config set openai.api_key sk-...")
            return self.openai_api_key
            
        elif self.provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("Anthropic Key missing. Run: mim token set <key>")
            return self.anthropic_api_key
            
        elif self.provider in ("zhipu", "glm"):
            if not self.zhipu_api_key:
                raise ValueError("GLM/Zhipu Key missing. Run: mim token set <key>")
            return self.zhipu_api_key
            
        raise ValueError(f"Unknown provider: {self.provider}")

# Global settings singleton
settings = Settings()
