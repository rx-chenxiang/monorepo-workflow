#!/usr/bin/env python3
"""Summarize testcase JSON for QA execution planning."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ",".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize testcase JSON.")
    parser.add_argument("--input", required=True, help="Path to testcase JSON.")
    parser.add_argument("--output", help="Optional Markdown output path.")
    args = parser.parse_args()

    data = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    cases = data.get("test_cases", [])
    if not isinstance(cases, list):
        raise ValueError("test_cases must be a list")

    by_priority = Counter(text(case.get("priority") or case.get("优先级")) for case in cases)
    by_dimension = Counter(text(case.get("test_dimension") or case.get("测试维度")) for case in cases)
    by_platform = Counter(text(case.get("platform") or case.get("平台")) for case in cases)
    buckets: dict[str, list[str]] = defaultdict(list)

    for case in cases:
        case_id = text(case.get("case_id") or case.get("用例ID"))
        title = text(case.get("title") or case.get("标题"))
        priority = text(case.get("priority") or case.get("优先级"))
        dimension = text(case.get("test_dimension") or case.get("测试维度"))
        label = f"{case_id} {priority} {dimension} {title}".strip()
        if priority in {"P0", "P1"}:
            buckets["必测 P0/P1"].append(label)
        elif dimension in {"断网测试", "旧版本兼容", "连点测试", "测试经验"}:
            buckets["风险补充"].append(label)
        elif dimension in {"UI展示", "交互效果"}:
            buckets["页面交互与视觉"].append(label)
        else:
            buckets["常规功能"].append(label)

    lines = [
        "# 测试用例执行摘要",
        "",
        f"- 用例总数：{len(cases)}",
        f"- 优先级分布：{dict(by_priority)}",
        f"- 平台分布：{dict(by_platform)}",
        f"- 测试维度分布：{dict(by_dimension)}",
        "",
    ]
    for bucket, items in buckets.items():
        lines.extend([f"## {bucket}", ""])
        lines.extend(f"- {item}" for item in items)
        lines.append("")

    output = "\n".join(lines).rstrip() + "\n"
    if args.output:
        path = Path(args.output).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(str(path))
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
