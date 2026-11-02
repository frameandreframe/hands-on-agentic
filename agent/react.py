"""ReAct 循环（纯文本协议版）—— 阶段 1 核心。

Sources:
- ReAct 论文: arxiv.org/abs/2210.03629（Thought/Action/Observation 循环）
- agent-expert-outline.md 思维 #1（agent=循环+工具）、#4（ACI）、#6（能跑的检查）
- 可测试性设计：llm_fn 依赖注入，测试全部注入假 LLM 不触网（tests/test_react.py）
"""
from __future__ import annotations

from collections.abc import Callable

from llm_utils import chat

MAX_STEPS = 8  # 预算思想的第一课：没有止损的循环是事故（思维 #9 前奏）

_SYSTEM = """你是 ReAct agent，每轮严格输出以下两行之一：
Thought: 你的推理
Action: 工具名 参数
或：
Thought: 你的推理
Finish: 最终答案
不要输出任何其他内容。可用工具：
{tools}"""


def parse_block(text: str) -> tuple[str | None, str | None, str | None]:
    """从模型输出解析三行协议，返回 (thought, action, finish)。

    解析器纪律：只认行前缀、每类只取第一个匹配、大小写不敏感——
    对不守协议的输出返回 None（由状态机处理，见 run_react）。
    """
    thought = action = finish = None
    for line in text.splitlines():
        s = line.strip()
        low = s.lower()
        if low.startswith("thought:") and thought is None:
            thought = s[len("thought:"):].strip()
        elif low.startswith("action:") and action is None:
            action = s[len("action:"):].strip()
        elif low.startswith("finish:") and finish is None:
            finish = s[len("finish:"):].strip()
    return thought, action, finish


def run_react(
    goal: str,
    tools: dict[str, Callable[[str], str]],
    llm_fn: Callable[[list[dict[str, str]]], str] = chat,
    max_steps: int = MAX_STEPS,
) -> dict:
    """执行 ReAct 循环，返回 {"answer": str, "steps": [...]}。

    状态机三种边界（失败关闭思想）：
    - 输出不守协议 → Observation 回 [格式错误]，让模型自我修正
    - 调用未知工具 → Observation 回 [未知工具]，不猜测、不崩溃
    - 步数耗尽仍无 Finish → 返回 [达到最大步数]，绝不假装完成
    """
    tool_lines = "\n".join(f"- {name}" for name in tools)
    messages: list[dict[str, str]] = [
        {"role": "system", "content": _SYSTEM.format(tools=tool_lines or "（无）")},
        {"role": "user", "content": f"目标：{goal}"},
    ]
    steps: list[dict[str, str | None]] = []
    for _ in range(max_steps):
        out = llm_fn(messages)
        thought, action, finish = parse_block(out)
        if finish is not None:
            steps.append({"thought": thought, "action": None, "observation": None})
            return {"answer": finish, "steps": steps}
        if action is None:
            observation = "[格式错误] 必须输出 Thought:/Action:/Finish:"
        else:
            name, _, arg = action.partition(" ")
            fn = tools.get(name)
            observation = fn(arg.strip()) if fn else f"[未知工具] {name}"
        steps.append({"thought": thought, "action": action, "observation": observation})
        messages.append({"role": "assistant", "content": out})
        messages.append({"role": "user", "content": f"Observation: {observation}"})
    return {"answer": "[达到最大步数，未完成]", "steps": steps}
