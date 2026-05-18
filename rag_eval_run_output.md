# RAG 手工评估运行结果

- 评估时间：2026-05-14T14:45:36.285531
- 知识库 chunk 数：71

---
## 问题 1: ReActAgent 的核心循环是什么？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：17
内容：### Q: SimpleAgent 和 ReActAgent 有什么区别？
A: SimpleAgent 是基础实现，支持单一工具调用；ReActAgent 添加了显式的 Thought-Action-Observation 循环，支持多步推理和多次工具调用。
```

```
来源：agent_notes.md
分数：16
内容：ReActAgent 的核心循环是 Thought、Action、Observation。Agent 会根据模型输出调用工具，再把工具结果放回上下文继续推理。
```

```
来源：chapter7_agent.md
分数：16
内容：ReActAgent（Reasoning + Acting）是结合推理与行动的智能体架构，其核心循环包含以下步骤：
```

---
## 问题 2: ToolRegistry 的作用是什么？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：19
内容：### Q: ToolRegistry 的核心作用是什么？
A: 集中管理所有可用工具，负责工具的注册、查找、执行和生成工具描述信息供 LLM 理解。
```

```
来源：my_questions.md
分数：17
内容：### Q: SimpleAgent 和 ReActAgent 有什么区别？
A: SimpleAgent 是基础实现，支持单一工具调用；ReActAgent 添加了显式的 Thought-Action-Observation 循环，支持多步推理和多次工具调用。
```

```
来源：chapter7_agent.md
分数：14
内容：ToolRegistry 是工具管理的核心组件，提供：
```

---
## 问题 3: RAG 的完整流程是什么？

**检索结果（Top K）：**

```
来源：agent_notes.md
分数：7
内容：RAG 的基本流程是加载文档、切分文本、检索相关片段、把片段放入上下文，再让模型回答。
```

```
来源：chapter8_rag.md
分数：7
内容：## RAG 完整流程
```

```
来源：my_questions.md
分数：7
内容：### Q: SimpleAgent 和 ReActAgent 有什么区别？
A: SimpleAgent 是基础实现，支持单一工具调用；ReActAgent 添加了显式的 Thought-Action-Observation 循环，支持多步推理和多次工具调用。
```

---
## 问题 4: SimpleAgent 支持多少个工具并行调用？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：19
内容：### Q: SimpleAgent 和 ReActAgent 有什么区别？
A: SimpleAgent 是基础实现，支持单一工具调用；ReActAgent 添加了显式的 Thought-Action-Observation 循环，支持多步推理和多次工具调用。
```

```
来源：my_questions.md
分数：15
内容：### Q: 如何在 Agent 中使用工具？
A: 通过 ToolRegistry 注册工具，在系统提示中说明工具列表和调用格式，LLM 输出中包含工具调用格式时，Agent 解析并执行。
```

```
来源：agent_notes.md
分数：14
内容：SimpleAgent 负责接收用户输入、构造 messages、调用 LLM，并保存对话历史。
```

---
## 问题 5: 如何实现自定义工具？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：10
内容：### Q: 如何实现自定义工具？
A: 继承 BaseTool，实现 `name`、`description` 属性和 `run()` 方法，然后通过 `registry.register()` 注册。
```

```
来源：chapter7_agent.md
分数：7
内容：实现自定义工具的步骤：
1. 创建类继承 BaseTool
2. 定义 name 和 description 属性
3. 实现 run() 方法处理具体逻辑
4. 通过 registry.register() 注册工具
```

```
来源：my_questions.md
分数：6
内容：### Q: 系统提示词的作用是什么？
A: 定义 Agent 的角色、能力、工具列表、行为规范等，直接影响 Agent 的表现。
```

---
## 问题 6: RAGTool 的评分函数如何工作？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：12
内容：### Q: RAG 系统如何判断一个 chunk 是否相关？
A: 当前实现通过计算查询中的字符在 chunk 中出现的次数作为相似度分数，分数需要高于 `min_score` 阈值。
```

```
来源：my_questions.md
分数：11
内容：### Q: 如何提高 RAG 的检索质量？
A: 改进评分函数（使用向量相似度而非字符匹配）、优化文本切分策略、增加知识库质量。
```

```
来源：my_questions.md
分数：10
内容：### Q: 如何在 Agent 中使用工具？
A: 通过 ToolRegistry 注册工具，在系统提示中说明工具列表和调用格式，LLM 输出中包含工具调用格式时，Agent 解析并执行。
```

---
## 问题 7: Agent 如何维护对话上下文？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：15
内容：### Q: Agent 如何维护对话上下文？
A: 通过 `_history` 列表存储所有消息，新请求时将历史消息加入到 LLM 调用中。
```

```
来源：my_questions.md
分数：10
内容：### Q: 如何清除对话历史？
A: 调用 Agent 的历史清除方法，或创建新的 Agent 实例重新开始对话。
```

```
来源：agent_notes.md
分数：8
内容：ReActAgent 的核心循环是 Thought、Action、Observation。Agent 会根据模型输出调用工具，再把工具结果放回上下文继续推理。
```

---
## 问题 8: RAG 系统的主要优势是什么？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：9
内容：### Q: RAG 系统如何判断一个 chunk 是否相关？
A: 当前实现通过计算查询中的字符在 chunk 中出现的次数作为相似度分数，分数需要高于 `min_score` 阈值。
```

```
来源：my_questions.md
分数：8
内容：### Q: 系统提示词的作用是什么？
A: 定义 Agent 的角色、能力、工具列表、行为规范等，直接影响 Agent 的表现。
```

```
来源：my_questions.md
分数：7
内容：### Q: SimpleAgent 和 ReActAgent 有什么区别？
A: SimpleAgent 是基础实现，支持单一工具调用；ReActAgent 添加了显式的 Thought-Action-Observation 循环，支持多步推理和多次工具调用。
```

---
## 问题 9: 工具调用的格式是什么？

**检索结果（Top K）：**

```
来源：my_questions.md
分数：10
内容：### Q: SimpleAgent 和 ReActAgent 有什么区别？
A: SimpleAgent 是基础实现，支持单一工具调用；ReActAgent 添加了显式的 Thought-Action-Observation 循环，支持多步推理和多次工具调用。
```

```
来源：chapter7_agent.md
分数：8
内容：### Action（行动）
基于思考结果，Agent 决定采取的行动，通常是调用一个特定的工具。行动格式为：`[工具名:参数]`
```

```
来源：my_questions.md
分数：8
内容：### Q: ToolRegistry 的核心作用是什么？
A: 集中管理所有可用工具，负责工具的注册、查找、执行和生成工具描述信息供 LLM 理解。
```

---
## 问题 10: RAGTool 返回的结果包含哪些字段？

**检索结果（Top K）：**

```
来源：chapter8_rag.md
分数：11
内容：### 返回格式
每个检索结果包含三个关键字段：
- `score`：相似度分数，值越高说明相关性越强
- `source`：文档来源（文件名），便于溯源
- `content`：实际内容，是问题相关的文本片段
```

```
来源：agent_notes.md
分数：9
内容：ReActAgent 的核心循环是 Thought、Action、Observation。Agent 会根据模型输出调用工具，再把工具结果放回上下文继续推理。
```

```
来源：my_questions.md
分数：9
内容：### Q: 如何在 Agent 中使用工具？
A: 通过 ToolRegistry 注册工具，在系统提示中说明工具列表和调用格式，LLM 输出中包含工具调用格式时，Agent 解析并执行。
```
