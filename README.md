# 通用项目工作区说明

## 当前文件说明

本仓库为 **通用项目工作区** monorepo：统一纳入后端 API、管理平台前端、门户端前端、官网前端四个子项目，便于多端协作、接口联调、需求文档沉淀与 AI Agent 调度。

> **打开方式**：请在 Cursor / VS Code / Codex 中以 **本仓库根目录**（含 `api`、`fornt_admin`、`m_front`、`pc_fornt`、`.codex`、`docs` 的目录）作为工作区根打开，勿单独只打开某个子文件夹。

## 拉取代码脚本

根目录提供 [`pull_repos.sh`](./pull_repos.sh) + [`repos.conf`](./repos.conf) 用于按配置 clone / pull 多个代码仓库。

常用命令：

```bash
# 拉取默认配置中的全部 https 仓库到指定目录
./pull_repos.sh --target-dir /Users/your-name/Documents/code

# 只拉取通用工作区
./pull_repos.sh --target-dir /Users/your-name/Documents/code --workspace general

# 只拉取某个项目仓库
./pull_repos.sh --target-dir /Users/your-name/Documents/code --project api

# 使用 SSH 配置源
./pull_repos.sh --target-dir /Users/your-name/Documents/code --transport ssh

# 先查看筛选结果，不执行 git clone / pull
./pull_repos.sh --workspace general --list
```

`repos.conf` 按 `[工作区]` 分组；仓库行格式为 `[传输方式]git_url|branch|target_dir|project_id`。当前通用模板不预置业务仓库地址，接入真实项目时按实际 Git 地址补充。

---

## 工作区概览

当前通用工作区仅保留四个子项目：

| 项目组 | 目录 | 角色 | 说明 |
|--------|------|------|------|
| **general**（通用全栈） | [api](./api/) | 后端 API | 统一承载服务端接口、鉴权、领域服务、任务队列等 |
| | [fornt_admin](./fornt_admin/) | 管理平台前端 | 面向运营 / 管理人员的后台管理平台 |
| | [m_front](./m_front/) | 门户端前端 | 面向用户的移动端、H5 或门户端 |
| | [pc_fornt](./pc_fornt/) | 官网前端 | 面向公开访问的 PC 官网或营销站点 |
| 通用 | [.codex](./.codex/) | AI 协作配置 | Agent、Skills、工作流规则（非业务代码） |
| 通用 | [docs](./docs/) | 工作区级文档 | 全栈需求、技术设计、编码计划，按 `docs/general/` 分层 |

### 口语调度（简表）

| 你说 | 范围 |
|------|------|
| **通用 / 全栈 / 全部 / 四端** | `api` + `fornt_admin` + `m_front` + `pc_fornt` |
| **后端 / API / 服务端 / 接口** | `api` |
| **管理平台 / 管理后台 / admin** | `fornt_admin` |
| **门户端 / 移动端 / H5** | `m_front` |
| **官网 / PC官网 / PC前端** | `pc_fornt` |

> `前端` 泛指三个前端子项目，未说明端别时需要先确认目标目录。完整别名见 [AGENTS.md](./AGENTS.md#口语速查)；AI 统一调度见 [`.codex/rules/project-routing.mdc`](./.codex/rules/project-routing.mdc)。

---

## 各子项目说明

### api — 通用后端 API

| 项 | 说明 |
|----|------|
| 定位 | 服务端接口、鉴权、领域服务、数据访问、异步任务等 |
| 代码目录 | [`api/`](./api/) |
| 文档入口 | [`api/docs/README.md`](./api/docs/README.md) |
| 模块索引 | [`api/docs/modules/README.md`](./api/docs/modules/README.md) |

### fornt_admin — 管理平台前端

| 项 | 说明 |
|----|------|
| 定位 | 面向内部运营、管理人员的 Web 管理平台 |
| 代码目录 | [`fornt_admin/`](./fornt_admin/) |
| 文档入口 | [`fornt_admin/docs/README.md`](./fornt_admin/docs/README.md) |
| 模块索引 | [`fornt_admin/docs/modules/README.md`](./fornt_admin/docs/modules/README.md) |

### m_front — 门户端前端

| 项 | 说明 |
|----|------|
| 定位 | 面向用户的移动端、H5、门户端体验 |
| 代码目录 | [`m_front/`](./m_front/) |
| 文档入口 | [`m_front/docs/README.md`](./m_front/docs/README.md) |
| 模块索引 | [`m_front/docs/modules/README.md`](./m_front/docs/modules/README.md) |

### pc_fornt — 官网前端

| 项 | 说明 |
|----|------|
| 定位 | 面向公开访问的 PC 官网、品牌站或营销站点 |
| 代码目录 | [`pc_fornt/`](./pc_fornt/) |
| 文档入口 | [`pc_fornt/docs/README.md`](./pc_fornt/docs/README.md) |
| 模块索引 | [`pc_fornt/docs/modules/README.md`](./pc_fornt/docs/modules/README.md) |

---

## 文档索引速查

| 用途 | 路径 |
|------|------|
| 工作区总说明 | 本文件 `README.md` |
| 工作区 AI 入口 | [AGENTS.md](./AGENTS.md) |
| 工作区需求文档 | [docs/README.md](./docs/README.md) |
| 四端联调约定 | [docs/general/workspace/联调约定.md](./docs/general/workspace/联调约定.md) |
| 后端模块索引 | [api/docs/modules/README.md](./api/docs/modules/README.md) |
| 管理平台模块索引 | [fornt_admin/docs/modules/README.md](./fornt_admin/docs/modules/README.md) |
| 门户端模块索引 | [m_front/docs/modules/README.md](./m_front/docs/modules/README.md) |
| 官网模块索引 | [pc_fornt/docs/modules/README.md](./pc_fornt/docs/modules/README.md) |
| 多端协作规则 | [.codex/rules/multi-project-workspace.mdc](./.codex/rules/multi-project-workspace.mdc) |
| 禁止前端 Mock | [.codex/rules/api-first-no-mock.mdc](./.codex/rules/api-first-no-mock.mdc) |
| Codex / Cursor 同步脚本 | [scripts/sync-codex-to-cursor.sh](./scripts/sync-codex-to-cursor.sh) |

<!-- AIGC:cursor|author:沉香|lines:约3|dates:2026-07|功能说明:工作区文档索引补充四端联调约定与Codex到Cursor同步脚本入口 -->
<!-- AIGC:cursor|author:沉香|lines:约120|dates:2026-07|功能说明:工作区说明初始化为通用四端版本，仅保留api、fornt_admin、m_front、pc_fornt四个子项目入口 -->
