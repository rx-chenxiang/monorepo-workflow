# Playwright 落地规范

## 目录结构

没有既有测试结构时，优先使用：

```text
tests/
  e2e/
    auth/
      login.spec.ts
    smoke/
      app-smoke.spec.ts
    modules/
      list.spec.ts
      create.spec.ts
      edit.spec.ts
    permission/
      permission.spec.ts
  pages/
    LoginPage.ts
    LayoutPage.ts
    ModulePage.ts
  fixtures/
    auth.ts
    test-data.ts
  utils/
    api-client.ts
    cleanup.ts
  .auth/
    admin.json
playwright.config.ts
```

## 推荐配置

第一阶段优先只跑桌面 Chrome，避免过早扩大矩阵：

```ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : 2,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'playwright-results.json' }]
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:5173',
    storageState: 'tests/.auth/admin.json',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } }
  ]
})
```

## 登录态复用

- 使用 `global.setup.ts` 或单独登录脚本生成 `tests/.auth/admin.json`。
- 账号、密码、测试地址从环境变量读取，例如 `BASE_URL`、`E2E_ADMIN_USER`、`E2E_ADMIN_PASSWORD`。
- 遇到验证码时，优先要求测试环境提供免验证码账号、固定验证码或后端测试登录入口。
- 多角色权限测试可生成多个 storageState，例如 `admin.json`、`readonly.json`、`operator.json`。

## Page Object Model

将页面动作放入 `pages/`，让 spec 只表达业务流程：

```ts
import { expect, type Locator, type Page } from '@playwright/test'

export class ModulePage {
  readonly page: Page
  readonly createButton: Locator
  readonly keywordInput: Locator
  readonly searchButton: Locator
  readonly table: Locator

  constructor(page: Page) {
    this.page = page
    this.createButton = page.getByTestId('module-create-button')
    this.keywordInput = page.getByTestId('module-search-input')
    this.searchButton = page.getByTestId('module-search-button')
    this.table = page.getByTestId('module-table')
  }

  async goto(path: string) {
    await this.page.goto(path)
    await expect(this.table).toBeVisible()
  }

  async searchByKeyword(keyword: string, apiKeyword: string) {
    await this.keywordInput.fill(keyword)
    await Promise.all([
      this.page.waitForResponse(resp => resp.url().includes(apiKeyword) && resp.status() === 200),
      this.searchButton.click()
    ])
  }
}
```

## 选择器规范

优先让前端补 `data-testid`；如果项目已重视可访问性，也可优先用 `getByRole`、`getByLabel`：

```vue
<button data-testid="module-create-button">新增</button>
<input data-testid="module-search-input" />
<table data-testid="module-table" />
```

命名建议：

```text
module-create-button
module-search-input
module-search-button
module-save-button
module-table
module-empty
module-status-select
module-delete-confirm
```

## 测试数据

- 新增数据统一使用 `QA_YYYYMMDD_` 前缀。
- 查询、编辑、删除只操作自动化创建的数据。
- 优先通过接口造数和清理，避免直接改库。
- 共享环境只做可回滚操作；删除、权限、系统配置类动作必须得到授权。
- 数据清理失败时在报告中标记残留数据，不隐藏环境污染风险。

## 用例标签

建议用标题或注释区分运行层级：

```ts
test('列表页可正常打开 @smoke', async ({ page }) => {})
test('新增业务数据成功 @regression', async ({ page }) => {})
```

常用命令：

```bash
npx playwright test --grep @smoke
npx playwright test tests/e2e/modules
npx playwright show-report
```

## Flaky 治理

- 使用 `--repeat-each=10` 复现不稳定问题。
- 对确认不稳定但暂未修复的用例使用 `test.fixme` 或单独隔离，不进入发版阻断。
- 记录 flaky 原因：接口慢、测试数据污染、权限差异、动画未稳定、环境偶发。
- 修复后再恢复到 `regression`。

## CI 建议

- 初期 CI 只跑 `chromium + smoke`。
- 测试环境部署完成后再跑 `regression`。
- 每次失败上传 `playwright-report`、截图、视频和 trace。
- 涉及数据写入的用例在 CI 中串行执行，等清理机制稳定后再并行。

<!-- AIGC:cursor|author:沉香|lines:约139|dates:2026-07|功能说明:将Playwright落地参考改造为通用中文前端E2E规范，覆盖目录、配置、POM、选择器、数据、CI和flaky治理 -->
