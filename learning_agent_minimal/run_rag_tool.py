from llm import MockLLM
from agent import SimpleAgent
from tools.rag_tool import RAGTool
from tools.registry import ToolRegistry
rag = RAGTool(knowledge_dir="learning_agent_minimal/knowledge_base")
print(rag.run("ReActAgent 的核心循环是什么？"))
print("-" * 40)
print(rag.run("ToolRegistry 是做什么的？"))
print("chunk 数量：", rag.get_chunk_count())