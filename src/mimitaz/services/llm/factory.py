from mimitaz.config import settings
from mimitaz.services.llm.provider import LLMProvider
from mimitaz.services.llm.providers.mock import MockProvider
from mimitaz.services.llm.providers.openai import OpenAIProvider
from mimitaz.services.llm.providers.anthropic import AnthropicProvider
from mimitaz.services.llm.providers.zhipu import ZhipuProvider

def get_provider() -> LLMProvider:
    """
    Factory function to return the configured provider.
    """
    if settings.debug and settings.provider == "mock":
        return MockProvider()
    
    if settings.provider == "openai":
        return OpenAIProvider()
    
    if settings.provider == "anthropic":
        return AnthropicProvider()
    
    if settings.provider in ("zhipu", "glm"):
        return ZhipuProvider()
        
    raise ValueError(f"Unknown provider '{settings.provider}'. Check your configuration.")
