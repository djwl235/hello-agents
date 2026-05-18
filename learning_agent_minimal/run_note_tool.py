from tools.note_tool import NoteTool
note = NoteTool(note_path="learning_agent_minimal/notes/learning_log.md")
print(note.run("add 今天学习了 NoteTool，理解了 add/search/list 三个动作"))
print("-" * 40)
print(note.run("search NoteTool"))
print("-" * 40)
print(note.run("list"))