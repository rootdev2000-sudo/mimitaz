from mimitaz.services.llm.providers.generic import GenericOpenAIProvider

class ZhipuProvider(GenericOpenAIProvider):
    """
    ZhipuAI (GLM-4) Integration via OpenAI-compatible endpoint.
    """
    def __init__(self):
        # ZhipuAI's OpenAI-compatible endpoint
        super().__init__(base_url="https://open.bigmodel.cn/api/paas/v4/chat/completions")
