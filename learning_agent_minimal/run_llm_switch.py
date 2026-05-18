from llm import MockLLM
from real_llm import RealLLM
from learning_assistant import LearningAssistant
mockLLM = MockLLM()
realLLM = RealLLM()
messages= []
messages.append({"role":"user","content":"测试问题"})
response1 = mockLLM.invoke(messages)
response2 = realLLM.invoke(messages)
print(f"mockllm:{response1}\n\nrealllm:{response2}")
assistant = LearningAssistant(llm=MockLLM())
print(assistant.answer("我现在应该复习 ReActAgent 的什么？"))