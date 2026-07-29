---
name: coding-agent-team-fullstack
description: >-
  全栈实现流水线（设计文档就绪后直接执行）：
  阶段零 按 AGENTS.md 识别项目组与子项目 →
  阶段一 api-developer 后端接口开发 →
  阶段二 接口验证 + 数据库测试数据注入（禁止前端 Mock）→
  阶段三 front-developer 管理端编码 →
  阶段四 doc-updater 文档同步 →
  阶段五汇总交付。
  触发：coding-agent-team-fullstack、全栈开发流水线、前后端一体开发、或设计文档已就绪需后端先行再管理端；
  适用于 bss / tiku / agency 等已注册项目组（见 AGENTS.md）。
---

# Coding Agent Team Fullstack（全栈实现阶段团队编排）

## 何时使用

用户**已完成需求分析与技术设计**，`{需求文档根}` 下技术设计方案与 coding-plan 已落盘，并明确触发本技能名称，或说明「后端先行、再管理端」。

- **范围**：`AGENTS.md` 已注册的**项目组双端**（后端子项目 + 配对管理端前端），无移动端客户端。
- **调度**：用户说项目组别名（如 bss / 题库中心 / 代理商系统）且需双端交付时，默认走本技能（见 `.codex/rules/project-routing.mdc`）。
- **不适用**：用户明确仅改一端 → 直接委派 `api-developer` 或 `front-developer`，勿强行走全栈流水线。

**流水线**：后端开发 → 接口验证 + 库表测试数据 → 管理端编码 → 文档同步 → 汇总交付

---

## 第零步：项目与范围识别（必须最先）

与 `api-developer`、`front-developer`、`doc-updater`、`requirements-to-tech-doc` 及 `project-routing.mdc` 一致：

```
用户表述 / @ 引用 / 当前改动路径
    ↓ Read AGENTS.md「项目注册表」+ project-routing.mdc
    ↓ 命中项目组别名且未单端限定 → 项目组双端
    ↓ 从项目组「包含子项目」绑定后端 {子项目ID}/{代码目录} 与前端 {frontId}/{frontRoot}
    ↓ 解析 {需求名称}（用户明说 / @docs/{项目组ID}/… / 设计文档路径推断）
    ↓ 未命中项目组或需求名含糊 → 一句话确认后再进入阶段一
```

### 占位符（识别成功后全程使用）

| 占位符 | 含义 |
|--------|------|
| `{项目组ID}` | `AGENTS.md` 项目组 ID（如 `bss`、`tiku`、`agency`） |
| `{需求名称}` | 与 `docs/{项目组ID}/` 下目录名一致 |
| `{需求文档根}` | `docs/{项目组ID}/{需求名称}/` |
| `{子项目ID}` / `{代码目录}` | 后端子项目 ID 与代码根（含尾斜杠） |
| `{frontId}` / `{frontRoot}` | 管理端子项目 ID 与代码根（含尾斜杠） |
| `{后端模块文档}` | `{代码目录}docs/modules/` 下由实际索引链接到的文档 |
| `{前端模块文档}` | `{frontRoot}docs/modules/` 下由实际索引链接到的文档 |
| `{项目文档}`（后端/前端） | `{代码目录}AGENTS.md`、`{代码目录}docs/README.md` / `{frontRoot}AGENTS.md`、`{frontRoot}docs/README.md` |
| `{Domain}` / `{模块名}` | 本次改动的后端域与前端模块（来自技术设计或 workflow 映射） |

需求文档三层结构见 [docs/README.md](../../../docs/README.md)：`{需求文档根}需求文档/`、`技术设计方案/`、`coding-plan/`。

### 已注册项目组来源

本技能不维护项目组速查表。所有项目组、子项目、别名与代码目录均从根 `AGENTS.md`「项目注册表」读取；扩展新项目组时只更新注册表，本技能沿用占位符和阶段逻辑。

---

## 总原则

1. **前置条件**：进入阶段一前，确认 `{需求文档根}技术设计方案/` 与 `{需求文档根}coding-plan/`（含 dev-brief，双端**强制**）已落盘。
2. **顺序依赖**：阶段二在阶段一验证通过后执行；阶段三在阶段二完成后执行；阶段四在阶段三完成后执行。
3. **上下文打包**：委派子代理时 `prompt` 须含：`{项目组ID}`、`{需求名称}`、`{需求文档根}`、改动范围、`.codex/rules` 禁忌。
4. **规范优先级**：`.codex/rules`、`api-first-no-mock.mdc`、已识别子项目的 `{项目文档}` 与 README。
5. **测试数据**：仅允许真实接口 + 数据库写入；**禁止**前端 Mock、拦截器假数据。
6. **子项目差异**：路由前缀、鉴权、目录树、禁止改动的核心文件均以各端 `{项目文档}` 为准，**禁止**将某一子项目约定默认套用到其他组。

---

## 阶段一：后端接口开发（委派 `api-developer`）

### 前置条件检查

- `{需求文档根}技术设计方案/`（实体/接口/路由说明）
- `{需求文档根}coding-plan/{需求名称}-coding.md` 或 `{模块}-dev-brief.md`（双端须有 dev-brief）
- 目标代码范围以 `{项目文档}` / `CODEBASE.md` 为准（常见：`{代码目录}app/Services/{Domain}/`、Controller、`routes/` 下管理端路由文件）

若缺失，**停止流水线**，提示用户先走 `requirements-to-tech-doc` 或人工补全设计文档。

### 如何调用

| 属性 | 值 |
|-----|---|
| `subagent_type` | `api-developer` |

**`prompt` 必须包含**：

