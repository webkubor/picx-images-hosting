# AI Agent 接入（一行提示词）

用 AI 编码工具（Claude Code / Codex / WorkBuddy / AGY / Hermes Agent / OpenClaw …）**一行命令都不用学**，把提示词丢给 agent 即可。

## 第一次，接入

```text
帮我接入我的免费图床 free-imgbed：克隆 https://github.com/webkubor/free-imgbed
并运行其中的 tools/imgbed install 完成全局安装；如果我有 GitHub 上的 fork 仓库，
用 imgbed init <我的fork地址> 登记。装好后告诉我怎么用。
```

## 之后日常，传图

```text
把 ./banner.png 传到图床的 my-project/ 目录，压缩后把直链给我
```

agent 自动完成压缩、提交、推送，并回一条点开就能看的 CDN 直链。

## 常驻配置

| 工具 | 接入方式 |
|---|---|
| Claude Code | 写进 `CLAUDE.md`，每个项目常驻可用 |
| Codex | 写进 `AGENTS.md` 常驻 |
| WorkBuddy / AGY / Hermes Agent / OpenClaw | 粘进对话或项目的 agent 配置/记忆文件即可，提示词通用 |

## 传完管理

```text
看看图床里 my-project 目录都有什么图
给 demo-banner 生成一条 @v1 标签的稳定链接
把图床里过期的活动图列出来，我确认后删掉
```
