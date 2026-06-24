from tools.embedding_rag_tool import EmbeddingRAGTool
from tools.rag_tool import RAGTool
from tools.vector_rag_tool import VectorRAGTool
from real_embedding import RealEmbedding
queries = [
    "RAG 检索知识库",
    "NoteTool 学习笔记",
    "ReActAgent 工具调用",
    "国王和帝王有什么关系",  
]
ragtool = RAGTool(knowledge_dir="learning_agent_minimal/knowledge_base")
vectorRagTool = VectorRAGTool()
embeddingRagTool = EmbeddingRAGTool(embedding=RealEmbedding())
for query in queries:
    print(f"=== Query: {query} ===")
    print("--- Keyword RAG ---\n")
    Keyword_RAG = ragtool.run(query)
    print(Keyword_RAG+"\n")
    print("--- Char Vector RAG ---\n")
    Char_Vector_RAG = vectorRagTool.run(query)
    print(Char_Vector_RAG+"\n")
    print("--- Embedding RAG ---\n")
    Embedding_RAG = embeddingRagTool.run(query)
    print(Embedding_RAG+"\n")