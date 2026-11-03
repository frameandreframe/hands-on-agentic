# Changelog

本文件条目遵守 Keep a Changelog 风格；每条附 Sources（设计源泉，可回源）。

## 周 tag 对应表

| tag | 周 | 内容一句话 |
|---|---|---|
| v0.1.0 | 阶段 0 | 点火：LLM 工具函数 + 小机器人 + 密钥保护 |
| v0.2.0 | W1 | ReAct 循环 + 门禁机器人 + ch01 课程包 |
| v0.3.0 | W2 | regression 首批 + demo 服务化 + 托管指导 + 仪式首运转 |
| v0.4.0 | W3 | tools 内核 + 打包构建课 + ch02 启动 + smoke.py |
| v0.5.0 | W4 | ch02 收官：runner 重试/熔断 + 验证手记 |
| v0.6.0 | W5（计划） | ch03 plan：规划器 + todo 状态机 |

## [v0.5.0] - 2026-11-03

### Added
- `agent/tools/runner.py`：ToolRunner（Transient/Fatal 错误分类、指数退避、连续失败熔断、半开恢复、wrap 装配）
- `tests/test_runner.py`（7 条：重试计数/致命不重试/耗尽上报/未分类保守/熔断拦截执行/半开恢复/ReAct 集成）
- `ch02-tools/2.3-retry-and-errors.ipynb`（重试三铁律 + 死循环反例练习）
- `ch02-tools/walkthrough.md`：跨周验证手记（三层金字塔 + 真调用脊线 + 四次「门禁抓作者」实录）

### Fixed
- runner 边界兜底经 `# noqa: BLE001` + 书面理由通过静态检查（noqa 纪律：仅限 catch-all 即功能的边界层）
- test_runner.py 导入格式 I001（自动修复）

### 事故记录（门禁纪律，2026-11-03，如实入库）
- **W4 首次推送时门禁为红**：制作人 shell 命令链 `pytest | tail -1` 的管道**吞掉了 pytest 退出码**，`&&` 链未刹车，红态混入 commit 2e63e92 并被打了 tag。
- **处置**：前向修复（2.3 notebook I001，回归测试第四次现场拦截）+ 删除并重打 v0.5.0 至绿态提交。
- **教训入库**：链式命令里禁止用管道包裹会失败的命令做闸门；要么先跑命令看退出码，要么用 `set -o pipefail`。（Missing Semester「Shell」讲次：exit code 是脚本的神经系统）
- stage-gate 启示：制作人自验时也必须贴**命令原始退出码**，不能贴管道美化后的输出。

### Sources（本次设计源泉）
- 错误分类对照 OpenAI API 错误码（429/5xx 可重试、400 不可）[未实访]
- agent-expert-outline.md 思维 #6/#9；ReAct 循环恢复思想（Building effective agents，访问 2026-11-02）

## [v0.4.0] - 2026-11-03

### Added
- `agent/tools/base.py`（Tool 基类：json_schema/prompt_line）+ `agent/tools/registry.py`（注册表：重名即炸/未知即报/to_callables 一键装配）
- `tests/test_tools.py`（7 条：含 schema 形状契约与「诚实的坑」用例）
- `smoke.py`：独立冒烟脚本（退出码可被 harness/CI 消费），替代管道写法；AGENTS.md §1 与 stage-gate A2 同步更新
- **打包构建落地**：pyproject 增加 hatchling 构建后端 + wheel 白名单（agent/demo/根模块，dev 依赖永不进产物）；`uv build` 实测产出 0.4.0 wheel+sdist
- 干净环境安装验证：临时 venv 安装 wheel → `from agent.react import parse_block` IMPORT-OK ✅
- `ch02-tools/`：lecture-notes（9 页，含打包构建课页与 Slide 1 ⭐ 核心章标注）+ 2.1-schema / 2.2-registry-dispatch 两本 notebook + exercises.md（三档 + smolagents 对照 + 卡点预告）
- AGENTS.md 瘦身复查：66 行（≤200 行纪律达标，思维 #7）

### Fixed
- 回归双层锁再次生效：ruff 先抓 smoke.py 盲捕获（BLE001）、再抓新 notebook 导入格式（I001）——「事故→门禁→永久回归」链路第三次现场演示

### Sources（本次设计源泉）
- Building effective agents 附录 2（ACI 三纪律，anthropic.com，访问 2026-11-02）
- MIT Missing Semester 2026「Packaging and Shipping Code」（missing.csail.mit.edu，访问 2026-11-02）
- agent-expert-outline.md 思维 #4/#6/#7

