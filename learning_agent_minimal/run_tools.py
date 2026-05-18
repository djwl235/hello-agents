from tools.registry import ToolRegistry
from tools.calculator import CalculatorTool
calculator = CalculatorTool()
tool_registry = ToolRegistry()
tool_registry.register(calculator)
print("可用工具：", tool_registry.list_tools())
print("工具说明：")
print(tool_registry.get_tools_description())

result = tool_registry.execute("calculator", "23 * 47")
print("计算结果：", result)

bad_result = tool_registry.execute("unknown", "123")
print("错误测试：", bad_result)