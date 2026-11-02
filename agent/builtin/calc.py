"""玩具计算器工具——课程第一个 ACI（agent-computer interface）。

Sources:
- agent-expert-outline.md 思维 #4（工具描述即文档、poka-yoke 防呆）
- Building effective agents 附录 2：工具接口的投入不少于提示词
"""
from __future__ import annotations

import ast
import operator

_BIN = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def _eval(node: ast.expr) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        return _BIN[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    raise ValueError(f"不允许的表达式节点: {type(node).__name__}")


def calc(expr: str) -> str:
    """安全求值算术表达式，如 "3*(7+2)"。

    只允许数字、+ - * / % // ** 与括号；任何其他输入返回可读错误
    （工具要友好失败——错误信息会进入模型的 Observation）。
    """
    try:
        return str(_eval(ast.parse(expr, mode="eval").body))
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as exc:
        return f"[calc 错误] {type(exc).__name__}: {exc}"
