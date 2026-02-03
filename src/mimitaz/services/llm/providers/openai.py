from mimitaz.services.llm.providers.generic import GenericOpenAIProvider

class OpenAIProvider(GenericOpenAIProvider):
    """
    Production-ready OpenAI integration.
    """
    def __init__(self):
        super().__init__(base_url="https://api.openai.com/v1/chat/completions")


    async def validate_connection(self, api_key: SecretStr) -> bool:
        headers = {"Authorization": f"Bearer {api_key.get_secret_value()}"}
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.openai.com/v1/models", headers=headers)
            return resp.status_code == 200
