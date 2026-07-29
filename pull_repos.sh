#!/usr/bin/env bash

set -u

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_LIST_FILE="${BASE_DIR}/repos.conf"
TARGET_ROOT="${PULL_REPOS_TARGET_DIR:-$BASE_DIR}"
TRANSPORT="${PULL_REPOS_TRANSPORT:-https}"

PULL_ARGS=(--ff-only)
FAILURES=()
WORKSPACE_FILTERS=()
PROJECT_FILTERS=()
LIST_ONLY=0
MATCHED_REPOS=0
HAS_REPO_ENTRY=0

log() {
  printf '%s\n' "$*"
}

usage() {
  cat <<'USAGE'
Usage:
  ./pull_repos.sh [options] [repos.conf]

Options:
  -c, --config FILE        Repository config file. Defaults to ./repos.conf.
  -d, --target-dir DIR     Clone/pull repositories under DIR. Defaults to this workspace.
  -w, --workspace NAME     Only pull a configured workspace section. Repeatable.
  -p, --project NAME       Only pull a project/repo directory. Repeatable.
  -t, --transport NAME     Pull tagged entries for a transport, such as https or ssh.
                           Defaults to https. Untagged entries are always eligible.
      --all-transports     Pull every configured transport entry.
      --list               List repositories selected by the filters without git calls.
  -h, --help               Show this help.

Config format:
  [workspace_name]
  [transport]git_url|branch(optional)|target_dir(optional)|project_id(optional)

Old entries using git_url|branch(optional) still work.
USAGE
}

trim() {
  local value="$*"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

abs_path() {
  local value="$1"

  if [[ "$value" == /* ]]; then
    printf '%s' "$value"
  else
    printf '%s/%s' "$(pwd)" "$value"
  fi
}

repo_dir_from_url() {
  local git_url="$1"
  local repo_name

  repo_name="${git_url%%\?*}"
  repo_name="${repo_name%/}"
  repo_name="${repo_name%.git}"
  repo_name="${repo_name##*/}"
  repo_name="${repo_name##*:}"

  printf '%s' "$repo_name"
}

require_arg() {
  local option="$1"
  local value="${2:-}"

  if [[ -z "$value" ]]; then
    log "Missing value for ${option}"
    exit 2
  fi
}

parse_args() {
  local positional_config_set=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -c|--config)
        require_arg "$1" "${2:-}"
        REPO_LIST_FILE="$2"
        shift 2
        ;;
      -d|--target-dir|--dest|--destination)
        require_arg "$1" "${2:-}"
        TARGET_ROOT="$2"
        shift 2
        ;;
      -w|--workspace)
        require_arg "$1" "${2:-}"
        WORKSPACE_FILTERS+=("$(trim "$2")")
        shift 2
        ;;
      -p|--project)
        require_arg "$1" "${2:-}"
        PROJECT_FILTERS+=("$(trim "$2")")
        shift 2
        ;;
      -t|--transport|--protocol)
        require_arg "$1" "${2:-}"
        TRANSPORT="$(trim "$2")"
        shift 2
        ;;
      --all-transports)
        TRANSPORT=""
        shift
        ;;
      --list)
        LIST_ONLY=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      --)
        shift
        if [[ $# -gt 0 ]]; then
          if [[ "$positional_config_set" -eq 1 ]]; then
            log "Only one positional config file is supported."
            exit 2
          fi
          REPO_LIST_FILE="$1"
          positional_config_set=1
          shift
        fi
        ;;
      -*)
        log "Unknown option: $1"
        usage
        exit 2
        ;;
      *)
        if [[ "$positional_config_set" -eq 1 ]]; then
          log "Only one positional config file is supported."
          exit 2
        fi
        REPO_LIST_FILE="$1"
        positional_config_set=1
        shift
        ;;
    esac
  done

  REPO_LIST_FILE="$(abs_path "$REPO_LIST_FILE")"
  TARGET_ROOT="$(abs_path "$TARGET_ROOT")"
}

