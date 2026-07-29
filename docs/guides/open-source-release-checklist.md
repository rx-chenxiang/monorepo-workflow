# 开源发布检查清单

本清单用于将 Monorepo Workflow 从“本地可用”推进到“GitHub 上可持续维护”。它参考成熟开源仓库常见的 README 导航、许可证、社区文件、自动检查和版本发布做法。

## 1. 发布内容

- [x] 根目录提供中英文 README，并互相链接。
- [x] README 说明项目价值、适用边界、快速开始、层级结构和验证方式。
- [x] 公开使用指南集中放在 `docs/guides/`。
- [x] 提供 `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md` 和 `SECURITY.md`。
- [x] 提供 Issue forms、Pull Request 模板和基础 CI。
- [x] 使用 `CHANGELOG.md` 记录面向使用者的重要变化。

## 2. 许可证与第三方内容

- [x] 根仓原创内容使用 MIT License。
- [x] 已知第三方组件记录在 `THIRD_PARTY_NOTICES.md`。
- [ ] 发布前再次确认每个复制、改编或打包的 Skill、脚本、字体、音频和图片允许再分发。
- [ ] 对新增第三方内容保留原始版权声明、许可证文件和来源链接。

根许可证不能替代第三方组件自身的授权。来源或许可不清楚的资产应在公开发布前移除或取得授权。

## 3. 隐私与安全

- [ ] 检查当前文件和完整 Git 历史，确认没有令牌、密钥、账号、内部域名、客户数据或个人隐私。
- [ ] 检查截图、音频、设计稿和示例数据的公开权限。
- [ ] 在 GitHub 仓库 Security 设置中启用 Private vulnerability reporting。
- [ ] 为默认分支启用 Secret scanning、Push protection 和适当的分支保护（取决于账号能力）。

推荐至少执行：

```bash
bash tests/pull_repos_test.sh
python3 scripts/check_markdown_links.py
git status --short
```

## 4. GitHub 仓库设置

- [ ] 填写一句话 Description，避免只重复仓库名。
- [ ] 设置 Topics，例如 `ai-agents`、`codex`、`cursor`、`monorepo`、`workflow`、`fullstack`。
- [ ] 设置 Social preview 图片，建议突出“四端 + 文档 + Agent 路由”。
- [ ] 确认 Issues 可用，并按需启用 Discussions。
- [ ] 将 CI 设为默认分支的必需检查。
- [ ] 确认合并策略；小型项目通常保留 Squash merge 即可。

建议 Description：

```text
AI-assisted workspace template for coordinating backend, admin, mobile/H5, and PC projects with documentation-driven agent workflows.
```

## 5. 首个版本

1. 将 `CHANGELOG.md` 的 `Unreleased` 内容整理为首个版本。
2. 创建语义化标签，例如 `v0.1.0`。
3. 在 GitHub Release 中说明适用人群、安装方式、已知限制和升级方式。
4. 发布后重新执行快速开始，确认公开用户只依赖仓库中已有的信息即可完成首次使用。

不要为了“看起来成熟”提前声明尚不存在的安装器、兼容平台或自动化能力。

## 6. 当前仓库已知待处理项

- [ ] `.codex/skills/coding-agent-team-fullstack/` 仍包含 `bss`、`tiku`、`agency` 等旧项目组示例，需要改为当前 `general` 四端模型或明确标注为示例。
- [ ] `.codex/skills/writing-tech-design-doc/` 与部分测试 Skill 仍包含 `docs/bss/` 等旧路径，需要统一为 `docs/general/{需求名称}/`。
- [ ] 复核 `.codex/skills/huashu-design/assets/` 中音频和其他素材的再分发范围；Skill 自带 MIT 许可证，但发布者仍应确认素材均包含在该授权内。

可用以下命令继续定位旧项目痕迹：

```bash
rg -n '\b(bss|tiku|agency)\b|docs/bss' .codex
```
