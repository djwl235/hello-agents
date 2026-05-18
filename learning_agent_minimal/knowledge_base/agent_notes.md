 # Agent 学习笔记

  SimpleAgent 负责接收用户输入、构造 messages、调用 LLM，并保存对话历史。

  ToolRegistry 负责注册工具、按名称查找工具，并统一执行工具。

  ReActAgent 的核心循环是 Thought、Action、Observation。Agent 会根据模型输出调用工具，再把工具结果放回上下文继续推理。

  RAG 的基本流程是加载文档、切分文本、检索相关片段、把片段放入上下文，再让模型回答。