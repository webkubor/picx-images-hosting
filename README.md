# picx-images-hosting

<p align="center">
  <a href="https://github.com/webkubor/picx-images-hosting"><img src="https://img.shields.io/github/stars/webkubor/picx-images-hosting?style=for-the-badge&color=coral" alt="Stars"></a>
  <a href="https://github.com/webkubor/picx-images-hosting/actions/workflows/check.yml"><img src="https://github.com/webkubor/picx-images-hosting/actions/workflows/check.yml/badge.svg" alt="assets-check"></a>
  <a href="https://github.com/webkubor/picx-images-hosting/commits"><img src="https://img.shields.io/github/last-commit/webkubor/picx-images-hosting?style=for-the-badge&color=4c9a6b" alt="最近提交"></a>
  <a href="https://github.com/webkubor/picx-images-hosting"><img src="https://img.shields.io/badge/img%20max-2MB-coral?style=for-the-badge" alt="img cap"></a>
  <a href="https://github.com/webkubor/picx-images-hosting"><img src="https://img.shields.io/badge/video%20max-10MB-coral?style=for-the-badge" alt="video cap"></a>
</p>

GitHub 开源项目**推广素材库**：各仓库的 logo、banner、OG 图、演示 GIF/MP4、宣传截图，
经 GitHub raw + jsDelivr CDN 分发。原图唯一权威来源是本地资源库（U 盘 `AI素材资源`）与 Cloudflare R2，不进这里。

## 红线（CI 强制）

1. **图片 ≤ 2MB，视频 ≤ 10MB**（jsDelivr 单文件上限 20MB，留余量）
2. **先压缩后进仓**：`tools/add.sh` 一条命令完成
3. **已上传文件不改名、不覆盖、不删除** —— 外链绑死路径
4. **内容重复即失败** —— 同一素材全仓只留一份，引用同一条外链

## 统一压缩上传

```bash
tools/add.sh <图片|视频> [目标目录]   # 默认落点 temp/YYYY-MM/
tools/check.sh                       # 本地预检（与 CI 同一套）
```

自动处理：长边 >2560px 等比缩小（sips）→ >100KB 的 png/jpg 转 WebP（cwebp q80，`brew install webp`）→ 超红线拒绝 → 重生成 [INDEX.md](INDEX.md) 并打印直链。

## 目录约定

- **`<项目名>/`**：该 GitHub 仓库的推广素材目录，命名建议
  `logo.*`、`banner.*`、`og.*`、`demo.gif` + `demo.mp4`、`shot-*.png`
- `temp/YYYY-MM/`：临时图（`add.sh` 默认落点）
- `blog/projects/…`、`dsh-env-inspector/`、`tombstone-reaper/`：历史路径，只读保留
- `web/`：R2 相册应用 pictures-lib 的仓内快照（非图床本体）

## 引用

各类场景的复制即用片段见 [TEMPLATES.md](TEMPLATES.md)。要点：

- CDN（优先）：`https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<路径>`
- 求稳用 git 标签替代 `@master`（标签不动图不动）
- GitHub raw 直链兜底；jsDelivr 缓存约 12h，`?updated=<时间戳>` 可立即刷新

## CI

`assets-check` 在每次 push / PR 时跑 `tools/check.sh`：尺寸红线、全仓重复检测、INDEX 新鲜度，不过即挡。

## 历史

- 2026-10-27 与 U 盘逐文件 MD5 比对，清除 541 张重复图（443MB）：**U 盘有全量副本，内容不丢，但引用旧路径的外链自此失效**。旧「只进不出」政策废止，以本 README 为准。

## 许可

本仓图片仅供 webkubor 个人项目使用。第三方使用请先联系。
