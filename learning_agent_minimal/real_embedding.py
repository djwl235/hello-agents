from openai import OpenAI
from embedding_base import BaseEmbedding
from config import Config
config = Config()
class RealEmbedding(BaseEmbedding):
    def __init__(self,model = None,base_url = None, api_key = None):
        self.model = model or config.embedding_model
        self.base_url = base_url or config.embedding_base_url
        self.api_key = api_key or config.embedding_api_key
        self._client = OpenAI(base_url=self.base_url,api_key = self.api_key)
    def embed(self, text):
        response = self._client.embeddings.create(
            model = self.model,
            input=text
        )
        return response.data[0].embedding