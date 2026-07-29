<div align="center">
  <h1>Monorepo Workflow</h1>
  <p><strong>An AI-assisted operating system for full-stack, multi-client delivery.</strong></p>
  <p>Coordinate requirements, API contracts, four project repositories, agent workflows, integration, and durable documentation from one workspace.</p>
  <p>
    <a href="./README.zh-CN.md">简体中文</a> ·
    <a href="./docs/guides/quick-start.md">Quick start</a> ·
    <a href="./docs/guides/workspace-architecture.md">Architecture</a> ·
    <a href="./CONTRIBUTING.md">Contributing</a>
  </p>
  <p>
    <a href="https://github.com/rx-chenxiang/monorepo-workflow/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/rx-chenxiang/monorepo-workflow/actions/workflows/ci.yml/badge.svg"></a>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-2ea44f.svg"></a>
  </p>
</div>

> Define requirements, boundaries, and contracts first; then let people and agents build and verify in the right project.

```text
requirements → technical design → coding plan → API → clients → integration / acceptance → durable documentation
```

Monorepo Workflow is a **workspace template and collaboration convention**, not a generated business application. It is designed for teams that keep backend and frontend code in separate Git repositories but need one reliable place for cross-project context.

## Why This Exists

Multi-client products often fail from inconsistent context rather than missing code: requirements are scattered, API contracts drift, agents edit the wrong project, frontends rely on mocks, and delivery knowledge disappears after a release.

This repository turns those failure points into explicit structure:

| Included | What it gives you |
|---|---|
| Four-project workspace | One backend, admin dashboard, mobile / H5 portal, and PC website under a shared operating model |
| Documentation-driven delivery | Separate feature delivery records from long-lived project knowledge |
| Agent routing | Map natural-language requests to the correct role, workflow, and project scope |
| API-first integration | Integrate clients with real backend contracts instead of mock-only flows |
| Multi-repository management | Preview, clone, or update real project repositories from `repos.conf` |
| Cross-tool configuration | Keep `.codex/` authoritative and generate the supported Cursor mirror |

## Choose an Adoption Path

| Path | Best for | Start here |
|---|---|---|
| Use as a template | A new multi-client workspace | Clone this repository and replace the examples in `repos.conf` |
| Connect existing repositories | A product already split across several Git repositories | Keep this root as the coordination repo and point `repos.conf` at the real repositories |
| Adopt only the workflow assets | A team that already has its own monorepo layout | Copy and adapt `AGENTS.md`, `.codex/`, and the relevant documentation templates |

Do not stack multiple copies of the same rules or Skills into one tool configuration. Pick one source of truth and document any generated mirrors.

## Quick Start

```bash
git clone https://github.com/rx-chenxiang/monorepo-workflow.git
cd monorepo-workflow

# Run the baseline checks
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py

# Edit repos.conf, then preview the repositories that would be touched
./pull_repos.sh --workspace general --list
```

After reviewing the selection, clone or update the configured repositories:

```bash
./pull_repos.sh --target-dir /path/to/workspace --workspace general
```

Continue with the [quick-start guide](./docs/guides/quick-start.md) and [repository configuration guide](./docs/guides/repository-configuration.md).

## How the Workspace Is Organized

```text
monorepo-workflow/
├── AGENTS.md              # Human / agent entry point and safe-change boundaries
├── .codex/                # Source of truth for rules, agents, and Skills
├── .cursor/               # Generated mirror of supported .codex assets
├── api/                   # Backend entry point and long-lived project docs
├── fornt_admin/           # Admin dashboard entry point and project docs
├── m_front/               # Mobile / H5 portal entry point and project docs
├── pc_fornt/              # PC website entry point and project docs
├── docs/
│   ├── guides/            # Stable public guides
│   ├── general/           # Cross-project feature delivery documents
│   └── _template/         # Skeleton copied for a new feature
├── scripts/               # Maintenance and verification scripts
└── tests/                 # Regression tests
```

The root repository tracks collaboration assets and project documentation. Real application source code can remain in four independent Git repositories. `fornt_admin` and `pc_fornt` are intentionally retained for compatibility; agent routing also recognizes `front_admin` and `pc_front`.

Read the [workspace architecture guide](./docs/guides/workspace-architecture.md) for ownership boundaries and the complete information flow.

## Project Responsibilities

| Project | Directory | Responsibility |
|---|---|---|
| Backend API | `api/` | APIs, authentication, domain services, data access, async jobs |
| Admin dashboard | `fornt_admin/` | Internal operations, administration, and back-office users |
| Mobile portal | `m_front/` | User-facing mobile, H5, and portal experiences |
| PC website | `pc_fornt/` | Public, marketing, and brand website experiences |

## Documentation and Agent Workflow

| Goal | Start here |
|---|---|
| Understand the human-agent execution model | [Agent workflow](./docs/guides/agent-workflow.md) |
| Start a cross-project feature | [Documentation center](./docs/README.md) |
| Configure actual business repositories | [Repository configuration](./docs/guides/repository-configuration.md) |
| Understand project boundaries | [Workspace architecture](./docs/guides/workspace-architecture.md) |
| Extend Codex or Cursor configuration | [.codex guide](./.codex/README.md) |
| Prepare a public release | [Open-source release checklist](./docs/guides/open-source-release-checklist.md) |

Cross-project feature documents live under:

```text
docs/general/{feature-name}/
├── 需求文档/
├── 技术设计方案/
└── coding-plan/
```

Reusable implementation knowledge belongs in each project's `{project}/docs/` directory. This keeps a feature's delivery trail separate from durable project knowledge.

## Source-of-Truth Rules

- Root `AGENTS.md` defines workspace routing, documentation order, and safe-change boundaries.
- `.codex/` is authoritative for rules, specialized agents, and Skills.
- `.cursor/` is a generated compatibility mirror, not a second editing source.
- `docs/general/` records feature delivery; `{project}/docs/` records long-lived implementation knowledge.
- Frontends integrate against the real `api/` contract; mock-only behavior is not an integration substitute.

After changing `.codex/README.md`, `.codex/rules/`, or `.codex/agents/`, run:

```bash
./scripts/sync-codex-to-cursor.sh
```

## Verification

```bash
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py
```

The same checks run in GitHub Actions through [`.github/workflows/ci.yml`](./.github/workflows/ci.yml).

## Project Status and Roadmap

The current repository provides a reusable coordination layer, documentation system, repository pull tooling, and Codex / Cursor workflow assets. It does not bootstrap application frameworks or deploy business services.

Planned improvements:

- Optional bootstrap scripts for real backend and frontend projects.
- More tests for repository safety and configuration edge cases.
- Versioned releases and migration notes for workflow changes.
- More reusable agent workflows and acceptance assets.

See [CHANGELOG.md](./CHANGELOG.md) for notable changes.

## Community

Issues and pull requests are welcome. Read [CONTRIBUTING.md](./CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing. Report vulnerabilities through [SECURITY.md](./SECURITY.md), not a public issue.

## License

The repository's original content is available under the [MIT License](./LICENSE). Bundled or adapted third-party components retain their original copyright and license terms; see [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).
