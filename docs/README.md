<div align="center">

<img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg" width="112" alt="free-imgbed logo">

# free-imgbed

**一个 GitHub 仓库，就是一台免费图床。**<br>
<sub><i>One GitHub repo is all it takes to run your own image CDN.</i></sub>

<a href="https://github.com/webkubor/free-imgbed/stargazers"><img src="https://img.shields.io/github/stars/webkubor/free-imgbed?style=flat-square&color=FF6F61" alt="Stars"></a>
<a href="https://github.com/webkubor/free-imgbed/actions/workflows/check.yml"><img src="https://github.com/webkubor/free-imgbed/actions/workflows/check.yml/badge.svg" alt="assets-check"></a>
<a href="https://github.com/webkubor/free-imgbed/blob/main/LICENSE"><img src="https://img.shields.io/badge/code%20license-MIT-4c9a6b?style=flat-square" alt="License"></a>
<a href="https://imgbed.webkubor.online"><img src="https://img.shields.io/badge/%F0%9F%93%9A%20%E6%96%87%E6%A1%A3-imgbed.webkubor.online-4c9a6b?style=flat-square" alt="Docs"></a>

**把图片提交进仓库，全世界就能通过一条链接看到它。** jsDelivr 全球分发 · CI 把关红线 · fork 改名即用 · 本仓就是活示例

</div>

---

## 🚀 快速开始

| 你想做什么 | 怎么做 |
|---|---|
| **传一张图** | `tools/add.sh 图片.png 目录/`（或 GitHub 网页拖拽上传） |
| **看一张图** | 链接粘进浏览器 —— 本页 logo 就是这么引用的：<br>`https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg` |
| **在别的项目里传** | `imgbed push 图片.png 目录/` —— 全局 CLI，压缩提交推送直链一条龙 |
| **用 AI 工具传** | Claude Code / Codex / WorkBuddy / AGY / Hermes / OpenClaw —— [一行提示词接入](https://imgbed.webkubor.online/guide/ai-agents) |

先 fork 改名，再把链接里的 `webkubor/free-imgbed` 换成你自己的 —— 就这些。

## 🛡 红线（CI 强制）

图片 ≤2MB · 视频 ≤10MB · 先压缩后进仓 · 已上传文件不改名不覆盖不删除 · 内容重复即失败

## 📚 文档

完整教程在 **[imgbed.webkubor.online](https://imgbed.webkubor.online)**（VitePress）：

[快速开始](https://imgbed.webkubor.online/guide/getting-started) · [命名与链接](https://imgbed.webkubor.online/guide/naming-and-links) · [查看与管理](https://imgbed.webkubor.online/guide/browsing) · [全局 CLI](https://imgbed.webkubor.online/guide/cli) · [压缩管线与透明度](https://imgbed.webkubor.online/guide/compression) · [自定义域名绑定](https://imgbed.webkubor.online/guide/custom-domain) · [国内 R2 镜像](https://imgbed.webkubor.online/guide/r2-mirror) · [AI Agent 接入](https://imgbed.webkubor.online/guide/ai-agents) · [CI 与红线](https://imgbed.webkubor.online/guide/ci) · [引用模板](https://imgbed.webkubor.online/guide/templates)

本地跑文档站：`cd docs && pnpm install && pnpm dev`

## 📜 历史与许可

<details>
<summary>演进史（点开）</summary>

本仓原为个人图床（PicX 上传的图片堆）。2026-10-27 起三步转身：
① 与本地资源库（U 盘）逐文件 MD5 比对，清除 541 张重复图（443MB），废止「只进不出」旧政策；
② 转型开源项目推广素材库 + 免费图床方案，加入 CI 与压缩管线；
③ `git filter-repo` 重写历史剥离已删素材，clone 体积 418MiB → 2MB，更名 free-imgbed，教程迁入 VitePress 文档站。

</details>

**许可**：代码（`tools/`、`.github/`、`docs/`）[MIT](LICENSE) 随便用；**图片素材**（各 `<项目>/` 目录内）© webkubor 保留所有权利，第三方使用请先联系。fork 做自己的图床时，请替换素材为你自己的内容。
