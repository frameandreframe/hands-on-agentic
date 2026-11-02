# ch01 作业：ReAct 循环（及格 / 良好 / 挑战）

> 交作业流程：`@submit-homework ch01 <档位>`（会自动跑三道检查并唤起批阅）。

## 本周卡点预告（先读，少踩坑）

1. **模型不守协议**：系统提示必须写「每轮严格输出以下两行之一」；不守协议时回 `[格式错误]` 让它自我修正，而不是直接崩溃或替它编答案。
2. **解析器脆弱**：只认行前缀、每类只取第一个匹配、大小写不敏感——不要上正则轰炸，先让测试（test_parse_block_*）变绿。
3. **温度影响守协议率**：temperature 越高越容易跑偏，实验时固定其他变量。
4. **真实调用花的是你的钱**：notebook 里真调用限 max_steps=4；测试永远注入假 LLM。

## 三档

| 档位 | 要求 | 验收 |
|---|---|---|
| 及格 | 两本 notebook 全部单元格跑通（提交前清输出）；`uv run pytest -q` 全绿；journal 三段齐全 | stage-gate PASS |
| 良好 | 及格 + 新增一个内置工具（timed_echo / fake_weather 任选）+ 在 `tests/regression/` 沉淀 1 条用例（用例名写清历史背景） | 新工具被 ReAct 正确调用；regression 绿 |
| 挑战 | 良好 + 实现「工具输出超长时截断」或「解析失败计数器」任一项 + 与 mini-swe-agent 的 loop 对比笔记 | 笔记 ≥5 条差异，每条有源码行号证据 |

## 开源对照（OSS 目标）

- 项目：[mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)（SWE-agent 官方极简版，约百行级 loop）
- **最小提交标准**：solutions 子仓 `ch01/compare-mini-swe-agent.md`——对照表 ≥5 行（协议形式/工具分发/错误处理/停止条件/提示词组织），每行注明你读到的文件与行为证据；不强求 PR，题解入子仓即可。

## AI 使用纪律（CS336 荣誉准则式）

- 允许：问 AI 概念（ReAct 为什么有效）、问报错含义、问 API 用法。
- 禁止：让 AI 直接产出作业实现并提交；关闭 IDE 的 AI 补全写核心循环（本阶段就 60 行，值得亲手敲）。
- 引用：凡 AI 帮你理解的结论，journal 里注明「经 AI 解释后自行验证」。

## 本作业设计出处

- MIT 6.S191 lab 作业体例（讲义+实验+提交）`[未实访]`；Stanford CS336 from-scratch 与荣誉准则（stanford-cs336.github.io/spring2025，访问 2026-11-02）；agent-expert-outline.md 思维 #1/#6/#11。
