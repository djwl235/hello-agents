import re
from llm_base import BaseLLM

class MockLLM(BaseLLM):
    def invoke(self,messages)->str:
        last_message = ""
        if messages is None:
            return "请输入问题"
        for i in range(len(messages)-1,-1,-1):
            if messages[i]["role"] == "user" and "刚才说了什么" in messages[i]["content"]:
                for j in range(i-1,-1,-1):
                    if messages[j]["role"] == "user":
                        last_message = messages[j]
                        return f"你刚才说了：{messages[j]['content']}"
                return "我还没有找到你之前说过的话。"
            elif messages[i]["role"] == "user" and "工具执行结果" in messages[i]["content"]:
                    content = messages[i]["content"]
                    content = content.replace("工具执行结果", "", 1).strip()
                    content = content.replace("请基于工具结果给出回答。", "", 1).strip()
                    result = ""
                    m = re.search(r"内容[:：]?\s*(.*)", content)
                    if m:
                        result = m.group(1).strip()
                    else:
                        result = content
                    return f"根据工具结果，答案是：{result}"
            elif messages[i]["role"] == "user" and "##相关知识库" in messages[i]["content"]: 
                    return "根据你的学习笔记，你最近在学习 NoteTool；根据知识库，你还需要复习 ReActAgent 的 Thought-Action-Observation 循环和 RAG 的基本流程。建议下一步复习 ReActAgent 与ToolRegistry 的关系。"
            elif messages[i]["role"] == "user" and "MCP" in messages[i]["content"] and "计算" in messages[i]["content"]:
                    content = messages[i]["content"]
                    # 从文本中提取两个数字
                    numbers = re.findall(r"\d+", content)
                    if len(numbers) >= 2:
                        return f"[TOOL_CALL:mcp_add:{numbers[0]} {numbers[1]}]"
                    else:
                        return "MCP 计算需要两个数字。"
            elif messages[i]["role"] == "user" and "MCP" in messages[i]["content"] and "统计字符" in messages[i]["content"]:
                    content = messages[i]["content"]
                    # 提取 "统计字符" 后面的文本
                    match = re.search(r"统计字符\s*[:：]?\s*(.*)", content)
                    if match:
                        text = match.group(1).strip()
                        return f"[TOOL_CALL:mcp_count_chars:{text}]"
                    else:
                        return "[TOOL_CALL:mcp_count_chars:]"
            elif messages[i]["role"] == "user" and re.search(r"计算\s*[:：]?\s*[\d\s\+\-\*/\(\)\.]+", messages[i]["content"]):
                    content = messages[i]["content"]
                    match = re.search(r"计算[:：]?\s*([\d\s\+\-\*/\(\)\.]+)", content)
                    if match:
                        expression = match.group(1).strip()
                    else:
                        expression = content.replace("计算", "", 1).strip()
                    return f"[TOOL_CALL:calculator:{expression}]"
            elif messages[i]["role"] == "user" and "查找本地知识库" in messages[i]["content"]:
                    content = messages[i]["content"]
                    return f"[TOOL_CALL:rag_search:{content}]"
            elif messages[i]["role"] == "user" and "记录" in messages[i]["content"]:
                    content = messages[i]["content"]
                    note = content.replace("记录", "", 1).strip()
                    return f"[TOOL_CALL:note:add {note}]"
            elif messages[i]["role"] == "user" and "查询笔记" in messages[i]["content"]: 
                    content = messages[i]["content"]
                    query = content.replace("查询笔记", "", 1).strip()
                    return f"[TOOL_CALL:note:search {query}]"
            
            elif messages[i]["role"] == "user":
                    last_message = messages[i]
                    break
        return f"我收到了你的问题：{last_message['content']}"