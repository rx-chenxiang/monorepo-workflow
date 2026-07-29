<div align="center">
  <h1>Monorepo Workflow</h1>
  <p><strong>面向 AI 辅助全栈、多端交付的协作操作系统。</strong></p>
  <p>在一个工作区中协调需求、API 契约、四个项目仓库、Agent 工作流、联调验收与长期文档。</p>
  <p>
    <a href="./README.md">English</a> ·
    <a href="./docs/guides/quick-start.md">快速开始</a> ·
    <a href="./docs/guides/workspace-architecture.md">工作区架构</a> ·
    <a href="./CONTRIBUTING.md">贡献指南</a>
  </p>
  <p>
    <a href="https://github.com/rx-chenxiang/monorepo-workflow/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/rx-chenxiang/monorepo-workflow/actions/workflows/ci.yml/badge.svg"></a>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-2ea44f.svg"></a>
  </p>
</div>

> 先把需求、边界与接口说清楚，再让人和 Agent 在正确的项目中实现并验证。

```text
需求 → 技术设计 → 编码计划 → API → 多端实现 → 联调 / 验收 → 文档沉淀
```

Monorepo Workflow 是一套**工作区模板和协作规范**，不是自动生成的业务系统。它适合后端和多个前端分别使用独立 Git 仓库、但仍需要统一协作上下文的团队。

## 为什么需要它

多端产品常见的问题不是缺少代码，而是缺少一致的协作上下文：需求分散、接口口径漂移、Agent 修改了错误的项目、前端长期依赖 Mock，或者实现知识在发布后丢失。

本仓库将这些问题转化为明确的目录与约束：

| 内置能力 | 带来的价值 |
|---|---|
| 四端工作区 | 用同一套协作模型协调后端、管理平台、移动 / H5 门户和 PC 官网 |
| 文档驱动交付 | 将一次需求的交付记录与项目长期知识分开维护 |
| Agent 路由 | 根据自然语言请求识别工作角色、流程与目标项目 |
| API 优先联调 | 前端使用真实后端契约，不以 Mock 代替联调 |
| 多仓库管理 | 通过 `repos.conf` 预览、拉取或更新真实业务仓库 |
| 跨工具配置 | 以 `.codex/` 为权威来源，生成受支持的 Cursor 镜像 |

## 选择接入方式

| 方式 | 适合场景 | 起点 |
|---|---|---|
| 直接作为模板 | 新建多端项目工作区 | 克隆本仓库，替换 `repos.conf` 中的示例 |
| 接入已有仓库 | 产品已经拆分为多个 Git 仓库 | 保留本仓库作为协调根仓，配置真实业务仓库地址 |
| 只采用协作资产 | 团队已有自己的 Monorepo 层级 | 按需复制并调整 `AGENTS.md`、`.codex/` 与文档模板 |

不要在同一工具中重复安装多份相同规则或 Skills。应确定唯一权威来源，并说明哪些目录由同步脚本生成。

## 快速开始

```bash
git clone https://github.com/rx-chenxiang/monorepo-workflow.git
cd monorepo-workflow

# 执行基础检查
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py

# 编辑 repos.conf 后，先预览将要操作的仓库
./pull_repos.sh --workspace general --list
```

确认列表无误后，再拉取或更新配置的业务仓库：

```bash
./pull_repos.sh --target-dir /path/to/workspace --workspace general
```

完整步骤见[快速开始指南](./docs/guides/quick-start.md)，配置格式见[仓库配置指南](./docs/guides/repository-configuration.md)。

## 工作区层级

