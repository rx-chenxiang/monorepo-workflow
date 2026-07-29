---
name: requirements-to-tech-doc
description: >-
  将原始需求（设计图、PRD、口头描述）转换为便于 Agent 与开发者读取的结构化技术文档，
  对齐本仓库 docs/ 体系与 .codex/rules 模块映射。产出模块技术规划、双端模块文档骨架或编码前置摘要。
  下游衔接 api-developer / front-developer / coding-agent-team-fullstack / doc-updater。
  触发：需求转技术文档、写技术规划、整理需求、模块技术方案、编码前文档准备、
  或用户 @docs/{项目组ID}/{需求名称} 要求产出可开发文档时。
---

# 需求 → 技术文档转换

## 何时使用

| 场景 | 使用本技能 | 下游（勿在本技能内写代码） |
|------|-----------|---------------------------|
| 原始需求 / 设计图 → 结构化技术规划 | ✅ | — |
| 单功能前端编码设计（§1～§5 + Apifox 表） | 先本技能整理输入 | `writing-tech-design-doc` |
| 技术规划已就绪 → **仅后端**编码 | 本技能产出规划 / dev-brief 后 | `@.codex/agents/api-developer.md`（`api-developer`） |
| 技术规划已就绪 → **仅管理端**编码 | 同上 | `@.codex/agents/front-developer.md`（`front-developer`） |
| 技术规划已就绪 → **项目组双端**编码 | 同上 | `coding-agent-team-fullstack`（内部分别委派 `api-developer` → `front-developer` → `doc-updater`） |
| 代码已写完，文档与实现对齐 | ❌ | `@.codex/agents/doc-updater.md`（`doc-updater`） |

> **边界**：本技能只产出/修订**需求与设计层**文档；模块文档 §3～§6 的「代码现状」由开发 Agent 或 `doc-updater` 以代码为准维护。

---

## 核心原则

1. **文档服务编码**：表格优先、路由/API/表结构可检索，避免散文式 PRD 复述。
2. **双端一致**：模块名与 `project-workflow-api` / `project-workflow-front` 映射表对齐，禁止自造模块名。
3. **不虚构接口**：无 Apifox / 后端文档时标「待确认」，列出待办而非编造字段。
4. **渐进落盘**：先模块技术规划 → 按需补双端模块文档骨架 → 单功能再拆前端技术设计。
5. **实体文档优先**：模块级代码文档以注册表命中的 `{代码目录}docs/modules/` 或 `{frontRoot}docs/modules/` 为准；根 `docs/{项目组ID}/` 只承载需求、技术设计和 coding-plan。

---

## 第零步：项目与范围识别（必须最先）

与 `api-developer`、`front-developer`、`doc-updater` 及 `project-routing.mdc` 一致：

```
用户表述 / @ 引用 / 设计图目录
    ↓ Read AGENTS.md「项目注册表」+ project-routing.mdc
    ↓ 判定范围：仅后端 / 仅前端 / 项目组双端（从 AGENTS.md 注册表读取 `{项目组ID}`）
    ↓ 绑定占位符（双端时同时绑定后端 + 前端两套）
    ↓ 未命中 → 一句话确认子项目与范围后再撰写
```

### 占位符（识别成功后全程使用）

| 占位符 | 含义（后端） | 含义（前端） |
|--------|-------------|-------------|
| `{子项目ID}` / `{frontId}` | 后端子项目 ID（见 AGENTS.md） | 管理端子项目 ID（见 AGENTS.md） |
| `{代码目录}` / `{frontRoot}` | 后端代码根目录，如 `{子项目ID}/` | 前端代码根目录，如 `{frontId}/` |
| `{模块文档}` | `{代码目录}docs/modules/README.md` 实际链接到的 Domain 文档 | `{frontRoot}docs/modules/README.md` 实际链接到的模块文档 |
| `{项目文档}` | `{代码目录}AGENTS.md`、`{代码目录}docs/README.md` 及实际存在的子项目 docs | `{frontRoot}AGENTS.md`、`{frontRoot}docs/README.md` 及实际存在的子项目 docs |
| `{项目组ID}` | 工作区项目组 ID（AGENTS.md「项目注册表」） | 同左 |
| `{需求文档根}` | `docs/{项目组ID}/{需求名称}/` | 同左 |

技术规划与 dev-brief 中写路径时：**只写注册表命中的子项目实体 docs 路径**（开发 Agent 编码前必读）。需求文档目录约定见 [docs/README.md](../../../docs/README.md)。

---

## 第一步：采集输入（按序）

1. **用户材料**：需求文本、范围边界、优先级、排期约束。
2. **设计资产**：`{需求文档根}需求文档/**` 下图片/原型；Read 图片提取页面、字段、交互、状态。
3. **已有文档**：
   - 同需求 `{需求文档根}技术设计方案/*.md`
   - 编码计划 `{需求文档根}coding-plan/*.md`
   - 双端 `{模块文档}`（后端 Domain / 前端模块，避免与规划冲突）
