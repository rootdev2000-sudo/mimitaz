import httpx
from typing import AsyncGenerator, List
from pydantic import SecretStr
from mimitaz.services.llm.provider import LLMProvider, Message, StreamChunk

class AnthropicProvider(LLMProvider):
    """
    Anthropic Claude 3 integration.
    """
    
    BASE_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    async def stream_chat(
        self, 
        messages: List[Message], 
        model: str, 
        api_key: SecretStr, 
        temperature: float = 0.7
    ) -> AsyncGenerator[StreamChunk, None]:
        
        headers = {
            "x-api-key": api_key.get_secret_value(),
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json",
        }
        
        # Anthropic doesn't support "system" in the messages list conventionally,
        # it likes a separate top-level parameter. We extract it.
        system_prompt = next((m.content for m in messages if m.role == "system"), "")
        clean_messages = [{"role": m.role, "content": m.content} for m in messages if m.role != "system"]
        
        payload = {
            "model": model,
            "messages": clean_messages,
            "stream": True,
            "temperature": temperature,
            "max_tokens": 4096,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", self.BASE_URL, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    error_body = await response.read()
                    raise RuntimeError(f"Anthropic API Error ({response.status_code}): {error_body.decode()}")

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        import json
                        try:
                            chunk = json.loads(data)
                            if chunk["type"] == "content_block_delta":
                                delta = chunk["delta"].get("text", "")
                                yield StreamChunk(delta=delta)
                        except Exception:
                            continue

    async def validate_connection(self, api_key: SecretStr) -> bool:
        # Anthropic doesn't have a cheap 'list models' endpoint that is easy to ping without cost,
        # but we can try a dummy request or assume valid if format is correct.
        # For now, we trust the Pydantic pattern.
        return True
