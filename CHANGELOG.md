# Changelog

本文件条目遵守 Keep a Changelog 风格；每条附 Sources（设计源泉，可回源）。

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
