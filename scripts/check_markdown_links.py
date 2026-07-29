#!/usr/bin/env python3
"""检查公开 Markdown 文档中的本地链接是否指向真实文件。"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent
PUBLIC_FILES = (
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "AGENTS.md",
)
PUBLIC_DIRECTORIES = (
    "docs",
    "api/docs",
    "fornt_admin/docs",
    "m_front/docs",
    "pc_fornt/docs",
    ".github",
)
LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
SKIPPED_SCHEMES = {"http", "https", "mailto", "tel", "data"}


def markdown_files() -> list[Path]:
    """收集稳定公开文档，避免把第三方 Skill 内部链接纳入根仓校验。"""

    files = [ROOT / name for name in PUBLIC_FILES if (ROOT / name).is_file()]
    for directory in PUBLIC_DIRECTORIES:
        base = ROOT / directory
        if base.is_dir():
            files.extend(base.rglob("*.md"))
    return sorted(set(files))


def local_target(raw_target: str) -> str | None:
    """从 Markdown 链接中提取不含标题、锚点和 URL 编码的本地路径。"""

    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(" ", 1)[0]

    target = unquote(target)
    parsed = urlparse(target)
    if parsed.scheme.lower() in SKIPPED_SCHEMES or target.startswith("#"):
        return None

    return target.split("#", 1)[0] or None


def main() -> int:
    failures: list[str] = []

    for document in markdown_files():
        content = document.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in LINK_PATTERN.finditer(line):
                target = local_target(match.group(1))
                if target is None:
                    continue

                resolved = (document.parent / target).resolve()
                if not resolved.exists():
                    relative_document = document.relative_to(ROOT)
                    failures.append(f"{relative_document}:{line_number}: {target}")

    if failures:
        print("发现无效的本地 Markdown 链接：", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print(f"Markdown link check passed ({len(markdown_files())} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
