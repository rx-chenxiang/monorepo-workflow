# 标准测试用例 JSON 模板

生成用例时先产出此 JSON，再运行 `scripts/validate_testcase_json.py`。不要直接写 Excel。

## 固定结构

```json
{
  "meta": {
    "requirement_name": "需求名称",
    "project": "general",
    "generated_date": "2026-07-06"
  },
  "test_cases": [
    {
      "case_id": "TC-001",
      "module": "客户管理",
      "platform": "后台",
      "page": "客户分配",
      "function_module": "批量分配",
      "test_dimension": "正常场景",
      "title": "验证销售主管可批量分配本组织待分配客户",
      "precondition": "测试环境已登录销售主管 A；存在 3 条本组织待分配客户；客户分配开关=开启。",
      "test_data": "账号：销售主管 A；数据：本组织待分配客户 3 条；配置：客户分配开关=开启。",
      "steps": [
        "在【客户分配】页面，进行【使用销售主管 A 打开页面】操作。",
        "在【客户分配】页面，进行【勾选 3 条本组织待分配客户并选择销售 B】操作。",
        "在【客户分配】页面，进行【提交批量分配】操作。"
      ],
      "expected": [
        "页面正常加载客户分配列表，待分配客户可被勾选。",
        "销售 B 可被选择，提交按钮可用。",
        "页面提示分配成功，接口返回 code=0，数据库客户负责人更新为销售 B。"
      ],
      "verification_layer": "页面：成功提示与列表负责人刷新；接口：assignCustomer 返回 code=0；数据库：customer.owner_id 更新。",
      "requirement_id": "REQ-001",
      "test_point_id": "TP-001",
      "priority": "P0",
      "type": "冒烟测试",
      "tags": ["批量分配", "主流程"],
      "owner": "系统生成",
      "remark": "无",
      "source_doc": "需求文档/客户分配 PRD.md",
      "source_heading": "3.1 批量分配",
      "source_excerpt": "销售主管可选择本组织待分配客户并批量分配给销售人员。"
    }
  ],
  "coverage_matrix": [
    {
      "requirement_id": "REQ-001",
      "requirement_name": "客户批量分配",
      "feature": "销售主管批量分配本组织待分配客户",
      "api_or_table": "assignCustomer; customer",
      "test_point_id": "TP-001",
      "linked_case_ids": "TC-001",
      "coverage_status": "已覆盖",
      "description": "覆盖主流程、接口响应和数据库负责人更新。",
      "source_doc": "需求文档/客户分配 PRD.md",
      "source_heading": "3.1 批量分配",
      "source_excerpt": "销售主管可选择本组织待分配客户并批量分配给销售人员。"
    }
  ],
  "review_report": [
    {
      "dimension": "覆盖度",
      "result": "通过",
      "description": "1 个需求、1 个测试点、1 条用例均已覆盖。"
    },
    {
      "dimension": "待确认",
      "result": "待确认",
      "description": "请人工确认测试账号、组织范围和开关配置。"
    }
  ],
  "business_profile": {
    "terms": ["客户分配", "待分配客户"],
    "roles": ["销售主管", "销售"],
    "rules": ["销售主管只能分配本组织客户"],
    "interfaces": ["assignCustomer"],
    "tables": ["customer"],
    "risks": ["批量操作", "数据范围"],
    "assumptions": ["测试账号和组织数据需人工准备"]
  }
}
```

## 生成要求

- `case_id`、`test_point_id`、`requirement_id` 必须从 `001` 连续编号，不得跳号。
- P0/P1 用例必须填写 `test_data` 和 `verification_layer`。
- `steps` 与 `expected` 建议都用数组，数量和语义尽量一一对应。
- `test_dimension` 只能取 `coverage-rules.md` 中的 11 个枚举。
- `type` 只能取 Excel 字段规范中的固定枚举，不要把“边界值”“权限”“接口”等维度写入 `type`。
- 每个 `test_cases` 和 `coverage_matrix` 条目都必须填写 `source_doc`、`source_heading`、`source_excerpt`。
- `source_excerpt` 只摘录短句，不要复制大段原文；无法定位来源时写入二次核对报告并标记 `待确认`。
- 涉及接口或数据表时，至少一条关联用例的 `verification_layer` 必须包含“接口”或“数据库/缓存/队列/日志”核验。
- P0/P1 超过 30% 时，`review_report` 必须有一条说明高风险原因，说明中包含 `P0/P1` 或 `高风险`。
