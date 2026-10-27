# AGENTS.md — AI 助手工作守则

## 这是什么

GitHub 开源项目**推广素材库**，同时是一套**开箱即用的 GitHub 免费图床方案**（fork 即用）：
logo / banner / OG 图 / 演示 GIF+MP4 / 宣传截图，GitHub raw + jsDelivr 分发。
内容仓，无构建无测试（`web/` 是 R2 相册应用快照，非图床本体）。
许可：代码 MIT（见 LICENSE），`<项目>/` 下图片 © webkubor 保留所有权利。

## 红线（CI 强制，2026-10-27 起）

- **图片 ≤ 2MB，视频 ≤ 10MB**，超限放 U 盘（`AI素材资源`）或 Cloudflare R2。
- **先压缩后进仓**：一律 `tools/add.sh`，提交前 `tools/check.sh` 预检。
- **已上传文件不改名、不覆盖、不删除** —— 外链绑死路径。
- **内容不重复**：同一素材全仓一份，新目录要放相同内容时引用已有外链。
- **原图不进仓**：U 盘是原图唯一权威来源。

## 目录约定

- 推广素材进顶层 `<项目名>/`；确认归属和展示用途的正式标识才用 `logo.*` 命名。banner、截图、favicon 不冒充 logo；现役外链保留。品牌来源及待设计项见 [BRAND-ASSETS.md](BRAND-ASSETS.md)，巡检用 `python3 tools/audit-brand.py`。
- 临时图进 `temp/YYYY-MM/`；`blog/projects/…` 等历史路径只读保留
- 引用片段抄 [TEMPLATES.md](TEMPLATES.md)

## 历史

2026-10-27 已按 U 盘 MD5 比对清除 541 张重复图（443MB），旧「只进不出」政策废止，以 README 为准。
