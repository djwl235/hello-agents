from pathlib import Path

from tools.base import BaseTool

from tools.vector_rag_tool import VectorRAGTool

vectorRAGTool = VectorRAGTool()
queries = [
    "RAG 检索知识库",
    "NoteTool 学习笔记",
    "天气预报和篮球比赛",
]
for query in queries:
    result = vectorRAGTool.run(query)
    print(query+"\n"+result+"\n")
