"""LLM 工具函数（吴恩达课程风格）：全课程唯一需要复用的底层调用入口。

密钥安全三铁律（违反任何一条 = 阶段不通过）：
1. 密钥只从环境变量或 .env 读取，绝不写进代码、notebook、文档。
2. 绝不打印密钥明文，只允许 masked_key() 显示掩码。
3. .env 永远不进 git（.gitignore 首行），提交前必须自查。

读取优先级：环境变量 ARK_API_KEY → 本目录 .env → 报错并指路。
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 读取同目录 .env；不覆盖已存在的环境变量

ARK_BASE_URL = os.environ.get(
    "ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"
)
ARK_MODEL = os.environ.get("ARK_MODEL", "glm-5.3-flash")

_client: OpenAI | None = None


def _api_key() -> str:
    key = os.environ.get("ARK_API_KEY")
    if not key:
        raise RuntimeError(
            "未找到 ARK_API_KEY。两种配置方式任选：\n"
            "  1) 环境变量：export ARK_API_KEY=你的密钥\n"
            "  2) 本目录创建 .env（已被 .gitignore 保护）：\n"
            "     cp .env.example .env   然后填入密钥"
        )
    return key


def masked_key() -> str:
    """返回掩码形式用于自检展示，例如 ark-****9a2c。绝不输出明文。"""
    key = os.environ.get("ARK_API_KEY", "")
    if not key:
        return "（未加载）"
    if len(key) <= 8:
        return "（长度异常，请检查密钥是否完整）"
    return f"{key[:4]}****{key[-4:]}"


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=_api_key(), base_url=ARK_BASE_URL)
    return _client


def get_llm_response(
    prompt: str,
    system: str | None = None,
    model: str | None = None,
    temperature: float = 0.7,
) -> str:
    """单轮调用（吴恩达式签名）：传入字符串，返回字符串。

    prompt       用户消息
    system       可选的系统提示（设定角色与边界）
    model        缺省读取 .env 中的 ARK_MODEL
    temperature  0=稳定可复现，1=更有创造性；课程作业会反复用到它
    """
    messages: list[dict[str, str]] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = _get_client().chat.completions.create(
        model=model or ARK_MODEL,
        messages=messages,  # type: ignore[arg-type]
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def chat(
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.7,
) -> str:
    """多轮调用：传入完整 messages 列表（小机器人用它维护对话历史）。"""
    response = _get_client().chat.completions.create(
        model=model or ARK_MODEL,
        messages=messages,  # type: ignore[arg-type]
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
