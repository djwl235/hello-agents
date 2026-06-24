import math
def text_to_vector(text: str):
    vector = {}
    for char in text:
        vector[char] = vector.get(char, 0) + 1
    return vector

def dot_product(vec1, vec2):
    total = 0
    for char, count1 in vec1.items():
        count2 = vec2.get(char)
        if count2 is not None:
            total += count1*count2
    return total
def vector_length(vec):
    result = 0
    for count in vec.values():
        result += count**2
    return math.sqrt(result)

def cosine_similarity(vec1, vec2):
    len1 = vector_length(vec1)
    len2 = vector_length(vec2)
    if len1 == 0 or len2 == 0:
        return 0
    return dot_product(vec1,vec2)/(len1 * len2)

def search(query, chunks, top_k=3):
    results = []
    query_vec = text_to_vector(query)
    for chunk in chunks:
        chunk_vec = text_to_vector(chunk)
        score = cosine_similarity(query_vec,chunk_vec)
        results.append((score,chunk))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_k]

chunks = [
    "ReActAgent 使用 Thought Action Observation 循环",
    "RAGTool 负责从知识库中检索相关内容",
    "NoteTool 用来记录和查询学习笔记",
]
query = "RAG 检索 知识库"
results = search(query, chunks, top_k=2)
for score, chunk in results:
    print(score, chunk)