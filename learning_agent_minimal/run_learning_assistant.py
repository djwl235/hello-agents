from learning_assistant import LearningAssistant

assistant = LearningAssistant(use_embedding_rag=True)
print(assistant.answer("记录今天复习了 RAGTool"))
print(assistant.answer("查询笔记 RAGTool"))
print(assistant.answer("请计算 12 + 30 / 3"))
print(assistant.answer("RAGTool 的评分函数哪里容易出问题？"))