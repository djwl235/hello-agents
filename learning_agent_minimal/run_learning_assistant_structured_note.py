from learning_assistant import LearningAssistant
from real_llm import RealLLM
assistant = LearningAssistant()

response = assistant.answer("结构化记录 RAG 检索增强生成是什么？")
response = assistant.answer("结构化查询 RAG 检索增强生成是什么？")
print(response)
