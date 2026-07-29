#!/usr/bin/env python3
"""Write testcase Markdown from JSON."""

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
        return "\n".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def numbered(value: Any) -> str:
    raw = text(value)
    if not raw:
        return ""
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return ""
    if all(re.match(r"^\s*\d+[\.、)]\s*", line) for line in lines):
        return "\n".join(lines)
    if len(lines) == 1:
        return lines[0]
    return "\n".join(f"{index}. {line}" for index, line in enumerate(lines, start=1))


def bullet(value: str) -> str:
    return value.replace("\n", "<br>")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write testcase Markdown.")
    parser.add_argument("--input", required=True, help="Input JSON path.")
    parser.add_argument("--output", required=True, help="Output Markdown path.")
    args = parser.parse_args()

    data = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
    title = meta.get("requirement_name") or meta.get("title") or "测试用例"

    lines: list[str] = [f"# {title} 测试用例", ""]

    lines.extend(["## 测试用例", ""])
    cases_by_group: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for case in rows(data, "test_cases"):
        key = (
            text(case.get("平台")) or "未标注平台",
            text(case.get("页面")) or "未标注页面",
            text(case.get("功能模块")) or "未标注功能模块",
        )
        cases_by_group[key].append(case)

    for (platform, page, function_module), cases in cases_by_group.items():
        lines.extend([f"### {platform} / {page} / {function_module}", ""])
        for case in cases:
            case_id = text(case.get("用例ID")) or "未编号"
            case_title = text(case.get("标题")) or "未命名用例"
            lines.extend(
                [
                    f"#### {case_id} {case_title}",
                    "",
                    f"- 目录：{text(case.get('目录'))}",
                    f"- 平台：{text(case.get('平台'))}",
                    f"- 页面：{text(case.get('页面'))}",
                    f"- 功能模块：{text(case.get('功能模块'))}",
                    f"- 测试维度：{text(case.get('测试维度'))}",
                    f"- 优先级：{text(case.get('优先级'))}",
                    f"- 类型：{text(case.get('类型'))}",
                    f"- 关联需求：{text(case.get('关联需求'))}",
                    f"- 关联测试点：{text(case.get('关联测试点'))}",
                    f"- 标签：{text(case.get('标签'))}",
                    f"- 来源文档：{text(case.get('source_doc'))}",
                    f"- 来源章节：{text(case.get('source_heading'))}",
                    f"- 来源摘录：{text(case.get('source_excerpt'))}",
                    "",
                    "**前置条件**",
                    "",
                    text(case.get("前置条件")) or "无",
                    "",
                    "**测试数据**",
                    "",
                    text(case.get("测试数据")) or "无",
                    "",
                    "**步骤描述**",
                    "",
                    numbered(case.get("步骤描述")) or "无",
                    "",
                    "**预期结果**",
                    "",
                    numbered(case.get("预期结果")) or "无",
                    "",
                    f"**验证层级**：{text(case.get('验证层级')) or '无'}",
                    "",
                    f"**备注**：{text(case.get('备注')) or '无'}",
                    "",
                ]
            )

    coverage = rows(data, "coverage_matrix")
    if coverage:
        lines.extend(["## 测试点覆盖矩阵", "", "| 需求ID | 需求名称 | 功能点 | 测试点ID | 关联用例ID | 覆盖状态 | 来源章节 | 来源摘录 |", "|---|---|---|---|---|---|---|---|"])
        for item in coverage:
            lines.append(
                "| {req} | {name} | {feature} | {point} | {cases} | {status} | {heading} | {excerpt} |".format(
                    req=bullet(text(item.get("需求ID"))),
                    name=bullet(text(item.get("需求名称"))),
                    feature=bullet(text(item.get("功能点"))),
                    point=bullet(text(item.get("测试点ID"))),
                    cases=bullet(text(item.get("关联用例ID"))),
                    status=bullet(text(item.get("覆盖状态"))),
                    heading=bullet(text(item.get("source_heading"))),
                    excerpt=bullet(text(item.get("source_excerpt"))),
                )
            )
        lines.append("")

    review = rows(data, "review_report")
    if review:
        lines.extend(["## 二次核对报告", "", "| 核对维度 | 核对结果 | 说明 |", "|---|---|---|"])
        for item in review:
            lines.append(
                f"| {bullet(text(item.get('核对维度')))} | {bullet(text(item.get('核对结果')))} | {bullet(text(item.get('说明')))} |"
            )
        lines.append("")

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
