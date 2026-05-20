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
  llm_base.py                 # LLM 接口基类
  config.py                   # 配置读取
  cli.py                      # CLI 入口
  tools/
    base.py                   # BaseTool
    registry.py               # ToolRegistry
    calculator.py             # CalculatorTool
    rag_tool.py               # RAGTool
    note_tool.py              # NoteTool
  knowledge_base/             # 本地知识库
  notes/                      # 学习笔记
  real_agent_eval_results.md  # 真实 LLM 评估结果
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
-> RAGTool 检索知识库
-> NoteTool 搜索学习笔记
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

## 已知问题

- RAG 仍是关键词/字符级检索，不理解语义。
- NoteTool 只是 Markdown 文件搜索，没有结构化索引。
- 记忆主要依赖当前 session 的 `_history` 和笔记文件，缺少自动记忆判断。
- 真实 LLM 有时会直接回答简单问题，而不是严格调用工具。
- 没有流式输出。
- 没有 Web 搜索能力。
- 还没有自动化评估脚本，只是手工记录结果。

## 下一步计划

优先级建议：

1. 增加端到端自动评估脚本，沉淀成功率和失败案例。
2. 优化 RAG：更好的 chunk 切分、关键词权重、向量检索。
3. 增加 LLM 工具调用稳定性测试和 prompt 调优。
4. 将 NoteTool 改成结构化笔记，支持类型、标签和摘要。
5. 视情况再考虑 LangGraph / LangChain，而不是过早重构。

当前阶段的重点是理解 Agent 工程闭环，而不是追求框架复杂度。
