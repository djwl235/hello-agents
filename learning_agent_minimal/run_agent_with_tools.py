from llm import MockLLM
from agent import SimpleAgent
from tools.calculator import CalculatorTool
from tools.rag_tool import RAGTool
from tools.registry import ToolRegistry
from tools.note_tool import NoteTool

registry = ToolRegistry()
registry.register(CalculatorTool())
registry.register(RAGTool(knowledge_dir="learning_agent_minimal/knowledge_base"))
registry.register(NoteTool(note_path="learning_agent_minimal/notes/learning_log.md"))
llm = MockLLM()

agent = SimpleAgent(
    name="工具助手",
    llm=llm,
    tool_registry=registry
)

# response = agent.run("请计算 23 * 47")
# print(response)

# response = agent.run("查找ReActAgent 的核心循环是什么？")
# print(response)

agent.run("记录今天学习了 NoteTool，理解了 add/search/list 三个动作")
response  = agent.run("查询笔记 NoteTool")
print(response)

print("历史消息数量：", len(agent.get_history()))