```text
monorepo-workflow/
├── AGENTS.md              # 人类 / Agent 总入口与安全变更边界
├── .codex/                # Rules、Agents、Skills 的权威来源
├── .cursor/               # 受支持 .codex 资产的生成镜像
├── api/                   # 后端入口与长期项目文档
├── fornt_admin/           # 管理平台入口与项目文档
├── m_front/               # 移动 / H5 门户入口与项目文档
├── pc_fornt/              # PC 官网入口与项目文档
├── docs/
│   ├── guides/            # 稳定公开指南
│   ├── general/           # 跨端需求交付资料
│   └── _template/         # 新需求复制使用的文档骨架
├── scripts/               # 维护与校验脚本
└── tests/                 # 回归测试
```

根仓库追踪协作资产和项目文档，真实业务源码可以继续放在四个独立 Git 仓库中。`fornt_admin` 与 `pc_fornt` 是为兼容现有模板保留的目录名；Agent 路由同时识别 `front_admin` 与 `pc_front`。

完整的所有权边界和信息流见[工作区架构](./docs/guides/workspace-architecture.md)。

## 四端职责

| 项目 | 目录 | 职责 |
|---|---|---|
| 后端 API | `api/` | 接口、鉴权、领域服务、数据访问、异步任务 |
| 管理平台 | `fornt_admin/` | 面向运营、管理员和内部业务人员 |
| 门户端 | `m_front/` | 面向用户的移动端、H5 或门户体验 |
| PC 官网 | `pc_fornt/` | 公开官网、营销站或品牌站 |

## 文档与 Agent 工作流

| 你要做什么 | 从这里开始 |
|---|---|
| 了解人和 Agent 的执行方式 | [Agent 工作流](./docs/guides/agent-workflow.md) |
| 新建一个跨端需求 | [文档中心](./docs/README.md) |
| 配置真实业务仓库 | [仓库配置](./docs/guides/repository-configuration.md) |
| 理解项目边界 | [工作区架构](./docs/guides/workspace-architecture.md) |
| 扩展 Codex / Cursor 配置 | [.codex 说明](./.codex/README.md) |
| 准备公开发布 | [开源发布检查清单](./docs/guides/open-source-release-checklist.md) |

跨端需求文档统一放在：

```text
docs/general/{需求名称}/
├── 需求文档/
├── 技术设计方案/
└── coding-plan/
```

各端可长期复用的实现知识放在各自的 `{project}/docs/` 中，从而避免“某次需求的交付过程”和“项目长期知识”混在一起。

## 唯一事实来源

- 根目录 `AGENTS.md` 定义工作区路由、文档读取顺序和安全变更边界。
- `.codex/` 是 Rules、专用 Agents 和 Skills 的权威来源。
- `.cursor/` 是生成的兼容镜像，不是第二个手工维护入口。
- `docs/general/` 记录需求交付，`{project}/docs/` 记录长期实现知识。
- 前端必须对接真实 `api/` 契约，Mock 不能替代联调。

修改 `.codex/README.md`、`.codex/rules/` 或 `.codex/agents/` 后执行：

```bash
./scripts/sync-codex-to-cursor.sh
```

## 验证

```bash
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py
```

GitHub Actions 会通过 [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) 执行相同检查。

## 项目状态与路线图

当前仓库已提供可复用的协调层、文档体系、仓库拉取工具和 Codex / Cursor 工作流资产；它不会初始化具体业务框架，也不会部署业务服务。

后续计划：

- 增加可选的后端和前端项目初始化脚本。
- 补充仓库安全与配置边界测试。
- 为工作流变更建立版本化发布和迁移说明。
- 完善更多可复用 Agent 工作流与验收资产。

重要变更记录见 [CHANGELOG.md](./CHANGELOG.md)。

## 社区协作

欢迎提交 Issue 和 Pull Request。参与前请阅读[贡献指南](./CONTRIBUTING.md)和[行为准则](./CODE_OF_CONDUCT.md)。安全漏洞请按[安全策略](./SECURITY.md)私下报告，不要创建公开 Issue。

## 许可证

本仓库原创内容采用 [MIT License](./LICENSE)。内置或改编的第三方组件继续遵循其原始版权和许可证条款，详见 [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)。
