# Learning Agent Minimal

一个用于 Agent 入门练习的个人学习助手 MVP。

项目目标不是做一个完整生产级 Agent，而是从 0 串起一个最小但完整的 Agent 工程闭环：

```text
用户输入
-> 意图路由
-> RAG / Note / Calculator 工具
-> ContextBuilder 构造上下文
-> ReAct Agent 循环
-> LLM 生成回答
-> 执行轨迹与评估
```

## 当前功能

- `SimpleAgent`：维护对话历史，执行 ReAct 风格工具调用循环。
- `ToolRegistry`：统一注册、查找和执行工具。
- `CalculatorTool`：支持简单数学表达式计算。
- `RAGTool`：基于本地 Markdown / txt 知识库做关键词检索。
- `NoteTool`：支持学习笔记的 `add`、`search`、`list`。
- `ContextBuilder`：组合最近对话、知识库片段、学习笔记和当前问题。
- `LearningAssistant`：封装学习助手主工作流。
- `MockLLM` / `RealLLM`：支持 mock 模型和真实 OpenAI-compatible 模型切换。
- `CLI`：支持命令行连续对话。
- 评估文档：包含 RAG 检索评估和真实 LLM Agent 评估。

## 项目结构

```text
learning_agent_minimal/
  agent.py                    # SimpleAgent / ReAct 循环
  learning_assistant.py        # 学习助手主工作流
  context.py                  # ContextBuilder
  message.py                  # Message 数据结构
  llm.py                      # MockLLM
  real_llm.py                 # 真实 LLM 调用
  real_embedding.py           # 真实 Embedding 调用
  embedding.py                # MockEmbedding
  embedding_base.py           # Embedding 接口基类
  llm_base.py                 # LLM 接口基类
  config.py                   # 配置读取
  cli.py                      # CLI 入口
  mcp_server.py               # 自定义 MCP Server 示例
  tools/
    base.py                   # BaseTool
    registry.py               # ToolRegistry
    calculator.py             # CalculatorTool
    rag_tool.py               # RAGTool
    vector_rag_tool.py        # 字符频率向量 RAG
    embedding_rag_tool.py     # Embedding RAG
    note_tool.py              # NoteTool
    structured_note_tool.py   # 结构化笔记工具
    mcp_proxy_tool.py         # MCP 工具代理
    mcp_tool_factory.py       # MCP 工具发现与注册
  knowledge_base/             # 本地知识库
  notes/                      # 学习笔记
  vector_index/               # Embedding 索引缓存
  eval_reports/               # 自动化评估报告
```

## 配置方式

复制 `.env.example` 为 `.env`，并填写真实模型配置：

```text
LLM_PROVIDER=openai-compatible
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_name_here
LLM_BASE_URL=https://api.example.com/v1
```

`.env` 已被 `.gitignore` 忽略，不要提交真实密钥。

## 运行方式

检查配置：

```powershell
python learning_agent_minimal\run_config_check.py
```

运行 CLI：

```powershell
python learning_agent_minimal\cli.py
```

单独测试工具：

```powershell
python learning_agent_minimal\run_tools.py
python learning_agent_minimal\run_rag_tool.py
python learning_agent_minimal\run_note_tool.py
```

测试学习助手工作流：

```powershell
python learning_agent_minimal\run_learning_assistant.py
```

测试真实 LLM：

```powershell
python learning_agent_minimal\run_real_llm_check.py
python learning_agent_minimal\run_real_agent_check.py
```

运行真实 Agent 评估：

```powershell
python learning_agent_minimal\run_real_agent_eval.py
```

## 核心流程

`LearningAssistant.answer()` 会先判断用户意图：

```text
记录 / 查询笔记 / 计算
-> 直接交给 Agent 走工具调用

其他学习问题
-> RAGTool/EmbeddingRAGTool 检索知识库
-> NoteTool/StructuredNoteTool 搜索学习笔记
-> ContextBuilder 构造上下文
-> Agent 调用 LLM 生成回答
```

`SimpleAgent` 的 ReAct 循环：

```text
1. 构造 system prompt + history + user input
2. 调用 LLM
3. 解析 [TOOL_CALL:工具名:参数]
4. 调用 ToolRegistry 执行工具
5. 将工具结果作为 Observation 放回 messages
6. 下一轮继续推理，直到得到最终答案或达到最大轮数
```
```text
MCPProxyTool / MCPToolFactory
将外部工具处理为统一接口,不改变调用方式前提下,自由接入外部工具
```
```text
RealEmbedding
接入真实模型,对知识库等进行向量化处理,同时在每次调用时首先判断是否存在vector_index,若有则直接加载不再初始化.
```

## 工具调用格式

LLM 如需调用工具，必须输出：

```text
[TOOL_CALL:工具名:参数]
```

示例：

```text
[TOOL_CALL:calculator:12 + 30 / 3]
[TOOL_CALL:note:add 今天复习了 RAGTool]
[TOOL_CALL:note:search RAGTool]
[TOOL_CALL:rag_search:ReActAgent 的核心循环是什么？]
```

## 测试与评估

已完成两类评估：

- RAG 检索评估：10 个问题，检查命中正确 chunk、Top1 正确率和无关 chunk。
- 真实 LLM Agent 评估：10 个端到端问题，覆盖计算、笔记、知识库、上下文历史。

当前真实 LLM 评估结果：

```text
总测试数：10
成功数：10
回答可用率：100%
```

注意：当前架构中，部分 RAG / Note 检索由 `LearningAssistant` 工作流主动执行，不一定表现为 LLM 显式输出 `TOOL_CALL`。

## 新增能力
```text
mcp:
同时支持外部工具及内部自己编写的工具, mcp_proxy_tool将mcp转化为tool_registr接口,即所有的工具都同样调用,同样描述没有区别,不增加新调用方式.
```
```text
Embedding RAG:
相较于原关键词RAG,新增了调用模型生成嵌入向量的新RAG,同时不移除原有RAG,可通过传参调用.相较于原有RAG,Embedding RAG更能落到生产环境,同时新增了向量存放json文件,便于保存已向量化的知识库,避免重复初始化.但可以优化接入各类向量数据库.
```
```text
Structured Note:
相较于原先笔记工具,整体功能不发生变化,但是新增例如summary tag等字段,记录更详细,同时summary字段便于后续总结使用.
```

