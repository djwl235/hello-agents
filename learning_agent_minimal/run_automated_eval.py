"""
自动化端到端评估脚本
自动运行所有测试case，验证结果，生成评估报告
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from learning_assistant import LearningAssistant
from real_llm import RealLLM


class EvalCase:
    """评估用例定义"""
    def __init__(self, 
                 case_id: int,
                 question: str,
                 expected_tools: List[str] = None,
                 expected_keywords: List[str] = None,
                 description: str = ""):
        self.case_id = case_id
        self.question = question
        self.expected_tools = expected_tools or []
        self.expected_keywords = expected_keywords or []
        self.description = description
        
        # 评估结果
        self.response = ""
        self.tools_called = []
        self.success = False
        self.keywords_found = []
        self.failure_reason = ""
        self.improvement_suggestion = ""
        self.execution_time = 0


class EvaluationEngine:
    """评估引擎"""
    def __init__(self, assistant: LearningAssistant):
        self.assistant = assistant
        self.cases = []
        self.results = []
        
    def add_case(self, case: EvalCase):
        """添加评估用例"""
        self.cases.append(case)
        
    def run_all_cases(self):
        """运行所有用例"""
        print("=" * 80)
        print("开始自动化端到端评估")
        print(f"总测试数: {len(self.cases)}")
        print("=" * 80)
        print()
        
        for i, case in enumerate(self.cases, 1):
            print(f"【测试 {i}/{len(self.cases)}】{case.description or case.question}")
            self._run_single_case(case)
            print(f"✓ 完成")
            print()
            
        return self.results
    
    def _run_single_case(self, case: EvalCase):
        """运行单个用例"""
        start_time = time.time()
        
        try:
            # 运行问题
            response = self.assistant.answer(case.question)
            case.response = response
            case.execution_time = time.time() - start_time
            
            # 验证结果
            self._validate_case(case)
            self.results.append(case)
            
        except Exception as e:
            case.failure_reason = str(e)
            case.success = False
            case.execution_time = time.time() - start_time
            self.results.append(case)
    
    def _validate_case(self, case: EvalCase):
        """验证用例结果"""
        response_lower = case.response.lower()
        
        # 检查关键词
        keywords_found = []
        for keyword in case.expected_keywords:
            if keyword.lower() in response_lower:
                keywords_found.append(keyword)
        
        case.keywords_found = keywords_found
        
        # 判断成功条件
        # 如果有期望的关键词，需要找到至少一个
        if case.expected_keywords:
            case.success = len(keywords_found) > 0
            if not case.success:
                case.failure_reason = f"未找到期望的关键词: {', '.join(case.expected_keywords)}"
        else:
            # 没有关键词要求的case，只要有非空回答就算成功
            case.success = bool(case.response.strip())
            if not case.success:
                case.failure_reason = "回答为空"
    
    def generate_report(self, output_file: str = None) -> str:
        """生成评估报告"""
        report_lines = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 报告头部
        report_lines.append("# 自动化端到端评估报告\n")
        report_lines.append(f"**生成时间**: {timestamp}\n")
        report_lines.append(f"**评估工具**: LearningAssistant (RealLLM)\n")
        
        # 统计信息
        total_cases = len(self.results)
        success_cases = sum(1 for r in self.results if r.success)
        failed_cases = total_cases - success_cases
        success_rate = (success_cases / total_cases * 100) if total_cases > 0 else 0
        total_time = sum(r.execution_time for r in self.results)
        
        report_lines.append(f"**总测试数**: {total_cases}\n")
        report_lines.append(f"**成功数**: {success_cases}\n")
        report_lines.append(f"**失败数**: {failed_cases}\n")
        report_lines.append(f"**成功率**: {success_rate:.1f}%\n")
        report_lines.append(f"**总耗时**: {total_time:.2f}s\n")
        
        report_lines.append("\n---\n\n")
        
        # 详细结果
        report_lines.append("## 测试详情\n\n")
        
        for case in self.results:
            report_lines.append(f"### 测试 {case.case_id}\n")
            report_lines.append(f"**问题**: {case.question}\n\n")
            report_lines.append(f"**期望关键词**: {', '.join(case.expected_keywords) if case.expected_keywords else '无'}\n\n")
            report_lines.append(f"**期望工具**: {', '.join(case.expected_tools) if case.expected_tools else '无'}\n\n")
            report_lines.append(f"**测试结果**: {'✅ 通过' if case.success else '❌ 失败'}\n\n")
            report_lines.append(f"**执行时间**: {case.execution_time:.2f}s\n\n")
            
            if case.keywords_found:
                report_lines.append(f"**找到关键词**: {', '.join(case.keywords_found)}\n\n")
            
            if case.failure_reason:
                report_lines.append(f"**失败原因**: {case.failure_reason}\n\n")
            
            report_lines.append(f"**回答内容**:\n```\n{case.response}\n```\n\n")
            report_lines.append("---\n\n")
        
        # 总结
        report_lines.append("## 测试总结\n\n")
        report_lines.append(f"- **通过率**: {success_rate:.1f}%\n")
        report_lines.append(f"- **总用例数**: {total_cases}\n")
        report_lines.append(f"- **平均耗时**: {total_time/total_cases:.2f}s\n")
        
        if failed_cases > 0:
            failed_case_ids = [str(r.case_id) for r in self.results if not r.success]
            report_lines.append(f"- **失败用例**: {', '.join(failed_case_ids)}\n")
        
        report_text = "".join(report_lines)
        
        # 保存到文件
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\n📝 报告已保存到: {output_file}")
        
        return report_text
    
    def generate_json_report(self, output_file: str = None) -> str:
        """生成JSON格式的详细报告"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_cases": len(self.results),
                "success_cases": sum(1 for r in self.results if r.success),
                "failed_cases": sum(1 for r in self.results if not r.success),
                "success_rate": (sum(1 for r in self.results if r.success) / len(self.results) * 100) if self.results else 0,
                "total_execution_time": sum(r.execution_time for r in self.results)
            },
            "cases": []
        }
        
        for case in self.results:
            case_data = {
                "case_id": case.case_id,
                "question": case.question,
                "description": case.description,
                "success": case.success,
                "execution_time": case.execution_time,
                "expected_tools": case.expected_tools,
                "expected_keywords": case.expected_keywords,
                "keywords_found": case.keywords_found,
                "failure_reason": case.failure_reason,
                "response": case.response
            }
            data["cases"].append(case_data)
        
        json_text = json.dumps(data, ensure_ascii=False, indent=2)
        
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_text)
            print(f"📊 JSON报告已保存到: {output_file}")
        
        return json_text


