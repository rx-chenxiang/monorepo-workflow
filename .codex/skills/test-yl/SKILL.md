---
name: test-yl
description: 从 PRD、需求文档、技术设计文档、接口文档或仓库 docs 目录生成中文测试用例资产。用户提到“测试用例生成”“生成测试用例”“QA 用例”“验收用例”“测试点覆盖矩阵”“测试设计脑图”“根据需求和开发文档出用例”，或提供需求文档路径与开发文档路径时使用本技能。输出包含测试用例 Excel、测试设计脑图 Markdown、测试用例 Markdown，并维护业务知识画像以减少幻觉。生成过程按平台、页面、功能模块拆解需求，覆盖功能入口、UI 展示、交互效果、更新机制、连点测试、断网测试、正常场景、异常场景、旧版本兼容、影响范围、测试经验等维度，并进行测试数据设计、权限矩阵、接口/数据验证、P0/P1 数量控制、技术一致性与自动质量校验。
---

# 测试用例生成

## 目标

根据需求文档和开发/技术文档生成可执行、可追溯、可复核的中文测试用例 Excel，而不是只生成看起来完整的清单。

## 输入解析

1. 接受以下输入形式：
   - 明确的需求文档路径 + 开发文档路径。
   - 一个需求目录，例如 `docs/general/xxx/`。
   - 工作区 + 需求名称，例如 `general 客资分配 测试用例生成`。
2. 若只给需求目录，优先查找：
   - `需求文档/` 下的 PRD、需求说明、原型说明。
   - `技术设计方案/` 下的技术方案、前端技术设计、后端技术设计。
   - `coding-plan/` 下的编码计划，仅作为补充材料。
3. 若存在多个候选文档且无法判断主文档，只问用户一次确认。
4. 输出目录选择：
   - 若用户给出输出路径，以用户路径为准。
   - 若输入是工作区需求目录 `docs/{项目组ID}/{需求名称}/` 且可写，默认输出到该目录下的 `测试资产/`，便于和 PRD、技术方案、coding-plan 一起归档。
   - 其他场景默认输出到用户桌面。禁止写死用户名或系统路径。

## 可用脚本

优先使用脚本处理重复且容易出错的环节。

- `scripts/extract_documents.py`：读取 `.md`、`.txt`、`.docx`、`.xlsx`、`.pdf` 文档并输出结构化 JSON。
- `scripts/preflight.py`：生成前检查依赖、输入文档可读性和输出目录写入权限。
- `scripts/write_testcase_workbook.py`：根据 JSON 数据生成包含四个工作表的 `.xlsx`。
- `scripts/write_testcase_markdown.py`：根据 JSON 数据生成测试用例 Markdown 文本。
- `scripts/write_test_design_mindmap.py`：根据 JSON 数据生成 Mermaid 测试设计脑图 Markdown。
- `scripts/update_business_profile.py`：根据本次用例 JSON 更新业务知识画像 Markdown。
- `scripts/validate_testcase_json.py`：生成 Excel 前校验字段完整性、编号追溯、覆盖矩阵和二次核对质量。

示例：

```bash
python3 scripts/preflight.py --input "需求.docx" --input "技术方案.md" --output-dir "$OUTPUT_DIR"
python3 scripts/extract_documents.py --input "需求.docx" --input "技术方案.md" --output /tmp/testcase_sources.json
python3 scripts/validate_testcase_json.py --input /tmp/testcase_cases.json
python3 scripts/write_testcase_workbook.py --input /tmp/testcase_cases.json --output "$OUTPUT_DIR/需求名称_测试用例_20260702.xlsx"
python3 scripts/write_testcase_markdown.py --input /tmp/testcase_cases.json --output "$OUTPUT_DIR/需求名称_测试用例_20260702.md"
python3 scripts/write_test_design_mindmap.py --input /tmp/testcase_cases.json --output "$OUTPUT_DIR/需求名称_测试设计脑图_20260702.md"
python3 scripts/update_business_profile.py --input /tmp/testcase_cases.json --profile "$OUTPUT_DIR/业务知识画像.md" --source "需求名称"
```

