from context import ContextBuilder
from message import Message

builder = ContextBuilder(max_history=4)

history = [
    Message(role="user", content="我昨天学了 ReActAgent"),
    Message(role="assistant", content="你理解了工具调用循环"),
]

context = builder.build(
    user_input="我现在应该复习什么？",
    history=history,
    rag_context="ReActAgent 的核心循环是 Thought、Action、Observation。",
    note_context="昨天卡点：max_iterations 的作用不够熟。"
)

print(context)