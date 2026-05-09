# Agent 入门学习方案

适用情况：

- 已经看完 `docs` 目录第 1-10 章。
- 第 7 章曾经手敲过代码，但已经过去约一周半，现在有些遗忘。
- 第 8、9、10 章主要是看文档，缺少完整手写和集成练习。
- 当前边实习边学习，学习时间不稳定。
- 预计还有约一个半月，但不能保证每天都有学习时间。

本方案的核心目标不是“学完 hello-agents 全部内容”，而是：

> 在 6 周左右，做出一个可以运行、可以展示、可以解释的个人学习助手 Agent。

这个 Agent 最低需要具备：

- 接收用户问题。
- 调用大模型或 Mock LLM。
- 调用工具。
- 检索本地学习资料。
- 保存学习笔记。
- 构造上下文。
- 输出可追踪日志。
- 用一组测试问题验证效果。

---

## 1. 当前水平判断

### 1.1 已经具备的基础

你已经完成了很重要的前置输入：

- 看过第 1-4 章，对 Agent 的概念、发展和经典范式有基本认识。
- 看过第 5-6 章，知道低代码平台和框架开发实践的大概方向。
- 手敲过第 7 章，至少接触过 Agent 框架核心代码。
- 看过第 8-10 章，知道记忆、RAG、上下文工程、通信协议这些能力存在。

这些内容足够支撑你进入“做项目练习”的阶段。

### 1.2 当前主要不足

现在的问题不是完全不会，而是缺少稳定输出能力：

1. 第 7 章框架没有内化

   你可能记得有 `Agent`、`Tool`、`LLM`、`Message`，但还不能很顺畅地从空目录重新设计出来。

2. 工具调用闭环不够熟

   一个真正的 Agent 不是一次 LLM 调用，而是：

   ```text
   用户输入
   -> Agent 构造上下文
   -> LLM 判断是否需要工具
   -> Agent 调用工具
   -> 工具返回 Observation
   -> Agent 再次推理
   -> 输出最终答案
   ```

3. 第 8-10 章还停留在概念层

   你看过 RAG、记忆、ContextBuilder、MCP/A2A，但还没有把它们真正接到自己的 Agent 里。

4. 缺少评估意识

   现在可能更关注“能不能跑”，但一个 Agent 做出来后还要回答：

   - 哪些问题答得对？
   - 哪些问题答错？
   - 是否调用了正确工具？
   - RAG 是否检索到了正确资料？
   - 失败原因是什么？

5. 学习目标边界不清

   “学完 hello-agents”这个目标太大，会制造焦虑。更合理的目标是“做出一个小而完整的 Agent 项目”。

---

## 2. 最终项目目标

建议最终项目叫：

```text
learning_agent
```

它是一个个人学习助手 Agent。

### 2.1 项目功能范围

最低版本需要支持：

1. 普通问答

   用户可以问普通问题，Agent 调用 LLM 回答。

2. 工具调用

   Agent 至少支持一个计算工具和一个本地资料检索工具。

3. 本地知识库问答

   可以把 `docs` 中部分章节或自己的学习笔记放进知识库，Agent 能检索后回答。

4. 学习笔记记录

   用户可以告诉 Agent：

   ```text
   今天我复习了第 7 章，但 ReActAgent 还是不太熟。
   ```

   Agent 可以把它保存下来。

5. 学习状态查询

   用户可以问：

   ```text
   我最近卡在哪里？
   ```

   Agent 能从笔记中回答。

6. 日志追踪

   每次运行至少记录：

   - 用户输入
   - 是否调用工具
   - 工具名称
   - 工具参数
   - 工具结果
   - 最终回答

7. 简单评估

   准备 20 个测试问题，记录回答是否正确。

### 2.2 最终目录结构建议

```text
learning_agent/
  README.md
  run.py
  message.py
  llm.py
  agent.py
  context.py
  logger.py
  tools/
    __init__.py
    base.py
    calculator.py
    rag_tool.py
    note_tool.py
  knowledge_base/
    chapter7_notes.md
    chapter8_notes.md
  notes/
    learning_log.md
  logs/
    runs.jsonl
  tests/
    test_cases.md
    eval_results.md
```

### 2.3 最终验收标准

完成时你需要能做到：

