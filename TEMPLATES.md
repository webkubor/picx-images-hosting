# 推广素材引用模板

> 链接前缀统一为 `https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master`
> 求稳可把 `@master` 换成 git 标签（如 `@v1`）：标签不动、图就不动，不受后续提交影响。

## README 顶部 logo（居中）

```html
<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/logo.png" width="120" alt="<项目> logo">
</div>
```

## Banner

```markdown
![<项目> banner](https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/banner.png)
```

## OG / 社交分享卡（项目官网 `<head>`）

> og 图保持 PNG/JPG，别用 WebP：`add.sh` 会自动对 `og.*` 保原格式优化。

```html
<meta property="og:image" content="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/og.png">
```

## 渐进增强：AVIF + WebP + PNG（`<picture>`）

`tools/add.sh --avif x.png` 额外产出 `.avif`（比 WebP 再小 20-30%）；三份都在时用：

```html
<picture>
  <source srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/banner.avif" type="image/avif">
  <source srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/banner.webp" type="image/webp">
  <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/banner.png" alt="banner">
</picture>
```

## 国内受众：R2 镜像

jsDelivr 自 2022 年起在中国大陆无 ICP、访问不稳。面向国内读者的页面，把素材同步到
Cloudflare R2 + 自定义域（本库配套管理端见 `web/`，线上 `img.webkubor.online`），
引用换成 `https://img.webkubor.online/<同路径>`，两套链接按受众选用。

## 演示动效：GIF 内嵌 + MP4 外链

GitHub README 不渲染外链 `<video>`，所以动画用 GIF 内嵌、完整视频给链接（kyvault 即此用法）：

```markdown
![demo](https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/demo.gif)

[▶ 观看完整演示（MP4）](https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@master/<项目>/demo.mp4)
```

## 缓存

- jsDelivr 缓存约 12 小时；同路径换图后，在链接后加 `?updated=<时间戳>` 立即刷新
- 首次上传后若链接 404，等一次缓存周期或用 raw 直链兜底：
  `https://raw.githubusercontent.com/webkubor/free-imgbed/master/<路径>`
