
from dotenv import load_dotenv
from my_llm import MyLLM # 注意:这里导入我们自己的类
load_dotenv()
llm = MyLLM(provider='modelscope')
messages = [{"role":"user","content":"你好，请介绍一下你自己。"}]
response_stream = llm.think(messages=messages)
print("ModelScope Response:")
for chunk in response_stream:
    pass