## [v0.3.0] - 2026-11-03

### Added
- `tests/regression/test_regressions.py`：首批 3 条回归（真实事件回锁：密钥错误 UX / ReAct 垃圾输入存活 / notebook ruff 事故）
- `demo/main.py` + `tests/test_demo.py`：FastAPI 服务化（/health + /chat，TestClient 注入假 LLM；本地真调用实测答案 27）
- `docs/guides/demo-hosting.md`：托管对比表（HF Spaces 主推）+ GitHub 主页挂载路径 + 卡点预告
- `docs/journal/ch01-review.md`：作业仪式首运转记录（提交单 + 三道检查 + 批阅五段，作为学员示范样例）
- `grade-homework.md` 第 2.5 步：AI 使用纪律核对（CS336 荣誉准则式）
- 依赖：fastapi、uvicorn、httpx（dev）
- ch01 lecture-notes Slide 1 标注 ⭐ 核心章

### Fixed
- regression 测试自caught：ruff PLW1510 拦截 subprocess.run 缺 check 参数（事故门禁化的现场演示，已修复并保留为教学素材）

### Sources（本次设计源泉）
- 事故回归化流程：agent-camp-outline.md §4.4（事故→复盘→改规则→eval 锁定）
- FastAPI 配置表：agent-camp-outline.md §5 阶段 0/1
- 托管推荐依据：agent-expert-outline.md 思维 #12；平台条款 [未实访] 已标注
- CS336 荣誉准则：stanford-cs336.github.io/spring2025（访问 2026-11-02）

## [v0.2.0] - 2026-11-02

### Added
- `agent/react.py`：纯文本协议 ReAct 循环（Thought/Action/Finish + 解析器 + 三种失败边界 + max_steps 预算）
- `agent/builtin/calc.py`：安全算术工具（AST 白名单求值，友好失败）
- `tests/test_react.py`：10 条测试——解析器、工具边界、状态机三种边界，全部注入假 LLM 不触网
- `ch01-react/`：lecture-notes.md（PPT 分页讲义）+ 1.1/1.2 两本 notebook + exercises.md（三档作业）
- `docs/arch/arch-agent-core.md`：agent/ 内核装配图（mermaid）
- `.github/workflows/gate.yml`：GitHub 门禁机器人（pytest + ruff）
- `.opencode/agent/course-producer.md` + `.opencode/command/next-week.md`：周驱动机制；AGENTS.md §5.1 自动推送豁免条款
- `docs/journal/ch01.md`：学员日志模板（stage-gate 第 9 项要求）
- `docs/guides/contributing-path.md`：贡献之路——前三次贡献 demo、最小提交与修复教导、贡献阶梯、Missing Semester 2026 融合映射
- `.opencode/agent/course-producer.md` 增补亲自验证律与 demo 辅助律
- gate.yml 补推成功，CI 首跑绿（16s）；分支保护实测：PR 需 `gate / test` 必过
- `ch01-react/walkthrough.md`：验证手记（四层验证金字塔 / 三招实现方式 / 实测记录表，供大家参考）
- course-producer 增补：验证手记律、周期打 tag 律（附注 tag、周周递增）、核心章节标注律（⭐=内核最小闭环四章）

### Sources（本次设计源泉）
- ReAct: arxiv.org/abs/2210.03629（循环协议）
- Building effective agents: anthropic.com/engineering/building-effective-agents（思维 #1/#4，访问 2026-11-02）
- Claude Code best practices: code.claude.com/docs（思维 #5/#6 确定性门禁，访问 2026-11-02）
- Stanford CS336: stanford-cs336.github.io/spring2025（思维 #10/#11 作业纪律，访问 2026-11-02）
- MIT 6.S191 体例 `[未实访]`

## [v0.1.0] - 2026-11-02

### Added
- `llm_utils.py`（get_llm_response/chat/masked_key，OpenAI 兼容 + 密钥三铁律）
- `chat.py`（终端小机器人）+ `00-first-call.ipynb` + 密钥保护三件套
- `tests/test_boot.py`（阶段 0 门禁 5 条）
- `.opencode/` 三 subagent + 三命令；AGENTS.md 项目规则

### Sources
- 吴恩达课程工具函数风格（get_llm_response 签名）
- hands-on-agentic 课程大纲 agent-camp-outline.md（阶段 0 定义）
