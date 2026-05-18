
class ToolRegistry:
    def __init__(self):
        self._tool = {}
    def register(self,tool):
        self._tool[tool.name] = tool
#     register：注册工具
#   get_tool：按名字找工具
#   list_tools：列出工具名
#   get_tools_description：给 LLM 看的工具说明
#   execute：统一执行工具
    def get_tool(self,name):
        return self._tool.get(name)
    def list_tools(self):
        return list(self._tool.keys())
    def get_tools_description(self):
        tool_description = []
        for tool_name,tool in self._tool.items():
            tool_description.append(f"- {tool.name}: {tool.description}")
        return "\n".join(tool_description)
    def execute(self,name,tool_input):
        tool = self.get_tool(name)
        if tool is None:
            return f"没有{name}工具"
        return tool.run(tool_input)
        