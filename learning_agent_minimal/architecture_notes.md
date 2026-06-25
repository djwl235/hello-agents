## 流程

`LearningAssistant.answer()` 会先判断用户意图route_intent：

```text
记录 / 查询笔记 / 计算
-> 直接交给 Agent 走工具调用

其他学习问题
-> RAGTool 检索知识库(取决于是否启用embeddingRAG)
-> NoteTool 搜索学习笔记
-> StructuredNoteTool 搜索结构化学习笔记
-> ContextBuilder 构造上下文
-> Agent 调用 LLM 生成回答
```

`直接工具调用` 的 流程：

```text
1. 意图识别
2. LLM解析 [TOOL_CALL:工具名:参数]
3. 调用 ToolRegistry 执行工具
```

`learning_advice` 的 流程：

```text
1. RAGTool 或 EmbeddingRAGTool
2. NoteTool + StructuredNoteTool
3. ContextBuilder 构建上下文 system prompt + history + user input
4. 调用 LLM
5. 解析 [TOOL_CALL:工具名:参数]
6. 调用 ToolRegistry 执行工具
7. 将工具结果作为 Observation 放回 messages
8. 下一轮继续推理，直到得到最终答案或达到最大轮数
```
# ToolRegistry 不关心工具来源，本地 Tool、MCPProxyTool、StructuredNoteTool 都统一暴露 name/description/run。