import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
load_dotenv()
class HelloAgentsLLM:
    def __init__(self,model:str=None,apiKey:str=None,baseUrl:str=None,timeout:int=None):
        self.model=model or os.getenv("LLM_MODEL_ID")
        apiKey=apiKey or os.getenv("LLM_API_KEY")
        baseUrl=baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
        if not all([self.model,apiKey,baseUrl]):
            raise ValueError("模型配置有不完整信息")
        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)
    def think(self,messages:List[Dict[str,str]],temperature :float=0)->str:
        print("正在调用"+self.model+"进行思考")
        try:
            response=self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            print("大语言模型响应成功")
            collected_content= []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                #print(content,end="",flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)
        except Exception as e:
            print("大预言模型响应错误")
            return None
if __name__ == '__main__':
    try:
        llmClient = HelloAgentsLLM()
        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]
        print("调用LLM")
        responseText=llmClient.think(exampleMessages)
        # if responseText:
        #     print("完整模型回应")
        #     print(responseText)
    except ValueError as e:
        print(e)