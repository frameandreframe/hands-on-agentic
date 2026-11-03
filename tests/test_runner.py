"""ToolRunner 测试：重试、退避、分类、熔断——注入 flaky 工具，不触网。"""
from __future__ import annotations

import pytest

from agent.tools.runner import (
    FatalToolError,
    RetryPolicy,
    ToolRunner,
    TransientToolError,
)


def _flaky(fail_times: int, exc: type[Exception] = TransientToolError):
    """前 fail_times 次抛异常，之后成功。附带调用计数。"""
    state = {"calls": 0}

    def fn(_: str) -> str:
        state["calls"] += 1
        if state["calls"] <= fail_times:
            raise exc("模拟故障")
        return "ok"

    fn.calls = state  # type: ignore[attr-defined]
    return fn


@pytest.fixture()
def fast_policy() -> RetryPolicy:
    return RetryPolicy(max_attempts=3, base_delay=0.01, cooldown=0.05, threshold=3)


def test_retry_eventually_succeeds(fast_policy: RetryPolicy) -> None:
    r = ToolRunner(policy=fast_policy)
    fn = _flaky(2)
    assert r.run("t", fn, "x") == "ok"
    assert fn.calls["calls"] == 3   # 前两次失败 + 第三次成功


def test_fatal_error_never_retried(fast_policy: RetryPolicy) -> None:
    r = ToolRunner(policy=fast_policy)
    fn = _flaky(99, exc=FatalToolError)
    out = r.run("t", fn, "x")
    assert "不可重试" in out
    assert fn.calls["calls"] == 1   # 一次都不该重试


def test_retries_exhausted_reports(fast_policy: RetryPolicy) -> None:
    r = ToolRunner(policy=fast_policy)
    fn = _flaky(99)
    out = r.run("t", fn, "x")
    assert "[失败]" in out and "已重试 3 次" in out
    assert fn.calls["calls"] == 3


def test_unclassified_exception_treated_fatal(fast_policy: RetryPolicy) -> None:
    """未分类异常保守处理：不重试，类型名保留进结果供调试。"""
    r = ToolRunner(policy=fast_policy)
    fn = _flaky(99, exc=ZeroDivisionError)
    out = r.run("t", fn, "x")
    assert "ZeroDivisionError" in out
    assert fn.calls["calls"] == 1


def test_circuit_opens_after_threshold(fast_policy: RetryPolicy) -> None:
    r = ToolRunner(policy=fast_policy)
    fn = _flaky(99)
    for _ in range(3):                       # 连续失败 3 次（每次内部重试 3 回合）
        r.run("t", fn, "x")
    calls_before = fn.calls["calls"]
    out = r.run("t", fn, "x")                # 第 4 次外部调用：应被熔断拦截
    assert "[熔断]" in out
    assert fn.calls["calls"] == calls_before  # 没有真的调用工具——快速失败


def test_circuit_half_open_recovers(fast_policy: RetryPolicy) -> None:
    import time as _time

    r = ToolRunner(policy=fast_policy)
    bad = _flaky(99)
    for _ in range(3):
        r.run("t", bad, "x")
    assert "[熔断]" in r.run("t", bad, "x")
    _time.sleep(fast_policy.cooldown + 0.02)  # 冷却结束 → 半开，允许一次试探
    good = _flaky(0)
    assert r.run("t", good, "x") == "ok"      # 试探成功 → 熔断关闭
    assert r.run("t", good, "x") == "ok"      # 正常路径恢复


def test_wrap_integrates_with_react(fast_policy: RetryPolicy) -> None:
    """runner.wrap 产物可直接进 run_react 的 tools 字典（装配闭环）。"""
    from agent.react import run_react

    r = ToolRunner(policy=fast_policy)
    script = iter(["Thought: 用\nAction: flaky hi", "Thought: 好\nFinish: done"])
    result = run_react(
        "x", {"flaky": r.wrap("flaky", _flaky(1))}, llm_fn=lambda m: next(script),
        max_steps=3,
    )
    assert result["answer"] == "done" or "Observation" in str(result["steps"])