PDF 读取依赖 `pypdf` 或 `pdfplumber`，若当前环境缺少依赖，应明确告知用户该文件无法自动抽取，并尝试读取其他可用文档。

## 生成流程

1. 读取文档，保留标题层级、表格、需求编号、角色、状态流、接口、数据表、开关配置、异常规则。
2. 读取已有业务知识画像：
   - 优先读取用户指定画像。
   - 若未指定，尝试读取需求目录或输出目录下的 `业务知识画像.md`。
   - 画像只作为术语、角色、规则、接口、表名参考；不得覆盖本次文档的明确描述。
3. 建立需求清单：
   - 需求编号使用 `REQ-001`。
   - 测试点编号使用 `TP-001`。
   - 用例编号使用 `TC-001`。
   - 三类编号必须从 `001` 连续递增，不得跳号。
   - 每条用例和覆盖矩阵都必须记录 `source_doc`、`source_heading`、`source_excerpt`。
4. 按 `references/generation-patterns.md` 拆解需求：
   - 先识别平台：后台、APP、小程序、H5、接口、定时任务等。
   - 再识别页面：同一需求中多个页面必须拆开建用例。
   - 再识别功能模块：同一页面下按功能入口、列表、表单、详情、状态流、导入导出等拆分。
   - 页面/表单/列表/详情/导入导出。
   - 接口/数据表/队列/缓存/定时任务。
   - 权限/角色/组织/数据范围。
   - 状态流/审批流/批量操作/灰度开关。
5. 先生成 P0/P1：
   - P0：核心冒烟、主链路正向、版本可用性。
   - P1：主流程负向、核心业务规则、权限、数据一致性。
   - P0+P1 合计数量应按影响范围控制，通常不超过总用例数的 30%；高风险需求超出时必须在二次核对报告说明原因。
6. 再按风险补充 P2/P3：
   - 边界值、等价类、异常容错、并发/幂等、灰度开关、兼容性、安全、UI 反馈。
7. 为每条用例整理步骤和预期结果：
   - `步骤描述` 使用 `1. ...`、`2. ...` 按序号换行。
   - 每个步骤优先使用 `在【xxx】页面，进行【xxx】操作` 格式，明确所在页面和动作。
   - `预期结果` 使用相同序号换行，与步骤尽量一一对应。
8. 为每条 P0/P1 用例补齐测试数据和验证层级：
   - 测试数据包含正常、边界、异常、权限、历史脏数据或跨组织数据。
   - 验证层级写明页面、接口、数据库、日志、队列、缓存中的实际核验点。
9. 不要臆造文档不存在的行为。必须推断时，在“二次核对报告”写入“假设项”或“待人工确认”。
10. 先运行 `scripts/validate_testcase_json.py`，该脚本默认使用严格模式；修正阻断问题后再生成所有交付物。
11. 保存测试用例 JSON，并生成 Excel、测试设计脑图、测试用例 Markdown，同时更新业务知识画像。
12. 生成后做一次自检：需求是否全覆盖、测试点是否有用例、P0/P1 比例是否合理、接口/数据表是否被验证、是否存在未确认假设。
13. 在最终回复中明确测试用例 JSON 路径；若用户要求继续验收、执行、跑用例或回归，下一步使用 `qa-test-execution` 并传入该 JSON 路径。

## 输出要求

输出文件命名：

```text
{需求名称}_测试用例_{YYYYMMDD}.xlsx
{需求名称}_测试用例_{YYYYMMDD}.md
{需求名称}_测试用例_{YYYYMMDD}.json
{需求名称}_测试设计脑图_{YYYYMMDD}.md
```

推荐归档位置：

- 工作区需求目录输入：`docs/{项目组ID}/{需求名称}/测试资产/`
- 非工作区散落文档输入：用户指定目录或桌面

每次生成必须同时输出：

