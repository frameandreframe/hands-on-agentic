"""ToolRunner：工具调用执行器——错误分类、指数退避、熔断。

Sources:
- agent-expert-outline.md 思维 #6（能跑的检查）/#9（预算与止损）
- Building effective agents（agents 从环境反馈中恢复，anthropic.com，访问 2026-11-02）
- 错误分类参考 OpenAI API 错误码设计：429/5xx=可重试，400=不可重试 [未实访]

三条铁律：
1. 可重试 ≠ 盲重试：只有 TransientToolError 才重试，FatalToolError 一次都不值得。
2. 退避必须有上限：指数退避 + max_attempts，两者缺一就是死循环反例。
3. 熔断失败关闭：连续失败达到阈值就拒绝调用（宁可快速失败，不可雪崩拖死循环）。
"""
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field


class TransientToolError(Exception):
    """可重试错误：网络抖动、超时、限流。"""


class FatalToolError(Exception):
    """不可重试错误：参数非法、权限不足——重试只是浪费。"""


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 0.2          # 秒；生产 0.2–1.0，测试调小
    cooldown: float = 1.0            # 熔断后的冷却秒数
    threshold: int = 3               # 连续失败多少次触发熔断


@dataclass
class ToolRunner:
    """包装任意工具函数：run(name, fn, arg) 永远返回字符串（友好失败进 Observation）。"""

    policy: RetryPolicy = field(default_factory=RetryPolicy)
    _consecutive_fail: dict[str, int] = field(default_factory=dict)
    _open_until: dict[str, float] = field(default_factory=dict)

    # -- 熔断状态 --
    def is_open(self, name: str) -> bool:
        until = self._open_until.get(name, 0.0)
        return time.monotonic() < until

    def _record_failure(self, name: str) -> None:
        n = self._consecutive_fail.get(name, 0) + 1
        self._consecutive_fail[name] = n
        if n >= self.policy.threshold:
            self._open_until[name] = time.monotonic() + self.policy.cooldown

    def _record_success(self, name: str) -> None:
        self._consecutive_fail[name] = 0
        self._open_until.pop(name, None)

    # -- 主入口 --
    def run(self, name: str, fn: Callable[[str], str], arg: str) -> str:
        if self.is_open(name):
            return f"[熔断] {name} 连续失败已达 {self.policy.threshold} 次，冷却中——快速失败优于雪崩"

        last = "未知失败"
        for attempt in range(1, self.policy.max_attempts + 1):
            try:
                result = fn(arg)
            except TransientToolError as exc:
                last = f"[失败] {type(exc).__name__}: {exc}"
                if attempt < self.policy.max_attempts:
                    time.sleep(self.policy.base_delay * (2 ** (attempt - 1)))  # 指数退避：0.2→0.4→0.8
                continue
            except FatalToolError as exc:
                self._record_failure(name)
                return f"[错误] {name} 不可重试: {exc}"   # 重试无意义，立即失败
            except Exception as exc:  # noqa: BLE001 —— 边界层兜底是本类的功能：未分类异常按不可重试处理（保守），类型名进结果供调试
                self._record_failure(name)
                return f"[错误] {name} {type(exc).__name__}: {exc}"
            self._record_success(name)
            return result

        self._record_failure(name)
        return f"{last}（已重试 {self.policy.max_attempts} 次）"

    def wrap(self, name: str, fn: Callable[[str], str]) -> Callable[[str], str]:
        """把保护逻辑包进函数本体——可直接塞进 run_react 的 tools 字典。"""
        return lambda arg: self.run(name, fn, arg)
