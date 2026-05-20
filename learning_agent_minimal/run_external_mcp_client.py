import asyncio
from pathlib import Path

from fastmcp import Client
async def main():
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
    client = Client(config)
    async with client:
        tools = await client.list_tools()
        for tool in tools:
              print(tool.name)
              print(tool.description)
              print(tool.inputSchema)
              print()
        result = await client.call_tool("list_directory", {"path": "learning_agent_minimal"})
        print(result.data)
        result = await client.call_tool("read_file", {"path": "learning_agent_minimal\README.md"})
        print(result.data)
if __name__ == "__main__":
    asyncio.run(main())