- 不看第 7 章源码，解释 Agent 主循环。
- 不看第 7 章源码，新增一个工具。
- 能演示一次完整流程：

  ```text
  用户问题
  -> Agent 判断需要检索资料
  -> 调用 RAGTool
  -> 读取检索结果
  -> 生成带来源的回答
  -> 保存日志
  ```

- 能演示一次学习笔记流程：

  ```text
  用户说今天学了什么
  -> Agent 调用 NoteTool 保存
  -> 后续用户询问学习状态
  -> Agent 查询笔记并回答
  ```

- 有 README、测试问题、失败案例。

---

## 3. 总体学习策略

### 3.1 不追求完整学完所有章节

优先级如下：

| 优先级 | 内容 | 处理方式 |
| --- | --- | --- |
| 最高 | 第 7 章 Agent 框架 | 必须重新掌握 |
| 高 | 第 8 章 RAG 和记忆 | 做最小可运行版本 |
| 高 | 第 9 章上下文工程 | 做简化版 ContextBuilder 和 NoteTool |
| 中 | 第 12 章评估 | 提前吸收评估思想，不必深挖所有 benchmark |
| 低 | 第 10 章通信协议 | 先了解，暂不深入 |
| 低 | 第 11 章 Agentic-RL | 暂时跳过 |
| 低 | 第 13-16 章综合项目 | 看架构，不做完整复现 |

### 3.2 学习方式从“看懂”改成“闭卷写出”

每个模块都按这个循环：

```text
看文档或代码 20-40 分钟
-> 合上资料写伪代码
-> 新建文件手写最小版本
-> 跑起来
-> 对照原代码补差距
-> 写 3-5 行总结
```

不要长时间只看文档。只看文档会产生“我好像懂了”的错觉，但从 0 写 Agent 需要输出能力。

### 3.3 每周只追一个核心产物

边实习时，最怕每天任务太多。每周只设一个核心目标：

- 第 1 周：找回第 7 章。
- 第 2 周：写出工具调用 Agent。
- 第 3 周：接入 RAG。
- 第 4 周：接入笔记和上下文。
- 第 5 周：做评估和稳定性。
- 第 6 周：整理成作品。

如果某周很忙，只完成最低版本，不重启计划。

---

## 4. 每日学习模板

### 4.1 工作日 30 分钟版本

适合很累、时间少的日子。

```text
5 分钟：回忆昨天写了什么
20 分钟：只完成一个小函数或读一个小文件
5 分钟：写学习日志
```

示例任务：

- 看 `my_simple_agent.py` 的 `run()` 方法。
- 写出 `Message` 类。
- 给 `CalculatorTool` 加一个异常处理。
- 记录今天哪里卡住。

### 4.2 工作日 60 分钟版本

适合普通学习日。

```text
10 分钟：不看资料，写出今天模块的职责
35 分钟：编码或复现
10 分钟：运行并调试
5 分钟：写总结
```

示例任务：

- 写 `ToolRegistry`。
- 写 `MockLLM`。
- 写一个最小 `SimpleAgent`。
- 把工具调用日志打印出来。

### 4.3 周末 2-3 小时版本

适合做集成。

```text
30 分钟：复盘本周代码
60-90 分钟：实现一个完整小功能
30 分钟：补测试和日志
20 分钟：写 README 或学习记录
```

示例任务：

- 集成 `ReActAgent + CalculatorTool`。
- 集成 `ReActAgent + RAGTool`。
- 准备 10 个测试问题。
- 写项目架构说明。

---

## 5. 六周详细计划

## 第 1 周：找回第 7 章框架感

目标：

> 重新理解第 7 章，不要求全部背下来，但要恢复 Agent 框架的整体结构。

### 本周重点

重点看这些文件：

```text
code/chapter7/my_simple_agent.py
code/chapter7/my_react_agent.py
code/chapter7/my_calculator_tool.py
code/chapter7/test_simple_agent.py
code/chapter7/test_react_agent.py
```

重点理解这些概念：

- `Message`：消息的数据结构。
- `LLM`：模型调用封装。
- `Agent`：负责组织对话和调用 LLM。
- `Tool`：外部能力封装。
- `ToolRegistry`：工具管理。
- `SimpleAgent`：普通对话 Agent。
- `ReActAgent`：可以思考、调用工具、观察结果的 Agent。

