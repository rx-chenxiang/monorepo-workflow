# 快速开始

本指南适用于两种情况：从零开始采用本工作区模板，或将已有的后端和前端仓库接入统一协作目录。

## 1. 获取模板并校验基础脚本

```bash
git clone https://github.com/rx-chenxiang/monorepo-workflow.git
cd monorepo-workflow
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py
```

测试通过时会分别输出 `pull_repos_test.sh passed` 和 `Markdown link check passed`。

## 2. 配置实际业务仓库

编辑根目录 [repos.conf](../../repos.conf)，将示例 URL 替换为团队真实仓库。一个典型的四端配置如下：

```text
[general]
[https]https://github.com/your-org/api.git|main|api|api
[https]https://github.com/your-org/fornt_admin.git|main|fornt_admin|fornt_admin
[https]https://github.com/your-org/m_front.git|main|m_front|m_front
[https]https://github.com/your-org/pc_fornt.git|main|pc_fornt|pc_fornt
```

配置字段和 SSH 示例见 [仓库配置指南](repository-configuration.md)。

## 3. 先预览，再拉取

先确认脚本将操作的仓库：

```bash
./pull_repos.sh --workspace general --list
```

确认无误后执行拉取或更新：

```bash
./pull_repos.sh --target-dir /path/to/workspace --workspace general
```

`--target-dir` 建议使用一个专门的工作目录，避免与模板根目录或已有业务目录混淆。

## 4. 让 Agent 读取正确上下文

Agent 进入仓库后从根目录 [AGENTS.md](../../AGENTS.md) 开始。它会根据任务意图和目标端，继续读取 `.codex/rules/`、对应子项目的 `AGENTS.md` 与 `docs/` 索引。

如果修改了 `.codex/README.md`、`.codex/rules/` 或 `.codex/agents/`，运行：

```bash
./scripts/sync-codex-to-cursor.sh
```

## 5. 开始一个新需求

```bash
cp -R docs/_template "docs/general/{需求名称}"
```

将 PRD、技术设计和编码计划分别填入新目录中的 `需求文档/`、`技术设计方案/`、`coding-plan/`。具体结构见 [文档中心](../README.md)。
