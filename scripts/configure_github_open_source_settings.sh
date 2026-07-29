#!/usr/bin/env bash
set -euo pipefail

# Configure or inspect the public GitHub repository for open-source maintenance.
# Write mode requires token scopes/permissions for repository administration,
# metadata, and security settings. Check mode can read public repository fields
# without a token, but branch protection and security settings often require auth.

OWNER="${OWNER:-rx-chenxiang}"
REPO="${REPO:-monorepo-workflow}"
BRANCH="${BRANCH:-main}"
STATUS_CONTEXT="${STATUS_CONTEXT:-verify}"
TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
API_ROOT="https://api.github.com"
REPOSITORY="${OWNER}/${REPO}"
MODE="${1:-apply}"

usage() {
  cat <<'EOF'
Usage:
  scripts/configure_github_open_source_settings.sh
  scripts/configure_github_open_source_settings.sh --check

Environment:
  OWNER=rx-chenxiang
  REPO=monorepo-workflow
  BRANCH=main
  STATUS_CONTEXT=verify
  GH_TOKEN=... or GITHUB_TOKEN=...
EOF
}

if [[ "${MODE}" != "apply" && "${MODE}" != "--check" ]]; then
  usage >&2
  exit 2
fi

if [[ "${MODE}" == "apply" && -z "${TOKEN}" ]]; then
  cat >&2 <<'EOF'
Missing GH_TOKEN or GITHUB_TOKEN.

Create a fine-grained GitHub token for this repository with Administration
write permission, then run:

  GH_TOKEN=... bash scripts/configure_github_open_source_settings.sh

If the required status check name in GitHub UI is not "verify", pass it with:

  STATUS_CONTEXT="CI / verify" GH_TOKEN=... bash scripts/configure_github_open_source_settings.sh
EOF
  exit 1
fi

api() {
  local method="$1"
  local path="$2"
  local payload="${3:-}"

  if [[ -n "${payload}" ]]; then
    if [[ -n "${TOKEN}" ]]; then
      curl -fsS \
        -X "${method}" \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "${API_ROOT}${path}" \
        -d "${payload}" >/dev/null
    else
      curl -fsS \
        -X "${method}" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "${API_ROOT}${path}" \
        -d "${payload}" >/dev/null
    fi
  else
    if [[ -n "${TOKEN}" ]]; then
      curl -fsS \
        -X "${method}" \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "${API_ROOT}${path}" >/dev/null
    else
      curl -fsS \
        -X "${method}" \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "${API_ROOT}${path}" >/dev/null
    fi
  fi
}

api_read() {
  local path="$1"
  if [[ -n "${TOKEN}" ]]; then
    curl -fsS \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "${API_ROOT}${path}"
  else
    curl -fsS \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "${API_ROOT}${path}"
  fi
}

optional_api() {
  local label="$1"
  local method="$2"
  local path="$3"
  local payload="${4:-}"

  if api "${method}" "${path}" "${payload}"; then
    printf '[ok] %s\n' "${label}"
  else
    printf '[warn] %s failed; check repository plan, token permissions, or GitHub feature availability.\n' "${label}" >&2
  fi
}

