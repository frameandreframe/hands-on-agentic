"""ch01 演示应用：FastAPI 暴露 ReAct 循环（/health + /chat）。

Sources:
- agent-camp-outline.md §5 阶段 0/1 FastAPI 前置配置表
- agent-expert-outline.md 思维 #12（演示物必须可见可访问）

说明：放置于 demo/ 包而非 ch01-react/demo/——Python 导入名不允许连字符，
课程材料留在 ch01-react/，可运行代码集中于 demo/（CHANGELOG 已记录此偏离）。
"""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agent.builtin.calc import calc
from agent.react import run_react
from llm_utils import chat

app = FastAPI(title="hands-on-agentic", version="0.5.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "0.5.0"}


class ChatIn(BaseModel):
    message: str
    max_steps: int = 4


@app.post("/chat")
def chat_endpoint(body: ChatIn) -> dict:
    """ReAct 循环服务化：模型守协议调工具，返回答案与全部步骤（透明优先）。"""
    result = run_react(body.message, {"calc": calc}, llm_fn=chat, max_steps=body.max_steps)
    return {"answer": result["answer"], "steps": result["steps"]}
