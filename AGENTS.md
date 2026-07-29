# Agents Guide

## Current File Purpose

This file is the shared operating guide for AI coding agents and human contributors working in this repository. It defines the workspace layout, routing rules, documentation expectations, and safe-change boundaries for the monorepo workflow template.

## Language And Communication

1. Use Simplified Chinese for maintainer-facing explanations unless the user explicitly asks for another language.
2. Keep code identifiers in the language and style already used by the target project.
3. Add clear Chinese comments for generated project files when comments are useful.
4. Keep changes small, readable, and aligned with KISS and SOLID principles.
5. If the target project, target app, or intended behavior is ambiguous, ask one concise clarification before changing code.
6. Do not rewrite unrelated files, shared components, or global configuration unless the task explicitly requires it.
7. After implementation, perform a basic self-check and document what was verified.

## Workspace Model

This repository is a generic full-stack, multi-client workspace template. The starter registry coordinates one backend and three frontend clients:

| Project ID | Directory | Role |
|------------|-----------|------|
| `api` | `api/` | Backend API |
| `fornt_admin` | `fornt_admin/` | Admin dashboard frontend |
| `m_front` | `m_front/` | Mobile / H5 portal frontend |
| `pc_fornt` | `pc_fornt/` | PC website frontend |

The directory names `fornt_admin` and `pc_fornt` are intentionally preserved for compatibility with the current template. Agents should also recognize the aliases `front_admin` and `pc_front` when interpreting user intent.

This four-project registry is the default topology, not the workspace limit. Maintainers may add project groups, services, clients, internal tools, or other repositories by extending the root registry, routing rules, `repos.conf`, and the new project's `AGENTS.md` and documentation indexes together.

## Routing Rules

Use the root registry and `.codex/rules/project-routing.mdc` before making changes.

| User Intent | Target Scope |
|-------------|--------------|
| `full stack`, `all`, `general`, `multi-client`, `四端`, `全栈` | `api` + `fornt_admin` + `m_front` + `pc_fornt` |
| `backend`, `API`, `server`, `接口`, `后端` | `api/` |
| `admin`, `dashboard`, `管理平台`, `管理后台` | `fornt_admin/` |
| `mobile`, `H5`, `portal`, `门户端`, `移动端` | `m_front/` |
| `website`, `PC site`, `官网`, `PC前端` | `pc_fornt/` |

When the user only says "frontend" and the target client cannot be inferred from paths or prior context, ask whether the target is `fornt_admin`, `m_front`, or `pc_fornt`.

## Documentation Layout

Workspace-level requirement and design documents live under:

```text
docs/general/{feature-name}/
├── 需求文档/
├── 技术设计方案/
└── coding-plan/
```

Long-lived implementation knowledge lives inside each project directory:

```text
{project}/docs/
├── README.md
├── modules/
├── codebase/
└── rules/
```

Before coding in a project, read in this order:

1. Root `AGENTS.md`.
2. `.codex/rules/project-routing.mdc`.
3. The matched workflow under `.codex/rules/`.
4. `{project}/AGENTS.md`, if present.
5. `{project}/docs/README.md`.
6. `{project}/docs/modules/README.md`.
7. Related files under `{project}/docs/codebase/` or `{project}/docs/rules/`.

Do not invent module documentation paths. Use the actual links and indexes that exist in the target project.

## Development Rules

1. Prefer existing project conventions over new abstractions.
2. Keep the implementation inside the matched project unless the task explicitly requires multi-client changes.
3. Frontend clients must use the real backend contract from `api/`; do not add mock-only behavior for integration work.
4. Backend changes must preserve existing request validation, authentication, error handling, and response contracts unless a breaking change is explicitly requested.
5. Frontend changes must cover loading, empty, error, permission, and responsive states when relevant.
6. For multi-client tasks, report changes by project: backend, admin, mobile portal, PC website, and integration verification.

## Version-Control Policy

The root repository tracks workflow assets, agent rules, documentation templates, and project docs. Real application source code in `api/`, `fornt_admin/`, `m_front`, and `pc_fornt` may be managed by separate repositories.

The root `.gitignore` intentionally keeps each project's `AGENTS.md` and `docs/` templates trackable while ignoring unregistered application source files by default.

## Important Files

| Purpose | Path |
|---------|------|
| Public overview | `README.md` |
| Chinese overview | `README.zh-CN.md` |
| Codex configuration source | `.codex/` |
| Cursor mirror | `.cursor/` |
| Codex-to-Cursor sync script | `scripts/sync-codex-to-cursor.sh` |
| Repository pull configuration | `repos.conf` |
| Repository pull script | `pull_repos.sh` |
| Integration agreement template | `docs/general/workspace/联调约定.md` |
| Public documentation index | `docs/README.md` |
| Open-source release checklist | `docs/guides/open-source-release-checklist.md` |
| Contribution and security policies | `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` |
| License and third-party notices | `LICENSE`, `THIRD_PARTY_NOTICES.md` |
| Baseline CI | `.github/workflows/ci.yml` |

## Maintenance Notes

1. Treat `.codex/` as the source of truth for rules and agents.
2. Run `scripts/sync-codex-to-cursor.sh` after changing `.codex/README.md`, `.codex/rules/`, or `.codex/agents/`.
3. Keep `README.md` and `README.zh-CN.md` aligned when changing public-facing project behavior.
4. Keep module templates under all four project docs directories aligned in structure and intent.
5. When adding third-party Skills, scripts, or assets, preserve their license and update `THIRD_PARTY_NOTICES.md`.

<!-- AIGC:cursor|author:沉香|lines:约130|dates:2026-07|功能说明:重写开源版AGENTS指南，面向AI Agent与贡献者说明四端工作区、路由规则、文档结构和维护策略 -->
