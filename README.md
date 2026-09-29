# picx-images-hosting

个人图床：所有公开图片的单一来源，通过 GitHub raw + jsDelivr CDN 分发。

## 用法

仓库里的每张图片都可以这样引用：

```
https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/<相对路径>
```

例如 `concert/02-beijing-v2.png`：

```
https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master/concert/02-beijing-v2.png
```

任何仓库的 README 文档、项目官网、博客文章只要引用这个前缀的链接，就和这张图绑死——改图不改链接。

## 目录

目录按主题分组：`concert/`、`coffee/`、`wallpaper/`、`brand/`、`boiling-snow-film/`、`projects/`、`web/`、`xianbei/` 等。完整列表见 [INDEX.md](INDEX.md)。

`INDEX.md` 是一次性脚本跑出来的（仓内没有留下该脚本），当前快照是 2026-09-18 14:47 UTC / 38 个目录 / 518 张图。索引与实际目录不一致时，以实际目录为准，按下面的格式手工补一行即可。

## 上传新图

> 2026 起本仓**冻结新增**（见 git log 里的 `chore: 撤回误上传`），新图改走 Cloudflare R2，再以自定义域名引用。
> 历史图片仍按原路径留在 GitHub raw + jsDelivr CDN 上，不影响已有链接。

如果你确实需要往这里补一张兼容历史的图：

1. 在合适的子目录放下原始文件（保持目录命名单数风格：`concert/` 而不是 `concerts/`）。
2. 补一条 `INDEX.md` 里的对应行，格式跟邻近条目保持一致：`- [目录名/](目录名/) — N images`。
3. `git add . && git commit && git push`。
4. 引用方刷新缓存（jsDelivr 缓存约 12 小时，可加 `?updated=<ts>` 立刻失效）。

## 许可

本仓图片仅供 webkubor 个人项目使用。第三方使用请先联系。