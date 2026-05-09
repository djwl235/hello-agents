class MockLLM:
    def invoke(self,messages)->str:
        last_message = ""
        if messages is None:
            return "请输入问题"
        for message in reversed(messages):
            if message["role"] == "user":
                last_message = message
                break
        return f"我收到了你的问题：{last_message["content"]}"