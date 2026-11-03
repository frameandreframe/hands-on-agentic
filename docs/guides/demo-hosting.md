# 演示托管指南：让 demo 出现在你的 GitHub 主页

> **Sources**: agent-expert-outline.md 思维 #12（演示物必须可见）；各平台条款时效性强，**标注[未实访]的细节以官网当日为准**。本文件验证状态：✅ 本地 uvicorn 路径已实测（2026-11-03）；远程托管路径为操作指南。

## 1. 免费托管怎么选（对比表）

| 平台 | 适合 | 费用 | 限制/陷阱 | 本课用途 |
|---|---|---|---|---|
| **GitHub Pages** | 静态页：讲义、报告、eval 报告 | 免费 | 只能静态；无后端 | 每章 walkthrough/journal 的公开版 |
| **HuggingFace Spaces** | Docker 跑 FastAPI 的动态 demo | 免费（CPU 基本型） | 闲置 48h 转休眠，访问自动唤醒 | **课程 demo 主推**（ch01 /chat 即可上线）|
| Render | Docker/FastAPI 免费 Web Service | 免费层 | 闲置 15 分钟休眠，冷启动约 50 秒 `[未实访]` | 备选 |
| Fly.io | 容器 | 新账户按量付费，无纯粹免费层 `[未实访]` | 需绑卡 | 不推荐新人 |
| Vercel | 前端/serverless | 免费 Hobby | Python 后端需改造为 serverless 形态 | 不推荐（形态不符） |

**结论：动态 demo 用 HF Spaces，静态成果用 GitHub Pages，都免费。**

## 2. 路径 A（主推）：ch01 demo 上 HuggingFace Spaces

本仓 demo 应用已就绪（`demo/main.py`：`/health` + `/chat`，✅ 已于 2026-11-03 本地实测）：

```bash
# 本地预演（必须先过）
uv run uvicorn demo.main:app --port 8000
curl -s localhost:8000/health          # {"status":"ok",...}
curl -s -X POST localhost:8000/chat -H 'Content-Type: application/json' \
  -d '{"message":"用 calc 计算 3*(7+2) 然后 Finish 数字"}'
```

上线步骤（Spaces 用 Docker 模式）：

```bash
# ① 在 hf.co 注册并新建 Space：SDK 选 Docker（Public）
# ② Space 仓库里放三个文件：
#    Dockerfile（预览版如下，ch05 容器化讲次正式落地 [未实测]）
#    demo/main.py + agent/ + llm_utils.py（不含 .env！）
# ③ 密钥进 Space 的 Settings → Variables and secrets：ARK_API_KEY / ARK_BASE_URL / ARK_MODEL
#    ——密钥三铁律的平台版：secrets 永远进平台密钥管理，不进任何文件
```

Dockerfile 预览（ch05 讲次逐行精讲）：

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev
COPY agent/ demo/ llm_utils.py chat.py ./
EXPOSE 7860
CMD ["uv", "run", "uvicorn", "demo.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

## 3. 路径 B：把 demo 挂上你的 GitHub 主页

GitHub 个人主页 = 名为 `<用户名>/<用户名>` 的特殊仓库的 README：

```bash
gh repo create <你的用户名>/<你的用户名> --public --clone
cd <你的用户名>
```

README 里加一段（练手：这就是你的第一个个人门面 PR）：

```markdown
## 🤖 正在建的东西
- [hands-on-agentic](https://github.com/frameandreframe/hands-on-agentic)：
  从零手写 agent，当前 v0.3.0
  - 在线 demo：https://huggingface.co/spaces/<你的用户名>/agentic-chat
  - [![gate](https://github.com/frameandreframe/hands-on-agentic/actions/workflows/gate.yml/badge.svg)](…/actions)
```

badge（CI 状态）+ demo 链接 + 版本号三件套——主页即作品集。

## 4. 成本参考（便宜路线）

- 全免费：HF Spaces + GitHub Pages（本课默认路径）
- 想要常驻不休眠：HF Spaces 升级 ~$9/月 或 Render 付费层 ~$7/月 `[未实访，以官网当日价格为准]`
- LLM 调用成本：课程 demo 用 glm-5.3-flash（推理模型、单次极低），公网 demo 记得在应用层限 max_steps（本仓默认 4）

## 5. 卡点预告

1. Spaces 构建失败第一原因：uv.lock 与 pyproject 不同步——先本地 `uv sync` 再提交。
2. Space 里报 401：九成是 secrets 名字写错（区分 `ARK_API_KEY` 大小写）。
3. 冷启动首次请求超时属正常（容器唤醒），报告里注明即可，不要误判为 bug。
