# 工作区需求文档（docs/）

## 当前文件说明

本目录存放 **跨子项目** 的需求与设计文档（PRD、技术方案、编码计划）。业务模块实现细节维护在各子项目自己的 `docs/` 下：`api/docs/`、`fornt_admin/docs/`、`m_front/docs/`、`pc_fornt/docs/`。

---

## 目录约定（权威）

```text
docs/general/{需求名称}/
├── 需求文档/          # PRD、原型、设计图、附件
├── 技术设计方案/      # 模块技术规划、全栈/前端技术设计文档
└── coding-plan/       # dev-brief、{需求名}-coding.md、各端编码计划
```

当前项目组 ID：**`general`**（见根目录 [AGENTS.md](../AGENTS.md)）。

---

## 新建需求（复制模板）

```bash
# 将 {你的需求名} 替换为实际名称，如「会员中心」
mkdir -p docs/general
cp -R docs/_template "docs/general/{你的需求名}"
```

勿使用字面目录名 `需求名称`；`docs/_template/` 仅作骨架复制源。

---

## 常见落盘路径

| 产出类型 | 路径 |
|---------|------|
| PRD / 设计图 | `docs/general/{需求名}/需求文档/**` |
| 模块技术规划 | `docs/general/{需求名}/技术设计方案/{序号}-{模块}模块技术规划.md` |
| 前端技术设计 | `docs/general/{需求名}/技术设计方案/{需求名}前端技术设计文档.md` |
| 编码前置摘要 | `docs/general/{需求名}/coding-plan/{模块}-dev-brief.md` |
| 编码阶段提示词 | `docs/general/{需求名}/coding-plan/{需求名}-coding.md` |

---

## 与子项目 docs 的区别

| 目录 | 用途 |
|------|------|
| 本目录 `docs/general/...` | 按**需求**组织的全栈交付文档 |
| `api/docs/modules/` | 后端 API 长期模块文档 |
| `fornt_admin/docs/modules/` | 管理平台长期模块文档 |
| `m_front/docs/modules/` | 门户端长期模块文档 |
| `pc_fornt/docs/modules/` | 官网长期模块文档 |

---

## 工作区级约定

| 文档 | 用途 |
|------|------|
| [general/workspace/联调约定.md](general/workspace/联调约定.md) | 四端端口、启动命令、接口代理、环境变量与验收门禁 |

<!-- AIGC:cursor|author:沉香|lines:约10|dates:2026-07|功能说明:docs索引新增工作区级四端联调约定入口 -->
<!-- AIGC:cursor|author:沉香|lines:约55|dates:2026-07|功能说明:需求文档目录初始化为通用版本，统一使用docs/general承载跨四端需求资料 -->
