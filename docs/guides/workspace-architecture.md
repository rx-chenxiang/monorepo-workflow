# 工作区架构

Monorepo Workflow 使用“统一协作根目录 + 独立业务仓库”的模型。根仓库保存协作资产，实际应用源码可以保留在各自的 Git 仓库中。

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
