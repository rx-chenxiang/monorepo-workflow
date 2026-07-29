#!/usr/bin/env python3
"""Preflight QA execution inputs and optional URLs."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "project",
    "requirement",
    "test_type",
    "frontend_url",
    "account_note",
    "data_permission",
    "device_scope",
]


def load_intake(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    intake_path = Path(path).expanduser()
    if not intake_path.exists():
        raise ValueError(f"intake file does not exist: {intake_path}")
    value = json.loads(intake_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("intake JSON must be an object")
    return value


def check_url(url: str, timeout: int) -> tuple[bool, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "qa-test-execution-preflight"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return True, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return exc.code < 500, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - report exact preflight failure
        return False, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight QA execution environment.")
    parser.add_argument("--intake", help="Path to intake JSON.")
    parser.add_argument("--url", action="append", default=[], help="URL to check; can repeat.")
    parser.add_argument("--timeout", type=int, default=10, help="URL timeout seconds.")
    args = parser.parse_args()

    try:
        intake = load_intake(args.intake)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    urls = list(args.url)
    for key in ["frontend_url", "admin_url", "api_doc_url"]:
        value = intake.get(key)
        if isinstance(value, str) and value.strip():
            urls.append(value.strip())

    missing = [field for field in REQUIRED_FIELDS if not str(intake.get(field, "")).strip()]
    if missing:
        print("Missing intake fields: " + ", ".join(missing))
    else:
        print("Required intake fields: OK")

    failed_urls = []
    for url in urls:
        ok, detail = check_url(url, args.timeout)
        status = "OK" if ok else "FAIL"
        print(f"{status} {url} -> {detail}")
        if not ok:
            failed_urls.append(url)

    if missing or failed_urls:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
