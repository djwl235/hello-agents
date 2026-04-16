import os
from typing import Optional
from openai import OpenAI
from hello_agents import HelloAgentsLLM
class MyLLM(HelloAgentsLLM):
    def __init__(self,model : Optional[str]=None,api_key :Optional[str]=None,base_url:Optional[str]=None,provider:Optional[str]=None,**kwargs):
        if provider=="modelscope":
            print("正在使用自定义的魔搭Provider")
            self.provider="modelscope"
            self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
            self.base_url = base_url or "https://api-inference.modelscope.cn/v1/"
            if not self.api_key:
                raise ValueError("ModelScope API key not found. Please set MODELSCOPE_API_KEY environment variable.")
            self.model = model or os.getenv("LLM_MODEL_ID") or "Qwen/Qwen3.5-35B-A3B"
            self.temperature = kwargs.get('temperature', 0.7)
            self.max_tokens = kwargs.get('max_tokens')
            self.timeout = kwargs.get('timeout',60)
            self._client = OpenAI(api_key=self.api_key,base_url=self.base_url,timeout=self.timeout)
        else:
            super.__init__(model=model, api_key=api_key, base_url=base_url, provider=provider, **kwargs)