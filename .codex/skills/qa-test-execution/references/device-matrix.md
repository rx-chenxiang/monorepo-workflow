# 设备覆盖矩阵

## 快速冒烟

适用于每次提测后的快速判断。

- iPhone 主流宽度 Safari 或 iOS WebView
- Android 主流宽度 Chrome 或 App WebView
- 桌面 Chrome 移动端模拟器，仅作辅助

## 功能验收

适用于新功能上线前。

- 小屏手机：例如 iPhone SE 宽度
- 常规 iPhone：例如 iPhone 13/14/15 宽度
- 常规 Android：例如 Pixel 或主流国产安卓宽度
- 大屏/平板窄屏：当页面响应式风险较高时加入

## 兼容专项

适用于页面布局、滚动、上传、支付、播放器、复杂交互。

- iOS Safari
- iOS App WebView
- Android Chrome
- Android App WebView
- 微信/小程序 WebView，如业务涉及

## 网络专项

- 离线
- 慢 3G
- 请求超时
- 接口 4xx/5xx
- 图片资源 404
- 恢复网络后刷新/重新进入
