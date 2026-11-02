---
description: RSI 自检：冷启动、隔离运行、证伪优先。禁止读取任何历史自检报告与学员日志
---
执行一轮 RSI 自检（AGENTS.md 第 4 节），范围：$ARGUMENTS（缺省 = 当前阶段产物）

## 隔离声明（先于一切工作输出在响应顶部）
本轮自检未读取：docs/selfcheck/ 任何旧报告、docs/journal/、其他 agent 历史结论。
允许的输入仅有：git log/diff、命令实际输出、当前代码、tests/ 台账、harness/ledger（阶段 7 起）。

## 步骤
1. 产物自检：对照 AGENTS.md 三道检查逐项复跑，结论分层 observed/derived/inferred/unknown，每条附「命令+输出关键行」。
2. 证伪项（必做）：选出当前实现中我最自信的 1 个结论，设计并执行一次尝试推翻它的检查，如实记录结果。
3. 流程自检：本阶段 AGENTS.md 规则里，哪条从未被触发（死规则）？哪次返工暴露了规则缺口？只依据 git log 与台账判断。
4. 落盘：docs/selfcheck/<YYYY-MM-DD>-run<N>.md（run 编号 = 当日序号，不看旧文件、直接按 git 里已有文件数+1 推断）。
5. 机读：docs/index.json 追加一条（stage、date、pass 率、unknown 数）。
6. 收尾：建议唤起 @stage-gate 做隔离抽查（D 节第 11/12 项）。

## 红线
UNKNOWN 只允许收敛不允许膨胀：本轮 unknown 数 > 上一轮时（仅可通过 index.json 数字比较，禁止读旧报告内容），立即停止自检并上报导师。
