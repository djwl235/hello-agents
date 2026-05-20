  1. MCP 解决了什么问题
  MCP全称是模型上下文协议，根本上是定义了一套外部工具的使用方式，agent想要接入外部工具只需要将其暴露出的接口适配成本地接口即可，无需再去编写一套代码。
  2. MCP Server / Client / Tool 的关系
  服务端提供工具，客户端调用服务端的工具。
  3. Tool / Resource / Prompt 的区别
  工具是能够真正执行产生作用的代码；资源是资料可以包括支持的能力等等；提示词是如何使用MCP工具的完成说明
  4. 我的项目里 MCP 的调用链
  learningAssistant调用MCPFactory，工厂通过创建client与服务端相连接列出拥有的工具同时注册到本地工具注册中心，接着调用Agent通过llm的返回来调用mcp工具。（到本地工具注册中心就与本地工具无二都是一样的调用方式了）
  5. MCPProxyTool 的作用
  将MCP工具的输入输出调用方式适配为和本地BaseTool一样的形式
  6. MCPToolFactory 的作用
  连接server列出工具资源提示词等，返回现有MCP工具
  7. 当前实现的限制
    - MCPProxyTool 的参数解析只支持一个 string 参数或两个 number 参数
  - 每次工具调用都会重新启动一次 MCP Server，效率不高
  - 真实 LLM 是否稳定选择 MCP 工具还没验证
  - Resource 和 Prompt 目前只在 client demo 中读取，还没接入 Agent 上下文
  8. 下一步可以优化什么
  接入外部MCP工具