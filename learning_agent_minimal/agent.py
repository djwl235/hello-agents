
from typing import Optional
from message import Message
class SimpleAgent:
    def __init__(self,name:str,llm,system_prompt:Optional[str]=None):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt or "你是一位有用的人工智能助手"
        self._history = []
    def run(self,input_text:str):
        messages = []
        messages.append({"role":"system","content":self.system_prompt})
        for message in self._history:
            messages.append({"role":message.role,"content":message.content})
        messages.append({"role":"user","content":input_text})
        response = self.llm.invoke(messages)
        self._history.append(Message(role="user",content=input_text))
        self._history.append(Message(role="assistant",content=response))
        return response
    def get_history(self):
        return self._history