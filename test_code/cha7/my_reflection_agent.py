DEFAULT_PROMPTS = {
    "initial": """
请根据以下要求完成任务:

任务: {task}

请提供一个完整、准确的回答。
""",
    "reflect": """
请仔细审查以下回答，并找出可能的问题或改进空间:

# 原始任务:
{task}

# 当前回答:
{content}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
如果回答已经很好，请回答"无需改进"。
""",
    "refine": """
请根据反馈意见改进你的回答:

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

请提供一个改进后的回答。
"""
}
import re
from typing import Any, Optional, List, Tuple
from hello_agents import ReflectionAgent, HelloAgentsLLM, Config, Message, ToolRegistry
from memory import Memory
class MyReflectionAgent(ReflectionAgent):
    def __init__(
            self,
            name:str,
            llm:HelloAgentsLLM,
            system_prompt:str=None,
            config:Optional[Config] = None,
            max_iterations : int = 3,
            custom_prompts: Optional[dict[str, str]] = None
    ):
        super().__init__(name, llm, system_prompt, config)
        self.max_iterations = max_iterations
        self.memory=Memory()
        self.prompt_templete = custom_prompts if custom_prompts else DEFAULT_PROMPTS
    def _collect_text(self, response) -> str:
        return ''.join(response)
    def run(self,task:str,**kwargs)->str:
        print(f"\n--- 开始处理任务 ---\n任务: {task}")
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = self.prompt_templete.get('initial').format(task = task)
        message = [{"role":"user","content":initial_prompt}]
        response_text = self._collect_text(self.llm.think(messages=message))
        self.memory.add_record('execution',response_text)
        for i in range(self.max_iterations):
            print(f"正在执行{i+1}/{self.max_iterations}轮反思")
            last_execution = self.memory.get_last_execution()
            reflect_prompt = self.prompt_templete.get('reflect').format(task = task,content = last_execution)
            message = [{"role":"user","content":reflect_prompt}]
            feedback = self._collect_text(self.llm.think(messages=message))
            print(feedback)
            self.memory.add_record("reflection", feedback)
            if "无需改进" in feedback:
                print("\n✅ 反思认为代码已无需改进，任务完成。")
                break
            refine_prompt = self.prompt_templete.get("refine").format(task = task,last_attempt = last_execution,feedback=feedback)
            message = [{"role":"user","content":refine_prompt}]
            refined_response = self._collect_text(self.llm.think(messages=message))
            self.memory.add_record("execution", refined_response)
        final_answer = self.memory.get_last_execution()
        print(f"任务最终完成：{final_answer}")
        return final_answer