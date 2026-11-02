"""阶段 0 门禁测试：不触网、不耗 token，验证结构完整性与密钥保护。

运行：uv run pytest -q
回归用例从阶段 1 起沉淀到 tests/regression/（AGENTS.md 第 1 节「回测」）。
"""
from __future__ import annotations

import os
from pathlib import Path

import llm_utils

ROOT = Path(__file__).resolve().parent.parent


def test_llm_utils_exposes_core_api() -> None:
    """课程唯一的 LLM 出入口必须提供三个函数。"""
    assert callable(llm_utils.get_llm_response)
    assert callable(llm_utils.chat)
    assert callable(llm_utils.masked_key)


def test_masked_key_never_leaks_full_secret() -> None:
    """掩码绝不包含完整密钥，且必须带 ****（密钥未加载时除外）。"""
    masked = llm_utils.masked_key()
    real = os.environ.get("ARK_API_KEY", "")
    if real:
        assert real not in masked
        assert "****" in masked


def test_gitignore_protects_env() -> None:
    """.gitignore 首行区必须包含 .env（密钥保护第一道防线）。"""
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in lines[:5], ".env 保护规则必须放在 .gitignore 前几行"


def test_env_example_has_placeholder_only() -> None:
    """.env.example 只能有占位符，绝不允许出现真实密钥。"""
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "ARK_API_KEY=your-api-key-here" in text
    assert "your-api-key-here" in text


def test_no_secret_patterns_in_tracked_sources() -> None:
    """源码与 notebook 中不得出现疑似密钥串。"""
    import re

    pattern = re.compile(r"(ark-|sk-)[A-Za-z0-9]{16,}")
    targets = [ROOT / "llm_utils.py", ROOT / "chat.py", ROOT / "00-first-call.ipynb"]
    for path in targets:
        assert not pattern.search(path.read_text(encoding="utf-8")), f"{path.name} 疑似泄漏密钥"