4. **项目规则**（必读）：
   - 根目录 `AGENTS.md`
   - `.codex/rules/project-routing.mdc`
   - `.codex/rules/multi-project-workspace.mdc`
   - 范围含后端 → `.codex/rules/project-workflow-api.mdc`
   - 范围含前端 → `.codex/rules/project-workflow-front.mdc`
5. **接口来源**（可选）：Apifox MCP、`{模块文档}` §4

规则、规划与已有实现冲突时，**以代码与 `{项目文档}` 为准**，在「待确认事项」说明。

---

## 第二步：识别模块与 Domain

按范围 **Read** 对应 workflow 的「业务别名 → Domain/模块」映射表（勿在本技能内维护大表）：

```
用户表述 → 后端 {Domain}、前端 {模块名}
         → 范围：仅后端 / 仅前端 / 双端
         → 已有技术规划路径（如有）
         → 设计图目录 `{需求文档根}需求文档/` …
```

双端需求须**分别**定位 `{Domain}` 与 `{模块名}`，并在技术规划 §4/§5 与双端模块文档骨架中可互相对照。

---

## 第三步：选择产出类型

详见 [output-routing.md](output-routing.md)。默认优先级：

| 优先级 | 产出 | 路径 |
|--------|------|------|
| P0 | **模块技术规划**（全栈首选） | `{需求文档根}技术设计方案/{序号}-{模块}模块技术规划.md` |
| P1 | 双端模块文档骨架（新模块或「规划中」） | 命中子项目实体 `{代码目录}docs/modules/` / `{frontRoot}docs/modules/` |
| P1 ⚠️ | **编码前置摘要**（双端范围**强制**，单端推荐） | 同目录 `{模块}-dev-brief.md` |
| P3 | 单功能前端技术设计 | 委托 `writing-tech-design-doc` |

用户指定路径或文档类型时从其约定。

---

## 第四步：撰写模块技术规划

骨架见 [reference-template-tech-planning.md](reference-template-tech-planning.md)。**一级章节固定 §1～§11**（管理端需求可简写原「客户端」相关节为「不涉及」或改为 `{frontRoot}` 页面表）。

规划中须显式写出：**范围（仅后端/仅前端/双端）**、配对 `{Domain}` ↔ `{模块名}`、以及下游建议委派的 Agent（见下文第七节）。

---

## 第五步：双端模块文档骨架（按需）

新模块或 frontmatter `状态: 规划中` 时，从命中子项目实际 `_template.md` 复制并预填：

| 端 | 模板（实体） | 预填内容 |
|----|-------------|---------|
| 后端 | `{代码目录}docs/modules/_template.md` | §3 表、§4 接口（与技术规划 §4/§5 一致） |
| 管理端 | `{frontRoot}docs/modules/_template.md` | §3 页面、§4 API（路径须与规划及后端 §4 可对照） |

同步更新：

- `{代码目录}docs/README.md`、`{代码目录}docs/modules/README.md` 索引
- `{frontRoot}docs/README.md`、`{frontRoot}docs/modules/README.md` 索引
- **新增后端 Domain**：仅当影响全局调度或别名识别时，更新根 `AGENTS.md` 或 `.codex/rules/project-workflow-api.mdc`

骨架阶段 §4 可标「待实现」；**禁止**编造未确认字段。实现后由 `api-developer` / `front-developer` 或 `doc-updater` 按代码刷新 §3～§6。

---

## 第六步：编码前置摘要（双端范围**强制**；单端推荐）

路径：`{需求文档根}coding-plan/{模块}-dev-brief.md`

```markdown
# {模块} 编码前置摘要

## 范围与子项目
- 范围：仅后端 / 仅前端 / 双端
- 后端：{子项目ID}、{代码目录}
- 前端：{frontId}、{frontRoot}

## 必读（开发 Agent 第一步）
- 技术规划：{相对路径}
- 后端模块文档：{模块文档}
- 管理端模块文档：{模块文档}
- 后端编码规范：{项目文档}（后端）
- 前端编码规范：{项目文档}（前端）
- workflow：project-workflow-api.mdc / project-workflow-front.mdc（按范围）

## 本轮范围
- 必须做：…
- 不做：…

## 接口清单（摘要）
| 路径 | 方法 | 说明 | 鉴权层级 |

## 待确认
- [ ] …

## 建议委派
- 仅后端：@.codex/agents/api-developer.md
- 仅前端：@.codex/agents/front-developer.md
- 双端：coding-agent-team-fullstack（或按 SOP 顺序 api-developer → front-developer → doc-updater）
```

---

## 第七节：下游开发 Agent 衔接

本技能落盘后，按**范围**选择（用户未缩小时：若命中 AGENTS.md 中**双端项目组**则默认双端，否则按识别结果）：

