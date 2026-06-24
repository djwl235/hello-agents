from pathlib import Path
from .base import BaseTool
import re
from datetime import datetime
import json
import uuid

class StructuredNoteTool(BaseTool):
    name = "structured_note"
    description = "结构化学习笔记工具，支持 add/search/list"
    def __init__(self, note_path="learning_agent_minimal/notes/structured_notes.jsonl"):
        self.note_path = Path(note_path)
        self.note_path.parent.mkdir(parents=True,exist_ok=True)
    def run(self, tool_input: str):
        tool_input = (tool_input or "").strip()
        if not tool_input:
            return "无笔记调用指令"
        if tool_input.lower().startswith("add"):
            content = self._extract_action_content(tool_input,"add")
            if not content:
                return "添加笔记失败：内容不能为空"
            self.add_note(content=content)
            return "日志记录完毕"
        elif tool_input.lower().startswith("search"):
            query = self._extract_action_content(tool_input,"search")
            if not query:
                return "查询内容不能为空"
            results = self.search_notes(query=query)
            if not results:
                return "没有找到相关笔记"
            return results
        elif tool_input.lower().startswith("list"):
            result = self.list_notes()
            return result
        else:
            return "无笔记调用指令"

    def add_note(self, content: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tags = self._extract_tags(content=content)
        note = {
            "id":str(uuid.uuid4()),
            "created_at":timestamp,
            "type":"learning",
            "tags":tags,
            "content":content,
            "summary":content[:50]
        }
        with self.note_path.open("a",encoding="utf-8") as f:
            f.write(json.dumps(note,ensure_ascii=False)+"\n")
        return
    
    def search_notes(self, query: str):
        results = []
        notes = self._load_notes()
        for note in notes:
            haystack = " ".join(
                [
                note.get("content", ""),
                note.get("summary", ""),
                " ".join(note.get("tags", [])),
                note.get("type", ""),
                ]
            )
            if query in haystack:
                results.append(note)
        if not results:
            return ""
        output = []
        for note in results:
            output.append(
                f"时间：{note['created_at']}\n"
                f"类型：{note['type']}\n"
                f"标签：{', '.join(note['tags'])}\n"
                f"摘要：{note['summary']}\n"
                f"内容：{note['content']}"
            )
        return "\n\n".join(output)
    
    def list_notes(self):
        text = self.note_path.read_text(encoding="UTF-8")
        if not text.strip():
            return "暂无学习笔记"
        return text
    
    def _load_notes(self):
        notes = []
        if self.note_path.exists():
            with open(self.note_path,"r",encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        notes.append(json.loads(line))
        return notes
    def _extract_action_content(self, tool_input, action):
        pattern = rf"^{action}\s*[:：]?\s*(.+)$"
        match = re.search(pattern, tool_input, re.IGNORECASE | re.DOTALL)
        if not match:
            return ""
        return match.group(1).strip()
    def _extract_tags(self,content:str):
        tags = []
        keywords = ["RAG", "Embedding", "min_score", "MCP", "Agent", "ToolRegistry", "NoteTool"]
        for keyward in keywords:
            if keyward in content:
                tags.append(keyward)
        return tags