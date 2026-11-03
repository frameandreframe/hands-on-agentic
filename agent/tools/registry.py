"""ToolRegistry：工具的注册表——查重、查找、列出、渲染提示行。

设计立场：注册表是模型与工具之间唯一的目录；未知工具在注册表层面
就被拒绝（与 ReAct 循环的 [未知工具] 边界呼应，两层防御）。
"""
from __future__ import annotations

from agent.tools.base import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """注册工具；重名立即拒绝（fail-closed：同名不同义是事故温床）。"""
        if tool.name in self._tools:
            raise ValueError(f"工具重名: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """按名取工具；未知名字抛 KeyError（调用方决定如何呈现给模型）。"""
        return self._tools[name]

    def names(self) -> list[str]:
        return sorted(self._tools)

    def prompt_lines(self) -> str:
        """渲染整个注册表为系统提示文本（空表返回「（无）」）。"""
        if not self._tools:
            return "（无）"
        return "\n".join(t.prompt_line() for t in sorted(self._tools.values(), key=lambda t: t.name))

    def to_callables(self) -> dict[str, object]:
        """导出为 {name: run} 字典——直接喂给 agent.react.run_react。"""
        return {name: t.run for name, t in self._tools.items()}
