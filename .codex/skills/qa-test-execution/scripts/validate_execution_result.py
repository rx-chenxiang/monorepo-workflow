#!/usr/bin/env python3
"""Validate QA execution result JSON before report generation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


STATUS_VALUES = {"通过", "失败", "阻塞", "跳过", "待确认", "未执行"}
PRIORITY_VALUES = {"P0", "P1", "P2", "P3"}
SURFACE_VALUES = {"cli", "api", "chrome", "computer-use", "manual", "mixed"}
# AIGC:cursor|author:沉香|lines:约1|dates:2026-07|功能说明:收紧测试执行面枚举，移除Playwright执行面以匹配Computer Use默认策略
RECOMMENDATION_VALUES = {"通过", "有条件通过", "不建议上线", "阻塞无法判断", ""}
EXECUTION_LEVEL_VALUES = {"冒烟验证", "P0/P1 验收", "完整回归", "复测", "自动化回归沉淀", ""}
OPEN_DEFECT_STATUSES = {"新建", "已确认", "修复中", "待复测", "reopen", "open"}
CLOSED_DEFECT_STATUSES = {"已关闭", "关闭", "closed"}
SEVERITY_VALUES = {"S1", "S2", "S3", "S4", "S1阻断", "S2严重", "S3一般", "S4轻微"}


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ",".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [text(item) for item in value if text(item)]
    raw = text(value)
    if not raw:
        return []
    return [item for item in re.split(r"[,，;；\s\n]+", raw) if item]


def load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("execution result JSON must be an object")
    return data


def add_missing(errors: list[str], row: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if not text(row.get(field))]
    if missing:
        errors.append(f"{label} 缺少必填字段: {', '.join(missing)}")


def is_open_defect(status: str) -> bool:
    return status not in CLOSED_DEFECT_STATUSES


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    meta = data.get("meta", {})
    results = data.get("results", [])
    defects = data.get("defects", [])
    risks = data.get("risks", [])
    artifacts = data.get("artifacts", [])

    if not isinstance(meta, dict):
        errors.append("meta 必须是对象")
        meta = {}
    if not isinstance(results, list):
        errors.append("results 必须是数组")
        results = []
    if not isinstance(defects, list):
        errors.append("defects 必须是数组")
        defects = []
    if not isinstance(risks, list):
        errors.append("risks 必须是数组")
    if not isinstance(artifacts, list):
        errors.append("artifacts 必须是数组")

    add_missing(errors, meta, ["project", "requirement", "environment", "test_type", "executor", "executed_at"], "meta")
    recommendation = text(meta.get("recommendation"))
    if recommendation not in RECOMMENDATION_VALUES:
        errors.append(f"meta.recommendation 无效: {recommendation}")
    execution_level = text(meta.get("execution_level"))
    if execution_level not in EXECUTION_LEVEL_VALUES:
        warnings.append(f"meta.execution_level 未在推荐枚举中: {execution_level}")

    defect_by_id: dict[str, dict[str, Any]] = {}
    open_s1_s2: list[str] = []
    open_defects_by_case: dict[str, list[str]] = {}

    for index, raw_defect in enumerate(defects, start=1):
        if not isinstance(raw_defect, dict):
            errors.append(f"defects[{index}] 必须是对象")
            continue
        label = f"缺陷第 {index} 行"
        add_missing(errors, raw_defect, ["id", "title", "severity", "status", "case_id"], label)
        defect_id = text(raw_defect.get("id"))
        if defect_id in defect_by_id:
            errors.append(f"{label} 缺陷ID重复: {defect_id}")
        if defect_id:
            defect_by_id[defect_id] = raw_defect
        severity = text(raw_defect.get("severity"))
        status = text(raw_defect.get("status"))
        case_id = text(raw_defect.get("case_id"))
        if severity and severity not in SEVERITY_VALUES:
            errors.append(f"{label} 严重级别无效: {severity}")
        if status and status not in OPEN_DEFECT_STATUSES | CLOSED_DEFECT_STATUSES | {"暂不处理"}:
            warnings.append(f"{label} 缺陷状态未在推荐枚举中: {status}")
        if is_open_defect(status) and case_id:
            open_defects_by_case.setdefault(case_id, []).append(defect_id)
        if severity in {"S1", "S2", "S1阻断", "S2严重"} and is_open_defect(status):
            open_s1_s2.append(defect_id)

    status_counts: Counter[str] = Counter()
    high_priority_failed_or_blocked: list[str] = []
    result_case_ids: list[str] = []

    for index, raw_result in enumerate(results, start=1):
        if not isinstance(raw_result, dict):
            errors.append(f"results[{index}] 必须是对象")
            continue
        label = f"执行结果第 {index} 行"
        add_missing(errors, raw_result, ["case_id", "title", "status"], label)
        case_id = text(raw_result.get("case_id"))
        title = text(raw_result.get("title"))
        status = text(raw_result.get("status"))
        priority = text(raw_result.get("priority"))
        surface = text(raw_result.get("surface"))
        result_case_ids.append(case_id)

        if case_id and not re.fullmatch(r"TC-\d{3,}", case_id):
            errors.append(f"{label} case_id 格式应为 TC-001: {case_id}")
        if status and status not in STATUS_VALUES:
            errors.append(f"{label} status 无效: {status}")
        if priority and priority not in PRIORITY_VALUES:
            errors.append(f"{label} priority 无效: {priority}")
        if surface and surface not in SURFACE_VALUES:
            errors.append(f"{label} surface 无效: {surface}")
        if not surface:
            warnings.append(f"{label} 未填写 surface，建议记录执行面: {case_id}")

        status_counts[status] += 1

        linked_defects = as_list(raw_result.get("defect_ids"))
        unknown_defects = [item for item in linked_defects if item not in defect_by_id]
        if unknown_defects:
            errors.append(f"{label} 关联了不存在的缺陷ID: {', '.join(unknown_defects)}")

        if status == "失败" and not (linked_defects or open_defects_by_case.get(case_id)):
            errors.append(f"{label} 失败用例必须关联缺陷: {case_id} {title}")
        if status == "阻塞" and not (text(raw_result.get("blocker_reason")) or text(raw_result.get("note"))):
            errors.append(f"{label} 阻塞用例必须填写 blocker_reason 或 note: {case_id}")
        if status == "待确认" and not (text(raw_result.get("confirm_owner")) or text(raw_result.get("note"))):
            errors.append(f"{label} 待确认用例必须填写 confirm_owner 或 note: {case_id}")
        if priority in {"P0", "P1"} and status in {"失败", "阻塞"}:
            high_priority_failed_or_blocked.append(case_id)
        if raw_result.get("human_assisted") is True and not (text(raw_result.get("confirmation")) or text(raw_result.get("note"))):
            warnings.append(f"{label} human_assisted=true 时建议填写 confirmation 或 note: {case_id}")
        if surface == "computer-use" and not (text(raw_result.get("confirmation")) or text(raw_result.get("note"))):
            warnings.append(f"{label} computer-use 执行建议填写 confirmation 或 note，说明是否涉及风险动作: {case_id}")

    duplicate_cases = {case_id for case_id in result_case_ids if case_id and result_case_ids.count(case_id) > 1}
    if duplicate_cases:
        errors.append(f"执行结果 case_id 重复: {', '.join(sorted(duplicate_cases))}")

    if recommendation == "通过" and (status_counts.get("失败") or status_counts.get("阻塞") or status_counts.get("待确认")):
        errors.append("存在失败/阻塞/待确认用例时，recommendation 不能为 通过")
    if high_priority_failed_or_blocked and recommendation in {"通过", "有条件通过"}:
        errors.append(f"P0/P1 存在失败或阻塞时，recommendation 不能为 {recommendation}: {', '.join(high_priority_failed_or_blocked)}")
    if open_s1_s2 and recommendation in {"通过", "有条件通过"}:
        errors.append(f"存在未关闭 S1/S2 缺陷时，recommendation 必须为 不建议上线 或更保守: {', '.join(open_s1_s2)}")
    if status_counts.get("阻塞") and recommendation in {"通过", "有条件通过"}:
        errors.append("存在阻塞用例时，recommendation 应为 阻塞无法判断，除非人工豁免并在 risks 中说明")

    if not results:
        warnings.append("results 为空，报告只能表达未执行或阻塞状态")
    if not text(meta.get("source_testcase_json")):
        warnings.append("meta.source_testcase_json 未填写，执行结果无法稳定追溯到 test-yl JSON")
    if not text(meta.get("execution_level")):
        warnings.append("meta.execution_level 未填写，建议记录执行等级")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate QA execution result JSON.")
    parser.add_argument("--input", required=True, help="Execution result JSON path.")
    parser.add_argument("--no-strict", action="store_true", help="Allow warnings.")
    args = parser.parse_args()

    try:
        data = load_json(args.input)
        errors, warnings = validate(data)
    except Exception as exc:  # noqa: BLE001 - command-line validator should report all load failures
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"[WARN] {warning}", file=sys.stderr)
    for error in errors:
        print(f"[ERROR] {error}", file=sys.stderr)

    if errors or (warnings and not args.no_strict):
        return 1
    print("执行结果 JSON 校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
