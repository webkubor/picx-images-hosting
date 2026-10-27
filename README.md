# picx-images-hosting

<p align="center">
  <a href="https://github.com/webkubor/picx-images-hosting"><img src="https://img.shields.io/github/stars/webkubor/picx-images-hosting?style=for-the-badge&color=coral" alt="Stars"></a>
  <a href="https://github.com/webkubor/picx-images-hosting/commits"><img src="https://img.shields.io/github/last-commit/webkubor/picx-images-hosting?style=for-the-badge&color=4c9a6b" alt="最近提交"></a>
  <a href="https://github.com/webkubor/picx-images-hosting"><img src="https://img.shields.io/github/license/webkubor/picx-images-hosting?style=for-the-badge&color=gold" alt="License"></a>
  <a href="https://github.com/webkubor/picx-images-hosting"><img src="https://img.shields.io/badge/max%20size-2MB-coral?style=for-the-badge" alt="size cap"></a>
</p>

个人图床：**只存「存证截图」和「临时小图」**，通过 GitHub raw + jsDelivr CDN 分发。
素材原图、完整资产与大图一律不进这里 —— 它们住在本地资源库（U 盘 `AI素材资源`）和 Cloudflare R2。

## 红线

1. **单文件 ≤ 2MB**，超限放 U 盘或 R2。
2. **先压缩后进仓**，用 `tools/add.sh` 一条命令完成（见下）。
3. **已上传文件不改名、不覆盖、不删除** —— 外链绑死路径。
4. **不存原图/大图**，原图永远以 U 盘为准，仓里只是分发副本。

## 统一压缩上传

```bash
tools/add.sh <图片> [目标目录]     # 默认落点 temp/YYYY-MM/
```

自动处理：长边 >2560px 等比缩小（sips）→ >100KB 的 png/jpg 转 WebP（cwebp q80，`brew install webp`）→ 超 2MB 拒绝 → 落盘后重生成 [INDEX.md](INDEX.md) 并打印 jsDelivr 直链。

## 目录约定

- `<项目名>/`（如 `dsh-env-inspector/`、`tombstone-reaper/`）：项目存证截图
- `temp/YYYY-MM/`：临时图（`add.sh` 默认落点）
- `blog/projects/…`：历史演示素材（只读保留）
- `web/`：R2 相册应用 pictures-lib 的仓内快照（非图床本体）

## 引用方式

```
https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<相对路径>
```

jsDelivr 缓存约 12 小时，紧急刷新可在链接后加 `?updated=<时间戳>`；GitHub raw 直链做兜底。

## 历史

- 2026-10-27 与 U 盘逐文件 MD5 比对，清除 541 张重复图（443MB）：**U 盘有全量副本，内容不丢，但引用旧路径的外链自此失效**。此前的「只进不出」政策同时废止，以本 README 为准。

## 许可

本仓图片仅供 webkubor 个人项目使用。第三方使用请先联系。
