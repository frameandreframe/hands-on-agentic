# ch01 讲义：ReAct——让模型「想一步、做一步、看一步」

> 体例：Stanford/MIT 课堂随课讲义，PPT 分页式，每页一个主张。
> Sources: ReAct（arxiv.org/abs/2210.03629）· agent-expert-outline.md 思维 #1/#6/#10 · MIT 6.S191 lab 体例 `[未实访]`

## Slide 1 · 学完这节课你能

- 用 60 行 Python 手写一个 ReAct 循环（不用任何框架）
- 说出循环的三种失败边界，并让它们「失败关闭」
- 为循环写出不触网的测试（依赖注入）

## Slide 2 · ReAct 是什么

三行协议：模型每轮只许输出 `Thought:`（推理）、`Action:`（工具调用）或 `Finish:`（最终答案）。
程序解析后执行工具，把结果作为 `Observation:` 喂回——「想一步、做一步、看一步」。
一手来源：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)（2022）。

## Slide 3 · 为什么有效（思维 #1）

> 「They are typically just LLMs using tools based on environmental feedback in a loop.」
> ——[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（Anthropic, 2024-12-19，访问 2026-11-02）

Agent 不是黑魔法：**循环 + 工具 + 反馈**。推理显式化（Thought 上墙）让错误可观察；Observation 回注让模型基于事实而非想象继续。harness 应该薄——模型聪明，外壳别抢戏。

## Slide 4 · 停止条件与预算

没有止损的循环是事故。三个出口：`Finish:`（正常）、`max_steps`（预算耗尽）、解析失败重试上限。
本课选择：步数耗尽 → 返回 `[达到最大步数，未完成]`——**失败关闭**，绝不假装完成（这是 ch07 harness 的第一块积木）。

## Slide 5 · 项目结构与创建顺序（PyCharm / 终端通用）

```bash
mkdir -p ch01-react agent/builtin tests docs/arch docs/journal
touch agent/__init__.py agent/builtin/__init__.py
```

创建顺序 = 依赖顺序（先被依赖、后依赖人）：

```text
llm_utils.py（已有）→ agent/react.py → agent/builtin/calc.py → tests/test_react.py → 课程文档
```

完整装配图：[docs/arch/arch-agent-core.md](../docs/arch/arch-agent-core.md)

## Slide 6 · 测试的目的与边界（思维 #6）

**目的四条**：① 锁定行为（重构的信心来源）② 回归保护（bug 修一次、测一辈子）③ 活文档（测试即用法示例）④ 门禁依据（CI 只认测试，不认口头承诺）。
**边界四条**：① 不测私有实现细节（重构后测试不该跟着改）② 不 mock 被测物本身 ③ 边界值优先（空串、未知工具、步数耗尽）④ 测试也有维护成本，宁缺毋滥。
本课示范：`tests/test_react.py` 全部注入假 LLM（`_scripted_llm`）——**测试永远不触网、不花钱**。

## Slide 7 · 超链接清单

| 资料 | 链接 | 用途 |
|---|---|---|
| ReAct 论文 | https://arxiv.org/abs/2210.03629 | 精读第 3 节即可 |
| Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | 思维 #1 出处 |
| mini-swe-agent（作业对照） | https://github.com/SWE-agent/mini-swe-agent | 百行级真实 agent loop |
| 本仓装配图 | docs/arch/arch-agent-core.md | 结构演进 |

## Slide 8 · 下一步预告

ch02 把 `Action:` 升级为真正的 function calling（JSON Schema）——今天的 `calc 3*(7+2)` 字符串协议是为了让你看清调度本质，下周换成工业协议。
