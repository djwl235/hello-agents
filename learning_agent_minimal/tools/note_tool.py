from tools.base import BaseTool
from pathlib import Path
import re
from datetime import datetime


class NoteTool(BaseTool):
    name = "note"
    description = "记录和搜索学习笔记。支持 add、search、list"

    def __init__(self,note_path="notes/learning_log.md"):
        self.note_path = Path(note_path)
        self.note_path.parent.mkdir(parents=True, exist_ok=True)
        self.note_path.touch(exist_ok=True)

    def run(self,tool_input):
        tool_input = (tool_input or "").strip()

        if not tool_input:
            return "无笔记调用指令"

        if tool_input.lower().startswith("add"):
            content = self._extract_action_content(tool_input, "add")
            if not content:
                return "添加笔记失败：内容不能为空"
            self.add_note(content=content)
            return "日志记录完毕"

        elif tool_input.lower().startswith("search"):
            content = self._extract_action_content(tool_input, "search")
            if not content:
                return "搜索笔记失败：查询词不能为空"
            results = self.search_notes(content)
            if not results:
                return "没有找到相关笔记"
            return results

        elif tool_input.lower().startswith("list"):
            result = self.list_notes()
            return result

        else:
            return "无笔记调用指令"

    def _extract_action_content(self, tool_input, action):
        pattern = rf"^{action}\s*[:：]?\s*(.+)$"
        match = re.search(pattern, tool_input, re.IGNORECASE | re.DOTALL)
        if not match:
            return ""
        return match.group(1).strip()

    def add_note(self,content):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        written_content = f"\n\n## {timestamp}\n\n{content}"
        with open(self.note_path,"a",encoding="UTF-8") as f:
            f.write(written_content)
        return
    def search_notes(self,query):
        results = []
        text = self.note_path.read_text(encoding="UTF-8")
        for paragraph in text.split("##"):
            if query in paragraph:
                results.append(paragraph)
        return "\n".join(results)

    def list_notes(self):
        text = self.note_path.read_text(encoding="UTF-8")
        if not text.strip():
            return "暂无学习笔记"
        return text
