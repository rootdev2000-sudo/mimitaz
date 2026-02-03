import os
import httpx
from typing import AsyncGenerator, List, Optional
from pydantic import SecretStr
from mimitaz.services.llm.provider import LLMProvider, Message, StreamChunk

class GenericOpenAIProvider(LLMProvider):
    """
    Generic OpenAI-compatible provider.
    Used for OpenAI, DeepSeek, Zhipu (GLM), etc.
    """
    
    def __init__(self, base_url: str = "https://api.openai.com/v1/chat/completions"):
        self.BASE_URL = base_url

    async def stream_chat(
        self, 
        messages: List[Message], 
        model: str, 
        api_key: SecretStr, 
        temperature: float = 0.7
    ) -> AsyncGenerator[StreamChunk, None]:
        
        headers = {
            "Authorization": f"Bearer {api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", self.BASE_URL, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    error_body = await response.read()
                    raise RuntimeError(f"API Error ({response.status_code}): {error_body.decode()}")

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        
                        import json
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            yield StreamChunk(delta=delta)
                        except Exception:
                            continue

    async def validate_connection(self, api_key: SecretStr) -> bool:
        # Simple ping check would go here
        return True