workspace_matches() {
  local workspace="$1"
  local filter

  if [[ ${#WORKSPACE_FILTERS[@]} -eq 0 ]]; then
    return 0
  fi

  for filter in "${WORKSPACE_FILTERS[@]}"; do
    if [[ "$workspace" == "$filter" ]]; then
      return 0
    fi
  done

  return 1
}

project_matches() {
  local repo_name="$1"
  local target_dir="$2"
  local project_id="$3"
  local filter

  if [[ ${#PROJECT_FILTERS[@]} -eq 0 ]]; then
    return 0
  fi

  for filter in "${PROJECT_FILTERS[@]}"; do
    if [[ "$repo_name" == "$filter" || "$target_dir" == "$filter" || "$project_id" == "$filter" ]]; then
      return 0
    fi
  done

  return 1
}

transport_matches() {
  local entry_transport="$1"

  if [[ -z "$TRANSPORT" || -z "$entry_transport" ]]; then
    return 0
  fi

  [[ "$entry_transport" == "$TRANSPORT" ]]
}

display_name() {
  local workspace="$1"
  local project_id="$2"

  if [[ -n "$workspace" ]]; then
    printf '%s/%s' "$workspace" "$project_id"
  else
    printf '%s' "$project_id"
  fi
}

update_repo() {
  local workspace="$1"
  local entry="$2"
  local entry_transport="" raw_entry git_url branch configured_dir project_id unused repo_name
  local target_dir target_path name

  raw_entry="$entry"
  if [[ "$raw_entry" == \[*\]* ]]; then
    entry_transport="${raw_entry%%]*}"
    entry_transport="${entry_transport#[}"
    raw_entry="${raw_entry#*]}"
  fi

  IFS='|' read -r git_url branch configured_dir project_id unused <<< "$raw_entry"
  git_url="$(trim "$git_url")"
  branch="$(trim "${branch:-}")"
  configured_dir="$(trim "${configured_dir:-}")"
  project_id="$(trim "${project_id:-}")"

  if [[ -n "${unused:-}" || -z "${git_url:-}" ]]; then
    log "[skip] Invalid repo entry: $entry"
    return 1
  fi

  repo_name="$(repo_dir_from_url "$git_url")"
  if [[ -z "${repo_name:-}" ]]; then
    log "[skip] Cannot infer directory name from: $git_url"
    return 1
  fi

  if ! transport_matches "$entry_transport"; then
    return 0
  fi

  if ! workspace_matches "$workspace"; then
    return 0
  fi

  if [[ -z "$project_id" ]]; then
    project_id="$repo_name"
  fi

  if [[ -n "$configured_dir" ]]; then
    target_dir="$configured_dir"
  else
    target_dir="$repo_name"
  fi

  if ! project_matches "$repo_name" "$target_dir" "$project_id"; then
    return 0
  fi

  MATCHED_REPOS=$((MATCHED_REPOS + 1))
  name="$(display_name "$workspace" "$project_id")"

  if [[ "$target_dir" == /* ]]; then
    target_path="$target_dir"
  else
    target_path="${TARGET_ROOT}/${target_dir}"
  fi

  if [[ "$LIST_ONLY" -eq 1 ]]; then
    log "[repo] ${name} transport=${entry_transport:-untagged} branch=${branch:-current} dir=${target_path} url=${git_url}"
    return 0
  fi

  mkdir -p "$(dirname "$target_path")"

  if [[ -d "$target_path/.git" ]]; then
    log "[pull] ${name} -> ${target_path}"
    if [[ -n "${branch:-}" ]]; then
      git -C "$target_path" fetch origin "$branch" &&
        git -C "$target_path" checkout "$branch" &&
        git -C "$target_path" pull "${PULL_ARGS[@]}" origin "$branch"
    else
      git -C "$target_path" pull "${PULL_ARGS[@]}"
    fi
  elif [[ -e "$target_path" ]]; then
    log "[fail] ${target_path} exists but is not a git repository"
    false
  else
    log "[clone] ${name} -> ${target_path}"
    if [[ -n "${branch:-}" ]]; then
      git clone --branch "$branch" "$git_url" "$target_path"
    else
      git clone "$git_url" "$target_path"
    fi
  fi
}

main() {
  parse_args "$@"

  if [[ ! -f "$REPO_LIST_FILE" ]]; then
    log "Repository list file not found: $REPO_LIST_FILE"
    exit 1
  fi

  if [[ "$LIST_ONLY" -ne 1 ]]; then
    mkdir -p "$TARGET_ROOT"
  fi

  local entry line current_workspace=""
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    entry="$(trim "$line")"

    if [[ -z "$entry" || "$entry" == \#* ]]; then
      continue
    fi

    if [[ "$entry" =~ ^\[[^][]+\]$ ]]; then
      current_workspace="${entry:1:${#entry}-2}"
      continue
    fi

    HAS_REPO_ENTRY=1
    if ! update_repo "$current_workspace" "$entry"; then
      FAILURES+=("$entry")
      log "[fail] $entry"
    fi
  done < "$REPO_LIST_FILE"

  if [[ "$HAS_REPO_ENTRY" -eq 0 ]]; then
    log "No repositories configured. Edit $REPO_LIST_FILE first."
    exit 1
  fi

  if [[ "$MATCHED_REPOS" -eq 0 ]]; then
    log "No repositories matched the selected filters."
    exit 1
  fi

  if [[ ${#FAILURES[@]} -gt 0 ]]; then
    log "Finished with failures:"
    printf '  - %s\n' "${FAILURES[@]}"
    exit 1
  fi

  if [[ "$LIST_ONLY" -eq 1 ]]; then
    log "Listed ${MATCHED_REPOS} repositories."
  else
    log "All selected repositories are up to date."
  fi
}

main "$@"
