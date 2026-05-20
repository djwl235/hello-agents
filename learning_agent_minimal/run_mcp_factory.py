from tools.mcp_tool_factory import MCPToolFactory
from tools.registry import ToolRegistry

tool_registry = ToolRegistry()

tool_factory = MCPToolFactory("learning_agent_minimal/mcp_server.py")
tools = tool_factory.create_tools()
for tool in tools:
    print(f"{tool.name}:{tool.description}")
    tool_registry.register(tool=tool)
result1 = tool_registry.execute(name="mcp_add",tool_input="12 30")
print(result1)
result2 = tool_registry.execute(name="mcp_count_chars",tool_input="hello agents")
print(result2)