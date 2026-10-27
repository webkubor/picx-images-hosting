# 引用模板

> 链接前缀统一 `https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main`；求稳把 `@main` 换 git 标签（如 `@v1`）。

## README 顶部 logo（居中）

```html
<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/<项目>/logo.png" width="120" alt="<项目> logo">
</div>
```

## Banner

```markdown
![<项目> banner](https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/<项目>/banner.png)
```

## OG / 社交分享卡（`<head>`）

```html
<meta property="og:image" content="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/<项目>/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/<项目>/og.png">
```

::: warning og 图保持 PNG/JPG
部分社交平台抓取器对 WebP/AVIF 兼容性差；`add.sh` 会对 `og.*` 自动保原格式。
:::

## 渐进增强：AVIF + WebP + PNG

```html
<picture>
  <source srcset="…/@main/<项目>/banner.avif" type="image/avif">
  <source srcset="…/@main/<项目>/banner.webp" type="image/webp">
  <img src="…/@main/<项目>/banner.png" alt="banner">
</picture>
```

## 演示动效：GIF 内嵌 + MP4 外链

GitHub README 不渲染外链 `<video>`，动画用 GIF、完整视频给链接：

```markdown
![demo](…/@main/<项目>/demo.gif)
[▶ 观看完整演示（MP4）](…/@main/<项目>/demo.mp4)
```

## 缓存

jsDelivr 缓存约 12h；同路径换图后加 `?updated=<时间戳>` 立即刷新；首次 404 等一个缓存周期或用 raw 兜底。