### Day 1：只看结构，不写代码

任务：

1. 打开第 7 章文档，只看目录和标题。
2. 打开 `code/chapter7`，看有哪些文件。
3. 在纸上或 Markdown 里画出关系：

   ```text
   User
   -> Agent
   -> LLM
   -> ToolRegistry
   -> Tool
   -> Agent
   -> User
   ```

输出：

```text
learning_agent_notes/day1_chapter7_map.md
```

如果不想新建目录，也可以直接写在草稿里。

验收：

- 能说出第 7 章为什么要拆成 LLM、Agent、Tool 三层。

### Day 2：复习 SimpleAgent

任务：

1. 看 `my_simple_agent.py`。
2. 重点看：

   - 初始化参数。
   - 对话历史保存。
   - `run()` 方法。
   - 是否支持工具。

3. 合上代码，写伪代码：

   ```python
   class SimpleAgent:
       def __init__(self, llm, system_prompt):
           ...

       def run(self, user_input):
           ...
   ```

验收：

- 能解释 `SimpleAgent.run()` 的输入、输出和中间步骤。

### Day 3：闭卷写 Message + MockLLM + SimpleAgent

任务：

新建练习目录：

```text
learning_agent/
```

先写三个文件：

```text
message.py
llm.py
agent.py
```

最小功能：

```text
用户输入
-> SimpleAgent 保存用户消息
-> MockLLM 返回固定回答
-> SimpleAgent 保存 assistant 消息
-> 打印回答
```

验收：

- 不接真实大模型也能跑。
- 能打印对话历史。

### Day 4：看 Tool 和 CalculatorTool

任务：

1. 看 `my_calculator_tool.py`。
2. 总结一个工具至少需要什么：

   - 名称。
   - 描述。
   - 参数。
   - 执行方法。
   - 返回结果。

3. 写自己的 `CalculatorTool`。

验收：

- 直接调用工具可以计算：

  ```text
  23 * 47
  ```

### Day 5：写 ToolRegistry

任务：

写：

```text
tools/base.py
tools/calculator.py
```

实现：

```python
registry.register(tool)
registry.get_tool("calculator")
registry.list_tools()
registry.execute("calculator", {"expression": "23 * 47"})
```

验收：

- 工具不存在时返回清晰错误。
- 参数错误时不崩溃。

### 周末：复盘第 7 章

任务：

1. 看 `my_react_agent.py`。
2. 写出 ReAct 循环伪代码：

   ```text
   for step in max_steps:
       prompt = build_prompt(task, tools, history)
       llm_output = llm.chat(prompt)
       if llm_output is final:
           return answer
       if llm_output is action:
           result = tool.execute(args)
           history.append(observation)
   ```

3. 先不用完整实现，只要能解释。

本周验收：

- 能闭卷解释 `SimpleAgent`。
- 能闭卷写出 `Message + MockLLM + SimpleAgent`。
- 能写一个可直接调用的 `CalculatorTool`。

---

## 第 2 周：写出最小工具调用 Agent

目标：

> 从 0 写出一个可以调用工具的 Agent。

### 本周重点

这周不追求复杂，不接 RAG，不接 MCP，只做工具调用闭环。

### 核心功能

需要完成：

- `BaseTool`
- `CalculatorTool`
- `ToolRegistry`
- `ReActAgent`
- 最大执行步数。
- 工具异常处理。
- 运行日志。

### 推荐实现格式

为了降低难度，可以先让 MockLLM 输出固定格式：

```text
Action: calculator
Action Input: {"expression": "23 * 47"}
```

或者：

```text
Final Answer: 结果是 1081
```

Agent 只需要解析这两种输出。

### Day 1：实现 BaseTool

任务：

```python
class BaseTool:
    name: str
    description: str

    def run(self, **kwargs):
        raise NotImplementedError
```

验收：

- 所有工具都继承它。
- 工具描述能被 Agent 拼进 prompt。

### Day 2：实现 ToolRegistry

任务：

实现：

```python
register(tool)
get_tool(name)
list_tool_descriptions()
execute(name, args)
```

验收：

- 调用不存在的工具时返回错误信息。
- 工具执行失败时返回错误信息。

### Day 3：实现 ReActAgent 第一版

