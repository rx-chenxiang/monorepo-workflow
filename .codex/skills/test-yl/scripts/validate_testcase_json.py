#!/usr/bin/env python3
"""Validate testcase JSON before writing the workbook."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ALIASES = {
    "case_id": "用例ID",
    "id": "用例ID",
    "module": "目录",
    "platform": "平台",
    "page": "页面",
    "function_module": "功能模块",
    "test_dimension": "测试维度",
    "title": "标题",
    "precondition": "前置条件",
    "test_data": "测试数据",
    "steps": "步骤描述",
    "expected": "预期结果",
    "verification_layer": "验证层级",
    "requirement_id": "关联需求",
    "test_point_id": "关联测试点",
    "priority": "优先级",
    "type": "类型",
    "tags": "标签",
    "status": "状态",
    "owner": "负责人",
    "remark": "备注",
    "requirement_name": "需求名称",
    "feature": "功能点",
    "api_or_table": "数据表/接口",
    "linked_case_ids": "关联用例ID",
    "coverage_status": "覆盖状态",
    "dimension": "核对维度",
    "result": "核对结果",
    "description": "说明",
}

CASE_REQUIRED = ["用例ID", "目录", "平台", "页面", "功能模块", "测试维度", "标题", "前置条件", "步骤描述", "预期结果", "关联需求", "关联测试点", "优先级", "类型"]
P0_P1_REQUIRED = CASE_REQUIRED + ["测试数据", "验证层级"]
SOURCE_REQUIRED = ["source_doc", "source_heading", "source_excerpt"]
COVERAGE_REQUIRED = ["需求ID", "需求名称", "功能点", "数据表/接口", "测试点ID", "关联用例ID", "覆盖状态"] + SOURCE_REQUIRED
REVIEW_REQUIRED = ["核对维度", "核对结果", "说明"]
TEST_TYPE_VALUES = {
    "回归测试",
    "功能测试",
    "性能测试",
    "兼容性测试",
    "易用性测试",
    "安全性测试",
    "稳定性测试",
    "接口测试",
    "自动化测试",
    "安装部署测试",
    "冒烟测试",
}
TEST_DIMENSION_VALUES = {
    "功能入口",
    "UI展示",
    "交互效果",
    "更新机制",
    "连点测试",
    "断网测试",
    "正常场景",
    "异常场景",
    "旧版本兼容",
    "影响范围",
    "测试经验",
}


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in row.items():
        normalized[ALIASES.get(key, key)] = value
    return normalized


def load_rows(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    rows = data.get(key, [])
    if not isinstance(rows, list):
        raise ValueError(f"{key} 必须是数组")
    normalized = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{key}[{index}] 必须是对象")
        normalized_row = normalize_row(row)
        if key == "coverage_matrix":
            if "requirement_id" in row:
                normalized_row["需求ID"] = row["requirement_id"]
            if "test_point_id" in row:
                normalized_row["测试点ID"] = row["test_point_id"]
        normalized.append(normalized_row)
    return normalized


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ",".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def split_ids(value: Any) -> set[str]:
    raw = text(value)
    if not raw or raw == "无":
        return set()
    return {item for item in re.split(r"[,，;；\s\n]+", raw) if item}


def count_numbered_items(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, list):
        return len([item for item in value if text(item)])
    raw = text(value)
    if not raw:
        return 0
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    numbered = [line for line in lines if re.match(r"^\s*\d+[\.、)]\s*", line)]
    if numbered:
        return len(numbered)
    return len(lines)


def numbered_lines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    raw = text(value)
    if not raw:
        return []
    return [line.strip() for line in raw.splitlines() if line.strip()]


def step_matches_page_action_format(line: str) -> bool:
    cleaned = re.sub(r"^\s*\d+[\.、)]\s*", "", line).strip()
    return bool(re.match(r"^在【[^】]+】页面，进行【[^】]+】操作", cleaned))


def add_missing(errors: list[str], row: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if not text(row.get(field))]
    if missing:
        errors.append(f"{label} 缺少必填字段: {', '.join(missing)}")


def find_duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def id_number(value: str, prefix: str) -> int | None:
    match = re.fullmatch(rf"{re.escape(prefix)}-(\d{{3,}})", value)
    if not match:
        return None
    return int(match.group(1))


def validate_contiguous_ids(errors: list[str], label: str, values: list[str], prefix: str) -> None:
    numbers = sorted({number for value in values if (number := id_number(value, prefix)) is not None})
    if not numbers:
        return
    expected = list(range(1, numbers[-1] + 1))
    if numbers != expected:
        missing = sorted(set(expected) - set(numbers))
        errors.append(f"{label} 编号必须从 {prefix}-001 连续递增，缺失: {', '.join(f'{prefix}-{item:03d}' for item in missing)}")


def contains_real_technical_target(value: Any) -> bool:
    raw = text(value)
    if not raw or raw in {"无", "不涉及", "待确认"}:
        return False
    return True


def has_interface_or_data_verification(value: Any) -> bool:
    raw = text(value)
    if not raw:
        return False
    technical_layers = ["接口", "数据库", "缓存", "队列", "日志"]
    return any(layer in raw for layer in technical_layers)


def review_explains_high_priority_ratio(review: list[dict[str, Any]]) -> bool:
    for row in review:
        dimension = text(row.get("核对维度"))
        description = text(row.get("说明"))
        combined = f"{dimension} {description}"
        if ("P0/P1" in combined or "高风险" in combined) and ("超" in combined or "原因" in combined or "风险" in combined):
            return True
    return False


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    cases = load_rows(data, "test_cases")
    coverage = load_rows(data, "coverage_matrix")
    review = load_rows(data, "review_report")

    if not cases:
        errors.append("test_cases 不能为空")
    if not coverage:
        errors.append("coverage_matrix 不能为空")
    if not review:
        errors.append("review_report 不能为空")

    case_ids: list[str] = []
    test_dimensions: set[str] = set()
    case_test_points: dict[str, set[str]] = {}
    case_requirements: dict[str, set[str]] = {}
    cases_by_test_point: dict[str, list[dict[str, Any]]] = {}

    for index, row in enumerate(cases, start=1):
        label = f"测试用例第 {index} 行"
        priority = text(row.get("优先级"))
        required = P0_P1_REQUIRED if priority in {"P0", "P1"} else CASE_REQUIRED
        required = required + SOURCE_REQUIRED
        add_missing(errors, row, required, label)

        case_id = text(row.get("用例ID"))
        if case_id:
            case_ids.append(case_id)
            if not re.fullmatch(r"TC-\d{3,}", case_id):
                errors.append(f"{label} 用例ID 格式应为 TC-001: {case_id}")

        if priority and priority not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"{label} 优先级无效: {priority}")

        case_type = text(row.get("类型"))
        if case_type and case_type not in TEST_TYPE_VALUES:
            errors.append(f"{label} 类型无效: {case_type}；必须是 {', '.join(sorted(TEST_TYPE_VALUES))}")

        test_dimension = text(row.get("测试维度"))
        if test_dimension:
            if test_dimension not in TEST_DIMENSION_VALUES:
                errors.append(f"{label} 测试维度无效: {test_dimension}；必须是 {', '.join(sorted(TEST_DIMENSION_VALUES))}")
            else:
                test_dimensions.add(test_dimension)

        linked_points = split_ids(row.get("关联测试点"))
        case_test_points[case_id] = linked_points
        case_requirements[case_id] = split_ids(row.get("关联需求"))
        for point_id in linked_points:
            cases_by_test_point.setdefault(point_id, []).append(row)

        if priority in {"P0", "P1"}:
            verification = text(row.get("验证层级"))
            known_layers = ["页面", "接口", "数据库", "日志", "队列", "缓存", "文件", "通知"]
            if verification and not any(layer in verification for layer in known_layers):
                warnings.append(f"{label} 验证层级过于模糊: {verification}")

        step_count = count_numbered_items(row.get("步骤描述"))
        expected_count = count_numbered_items(row.get("预期结果"))
        if step_count and expected_count and step_count != expected_count:
            warnings.append(f"{label} 步骤描述数量({step_count})与预期结果数量({expected_count})不一致")
        for step_index, step in enumerate(numbered_lines(row.get("步骤描述")), start=1):
            if not step_matches_page_action_format(step):
                warnings.append(f"{label} 第 {step_index} 个步骤建议使用“在【xxx】页面，进行【xxx】操作”格式")

    duplicate_cases = find_duplicates(case_ids)
    if duplicate_cases:
        errors.append(f"用例ID 重复: {', '.join(sorted(duplicate_cases))}")
    validate_contiguous_ids(errors, "用例ID", case_ids, "TC")

    high_priority_count = sum(1 for row in cases if text(row.get("优先级")) in {"P0", "P1"})
    high_priority_ratio = high_priority_count / len(cases) if cases else 0
    high_priority_ratio_exceeded = bool(cases and high_priority_ratio > 0.3)

    missing_test_dimensions = TEST_DIMENSION_VALUES - test_dimensions
    if missing_test_dimensions:
        if len(cases) >= len(TEST_DIMENSION_VALUES):
            warnings.append(f"测试维度未完整覆盖: {', '.join(sorted(missing_test_dimensions))}")

    case_id_set = set(case_ids)
    requirement_ids: set[str] = set()
    requirement_id_values: list[str] = []
    test_point_ids: set[str] = set()
    test_point_id_values: list[str] = []
    linked_test_points: set[str] = set()
    should_have_cases: set[str] = set()
    technical_test_points: set[str] = set()

    for index, row in enumerate(coverage, start=1):
        label = f"覆盖矩阵第 {index} 行"
        add_missing(errors, row, COVERAGE_REQUIRED, label)

        requirement_id = text(row.get("需求ID"))
        test_point_id = text(row.get("测试点ID"))
        status = text(row.get("覆盖状态"))
        linked_cases = split_ids(row.get("关联用例ID"))

        if requirement_id:
            requirement_ids.add(requirement_id)
            requirement_id_values.append(requirement_id)
            if not re.fullmatch(r"REQ-\d{3,}", requirement_id):
                errors.append(f"{label} 需求ID 格式应为 REQ-001: {requirement_id}")
        if test_point_id:
            test_point_ids.add(test_point_id)
            test_point_id_values.append(test_point_id)
            if not re.fullmatch(r"TP-\d{3,}", test_point_id):
                errors.append(f"{label} 测试点ID 格式应为 TP-001: {test_point_id}")
        if status and status not in {"已覆盖", "部分覆盖", "未覆盖", "待确认"}:
            errors.append(f"{label} 覆盖状态无效: {status}")

        unknown_cases = linked_cases - case_id_set
        if unknown_cases:
            errors.append(f"{label} 关联了不存在的用例ID: {', '.join(sorted(unknown_cases))}")
        if status in {"已覆盖", "部分覆盖"}:
            should_have_cases.add(test_point_id)
            if not linked_cases:
                errors.append(f"{label} 标记{status}但关联用例ID为空")
        if linked_cases:
            linked_test_points.add(test_point_id)
        if contains_real_technical_target(row.get("数据表/接口")):
            technical_test_points.add(test_point_id)

    duplicate_test_points = find_duplicates([text(row.get("测试点ID")) for row in coverage if text(row.get("测试点ID"))])
    if duplicate_test_points:
        errors.append(f"测试点ID 重复: {', '.join(sorted(duplicate_test_points))}")
    validate_contiguous_ids(errors, "需求ID", requirement_id_values, "REQ")
    validate_contiguous_ids(errors, "测试点ID", test_point_id_values, "TP")

    for case_id, points in case_test_points.items():
        unknown_points = points - test_point_ids
        if unknown_points:
            errors.append(f"{case_id} 关联了覆盖矩阵不存在的测试点: {', '.join(sorted(unknown_points))}")

    for case_id, requirements in case_requirements.items():
        unknown_requirements = requirements - requirement_ids
        if unknown_requirements:
            errors.append(f"{case_id} 关联了覆盖矩阵不存在的需求: {', '.join(sorted(unknown_requirements))}")

    missing_case_points = should_have_cases - linked_test_points
    if missing_case_points:
        warnings.append(f"以下测试点未关联任何用例: {', '.join(sorted(missing_case_points))}")

    for test_point_id in sorted(technical_test_points):
        linked_cases = cases_by_test_point.get(test_point_id, [])
        if linked_cases and not any(has_interface_or_data_verification(case.get("验证层级")) or has_interface_or_data_verification(case.get("预期结果")) for case in linked_cases):
            errors.append(f"{test_point_id} 涉及接口或数据表，但关联用例未写明接口/数据库/缓存/队列/日志核验点")

    review_results: list[str] = []
    review_dimensions: set[str] = set()
    for index, row in enumerate(review, start=1):
        label = f"二次核对第 {index} 行"
        add_missing(errors, row, REVIEW_REQUIRED, label)
        result = text(row.get("核对结果"))
        dimension = text(row.get("核对维度"))
        if result:
            review_results.append(result)
        if dimension:
            review_dimensions.add(dimension)
        if result and result not in {"通过", "部分通过", "未通过", "待确认"}:
            errors.append(f"{label} 核对结果无效: {result}")

    if review and review_results and set(review_results) == {"通过"}:
        warnings.append("二次核对报告全部为通过，请确认没有隐藏缺口、假设或待确认项")

    recommended_dimensions = {"覆盖度", "主流程", "异常", "权限", "接口", "数据表", "待确认"}
    missing_dimensions = recommended_dimensions - review_dimensions
    if missing_dimensions:
        warnings.append(f"二次核对报告建议补充维度: {', '.join(sorted(missing_dimensions))}")

    if high_priority_ratio_exceeded:
        ratio_text = f"P0/P1 用例占比 {high_priority_count}/{len(cases)} ({high_priority_ratio:.0%})"
        if not review_explains_high_priority_ratio(review):
            errors.append(f"{ratio_text}，超过 30% 时必须在二次核对报告说明高风险原因")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate testcase JSON quality.")
    parser.add_argument("--input", required=True, help="Input JSON path.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures. This is the default.")
    parser.add_argument("--no-strict", action="store_true", help="Allow warnings and only fail on errors.")
    args = parser.parse_args()

    data = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    errors, warnings = validate(data)

    for warning in warnings:
        print(f"[WARN] {warning}", file=sys.stderr)
    for error in errors:
        print(f"[ERROR] {error}", file=sys.stderr)

    strict = not args.no_strict
    if errors or (strict and warnings):
        return 1
    print("测试用例 JSON 校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
