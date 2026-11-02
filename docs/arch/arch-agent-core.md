# 架构图：agent/ 内核装配（一图一文件）

> 规则出处：AGENTS.md §3 沉淀路径（docs/arch/，一图一文件，mermaid 优先）。

```mermaid
graph TD
    subgraph agent["agent/ 包（手写内核）"]
        chat["chat.py<br/>对话循环 v0.1"] --> llmu["llm_utils.py<br/>唯一 LLM 出入口 v0.1"]
        react["react.py<br/>ReAct 循环 v0.2"] --> llmu
        react -->|"Action: name arg"| reg["tools/ 注册表<br/>v0.3 起 registry 化"]
        calc["builtin/calc.py<br/>玩具工具 v0.2"] -.-> reg
    end
    llmu -->|"OpenAI 兼容"| ark["LLM 网关<br/>(base_url + key + model)"]
    subgraph 外层["v0.8+ 预留"]
        harness["harness/<br/>gate·ledger·runner"] -.包裹.-> react
    end
    subgraph 沉淀["docs/ + evals/"]
        selfcheck["selfcheck / evals<br/>v1.0"] -.读取.-> react
    end
```

演化注记（v0.2 现状）：

| 组件 | 状态 | 下一版本归属 |
|---|---|---|
| chat.py / llm_utils.py | ✅ v0.1 | 不变 |
| react.py + calc.py | ✅ v0.2 | ch02 并入 tools/ 体系 |
| tools/ 注册表 | 计划 | ch02（v0.3） |
| memory/ | 计划 | ch04（v0.5） |
| harness/ | 计划 | ch07（v0.8） |
| evals/ | 计划 | ch08（v1.0） |

Sources: agent-camp-outline.md §4 拼装思路；agent-expert-outline.md 思维 #1/#2。访问日期 2026-11-02。