任务：

实现最小循环：

```text
构造 prompt
-> 调用 MockLLM
-> 解析 Action
-> 调用工具
-> 把 Observation 放回历史
-> 再调用 MockLLM
-> 输出 Final Answer
```

验收：

- 用 MockLLM 跑通一次工具调用。

### Day 4：接真实 LLM

任务：

如果 API 环境已配置，接真实 LLM。  
如果没有配置，就继续用 MockLLM，不影响本周目标。

验收：

- 真实 LLM 能回答普通问题。
- 如果调用工具不稳定，先不强求。

### Day 5：加日志

任务：

每次运行写入：

```json
{
  "user_input": "...",
  "steps": [
    {
      "llm_output": "...",
      "tool": "calculator",
      "tool_args": {},
      "observation": "..."
    }
  ],
  "final_answer": "..."
}
```

验收：

- 能在 `logs/runs.jsonl` 中看到每次运行记录。

### 周末：做一次小演示

演示任务：

```text
请帮我计算 23 * 47，然后解释计算结果。
```

Agent 应该：

```text
调用 calculator
-> 得到 1081
-> 输出解释
```

本周验收：

- 能从 0 写出工具调用 Agent。
- 能新增一个工具。
- 能通过日志看见 Agent 做了什么。

---

## 第 3 周：接入 RAG，做本地资料问答

目标：

> 把第 8 章的 RAG 能力做成一个工具，接到自己的 Agent 中。

### 本周重点

先做最小版本，不要一开始就上复杂向量数据库。

推荐顺序：

1. 关键词检索版本。
2. 如果有余力，再做 embedding 版本。

### 最小 RAG 流程

```text
读取 Markdown / txt
-> 切分 chunk
-> 保存 chunk
-> 根据用户问题检索相关 chunk
-> 返回 top-k chunk
-> Agent 根据 chunk 回答
```

### Day 1：准备知识库

任务：

在 `learning_agent/knowledge_base/` 中放入 2-3 个文件：

```text
chapter7_notes.md
chapter8_notes.md
my_learning_notes.md
```

可以先手动总结，不需要把整章文档全部复制进去。

建议内容：

- 第 7 章 Agent 框架总结。
- 第 8 章 RAG 总结。
- 自己容易忘的点。

验收：

- 知识库文件内容清晰，适合被检索。

### Day 2：实现文档加载和切分

任务：

写：

```text
tools/rag_tool.py
```

实现：

```python
load_documents(path)
split_text(text, chunk_size=500)
```

验收：

- 能打印出所有 chunk。

### Day 3：实现关键词检索

任务：

先用简单规则：

- 用户问题分词可以先用空格或字符匹配。
- 计算 query 和 chunk 的关键词重合数。
- 返回 top-k。

验收：

- 问“ReActAgent 是什么”，能检索到第 7 章相关 chunk。

### Day 4：封装成 RAGTool

任务：

工具接口：

```python
RAGTool.run(query: str, top_k: int = 3)
```

返回：

```text
来源文件
chunk 内容
匹配分数
```

验收：

- Agent 可以调用 `rag_search` 工具。

### Day 5：让 Agent 基于检索结果回答

任务：

修改 prompt：

```text
你必须优先基于检索结果回答。
如果检索结果不足，请说明资料中没有找到明确答案。
回答时带上来源文件。
```

验收：

- 问知识库相关问题时，Agent 调用 RAGTool。
- 回答带来源。

### 周末：准备 10 个 RAG 测试问题

示例：

```text
1. SimpleAgent 的职责是什么？
2. ToolRegistry 解决什么问题？
3. ReActAgent 的循环过程是什么？
4. RAGTool 的基本流程是什么？
5. 为什么 Agent 需要记忆？
```

本周验收：

- 能用 Agent 问答本地资料。
- 能看到检索来源。
- 查不到时不会胡编。

---

## 第 4 周：加入学习笔记和上下文

目标：

> 让 Agent 能记录学习过程，并在后续对话中使用这些记录。

### 本周重点

从第 9 章中抽取两个核心能力：

- `NoteTool`
- 简化版 `ContextBuilder`

不需要完整复刻第 9 章所有功能。

### Day 1：设计笔记格式

建议使用 Markdown：

```text
notes/learning_log.md
```

