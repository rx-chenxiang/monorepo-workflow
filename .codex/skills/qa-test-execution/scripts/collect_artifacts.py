#!/usr/bin/env python3
"""Index QA artifacts under a directory."""

from __future__ import annotations

import argparse
from pathlib import Path


KINDS = {
    ".png": "截图",
    ".jpg": "截图",
    ".jpeg": "截图",
    ".webp": "截图",
    ".webm": "视频",
    ".mp4": "视频",
    ".zip": "Trace",
    ".har": "接口HAR",
    ".json": "JSON",
    ".log": "日志",
    ".txt": "文本",
    ".md": "Markdown",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect QA artifact index.")
    parser.add_argument("--dir", required=True, help="Artifact directory.")
    parser.add_argument("--output", required=True, help="Markdown index output.")
    args = parser.parse_args()

    root = Path(args.dir).expanduser().resolve()
    output = Path(args.output).expanduser()
    files = [path for path in root.rglob("*") if path.is_file()]
    lines = ["# 测试证据索引", "", f"目录：{root}", ""]
    if files:
        lines.append("| 类型 | 文件 | 大小 |")
        lines.append("|---|---|---:|")
        for path in sorted(files):
            kind = KINDS.get(path.suffix.lower(), "其他")
            size = path.stat().st_size
            lines.append(f"| {kind} | {path} | {size} |")
    else:
        lines.append("暂无证据文件。")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
