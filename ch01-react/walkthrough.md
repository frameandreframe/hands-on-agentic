# ch01 验证手记：ReAct 循环的验证思路与实现方式

> **性质**：制作人（course-producer）的验证手记，每章作业验证后产出一份，**供大家参考**——看懂「怎么验证」与「为什么这么验证」，比自己写出代码更重要。
> **Sources**: agent-expert-outline.md 思维 #6（能跑的检查）/ #9（预算止损）；亲自验证律（course-producer SOP）。验证日期 2026-11-03。

## 1. 验证思路：四层金字塔（从便宜到昂贵）

```text
        ┌─ L4 E2E 真调用 ──── 1 次，验证「模型真的守协议」（最贵，最后跑）
      ┌─ L3 状态机边界 ──── 注入假 LLM，验证三种失败关闭（中）
    ┌─ L2 工具防呆 ──────── 注入恶意/非法输入，验证友好失败（中）
  ┌─ L1 解析器单元 ──────── 纯函数，秒级反馈（最便宜，最先跑）
```

**原则：把贵的验证留到最后、把便宜的验证做厚。** L1–L3 全部不触网（16 条测试 <0.5 秒跑完），只有 L4 花一次真实 token。

## 2. 实现方式（关键三招）

### 招式 1：依赖注入让测试零成本

```python
def _scripted_llm(script: list[str]):
    it = iter(script)
    def _fn(messages): return next(it)
    return _fn

result = run_react("x", {}, llm_fn=_scripted_llm(["Thought: 直接\nFinish: 42"]))
```

`run_react` 的 LLM 是参数不是硬编码——测试时塞入「按剧本演出的假 LLM」，循环逻辑被完整驱动但分文不花。**这一招贯穿全课程**：ch04 的假 embedding、ch07 的假门禁同理。

### 招式 2：失败关闭的三种边界各配一条负面测试

| 边界 | 测试 | 断言 |
|---|---|---|
| 格式错误 | 模型输出闲聊 | observation 含 `[格式错误]` |
| 未知工具 | `Action: nope x` | observation 含 `[未知工具]` |
| 步数耗尽 | 永不 Finish 的剧本 ×3 步 | answer 含 `最大步数`（**不许是假装的答案**） |

负面用例多于正面用例（10 条里 6 条负面）——循环代码的健壮性几乎全部来自边界。

### 招式 3：工具防呆 = AST 白名单（poka-yoke）

`calc` 不用 `eval`，用 AST 白名单遍历：只允许数字与七种运算符，其余节点直接 `ValueError`。`calc("__import__('os')")` 返回 `[calc 错误] ValueError: 不允许的表达式节点: Call`——**工具的错误信息会进入模型的 Observation**，所以它必须是可读的、非致命的。

## 3. 实测记录（✅ 全部真实执行，2026-11-03）

| 验证项 | 命令 | 结果 |
|---|---|---|
| L1–L3 测试 | `uv run pytest -q` | 16 passed, 0.3s |
| 静态检查 | `uvx ruff check .` | All checks passed |
| 冒烟（真调用） | `printf "你好\n退出\n" \| uv run python chat.py` | 机器人正常回复 |
| L4 E2E | `run_react("用 calc 计算 3*(7+2)...")` | 答案 27，2 步收尾：`Action: calc 3*(7+2)` → `obs=27` → `Finish: 27` |
| CI 首跑 | GitHub Actions `gate` | success，16s（PR 检查名 `gate / test` 已纳入分支保护） |
| 真实踩坑 → 教学素材 | OAuth 缺 workflow scope 被拒推；admin 直推出现 bypass 提示 | 均已写入 docs/guides/contributing-path.md 卡点 |

## 4. 供大家参考的复刻路径

1. 先读 lecture-notes.md Slide 2–4（协议与停止条件）
2. 跑 `uv run pytest -q tests/test_react.py -v` 看每条测试名的意图
3. 对照 `agent/react.py` 逐行找「测试 ↔ 实现」的对应关系（每条测试锁一段行为）
4. 自己重写 my_parse（notebook 1.1 第 3 格），用测试验证你的版本
5. 卡住时回看 docs/guides/contributing-path.md §2 修复四步——先失败测试，后修复

> 学员作业的参考题解不在此文件（进 solutions 子仓）；本手记只讲「验证的思路与实现方式」。