格式：

```markdown
## 2026-05-09

- 学习内容：复习第 7 章 SimpleAgent。
- 卡点：ReActAgent 的工具调用循环还不熟。
- 下一步：闭卷写 ToolRegistry。
```

验收：

- 笔记格式固定，方便后续检索。

### Day 2：实现 NoteTool 写入

工具：

```python
NoteTool.run(action="add", content="...")
```

支持：

- 添加学习记录。
- 添加卡点。
- 添加下一步计划。

验收：

- Agent 能调用 NoteTool 写入 Markdown 文件。

### Day 3：实现 NoteTool 查询

支持：

```python
NoteTool.run(action="search", query="ReAct")
```

验收：

- 能查到过去记录的卡点。

### Day 4：实现简化 ContextBuilder

先实现最小版本：

```python
class ContextBuilder:
    def build(self, user_input, recent_messages, notes, retrieved_docs):
        ...
```

构造上下文时包含：

- 最近 3-5 轮对话。
- 相关笔记。
- RAG 检索结果。

验收：

- Agent 回答时可以看到相关历史信息。

### Day 5：多轮测试

测试流程：

```text
第一轮：我今天复习了第 7 章，但 ReActAgent 还是不熟。
第二轮：请记录这个卡点。
第三轮：我最近学 Agent 卡在哪里？
```

验收：

- Agent 能保存并查询学习状态。

### 周末：整合 RAG + NoteTool

目标：

```text
用户问学习问题
-> Agent 先检索知识库
-> 再查询个人笔记
-> 综合回答
```

本周验收：

- Agent 有最小长期记忆能力。
- 能记录学习状态。
- 能查询历史卡点。

---

## 第 5 周：评估、异常处理和稳定性

目标：

> 不只是让 Agent 能跑，而是知道它哪里好、哪里差、哪里容易失败。

### 本周重点

参考第 12 章的思想，但不要一开始深入 BFCL/GAIA。  
先做自己的小评估集。

### Day 1：准备测试问题

写：

```text
tests/test_cases.md
```

至少 20 个问题，分成 4 类：

1. 普通问答。
2. 计算工具。
3. 知识库问答。
4. 学习笔记查询。

示例：

```markdown
## 计算工具

1. 请计算 23 * 47。
   - 期望：调用 calculator，答案 1081。

## 知识库问答

1. ReActAgent 的核心循环是什么？
   - 期望：调用 rag_search，并回答 Thought/Action/Observation/Final。
```

验收：

- 每个问题都有期望行为。

### Day 2：手动跑测试

任务：

逐个运行 20 个问题，记录：

- 是否答对。
- 是否调用正确工具。
- 是否引用正确来源。
- 错误原因。

输出：

```text
tests/eval_results.md
```

验收：

- 有一份真实评估结果。

### Day 3：补异常处理

重点处理：

- 工具不存在。
- 工具参数不是合法 JSON。
- 工具执行报错。
- RAG 查不到结果。
- LLM 输出格式不符合预期。
- ReAct 超过最大轮数。

验收：

- 常见错误不会让程序直接崩溃。

### Day 4：优化 prompt

优化系统提示词：

```text
当你需要外部信息时，必须调用工具。
当工具结果不足时，不要编造。
最终答案要简洁，并说明依据。
```

验收：

- 工具调用准确率有所提升。

### Day 5：记录 5 个失败案例

每个失败案例记录：

```text
问题：
期望：
实际：
失败原因：
改进方案：
```

验收：

- 至少 5 个失败案例。
- 每个案例都有下一步改进思路。

### 周末：做一次小版本总结

写：

```text
README.md
```

包含：

- 项目简介。
- 架构说明。
- 如何运行。
- 支持的工具。
- 示例对话。
- 测试结果。
- 已知问题。

本周验收：

- 有测试集。
- 有评估结果。
- 有失败案例。
- 程序稳定性明显提升。

---

## 第 6 周：整理成可展示作品

目标：

> 把学习成果整理成一个别人能看懂、你自己能讲清楚的小项目。

### Day 1：整理代码结构

任务：

- 删除临时文件。
- 保留必要日志样例。
- 确保目录结构清晰。
- 每个模块职责明确。

验收：

- 打开项目目录能快速看出入口文件和核心模块。

