# 贡献之路：从第一次克隆到重构优化

> **Sources**（可回源）：MIT Missing Semester 2026（missing.csail.mit.edu，访问 2026-11-02，observed）· Stanford CS336 荣誉准则（stanford-cs336.github.io/spring2025，访问 2026-11-02）· 本仓库命令均为 **2026-11-02 真实执行验证**（标注 ✅）。

## 0. 贡献阶梯总览

| 阶 | 内容 | 对应周次 | 门槛 |
|---|---|---|---|
| Ⅰ | 改文档错字 / 补一句话 | W1–W2 | 会 clone/commit/PR |
| Ⅱ | solutions 子仓交题解 | W2 起 | 三道检查 |
| Ⅲ | 写特性（先测试后实现） | ch02 起 | 良好档作业 |
| Ⅳ | 跑门禁并读懂 CI 输出 | 全程 | 必修 |
| Ⅴ | 重构（门禁保护下） | ch04 起 | 及格档以上 |
| Ⅵ | 上游开源项目贡献 | ch05 起 | 挑战档 |

## 1. 前三次贡献 demo（逐条照抄）

> 前三次照抄是**规定动作**：先让流程肌肉记忆成型，再谈理解。第 4 次起只给提示。

### Demo 1（第 1 次）：修复主仓一个文档错字

```bash
# ① 克隆主仓（公开仓，无需权限）✅ 已验证
git clone https://github.com/frameandreframe/hands-on-agentic.git
cd hands-on-agentic
uv sync                                   # 装依赖（lock 文件保证版本一致）

# ② 开分支：命名规范 feat|fix|docs/<主题>
git switch -c docs/fix-typo

# ③ 最小改动：只改一个错字，不动别的行
#    用编辑器改 docs/ 某文件后：
git diff                                   # 亲眼确认 diff 只有你那一行
git add <文件> && git commit -m "docs: fix typo in ch01 lecture notes"

# ④ 推送 + 开 PR（gh 已登录）
git push -u origin docs/fix-typo
gh pr create --fill
# PR 上会自动跑 gate / test 检查，绿色才能合并（分支保护已配置）✅ 已验证
gh pr checks                               # 查看 CI 状态
```

**实测注意点**：
- 首次 push 时若见 `Bypassed rule violations ... Required status check "gate / test"`（管理员直推 master 才会出现）——学员走 PR 流程不会遇到；CI 首跑实测 16 秒全绿 ✅。
- CI 输出里的 `Node.js 20 is deprecated` 等黄色 annotation 是常态噪音，**学会区分 annotation（提示）与 error（失败）**是 Missing Semester「Debugging」讲次的基本功。

### Demo 2（第 2 次）：solutions 子仓交题解

```bash
# 前置：你需要题解仓访问权（向导师申请协作者）
# 主仓克隆时一并拉子仓（需 gh auth login 的凭据）✅ 已验证
git clone --recurse-submodules https://github.com/frameandreframe/hands-on-agentic.git

# 已克隆过的补拉子仓：
cd hands-on-agentic && git submodule update --init --recursive

# 题解只进子仓（AGENTS.md §3：主仓禁止出现题解）
cd solutions && git switch -c solutions/ch01
mkdir -p ch01 && $EDITOR ch01/exercises-solutions.md   # 中文讲解+中文注释
git add -A && git commit -m "solutions: ch01 exercises"
git push -u origin solutions/ch01 && gh pr create --fill --repo frameandreframe/hands-on-agentic-solutions
```

**实测发现（重要）**：无权限者克隆时子仓拉取会失败——**这是特性不是 bug**（防剧透）；有 `gh auth login` 凭据者自动通过 ✅。

### Demo 3（第 3 次）：给上游开源项目提文档修正

以 [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) 为例：

