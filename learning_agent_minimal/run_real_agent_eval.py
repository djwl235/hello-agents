from learning_assistant import LearningAssistant
from real_llm import RealLLM

assistant = LearningAssistant(llm=RealLLM())

cases = [
    "请计算 12 + 30 / 3",
    "请计算 8 * 9",
    "记录今天复习了 RealLLM 工具调用",
    "查询笔记 RAGTool",
    "查询笔记 RealLLM",
    "RAGTool 的评分函数哪里容易出问题？",
    "我现在应该复习 ReActAgent 的什么？",
    "ToolRegistry 的作用是什么？",
    "刚才我问了什么？",
    "查找本地知识库 ReActAgent 的核心循环是什么？"
]

for case in cases:
    print("运行轨迹:\n")
    response = assistant.answer(case)
    print(f"问题:{case}\n\n答案：{response}")

# print(assistant.answer("请计算 12 + 30 / 3"))
# print(assistant.answer("查询笔记 RAGTool"))
# print(assistant.answer("RAGTool 的评分函数哪里容易出问题？"))