check_settings() {
  printf '[check] Repository profile\n'
  local repo_check_json
  repo_check_json="$(mktemp)"
  api_read "/repos/${REPOSITORY}" >"${repo_check_json}"
  python3 - "${repo_check_json}" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as file:
    repo = json.load(file)
fields = [
    ("visibility", repo.get("visibility")),
    ("private", repo.get("private")),
    ("description", repo.get("description")),
    ("is_template", repo.get("is_template")),
    ("has_issues", repo.get("has_issues")),
    ("has_projects", repo.get("has_projects")),
    ("has_wiki", repo.get("has_wiki")),
    ("allow_squash_merge", repo.get("allow_squash_merge")),
    ("allow_merge_commit", repo.get("allow_merge_commit")),
    ("allow_rebase_merge", repo.get("allow_rebase_merge")),
    ("delete_branch_on_merge", repo.get("delete_branch_on_merge")),
]
for key, value in fields:
    print(f"  {key}: {value}")
print("  topics:", ", ".join(repo.get("topics") or []))
security = repo.get("security_and_analysis") or {}
for key, value in security.items():
    status = value.get("status") if isinstance(value, dict) else value
    print(f"  security_and_analysis.{key}: {status}")
PY
  rm -f "${repo_check_json}"

  printf '[check] Branch protection for %s\n' "${BRANCH}"
  if api_read "/repos/${REPOSITORY}/branches/${BRANCH}/protection" >/tmp/github_branch_protection_check.json 2>/dev/null; then
    python3 -c '
import json
with open("/tmp/github_branch_protection_check.json", "r", encoding="utf-8") as file:
    data = json.load(file)
checks = data.get("required_status_checks") or {}
reviews = data.get("required_pull_request_reviews") or {}
print("  required_status_checks.strict:", checks.get("strict"))
print("  required_status_checks.contexts:", ", ".join(checks.get("contexts") or []))
print("  enforce_admins:", bool((data.get("enforce_admins") or {}).get("enabled")))
print("  required_pull_request_reviews.required_approving_review_count:", reviews.get("required_approving_review_count"))
print("  required_linear_history:", bool((data.get("required_linear_history") or {}).get("enabled")))
print("  required_conversation_resolution:", bool((data.get("required_conversation_resolution") or {}).get("enabled")))
print("  allow_force_pushes:", bool((data.get("allow_force_pushes") or {}).get("enabled")))
print("  allow_deletions:", bool((data.get("allow_deletions") or {}).get("enabled")))
'
  else
    printf '  unavailable: branch protection is disabled or the current token cannot read it.\n'
  fi

  printf '[check] Optional security endpoints\n'
  if api_read "/repos/${REPOSITORY}/private-vulnerability-reporting" >/dev/null 2>&1; then
    printf '  private_vulnerability_reporting: readable/enabled\n'
  else
    printf '  private_vulnerability_reporting: unavailable to current token or disabled\n'
  fi
}

if [[ "${MODE}" == "--check" ]]; then
  check_settings
  exit 0
fi

printf '[1/5] Updating repository profile and merge policy...\n'
api PATCH "/repos/${REPOSITORY}" "{
  \"description\": \"AI-assisted workspace template for coordinating backend, admin, mobile/H5, and PC projects with documentation-driven agent workflows.\",
  \"homepage\": \"\",
  \"private\": false,
  \"has_issues\": true,
  \"has_projects\": true,
  \"has_wiki\": false,
  \"has_downloads\": false,
  \"is_template\": true,
  \"allow_squash_merge\": true,
  \"allow_merge_commit\": false,
  \"allow_rebase_merge\": false,
  \"delete_branch_on_merge\": true,
  \"allow_update_branch\": true
}"

printf '[2/5] Updating repository topics...\n'
api PUT "/repos/${REPOSITORY}/topics" '{
  "names": [
    "ai-agents",
    "codex",
    "cursor",
    "monorepo",
    "workflow",
    "fullstack",
    "documentation",
    "developer-tools"
  ]
}'

printf '[3/5] Enabling branch protection on %s...\n' "${BRANCH}"
api PUT "/repos/${REPOSITORY}/branches/${BRANCH}/protection" "{
  \"required_status_checks\": {
    \"strict\": true,
    \"contexts\": [\"${STATUS_CONTEXT}\"]
  },
  \"enforce_admins\": true,
  \"required_pull_request_reviews\": {
    \"dismiss_stale_reviews\": true,
    \"require_code_owner_reviews\": false,
    \"required_approving_review_count\": 1
  },
  \"restrictions\": null,
  \"required_linear_history\": true,
  \"allow_force_pushes\": false,
  \"allow_deletions\": false,
  \"block_creations\": false,
  \"required_conversation_resolution\": true,
  \"lock_branch\": false,
  \"allow_fork_syncing\": true
}"

printf '[4/5] Enabling security features where the account plan allows them...\n'
optional_api "Dependabot alerts" PUT "/repos/${REPOSITORY}/vulnerability-alerts"
optional_api "Dependabot security updates" PUT "/repos/${REPOSITORY}/automated-security-fixes"
optional_api "Private vulnerability reporting" PUT "/repos/${REPOSITORY}/private-vulnerability-reporting"
optional_api "Secret scanning and push protection" PATCH "/repos/${REPOSITORY}" '{
  "security_and_analysis": {
    "secret_scanning": { "status": "enabled" },
    "secret_scanning_push_protection": { "status": "enabled" }
  }
}'

printf '[5/5] Done. Verify in GitHub Settings that the required status context is correct: %s\n' "${STATUS_CONTEXT}"
check_settings
