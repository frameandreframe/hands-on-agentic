# ch02 作业：tool use（W3–W4，及格 / 良好 / 挑战）

> 交作业流程：`@submit-homework ch02 <档位>`。⭐ 核心章：结业必修。

## 本周卡点预告（先读，少踩坑）

1. **required 位置错**：它是顶层字段，不是参数定义的子字段——2.1 的 check_schema 会当场教你（先错后对是设计好的路径）。
2. **schema 字段名与实现不同步**：模型按 schema 传参，按错名字传来的参数你的工具接不住——test_calc_tool_schema_mismatch_is_visible 就是这个坑。
3. **uv.lock 漂移**：`uv add` 之后忘了提交 lock，别人的环境立刻坏——依赖变更与 lock 必须**同一提交**。
4. **真调用烧钱**：2.2 的可选格一次约两次模型往返；练习全部用注入假 LLM 完成。

## 三档

| 档位 | 要求 | 验收 |
|---|---|---|
| 及格 | 两本 notebook 全通；check_schema 对错误示例全部报警；pytest 全绿 | stage-gate PASS |
| 良好 | 及格 + 新工具（timed_echo 或 fake_weather）注册进 registry + schema 手写通过 check_schema + 1 条 regression | 新工具被 run_react 正确调用 |
| 挑战 | 良好 + 实现「工具描述超长截断」或「参数白名单校验」任一项 + 与 OpenAI function calling 文档的 schema 做对照笔记（≥5 行） | 笔记注明读到的文档章节 |

## 开源对照（OSS 目标）

- 项目：[smolagents](https://github.com/huggingface/smolagents) 的 `Tool` 类设计（huggingface 官方极简 agent 库）
- **最小提交标准**：solutions 子仓 `ch02/compare-smolagents-tool.md`——对照表 ≥5 行（工具定义方式/schema 生成/错误处理/注册机制/与 ACI 三纪律的吻合度），每行注明源码文件。

## AI 使用纪律（CS336 荣誉准则式）

- 允许：问 schema 语法、问报错含义、问「为什么 required 在顶层」。
- 禁止：让 AI 生成整个 Tool 类/registry 实现直接提交；写核心代码时关闭 AI 补全。
- 引用：凡 AI 帮助理解的结论，journal 注明「经 AI 解释后自行验证」。

## 本作业设计出处

- Building effective agents 附录 2（ACI/poka-yoke，访问 2026-11-02）；agent-expert-outline.md 思维 #4/#6；MIT Missing Semester 2026「Packaging and Shipping Code」（访问 2026-11-02）；Stanford CS336 荣誉准则。
