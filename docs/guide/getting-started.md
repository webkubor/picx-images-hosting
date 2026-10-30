# 快速开始

> 第 0 步：fork 本仓（或 clone 后推到你自己的新仓）。之后所有链接里的 `webkubor/free-imgbed` 都换成 `你的用户名/你的仓`。

## 它是什么形态？

一句话：**把图片放进仓库，全世界就能通过一条链接看到它。** 它不是网页服务也不是 App，形态是「Git 仓库 + 三条终端命令」：

| 你想做什么 | 怎么做 | 需要什么 |
|---|---|---|
| 传一张图 | 终端 `tools/add.sh 图片.png 目录/`，或 GitHub 网页直接拖 | 一行命令 / 纯网页都行 |
| 看一张图 | 把图床链接粘进浏览器地址栏 | 只需浏览器 |
| 在网页 / README 里显示 | 粘一条 `<img>` 或 Markdown | 任何编辑器 |

## 5 分钟上手（拿本仓 logo 走一遍真流程）

**① 传** —— 文件放哪个目录、叫什么名，链接就是什么：

```bash
tools/add.sh ~/Desktop/my-logo.png 我的项目名/
```

屏幕直接打印成果，链接不用你自己拼：

```
✓ 我的项目名/my-logo.webp  (61KB)
  https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/我的项目名/my-logo.webp
```

**② 看** —— 把链接粘进浏览器地址栏就打开了。真实例子，点开就是 README 页头那张 logo：

> 🔗 <https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/mark-v3.svg>

在任意网页 / README 里写一行，图就出现在那里：

```html
<img src="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/free-imgbed/mark-v3.svg" width="112">
```

::: tip 不想碰终端？
GitHub 网页上 **Add file → Upload files** 直接拖图也能传，链接规则相同——只是没压缩，超 2MB 会被 CI 拦下，推荐命令行。
:::

## 全局 CLI：在别的项目里也能传

装一次全局 CLI，之后**任何目录**一条命令直达链接（压缩、提交、推送全自动）：

```bash
tools/imgbed install                    # 软链到 ~/.local/bin
imgbed init <你的fork仓库地址>           # 登记仓库（首次）
imgbed push banner.png my-project/      # 任意目录上传，直接打印直链
imgbed link my-project/banner.webp      # 查已有文件的直链
```

详见 [全局 CLI](./cli)。
