from importlib import metadata

try:
    from hello_agents.tools import MCPTool, A2ATool, ANPTool
except ImportError as exc:
    installed_version = metadata.version("hello-agents")
    raise SystemExit(
        "当前环境里的 hello-agents 版本是 "
        f"{installed_version}，它不包含 MCPTool / A2ATool / ANPTool。"
        " 这个示例需要支持协议模块的较新版本 hello-agents[protocols]，"
        "并且建议使用 Python 3.11 或 3.12，而不是 Python 3.13。"
    ) from exc

# 1. MCP：访问工具
mcp_tool = MCPTool()
result = mcp_tool.run({
    "action": "call_tool",
    "tool_name": "add",
    "arguments": {"a": 10, "b": 20}
})
print(f"MCP计算结果: {result}")  # 输出: 30.0

# 2. ANP：服务发现
anp_tool = ANPTool()
anp_tool.run({
    "action": "register_service",
    "service_id": "calculator",
    "service_type": "math",
    "endpoint": "http://localhost:8080"
})
services = anp_tool.run({"action": "discover_services"})
print(f"发现的服务: {services}")

# 3. A2A：智能体通信
a2a_tool = A2ATool("http://localhost:5000")
print("A2A工具创建成功")