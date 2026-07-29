# 执行结果 JSON 字段规范

## 顶层结构

| 字段 | 类型 | 要求 |
|---|---|---|
| meta | object | 必填，记录项目、需求、环境、执行人和来源 |
| results | array | 必填，每条记录对应一条执行用例 |
| defects | array | 必填，可为空 |
| risks | array | 必填，可为空 |
| artifacts | array | 必填，可为空 |

## meta

| 字段 | 要求 |
|---|---|
| project | 项目组和子项目 |
| requirement | 需求名称 |
| environment | 测试环境 |
| test_type | 冒烟 / 功能 / 验收 / 回归 / 复测 |
| execution_level | 推荐填写：冒烟验证 / P0/P1 验收 / 完整回归 / 复测 / 自动化回归沉淀 |
| executor | 执行人 |
| executed_at | 执行时间 |
| source_testcase_json | 来源测试用例 JSON，推荐填写 |
| recommendation | 可空；为空时由报告脚本按结果推断 |

## results

| 字段 | 要求 |
|---|---|
| case_id | 必填，来自 test-yl 的 `TC-*` |
| title | 必填 |
| priority | 推荐填写，P0/P1/P2/P3 |
| status | 必填：通过、失败、阻塞、跳过、待确认、未执行 |
| surface | 推荐填写：cli、api、computer-use、chrome、manual、mixed；界面测试默认填写 computer-use |
| human_assisted | 推荐填写，布尔值；验证码、登录接力、人工视觉确认等为 true |
| confirmation | 涉及 Computer Use 风险动作时填写确认说明或用户接力说明 |
| evidence | 推荐填写，截图、视频、trace、接口响应路径 |
| defect_ids | 失败时必填，关联 defects[].id |
| blocker_reason | 阻塞时必填，或在 note 中说明 |
| confirm_owner | 待确认时必填，或在 note 中说明 |
| note | 执行说明 |

## defects

| 字段 | 要求 |
|---|---|
| id | 必填，建议 `BUG-001` |
| title | 必填 |
| severity | 必填：S1、S2、S3、S4，或 S1阻断、S2严重、S3一般、S4轻微 |
| status | 必填：新建、已确认、修复中、待复测、已关闭、暂不处理 |
| case_id | 必填，关联用例 |
| evidence | 推荐填写 |

## artifacts

可以使用字符串路径，也可以使用对象：

```json
{
  "path": "artifacts/TC-001.png",
  "type": "截图",
  "case_id": "TC-001",
  "description": "首页广告展示"
}
```

## 浏览器/桌面执行补充

- 使用 `chrome` 时，证据应包含 URL、截图、控制台错误或网络请求记录。
- 使用 `computer-use` 时，涉及上传、敏感数据传输、删除/移动、权限/账号/支付/系统设置、验证码等动作，必须记录 `confirmation` 或在 `note` 中说明用户接力。
- 使用 `manual` 或 `human_assisted: true` 时，应说明人工参与的原因和范围。

<!-- AIGC:cursor|author:沉香|lines:约2|dates:2026-07|功能说明:同步执行结果字段规范，明确界面测试默认记录为computer-use -->
