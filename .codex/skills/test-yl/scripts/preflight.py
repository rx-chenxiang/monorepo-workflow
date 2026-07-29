#!/usr/bin/env python3
"""Preflight checks for testcase generation inputs and output location."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import tempfile
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".txt", ".docx", ".xlsx", ".pdf"}


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def add_issue(issues: list[str], message: str) -> None:
    issues.append(message)


def check_base_dependencies(errors: list[str]) -> None:
    if not has_module("openpyxl"):
        add_issue(errors, "缺少依赖 openpyxl，无法读取 .xlsx 或生成 Excel")


def check_input(path: Path, errors: list[str], warnings: list[str]) -> None:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        add_issue(errors, f"{path}: 不支持的文件类型 {suffix or '无后缀'}")
        return
    if not path.exists():
        add_issue(errors, f"{path}: 文件不存在")
        return
    if not path.is_file():
        add_issue(errors, f"{path}: 不是普通文件")
        return
    if not os.access(path, os.R_OK):
        add_issue(errors, f"{path}: 无读取权限")
        return

    if suffix == ".docx" and not has_module("docx"):
        add_issue(errors, f"{path}: 读取 .docx 需要 python-docx")
    elif suffix == ".xlsx" and not has_module("openpyxl"):
        add_issue(errors, f"{path}: 读取 .xlsx 需要 openpyxl")
    elif suffix == ".pdf" and not (has_module("pdfplumber") or has_module("pypdf")):
        add_issue(errors, f"{path}: 读取 .pdf 需要 pdfplumber 或 pypdf")

    if path.stat().st_size == 0:
        add_issue(warnings, f"{path}: 文件为空，请确认是否为有效需求文档")


def check_output_dir(path: Path, errors: list[str]) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        add_issue(errors, f"{path}: 无法创建输出目录: {exc}")
        return
    if not path.is_dir():
        add_issue(errors, f"{path}: 不是目录")
        return
    if not os.access(path, os.W_OK):
        add_issue(errors, f"{path}: 无写入权限")
        return

    try:
        with tempfile.NamedTemporaryFile(prefix=".test-yl-", dir=path, delete=True) as handle:
            handle.write(b"ok")
            handle.flush()
    except OSError as exc:
        add_issue(errors, f"{path}: 写入测试失败: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight checks for test-yl generation.")
    parser.add_argument("--input", action="append", default=[], help="Source document path. Repeat for multiple files.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated assets.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    check_base_dependencies(errors)
    for item in args.input:
        check_input(Path(item).expanduser(), errors, warnings)
    check_output_dir(Path(args.output_dir).expanduser(), errors)

    for warning in warnings:
        print(f"[WARN] {warning}", file=sys.stderr)
    for error in errors:
        print(f"[ERROR] {error}", file=sys.stderr)

    if errors:
        return 1
    print("test-yl 生成前检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
