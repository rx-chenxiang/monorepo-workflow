# .codex · 目录结构

## 当前文件说明

本目录为 monorepo 根目录下唯一的 Codex 协作配置中心（Rules、Agents、Skills）。**项目名与别名** 见根目录 [AGENTS.md](../AGENTS.md)；**口语 → 角色 + 项目范围** 见 `rules/project-routing.mdc`；**人类工作区说明** 见 [README.md](../README.md)；**需求文档落盘** 见 [docs/README.md](../docs/README.md)。

> `.codex` 是权威配置源；`.cursor` 仅镜像 `README.md`、`rules/`、`agents/`，同步脚本见 [scripts/sync-codex-to-cursor.sh](../scripts/sync-codex-to-cursor.sh)。技能目录以 `.codex/skills/` 为准，避免双份大文件漂移。

```
.codex/
├── README.md                 # 本文件：目录结构
├── rules/
│   ├── project-routing.mdc           # ★ 口语 → workflow + 项目范围（alwaysApply）
│   ├── multi-project-workspace.mdc
│   ├── subdir-rule-priority.mdc
│   ├── project-workflow-product.mdc  # 产品 / PRD / 需求规划
│   ├── project-workflow-ui.mdc       # 设计 / 原型
│   ├── project-workflow-test.mdc     # 测试 / E2E / 验收
│   ├── project-workflow-api.mdc      # 后端 API
│   ├── project-workflow-front.mdc    # 三前端开发
│   ├── api-first-no-mock.mdc
│   ├── code-review.md
│   └── security.md
├── agents/
│   ├── api-developer.md              # 后端编码
│   ├── front-developer.md            # 管理端编码
│   ├── doc-updater.md                # 文档同步
│   ├── code-reviewer.md
│   ├── security-reviewer.md
│   ├── e2e-runner.md
│   ├── browser-functional-test.md
│   ├── vue-frontend-architect.md
│   ├── ux-verification-checklist.md
│   ├── tdd-guide.md
│   ├── performance-optimizer.md
│   └── legacy-style-compat.md
└── skills/
    ├── coding-agent-team-fullstack/  # 全栈五阶段（后端→验证→前端→文档）
    ├── requirements-to-tech-doc/     # 需求 → 技术规划
    ├── writing-tech-design-doc/      # 前端 §1～§5 技术设计
    ├── ai-browser-agent/             # Playwright 浏览器验收
    ├── e2e-testing/                  # E2E 测试模式
    ├── front-e2e-testing/            # 前端代码化自动化测试
    ├── qa-test-execution/            # 功能 / 验收 / 回归测试执行
    ├── test-yl/                      # 测试用例资产生成
    ├── ui-ux-pro-max/                # UI / UX 设计知识库
    └── huashu-design/                # HTML 高保真原型（demos 大文件见 .gitignore）
```

<!-- AIGC:cursor|author:沉香|lines:约5|dates:2026-07|功能说明:补充.codex为权威配置源、.cursor仅镜像rules与agents，并泛化api/front工作流描述 -->
<!-- AIGC:cursor|author:沉香|lines:约4|dates:2026-07|功能说明:将协作配置目录说明从旧.cursor口径统一为.codex口径 -->
