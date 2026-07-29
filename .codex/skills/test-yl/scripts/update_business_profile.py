#!/usr/bin/env python3
"""Append or create a reusable business knowledge profile."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [line.strip("- ").strip() for line in value.splitlines() if line.strip()]
    return [str(value).strip()]


def bullet_section(title: str, values: list[str]) -> list[str]:
    lines = [f"### {title}", ""]
    if values:
        lines.extend(f"- {value}" for value in values)
    else:
        lines.append("- 暂无")
    lines.append("")
    return lines


def collect_from_cases(data: dict[str, Any]) -> dict[str, list[str]]:
    profile = data.get("business_profile", {}) if isinstance(data.get("business_profile"), dict) else {}
    result = {
        "terms": as_list(profile.get("terms")),
        "roles": as_list(profile.get("roles")),
        "rules": as_list(profile.get("rules")),
        "interfaces": as_list(profile.get("interfaces")),
        "tables": as_list(profile.get("tables")),
        "risks": as_list(profile.get("risks")),
        "assumptions": as_list(profile.get("assumptions")),
    }

    for row in data.get("coverage_matrix", []):
        if not isinstance(row, dict):
            continue
        feature = row.get("功能点") or row.get("feature")
        api_or_table = row.get("数据表/接口") or row.get("api_or_table")
        if feature:
            result["rules"].append(str(feature))
        if api_or_table and str(api_or_table).strip() not in {"无", "待确认"}:
            result["interfaces"].append(str(api_or_table))

    for row in data.get("test_cases", []):
        if not isinstance(row, dict):
            continue
        platform = row.get("平台") or row.get("platform")
        page = row.get("页面") or row.get("page")
        function_module = row.get("功能模块") or row.get("function_module")
        if platform:
            result["terms"].append(f"平台：{platform}")
        if page:
            result["terms"].append(f"页面：{page}")
        if function_module:
            result["rules"].append(f"功能模块：{function_module}")

    for row in data.get("review_report", []):
        if not isinstance(row, dict):
            continue
        result_value = row.get("核对结果") or row.get("result")
        description = row.get("说明") or row.get("description")
        if result_value in {"待确认", "部分通过", "未通过"} and description:
            result["assumptions"].append(str(description))

    return {key: sorted(set(values)) for key, values in result.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Update business knowledge profile.")
    parser.add_argument("--input", required=True, help="Input testcase JSON path.")
    parser.add_argument("--profile", required=True, help="Business profile Markdown path.")
    parser.add_argument("--source", default="", help="Source requirement name or document.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    profile_path = Path(args.profile).expanduser()
    data = json.loads(input_path.read_text(encoding="utf-8"))
    profile = collect_from_cases(data)
    meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
    source = args.source or meta.get("requirement_name", "")

    existing = profile_path.read_text(encoding="utf-8") if profile_path.exists() else "# 业务知识画像\n\n"
    lines = [existing.rstrip(), "", f"## {date.today().isoformat()} {source}".rstrip(), ""]
    lines.extend(bullet_section("业务术语", profile["terms"]))
    lines.extend(bullet_section("角色权限", profile["roles"]))
    lines.extend(bullet_section("核心规则", profile["rules"]))
    lines.extend(bullet_section("接口/数据表/技术对象", profile["interfaces"] + profile["tables"]))
    lines.extend(bullet_section("风险点", profile["risks"]))
    lines.extend(bullet_section("待确认项", profile["assumptions"]))

    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(profile_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
