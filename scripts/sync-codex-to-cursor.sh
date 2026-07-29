#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$ROOT_DIR/.cursor/rules" "$ROOT_DIR/.cursor/agents"
cp "$ROOT_DIR/.codex/README.md" "$ROOT_DIR/.cursor/README.md"
cp "$ROOT_DIR/.codex/rules/"* "$ROOT_DIR/.cursor/rules/"
cp "$ROOT_DIR/.codex/agents/"* "$ROOT_DIR/.cursor/agents/"

echo "Synced .codex rules and agents to .cursor."

# AIGC:cursor|author:沉香|lines:约12|dates:2026-07 功能说明:新增Codex到Cursor规则与Agent镜像同步脚本，技能目录以.codex/skills为准不复制
