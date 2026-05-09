from llm import MockLLM
from agent import SimpleAgent
llm = MockLLM()
agent = SimpleAgent(name="学习助手",llm=llm)
print(agent.run("你好"))
print(agent.run("我刚才说了什么？"))
print("历史消息数量：", len(agent.get_history()))
for msg in agent.get_history():
    print(msg.role, ":", msg.content)