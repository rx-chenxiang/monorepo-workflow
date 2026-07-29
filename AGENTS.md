# 通用项目工作区 · 项目注册表

### 通用规则

1. 叫我沉香帅哥
2. 总是用简体中文回答与注释
3. 编码时，请补充完整注释与当前文件说明
5. 在代码实现时，符合"KISS原则"和"SOLID原则"
6. 确保代码可读性，为每一处添加标准的中文注释说明
7. 代码变更范围最小化，避免修改公共组件、全局状态
8. 实现后进行基本逻辑自检，确保状态管理与生命周期正确
9. 如有疑问，先询问再修改，不要擅自改变原有设计
10. 对生成的代码按照生成行数每次都添加AIGC注释 不要修改或删除以往注释  新增代码行数不要超过生成行数与页面最大行数 示例为  AIGC:cursor|author:沉香|lines:如200(说明:本次新增代码数)|dates:2025-11 功能说明


## 当前文件说明

本文件**仅存放通用项目名称、别名与目录映射**，作为 AI 与人类共用的「项目是谁」速查表。

具体规则请读项目内对应文件，勿在本文件重复维护。Codex 执行任务时，按本表读取 `.codex/rules/` 下对应的 `.mdc` 或 `.md` 规则文件。

| 用途 | 路径 |
|------|------|
| 口语 → 代码范围路由 | `.codex/rules/project-routing.mdc` |
| 多端协作与联调 | `.codex/rules/multi-project-workspace.mdc` |
| 接口优先与禁止 Mock | `.codex/rules/api-first-no-mock.mdc` |
| 产品 workflow | `.codex/rules/project-workflow-product.mdc` |
| 后端 workflow | `.codex/rules/project-workflow-api.mdc` |
| 前端 workflow | `.codex/rules/project-workflow-front.mdc` |
| 设计 workflow | `.codex/rules/project-workflow-ui.mdc` |
| 测试 workflow | `.codex/rules/project-workflow-test.mdc` |
| 代码审查规则 | `.codex/rules/code-review.md` |
| 安全规则 | `.codex/rules/security.md` |
| 子目录规则优先级 | `.codex/rules/subdir-rule-priority.mdc` |
| Agent / Skill 索引 | `.codex/README.md` |
| 需求文档目录说明 | `docs/README.md` |
| 工作区总说明 | `README.md` |

---

## 口语速查

### 项目范围（改哪里的代码）

| 你说 | 范围 |
|------|------|
| **通用 / 全栈 / 全部 / 四端 / 整个项目** | 四端：`api` + `fornt_admin` + `m_front` + `pc_fornt` |
| **后端 / API / 服务端 / 接口** | 后端：`api` |
| **管理平台 / 管理后台 / admin / fornt_admin** | 管理平台前端：`fornt_admin` |
| **门户端 / 移动端 / H5 / m_front** | 门户端前端：`m_front` |
| **官网 / PC官网 / PC前端 / pc_fornt** | 官网前端：`pc_fornt` |
| **某子项目专属别名**（如 `api`、`fornt_admin`、`m_front`、`pc_fornt`） | 仅该子项目目录 |

> **泛指词消歧**：`前端` 同时可能指管理平台、门户端或官网；未携带端别时，按 `project-routing.mdc` 第一步 D「一句话确认」。`后端`、`API` 默认指向唯一后端目录 `api/`。

调度规则：`.codex/rules/project-routing.mdc`（alwaysApply）。

### 工作角色（做什么）

| 你说 | workflow 规则 | 主要 docs |
|------|--------------|-----------|
| **产品 / PRD / 需求 / 技术规划** | `project-workflow-product.mdc` | `docs/general/{需求名称}/需求文档/`、`docs/general/{需求名称}/技术设计方案/` |
| **设计 / UI / 原型 / 交互** | `project-workflow-ui.mdc` | `docs/general/{需求名称}/需求文档/` |
| **测试 / E2E / 验收 / 回归** | `project-workflow-test.mdc` | 先匹配子项目 → `AGENTS.md`、`docs/README.md` 与实际存在的自测/回归文档 |
| **写接口 / Laravel / Domain / Controller / Service** | `project-workflow-api.mdc` | `docs/general/{需求名称}/技术设计方案/`、`api/AGENTS.md` → `api/docs/README.md` → 模块索引实际链接文件 |
| **写页面 / Vue / 管理端 / 门户端 / 官网** | `project-workflow-front.mdc` | `docs/general/{需求名称}/技术设计方案/`、先匹配前端目录 → `{frontRoot}/docs/modules/README.md` 的实际链接文件 |

