from llm_base import BaseLLM
from config import Config
from typing import Optional
from openai import OpenAI
config = Config()

class RealLLM(BaseLLM):
    def __init__(self,model:Optional[str]= None,base_url:Optional[str]= None,api_key:Optional[str]= None,provider:Optional[str]= None,temperature:float = 0.7,max_tokens:Optional[int]=None,**kwargs):
        self.model = model or config.llm_model
        self.base_url = base_url or config.llm_base_url
        self.api_key = api_key or config.llm_api_key
        self.provider = provider or config.llm_provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = self._create_client()
    def _create_client(self)->OpenAI:
        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )


    def invoke(self,messages)->str:
        try:
            response = self._client.chat.completions.create(
                messages=messages,
                model = self.model
            )
            return response.choices[0].message.content
        except Exception as e:
            return (f"LLM调用失败: {str(e)}")