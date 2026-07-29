# 浏览器与桌面控制策略

本策略用于在测试执行时选择合适的操作面，并沉淀证据。后台、H5、App 等界面测试默认使用 Codex 的 `computer-use:computer-use` 电脑操控能力；只有当场景明确不需要界面或需要专门数据核验时，才切换到 CLI/API 或人工确认。

## 执行面选择

| 执行面 | 适用场景 | 不适用场景 |
|---|---|---|
| CLI/API | 构建、lint、单元测试、接口校验、数据准备、日志分析 | 必须观察真实页面交互或本机 App UI |
| computer-use | 默认执行面：后台、H5、App、用户已打开的浏览器标签页、本机 Mac App、系统弹窗、文件选择器、原生 WebView | 可用 CLI/API 稳定完成且无需观察界面的纯数据校验 |
| chrome | 仅当用户明确要求 Chrome 专用 connector，或 Computer Use 无法完成且必须复用 Chrome profile/插件/已有标签页时使用 | 默认测试执行；可由 Computer Use 接管的普通浏览器界面 |
| manual | 主观视觉确认、验证码、人为审批、无法自动化但需要确认的点 | 可稳定自动化且无外部副作用的断言 |

## Computer Use 使用规则

- 界面测试默认使用 `computer-use:computer-use`，优先复用用户已打开的业务窗口或浏览器标签页。
- 每个关键用例至少记录：页面 URL、截图、页面文本、操作步骤；需要接口核验时补充请求/响应片段或日志。
- 接管用户已有业务标签页时，保持在业务页面执行，不主动打开、聚焦或停留在 DevTools 控制层。
- 每个业务目标默认只允许一次点击。若点击返回超时、命中检测异常或页面无响应，禁止立刻对同一目标补点、双击或连续点击；应先读取 URL、页面文本、截图、弹窗和日志，依据页面实际变化判定结果。
- H5/App/后台页面点击必须是单次按下后立即抬起的普通单点；禁止双击、连续点击、长按、按住拖动式试探、坐标补点或任何会唤出 Chrome/DevTools/插件控制层的交互。若单点后出现控制层、元素检查层或自动化悬浮层，先由 Agent 自动收起或避开控制层、恢复业务页面焦点，再继续按用例托管执行；不得因此把普通业务步骤直接标记为 `human_assisted`、`阻塞` 或 `待确认`。
- 只有用例本身明确要求双击、连点、长按、拖拽或压力测试时，才能执行多次点击，并必须在执行结果 `note` 中说明触发原因和点击次数。
- 不用 Computer Use 代替 CLI/API 可稳定完成的纯后端校验；但只要需要观察或操作真实界面，默认回到 Computer Use。
- 遇到以下动作，必须遵守 Computer Use 确认策略：
  - 验证码：动作前确认，或交给用户人工完成，并记录为 `human_assisted`。
  - 上传文件、传输敏感数据、修改权限/账号、删除/移动数据、提交表单、安装软件、修改系统设置：动作前确认。
  - 浏览器安全拦截、改密码最终提交：交给用户处理，不由 Agent 操作绕过。
- 使用 Computer Use 产生外部副作用前，说明风险、目标位置、将提交或修改的具体内容。

## 验证码与登录处理

- 登录可在用户明确测试目标中视为被允许；若跳转到第三方或涉及保存密码/权限授权，动作前确认。
- Agent 不主动破解或绕过验证码。若验证码阻塞自动化：
  - 记录阻塞页面截图和原因；
  - 请求用户人工完成，或获得动作前确认后继续；
  - 在执行结果中标记 `human_assisted: true`。
- 用户明确授权处理测试环境腾讯滑块验证码时，按 `tencent-captcha-slider.md` 执行：截图定位滑块与缺口，一次连续拖动，拖动后用页面文本、URL、接口日志和 token 写入判断是否成功。
- 若 mock 验证码导致白屏或接口异常，应单独记录为环境/集成风险，不与真实业务缺陷混淆。

## 证据字段要求

执行结果中建议记录以下字段：

```json
{
  "surface": "computer-use",
  "human_assisted": false,
  "confirmation": "",
  "evidence": [
    "artifacts/TC-001.png",
    "artifacts/TC-001-console.json",
    "artifacts/TC-001-network.har"
  ]
}
```

`surface` 可选值：`cli`、`api`、`computer-use`、`chrome`、`manual`、`mixed`，界面测试默认填写 `computer-use`。

如果同一条用例混合多个执行面，使用 `mixed`，并在 `note` 中说明组合方式。

<!-- AIGC:cursor|author:沉香|lines:约1|dates:2026-07|功能说明:补充用户授权后腾讯滑块验证码测试执行入口，复用滑块定位和拖动判定流程 -->
<!-- AIGC:cursor|author:沉香|lines:约1|dates:2026-07|功能说明:调整Chrome控制层恢复策略，要求Agent自动收起控制层并继续托管普通业务步骤 -->
<!-- AIGC:cursor|author:沉香|lines:约1|dates:2026-07|功能说明:强化Chrome H5接管点击策略，禁止触发控制层的双击、长按、补点和连续点击 -->
<!-- AIGC:cursor|author:沉香|lines:约4|dates:2026-07|功能说明:补充Chrome接管测试规则，避免打开控制层并强制默认单次点击，控制点击超时后的处理方式 -->
<!-- AIGC:cursor|author:沉香|lines:约18|dates:2026-07|功能说明:将界面测试默认执行面调整为Codex Computer Use，弱化Chrome专用与Playwright路径 -->