| 范围 | 推荐下一步 | Agent 定义文件 |
|------|-----------|----------------|
| 仅后端 | 用户确认规划后，委派后端开发 | `.codex/agents/api-developer.md` |
| 仅前端 | 用户确认规划后，委派管理端开发 | `.codex/agents/front-developer.md` |
| 项目组双端 | `coding-agent-team-fullstack`（设计文档路径 + dev-brief 须写入委派 prompt） | 阶段一/三/四见 `.codex/skills/coding-agent-team-fullstack/SKILL.md` |
| 任意端编码结束 | 开发 Agent 已同步 §3～§6 时可跳过；否则批量对齐 | `.codex/agents/doc-updater.md` |

**委派 prompt 最少包含**（与三个 Agent 一致）：需求名称、范围、必读技术规划与 `{模块文档}` 路径、接口/页面清单、`.codex/rules/api-first-no-mock.mdc` 约束。

**勿在本技能会话内**：直接改 `{代码目录}`、`{frontRoot}` 下业务代码；那是 `api-developer` / `front-developer` 的职责。

---

## 质量自检

- [ ] 已 Read `AGENTS.md` 并完成范围识别（仅后端 / 仅前端 / 双端）
- [ ] 模块名 / Domain 与两份 `project-workflow-*.mdc` 映射表一致
- [ ] §4 数据模型与 `{代码目录}` 下目标 Domain Models 方向一致（或已标待确认）
- [ ] §5 API 区分 webApi（`/web_api/`）与 api 签名路由，无依据接口已标待确认
- [ ] 双端规划：后端 §4 与前端 §4（骨架）路径可对照
- [ ] P1 骨架已写入注册表命中的子项目实体 docs 路径
- [ ] 已列出「待确认事项」
- [ ] 文件已写入约定路径
- [ ] **双端范围**：dev-brief 已落盘（强制）；单端范围：dev-brief 已落盘或已说明跳过原因
- [ ] 交付回复末尾已输出「交接就绪检查单」（G1～G5）

---

## 交付回复格式

1. **范围与子项目**：仅后端 / 仅前端 / 双端；`{子项目ID}`、`{frontId}` 等
2. **产出清单**：路径 + 一句话说明（使用注册表命中的子项目实体 docs 路径）
3. **模块映射**：`{Domain}` ↔ `{模块名}`、涉及子项目
4. **待确认事项**：编号列表
5. **建议下一步**（示例）：
   - 双端：「确认后运行 `coding-agent-team-fullstack`，或依次 `@api-developer` → `@front-developer`」
   - 仅后端：「确认后 `@.codex/agents/api-developer.md`」
   - 仅文档落后：「`@.codex/agents/doc-updater.md`」

---

## 交接就绪检查单（必须在交付回复末尾输出）

> 每次文档落盘后，Agent **必须**在回复最后输出如下检查单，供用户确认后再触发编码阶段。
> 用户回复「确认」或「开始编码」后，才视为满足 `coding-agent-team-fullstack` 门禁 G4。

```
## ✅ 文档就绪检查单

| 项 | 状态 | 说明 |
|----|------|------|
| G1 项目范围 | ✅ / ⚠️ 待确认 | 仅后端 / 仅前端 / 双端 |
| G2 技术规划落盘 | ✅ / ❌ 缺失 | 路径：`{需求文档根}技术设计方案/xxx.md` |
| G3 Domain/模块名映射 | ✅ / ❌ 未找到 | {Domain} ↔ {模块名} |
| G4 用户确认 | ⏳ 等待您确认 | 确认规划内容无误后，回复「确认」 |
| G5 范围边界 | ✅ / ⚠️ 待补充 | 包含：… / 不包含：… |

> 全部 ✅ 后，可触发编码阶段：
> - 双端：`coding-agent-team-fullstack`
   > - 仅后端：`@.codex/agents/api-developer.md`
   > - 仅前端：`@.codex/agents/front-developer.md`
```

---

## 参考

- 骨架：[reference-template-tech-planning.md](reference-template-tech-planning.md)
- 产出路由：[output-routing.md](output-routing.md)
- 开发 Agent：`.codex/agents/api-developer.md`、`.codex/agents/front-developer.md`、`.codex/agents/doc-updater.md`
- 全栈编排：`.codex/skills/coding-agent-team-fullstack/SKILL.md`

<!-- AIGC:cursor|author:沉香|lines:约95|dates:2026-06|功能说明:需求转技术文档对齐双项目docs/ahyk_bss与docs/bss_front，移除cool-uni与三端约定 -->
<!-- AIGC:cursor|author:沉香|lines:约115|dates:2026-06|功能说明:对齐api-developer/front-developer/doc-updater占位符、双路径、下游委派与dev-brief模板 -->
<!-- AIGC:cursor|author:沉香|lines:30|dates:2026-06|功能说明:P1修复-新增交接就绪检查单(G1~G5)、双端dev-brief升为强制、质量自检补两条 -->
<!-- AIGC:cursor|author:沉香|lines:约22|dates:2026-06|功能说明:去除bss/ahyk_bss/bss_front硬编码，统一为{项目组ID}/{需求文档根}等占位符 -->
<!-- AIGC:cursor|author:沉香|lines:约36|dates:2026-07|功能说明:需求转技术文档链路改为.codex与注册表命中的子项目实体docs口径，移除规则侧模块文档强制同步 -->
