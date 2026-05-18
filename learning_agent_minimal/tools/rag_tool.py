from pathlib import Path
from tools.base import BaseTool
class RAGTool(BaseTool):
    name = "rag_search"
    description = "检索本地资料返回相似资料"
    def __init__(self,knowledge_dir="knowledge_base", top_k=3,min_score = 3):
        self.knowledge_dir = Path(knowledge_dir)
        self.top_k = top_k
        self.chunks = self.load_documents()
        self.min_score = min_score
    def load_documents(self):
        chunks = []
        for path in self.knowledge_dir.glob("*"):
            if path.suffix not in [".md",".txt"]:
                continue
            text = path.read_text(encoding="utf-8")
            for paragraph in text.split("\n\n"):
                paragraph = paragraph.strip()
                if paragraph:
                    chunks.append({"source":path.name,"content":paragraph})
        return chunks
    def score(self,query,content):
        score = 0
        for char in query:
            if char.strip() and char in content:
                score+=1
            if ("RAG" in char and "RAG" in content) or ("ToolRegistry" in char and "ToolRegistry" in content) or ("ReActAgent" in char and "ReActAgent" in content):
                score+=5
        return score
    def run(self,tool_input):
        results = []
        for chunk in self.chunks:
            score = self.score(tool_input, chunk["content"])
            if score > self.min_score:
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
    def get_chunk_count(self):
        return len(self.chunks)