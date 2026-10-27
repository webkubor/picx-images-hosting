# 查看与管理图片

- **全仓总目录**：[INDEX.md](https://github.com/webkubor/free-imgbed/blob/main/INDEX.md)，每个目录多少张一目了然，`tools/index.sh` 自动生成
- **逐张看**：GitHub 仓库页点进目录 → 点文件即预览；或把任意 CDN/raw 链接粘进浏览器
- **找链接**：`tools/add.sh` / `imgbed push` 上传时打印；历史图片的链接 = 固定前缀 + 仓内路径
- **删除/替换要谨慎**：外链可能散布在各项目 README、社交卡里。删除前用全仓搜索确认引用；替换同路径图片后记得 `?updated=` 刷缓存
