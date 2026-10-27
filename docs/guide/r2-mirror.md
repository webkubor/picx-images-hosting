# 国内 R2 镜像

jsDelivr 自 2022 年起在中国大陆无 ICP、访问不稳。面向国内读者的页面，把素材同步到 Cloudflare R2 + 自定义域：

- 本仓配套管理端快照在 [`web/`](https://github.com/webkubor/free-imgbed/tree/main/web)，线上 `img.webkubor.online`
- 引用换 `https://img.webkubor.online/<同路径>`，两套链接按受众选用
- 同步策略：新图走 R2 上传，历史图按需搬运（U 盘是原图权威来源，仓与 R2 都只是分发副本）
