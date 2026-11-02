"""阶段 1 测试：解析器、状态机边界、工具调用。

Sources:
- agent-expert-outline.md 思维 #6（给 agent 一个能跑的检查）
- 测试纪律：全部注入假 LLM，不触网、不耗 token；负面用例 ≥ 正面用例
"""
from __future__ import annotations

from collections.abc import Callable

from agent.builtin.calc import calc
from agent.react import parse_block, run_react


def _scripted_llm(script: list[str]) -> Callable[[list[dict[str, str]]], str]:
    """注入式假 LLM：按脚本逐轮返回预设输出（依赖注入示范）。"""
    it = iter(script)

    def _fn(messages: list[dict[str, str]]) -> str:
        return next(it)

    return _fn


# ---- parse_block：解析器 ----


def test_parse_block_full() -> None:
    t, a, f = parse_block("Thought: 需要计算\nAction: calc 1+1")
    assert t == "需要计算" and a == "calc 1+1" and f is None


def test_parse_block_finish_case_insensitive() -> None:
    t, a, f = parse_block("thought: 直接回答\nfinish: 42")
    assert (t, a, f) == ("直接回答", None, "42")


def test_parse_block_garbage_returns_none() -> None:
    assert parse_block("你好，任务完成了！") == (None, None, None)


def test_parse_block_takes_first_match() -> None:
    t, a, _f = parse_block("Thought: 一\nThought: 二\nAction: calc 1")
    assert t == "一" and a == "calc 1"


# ---- calc：工具边界 ----


def test_calc_basic_and_precedence() -> None:
    assert calc("3*(7+2)") == "27"
    assert calc("2**3") == "8"


def test_calc_friendly_failures() -> None:
    assert calc("1/0").startswith("[calc 错误]")
    assert calc("__import__('os')").startswith("[calc 错误]")
    assert calc("").startswith("[calc 错误]")


# ---- run_react：状态机三种边界 ----


def test_react_finishes_immediately() -> None:
    result = run_react("回答42", {}, llm_fn=_scripted_llm(["Thought: 无需工具\nFinish: 42"]))
    assert result["answer"] == "42"
    assert len(result["steps"]) == 1


def test_react_uses_tool_then_finishes() -> None:
    script = ["Thought: 需要计算\nAction: calc 3*(7+2)", "Thought: 得到27\nFinish: 27"]
    result = run_react("计算", {"calc": calc}, llm_fn=_scripted_llm(script))
    assert result["steps"][0]["observation"] == "27"
    assert result["answer"] == "27"


def test_react_unknown_tool_reported() -> None:
    script = ["Thought: 试试\nAction: nope x", "Thought: 停\nFinish: done"]
    result = run_react("x", {}, llm_fn=_scripted_llm(script))
    assert "未知工具" in result["steps"][0]["observation"]


def test_react_malformed_gets_format_error() -> None:
    script = ["我直接回答好啦不用什么协议", "Thought: 好了\nFinish: done"]
    result = run_react("x", {}, llm_fn=_scripted_llm(script))
    assert "格式错误" in result["steps"][0]["observation"]


def test_react_max_steps_fail_closed() -> None:
    script = ["Thought: 绕圈\nAction: calc 1"] * 20
    result = run_react("x", {"calc": calc}, llm_fn=_scripted_llm(script), max_steps=3)
    assert "最大步数" in result["answer"]
