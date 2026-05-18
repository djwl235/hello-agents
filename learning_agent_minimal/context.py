class ContextBuilder:
    def __init__(self,max_history = 4):
        self.max_history = max_history
    def format_history(self,history):
        history = history or []
        history_result = ""
        history_content = ""
        for msg in history[-self.max_history:]:
            history_content = f"{msg.role}:{msg.content}\n"
            history_result+=history_content
            history_content = ""
        return history_result
    def build(self,user_input,history = None,rag_context = None , note_context = None):
        history_result = self.format_history(history)
        rag_result = rag_context or "无相关知识库内容"
        note_result = note_context or "无相关学习笔记"
        result = f"##最近对话\n{history_result}\n##相关知识库\n{rag_result}\n##相关学习笔记\n{note_result}\n##当前问题\n{user_input}"
        return result