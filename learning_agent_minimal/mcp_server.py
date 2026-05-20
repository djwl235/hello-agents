"""
Minimal MCP server for learning.

Run as an MCP stdio server:
    python mcp_server.py
"""

from fastmcp import FastMCP


mcp = FastMCP("LearningMCPServer")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


@mcp.tool()
def count_chars(text: str) -> int:
    """Return the number of characters in text."""
    return len(text)


@mcp.resource("config://learning-assistant")
def get_learning_config()->str:
    """返回学习助手的配置和能力"""
    return """
    学习助手支持的能力：
    1. Tool: add - 两个数字相加
    2. Tool: count_chars - 统计字符数
    3. Prompt: mcp_learning_prompt - 如何使用 MCP 工具
    """

@mcp.prompt("mcp_learning_prompt")
def mcp_learning_guide() -> str:
    """返回如何使用 MCP 工具的提示词"""
    return """
    # 如何使用 MCP 工具
    
    1. 基础计算：使用 add 工具
       - 输入：两个数字
       - 格式：[TOOL_CALL:mcp_add:12 30]
    
    2. 字符统计：使用 count_chars 工具
       - 输入：任意文本
       - 格式：[TOOL_CALL:mcp_count_chars:hello agents]
    
    3. 查询资源：通过 list_resources 获取
       - config://learning-assistant 配置信息
       - status://learning-state 学习状态
    """

if __name__ == "__main__":
    mcp.run()
