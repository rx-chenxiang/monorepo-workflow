# 贡献指南

感谢你愿意改进 Monorepo Workflow。本仓库关注可复用的工作区协作资产：规则、Agent、Skills、文档模板、脚本与测试，而不是某个具体业务系统。

## 开始前

1. 阅读根目录 [AGENTS.md](./AGENTS.md)，了解项目边界和文档约定。
2. 先搜索已有 Issue，避免重复讨论。
3. 对较大的规则、目录或工作流调整，建议先创建 Issue 说明问题、适用场景和预期结果。

## 适合贡献的内容

- 面向多端协作的规则、Agent 工作流和 Skills。
- 需求、技术设计、测试、联调和模块文档模板。
- `pull_repos.sh`、同步脚本及其测试。
- 文档修正、示例和跨工具兼容性改进。

请勿提交真实业务源码、访问令牌、密钥、客户数据、包含个人信息的截图或无法公开再分发的素材。

## 提交流程

```bash
# 1. Fork 后克隆自己的仓库
git clone https://github.com/<your-account>/monorepo-workflow.git
cd monorepo-workflow

# 2. 创建清晰的分支
git switch -c docs/improve-agent-workflow

# 3. 完成修改后执行相关验证
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py

# 4. 提交并推送
git add <changed-files>
git commit -m "docs: improve agent workflow guide"
git push -u origin docs/improve-agent-workflow
```

然后从 GitHub 创建 Pull Request，并按模板说明动机、影响范围和验证结果。

## 变更要求

- 变更要小而聚焦，不重写无关配置或共享组件。
- 修改公开行为时，同步更新 [README.md](./README.md) 和 [README.zh-CN.md](./README.zh-CN.md)。
- 修改 `.codex/README.md`、`.codex/rules/` 或 `.codex/agents/` 后，运行 `./scripts/sync-codex-to-cursor.sh` 并提交对应 `.cursor/` 镜像变更。
- 增加或修改脚本时，补充或更新可执行测试。
- 文档链接应使用相对路径，并确保文件真实存在。
- 引入第三方 Skill、脚本或资产时，必须更新 `THIRD_PARTY_NOTICES.md` 并保留其许可证。
- 涉及四端的变更，在 PR 中按后端、管理平台、门户端、PC 官网和联调验证说明影响。

## Pull Request 检查清单

- [ ] 变更只覆盖当前问题所需范围。
- [ ] 没有提交密钥、个人信息或业务数据。
- [ ] 已更新关联文档和中英文 README（如适用）。
- [ ] 已执行相关脚本或测试，并在 PR 中记录结果。
- [ ] `.codex` 修改已同步到 `.cursor`（如适用）。
- [ ] 新增第三方组件已保留许可证并更新第三方声明（如适用）。

## 行为规范与安全问题

参与本项目即表示遵守 [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)。安全漏洞请遵循 [SECURITY.md](./SECURITY.md)，不要在公开 Issue 或 PR 中披露可利用细节。
