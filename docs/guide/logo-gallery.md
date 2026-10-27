---
title: 项目 logo 墙
---

# 项目 logo 墙

仓库里各项目的标识，按 `<项目名>/` 归档；深浅两版用 `<picture>` 按系统主题自动切换。
本表由 `tools/gallery.sh` 自动生成，与 README 中的同名区块保持一致。

<div align="center">

| 项目 | 标识 |
|---|---|
| chat-mood-gen | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/chat-mood-gen/logo.svg" width="120" alt="chat-mood-gen logo"> |
| claude-usage-statusline | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/claude-usage-statusline/logo.svg" width="120" alt="claude-usage-statusline logo"> |
| device-passport | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/device-passport/logo.svg" width="120" alt="device-passport logo"> |
| dsh-llm-hub | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/dsh-llm-hub/logo.png" width="120" alt="dsh-llm-hub logo"> |
| facet | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/facet/icon.svg" width="120" alt="facet logo"> |
| free-imgbed | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg" width="120" alt="free-imgbed logo"> |
| reel-kit | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/reel-kit/logo.svg" width="120" alt="reel-kit logo"> |
| scorecard | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/scorecard/logo-v2.svg" width="120" alt="scorecard logo"> |
| supercli | <picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/supercli/logo-dark.svg"><img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/supercli/logo.svg" width="120" alt="supercli logo"></picture> |
| voxflow | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/voxflow/logo-icon.webp" width="120" alt="voxflow logo"> |
| wallpaper-generator | <img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/wallpaper-generator/logo.svg" width="120" alt="wallpaper-generator logo"> |

</div>

## 规范与来源

每个标识的来源、跨项目复用关系，以及哪些项目尚缺独立 logo，见仓库的
[BRAND-ASSETS.md](https://github.com/webkubor/free-imgbed/blob/main/BRAND-ASSETS.md)。

新增或替换标识后：

```bash
tools/add.sh 我的新logo.svg 我的项目名/    # 压缩入库并打印直链
tools/gallery.sh                            # 刷新 README 与本页的 logo 墙
tools/check.sh                              # 本地预检（CI 同一套）
```