### Day 2：补 README

README 至少包含：

```markdown
# Learning Agent

## 项目目标

## 核心功能

## 架构设计

## 运行方式

## 工具列表

## 示例对话

## 测试结果

## 已知问题

## 下一步计划
```

验收：

- 别人看 README 能知道你做了什么。

### Day 3：画架构图

可以用文本图：

```text
User
  |
  v
ReActAgent
  |
  +--> LLMClient
  |
  +--> ToolRegistry
          |
          +--> CalculatorTool
          +--> RAGTool
          +--> NoteTool
  |
  +--> ContextBuilder
  |
  +--> Logger
```

验收：

- 你能根据架构图讲 3-5 分钟。

### Day 4：准备演示脚本

演示流程：

1. 普通问答。
2. 计算工具调用。
3. 本地资料问答。
4. 学习笔记保存。
5. 学习状态查询。
6. 查看日志和测试结果。

验收：

- 能稳定演示 5-10 分钟。

### Day 5：最终复盘

写最终总结：

```text
我现在理解的 Agent 是什么？
我写的 Agent 主循环是什么？
ToolRegistry 解决什么问题？
RAGTool 如何工作？
ContextBuilder 如何工作？
我的 Agent 当前有哪些缺陷？
```

验收：

- 能用自己的话解释，而不是背文档。

### 周末：最终验收

最终检查清单：

- [ ] 可以运行 `python run.py`。
- [ ] 可以普通问答。
- [ ] 可以调用计算工具。
- [ ] 可以检索本地知识库。
- [ ] 可以保存学习笔记。
- [ ] 可以查询学习笔记。
- [ ] 有运行日志。
- [ ] 有 20 个测试问题。
- [ ] 有评估结果。
- [ ] 有 README。
- [ ] 能讲清楚架构。

---

## 6. 如果学习时间不足，如何降级

### 6.1 最低可交付版本

如果时间非常紧，只保留：

- `SimpleAgent`
- `ToolRegistry`
- `CalculatorTool`
- `RAGTool`
- README
- 10 个测试问题

可以暂时砍掉：

- NoteTool
- ContextBuilder
- MCP/A2A
- Web UI
- 向量数据库
- 自动评估脚本

最低可交付目标：

> 能从 0 写出一个可以调用工具、可以检索本地资料并回答问题的 Agent。

### 6.2 如果一周完全没时间

不要重启计划。下一次恢复时只做三件事：

1. 读上次写的 README 或学习日志。
2. 运行一次当前代码。
3. 修一个最小问题。

恢复学习时不要重新从第 1 章开始看。

### 6.3 如果只能学 2-3 周

压缩路线：

```text
第 1 周：第 7 章最小框架 + 工具调用
第 2 周：RAGTool + 本地资料问答
第 3 周：README + 测试问题 + 演示
```

放弃：

- NoteTool。
- ContextBuilder。
- 第 10 章协议。
- 第 11 章 Agentic-RL。
- 大项目复现。

---

## 7. 每章如何处理

### 第 7 章：必须重新掌握

学习方式：

1. 先看代码结构。
2. 再看 `SimpleAgent`。
3. 再看 `Tool`。
4. 最后看 `ReActAgent`。
5. 闭卷写最小版本。

重点问题：

- 为什么要有 `Message`？
- 为什么要封装 `LLMClient`？
- `SimpleAgent` 和 `ReActAgent` 的区别是什么？
- 工具为什么要注册？
- Agent 如何知道有哪些工具？
- 最大执行步数解决什么问题？

完成标准：

- 能闭卷写出一个最小 Agent。
- 能新增一个工具。
- 能解释工具调用流程。

### 第 8 章：只取 RAG 和记忆核心

学习方式：

1. 先不用复杂数据库。
2. 先做关键词检索。
3. 再封装成工具。
4. 最后接 Agent。

重点问题：

- 文档为什么要切分？
- chunk 太大或太小有什么问题？
- top-k 是什么？
- 为什么回答要带来源？
- 查不到时该怎么回答？

完成标准：

- Agent 可以问答本地资料。
- 回答有来源。
- 查不到不编造。

### 第 9 章：只取 NoteTool 和 ContextBuilder

学习方式：

1. 先实现 Markdown 笔记。
2. 再实现查询笔记。
3. 最后把笔记放进上下文。

