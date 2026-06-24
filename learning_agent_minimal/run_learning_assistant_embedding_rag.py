from learning_assistant import LearningAssistant
from real_llm import RealLLM
assistant = LearningAssistant(use_embedding_rag=True,llm = RealLLM())

response = assistant.answer("RAG 检索增强生成是什么？")
print(response)

print("使用的 RAG 工具:", assistant.rag_tool_name)