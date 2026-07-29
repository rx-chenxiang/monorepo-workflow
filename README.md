# Monorepo Workflow

[简体中文](./README.zh-CN.md) | English

Monorepo Workflow is an open-source workspace template for coordinating full-stack, multi-client product development with AI coding agents. It is designed for teams that need one backend API, multiple frontend clients, structured product docs, coding plans, and repeatable agent workflows in one repository.

## What This Project Provides

- A generic four-part workspace: backend API, admin dashboard, mobile / H5 portal, and PC website.
- Agent-friendly routing rules for deciding which project should be changed.
- Documentation templates for requirements, technical design, coding plans, module docs, and integration agreements.
- Codex and Cursor-compatible rules and agent definitions.
- A repository pull script for cloning or updating multiple project repositories from one config file.
- Guardrails for API-first frontend integration and avoiding mock-only development.

## Workspace Layout

```text
.
├── AGENTS.md                         # Agent and contributor guide
├── README.md                         # English README
├── README.zh-CN.md                   # Chinese README
├── api/                              # Backend API docs and agent entry
├── fornt_admin/                      # Admin dashboard docs and agent entry
├── m_front/                          # Mobile / H5 portal docs and agent entry
├── pc_fornt/                         # PC website docs and agent entry
├── docs/                             # Workspace-level requirements and designs
├── .codex/                           # Source of truth for Codex rules, agents, skills
├── .cursor/                          # Cursor mirror for rules and agents
├── scripts/sync-codex-to-cursor.sh   # Sync .codex rules and agents to .cursor
├── pull_repos.sh                     # Clone / pull repositories from repos.conf
└── repos.conf                        # Repository source configuration template
```

## Project Roles

| Project | Directory | Role |
|---------|-----------|------|
| Backend API | `api/` | API service, authentication, domain services, data access |
| Admin dashboard | `fornt_admin/` | Internal operations and management UI |
| Mobile portal | `m_front/` | User-facing mobile, H5, or portal client |
| PC website | `pc_fornt/` | Public website, marketing site, or brand site |

> Note: `fornt_admin` and `pc_fornt` are intentionally preserved as directory names for compatibility with the current template. Aliases such as `front_admin` and `pc_front` are documented for agent routing.

## Quick Start

Clone this repository:

```bash
git clone https://github.com/rx-chenxiang/monorepo-workflow.git
cd monorepo-workflow
```

Check the pull script:

```bash
bash tests/pull_repos_test.sh
```

Configure actual repositories in `repos.conf`, then list selected repositories:

```bash
./pull_repos.sh --workspace general --list
```

Clone or update configured repositories:

```bash
./pull_repos.sh --target-dir /path/to/workspace --workspace general
```

## Repository Configuration

`repos.conf` uses this format:

```text
[workspace_name]
[transport]git_url|branch(optional)|target_dir(optional)|project_id(optional)
```

Example:

```text
[general]
[https]https://github.com/your-org/api.git|main|api|api
[https]https://github.com/your-org/fornt_admin.git|main|fornt_admin|fornt_admin
[https]https://github.com/your-org/m_front.git|main|m_front|m_front
[https]https://github.com/your-org/pc_fornt.git|main|pc_fornt|pc_fornt
```

## Documentation Workflow

Workspace-level feature documents live under:

```text
docs/general/{feature-name}/
├── 需求文档/
├── 技术设计方案/
└── coding-plan/
```

Each project keeps long-lived implementation knowledge under its own `docs/` directory:

```text
{project}/docs/
├── README.md
├── modules/
├── codebase/
└── rules/
```

Module templates are available at:

- `api/docs/modules/_template.md`
- `fornt_admin/docs/modules/_template.md`
- `m_front/docs/modules/_template.md`
- `pc_fornt/docs/modules/_template.md`

## Agent Workflow

`.codex/` is the source of truth for AI agent configuration:

- `.codex/rules/project-routing.mdc`
- `.codex/rules/multi-project-workspace.mdc`
- `.codex/rules/project-workflow-api.mdc`
- `.codex/rules/project-workflow-front.mdc`
- `.codex/agents/`
- `.codex/skills/`

`.cursor/` mirrors only `README.md`, `rules/`, and `agents/`. After changing `.codex`, run:

```bash
./scripts/sync-codex-to-cursor.sh
```

## Integration Guardrails

- Frontend clients should integrate with the real `api/` contract.
- Mock-only frontend behavior should not replace backend integration.
- Multi-client features should document each client's responsibility.
- Integration assumptions should be recorded in `docs/general/workspace/联调约定.md` or in the feature technical design.

## What Is Tracked In The Root Repository

The root repository is meant to track:

- Workflow rules and agent definitions.
- Documentation templates.
- Project-level `AGENTS.md` and `docs/`.
- Repository management scripts.
- Workspace-level requirement and design docs.

Actual application source code under `api/`, `fornt_admin/`, `m_front/`, and `pc_fornt` can be managed by separate repositories. The root `.gitignore` keeps project docs trackable while ignoring unregistered application source by default.

## Verification

Run:

```bash
bash tests/pull_repos_test.sh
```

Expected output:

```text
pull_repos_test.sh passed
```

## Roadmap

- Add optional bootstrap scripts for creating real backend and frontend projects.
- Add CI checks for documentation links and rule synchronization.
- Add example `repos.conf` variants for HTTPS and SSH.
- Add contribution and license files for public collaboration.

## Contributing

Issues and pull requests are welcome. Please keep changes scoped, update both English and Chinese README files when public behavior changes, and keep `.codex` and `.cursor` synchronized through the sync script.

## License

No license file has been added yet. Add a `LICENSE` file before advertising this repository as reusable open-source software.

<!-- AIGC:cursor|author:沉香|lines:约165|dates:2026-07|功能说明:初始化开源英文README，介绍项目定位、目录结构、快速开始、文档流、Agent配置与开源注意事项 -->