- `{项目组ID}`、`{需求名称}`、业务目标
- **必读**：`{需求文档根}技术设计方案/`、`{后端模块文档}`、`.codex/rules/project-workflow-api.mdc`
- **禁止套用**：其他项目组的「业务别名 → Domain」映射表（如 bss 大表不可用于 `tiku_center_api`）
- 接口清单：Controller@action、Service 方法、鉴权层级（以 `{项目文档}` 为准）
- 实现范围与验收标准
- **工程约束**：遵守 `{代码目录}` 分层；禁止改动项见 `{项目文档}`（如中间件链、多库连接配置等）

### 主会话收尾

暂存：接口清单、变更文件、表名与关键字段、管理端路由前缀、未决风险。

---

## 阶段二：接口验证 + 数据库测试数据注入

> 必须在阶段一**完全通过**后执行。由主会话或具备 Shell/接口调用能力的 Agent 执行，不委派 front-developer。

### 目标

1. 验证新增/修改接口可正常响应（路由前缀与入口文件见 `{项目文档}`，如 `web_api`、`/api/` 等）。
2. 通过**真实接口**或受控 SQL/Seeder 写入测试数据，保证联调表有足够样本（状态枚举、分页场景）。

### 与 api-first-no-mock 的关系

| 允许 | 禁止 |
|------|------|
| 数据库种子、调用真实业务写入接口 | 前端本地 Mock、axios 伪造响应 |
| 开发环境约定的 Debug/绕过方式（若 `{项目文档}` 允许） | 用假 JSON 代替未就绪后端 |

### 验证检查清单

```
接口验证：
- [ ] 新增路由可访问，状态码与契约一致
- [ ] 列表/详情/更新/删除（若有）链路通
- [ ] 鉴权方式符合设计（JWT / 签名 / Session 等，见 {项目文档}）

测试数据：
- [ ] 关键表有足够联调数据（建议 ≥5 条，分页场景 ≥15 条）
- [ ] 状态枚举均有样本
- [ ] 外键关联 ID 有效
```

---

## 阶段三：管理端编码（委派 `front-developer`）

> 必须在阶段二完成后执行。

| 属性 | 值 |
|-----|---|
| `subagent_type` | `front-developer` |

**`prompt` 必须包含**：

- `{项目组ID}`、`{需求名称}`、`{需求文档根}` 路径
- **必读**：`{前端模块文档}`、`{后端模块文档}` §4（或技术设计中的接口表）
- 阶段一接口清单（路径、前端 API 封装函数名、入参要点）
- 实现范围：views、路由、API 层、组件复用（具体目录见 `{frontRoot}` `{项目文档}`）
- **工程约束**：不修改 `{项目文档}` 标明的请求/加密/鉴权核心文件；路由注册方式见 `{frontRoot}` 约定；**禁止 Mock**

---

## 阶段四：文档同步（委派 `doc-updater`）

> 阶段三子代理返回后执行。

| 属性 | 值 |
|-----|---|
| `subagent_type` | `doc-updater` |

**`prompt` 须包含**：

- `{项目组ID}`、`{需求名称}`、后端/前端变更文件清单
- 需更新：命中后端子项目实际 `{代码目录}docs/modules/` 文档；命中前端子项目实际 `{frontRoot}docs/modules/` 文档
- 新 Domain/模块时同步命中子项目 `docs/README.md`、`docs/modules/README.md`；仅当注册表或调度映射变化时更新 `AGENTS.md` 与 `project-workflow-*.mdc`
- 架构级变更是否涉及 `{代码目录}docs/codebase/`（若该子项目存在该体系）
- 业务范围变化时修订 `{需求文档根}技术设计方案/` 差量（若需要）

---

## 阶段五：汇总交付

向用户输出（简体中文），**将占位符替换为本次实际子项目名**：

1. **后端**（`{子项目ID}`）：接口清单、Domain/模块、关键逻辑
2. **测试数据**：各表样本数量与注意点
3. **管理端**（`{frontId}`）：页面/API 变更、本地验证步骤（启动命令与代理前缀见 `{frontRoot}` README / `{项目文档}`）
4. **文档**：已更新的 `{后端模块文档}`、`{前端模块文档}`、`{需求文档根}` 文件列表
5. **待办**：跨端未关闭项、待确认接口字段

---

## 反模式（勿做）

- 未识别 `{项目组ID}` / `{需求名称}` 即开始编码
- 设计文档未落盘直接编码
- 接口未通就启动前端，或用 Mock 顶替
- 测试数据仅用 `test1/test2` 无业务含义
- 虚构字段或偏离 Apifox / 模块文档 §4
- 将 bss 的 Domain 映射或目录约定硬套到 tiku / agency

---

## 附加参考

- 子代理：`.codex/agents/api-developer.md`、`.codex/agents/front-developer.md`、`.codex/agents/doc-updater.md`
- 需求转文档：`.codex/skills/requirements-to-tech-doc/SKILL.md`
- 项目注册与别名：根目录 `AGENTS.md`
- 口语路由：`.codex/rules/project-routing.mdc`
- 双端协作：`.codex/rules/multi-project-workspace.mdc`

<!-- AIGC:cursor|author:沉香|lines:约175|dates:2026-06|功能说明:全栈流水线泛化——第零步占位符识别项目组/子项目/需求文档根，五阶段路径与约束改为docs/{项目组ID}/与{代码目录}/{frontRoot}，移除ahyk_bss/bss_front硬编码，附bss/tiku/agency速查表 -->
<!-- AIGC:cursor|author:沉香|lines:约20|dates:2026-07|功能说明:全栈流水线文档同步阶段改为注册表命中的子项目实体docs口径，移除项目组速查表与规则侧docs/{id}/modules强制同步 -->
