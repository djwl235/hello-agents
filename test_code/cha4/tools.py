import os
from dotenv import load_dotenv
from serpapi import SerpApiClient
load_dotenv()
def search(query:str)->str:
    print("正在网页搜索："+query)
    try:
        api_key=os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "搜索api_key未配置"
        params = {
            "engine" : "google",
            "q" : query,
            "api_key":api_key,
            "gl":"cn",
            "hl":"zh-cn",
        }
        client = SerpApiClient(params)
        results=client.get_dict()
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            snippets=[]
            for i,res in enumerate(results["organic_results"][:3]):
                snippet_text = res.get('snippet', '') or res.get('snippets', '')
                text = f"{i+1}. {res.get('title', '')}\n{snippet_text}\n"
                snippets.append(text)
            return "\n".join(snippets)
        return "没找到关于"+query+"的信息"
    except Exception as e:
        return "搜索时发生错误: "+str(e)
from typing import Dict, Any
class ToolExecutor:
    def __init__(self):
        self.tools:Dict[str,Dict[str,Any]]={}
    def registerTool(self,name:str,description:str,func:callable):
        if name in self.tools:
            print("警告，已存在此工具，将被覆盖")
        self.tools[name]={"description":description,"func":func}
        print(name+"工具已注册")
    def getTool(self,name:str)->callable:
        if name not in self.tools:
            return None
        return self.tools[name].get("func")
    def getAvailableTools(self)->str:
        result=[]
        for name,info in self.tools.items():
            result.append('\n'+name+info['description'])
        return "\n".join(result)
    
if __name__ == '__main__':
    toolExecutor=ToolExecutor()
    search_description = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("Search", search_description, search)
    print(toolExecutor.getAvailableTools())
    print("\n--- 执行 Action: Search['华为手机的最新型号'] ---")
    tool_name = "Search"
    tool_input = "华为手机的最新型号"
    tool_func=toolExecutor.getTool(tool_name)
    if tool_func :
        observation = tool_func(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")