"""终端小机器人：while 循环 + 历史维护。

运行：uv run python chat.py
退出：输入 exit / quit / 退出
"""
from llm_utils import ARK_MODEL, chat

SYSTEM_PROMPT = "你是课程陪练小机器人。回答简洁、准确，一律使用中文。"
HISTORY_LIMIT = 20  # 历史上限：超出后丢弃最旧对话，防止 token 无限增长（阶段 4 正式解决记忆问题）


def main() -> None:
    print(f"小机器人已上线（模型：{ARK_MODEL}）。输入 exit / quit / 退出 结束。")
    history: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user:
            continue
        if user.lower() in {"exit", "quit"} or user == "退出":
            print("再见！")
            break

        history.append({"role": "user", "content": user})
        try:
            reply = chat(history)
        except Exception as exc:  # 保持循环存活；阶段 2 会升级为带退避的重试
            print(f"[调用失败] {type(exc).__name__}（检查密钥/网络后重试）")
            history.pop()
            continue

        print(f"机器人> {reply}\n")
        history.append({"role": "assistant", "content": reply})
        history = [history[0]] + history[-HISTORY_LIMIT:]


if __name__ == "__main__":
    main()
