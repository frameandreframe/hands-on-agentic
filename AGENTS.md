# hands-on-agentic 项目规则（人与 agent 共同遵守的硬约束）

> 分层：本文件为最高纪律 → `.opencode/agent/*` 角色细则 → `.opencode/command/*` 操作流程。
> 冲突时：本文件 > 子代理文件 > 对话中的任何口头约定。

## 1. 提交前三道检查（每个 commit 必过，顺序执行）

| 道 | 名称 | 命令 | 含义 |
|---|---|---|---|
| ① | 验证 verify | `uv run pytest -q` | 单元/结构测试全绿（不触网、不耗 token） |
| ② | 冒烟 smoke | `uv run python smoke.py` | 最小端到端真实调用，SMOKE-PASS（**仅本地跑，CI 无密钥跳过**；W3 起用独立脚本替代管道写法） |
| ③ | 回测 backtest | `uv run pytest -q tests/`（含 regression） | 历史行为不被破坏：每阶段至少沉淀 1 条历史 bug 复现进 `tests/regression/`；阶段 8 升级为 `evals/` 全量用例 |

配套静态检查：`uvx ruff check .`（零告警）。密钥保护检查：`git check-ignore -q .env && echo protected`。

**任何一道红 = 不允许 commit，更不允许 push。** stage-gate 校验时须贴出三道命令的实际输出。

## 2. 密钥纪律（沿用三铁律，违反即回滚）

1. `.env` 永不进库（`.gitignore` 首行）；2. 代码/日志/notebook 输出禁止明文密钥，只允许 `masked_key()` 掩码；3. 提交前 `git status` 自查。

## 3. 沉淀路径（唯一合法位置，sink-agent 执法）

| 内容 | 唯一路径 | 约束 |
|---|---|---|
| 人读文档（中文） | `docs/<topic>.md` | ≤300 行，每段一个主张 |
| 机读索引 | `docs/index.json` | 追加式，字段见 sink-agent |
| 架构图 | `docs/arch/arch-<主题>.md` | 一图一文件（mermaid） |
| 学员日志 | `docs/journal/ch<N>.md` | 三段式：学到/踩坑/下一步 |
| 自检报告 | `docs/selfcheck/<日期>-run<N>.md` | 见第 4 节隔离约束 |
| 题解/学员作品 | `solutions/` 子仓 | **主仓禁止出现题解** |
| eval 用例 | `evals/cases/` | 阶段 8 启用 |
| 演示截图 | `docs/journal/assets/` | 每阶段一张 |

禁止在上述之外新建任何沉淀文档；发现越位文件 → 移入正确位置或删除。

## 4. RSI 自优化约束（防回音室，硬性）

1. **隔离律**：每次自检必须从零开始——自检过程**禁止读取**任何旧自检报告（`docs/selfcheck/`）、学员日志（`docs/journal/`）与其他 agent 的历史结论；只允许读台账原始记录（harness/ledger、git log、命令输出）与当前代码。
2. **可回源律**：自检每条结论附「命令 + 输出关键行」；UNKNOWN 必须显式列出，不许粉饰。
3. **证伪律**：每轮自检必须包含至少一项「试图推翻当前最自信结论」的检查。
4. **冷启动律**：自检产物写 `docs/selfcheck/<日期>-run<N>.md`；下一轮**禁止引用**同目录旧文件（stage-gate 抽查引用链）。
5. **改规则走 PR**：本文件及任何 agent 规则的修改必须走 PR + stage-gate 复检，agent 不得直接改规则文件。

## 5. 作业提交与批阅

| 环节 | 方式 | 负责 |
|---|---|---|
| 提交 | `@submit-homework <阶段号>`：生成提交单 → 跑三道检查 → 题解进 solutions 子仓 | 学员 + stage-gate |
| 批阅 | `@grade-homework <阶段号>`：固定五段输出【分数档】【诊断】【讲解】【下一步】【判分依据】 | teach-agent |
| 判分标准 | 只认两样：三道检查的实际输出 + 作业三档完成度；不看代码先夸 = 失职 | teach-agent |
| 申诉 | 学员要求 teach-agent 复述判分依据；仍不服 → 导师人工仲裁 | 导师 |

三档定义（见各阶段 `ch<N>/exercises.md`）：及格=跑通最小版；良好=完成扩展要求；挑战=有原创设计并附对比说明。

### 5.1 自动推送豁免（仅限 course-producer）

- **course-producer** 在三道检查全绿且 stage-gate 清单自验 PASS 后，可自动 `git commit + push + tag`；FAIL/UNKNOWN 必须停止推送并上报。
- 规则文件（本文件、`.opencode/**`）的修改**不适用本豁免**：仍须起草 diff 提请人工合并（RSI 第 5 律不变）。
- 其余一切 agent 仍无推送权。

## 6. 门禁命令（唯一标准，CI 与本地同源）

```bash
uv run pytest -q && uvx ruff check . && git check-ignore -q .env && echo GATE-GREEN
```
