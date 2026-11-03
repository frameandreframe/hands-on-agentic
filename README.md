# hands-on-agentic

《动手从 0 构建 Agent，实现 Agentic》课程点火阶段（v0.1.0）。不用框架，从一次 LLM 调用开始。

## 快速开始

```bash
uv sync                          # 安装依赖（自动创建 .venv）
cp .env.example .env             # 填入你的 ARK_API_KEY（已被 .gitignore 保护）
uv run python chat.py            # 终端小机器人（exit/quit/退出 结束）
uv run jupyter lab               # 打开 00-first-call.ipynb 跟学
```

若环境变量中已有 `ARK_API_KEY`，无需 `.env`。

## 密钥安全三铁律

1. 密钥只从环境变量或 `.env` 读取，绝不写进代码与文档
2. 绝不打印明文，只允许 `masked_key()` 掩码展示
3. `.env` 永远不进 git，提交前自查 `git status`

## 课程阶段（⭐ = 核心章：构成 agent 内核最小闭环）

| 周 | 章 | 版本 tag | 状态 |
|---|---|---|---|
| 1 | 阶段 0 点火 | v0.1.0 | ✅ |
| 2 | ⭐ ch01 ReAct | v0.2.0 | ✅ |
| 3–4 | ⭐ ch02 tool use | v0.3.0（计划） | ⏳ |
| 5–6 | ch03 plan | v0.4.0 | ⏳ |
| 7–8 | ch04 memory | v0.5.0 | ⏳ |
| 9–11 | ch05 协议 MCP/A2A/ACP | v0.6.0 | ⏳ |
| 12 | ch06 skill 与专家 | v0.7.0 | ⏳ |
| 13–14 | ⭐ ch07 harness | v0.8.0 | ⏳ |
| 15–16 | ⭐ ch08 RSI | v1.0.0 | ⏳ |

每章交付后产出验证手记 `ch<N>/walkthrough.md`（验证思路 + 实测记录，供参考）。

## 课程大纲

见上级目录 `agent-camp-outline.md`（9 阶段路线图 / 三 subagent 规范 / 开源发布规范）。
