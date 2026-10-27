# 浏览器验收截图

打开 [截图索引页](index.html)，或访问部署后的 `/design/screenshots/index.html`。

| 文件 | 页面状态 | 采集方式 |
|---|---|---|
| `review-light-128.webp` | 1200×1000 视口，浅底，128px logo，首屏两个项目 | Browser Use 实际 screenshot，PNG 转 WebP（quality 86） |
| `review-dark-128.webp` | 1200×1000 视口，深底，128px logo，首屏两个项目 | 实际点击 Dark 后 Browser Use screenshot，PNG 转 WebP（quality 86） |

截图来自本地 `design/logo-review.html`，用于保存本次验收状态；线上页面由同一 HTML 源构建发布。图内内容未重新绘制，不能把截图当全部 12 项在全部环境中的通过证明。

本轮另核实：32px 选择后图像真实宽高为32，390px视口下文档宽390无横向溢出；实际点击复制任务后反馈“已复制完整任务”。手机截图准备连续超时，未归档手机截图。

原始浏览器 PNG 的 SHA-256：

- 浅底：`59bec900e28365b49fb75c213483fc1f7d5e04e5740a799313e71b4feb7539f2`
- 深底：`fa0057ceeefd78fb4813876940cbb9a9449e0b2f1e7ffaad2d41bb76fc4a91ff`

复用时请重新实际截图，并记录页面版本、背景、尺寸、视口和测试范围，不要复制本次截图当新项目验收结果。
