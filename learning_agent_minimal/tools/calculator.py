from .base import BaseTool
class CalculatorTool(BaseTool):
    name = "calculator"
    description = "可用于计算，例如23 * 37"
    def run(self,tool_input:str):
        if tool_input is None:
            return "请输入要计算的式子"
        try:
            result = eval(tool_input)
            return str(result)
        except Exception as e:
            return f"计算错误{e}"
