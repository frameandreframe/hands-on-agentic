# ch02 讲义：tool use——从字符串协议到 JSON Schema

> **⭐ 核心章**（内核最小闭环之一：工具。结业必修并纳入答辩。）
>
> Sources: agent-expert-outline.md 思维 #4（ACI）· Building effective agents 附录 2（anthropic.com/engineering/building-effective-agents，访问 2026-11-02）· 课前自修：Missing Semester「Packaging and Shipping Code」讲次（missing.csail.mit.edu，2026 版，访问 2026-11-02）

## Slide 1 · 学完这两周你能

- 手写符合工业协议的 JSON Schema（并一眼看出错在哪）
- 实现 ToolRegistry：注册、查重、渲染提示行、对接 ReAct 循环
- 完成本仓第一次 `uv build` 并在干净环境安装验证

## Slide 2 · 为什么字符串协议不够用

ch01 的 `Action: calc 3*(7+2)` 是空格分隔的约定——参数一多（可选参数、类型、嵌套）就崩。
工业协议 = **JSON Schema 描述参数** + **模型输出结构化 tool_call**。协议升级不改循环本质：还是「想→调→看」。

## Slide 3 · JSON Schema 手写：最易错的一处

错误示例（把 required 塞进 properties）：

```json
{"properties": {"expr": {"type": "string", "required": true}}}
```

正解（required 在**顶层**，与 properties 平级）：

```json
{"type": "object", "properties": {"expr": {"type": "string", "description": "算术表达式"}}, "required": ["expr"]}
```

口诀：**properties 管字段长什么样，required 管哪些必须来**——两个平级兄弟，不是父子。

## Slide 4 · ACI 三纪律（思维 #4）

1. **描述即文档**：description 写清「做什么 + 不做什么」，模型按它决定调不调。
2. **poka-yoke**：schema 类型收紧、枚举限定——让模型想错都难。
3. **诚实对齐**：schema 字段名必须与实现一致（tests/test_tools.py 里 test_calc_tool_schema_mismatch_is_visible 就是这个坑的活标本）。

> 引文：「we actually spent more time optimizing our tools than the overall prompt.」——Building effective agents 附录 2。

## Slide 5 · 项目结构与创建顺序（本周新增文件）

```bash
mkdir -p ch02-tools agent/tools
touch agent/tools/__init__.py agent/tools/base.py agent/tools/registry.py
touch ch02-tools/2.1-schema.ipynb ch02-tools/2.2-registry-dispatch.ipynb
```

顺序 = 依赖顺序：base.py（Tool 定义）→ registry.py（目录）→ tests/test_tools.py（锁行为）→ notebook（教学包装）。
装配图更新：[docs/arch/arch-agent-core.md](../docs/arch/arch-agent-core.md)（react.py → tools/ 注册表连线本周变实线）。

## Slide 6 · 测试的目的与边界（本周扩展）

新边界两条：① **schema 形状可测**（`json_schema()` 输出断言——结构即契约）；② **重复注册必须炸**（fail-closed：同名不同义是事故温床，`pytest.raises(ValueError)`）。
警惕：不要为 dataclass 的字段赋值写测试——那是测语言，不是测行为。

## Slide 7 · 打包构建课（Missing Semester「Packaging」同款主题）

本仓 W3 已落地，逐步复盘：

```bash
# ① pyproject.toml 声明构建后端（没有它 uv build 直接拒绝）
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# ② 声明「什么进 wheel」：运行时需要的包；dev 依赖（pytest/jupyter）永不进产物
[tool.hatch.build.targets.wheel]
packages = ["agent", "demo"]

# ③ 构建 + 三验
uv build                              # 产出 dist/*.whl + *.tar.gz
tar -tf dist/*.tar.gz | head          # 验 sdist 内容
uv venv /tmp/v && uv pip install --python /tmp/v/bin/python dist/*.whl   # 干净环境
/tmp/v/bin/python -c "from agent.react import parse_block; print('OK')"
```

**版本策略**：pyproject version = 当前周 tag（v0.4.0）；dev 依赖永不打包；lock 文件必须与 pyproject 同步提交（HF Spaces 构建失败第一原因）。

## Slide 8 · 超链接清单

| 资料 | 链接 | 用途 |
|---|---|---|
| Building effective agents 附录 2 | https://www.anthropic.com/engineering/building-effective-agents | ACI 三纪律出处 |
| JSON Schema 官方 | https://json-schema.org/learn/getting-started-step-by-step | 2.1 参考手册 |
| OpenAI function calling 指南 | https://platform.openai.com/docs/guides/function-calling | 2.2 工业协议对照 |
| Missing Semester 2026 | https://missing.csail.mit.edu | 课前自修：Packaging 讲次 |
| 本仓打包实证 | CHANGELOG v0.4.0 | uv build 全记录 |

## Slide 9 · 下一步预告

2.3（W4）：错误重试与超时——工具调用永远可能失败，runner 要让失败「可见、可重试、可熔断」。
