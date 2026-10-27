---
layout: home

hero:
  name: "free-imgbed"
  text: "一个 GitHub 仓库，就是一台免费图床"
  tagline: 图片提交进仓库，全世界通过一条链接看到 · jsDelivr 全球 CDN · CI 把关红线 · fork 改名即用
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/getting-started
    - theme: alt
      text: GitHub 仓库
      link: https://github.com/webkubor/free-imgbed
  image:
    src: https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg
    alt: free-imgbed

features:
  - icon: 🗜️
    title: 透明度安全的压缩
    details: 带 alpha 的 PNG 走无损 WebP（实测逐位保留），不透明才上有损，AVIF 一键再省 20-30%
  - icon: 🛡️
    title: CI 强制红线
    details: 图片 ≤2MB / 视频 ≤10MB、全仓内容查重、索引新鲜度，push 时自动拦截
  - icon: 🌍
    title: 全球分发 + 国内镜像
    details: GitHub raw + jsDelivr 直链开箱即用，国内读者可切 Cloudflare R2 自定义域镜像
  - icon: 🤖
    title: AI Agent 一行接入
    details: Claude Code / Codex / WorkBuddy / AGY / Hermes / OpenClaw —— 一行提示词完成接入与传图
  - icon: 📦
    title: 零依赖起步
    details: 不用装服务，clone 仅 ~2MB；三条命令管上传，任意项目里 imgbed push 直达链接
  - icon: ⚖️
    title: 代码 MIT 开源
    details: tools / workflow / 文档随便用随便改；fork 之后替换素材就是你自己的图床
