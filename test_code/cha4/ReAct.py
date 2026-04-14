import re
from llm_client import HelloAgentsLLM
from tools import search,ToolExecutor
REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用工具。
- `Finish[最终答案]`：当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。


现在，请开始解决以下问题：
Question: {question}
History: {history}
"""
class ReActAgent:
    def __init__(self,llm_client:HelloAgentsLLM,toolExecutor:ToolExecutor,max_steps:int = 5):
        self.llm_client=llm_client
        self.toolExecutor=toolExecutor
        self.max_steps=max_steps
        self.history=[]
    def run(self,question:str):
        self.history=[]
        current_step=0
        while current_step<self.max_steps:
            current_step+=1
            print(f"当前是第{current_step}步")
            tool_desc=self.toolExecutor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt=REACT_PROMPT_TEMPLATE.format(
                tools=tool_desc,
                question=question,
                history=history_str
            )
            messages=[{"role":"user","content":prompt}]
            response_text=self.llm_client.think(messages=messages)
            if not response_text:
                print("LLM响应错误")
                break
            thought,action = self._parse_output(response_text)
            if thought:
                print(f"思考：{thought}")
            if not action:
                print("未解析出action，流程终止")
                break
            if action.startswith("Finish"):
                finish_match = re.match(r"Finish\[(.*)\]\s*$", action, re.DOTALL)
                if not finish_match:
                    print(f"Finish格式错误：{action}")
                    break
                final_answer = finish_match.group(1).strip()
                print(f"最终答案：{final_answer}")
                return final_answer
            tool_name,tool_input=self._parse_action(action)
            if tool_name == None or tool_input==None:
                print(f"action解析错误{tool_name}{tool_input}")
                break
            print(f"行动: {tool_name}[{tool_input}]")
            tool_func=self.toolExecutor.getTool(tool_name)
            if not tool_func:
                observation = f"错误，未找到{tool_name}工具"
            else:
                observation = tool_func(tool_input)
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")
        print("已达到最大步数，流程终止")
        return None
        
    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。
        """
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None
if __name__ == '__main__':
    toolExecutor=ToolExecutor()
    toolExecutor.registerTool("Search","一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。",search)
    llm_client = HelloAgentsLLM()
    agent = ReActAgent(llm_client=llm_client,toolExecutor=toolExecutor)
    question="英伟达最新显卡"
    agent.run(question=question)
