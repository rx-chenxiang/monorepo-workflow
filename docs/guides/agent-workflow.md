# Agent 工作流

本模板将 Agent 当作协作成员，而不是脱离项目上下文的代码生成器。规则、文档与目录边界共同决定 Agent 可以在哪个项目做什么。

## 配置层级

```text
AGENTS.md
  └── .codex/rules/project-routing.mdc
        ├── 角色工作流（产品 / 设计 / 测试 / API / 前端）
        └── 项目范围（api / fornt_admin / m_front / pc_fornt / general）
              └── {project}/AGENTS.md → {project}/docs/README.md → 模块文档
```

根目录 [AGENTS.md](../../AGENTS.md) 是人类贡献者和 Agent 的共同入口。它定义项目注册表、目录边界、文档优先级和验证要求。

## 一次任务如何被路由

1. 识别任务角色，例如产品、设计、测试、后端或前端开发。
2. 识别目标范围：某一端，或 `general` 全部四端。
3. 读取与该角色和范围匹配的规则及项目文档。
4. 在限定范围内实现，并同步所影响的文档。
5. 按任务风险执行基础验证；跨端需求按端汇报结果。

## 关键约束

- 当前默认注册表中，`general`、`全栈`、`四端` 等请求覆盖 `api`、`fornt_admin`、`m_front`、`pc_fornt`。
- 只说“前端”而无法由上下文推断目标端时，需要先确认是管理平台、门户端还是 PC 官网。
- 前端联调以真实 API 契约为准，Mock 不能替代后端集成。
- `.codex/` 是权威来源；`.cursor/` 是可再生成的镜像，不应直接作为规则来源修改。
- 新增项目或项目组时，必须同时扩展根注册表、路由规则、仓库配置和项目文档入口。

## 修改配置后的同步

仅当修改 `.codex/README.md`、`.codex/rules/` 或 `.codex/agents/` 时，需要执行：

```bash
./scripts/sync-codex-to-cursor.sh
```

Skills 只保留在 `.codex/skills/`。这既避免重复维护，也让公开仓库的配置层次保持可读。