def setup_eval_cases() -> List[EvalCase]:
    """设置所有评估用例"""
    cases = [
        EvalCase(
            case_id=1,
            question="请计算 12 + 30 / 3",
            expected_tools=["calculator"],
            expected_keywords=["22"],
            description="基础算术计算 (加除法)"
        ),
        EvalCase(
            case_id=2,
            question="请计算 8 * 9",
            expected_tools=[],  # 可能直接计算或调用工具
            expected_keywords=["72"],
            description="基础算术计算 (乘法)"
        ),
        EvalCase(
            case_id=3,
            question="记录今天复习了 RealLLM 工具调用",
            expected_tools=["note"],
            expected_keywords=["成功", "记录"],
            description="笔记记录功能"
        ),
        EvalCase(
            case_id=4,
            question="查询笔记 RAGTool",
            expected_tools=["note"],
            expected_keywords=["RAGTool"],
            description="笔记查询 - RAGTool"
        ),
        EvalCase(
            case_id=5,
            question="查询笔记 RealLLM",
            expected_tools=["note"],
            expected_keywords=["RealLLM"],
            description="笔记查询 - RealLLM"
        ),
        EvalCase(
            case_id=6,
            question="RAGTool 的评分函数哪里容易出问题？",
            expected_tools=[],
            expected_keywords=["字符", "语义", "匹配"],
            description="知识库问答 - RAGTool评分"
        ),
        EvalCase(
            case_id=7,
            question="我现在应该复习 ReActAgent 的什么？",
            expected_tools=[],
            expected_keywords=["ReActAgent", "复习", "核心"],
            description="学习建议 - ReActAgent"
        ),
        EvalCase(
            case_id=8,
            question="ToolRegistry 的作用是什么？",
            expected_tools=[],
            expected_keywords=["ToolRegistry", "工具", "管理"],
            description="知识库问答 - ToolRegistry"
        ),
        EvalCase(
            case_id=9,
            question="刚才我问了什么？",
            expected_tools=[],
            expected_keywords=["ToolRegistry"],
            description="上下文记忆 - 回忆前一个问题"
        ),
        EvalCase(
            case_id=10,
            question="查找本地知识库 ReActAgent 的核心循环是什么？",
            expected_tools=[],
            expected_keywords=["ReActAgent", "思考", "动作", "观察"],
            description="知识库问答 - ReActAgent核心循环"
        ),
    ]
    return cases


def main():
    """主函数"""
    # 初始化助手和评估引擎
    print("初始化 LearningAssistant...")
    assistant = LearningAssistant(llm=RealLLM())
    engine = EvaluationEngine(assistant)
    
    # 添加所有用例
    print("加载测试用例...")
    for case in setup_eval_cases():
        engine.add_case(case)
    
    print(f"已加载 {len(engine.cases)} 个测试用例\n")
    
    # 运行评估
    engine.run_all_cases()
    
    # 生成报告
    print("\n" + "=" * 80)
    print("生成评估报告")
    print("=" * 80 + "\n")
    
    # 生成Markdown报告
    report_path = "learning_agent_minimal/eval_reports/automated_eval_report.md"
    engine.generate_report(report_path)
    
    # 生成JSON报告
    json_report_path = "learning_agent_minimal/eval_reports/automated_eval_report.json"
    engine.generate_json_report(json_report_path)
    
    # 打印控制台总结
    total = len(engine.results)
    success = sum(1 for r in engine.results if r.success)
    print(f"\n{'='*80}")
    print(f"评估完成！成功率: {success}/{total} ({success/total*100:.1f}%)")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
