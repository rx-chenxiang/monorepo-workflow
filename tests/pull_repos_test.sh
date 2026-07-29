#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

CONFIG_FILE="$TMP_DIR/repos.conf"
TARGET_DIR="$TMP_DIR/checkouts"
BIN_DIR="$TMP_DIR/bin"
GIT_LOG="$TMP_DIR/git.log"

mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/git" <<'FAKE_GIT'
#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' "$*" >> "$GIT_LOG"

if [[ "${1:-}" == "clone" ]]; then
  shift
  branch=""
  if [[ "${1:-}" == "--branch" ]]; then
    branch="$2"
    shift 2
  fi
  url="$1"
  target="$2"
  mkdir -p "$target/.git"
  printf 'branch=%s url=%s target=%s\n' "$branch" "$url" "$target" >> "$GIT_LOG"
  exit 0
fi

if [[ "${1:-}" == "-C" ]]; then
  exit 0
fi

exit 0
FAKE_GIT
chmod +x "$BIN_DIR/git"

cat > "$CONFIG_FILE" <<'REPOS'
[general]
[https]https://example.com/your-org/api.git|main|api|api
[ssh]git@example.com:your-org/api.git|main|api|api
[https]https://example.com/your-org/fornt_admin.git|main|fornt_admin|fornt_admin
[https]https://example.com/your-org/m_front.git|main|m_front|m_front
[https]https://example.com/your-org/pc_fornt.git|main|pc_fornt|pc_fornt
REPOS

PATH="$BIN_DIR:$PATH" GIT_LOG="$GIT_LOG" \
  bash "$ROOT_DIR/pull_repos.sh" \
    --config "$CONFIG_FILE" \
    --target-dir "$TARGET_DIR" \
    --workspace general \
    --project m_front \
    --transport https

if [[ ! -d "$TARGET_DIR/m_front/.git" ]]; then
  echo "expected selected project to be cloned under target dir"
  exit 1
fi

if [[ -e "$TARGET_DIR/api" || -e "$TARGET_DIR/fornt_admin" || -e "$TARGET_DIR/pc_fornt" ]]; then
  echo "workspace/project filters cloned unexpected repositories"
  exit 1
fi

if ! grep -q 'url=https://example.com/your-org/m_front.git' "$GIT_LOG"; then
  echo "expected transport prefix to be removed from clone URL"
  exit 1
fi

if grep -q 'api.git\|fornt_admin.git\|pc_fornt.git\|\[https\]\|\[ssh\]' "$GIT_LOG"; then
  echo "unexpected repository or transport marker appeared in git calls"
  exit 1
fi

echo "pull_repos_test.sh passed"

# AIGC:cursor|author:沉香|lines:约78|dates:2026-07 功能说明:拉取脚本测试改为通用general四端配置，移除旧业务仓库样例
