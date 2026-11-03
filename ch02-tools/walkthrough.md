# ch02 验证手记：工具体系的分层验证（两周跨度章）

> **性质**：course-producer 验证手记，供大家参考。ch02 为 ⭐ 核心章，跨 W3–W4 两周，验证对象：schema → registry → runner 三层。
> **Sources**: agent-expert-outline.md 思维 #4/#6/#9 · 亲自验证律。验证日期 2026-11-03。

## 1. 验证思路：三层金字塔 + 一条「真调用脊线」

```text
L4 真调用脊线 ── smoke.py（密钥→网关→模型）+ /chat 真调用（答案 27）
L3 runner 行为 ── 7 条注入 flaky：重试计数/分类/退避/熔断开-关
L2 registry 纪律 ── 7 条：重名炸/未知报/prompt 渲染/to_callables 装配
L1 schema 契约 ── json_schema() 形状断言 + 「诚实的坑」对齐用例
```

跨周章的验证要点：**每周收口都必须全绿**——W3 收在 L1/L2，W4 补齐 L3 并把 L4 从「能通」升级为「有保护地通」（runner 上岗）。

## 2. 实现方式：三招

1. **错误分类是重试的前提**：`TransientToolError`（可重试）与 `FatalToolError`（一次都别试）是两个类型而不是布尔参数——类型即文档，pytest.raises 直接收紧行为。
2. **指数退避两个参数都可调**：`RetryPolicy(base_delay=0.01, max_attempts=3)`——生产默认 0.2s 起步，测试 0.01s 把 3 次重试压进毫秒级。**测试里等待时间必须是参数，不是常数 sleep**。
3. **熔断用计数器不用定时器轮询**：`_consecutive_fail` 字典 + `time.monotonic()` 冷却戳，半开=冷却到期后放行一次试探。第 4 次调用断言「工具没有被执行」——快速失败是可测的行为，不是口号。

## 3. 实测记录（✅ 全部真实执行，2026-11-03）

| 验证项 | 命令 | 结果 |
|---|---|---|
| 全量测试 | `uv run pytest -q` | 35 passed（W3 收口 28 → W4 收口 35） |
| 静态 | `uvx ruff check .` | All checks passed（见 §4 两次拦截） |
| 冒烟 | `uv run python smoke.py` | SMOKE-PASS reply='ok' |
| 熔断触发（L3） | notebook 2.3 第 3 格：3 次连续失败后第 4 次 | `[熔断]` 返回且 **工具未被执行**（calls 不增）✅ |
| 装配（L3→循环） | `r.wrap("flaky", fn)` 塞进 run_react | 循环对保护逻辑无感知，正常收尾 ✅ |
| 真调用（L4） | W2 的 /chat 真调用 + 本周 smoke | 答案 27 / SMOKE-PASS ✅ |
| 打包（W3 遗产复验） | `uv build` + 干净 venv 安装 | wheel 0.4.0 → IMPORT-OK ✅ |

## 4. 两次「门禁抓作者」实录（本周最大的教学素材）

1. **BLE001 ×2**：smoke.py 的盲捕获（W3）、runner.py 的边界兜底（W4）——前者改为收窄 `(APIError, RuntimeError)`；后者是**故意的功能**（边界层必须兜底），走了 `# noqa: BLE001` + 书面理由。
2. **I001 ×2**：两本新 notebook 导入格式。
   > noqa 纪律：只允许在「catch-all 本身就是功能」的边界层使用，且必须写明理由——没有理由的 noqa 是技术债的遮羞布。
3. **PLW1510**（W2）：regression 测试自己缺 `check=False`。

## 5. 供大家参考的复刻路径

1. 跑 `uv run pytest -q tests/test_tools.py tests/test_runner.py -v`，把 14 条测试名念一遍——每条是一个行为契约。
2. 打开 `runner.py` 只看 `run()` 的异常三分支：Transient 循环 / Fatal 直返 / 兜底直返。
3. notebook 2.3 第 3 格亲手跑熔断：改 threshold=1 再跑，体会参数即语义。
4. 失败注入法（`_flaky`/`_scripted`）是本课程可复用到底的验证武器，ch07 harness 会升级它为 eval 注入。
