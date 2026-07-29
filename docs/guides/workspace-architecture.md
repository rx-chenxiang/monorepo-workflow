# 工作区架构

Monorepo Workflow 使用“统一协作根目录 + 独立业务仓库”的模型。根仓库保存协作资产，实际应用源码可以保留在各自的 Git 仓库中。默认四端只是起步注册表，不是项目数量上限。

## 两类资产

```text
根仓库（本仓库）
├── 协作规则：AGENTS.md、.codex/、.cursor/
├── 文档资产：docs/、四端的 AGENTS.md 与 docs/
└── 工具资产：pull_repos.sh、repos.conf、tests/

业务仓库（按需接入）
├── api/
├── fornt_admin/
├── m_front/
└── pc_fornt/
```

根目录 `.gitignore` 默认允许提交四端的 `AGENTS.md` 与 `docs/`，忽略其余未经登记的业务源码。这使协作规范可以开源复用，同时不改变业务仓库自身的版本控制边界。

## 信息流

```text
需求文档（docs/general/{需求}/）
        ↓
技术设计与编码计划
        ↓
API 契约与各端实现
        ↓
联调约定和验收结果
        ↓
各端长期模块文档（{project}/docs/）
```

- `docs/general/`：记录一次需求从规划到交付的跨端过程。
- `{project}/docs/`：记录某一项目可复用、可长期维护的实现知识。
- `docs/general/workspace/联调约定.md`：记录四端启动、代理、环境变量和验收门禁等工作区级约定。

## 目录边界

| 范围 | 主入口 | 典型内容 |
|---|---|---|
| 工作区 | `AGENTS.md`、`docs/`、`.codex/` | 角色路由、跨端文档、公共规则 |
| 后端 | `api/` | API、鉴权、领域逻辑和服务端文档 |
| 管理平台 | `fornt_admin/` | 内部运营与管理界面 |
| 门户端 | `m_front/` | 用户侧移动 / H5 / 门户体验 |
| PC 官网 | `pc_fornt/` | 公开品牌与营销体验 |

当某次改动涉及多个端时，应先明确接口与职责边界，再分别实现和验证；不要把多端改动伪装成单一项目的局部修改。

## 扩展项目与项目组

新增项目时，不需要把它塞进现有四个目录。可以新增项目组、服务端、客户端、内部工具、数据工程或自动化仓库，但必须同时维护以下入口，避免“仓库加了、协作上下文没加”：

1. 在根 `AGENTS.md` 注册项目 ID、代码目录、职责和触发别名。
2. 在 `.codex/rules/project-routing.mdc` 增加意图到项目范围的路由。
3. 在 `repos.conf` 增加对应工作区、仓库地址、目标目录和项目 ID。
4. 为新项目提供 `{project}/AGENTS.md` 与 `{project}/docs/` 索引。
5. 涉及跨项目交付时，在 `docs/general/{需求名称}/` 记录职责边界和联调约定。

```text
统一协作根仓
├── general（默认产品组）
│   ├── api
│   ├── fornt_admin
│   ├── m_front
│   └── pc_fornt
├── product_b（可选新产品组）
│   ├── service
│   └── client
└── internal（可选内部系统）
    ├── data
    └── automation
```

所有项目共享协作方式，但不要求共享技术栈、发布节奏或 Git 历史。
