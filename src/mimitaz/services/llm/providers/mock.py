import asyncio
from typing import AsyncGenerator, List
from pydantic import SecretStr
from mimitaz.services.llm.provider import LLMProvider, Message, StreamChunk

class MockProvider(LLMProvider):
    """
    A fake provider for testing UI flows without spending money.
    Mimics the streaming behavior of GPT-4.
    """
    
    async def stream_chat(
        self, 
        messages: List[Message], 
        model: str, 
        api_key: SecretStr, 
        temperature: float = 0.7
    ) -> AsyncGenerator[StreamChunk, None]:
        
        # Simulating "Thinking" latency
        await asyncio.sleep(0.5)
        
        response_text = (
            "This is a **simulated response** from the *Mock Provider*.\n\n"
            "I act like a real LLM to test the UI pipeline.\n"
            "- I stream tokens.\n"
            "- I respect Markdown.\n"
            "- I am free to use.\n\n"
            "```python\n"
            "def hello_world():\n"
            "    print('Mimitaz is ready.')\n"
            "```"
        )
        
        # Stream character by character to simulate token generation
        for char in response_text:
            yield StreamChunk(delta=char)
            # Random jitter for realism
            await asyncio.sleep(0.01)
            
        yield StreamChunk(delta="", finish_reason="stop")

    async def validate_connection(self, api_key: SecretStr) -> bool:
        return True
