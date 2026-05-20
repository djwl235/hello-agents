import asyncio
from fastmcp import Client
from .base import BaseTool

class MCPProxyTool(BaseTool):
    def __init__(self,name,description,server_config,remote_tool_name,input_schema):
        self.name = name
        self.description = description
        self.server_config = server_config
        self.remote_tool_name = remote_tool_name
        self.input_schema = input_schema
    def run(self,tool_input:str):
        try:
            arguments = self._parse_input(tool_input)
            result = asyncio.run(self._call_remote_tool(arguments=arguments))
            return str(result)
        except Exception as e:
            return f"MCP 工具调用失败: {e}"

    def _parse_input(self, tool_input: str):
        properties = self.input_schema["properties"]
        if len(properties) == 1:
            for key,value in properties.items():
                if value["type"] == "string":
                    return {key: tool_input}
                elif value["type"] == "number":
                    return {key: float(tool_input)}
        elif len(properties) == 2:
            for key,value in properties.items():
                if value["type"] != "number":
                    raise ValueError("暂不支持这个 MCP 工具参数格式")
            kname = []
            for key in properties:
                kname.append(key)
            number = tool_input.split()
            if len(number) != 2:
                raise ValueError("暂不支持这个 MCP 工具参数格式")
            else:
                return {kname[0]: float(number[0]), kname[1]: float(number[1])}
        raise ValueError("暂不支持这个 MCP 工具参数格式")
    async def _call_remote_tool(self,arguments):
        client = Client(self.server_config)
        async with client:
            result = await client.call_tool(name=self.remote_tool_name,arguments=arguments)
            return result.data
        