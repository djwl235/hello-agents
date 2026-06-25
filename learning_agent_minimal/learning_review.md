1. MCP 解决了什么问题？
    MCP 把工具发现、参数 schema 和调用方式标准化，减少每个工具都单独适配的成本。Agent 可以通过 MCP Client 连接 MCP Server，发现并调用别人发布的工具，也可以把自己写的能力暴露成 MCP 工具。需要注意的是，MCP 不等于自动免鉴权，很多外部 MCP Server 仍然需要配置 API key 或授权信息。
2. Embedding RAG 比关键词 RAG 强在哪里？
    关键词 RAG 主要依赖字面匹配，容易漏掉同义表达，也容易因为字符重合产生误召回。Embedding RAG 会把 query 和 chunk 都转换成向量，再计算 query embedding 与 chunk embedding 的相似度，因此更能捕捉语义相关性。“国王 - 男性 + 女性 = 女王”适合帮助理解词向量空间，但在 RAG 中实际比较的是 query embedding 和 chunk embedding。
3. min_score 和 top_k 的区别是什么？
    前者是一个门槛只有query和content的分数大于这个才能够计入到results中待选择,而后者是选择几个,即在前述已经计入results中的选择分数前k个的
4. StructuredNoteTool 比 NoteTool 强在哪里？
    包括了tags summary content等不同的key,summary更方便上下文压缩,tag方便快速分类和检索,type区分这条笔记的种类
5. 当前项目还有哪些限制？
    StructuredNoteTool的type固定为learning,summary直接截取50个,应该接入llm进行总结摘要,整体结构有些混乱.
6. 如果从 0 重写，我会怎么设计？
    首先完成agent loop的最小mvp,之后完成工具中心(同时接入mcp),接着为embeddingRAG,最后是结构化notetool.同时跳过vectorRAG,普通notetool等功能.

1. 用户问题 -> LearningAssistant -> RAG/Note -> ContextBuilder -> Agent -> LLM
    用户输入问题,LearningAssistant首先进行意图路由,如果为工具请求那么进入下述的2.否则首先调用RAG和Note工具搜索与用户输入相关的上下文,调用ContextBuilder将历史记录RAG等工具得到的内容构建为上下文输入给Agent作为整体的用户输入,SimpleAgent 会构造 system prompt + history + 当前用户输入；如果注册了工具，还会把工具描述和工具调用格式加入 system prompt，然后调用 LLM。
2. 用户工具请求 -> Agent -> ToolRegistry -> Tool / MCPProxyTool -> Observation
    用户工具请求不再LearningAssistant进行上下文拼接直接输入给agent,agent将其输入给llm得到符合规范的工具调用格式输入到ToolRegistry中,ToolRegistry据此调用工具,得到的结果作为Observation加入上下文中,SimpleAgent 最多循环 max_iterations 次；如果 LLM 一直请求工具，循环结束后返回最后一次 LLM 输出,没达到便继续将上下文输入给llm进行下一轮迭代直到输出最终回答或达到最大迭代次数为止.
3. 知识库 -> chunk -> embedding -> index cache -> query embedding -> top_k + min_score
    知识库通过函数在按空行切分 chunk将chunk输入模型得到向量,同时将此向量存放到json以便下一次使用;用户查询时将查询也向量化,利用余弦相似度计算,通过top_k + min_score予以筛选.top_k 决定最多返回几个 chunk，min_score 决定低于相似度阈值的 chunk 不进入候选结果。