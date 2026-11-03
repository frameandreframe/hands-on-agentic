"""ch01 demo 应用测试：TestClient 注入假 LLM，不触网。"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from demo import main as demo_main


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """注入剧本化假 LLM：一轮工具调用 + 一轮收尾（与 test_react 同款招式）。"""
    it = iter(["Thought: 需要计算\nAction: calc 3*(7+2)", "Thought: 得到27\nFinish: 27"])
    monkeypatch.setattr(demo_main, "chat", lambda messages: next(it))
    return TestClient(demo_main.app)


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "version": "0.3.0"}


def test_chat_returns_answer_and_steps(client: TestClient) -> None:
    r = client.post("/chat", json={"message": "计算 3*(7+2)"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "27"
    assert body["steps"][0]["observation"] == "27"
