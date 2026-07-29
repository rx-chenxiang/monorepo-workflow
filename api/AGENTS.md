# api · 后端 API 子项目说明

## 当前文件说明

本文件说明 `api/` 子项目的职责边界、文档入口与 Agent 读取顺序。`api/` 是通用工作区唯一后端服务目录，承载接口、鉴权、领域服务、数据访问、异步任务等服务端能力。

## 子项目边界

| 项 | 说明 |
|----|------|
| 子项目 ID | `api` |
| 角色 | 后端 API |
| 代码目录 | `api/` |
| 根规则 | `../.codex/rules/project-workflow-api.mdc` |
| 文档入口 | `docs/README.md` |

## Agent 读取顺序

1. 先读根目录 `../AGENTS.md`，确认本次任务是否只命中 `api`。
2. 再读本文件，确认后端边界。
3. 继续读 `docs/README.md`、`docs/modules/README.md` 与任务相关专题。
4. 编码完成后，按实际变更同步模块文档或专题文档。

<!-- AIGC:cursor|author:沉香|lines:约28|dates:2026-07|功能说明:新增通用后端api子项目Agent入口说明 -->