```bash
# ① 网页上点 Fork，然后：
gh repo clone <你的用户名>/mini-swe-agent && cd mini-swe-agent
# ② 先搜：这个错字/问题是否已有人提过（开源礼仪第一课）
gh issue list --repo SWE-agent/mini-swe-agent --search "typo in README"
# ③ 小步：一 PR 只解决一件事；标题用项目惯例（先看该仓最近 PR 标题风格）
git switch -c docs/fix-readme-typo && $EDITOR README.md
git commit -m "docs: fix typo in README installation section"
git push -u origin docs/fix-readme-typo && gh pr create --fill
# ④ 被要求改？在原分支追加 commit 再 push，PR 自动更新——不要新开 PR
```

## 2. 最小提交与修复教导

### 最小提交三律

1. **一个意图一个提交**：commit message 说得清「这一把干了什么」——说不清就是混了多个意图。
2. **diff 最小可审**：审阅者 30 秒能看完；顺手改了别的东西 = 拆开重提。
3. **message 用前缀**：`feat|fix|docs|chore|ci|solutions: 一句话`（与本仓 CHANGELOG 对齐）。

### 修复四步（bug → 回归锁定）

```text
① 复现：一条命令稳定触发 bug（复现不了的 bug 不修，先加日志观察）
② 失败测试：把复现写成测试，放进 tests/regression/，命名讲清历史背景
   例：test_regression_2026_11_empty_repo_submodule_add_fails
③ 最小修复：改动只为了绿灯，不顺手重构（越界的重构单独开任务，AGENTS.md §5）
④ 回归锁定：修复的测试永久留在 regression/——这个 bug 从此不可能无声复活
```

> 为什么②必须在③前：先红的测试证明你**真的复现了**；修复后它变绿证明你**真的修好了**。这两件事各需证据，思维 #6「给 agent 一个能跑的检查」的微缩版。

## 3. 贡献阶梯详解（写特性 → 测试 → 门禁 → 重构 → 优化）

- **写特性**（Ⅲ 阶）：永远「失败测试先行」——在 tests/ 写一个红的测试描述期望行为，实现到它变绿。特性代码与测试代码**同一个提交**（AGENTS.md 测试纪律）。
- **跑门禁**（Ⅳ 阶）：本地三道检查 = CI 的预演（同一套命令，AGENTS.md §6）；CI 红了先读**自己 PR 的日志**再问人；区分 annotation / warning / error。
- **重构**（Ⅴ 阶）：**先确认门禁覆盖目标代码**（没测试保护的重构 = 裸奔），然后小步走：每步 diff 可审、测试全绿、行为不变。重构 PR 里禁止混入行为变更。
- **优化**（Ⅵ 阶）：先测量再优化（Missing Semester「Debugging and Profiling」讲次精神）——用数据证明瓶颈，优化后用同一数据证明改善。

## 4. Missing Semester 2026 融合映射

> 该课 2026 版把 AI 工具**融入每一讲而非单设一讲**（「AI is a cross-functional enabling technology」）——与本课程「agent 即工具链一部分」的立场一致。observed：2026-11-02。

| Missing Semester 2026 讲次 | 本课程落点 | 衔接任务 |
|---|---|---|
| Course Overview + Shell | 阶段 0 环境 | 开营前自修：管道/重定向（本课冒烟测试用到 `\|`）|
| Command-line Environment | AGENTS.md / uv / pycharm 页 | W1 lecture-notes Slide 5 |
| Development Environment and Tools | uv / jupyter / opencode 全链 | ch00 |
| Debugging and Profiling | ch01 状态机调试；ch07 harness | 读 CI 日志练习（Demo 1 注记） |
| Version Control and Git | W1–W2 全部 demo | 本文件第 1 节 |
| **Packaging and Shipping Code** | W3 打包构建课 / ch02 交付 | uv build/publish |
| **Agentic Coding** | 全课程 + agent-expert-outline.md 思维 12 条 | 开营导读材料 |
| **Code Quality** | 三道检查 / ruff / 门禁机器人 | W1 已落地 |

映射使用规则：每章 lecture-notes 的「课前自修」一节给出对应讲次链接；作业卡点优先回看对应讲次再求助。