重点问题：

- 上下文不只是历史对话，还包括什么？
- 为什么长任务需要笔记？
- 什么信息应该进入 prompt？
- 什么信息不应该进入 prompt？

完成标准：

- Agent 能记录学习状态。
- Agent 能查询历史卡点。

### 第 10 章：暂时只了解

学习方式：

- 看 MCP/A2A 是解决什么问题。
- 跑一个示例即可。
- 不要深入协议细节。

完成标准：

- 能说出普通 Tool 和 MCP Tool 的区别。

### 第 11 章：暂时跳过

原因：

- Agentic-RL 对入门从 0 写 Agent 不是关键路径。
- 它更偏训练和优化，不适合当前阶段优先投入。

### 第 12 章：提前吸收评估思想

学习方式：

- 不需要完整跑 benchmark。
- 重点学“怎么判断 Agent 好不好”。

重点问题：

- 什么是工具调用准确率？
- 什么是任务成功率？
- 为什么需要失败案例？
- LLM Judge 有什么风险？

完成标准：

- 自己有 20 个测试问题。
- 有评估结果和失败分析。

### 第 13-16 章：作为项目参考

学习方式：

- 看架构。
- 看项目如何拆模块。
- 不完整复现。

完成标准：

- 能借鉴它们的项目结构和 README 写法。

---

## 8. 每周复盘模板

每周末写一次，控制在 10-15 分钟。

```markdown
# 第 X 周复盘

## 本周完成

- 

## 本周没完成

- 

## 卡住的问题

- 

## 我现在能解释清楚的概念

- 

## 我还解释不清楚的概念

- 

## 下周最重要的一件事

- 
```

复盘不是为了写得漂亮，而是为了防止学习断线。

---

## 9. 学习日志模板

每天只需要写 3-5 行。

```markdown
## 2026-xx-xx

- 今天学了：
- 今天写了：
- 今天卡住：
- 明天只做：
```

示例：

```markdown
## 2026-05-09

- 今天学了：复习 SimpleAgent 的 run 流程。
- 今天写了：Message、MockLLM、SimpleAgent。
- 今天卡住：工具调用结果如何重新放回 prompt。
- 明天只做：看 CalculatorTool 并写自己的 BaseTool。
```

---

## 10. 不要做的事情

当前阶段尽量避免：

1. 不要重新从第 1 章完整精读。
2. 不要追求把所有章节都学完。
3. 不要一开始做 Web UI。
4. 不要一开始上复杂向量数据库。
5. 不要一开始研究第 11 章 Agentic-RL。
6. 不要为了“完美架构”重构太多。
7. 不要只看文档不写代码。
8. 不要因为中断几天就放弃整个计划。

---

## 11. 建议的第一天行动

今天只做这几件事：

1. 打开第 7 章文档，只看目录 10 分钟。
2. 打开：

   ```text
   code/chapter7/my_simple_agent.py
   ```

   只看 `SimpleAgent` 的结构，不逐行背。

3. 新建：

   ```text
   learning_agent/
   ```

4. 闭卷写：

   ```text
   message.py
   llm.py
   agent.py
   run.py
   ```

5. 跑通：

   ```text
   用户输入
   -> MockLLM 返回固定回答
   -> Agent 保存历史
   -> 打印回答
   ```

今天的目标不是写得完整，而是重新启动输出能力。

---

## 12. 最终判断标准

当你做到下面这些，就可以认为自己完成了 Agent 入门：

- 能从 0 写出 `SimpleAgent`。
- 能从 0 写出 `Tool` 和 `ToolRegistry`。
- 能写一个 `ReActAgent` 最小循环。
- 能新增一个自定义工具。
- 能把 RAG 封装成工具。
- 能让 Agent 基于本地资料回答问题。
- 能保存和查询学习笔记。
- 能记录运行日志。
- 能用测试问题评估 Agent。
- 能讲清楚当前项目架构和缺陷。

不需要等到学完所有章节才算入门。  
你真正需要的是完成一个小闭环：

```text
Agent 框架
-> 工具调用
-> 本地资料检索
-> 上下文和笔记
-> 日志和评估
-> 可展示项目
```

完成这个闭环后，再继续学习第 10、11、13-16 章，会轻松很多。
