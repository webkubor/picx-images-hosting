<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg" width="112" alt="free-imgbed logo">

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

`https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg`

在其他项目里传图，可先在图床仓库执行 `tools/imgbed install`，登记自己的 Fork：`imgbed init <你的仓库地址>`；此后在任意目录执行 `imgbed push logo.png my-project/`，由 CLI 压缩、提交、推送并打印直链。

> 图片上限 2 MB，视频上限 10 MB。已有图片路径被外部 README 引用时不要改名或覆盖；要换图，上传一个带版本号的新文件。

## 文档

VitePress 教程： [快速开始](docs/guide/getting-started.md) · [命名与链接](docs/guide/naming-and-links.md) · [全局 CLI](docs/guide/cli.md) · [压缩及透明度](docs/guide/compression.md) · [AI Agent 接入](docs/guide/ai-agents.md) · [自定义域名](docs/guide/custom-domain.md) · [引用模板](docs/guide/templates.md)。

文档站部署在 `imgbed.webkubor.online`；域名的 HTTPS 证书验证完成前，以上仓库内链接可直接阅读，图片引用优先使用已可用的 **HTTPS jsDelivr 链接**。
