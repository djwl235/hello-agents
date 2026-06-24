from embedding_base import BaseEmbedding

class MockEmbedding(BaseEmbedding):
    def embed(self, text: str) -> list[float]:
        agent_score = 0
        rag_score = 0
        note_score = 0
        for keyword in ["RAG", "检索", "知识库"]:
            if keyword in text:
                rag_score += 1
        for keyword in ["Agent", "ReAct", "ToolRegistry"]:
            if keyword in text:
                agent_score += 1
        for keyword in ["Note", "笔记"]:
            if keyword in text:
                note_score += 1
        return [agent_score,rag_score,note_score]