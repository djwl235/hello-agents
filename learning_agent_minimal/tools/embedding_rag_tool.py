from embedding import MockEmbedding
from real_embedding import RealEmbedding
from pathlib import Path
from .base import BaseTool
import math
import json
class EmbeddingRAGTool(BaseTool):
    name = "embedding_rag_search"
    description = "使用 embedding 向量从本地知识库检索相关内容"
    def __init__(self,knowledge_dir = "learning_agent_minimal/knowledge_base",embedding = None,top_k=3,min_score = 0.5,use_cache=True,force_rebuild=False):
        self.knowledge_dir = Path(knowledge_dir)
        self.embedding = embedding or MockEmbedding()
        self.top_k = top_k
        self.use_cache = use_cache
        self.force_rebuild = force_rebuild
        self.index_path = Path("learning_agent_minimal/vector_index/embedding_index.json")
        self.chunks = self._build_index()
        self.min_score = min_score

    def run(self, tool_input: str):
        results= []
        query_embedding = self.embedding.embed(tool_input)
        for chunk in self.chunks:
            chunk_embedding = chunk["embedding"]
            score = self._score(query_embedding=query_embedding,chunk_embedding=chunk_embedding)
            if score > self.min_score:
                results.append({
                    "score": score,
                    "source": chunk["source"],
                    "content": chunk["content"]
                })
        results.sort(key=lambda x:x["score"],reverse=True)
        top_results = results[:self.top_k]
        if not top_results:
            return "没有检索到相关资料"
        output = []
        for item in top_results:
            output.append(
                f"来源：{item['source']}\n"
                f"分数：{item['score']}\n"
                f"内容：{item['content']}"
            )
        return "\n\n".join(output)

    def _build_index(self):
        chunks = []
        if self.use_cache and not self.force_rebuild and self.index_path.exists():
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        
        for path in self.knowledge_dir.glob("*"):
            if path.suffix not in ['.md','.txt']:
                continue
            text = path.read_text(encoding="utf-8")
            for paragraph in self._split_chunks(text=text):
                embedd_score = self.embedding.embed(paragraph)
                chunks.append({"source":path.name,"content":paragraph,"embedding":embedd_score})
        if self.use_cache:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            self.index_path.write_text(
              json.dumps(chunks, ensure_ascii=False, indent=2),
              encoding="utf-8",
            )
        return chunks
    def _split_chunks(self, text: str):
        chunks = []
        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                chunks.append(paragraph)
        return chunks

    def _score(self, query_embedding, chunk_embedding):
        return self.cosine_similarity(query_embedding,chunk_embedding)

    def dot_product(self,vec1, vec2):
        total = sum(a * b for a, b in zip(vec1, vec2))
        return total

    def vector_length(self,vec):
        result = 0
        for count in vec:
            result += count**2
        return math.sqrt(result)

    def cosine_similarity(self,vec1, vec2):
        len1 = self.vector_length(vec1)
        len2 = self.vector_length(vec2)
        if len1 == 0 or len2 == 0:
            return 0
        return self.dot_product(vec1,vec2)/(len1 * len2)