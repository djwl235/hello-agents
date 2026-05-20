from llm import MockLLM
from agent import SimpleAgent
from tools.calculator import CalculatorTool
from tools.rag_tool import RAGTool
from tools.registry import ToolRegistry
from tools.note_tool import NoteTool
from context import ContextBuilder
from tools.mcp_tool_factory import MCPToolFactory
class LearningAssistant:
    def __init__(self,server_path = None,llm = None):
        self.llm = llm or MockLLM()
        self.tool_registry = ToolRegistry()
        self.tool_registry.register(CalculatorTool())
        self.tool_registry.register(RAGTool(knowledge_dir="learning_agent_minimal/knowledge_base"))
        self.tool_registry.register(NoteTool(note_path="learning_agent_minimal/notes/learning_log.md"))
        self.server_path = server_path
        self.add_MCP_tool()
        self.agent = SimpleAgent(name="学习助手",
                    llm= self.llm,
                    tool_registry=self.tool_registry)
    def answer(self,user_input):
        intent = self.route_intent(user_input=user_input)
        if intent == "direct_tool":
            return self.agent.run(user_input)
        rag_query = self.build_rag_query(user_input=user_input)
        note_query = self.build_note_query(user_input=user_input)
        rag_context = self.tool_registry.execute("rag_search",rag_query)
        note_context = self.tool_registry.execute("note",f"search {note_query}")
        context = ContextBuilder().build(
            history=self.agent.get_history(),
            user_input=user_input,
            rag_context=rag_context,
            note_context=note_context
        )
        return self.agent.run(context)
    def build_rag_query(self,user_input):
        return user_input
    def build_note_query(self,user_input):
        keywords = ["NoteTool", "RAGTool", "ReActAgent", "ToolRegistry", "ContextBuilder"]
        for keyword in keywords:
            if keyword in user_input:
                return keyword
        return user_input
    def route_intent(self,user_input):
        if "记录" in user_input:
          return "direct_tool"
        if "查询笔记" in user_input:
            return "direct_tool"
        if "MCP" in user_input and ("计算" in user_input or "统计字符" in user_input):
            return "direct_tool"
        if "计算" in user_input:
            return "direct_tool"
        return "learning_advice"
    def add_MCP_tool(self):
        if self.server_path == None:
            return
        tools = MCPToolFactory(server_config=self.server_path).create_tools()
        for tool in tools:
            self.tool_registry.register(tool=tool)
        return