from learning_assistant import LearningAssistant
from real_llm import RealLLM
from pathlib import Path
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
assistant = LearningAssistant(llm= RealLLM(),server_path = config)
print(assistant.tool_registry.list_tools())

print(assistant.answer("请通过 MCP 列出 learning_agent_minimal 文件夹下的内容"))