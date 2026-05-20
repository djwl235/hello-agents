
from fastmcp import Client
import asyncio
from pathlib import Path
from tools.mcp_proxy_tool import MCPProxyTool
from tools.mcp_tool_factory import MCPToolFactory
from tools.registry import ToolRegistry
def main():
    root_dir = Path("learning_agent_minimal").resolve()
    config = {
      "mcpServers": {
          "filesystem": {
              "command": "npx",
              "args": [
                  "-y",
                  "@modelcontextprotocol/server-filesystem",
                  str(root_dir),
              ],
              "transport": "stdio",
          }
      }
    }
    tool_registry = ToolRegistry()
    tools = MCPToolFactory(config).create_tools()
    for tool in tools:
        print(tool.name)
        print(tool.description)
        print(tool.input_schema)
        print()
        tool_registry.register(tool=tool)
    result = tool_registry.execute(name="mcp_list_directory",tool_input="learning_agent_minimal")
    print(result)

if __name__ == '__main__':
    main()