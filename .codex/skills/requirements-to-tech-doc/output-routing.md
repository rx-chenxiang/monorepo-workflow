# 产出类型路由

根据需求粒度与目标，选择一种或多种产出（可组合）。

## 决策树

```
用户需求
├─ 仅口头/图片、无结构化文档？
│   └─ P0 模块技术规划（§1～§11）
├─ 新模块、双端 modules/*.md 为空或「规划中」？
│   └─ P0 技术规划 + P1 双端模块文档骨架
├─ 技术规划已有，要启动全栈编码？（双端范围）
│   └─ P1【强制】编码前置摘要 dev-brief.md（双端必须，不可跳过）
├─ 技术规划已有，要启动编码？（仅后端或仅前端）
│   └─ P2 编码前置摘要 dev-brief.md（推荐）
├─ 单一页面/小功能迭代（范围 < 1 模块）？
│   └─ P3 调用 writing-tech-design-doc
├─ 仅管理端、无后端新接口？
│   └─ 技术规划以 bss_front 页面/API 为主；后端 § 可引用已有 Domain 文档
└─ 代码已落地、文档落后？
    └─ 不用本技能 → doc-updater
```

> **双端 dev-brief 强制说明**：范围为任一 `AGENTS.md` 注册项目组双端时，dev-brief 是阶段间信息交接的核心载体，
> 省略会导致子代理 prompt 信息不完整、接口清单遗漏、范围边界不清。**不允许跳过**。

## 产出对照表

| 类型 | 文件名模式 | 主要读者 | 下游技能 |
|------|-----------|---------|---------|
| 模块技术规划 | `{序号}-{模块}模块技术规划.md` | 全栈、产品、Agent | `coding-agent-team-fullstack` |
| 模块文档骨架 | 注册表命中子项目 `{代码根}docs/modules/*` | 各端开发者 / `doc-updater` | `api-developer` / `front-developer`；编码后 §3～§6 以代码为准 |
| 编码前置摘要 | `docs/{项目组ID}/{需求名}/coding-plan/{模块}-dev-brief.md` | 子 Agent | `api-developer`、`front-developer`；双端见 `coding-agent-team-fullstack` |
| 前端技术设计 | `docs/{项目组ID}/{需求名}/技术设计方案/{需求名}前端技术设计文档.md` | 前端编码 | `writing-tech-design-doc` |

## 范围边界写法

在技术规划 §1 或 dev-brief 中必须显式列出：

```markdown
### 范围边界
**包含**：…
**不包含**（本轮不做）：…
**依赖其他模块**：…（只写接口契约，不展开实现）
```

<!-- AIGC:cursor|author:沉香|lines:约40|dates:2026-06|功能说明:产出路由对齐ahyk_bss+bss_front双项目 -->
