import re
from typing import Optional
from message import Message
from tools.registry import ToolRegistry
class SimpleAgent:
    def __init__(self,name:str,llm,system_prompt:Optional[str]=None,tool_registry:Optional[ToolRegistry]=None,max_iterations=5):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt or "你是一位有用的人工智能助手"
        self._history = []
        self.tool_registry = tool_registry
        self.max_iterations = max_iterations
        self.last_steps = []
    def run(self,input_text:str):
        steps = []
        current_iterations=0
        system_prompt = self.system_prompt
        if self.tool_registry:
            system_prompt += "\n\n你可以使用以下工具：\n"
            system_prompt += self.tool_registry.get_tools_description()
            system_prompt += """\n\n  如果需要调用工具，只能输出：
                                [TOOL_CALL:工具名:参数]
                                不要解释，不要加 Markdown，不要输出多个格式。
                                如果已经看到工具执行结果，请直接给最终答案，不要再次调用工具。"""
        messages = []
        messages.append({"role":"system","content":system_prompt})
        for message in self._history:
            messages.append({"role":message.role,"content":message.content})
        messages.append({"role":"user","content":input_text})

        
        while current_iterations < self.max_iterations:
            response = self.llm.invoke(messages)
            tool_call = self.parse_tool_call(response)
            if tool_call and self.tool_registry:
                current_iterations+=1
                tool_result = self.tool_registry.execute(tool_call["tool_name"],tool_call["tool_input"])
                clean_response = response.replace(tool_call["raw"], "").strip()
                messages.append({"role": "assistant", "content": clean_response})
                messages.append({"role": "user", "content": f"工具执行结果：{tool_result}\n请基于工具结果给出回答。"})

                steps.append({
                "steps":current_iterations,
                "llm_output":response,
                "tool_name":tool_call["tool_name"],
                "tool_input":tool_call["tool_input"],
                "observation":tool_result
            })
                tool_result = None
            else:
                steps.append({
                "steps":current_iterations+1,
                "llm_output":response,
                "tool_name":None,
                "tool_input":None,
                "observation":None
            })
                break
            
        self.last_steps = steps   
        self._history.append(Message(role = "user",content = input_text))
        self._history.append(Message(role = "assistant",content = response))
        for step in steps:
            print(f"Step{step["steps"]}\nLLM输出：{step["llm_output"]}\nAction：{step["tool_name"]}\nAction Input：{step["tool_input"]}\nObservation：{step["observation"]}")
        return response
    def get_history(self):
        return self._history
    def parse_tool_call(self, text):
        pattern = r"\[TOOL_CALL:([^:]+):([^\]]+)\]"
        match = re.search(pattern, text)

        if not match:
            return None

        return {
            "tool_name": match.group(1).strip(),
            "tool_input": match.group(2).strip(),
            "raw": match.group(0)
        }
    def get_last_steps(self):
        return self.last_steps