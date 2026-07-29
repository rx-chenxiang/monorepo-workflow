# Monorepo Workflow

简体中文 | [English](./README.md)

Monorepo Workflow 是一个面向全栈全端开发的开源工作区模板，用来把后端 API、管理平台、移动 / H5 门户端、PC 官网、多端需求文档、编码计划和 AI Agent 工作流组织在同一个仓库中。

## 这个项目提供什么

- 通用四端工作区：后端 API、管理平台、移动 / H5 门户端、PC 官网。
- 面向 AI Agent 的口语路由规则，用于判断应该修改哪个子项目。
- 需求文档、技术设计、编码计划、模块文档、联调约定等模板。
- 兼容 Codex 和 Cursor 的规则与 Agent 定义。
- 通过 `repos.conf` 管理多个项目仓库的 clone / pull 脚本。
- 接口优先、禁止仅靠 Mock 联调的开发约束。

## 工作区结构

```text
.
├── AGENTS.md                         # Agent 与贡献者指南
├── README.md                         # 英文 README
├── README.zh-CN.md                   # 中文 README
├── api/                              # 后端 API 文档与 Agent 入口
├── fornt_admin/                      # 管理平台文档与 Agent 入口
├── m_front/                          # 移动 / H5 门户端文档与 Agent 入口
├── pc_fornt/                         # PC 官网文档与 Agent 入口
├── docs/                             # 工作区级需求与设计文档
├── .codex/                           # Codex 规则、Agent、Skills 的权威来源
├── .cursor/                          # Cursor 规则与 Agent 镜像
├── scripts/sync-codex-to-cursor.sh   # 同步 .codex 到 .cursor
├── pull_repos.sh                     # 按 repos.conf 拉取仓库
└── repos.conf                        # 仓库源配置模板
```

## 四端角色

| 项目 | 目录 | 角色 |
|------|------|------|
| 后端 API | `api/` | API 服务、鉴权、领域服务、数据访问 |
| 管理平台 | `fornt_admin/` | 面向内部运营和管理人员的后台 |
| 门户端 | `m_front/` | 面向用户的移动端、H5 或门户端 |
| PC 官网 | `pc_fornt/` | 公开官网、营销站或品牌站 |

> 说明：`fornt_admin` 和 `pc_fornt` 是当前模板保留的目录名。Agent 路由中同时记录了 `front_admin`、`pc_front` 等常见别名。

## 快速开始

克隆仓库：

```bash
git clone https://github.com/rx-chenxiang/monorepo-workflow.git
cd monorepo-workflow
```

验证拉取脚本：

```bash
bash tests/pull_repos_test.sh
```

在 `repos.conf` 中配置真实仓库后，先查看筛选结果：

```bash
./pull_repos.sh --workspace general --list
```

拉取或更新已配置仓库：

```bash
./pull_repos.sh --target-dir /path/to/workspace --workspace general
```

## 仓库配置

`repos.conf` 格式如下：

```text
[workspace_name]
[transport]git_url|branch(optional)|target_dir(optional)|project_id(optional)
```

示例：

```text
[general]
[https]https://github.com/your-org/api.git|main|api|api
[https]https://github.com/your-org/fornt_admin.git|main|fornt_admin|fornt_admin
[https]https://github.com/your-org/m_front.git|main|m_front|m_front
[https]https://github.com/your-org/pc_fornt.git|main|pc_fornt|pc_fornt
```

## 文档工作流

工作区级需求文档放在：

```text
docs/general/{需求名称}/
├── 需求文档/
├── 技术设计方案/
└── coding-plan/
```

长期代码知识维护在各子项目自己的 `docs/` 中：

```text
{project}/docs/
├── README.md
├── modules/
├── codebase/
└── rules/
```

模块模板位置：

- `api/docs/modules/_template.md`
- `fornt_admin/docs/modules/_template.md`
- `m_front/docs/modules/_template.md`
- `pc_fornt/docs/modules/_template.md`

## Agent 工作流

`.codex/` 是 AI Agent 配置的权威来源：

- `.codex/rules/project-routing.mdc`
- `.codex/rules/multi-project-workspace.mdc`
- `.codex/rules/project-workflow-api.mdc`
- `.codex/rules/project-workflow-front.mdc`
- `.codex/agents/`
- `.codex/skills/`

`.cursor/` 只镜像 `README.md`、`rules/`、`agents/`。修改 `.codex` 后运行：

```bash
./scripts/sync-codex-to-cursor.sh
```

## 联调约束

- 前端应对接真实 `api/` 契约。
- 不允许用仅 Mock 的前端行为替代真实后端联调。
- 多端需求需要说明每一端的职责边界。
- 联调假设应写入 `docs/general/workspace/联调约定.md` 或需求技术设计方案。

## 根仓库追踪什么

根仓库用于追踪：

- 工作流规则与 Agent 定义。
- 文档模板。
- 各子项目的 `AGENTS.md` 与 `docs/`。
- 仓库管理脚本。
- 工作区级需求与设计文档。

真实业务源码可以由 `api/`、`fornt_admin/`、`m_front/`、`pc_fornt/` 各自独立仓库管理。根 `.gitignore` 默认保留项目文档，忽略未登记的业务源码。

## 验证

运行：

```bash
bash tests/pull_repos_test.sh
```

期望输出：

```text
pull_repos_test.sh passed
```

## 路线图

- 增加一键初始化真实后端和前端项目的脚本。
- 增加文档链接和 `.codex` / `.cursor` 同步检查 CI。
- 增加 HTTPS / SSH 两类 `repos.conf` 示例。
- 增加贡献指南和开源许可证文件。

## 贡献

欢迎提交 Issue 和 Pull Request。请保持变更范围清晰；当公开行为变化时，同步更新中英文 README；修改 `.codex` 后请运行同步脚本更新 `.cursor`。

## 许可证

当前尚未添加 `LICENSE` 文件。正式宣传为可复用开源软件前，请先补充许可证。

<!-- AIGC:cursor|author:沉香|lines:约165|dates:2026-07|功能说明:初始化开源中文README，说明项目定位、目录结构、快速开始、文档流、Agent配置与开源注意事项 -->
