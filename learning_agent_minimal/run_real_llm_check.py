from real_llm import RealLLM
llm = RealLLM()
messages = []
messages.append({"role":"user","content":"你好"})
print(llm.invoke(messages=messages))