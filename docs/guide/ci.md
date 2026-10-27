# CI 与红线

`assets-check` 在每次 push / PR 跑 `tools/check.sh`，三道闸：

1. **尺寸红线**：图片 ≤2MB、视频 ≤10MB（jsDelivr 单文件上限 20MB，留余量）
2. **全仓重复检测**：MD5 相同的文件即失败 —— 同一素材全仓只留一份
3. **索引新鲜度**：INDEX.md 与实际目录不一致即失败（本地 `tools/index.sh` 重生成）

不过即挡，不靠自觉。部署：`deploy-docs` workflow 把 `docs/` 构建后发布到 Pages（自定义域名见[自定义域名绑定](./custom-domain)）。
