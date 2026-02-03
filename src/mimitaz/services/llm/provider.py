from typing import Protocol, AsyncGenerator, List, Any
from dataclasses import dataclass
from pydantic import SecretStr

@dataclass
class Message:
    role: str  # "user", "assistant", "system"
    content: str

@dataclass
class StreamChunk:
    delta: str
    finish_reason: str | None = None

class LLMProvider(Protocol):
    """
    Protocol definition for Model Providers.
    Any class implementing this can be used as a backend for Mimitaz.
    """
    
    async def stream_chat(
        self, 
        messages: List[Message], 
        model: str, 
        api_key: SecretStr,
        temperature: float = 0.7
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Stream response from the provider.
        """
        ...

    async def validate_connection(self, api_key: SecretStr) -> bool:
        """
        Ping the provider to check if the key is valid.
        """
        ...
