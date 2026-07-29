# 仓库配置

`repos.conf` 描述实际业务仓库的来源；`pull_repos.sh` 根据该文件克隆或以 fast-forward 方式更新仓库。模板本身不包含业务源码。

## 配置格式

```text
[workspace_name]
[transport]git_url|branch(optional)|target_dir(optional)|project_id(optional)
```

- `workspace_name`：仓库分组，例如 `general`。
- `transport`：可选的连接方式标签，例如 `https` 或 `ssh`。
- `git_url`：Git 仓库地址。
- `branch`：可选；克隆时检出的分支。
- `target_dir`：可选；在目标工作目录下的目录名。
- `project_id`：可选；用于按项目筛选，与 Agent 注册表保持一致。

## 四端示例

```text
[general]
[https]https://github.com/your-org/api.git|main|api|api
[https]https://github.com/your-org/fornt_admin.git|main|fornt_admin|fornt_admin
[https]https://github.com/your-org/m_front.git|main|m_front|m_front
[https]https://github.com/your-org/pc_fornt.git|main|pc_fornt|pc_fornt
```

若团队同时维护 SSH 地址，可在相同工作区中增加对应条目，再用 `--transport ssh` 筛选：

```text
[general]
[ssh]git@github.com:your-org/api.git|main|api|api
```

不要在一次命令中使用 `--all-transports` 拉取指向同一目录的 HTTPS 与 SSH 重复条目。

## 常用命令

```bash
# 只查看 general 分组中的仓库，不执行 Git 操作
./pull_repos.sh --workspace general --list

# 只处理一个项目
./pull_repos.sh --workspace general --project api --target-dir /path/to/workspace

# 只使用 SSH 条目
./pull_repos.sh --workspace general --transport ssh --target-dir /path/to/workspace

# 查看全部参数
./pull_repos.sh --help
```

## 使用约束

1. 执行写操作前先使用 `--list` 复核范围。
2. `project_id`、`target_dir` 与根目录 [AGENTS.md](../../AGENTS.md) 中的项目 ID 保持一致。
3. 业务仓库各自拥有独立 Git 历史；不要将业务源码从工作区根仓提交。
4. 需要自定义配置文件时，使用 `--config /path/to/repos.conf`。