1. 测试用例 JSON：机器可读主数据，作为 Excel、Markdown、脑图和 `qa-test-execution` 执行流的唯一事实来源。
2. 测试用例 Excel：固定包含 `测试用例`、`结构化明细`、`测试点覆盖矩阵`、`二次核对报告` 四个工作表。
3. 测试设计脑图 Markdown：使用 Mermaid `mindmap`，按需求、测试点、类型、优先级组织。
4. 测试用例 Markdown：便于评审、复制、提交评审或沉淀到 docs。

`测试用例` 工作表表头必须严格为：

```text
序号、标题、目录、负责人、前置条件、步骤描述、预期结果、关联工作项、优先级、类型、标签
```

平台、页面、功能模块、测试维度、用例ID 等内部元数据仍需在 JSON、Markdown、脑图中保留；写入 Excel 时合并到 `目录`、`关联工作项`、`标签`。

`结构化明细` 工作表至少包含：

```text
用例ID、平台、页面、功能模块、测试维度、测试数据、验证层级、备注、source_doc、source_heading、source_excerpt
```

业务知识画像：

- 若用户指定画像路径，更新该路径。
- 若用户未指定，输出或更新 `{输出目录}/业务知识画像.md`。
- 画像记录业务术语、角色权限、核心规则、接口/数据表、风险点、待确认项和来源日期。

详细字段规范见 `references/testcase-schema.md`。
标准 JSON 模板见 `references/json-generation-template.md`。
机器校验 Schema 见 `references/testcase.schema.json`。
覆盖与优先级规则见 `references/coverage-rules.md`。
需求拆解、测试数据、权限矩阵、接口/数据验证规则见 `references/generation-patterns.md`。

交接执行：

- 生成的 `{需求名称}_测试用例_{YYYYMMDD}.json` 必须保留 `meta`、`test_cases`、`coverage_matrix`、`review_report`、`business_profile`。
- `case_id`、`requirement_id`、`test_point_id` 是后续执行、缺陷、报告和自动化回归的稳定关联键，生成后不得因排序或筛选重排而改变。
- 交给 `qa-test-execution` 时，优先使用 JSON；Excel 和 Markdown 仅作为评审和人工阅读资产。
- 若执行环境、账号、测试数据授权或设备范围缺失，交接时列出缺口，交由 `qa-test-execution` 生成测试委托单或阻塞清单。

## 质量门禁

生成完成前必须满足：

- 每个 `REQ-*` 至少对应一个 `TP-*`。
- 每个已覆盖 `TP-*` 至少对应一个 `TC-*`。
- `REQ-*`、`TP-*`、`TC-*` 必须分别从 `001` 连续编号。
- 每条用例必须填写 `平台`、`页面`、`功能模块`、`测试维度`，多平台/多页面需求必须按页面生成对应用例。
- 每条用例和每条覆盖矩阵必须填写 `source_doc`、`source_heading`、`source_excerpt`。
- P0/P1 用例必须包含明确前置条件、测试数据、步骤、预期结果、验证层级。
- `步骤描述` 和 `预期结果` 尽量按相同序号换行并一一对应。
- `步骤描述` 优先使用 `在【xxx】页面，进行【xxx】操作` 格式。
- 用例整体必须覆盖：功能入口、UI展示、交互效果、更新机制、连点测试、断网测试、正常场景、异常场景、旧版本兼容、影响范围、测试经验。
- P0+P1 总量通常不超过总用例数的 30%；超出时必须在“二次核对报告”说明高风险原因。
- “类型”列只能使用：回归测试、功能测试、性能测试、兼容性测试、易用性测试、安全性测试、稳定性测试、接口测试、自动化测试、安装部署测试、冒烟测试。
- 涉及权限、金额、订单、状态流转、数据删除、批量操作、灰度开关的需求，必须有异常或安全/一致性用例。
- 涉及接口或数据表的需求，至少有一条用例写明接口响应和数据库/缓存/队列/日志中的核验点。
- “二次核对报告”不得默认全通过；发现缺口时如实写 `未通过`、`部分通过` 或 `待确认`。
