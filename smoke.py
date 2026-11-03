"""独立冒烟脚本：三道检查之②（AGENTS.md §1）。

替代旧的管道写法，退出码可直接被 harness/CI 消费：
  uv run python smoke.py    # 退出码 0=通过，1=失败
真调用一次 LLM（成本≈一次短回复），验证「密钥→网关→模型」全链路。
"""
from __future__ import annotations

import sys

from openai import APIError

from llm_utils import chat


def main() -> int:
    try:
        reply = chat([{"role": "user", "content": "只回复两个字母: ok"}])
    except (APIError, RuntimeError) as exc:  # 网络/密钥类失败；其余异常应响亮崩溃
        print(f"SMOKE-FAIL {type(exc).__name__}")
        return 1
    ok = bool(reply.strip())
    print(f"SMOKE-{'PASS' if ok else 'FAIL'} reply={reply.strip()[:50]!r}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
