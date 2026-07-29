#!/usr/bin/env python3
"""Build a Markdown QA report from execution result JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "<br>".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def table_row(values: list[Any]) -> str:
    escaped = [text(value).replace("|", "\\|") for value in values]
    return "| " + " | ".join(escaped) + " |"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build QA test report Markdown.")
    parser.add_argument("--input", required=True, help="Execution result JSON.")
    parser.add_argument("--output", required=True, help="Markdown output path.")
    args = parser.parse_args()

    data = json.loads(Path(args.input).expanduser().read_text(encoding="utf-8"))
    meta = data.get("meta", {}) if isinstance(data.get("meta"), dict) else {}
    results = data.get("results", [])
    defects = data.get("defects", [])
    risks = data.get("risks", [])
    artifacts = data.get("artifacts", [])
    if not isinstance(results, list):
        raise ValueError("results must be a list")
    if not isinstance(defects, list):
        raise ValueError("defects must be a list")

    status_counts = Counter(text(item.get("status")) for item in results if isinstance(item, dict))
    high_priority_failed_or_blocked = [
        text(item.get("case_id"))
        for item in results
        if isinstance(item, dict)
        and text(item.get("priority")) in {"P0", "P1"}
        and text(item.get("status")) in {"失败", "阻塞"}
    ]
    open_s1_s2 = [
        item for item in defects
        if isinstance(item, dict)
        and text(item.get("severity")) in {"S1", "S2", "S1阻断", "S2严重"}
        and text(item.get("status")) not in {"已关闭", "关闭", "closed"}
    ]
    recommendation = text(meta.get("recommendation"))
    if not recommendation:
        if status_counts.get("阻塞", 0):
            recommendation = "阻塞无法判断"
        elif open_s1_s2 or high_priority_failed_or_blocked:
            recommendation = "不建议上线"
        elif status_counts.get("失败", 0):
            recommendation = "不建议上线"
        elif defects or risks:
            recommendation = "有条件通过"
        else:
            recommendation = "通过"

    title = text(meta.get("requirement")) or "测试报告"
    lines = [
        f"# {title} 测试报告",
        "",
        "## 基本信息",
        "",
        table_row(["字段", "内容"]),
        table_row(["---", "---"]),
        table_row(["项目", meta.get("project", "")]),
        table_row(["环境", meta.get("environment", "")]),
        table_row(["测试类型", meta.get("test_type", "")]),
        table_row(["执行等级", meta.get("execution_level", "")]),
        table_row(["执行时间", meta.get("executed_at", datetime.now().strftime("%Y-%m-%d %H:%M"))]),
        table_row(["执行人", meta.get("executor", "Codex")]),
        "",
        "## 结论",
        "",
        table_row(["指标", "数量"]),
        table_row(["---", "---:"]),
        table_row(["用例总数", len(results)]),
        table_row(["通过", status_counts.get("通过", 0)]),
        table_row(["失败", status_counts.get("失败", 0)]),
        table_row(["阻塞", status_counts.get("阻塞", 0)]),
        table_row(["跳过", status_counts.get("跳过", 0)]),
        table_row(["待确认", status_counts.get("待确认", 0)]),
        table_row(["未执行", status_counts.get("未执行", 0)]),
        "",
        f"上线建议：{recommendation}",
        "",
        "## 缺陷清单",
        "",
        table_row(["ID", "严重级别", "标题", "关联用例", "状态", "证据"]),
        table_row(["---", "---", "---", "---", "---", "---"]),
    ]

    if defects:
        for item in defects:
            if isinstance(item, dict):
                lines.append(table_row([
                    item.get("id", ""),
                    item.get("severity", ""),
                    item.get("title", ""),
                    item.get("case_id", ""),
                    item.get("status", ""),
                    item.get("evidence", ""),
                ]))
    else:
        lines.append(table_row(["无", "", "", "", "", ""]))

    lines.extend(["", "## 风险与待确认", ""])
    if risks:
        lines.extend(f"- {text(item)}" for item in risks)
    else:
        lines.append("- 无")

    lines.extend(["", "## 证据索引", ""])
    if artifacts:
        for item in artifacts:
            lines.append(f"- {text(item)}")
    else:
        lines.append("- 无")

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
