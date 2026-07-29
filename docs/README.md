# 文档中心

本目录承载工作区的公开使用指南、跨项目需求交付资料和需求模板。默认四端的实现细节与长期模块知识放在各自的 `docs/` 目录中：`api/docs/`、`fornt_admin/docs/`、`m_front/docs/`、`pc_fornt/docs/`；新增项目沿用相同结构。

## 目录职责

```text
docs/
├── README.md                 # 本索引
├── guides/                   # 面向使用者与贡献者的稳定指南
├── general/                  # 按需求组织的跨端交付资料
└── _template/                # 新建需求时复制的目录骨架
```

| 目录 | 适合存放 | 不应存放 |
|---|---|---|
| `guides/` | 上手、配置、架构、协作流程 | 某次具体需求的 PRD 或临时讨论 |
| `general/{需求名称}/` | PRD、设计稿、技术设计、编码计划、联调说明 | 可跨需求复用的某端模块知识 |
| `_template/` | 新需求的空白目录骨架 | 已完成需求的实际交付内容 |
| `{project}/docs/` | 后端或单个前端长期模块知识、代码库约定 | 跨四端的需求交付过程 |

## 使用指南

- [快速开始](guides/quick-start.md)：首次接入模板与校验脚本。
- [仓库配置](guides/repository-configuration.md)：配置和使用 `repos.conf`。
- [Agent 工作流](guides/agent-workflow.md)：人和 Agent 的职责、读取顺序与同步方式。
- [工作区架构](guides/workspace-architecture.md)：目录层级、四端边界与信息流。
- [开源发布检查清单](guides/open-source-release-checklist.md)：许可证、第三方内容、GitHub 设置与首发准备。

## 跨端需求文档

每个跨端需求使用独立目录：

```text
docs/general/{需求名称}/
├── 需求文档/          # PRD、原型、设计图、附件
├── 技术设计方案/      # 模块技术规划、全栈 / 前端技术设计
└── coding-plan/       # dev-brief、编码计划、验收前置资料
```

当前项目组 ID 为 `general`，详见根目录 [AGENTS.md](../AGENTS.md)。

新建需求时复制模板：

```bash
cp -R docs/_template "docs/general/{你的需求名}"
```

请替换 `{你的需求名}`，不要创建字面目录名 `需求名称`。`docs/_template/` 只作为复制源。

## 常见落盘路径

| 产出 | 推荐路径 |
|---|---|
| PRD / 设计图 / 附件 | `docs/general/{需求名}/需求文档/` |
| 模块技术规划 | `docs/general/{需求名}/技术设计方案/{序号}-{模块}模块技术规划.md` |
| 前端技术设计 | `docs/general/{需求名}/技术设计方案/{需求名}前端技术设计文档.md` |
| 编码前置摘要 | `docs/general/{需求名}/coding-plan/{模块}-dev-brief.md` |
| 编码阶段计划 | `docs/general/{需求名}/coding-plan/{需求名}-coding.md` |
| 四端联调约定 | [general/workspace/联调约定.md](general/workspace/联调约定.md) |
