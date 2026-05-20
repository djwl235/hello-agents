import asyncio
from pathlib import Path
from fastmcp import Client
from .mcp_proxy_tool import MCPProxyTool
class MCPToolFactory:
    def __init__(self,server_config):
        self.server_config = server_config
    def create_tools(self):
        return asyncio.run(self._create_tools())
    async def _create_tools(self):
        client = Client(self.server_config)
        proxy_tools = []
        async with client:
            remote_tools = await client.list_tools()
            for remote_tool in remote_tools:
                tool = MCPProxyTool(
                    name = f"mcp_{remote_tool.name}",
                    description=remote_tool.description,
                    server_config=self.server_config,
                    remote_tool_name=remote_tool.name,
                    input_schema=remote_tool.inputSchema
                )
                proxy_tools.append(tool)
        return proxy_tools