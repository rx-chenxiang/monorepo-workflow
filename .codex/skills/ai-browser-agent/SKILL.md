---
name: ai-browser-agent
description: 使用 playwright MCP 以 AI Agent 模式自主控制浏览器，模拟人工操作完成多步骤任务、UI 验证、截图对比。触发场景：用户说"帮我点击/测试/验证某个页面"、"自动操作浏览器"、"AI 自动测试"、"模拟用户操作"、browser agent、自动化验收。
---

# AI 浏览器自主操作 Agent

使用 **`playwright` MCP** 工具以自主 Agent 模式操控浏览器，无需用户手动选择元素。

> MCP Server 名称：`playwright`（已配置在 `~/.cursor/mcp.json`）

## Agent 工作原则

执行任何浏览器任务时，严格遵循以下循环，**不要在中途询问用户**：

```
感知 → 决策 → 执行 → 验证 → 循环
```

1. **感知**：`browser_snapshot` 获取页面无障碍树，理解可交互元素
2. **决策**：根据任务目标，自主判断下一步（点击/输入/JS注入/导航）
3. **执行**：调用对应工具
4. **验证**：`browser_snapshot` 或 `browser_screenshot` 确认操作结果
5. **循环**：未完成则继续；遇到错误自动重试（最多 3 次）

## 工具速查表

| 工具 | 用途 |
|---|---|
| `browser_navigate` | 打开 URL |
| `browser_snapshot` | 获取页面无障碍树（返回可交互元素 ref） |
| `browser_screenshot` | 截图（结果验证/视觉确认） |
| `browser_click` | 点击元素（传 ref 或 selector） |
| `browser_fill` | 清空并填写输入框 |
| `browser_type` | 追加输入文字 |
| `browser_press_key` | 按键（Enter / Tab 等） |
| `browser_evaluate` | **执行 JavaScript**（点击 uni-button 等无障碍属性缺失元素的唯一可靠方式） |
| `browser_wait_for` | 等待元素/URL/文本出现 |
| `browser_close` | 关闭浏览器 |

## 标准操作流程

### 启动任务

```
1. browser_navigate  → 打开目标页面
2. browser_snapshot  → 读取初始页面结构
3. 开始 Agent 循环
```

### 元素定位策略（优先级排序）

1. **snapshot ref** — 最精确，用 snapshot 返回的 ref ID
2. **CSS selector** — 传给 `browser_click` 的 `selector` 参数
3. **browser_evaluate** — 当前两者失效时，用 JS 直接操作 DOM（见下方示例）
4. **browser_screenshot** — 视觉兜底，截图分析后再决策

### uni-button 点击（本项目专用）

`uni-button` 编译后无 ARIA 属性，不出现在 snapshot refs，**必须用 JS 点击**：

```javascript
// browser_evaluate 参数示例

// 通过文字内容点击按钮
document.querySelector('uni-button')?.click()

// 精确匹配按钮文字
[...document.querySelectorAll('uni-button')]
  .find(el => el.textContent.includes('登录'))?.click()

// 点击 class 定位的按钮
document.querySelector('.login-btn uni-button')?.click()
```

### 等待策略

- 点击后：`browser_snapshot` 检查 DOM 是否变化
- 表单提交后：`browser_wait_for` 等待 URL 变化或新元素出现
- **禁止固定等待**：不使用 sleep，用状态变化判断

### 错误自恢复

```
操作失败 → browser_screenshot 确认当前状态
         → 分析失败原因
         → 若为无障碍问题 → 改用 browser_evaluate
         → 若为时序问题   → browser_wait_for 后重试
最多重试 3 次 → 仍失败则报告具体卡点
```

## 本项目关键信息

| 项目 | 值 |
|---|---|
| H5 地址 | `http://localhost:5173` |
| 路由格式 | Hash 路由，如 `/#/pages/login/login` |
| 框架 | uni-app H5，`<text>→<span>`，`<button>→<uni-button>` |
| Toast 容器 | `.uni-sample-toast` |
| Toast 文字 | `.uni-simple-toast__text` |
| 输入框 | `.uni-input-wrapper input`，placeholder 是独立 `div` |
| 登录按钮 JS | `document.querySelector('.login-btn uni-button')?.click()` |

## 常用任务模板

### 登录验证

```
1. browser_navigate('/#/pages/login/login')
2. browser_snapshot → 确认页面加载
3. browser_fill(手机号 ref, '手机号')
4. browser_fill(验证码 ref, '验证码')
5. browser_evaluate → 点击登录按钮
6. browser_wait_for → 等待 URL 不含 /login
7. browser_screenshot → 截图验证已登录
```

### 表单冒烟测试

```
1. browser_navigate → 进入表单页
2. browser_evaluate → 直接点击提交（空表单）
3. browser_snapshot  → 检查 toast 是否出现
4. 逐字段填写边界值，重复步骤 2-3
```

### UI 截图验收

```
1. browser_navigate → 目标页面
2. browser_wait_for → 等待关键元素可见
3. browser_screenshot → 全屏截图
4. 分析布局、颜色、文案是否符合设计稿
```

## 任务完成后必须输出

```markdown
## 操作结果

- **执行步骤**：逐步列出实际执行的操作
- **关键截图**：附登录前/后等关键节点截图
- **验证结论**：通过 ✅ / 失败 ❌ + 原因
- **发现问题**：（如有 UI/功能异常，详细描述复现路径）
```
