"""Tool 基类：名字 + 描述 + JSON Schema + 可调用体。

设计立场（思维 #4）：描述与 schema 是写给模型看的「文档」，
写得含糊 = 模型调用就含糊；schema 是 poka-yoke 的第一道防线。
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Tool:
    """一个可被模型调用的工具。

    name         唯一标识，模型在 Action 里引用它
    description  一句话职责 + 边界（做什么、不做什么）
    parameters   JSON Schema 的 properties 部分（手写，见 ch02 2.1）
    required     必填参数名列表
    run          执行函数：接收单字符串参数，返回字符串（永远字符串——友好失败）
    """

    name: str
    description: str
    run: Callable[[str], str]
    parameters: dict = field(default_factory=lambda: {
        "arg": {"type": "string", "description": "工具输入，单个字符串参数"}
    })
    required: tuple[str, ...] = ("arg",)

    def json_schema(self) -> dict:
        """组装完整 JSON Schema（工业协议形态，ch02 2.1 逐字段讲解）。"""
        return {
            "type": "object",
            "properties": dict(self.parameters),
            "required": list(self.required),
        }

    def prompt_line(self) -> str:
        """渲染成系统提示里的一行：模型读它决定调不调、怎么调。"""
        return f"- {self.name}: {self.description}"


def tool_from_fn(fn: Callable[[str], str], name: str, description: str) -> Tool:
    """从普通函数快速构造 Tool（默认单字符串参数 schema）。"""
    return Tool(name=name, description=description, run=fn)
