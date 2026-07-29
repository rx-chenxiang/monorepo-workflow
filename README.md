<div align="center">
  <h1>Monorepo Workflow</h1>
  <p><strong>One developer. Every project. One shared context.</strong></p>
  <p>Run product, design, backend, frontend, testing, review, and documentation as one AI-assisted delivery system—without project silos.</p>
  <p><code>1 operator × shared context × specialist agents = company-wide delivery</code></p>
  <p>
    <a href="https://github.com/rx-chenxiang/monorepo-workflow/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/rx-chenxiang/monorepo-workflow/actions/workflows/ci.yml/badge.svg"></a>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-2ea44f.svg"></a>
  </p>
  <p>
    <a href="./README.zh-CN.md">简体中文</a> ·
    <a href="#30-second-start">Quick start</a> ·
    <a href="./docs/guides/workspace-architecture.md">Architecture</a> ·
    <a href="./CONTRIBUTING.md">Contributing</a>
  </p>
  <p><strong>Quick start:</strong> <code>git clone https://github.com/rx-chenxiang/monorepo-workflow.git</code></p>
</div>

![One person company-wide project delivery blueprint](./assets/readme/one-person-company-blueprint.png)

## 30-Second Start

```bash
git clone https://github.com/rx-chenxiang/monorepo-workflow.git
cd monorepo-workflow

# Verify the workspace
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py
```

Then point [`repos.conf`](./repos.conf) at your real repositories and preview the selection before cloning or updating anything:

```bash
./pull_repos.sh --workspace general --list
```

Continue with the [quick-start guide](./docs/guides/quick-start.md).

## The Problem It Solves

Most AI coding setups stop at the repository boundary. Every new repo means rebuilding context, repeating architectural decisions, reconnecting requirements, and manually handing work between product, design, development, testing, and documentation.

Monorepo Workflow adds a coordination layer above those repositories:

```text
idea → requirement → design → plan → build → test → review → document → improve
```

One operator keeps the goal. Specialist agents take the right role. Explicit routing sends work to the right project. Durable documentation carries knowledge into the next task.

## Why It Is Different

| Typical repo-by-repo workflow | Monorepo Workflow |
|---|---|
| Context resets when you switch repositories | Shared requirements, contracts, decisions, and project knowledge |
| Prompts decide scope ad hoc | Explicit role × project routing before changes begin |
| “Monorepo” means all source must share one Git history | A coordination repo can govern many independent repositories |
| Frontends drift toward local mocks | API-first integration keeps clients aligned with real contracts |
| Handoffs lose reasoning and implementation knowledge | Delivery docs and long-lived project docs preserve both |
| Adding a project means inventing a new process | Register another project or project group and reuse the workflow |

This is not a collection of clever prompts. It is a versioned operating model for how humans and agents understand, change, verify, and remember work across a company.

## One Person, the Whole Development Workflow

| Stage | Built-in capability |
|---|---|
| Discover | Turn raw ideas, PRDs, screenshots, and verbal requirements into structured plans |
| Design | Produce UI directions, prototypes, technical designs, and implementation briefs |
| Build | Route backend, admin, mobile, website, or future project work to the correct context |
| Verify | Execute code review, security review, functional testing, Playwright E2E, and acceptance workflows |
| Remember | Maintain requirements, decisions, module knowledge, regression notes, and changelogs |
| Operate | Preview, clone, update, and coordinate repositories without merging their Git histories |

The repository currently includes **12 specialized agents, 10 reusable Skills, and 11 routing / workflow rules**. They help a solo developer or small technical team cover the development workflow normally split across several roles.

## More Than Four Projects

The included registry starts with one backend and three clients:

```text
api · fornt_admin · m_front · pc_fornt
```

That is the starter topology, not the product boundary. `repos.conf` supports multiple workspace sections and arbitrary project IDs. The routing registry, project-level `AGENTS.md`, and documentation indexes can be extended for more services, clients, internal tools, data projects, automation repositories, or separate product lines.

```text
shared coordination layer
├── product group A
│   ├── api
│   ├── admin
│   └── mobile
├── product group B
│   ├── service
│   └── website
└── internal systems
    ├── data
    ├── automation
    └── operations
```

Read [workspace architecture](./docs/guides/workspace-architecture.md) for the extension model.

## How the System Works

```text
your request
    ↓
role detection: product / design / backend / frontend / QA / review / docs
    ↓
project routing: one project / one group / company-wide scope
    ↓
project context: AGENTS.md → docs index → module knowledge → real code
    ↓
implementation and verification
    ↓
durable documentation for the next task
```

Five rules keep the system coherent:

1. One authoritative routing registry.
2. Real backend contracts instead of mock-only integration.
3. Feature delivery documents separated from long-lived project knowledge.
4. Independent business repositories kept independent.
5. Every implementation ends with proportional verification and documentation.

## Workspace Layout

```text
monorepo-workflow/
├── AGENTS.md              # Company-wide routing and safe-change boundaries
├── .codex/                # Source of truth for rules, agents, and Skills
├── .cursor/               # Generated compatibility mirror
├── api/                   # Starter backend project context
├── fornt_admin/           # Starter admin project context
├── m_front/               # Starter mobile / H5 project context
├── pc_fornt/              # Starter PC website project context
├── docs/
│   ├── guides/            # Public setup and architecture guides
│   ├── general/           # Cross-project feature delivery documents
│   └── _template/         # New-feature documentation skeleton
├── scripts/               # Maintenance and verification
└── tests/                 # Regression checks
```

Real application source code can remain in separate Git repositories. The root repository tracks the collaboration system and the knowledge needed to operate across them.

## Documentation Map

| Goal | Start here |
|---|---|
| Connect existing repositories | [Quick start](./docs/guides/quick-start.md) |
| Configure project groups and repository sources | [Repository configuration](./docs/guides/repository-configuration.md) |
| Understand human-agent coordination | [Agent workflow](./docs/guides/agent-workflow.md) |
| Add projects or understand ownership boundaries | [Workspace architecture](./docs/guides/workspace-architecture.md) |
| Start a cross-project feature | [Documentation center](./docs/README.md) |
| Extend Codex or Cursor configuration | [.codex guide](./.codex/README.md) |
| Prepare a public release | [Open-source release checklist](./docs/guides/open-source-release-checklist.md) |

## Adopt It Your Way

| Path | Best for |
|---|---|
| Use the whole template | A solo developer or small team starting a multi-project product |
| Connect existing repositories | A company that already has isolated backend, frontend, or service repositories |
| Adopt only the operating model | A team with an existing monorepo that wants routing, documentation, and verification conventions |

Do not install duplicate copies of the same rules or Skills into one tool. Pick one source of truth and document generated mirrors.

## Verification

```bash
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py
```

The same baseline runs in [GitHub Actions](./.github/workflows/ci.yml).

## Project Status

The project currently provides the coordination layer, repository tooling, documentation system, and Codex / Cursor workflow assets. It does not generate business applications or deploy production services for you.

See [CHANGELOG.md](./CHANGELOG.md) for notable changes and the [release checklist](./docs/guides/open-source-release-checklist.md) for known pre-release cleanup items.

## Community

Issues and pull requests are welcome. Read [CONTRIBUTING.md](./CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing. Report vulnerabilities through [SECURITY.md](./SECURITY.md), not a public issue.

## License

Original repository content is available under the [MIT License](./LICENSE). Bundled or adapted third-party components retain their original terms; see [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).
