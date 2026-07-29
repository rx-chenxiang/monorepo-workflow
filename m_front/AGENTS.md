# m_front · 门户端前端子项目说明

## 当前文件说明

本文件说明 `m_front/` 子项目的职责边界、文档入口与 Agent 读取顺序。`m_front/` 是通用工作区的门户端前端目录，面向用户侧移动端、H5 或门户体验。

## 子项目边界

| 项 | 说明 |
|----|------|
| 子项目 ID | `m_front` |
| 角色 | 门户端前端 |
| 代码目录 | `m_front/` |
| 根规则 | `../.codex/rules/project-workflow-front.mdc` |
| 文档入口 | `docs/README.md` |

## Agent 读取顺序

1. 先读根目录 `../AGENTS.md`，确认本次任务是否命中门户端。
2. 再读本文件，确认门户端边界。
3. 继续读 `docs/README.md`、`docs/modules/README.md` 与任务相关专题。
4. 编码完成后，按实际变更同步模块文档或专题文档。

<!-- AIGC:cursor|author:沉香|lines:约28|dates:2026-07|功能说明:新增m_front门户端前端Agent入口说明 -->
