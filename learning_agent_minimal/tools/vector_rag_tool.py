from pathlib import Path

from .base import BaseTool
import math

class VectorRAGTool(BaseTool):
    name = "vector_rag_search"
    description = "使用向量相似度从本地知识库检索相关内容"

    def __init__(self, knowledge_dir="learning_agent_minimal/knowledge_base", top_k=3):
        self.knowledge_dir = Path(knowledge_dir)
        self.top_k = top_k
        self.chunks = self._load_documents()

    def run(self, tool_input: str):
        results= []
        for chunk in self.chunks:
            score = self._score(tool_input, chunk["content"])
            if score>0:
                results.append({
                            "score": score,
                            "source": chunk["source"],
                            "content": chunk["content"]
                        })
        results.sort(key=lambda x:x["score"],reverse=True)
        top_results = results[:self.top_k]
        if not top_results:
              return "没有检索到相关资料。"
        output = []
        for item in top_results:
            output.append(
                f"来源：{item['source']}\n"
                f"分数：{item['score']}\n"
                f"内容：{item['content']}"
            )

        return "\n\n".join(output)
    
    def _load_documents(self):
        chunks = []
        for path in self.knowledge_dir.glob("*"):
            if path.suffix not in [".md",".txt"]:
                continue
            text = path.read_text(encoding="utf-8")
            for paragraph in self._split_chunks(text=text):
                chunks.append({"source":path.name,"content":paragraph})
        return chunks 

    def _split_chunks(self, text: str):
        chunks = []
        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                chunks.append(paragraph)
        return chunks

    def _score(self, query: str, chunk: str):
        query = self.text_to_vector(query)
        chunk = self.text_to_vector(chunk)
        return self.cosine_similarity(query,chunk)
    def text_to_vector(self,text: str):
        vector = {}
        for char in text:
            vector[char] = vector.get(char, 0) + 1
        return vector

    def dot_product(self,vec1, vec2):
        total = 0
        for char, count1 in vec1.items():
            count2 = vec2.get(char)
            if count2 is not None:
                total += count1*count2
        return total
    
    def vector_length(self,vec):
        result = 0
        for count in vec.values():
            result += count**2
        return math.sqrt(result)

    def cosine_similarity(self,vec1, vec2):
        len1 = self.vector_length(vec1)
        len2 = self.vector_length(vec2)
        if len1 == 0 or len2 == 0:
            return 0
        return self.dot_product(vec1,vec2)/(len1 * len2)