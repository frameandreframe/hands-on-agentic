"""agent.tools 测试：注册表纪律 + schema 组装——全部离线。"""
from __future__ import annotations

import pytest

from agent.builtin.calc import calc
from agent.tools.base import Tool, tool_from_fn
from agent.tools.registry import ToolRegistry


@pytest.fixture()
def reg() -> ToolRegistry:
    r = ToolRegistry()
    r.register(tool_from_fn(calc, "calc", "安全求值算术表达式，如 3*(7+2)。只支持四则与括号。"))
    return r


def test_register_and_get(reg: ToolRegistry) -> None:
    assert reg.names() == ["calc"]
    assert reg.get("calc").run("1+1") == "2"


def test_duplicate_name_rejected(reg: ToolRegistry) -> None:
    with pytest.raises(ValueError, match="重名"):
        reg.register(tool_from_fn(calc, "calc", "重复注册"))


def test_unknown_name_raises(reg: ToolRegistry) -> None:
    with pytest.raises(KeyError):
        reg.get("nope")


def test_json_schema_shape(reg: ToolRegistry) -> None:
    schema = reg.get("calc").json_schema()
    # required 必须在顶层、properties 之下才是字段定义——2.1 的核心考点
    assert schema["type"] == "object"
    assert "expr" not in schema  # 默认参数名是 arg，说明 schema 与实现要人工对齐
    assert schema["required"] == ["arg"]


def test_calc_tool_schema_mismatch_is_visible() -> None:
    """诚实的坑：calc 实际解析整串表达式，默认 schema 的 arg 语义没错，但字段名要一致。

    教学点：schema 写错字段名，模型就会按错误字段传参——工具描述与
    实现的对齐是 ACI 工程的核心纪律（思维 #4）。
    """
    t = Tool(
        name="calc",
        description="求值",
        run=calc,
        parameters={"expr": {"type": "string", "description": "算术表达式"}},
        required=("expr",),
    )
    assert t.json_schema()["required"] == ["expr"]


def test_prompt_lines_and_empty_registry() -> None:
    empty = ToolRegistry()
    assert empty.prompt_lines() == "（无）"
    reg = ToolRegistry()
    reg.register(tool_from_fn(calc, "calc", "求值算术表达式"))
    assert reg.prompt_lines() == "- calc: 求值算术表达式"


def test_to_callables_feeds_react(reg: ToolRegistry) -> None:
    """注册表导出的可调用字典能直接接进 ReAct 循环（装配闭环）。"""
    from agent.react import run_react

    script = ["Thought: 算\nAction: calc 2**10", "Thought: 1024\nFinish: 1024"]
    it = iter(script)
    result = run_react("算 2**10", reg.to_callables(), llm_fn=lambda m: next(it))
    assert result["answer"] == "1024"
