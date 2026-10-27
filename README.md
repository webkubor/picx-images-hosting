<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/mark-v3.svg" width="112" alt="free-imgbed logo">

  # free-imgbed

  **一个 GitHub 仓库，就是一台免费图床。**

  [![CI](https://github.com/webkubor/free-imgbed/actions/workflows/check.yml/badge.svg)](https://github.com/webkubor/free-imgbed/actions/workflows/check.yml)
  [![License](https://img.shields.io/badge/code-MIT-4c9a6b)](LICENSE)
</div>

图片和项目推广素材提交到仓库后，可通过 GitHub raw、jsDelivr CDN 访问。这里集中管理 README 的 logo、banner、截图及演示视频；[品牌资产清单](BRAND-ASSETS.md)记录现役路径、复用关系和待设计项。代码按 MIT 许可发布，项目图片素材保留原权利。

## 开始使用

1. Fork 此仓库并克隆到本机。需要压缩图片时安装 `cwebp`；在 macOS 上可执行 `brew install webp`。
2. 在仓库目录上传一张图片：`tools/add.sh ~/Desktop/logo.png my-project/`。文件名决定 URL 末尾的名称；脚本可能将 PNG/JPG 压缩为 `.webp`，以**实际打印的链接**为准。
3. 提交并推送脚本生成的文件和 `INDEX.md`，然后把链接贴进 README 或浏览器。

本页 logo 就是一个可点开的真实图片链接：

`https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/mark-v3.svg`

在其他项目里传图，可先在图床仓库执行 `tools/imgbed install`，登记自己的 Fork：`imgbed init <你的仓库地址>`；此后在任意目录执行 `imgbed push logo.png my-project/`，由 CLI 压缩、提交、推送并打印直链。

> 图片上限 2 MB，视频上限 10 MB。已有图片路径被外部 README 引用时不要改名或覆盖；要换图，上传一个带版本号的新文件。

## 文档

品牌交付：[新旧 logo 与颜色体系对照](https://imgbed.webkubor.online/design/logo-review.html) · [18 项待设计任务](https://imgbed.webkubor.online/design/logo-briefs.html) · [设计师 skill](.agents/skills/logo-brand-designer/SKILL.md) · [交付说明](design/DELIVERY.md)。每个新版都有透明底 1:1 SVG、颜色 token 和设计理念；页面可切深浅背景和尺寸，也可复制完整任务交给自己的设计 Agent。

VitePress 教程： [快速开始](docs/guide/getting-started.md) · [命名与链接](docs/guide/naming-and-links.md) · [全局 CLI](docs/guide/cli.md) · [压缩及透明度](docs/guide/compression.md) · [AI Agent 接入](docs/guide/ai-agents.md) · [自定义域名](docs/guide/custom-domain.md) · [引用模板](docs/guide/templates.md)。

自有域名也提供 HTTPS 图片地址，例如 [imgbed.webkubor.online/free-imgbed/logo.svg](https://imgbed.webkubor.online/free-imgbed/logo.svg)。新图须等 Pages 部署完成才会出现在自有域名下；目前文档首页偶发超时，README 图片优先使用上面已验证的 jsDelivr HTTPS 链接。

<!-- logo-gallery:start -->

## 🖼 项目 logo 墙

优先展示 `brand/*.json` 指定的新符号；深色主题用 `<picture>` 按系统偏好加载对应 `darkAsset`。旧素材 URL 继续保留。

| 项目 | 标识 | 文件 |
|---|---|---|
| chat-mood-gen | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/chat-mood-gen/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/chat-mood-gen/mark-v3.svg" width="120" height="120" alt="chat-mood-gen logo"></picture> | `chat-mood-gen/mark-v3.svg` |
| claude-usage-statusline | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/claude-usage-statusline/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/claude-usage-statusline/mark-v3.svg" width="120" height="120" alt="claude-usage-statusline logo"></picture> | `claude-usage-statusline/mark-v3.svg` |
| device-passport | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/device-passport/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/device-passport/mark-v3.svg" width="120" height="120" alt="device-passport logo"></picture> | `device-passport/mark-v3.svg` |
| dsh-llm-hub | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/dsh-llm-hub/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/dsh-llm-hub/mark-v3.svg" width="120" height="120" alt="dsh-llm-hub logo"></picture> | `dsh-llm-hub/mark-v3.svg` |
| facet | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/facet/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/facet/mark-v3.svg" width="120" height="120" alt="facet logo"></picture> | `facet/mark-v3.svg` |
| free-imgbed | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/mark-v3.svg" width="120" height="120" alt="free-imgbed logo"> | `free-imgbed/mark-v3.svg` |
| reel-kit | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/reel-kit/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/reel-kit/mark-v3.svg" width="120" height="120" alt="reel-kit logo"></picture> | `reel-kit/mark-v3.svg` |
| scorecard | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/scorecard/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/scorecard/mark-v3.svg" width="120" height="120" alt="scorecard logo"></picture> | `scorecard/mark-v3.svg` |
| supercli | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/supercli/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/supercli/mark-v3.svg" width="120" height="120" alt="supercli logo"></picture> | `supercli/mark-v3.svg` |
| vite-plugin-agent-eyes | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/vite-plugin-agent-eyes/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/vite-plugin-agent-eyes/mark-v3.svg" width="120" height="120" alt="vite-plugin-agent-eyes logo"></picture> | `vite-plugin-agent-eyes/mark-v3.svg` |
| voxflow | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/voxflow/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/voxflow/mark-v3.svg" width="120" height="120" alt="voxflow logo"></picture> | `voxflow/mark-v3.svg` |
| wallpaper-generator | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/wallpaper-generator/mark-v3-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/wallpaper-generator/mark-v3.svg" width="120" height="120" alt="wallpaper-generator logo"></picture> | `wallpaper-generator/mark-v3.svg` |

<!-- logo-gallery:end -->
