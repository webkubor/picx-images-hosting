# 推广素材引用模板

> 链接前缀统一为 `https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master`
> 求稳可把 `@master` 换成 git 标签（如 `@v1`）：标签不动、图就不动，不受后续提交影响。

## README 顶部 logo（居中）

```html
<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<项目>/logo.png" width="120" alt="<项目> logo">
</div>
```

## Banner

```markdown
![<项目> banner](https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<项目>/banner.png)
```

## OG / 社交分享卡（项目官网 `<head>`）

```html
<meta property="og:image" content="https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<项目>/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<项目>/og.png">
```

## 演示动效：GIF 内嵌 + MP4 外链

GitHub README 不渲染外链 `<video>`，所以动画用 GIF 内嵌、完整视频给链接（kyvault 即此用法）：

```markdown
![demo](https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<项目>/demo.gif)

[▶ 观看完整演示（MP4）](https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<项目>/demo.mp4)
```

## 缓存

- jsDelivr 缓存约 12 小时；同路径换图后，在链接后加 `?updated=<时间戳>` 立即刷新
- 首次上传后若链接 404，等一次缓存周期或用 raw 直链兜底：
  `https://raw.githubusercontent.com/webkubor/picx-images-hosting/master/<路径>`
