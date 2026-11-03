# ch01 作业提交与批阅记录（仪式首运转 demo）

> 本文件即「提交→批阅」流程的**示范样例**（demo 辅助律：前三次照抄此格式）。日期 2026-11-03。

## 提交单

- **阶段/档位**：ch01 / 及格档（部分达到良好档要素）
- **变更清单**：agent/react.py、agent/builtin/calc.py、tests/test_react.py（10 条）、tests/regression/（3 条）、ch01-react/ 四件套、demo/main.py、docs/guides/demo-hosting.md
- **一句话自述**：手写纯文本协议 ReAct 循环，三种失败边界失败关闭，FastAPI 服务化并本地实测。
- **自查三问**：① 验证了什么——21 条测试全绿 + ruff 绿 + 冒烟真调用 + /chat 真调用返回 27；② 没验证什么——HF Spaces 远程部署路径（标注[未实测]，ch05 落地）；③ 抄了什么——ReAct 协议形式（arXiv:2210.03629），实现自写。
- **AI 使用纪律核对**：实现自写 ✅；引用已注明来源 ✅（grade-homework 第 2.5 步通过）。

## 门禁输出（三道检查，✅ 2026-11-03 实跑）

```text
① 验证：uv run pytest -q          → 21 passed in 0.44s
② 冒烟：chat.py 真调用            → 机器人正常回复（非空）
③ 回测：uv run pytest -q tests/   → 21 passed（含 regression 首批 3 条）
静态：uvx ruff check .            → All checks passed!
```

## 批阅（五段，teach-agent 格式）

【分数档】**及格 PASS**（良好档要素达成 2/2 的预备：regression 已沉淀，新工具未做——留给学员作业）

【诊断】循环/解析/边界/服务化四层全部有测试锁定；E2E 真调用两步收尾干净；demo /chat 返回结构透明（answer+steps）。

【讲解】本批最值得学的一处：regression 测试**当场拦住了它自己**（ruff PLW1510 抓住 subprocess.run 缺 check 参数）——这就是「事故门禁化」的完整闭环演示：写测试→门禁抓作者→修复→永久锁定。

【下一步】① 学员完成 exercises.md 良好档（新工具 + 1 条 regression）；② 把 /chat 部署到 HF Spaces 并挂上 GitHub 主页；③ journal「踩坑」段改写为第一人称。

【判分依据】exercises.md 及格档三条件：notebook 无输出✓、pytest 全绿✓、journal 三段✓；门禁输出如上✓；判分过程未读取任何历史批阅结论（独立批阅纪律）。
