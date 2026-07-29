#!/usr/bin/env python3
"""Write a Mermaid mindmap for testcase design from JSON."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ALIASES = {
    "case_id": "用例ID",
    "module": "目录",
    "platform": "平台",
    "page": "页面",
    "function_module": "功能模块",
    "test_dimension": "测试维度",
    "title": "标题",
    "requirement_id": "关联需求",
    "test_point_id": "关联测试点",
    "priority": "优先级",
    "type": "类型",
    "requirement_name": "需求名称",
    "feature": "功能点",
    "coverage_status": "覆盖状态",
}


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {ALIASES.get(key, key): value for key, value in row.items()}


def rows(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key, [])
    if not isinstance(value, list):
        return []
    normalized_rows = []
    for row in value:
        if not isinstance(row, dict):
            continue
        normalized = normalize_row(row)
        if key == "coverage_matrix":
            if "requirement_id" in row:
                normalized["需求ID"] = row["requirement_id"]
            if "test_point_id" in row:
                normalized["测试点ID"] = row["test_point_id"]
        normalized_rows.append(normalized)
    return normalized_rows


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ",".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def split_ids(value: Any) -> list[str]:
    raw = text(value)
    if not raw:
        return []
    return [item for item in re.split(r"[,，;；\s\n]+", raw) if item]


def node(value: str) -> str:
    value = value.replace('"', "'").replace("\n", " ").strip()
    return value[:80] if value else "未命名"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write Mermaid testcase mindmap.")
    parser.add_argument("--input", required=True, help="Input JSON path.")
    parser.add_argument("--output", required=True, help="Output Markdown path.")
    args = parser.parse_args()

    data = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
    title = text(meta.get("requirement_name") or meta.get("title") or "测试设计")

    coverage_by_req: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in rows(data, "coverage_matrix"):
        coverage_by_req[text(item.get("需求ID")) or "REQ-未编号"].append(item)

    cases_by_point: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in rows(data, "test_cases"):
        for point_id in split_ids(case.get("关联测试点")):
            cases_by_point[point_id].append(case)

    cases_by_platform_page: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for case in rows(data, "test_cases"):
        key = (
            text(case.get("平台")) or "未标注平台",
            text(case.get("页面")) or "未标注页面",
            text(case.get("功能模块")) or "未标注功能模块",
        )
        cases_by_platform_page[key].append(case)

    lines = [f"# {title} 测试设计脑图", "", "```mermaid", "mindmap", f'  root(("{node(title)}"))']

    for (platform, page, function_module), cases in cases_by_platform_page.items():
        lines.append(f'    {node(platform)}')
        lines.append(f'      {node(page)}')
        lines.append(f'        {node(function_module)}')
        for case in cases:
            case_id = text(case.get("用例ID"))
            priority = text(case.get("优先级"))
            case_type = text(case.get("类型"))
            dimension = text(case.get("测试维度"))
            case_title = text(case.get("标题"))
            lines.append(f'          {node(case_id + " " + priority + " " + case_type + " " + dimension)}')
            lines.append(f'            {node(case_title)}')

    lines.append("    覆盖矩阵")

    for requirement_id, items in coverage_by_req.items():
        requirement_name = text(items[0].get("需求名称")) if items else ""
        lines.append(f'      {node(requirement_id + " " + requirement_name)}')
        for item in items:
            point_id = text(item.get("测试点ID"))
            feature = text(item.get("功能点"))
            status = text(item.get("覆盖状态"))
            lines.append(f'        {node(point_id + " " + feature + " [" + status + "]")}')
            for case in cases_by_point.get(point_id, []):
                case_id = text(case.get("用例ID"))
                case_title = text(case.get("标题"))
                priority = text(case.get("优先级"))
                case_type = text(case.get("类型"))
                dimension = text(case.get("测试维度"))
                lines.append(f'          {node(case_id + " " + priority + " " + case_type + " " + dimension)}')
                lines.append(f'            {node(case_title)}')

    lines.extend(["```", ""])

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
