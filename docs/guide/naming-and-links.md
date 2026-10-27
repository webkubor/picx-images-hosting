# 图片命名与链接

## 图床链接长什么样

以本仓 logo 的链接为例，一共四段：

- `https://cdn.jsdelivr.net/gh/` —— 固定前缀，永远不变
- `webkubor` / `free-imgbed` —— GitHub 用户名 / 仓库名（fork 后换成你自己的）
- `@main` —— 分支或标签；求稳可换成 `@v1`：标签不动、图就不动
- `free-imgbed/logo.svg` —— **仓内路径 = 你放的目录 + 文件名**，这就是「图片名」的来源

## 三种等价形态

| 形态 | 长这样 | 适合 |
|---|---|---|
| CDN（推荐） | `cdn.jsdelivr.net/gh/用户/仓@main/路径` | 网页、README（缓存 ~12h，`?updated=<时间戳>` 立即刷新） |
| raw 兜底 | `raw.githubusercontent.com/用户/仓/main/路径` | CDN 抽风时的备份 |
| 国内镜像 | `img.webkubor.online/路径` | 大陆读者，见 [R2 镜像](./r2-mirror) |

## 命名规则

- 文件名叫什么，链接最后一段就是什么（`add.sh` 可能只把扩展名换成 `.webp`）
- 建议小写英文 + 连字符：`my-logo.png`、`demo-01.jpg`；中文文件名可用，但外链里会出现转义串
- **传完不改名** —— 外链绑死路径；要换新版传 `my-logo-v2.png`
- 同名上传会被**拒绝**（防弄断已有外链）；确要替换内容时用「同路径 + `?updated=<时间戳>` 刷缓存」的方式，并确认旧外链用途
