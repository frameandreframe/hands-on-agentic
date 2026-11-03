"""首批回归用例：三个真实历史事件的永久锁定。

Sources:
- agent-expert-outline.md 思维 #6（能跑的检查）与 RSI 事故回归化流程
- 事件记录同步于 CHANGELOG v0.3.0 与 contributing-path.md 卡点预告
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from agent.react import run_react
from llm_utils import _api_key

ROOT = Path(__file__).resolve().parents[2]


def _scripted(*lines: str):
    it = iter(lines)
    return lambda messages: next(it)


def test_regression_2026_11_02_missing_key_error_is_actionable(monkeypatch: pytest.MonkeyPatch) -> None:
    """背景：2026-11-02 首接自建网关，401 报错不含任何指路信息，排查 15 分钟。

    锁定：密钥缺失时必须抛出「可行动」的错误——点名变量、给出两种配置路径。
    （llm_utils._api_key 是密钥 UX 的落点，测试私有缝是本条的意义所在）
    """
    monkeypatch.delenv("ARK_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as ei:
        _api_key()
    msg = str(ei.value)
    assert "ARK_API_KEY" in msg
    assert "export" in msg          # 路径①：环境变量
    assert ".env" in msg            # 路径②：本地文件


def test_regression_2026_11_03_react_survives_pure_garbage() -> None:
    """背景：2026-11-03 E2E 前发现真实模型可能输出非协议闲聊。

    锁定：垃圾输出 → [格式错误] Observation → 循环继续 → 最终正常收尾。
    整条链路任何一环崩溃都算回归。
    """
    script = ("大家好呀，任务完成啦！", "真的，相信我", "Thought: 好\nFinish: ok")
    result = run_react("x", {}, llm_fn=_scripted(*script), max_steps=5)
    assert "格式错误" in result["steps"][0]["observation"]
    assert "格式错误" in result["steps"][1]["observation"]
    assert result["answer"] == "ok"


def test_regression_2026_11_03_notebook_cells_pass_ruff() -> None:
    """背景：2026-11-03 两本 notebook 的代码单元格因导入格式被 ruff 拦截（I001）。

    锁定：notebook 代码与 .py 同受静态检查约束（ruff 默认支持 ipynb）。
    与门禁 A4 双层锁——事故门禁化的完整示例：事故→测试→永久回归。
    """
    r = subprocess.run(
        ["uvx", "ruff", "check", "."],
        cwd=ROOT, capture_output=True, text=True, timeout=180, check=False,
    )
    assert r.returncode == 0, r.stdout
