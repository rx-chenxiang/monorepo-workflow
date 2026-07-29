# test-yl 到 qa-test-execution 交接协议

## 交接目标

`test-yl` 负责生成测试设计资产，`qa-test-execution` 负责执行。两者之间必须使用机器可读 JSON 交接，Excel 和 Markdown 只作为人工评审材料。

## 输入文件

`qa-test-execution` 优先接收：

```text
{需求名称}_测试用例_{YYYYMMDD}.json
```

该 JSON 必须包含：

- `meta`
- `test_cases`
- `coverage_matrix`
- `review_report`
- `business_profile`

交接时还应补充执行上下文；若缺失，由 `qa-test-execution` 生成阻塞清单或测试委托单：

- 推荐执行等级：冒烟验证 / P0/P1 验收 / 完整回归 / 复测 / 自动化回归沉淀
- 测试环境地址和登录入口
- 测试账号、账号角色与权限
- 测试数据授权和清理方式
- 设备/浏览器范围
- 已知待确认项、视觉主观项确认人和上线阻断规则

## 稳定关联键

以下字段生成后必须稳定，不得因筛选、排序、执行状态变化而改号：

- `requirement_id` / `需求ID`
- `test_point_id` / `测试点ID`
- `case_id` / `用例ID`

执行结果、缺陷、证据、自动化用例都必须通过 `case_id` 关联回测试用例。

## 执行结果 JSON

执行结果文件建议命名：

```text
{需求名称}_测试执行结果_{YYYYMMDD}.json
```

最小结构：

```json
{
  "meta": {
    "project": "h5 / ahyk_h5_front",
    "requirement": "需求名称",
    "environment": "测试环境",
    "test_type": "功能测试",
    "execution_level": "P0/P1 验收",
    "executor": "Codex",
    "executed_at": "2026-07-06 12:00",
    "source_testcase_json": "测试用例JSON路径",
    "recommendation": ""
  },
  "results": [
    {
      "case_id": "TC-001",
      "title": "验证xxx",
      "priority": "P0",
      "status": "通过",
      "executor": "Codex",
      "executed_at": "2026-07-06 12:10",
      "environment": "测试环境",
      "evidence": ["artifacts/TC-001.png"],
      "note": "无"
    }
  ],
  "defects": [],
  "risks": [],
  "artifacts": []
}
```

## 状态枚举

`results[].status` 只能使用：

- `通过`
- `失败`
- `阻塞`
- `跳过`
- `待确认`
- `未执行`

## 一致性规则

- `失败` 用例必须至少关联一个未关闭缺陷。
- `阻塞` 用例必须填写 `blocker_reason` 或 `note`。
- `待确认` 用例必须填写 `confirm_owner` 或 `note`。
- P0/P1 失败或阻塞时，最终建议不得为 `通过`。
- 存在未关闭 S1/S2 缺陷时，最终建议必须为 `不建议上线` 或更保守。
- 存在阻塞用例时，最终建议应为 `阻塞无法判断`，除非用户明确人工豁免。

## 自动化交接

适合沉淀自动化的用例应在执行结果或报告中标记：

```json
{
  "automation_candidate": true,
  "automation_reason": "规则客观稳定，可通过页面元素和接口响应断言"
}
```
