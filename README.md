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
- **开源项目推广素材管理** —— 按项目归档 logo / banner / OG 图 / 演示 GIF+MP4；项目 logo 的来源、重复关系与待设计项见 [品牌资产清单](BRAND-ASSETS.md)

## 🧭 这是什么

一句话：**把图片放进这个仓库，全世界就能通过一条链接看到它。**

它不是网页服务，也不是 App，形态是「Git 仓库 + 三条终端命令」：

| 你想做什么 | 怎么做 | 需要什么 |
|---|---|---|
| 传一张图 | 终端敲 `tools/add.sh 图片.png 目录/`，或 GitHub 网页直接拖 | 一行命令 / 纯网页都行 |
| 看一张图 | 把图床链接粘进浏览器地址栏 | 只需浏览器 |
| 在网页 / README 里显示 | 粘一条 `<img>` 或 Markdown | 任何编辑器 |

## 🚀 5 分钟上手（拿本页 logo 走一遍真流程）

> **第 0 步**：fork 本仓（或 clone 后推到你自己的新仓）。之后所有链接里的 `webkubor/free-imgbed` 都换成 `你的用户名/你的仓`。下面用本仓当例子走真实流程。

本页头上的 logo 🟠 就是用这套流程传上去的，全程两步：

**① 传** —— 文件放哪个目录、叫什么名，链接就是什么：

```bash
# 起好名再传（建议小写英文 + 连字符，如 my-logo.png）
tools/add.sh ~/Desktop/my-logo.png 我的项目名/
```

屏幕直接打印成果，链接不用你自己拼：

```
✓ 我的项目名/my-logo.webp  (61KB)
  https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/我的项目名/my-logo.webp
```

**② 看** —— 把链接粘进浏览器地址栏就打开了。真实例子，点开就是本页那张 logo：

> 🔗 **https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg**

在任意网页 / README 里写一行，图就出现在那里（本页头图就是这么来的）：

```html
<img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/logo.svg" width="112">
```

> 💡 不想碰终端？GitHub 网页上 **Add file → Upload files** 直接拖图也能传，链接规则相同——只是没压缩，超 2MB 会被 CI 拦下，所以还是推荐命令行。
>
> 🌍 **在别的项目里做图，懒得切目录？** 装一次全局 CLI，之后任何目录 `imgbed push 图片.png 目录/` 一条到位——压缩、提交、推送、直链全自动（见下）。

## 🔗 图床链接长什么样

以上面 logo 的链接为例，一共四段：

- `https://cdn.jsdelivr.net/gh/` —— 固定前缀，永远不变
- `webkubor` / `free-imgbed` —— 你的 GitHub 用户名 / 仓库名（fork 后换成你自己的）
- `@main` —— 分支或标签（求稳可换成 `@v1`：标签不动、图就不动）
- `free-imgbed/logo.svg` —— **仓内路径 = 你放的目录 + 文件名**，这就是"图片名"的来源

三种等价形态，随便换用：

| 形态 | 长这样 | 适合 |
|---|---|---|
| CDN（推荐） | `cdn.jsdelivr.net/gh/用户/仓@main/路径` | 网页、README（缓存 ~12h，`?updated=<时间戳>` 立即刷新） |
| raw 兜底 | `raw.githubusercontent.com/用户/仓/main/路径` | CDN 抽风时的备份 |
| 国内镜像 | `img.webkubor.online/路径` | 大陆读者（见 [TEMPLATES.md](TEMPLATES.md) R2 方案） |

## 🖼 怎么查看 / 管理图片

- **全仓总目录**：[INDEX.md](INDEX.md)，每个目录多少张一目了然
- **逐张看**：仓库页点进目录 → 点文件即预览；或把任意 CDN/raw 链接粘进浏览器
- **命名规则**：文件名叫什么，链接就是什么（`add.sh` 可能只把扩展名换成 `.webp`）；**传完不改名**——外链绑死路径，要换新版就传 `my-logo-v2.png`，同名会被拒绝以防弄断已有外链

## ⌨️ 日常命令

**仓库内（在图床仓目录里用）：**

| 命令 | 作用 |
|---|---|
| `tools/add.sh <图片\|视频> [目录]` | 压缩上传；`-k` 保原格式，`--avif` 转 AVIF |
| `tools/check.sh` | 本地预检（与 CI 同一套） |
| `tools/index.sh` | 重生成 [INDEX.md](INDEX.md) |

**全局 CLI（装一次，任何项目里用）：**

```bash
tools/imgbed install          # 软链到 ~/.local/bin，之后任意位置可用 imgbed
imgbed init <你的fork地址>    # 登记图床仓库（首次）
imgbed push banner.png my-project/   # 任意目录：压缩→提交→推送→打印直链
imgbed link my-project/banner.webp   # 查已有文件的直链
```

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

## 🤖 AI Agent 接入（一行提示词）

用 AI 编码工具（Claude Code / Codex / WorkBuddy / AGY / Hermes Agent / OpenClaw …）的话，**你一行命令都不用学**，把提示词丢给 agent 就行。

**第一次，接入（一句话）：**

```text
帮我接入我的免费图床 free-imgbed：克隆 https://github.com/webkubor/free-imgbed
并运行其中的 tools/imgbed install 完成全局安装；如果我有 GitHub 上的 fork 仓库，
用 imgbed init <我的fork地址> 登记。装好后告诉我怎么用。
```

**之后日常，传图（一句话）：**

```text
把 ./banner.png 传到图床的 my-project/ 目录，压缩后把直链给我
```

agent 会自动完成压缩、提交、推送，并回你一条点开就能看的 CDN 直链。

| 工具 | 怎么接入 |
|---|---|
| Claude Code | 提示词直接粘进对话；写进 `CLAUDE.md` 则每个项目常驻可用 |
| Codex | 提示词粘进对话；写进 `AGENTS.md` 常驻 |
| WorkBuddy / AGY / Hermes Agent / OpenClaw | 粘进对话或项目的 agent 配置/记忆文件即可，提示词通用 |

> 多项目团队可以把接入提示词放进各自的 agent 配置文件，一次配置、全项目受益。

## 🛡 CI

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
