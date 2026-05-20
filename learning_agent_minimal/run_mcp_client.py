import asyncio
from pathlib import Path

from fastmcp import Client


async def main():
    server_path = Path(__file__).with_name("mcp_server.py")
    client = Client(server_path)

    async with client:
        tools = await client.list_tools()
        print("Available MCP tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            print(f"  input schema: {tool.inputSchema}")

        add_result = await client.call_tool("add", {"a": 12, "b": 30})
        print(f"add result data: {add_result.data}")

        count_result = await client.call_tool(
            "count_chars",
            {"text": "hello agents"},
        )
        print(f"count_chars result data: {count_result.data}")
        
        resources = await client.list_resources()
        print("Available resources:")
        for resource in resources:
            print(f"- {resource.uri}: {resource.description}")
        
        try:
            config = await client.read_resource("config://learning-assistant")
            print(f"Config object type: {type(config)}")
            print(f"Config content: {config}")
        except Exception as e:
            print(f"Error reading resource: {e}")

        prompts = await client.list_prompts()
        print("Available prompts:")
        for prompt in prompts:
            print(f"- {prompt.name}: {prompt.description}")
        
        try:
            guide = await client.get_prompt("mcp_learning_prompt")
            print(f"Learning guide type: {type(guide)}")
            print(f"Learning guide: {guide}")
        except Exception as e:
            print(f"Error getting prompt: {e}")

if __name__ == '__main__':
    asyncio.run(main())
