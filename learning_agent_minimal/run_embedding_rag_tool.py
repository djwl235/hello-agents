from tools.embedding_rag_tool import EmbeddingRAGTool
from real_embedding import RealEmbedding
tool = EmbeddingRAGTool(embedding=RealEmbedding(),force_rebuild=False)
queries = [
      "RAG 检索知识库",
      "NoteTool 学习笔记",
      "ReActAgent 工具调用",
      "天气预报和篮球比赛",
]
for query in queries:
    print("=" * 60)
    print(query)
    print(tool.run(query))