<div align="center">

<img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg" width="112" alt="free-imgbed logo">

# free-imgbed

**一个 GitHub 仓库，就是一台免费图床。**<br>
<sub><i>One GitHub repo is all it takes to run your own image CDN.</i></sub>

<a href="https://github.com/webkubor/free-imgbed/stargazers"><img src="https://img.shields.io/github/stars/webkubor/free-imgbed?style=flat-square&color=FF6F61" alt="Stars"></a>
<a href="https://github.com/webkubor/free-imgbed/actions/workflows/check.yml"><img src="https://github.com/webkubor/free-imgbed/actions/workflows/check.yml/badge.svg" alt="assets-check"></a>
<a href="https://github.com/webkubor/free-imgbed/blob/main/LICENSE"><img src="https://img.shields.io/badge/code%20license-MIT-4c9a6b?style=flat-square" alt="License"></a>
<img src="https://img.shields.io/badge/%E5%9B%BE%E7%89%87%E2%89%A42MB-FF9F45?style=flat-square" alt="img cap">
<img src="https://img.shields.io/badge/%E8%A7%86%E9%A2%91%E2%89%A410MB-8b949e?style=flat-square" alt="video cap">

图片走 GitHub raw + jsDelivr 全球 CDN · fork 改名即用 · 本仓本身就是活示例

</div>

---

## ✨ 特性

- **零依赖起步** —— 不用装任何服务，仓库即图床，`clone` 仅 ~2MB
- **透明度安全的压缩管线** —— 带 alpha 的 PNG 走无损 WebP（实测逐位保留），不透明才上有损；永远不会越压越大
- **AVIF 渐进增强** —— `--avif` 一键再省 20-30%，`<picture>` 三源模板现成可抄
- **CI 强制红线** —— 图片 ≤2MB / 视频 ≤10MB、全仓内容查重、索引新鲜度，超了就挡，不靠自觉
- **开源项目推广素材管理** —— 按项目归档 logo / banner / OG 图 / 演示 GIF+MP4，引用模板复制即用

## 🚀 快速开始

```bash
# 1. fork（或 clone 后推到你自己的新仓），改成你喜欢的名字
# 2. 本地 clone，把示例素材换成你的
git clone git@github.com:<你的用户名>/<你的仓>.git

# 3. 上传：一条命令，自动缩放 + 压缩 + 生成直链
tools/add.sh 我的图片.png <项目名>/

# 4. 任意项目里引用
# https://cdn.jsdelivr.net/gh/<你的用户名>/<你的仓>@main/<路径>
```

<!-- fork 后记得把上面命令和本文件里的仓库地址换成你自己的 -->

## ⌨️ 日常命令

| 命令 | 作用 |
|---|---|
| `tools/add.sh <图片\|视频> [目录]` | 压缩上传；`-k` 保原格式，`--avif` 转 AVIF |
| `tools/check.sh` | 本地预检（与 CI 同一套） |
| `tools/index.sh` | 重生成 [INDEX.md](INDEX.md) |

自动处理：长边 >2560px 等比缩小 → 按图分派压缩 → 超红线拒绝 → 重生成索引并打印直链。
依赖：`brew install webp`（必需）、`libavif`（AVIF 可选）、`oxipng pngquant`（保格式可选）。

## 🗜 压缩管线（透明度安全）

| 输入 | 处理 | 透明度 |
|---|---|---|
| 带 alpha 的 PNG | 无损 WebP（`cwebp -lossless -z9`），不更小则放弃 | **逐位保留**（实测往返一致） |
| 不透明 png/jpg | 有损 WebP q80 `-mt -sharp_yuv`（图形边缘锐化） | 无透明，不涉及 |
| `--avif` | AVIF 代替 WebP（再小 20-30%）；透明走无损 | 逐位保留（实测像素全等） |
| `og.*` / `-k` | 原格式内优化：oxipng / optipng 无损优先 | 保留 |

> og 社交分享卡默认不转现代格式 —— 部分社交平台抓取器兼容性差，PNG/JPG 最稳。

## 📁 目录约定

- **`<项目名>/`**：该仓库的推广素材，命名建议 `logo.*`、`banner.*`、`og.*`、`demo.gif` + `demo.mp4`、`shot-*.png`
- `temp/YYYY-MM/`：临时图（`add.sh` 默认落点）
- `free-imgbed/`：本方案自己的 logo（吃自己的狗粮 🐶）
- `web/` 是配套 R2 相册应用快照；其余历史路径只读保留

## 🔗 引用

复制即用片段（居中 logo、`<picture>` 渐进增强、国内 R2 镜像、缓存刷新）见 **[TEMPLATES.md](TEMPLATES.md)**。

```
https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/<路径>
```

## 🤖 CI

`assets-check` 在每次 push / PR 跑 `tools/check.sh`：尺寸红线、全仓重复检测、索引新鲜度，不过即挡。

## 📜 历史与许可

<details>
<summary>演进史（点开）</summary>

本仓原为个人图床（PicX 上传的图片堆）。2026-10-27 起三步转身：
① 与本地资源库（U 盘）逐文件 MD5 比对，清除 541 张重复图（443MB），废止「只进不出」旧政策；
② 转型开源项目推广素材库 + 免费图床方案，加入 CI 与压缩管线；
③ `git filter-repo` 重写历史剥离已删素材，clone 体积 418MiB → 2MB，更名 free-imgbed。

</details>

**许可**：代码（`tools/`、`.github/`、文档）[MIT](LICENSE) 随便用；**图片素材**（各 `<项目>/` 目录内）© webkubor 保留所有权利，第三方使用请先联系。fork 做自己的图床时，请替换素材为你自己的内容。
