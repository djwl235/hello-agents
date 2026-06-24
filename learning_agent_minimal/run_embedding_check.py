import math
from embedding import MockEmbedding
texts = [
    ("RAG 检索知识库", "RAGTool 负责从知识库中检索相关内容"),
    ("RAG 检索知识库", "NoteTool 用来记录学习笔记"),
    ("ReActAgent 工具调用", "ToolRegistry 管理 Agent 可用工具"),
]

mockEmbedding = MockEmbedding()

def dot_product(vec1, vec2):
    total = sum(a * b for a, b in zip(vec1, vec2))
    return total

def vector_length(vec):
    result = 0
    for count in vec:
        result += count**2
    return math.sqrt(result)

def cosine_similarity(vec1, vec2):
    len1 = vector_length(vec1)
    len2 = vector_length(vec2)
    if len1 == 0 or len2 == 0:
        return 0
    return dot_product(vec1,vec2)/(len1 * len2)

def main():
    for text in texts:
        vec1 = mockEmbedding.embed(text[0])
        vec2 = mockEmbedding.embed(text[1])
        print(cosine_similarity(vec1,vec2))
if __name__ == '__main__':
    main()
