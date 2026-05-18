from learning_assistant import LearningAssistant
from real_llm import RealLLM

assistant = LearningAssistant(llm=RealLLM())

print(assistant.answer("请计算 12 + 30 / 3"))
print(assistant.answer("查询笔记 RAGTool"))
print(assistant.answer("RAGTool 的评分函数哪里容易出问题？"))