> **docs 目录约定**：根目录 `docs/` 按 `docs/general/{需求名称}/` 分层组织，每个需求下含三个子目录：  
> `需求文档/`（PRD）、`技术设计方案/`（技术方案）、`coding-plan/`（api-developer / front-developer 编码计划输出）。  
> 模块级代码文档维护在各子项目实体目录内；命中子项目后，先 Read `{代码目录}AGENTS.md`（存在时）与 `{代码目录}docs/README.md`，再按其 `docs/rules/`、`docs/modules/`、`docs/codebase/` 和 `docs/skills/` 索引加载任务所需上下文。

### 子项目文档优先级

命中任一已注册子项目别名或改动路径位于其 `{代码目录}` 时，在读取根 `.codex/rules/` 对应 workflow 后，优先加载该子项目内版本化文档；文件或目录不存在时跳过，不得臆造路径。

1. `{代码目录}AGENTS.md`：项目边界、检索方式与验证入口。
2. `{代码目录}docs/README.md`：项目文档总索引与各目录职责。
3. `{代码目录}docs/rules/`：优先读取冷启动、核心规则及与本次任务匹配的专项规则。
4. `{代码目录}docs/modules/README.md`：业务别名、模块映射与代码路径；具体模块文档以索引实际链接为准，不得假定统一文件名或目录结构。
5. `{代码目录}docs/codebase/` 与 `{代码目录}docs/skills/`：按任务读取复杂业务专题、运维 SOP 和领域 workflow。

涉及 HTTP 接口时，按子项目 `docs/codebase/` 中实际存在的鉴权/API 文档补充上下文；编码完成后，按实际存在的自测或回归文档执行验证。

---

## 项目注册表

扩展别名或新项目时，**同步更新本节**与 `.codex/rules/project-routing.mdc`「别名速查」。

### 项目组：general

| 字段 | 值 |
|------|-----|
| **项目组 ID** | `general` |
| **显示名** | 通用业务系统（全栈四端） |
| **包含子项目** | `api`（后端）+ `fornt_admin`（管理平台前端）+ `m_front`（门户端前端）+ `pc_fornt`（官网前端） |

**触发别名**（任一说辞即命中 general 项目组）：

`general`、`通用`、`通用项目`、`全栈`、`全部`、`四端`、`整个项目`、`前后端`、`多端`

### 子项目：api

| 字段 | 值 |
|------|-----|
| **子项目 ID** | `api` |
| **显示名** | 通用后端 API |
| **代码目录** | `api/` |
| **技术栈** | 按实际项目初始化；默认按后端 API 服务识别 |

**触发别名**：`api`、`后端`、`API`、`接口`、`服务端`、`server`

### 子项目：fornt_admin

| 字段 | 值 |
|------|-----|
| **子项目 ID** | `fornt_admin` |
| **显示名** | 通用管理平台前端 |
| **代码目录** | `fornt_admin/` |
| **技术栈** | 按实际项目初始化；默认按 Web 管理端识别 |

**触发别名**：`fornt_admin`、`front_admin`、`管理平台`、`管理后台`、`后台前端`、`admin`

### 子项目：m_front

| 字段 | 值 |
|------|-----|
| **子项目 ID** | `m_front` |
| **显示名** | 通用门户端前端 |
| **代码目录** | `m_front/` |
| **技术栈** | 按实际项目初始化；默认按移动端 / H5 / 门户端识别 |

**触发别名**：`m_front`、`门户端`、`移动端`、`H5`、`h5`、`C端`、`用户端`

### 子项目：pc_fornt

| 字段 | 值 |
|------|-----|
| **子项目 ID** | `pc_fornt` |
| **显示名** | 通用官网前端 |
| **代码目录** | `pc_fornt/` |
| **技术栈** | 按实际项目初始化；默认按 PC 官网 / 官网前端识别 |

**触发别名**：`pc_fornt`、`pc_front`、`官网`、`PC官网`、`PC前端`、`官网前端`

<!-- AIGC:cursor|author:沉香|lines:约135|dates:2026-07|功能说明:初始化通用版本项目注册表，仅保留api、fornt_admin、m_front、pc_fornt四端目录与口语路由 -->
