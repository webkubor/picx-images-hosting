# free-imgbed

<p align="center">
  <a href="https://github.com/webkubor/free-imgbed"><img src="https://img.shields.io/github/stars/webkubor/free-imgbed?style=for-the-badge&color=coral" alt="Stars"></a>
  <a href="https://github.com/webkubor/free-imgbed/actions/workflows/check.yml"><img src="https://github.com/webkubor/free-imgbed/actions/workflows/check.yml/badge.svg" alt="assets-check"></a>
  <a href="https://github.com/webkubor/free-imgbed/blob/main/LICENSE"><img src="https://img.shields.io/badge/code%20license-MIT-4c9a6b?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/webkubor/free-imgbed"><img src="https://img.shields.io/badge/img%20max-2MB-coral?style=for-the-badge" alt="img cap"></a>
  <a href="https://github.com/webkubor/free-imgbed"><img src="https://img.shields.io/badge/video%20max-10MB-coral?style=for-the-badge" alt="video cap"></a>
</p>

**开箱即用的 GitHub 免费图床**：一个仓库就是一台图床 —— 图片经 GitHub raw + jsDelivr 全球 CDN 分发，
CI 自动拦截超限与重复，`tools/` 三条命令管压缩上传。fork 改名即是你的图床。
本仓同时是 webkubor 的开源项目推广素材库（本方案的活示例）。

## 快速开始

1. fork 本仓（或 clone 后推到你自己的新仓），改成你喜欢的名字
2. 本地 clone，把 `<项目>/` 里的示例素材换成你的内容
3. 上传：`tools/add.sh <图片> <目录>`，按打印出的提示 commit + push
4. 任意项目里引用：`https://cdn.jsdelivr.net/gh/<你的用户名>/<你的仓>@main/<路径>`
   ——README / TEMPLATES 里的片段把前缀替换掉即可直接用

## 红线（CI 强制）

1. **图片 ≤ 2MB，视频 ≤ 10MB**（jsDelivr 单文件上限 20MB，留余量）
2. **先压缩后进仓**：`tools/add.sh` 一条命令完成
3. **已上传文件不改名、不覆盖、不删除** —— 外链绑死路径
4. **内容重复即失败** —— 同一素材全仓只留一份

## 日常命令

```bash
tools/add.sh <图片|视频> [目标目录]   # 压缩上传；-k 保原格式，--avif 转 AVIF
tools/check.sh                       # 本地预检（与 CI 同一套）
tools/index.sh                       # 重生成索引
```

## 压缩管线（透明度安全）

| 输入 | 处理 | 透明度 |
|---|---|---|
| 带 alpha 的 PNG | 无损 WebP（`cwebp -lossless -z9`），不更小则放弃 | **逐位保留**（实测往返一致） |
| 不透明 png/jpg | 有损 WebP q80 `-mt -sharp_yuv`（图形边缘锐化） | 无透明，不涉及 |
| `--avif` | AVIF 代替 WebP（再小 20-30%）；透明走无损 | 逐位保留（实测像素全等） |
| `og.*` / `-k` | 原格式内优化：oxipng / optipng 无损优先 | 保留 |

依赖：`brew install webp`（必需）、`brew install libavif`（AVIF 可选）、
`brew install oxipng pngquant`（保格式可选，pngquant 为有损量化兜底，alpha 保留）。
og 社交分享卡默认不转现代格式 —— 部分社交平台抓取器兼容性差，PNG/JPG 最稳。

## 目录约定

- **`<项目名>/`**：该 GitHub 仓库的推广素材，命名建议
  `logo.*`、`banner.*`、`og.*`、`demo.gif` + `demo.mp4`、`shot-*.png`
- `temp/YYYY-MM/`：临时图（`add.sh` 默认落点）
- `blog/projects/…` 等历史路径只读保留；`web/` 是配套 R2 相册应用快照

## 引用

复制即用片段（含 `<picture>` 渐进增强、国内 R2 镜像说明）见 [TEMPLATES.md](TEMPLATES.md)。
CDN 前缀：`https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/<路径>`；
求稳可用 git 标签替代 `@main`；缓存约 12h，`?updated=<时间戳>` 立即刷新。

## CI

`assets-check` 在每次 push / PR 跑 `tools/check.sh`：尺寸红线、全仓重复检测、索引新鲜度，不过即挡。

## 许可

- **代码**（`tools/`、`.github/`、脚本与文档）：[MIT](LICENSE)，随便用、随便改
- **图片素材**（各 `<项目>/` 目录内）：© webkubor 保留所有权利，仅供其本人项目使用，第三方使用请先联系
- fork 做自己的图床时，请替换素材目录为你自己的内容

## 历史

2026-10-27 与 U 盘逐文件 MD5 比对清除 541 张重复图（443MB），旧「只进不出」政策废止，以本 README 为准；
同日重写 git 历史、剥离已删素材的大对象，clone 体积由 418MiB 降至个位数 MB —— fork 零负担。
