from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from typing import List
from hello_agents.tools import MemoryTool
def memory_exeucute_demo():
    print("MemoryTool基础操作演示")
    memorytool = MemoryTool(
        user_id="demouser",
        memory_types=["working", "episodic", "semantic", "perceptual"]
    )
    return memorytool
def add_memory_demo(memorytool):
    print("添加工作记忆")
    result = memorytool.run({
        "action":"add",
        "content":"正在学习HelloAgents框架的记忆系统",
        "memory_type":"working",
        "importance":0.7,
        "task_type":"learning"
    })
    print(f"工作记忆{result}")
    print("添加情景记忆")
    result = memorytool.run({
        "action":"add",
        "content":"2024年开始深入研究AI Agent技术",
        "memory_type":"episodic",
        "importance":0.8,
        "event_type":"milestone",
        "location":"研发中心"
    })
    print(f"情景记忆: {result}")
    print("添加语义记忆")
    result = memorytool.run({
        "action":"add",
        "content":"记忆系统包括工作记忆、情景记忆、语义记忆和感知记忆四种类型",
        "memory_type":"semantic",
        "importance":0.9,
        "concept":"memory_types",
        "domain":"cognitive_science"
    })
    print(f"语义记忆: {result}")
    print("添加感知记忆")
    result = memorytool.run({
        "action":"add",
        "content":"查看了记忆系统的架构图和实现代码",
        "memory_type":"perceptual",
        "importance":0.6,
        "modality":"document",
        "source":"technical_documentation"
    })
    print(f"感知记忆: {result}")
def search_memory_demo(memorytool):
    print("\n🔍 搜索记忆演示")
    print("-" * 30)
    
    # 基础搜索
    print("基础搜索 - '记忆系统':")
    result = memorytool.run({
        "action":"search",
        "query":"记忆系统",
        "limit":3
    })
    print(result)

    print("搜索语义记忆中的记忆")
    result = memorytool.run({
        "action":"search",
        "query":"记忆",
        "limit":3,
        "memory_type":"semantic"
    })
    print(result)

    print("\n高重要性记忆搜索")
    result = memorytool.run({
        "action":"search", 
        "query":"AI Agent", 
        "min_importance":0.7, 
        "limit":3
    })
    print(result)

def memory_summary_demo(memorytool):
    print("获取记忆摘要")
    result = memorytool.run({
        "action":"summary",
        "limit":5
    })
    print("记忆摘要:")
    print(result)
    print("\n📊 统计信息:")
    result = memorytool.run({"action": "stats"})
    print(result)
def memory_management_demo(memorytool):
    print("记忆管理演示")
    print("遗忘低重要性记忆")
    memorytool.run({
        "action":"add",
        "content":"非重要记忆测试",
        "memory_type":"working",
        "importance":0.1,
        "task_type":"learning1"
    })
    result = memorytool.run({
        "action":"forget",
        "threshold":0.1
    })
    print(result)
    print("\n记忆整合 (working → episodic):")
    result = memorytool.run({
        "action":"consolidate",
        "from_type":"working",
        "to_type":"episodic",
        "importance_threshold":0.6
    })
    print(result)
def main():
    print("🚀 MemoryTool基础操作完整演示")
    print("展示记忆系统的核心功能和操作方法")
    print("=" * 60)
    try:
        # 1. 初始化MemoryTool
        memory_tool = memory_exeucute_demo()
        
        # 2. 添加记忆演示
        add_memory_demo(memory_tool)
        
        # 3. 搜索记忆演示
        search_memory_demo(memory_tool)
        
        # 4. 记忆摘要演示
        memory_summary_demo(memory_tool)
        
        # 5. 记忆管理演示
        memory_management_demo(memory_tool)
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
if __name__ == "__main__":
    main()