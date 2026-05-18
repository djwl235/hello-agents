from learning_assistant import LearningAssistant
from llm import MockLLM
def main():
    assistant = LearningAssistant(llm=MockLLM())

    print("学习助手已启动，输入 exit 或 quit 退出。")
    while True:
        user_input = input("\n你：").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("已退出。")
            break
        if not user_input:
            continue
        response = assistant.answer(user_input=user_input)
        print(f"\nassistant：{response}")
if __name__ == "__main__":
    main()
    