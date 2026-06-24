from real_embedding import RealEmbedding
import math
def cosine_similarity(vec1,vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    len1 = math.sqrt(sum(a * a for a in vec1))
    len2 = math.sqrt(sum(b * b for b in vec2))
    if len1 == 0 or len2 == 0:
        return 0
    return dot / (len1 * len2)
embedding = RealEmbedding()

pairs = [
    ("国王", "帝王"),
    ("国王", "天气预报"),
    ("RAG 检索知识库", "RAGTool 负责从知识库中检索相关内容"),
]
for a,b in pairs:
    vec1 = embedding.embed(a)
    vec2 = embedding.embed(b)
    print(a, b)
    print("向量长度:", len(vec1), len(vec2))
    print("相似度:", cosine_similarity(vec1, vec2))
    print()