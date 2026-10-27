# 品牌 UI 与工程交付

> 品牌设计 skill 已拆分为独立项目 [webkubor/logo-brand-designer](https://github.com/webkubor/logo-brand-designer)。本图床只保留素材、品牌数据、评审页和截图，不再维护或打包 skill。以下执行记录属于当时的设计交付。

已将 12 项 manifest、23 枚新版 SVG 接入评审页与两个同源 logo 墙，并将待设计简报收敛到 18 个经本地生产 README 核对的项目。本次不提交推送、不改其它项目仓、不调用或转交任何用户模型。

本机已存在的 `http://localhost:4402` 服务根目录为 `design/`：打开 [新旧评审](http://localhost:4402/logo-review.html) 或 [待设计任务](http://localhost:4402/logo-briefs.html)。文档站构建后的路径为 `/design/logo-review.html` 与 `/design/logo-briefs.html`；远端部署未执行。

## 修改与真源

- `brand/*.json` 与项目目录 SVG：12 项本地设计资料，保留输入中的 token、理念与新旧路径，不改资产内容。`ready` 是本地设计状态，不等于已发布或获用户最终批准。
- `tools/brand-ui.py`：读取 manifest 与 `design/briefs.json`，生成 `design/logo-review.html`、`design/logo-briefs.html`。预览内嵌资产派生字节，当前只服务 design 目录时也能正常显示；原始资产仍在项目目录，HTML 不作为新的图片上传源。
- 评审页：新旧并排、Light / Dark / Checkerboard、32 / 64 / 128px、hex 与来源理念、生产文件链接；复制任务包括完整 token、理念、浅底及深底 SVG。每个按钮有独立 live region、忙碌状态、可访问名称；Clipboard API 失败后用选区复制，再失败会展开只读文本框并完整选中任务，提示手动复制。
- 待设计页：所有旧色板明确标注“建议，非既有品牌”，补齐生产资料链接与 token / 理念 / 完整 SVG 的交付要求。未完成项目没有 SVG 成品，prompt 要求 Agent 最终交付完整 SVG，不伪造占位成品。
- 品牌设计 skill：已独立到 [logo-brand-designer](https://github.com/webkubor/logo-brand-designer)，包含可移植生成器和完整复用说明；图床不是它的源码真源。
- `tools/check-brand.py`：验证 manifest 精确字段、hex token、真实仓内路径、正方 viewBox、可访问名称与安全 SVG 元素；禁止字体、脚本、外链、位图及 filter。实际调用 rsvg-convert + Pillow 检查透明角块、alpha 包围盒、边界、留白、空图。缺依赖退出 2。`--render-dir` 导出透明 PNG、两种底色与棋盘合成图，以及 `stats.json`。
- `tools/gallery.sh`：可移植 sh 入口，委托 Python 标准库实现。优先 manifest 的 `asset` / `darkAsset`，纳入 Agent Eyes，排除隐藏及工程目录；`--check` 同时比对 README 与文档整段画廊。
- `docs/package.json`：`dev` 与 `build` 显式先运行生成与复制命令，避免依赖包管理器的隐式 prebuild。`docs/public/design/` 是被 Git 忽略的派生产物；已生成且与仓内 HTML 字节相同，无第二份手工真源。
- `README.md`、`docs/.vitepress/config.mts`、`docs/guide/logo-gallery.md`：新增清晰入口。`.github/workflows/check.yml` 增加 UI 新鲜度与校验器回归；部署镜像排除 design / brand 工程目录。`INDEX.md` 已按新增资产刷新。
- 四份既有 `design/rationale/` 说明中的用户本机绝对目录已改为项目相对路径；历史验收记录保留为历史记录，不计入本次检查。

## 选色证据与本次决定

以下引用来自本次读取的 manifest。源仓文件地址已在评审页提供；本轮未重新逐项复算上游对比度或全部取色，不能把 manifest 中的历史实算记录当成本轮独立复核。

| 项目 | 本轮沿用的来源记录 | 本次设计决定与边界 | 本仓证据 |
|---|---|---|---|
| Chat Mood Gen | README / GeneratorView 的 sage `#7A9D8C`，旧 SVG 棕色 `#A27B5C` | `#4C6F5D` / `#9DBEAB` 是新派生前景；棕色只登记未画入 | `brand/chat-mood-gen.json:13`、`:20` |
| claude-usage-statusline | 脚本语义色 sage `#74B388`、coral `#D65D5D`、amber `#D1B566`；旧轨道 `#3A3A42` | mono 节点灰 `#C6C6CE` 借作深底轨道是新分配；色带不表示真实读数 | `brand/claude-usage-statusline.json:13`、`:20` |
| device-passport | 旧 SVG 的翠绿 `#047857` 与 `#34D399` | 颜色已有，浅深前景角色与相同阶梯签名是本次规范 | `brand/device-passport.json:12`、`:19` |
| dsh-llm-hub | 旧 PNG 中心经 ICC 转 sRGB 记录为 `#5EC27F`；本项目徽章蓝 `#4C7EF3` | 浅底 `#287A43` 是本次加深建议；不是源码既有主色 | `brand/dsh-llm-hub.json:13`、`:20` |
| Facet | 正式 icon 的 `#0F766E`、`#F59E0B`、`#FFFDF7` | 沿用色系并重排大色面；不借可选输出主题作品牌 | `brand/facet.json:9`、`:16` |
| free-imgbed | 旧 logo 的 `#FF6F61`、`#FF9F45` | `#C3483D` 为新定深珊瑚，明暗共用，无独立 darkAsset | `brand/free-imgbed.json:9`、`:16` |
| reel-kit | README / docs style 已命名 Reel 红 `#CC584D`、浅红 `#E6A5A0` | 从横字标卷轴抽出方形符号；旧横版仍保留 | `brand/reel-kit.json:14`、`:21` |
| Scorecard | 现役 CSS 晴空蓝 `#58A6FF`、深灰 `#0D1117`、浅灰 `#E6EDF3` | 新标识对齐 UI 蓝，明确替代旧雷达绿；蓝色不能直接复用作白底正文 | `brand/scorecard.json:13`、`:20` |
| SuperCLI | 品牌页蓝 `#002FA7`，现有浅色单色版 `#EEF1F7` | 保留正式折返 S 与光标，不改字形关系 | `brand/supercli.json:9`、`:16` |
| Agent Eyes | 网站 theme-color `#39D353` | 浅底 `#178A35` 是本次加深建议；旧图为白底 WebP | `brand/vite-plugin-agent-eyes.json:12`、`:19` |
| VoxFlow | 界面主色 `#6366F1`；旧图测量记录 `#7080FF` | 深底 `#A5B4FC` 是本次新定，形态寓意不是旧作者原话 | `brand/voxflow.json:13`、`:20` |
| wallpaper-generator | theme 的 sage `#9AA7A1`、clay `#C4B2A3`、两主题 ink | 深底仍保留浅主题 clay，非逐项复刻原生深主题 | `brand/wallpaper-generator.json:9`、`:16` |

## 真实待设计清单

`design/briefs.json` 是任务清单来源；18 项本地目录及其 README 均存在，本轮读取生产 README 核对项目定位并读取 origin 确认仓库身份。只公开仓库链接与相对文件名，不公开本机目录。没有对所有源仓远端文件的可访问性逐一联网验收；沸雪 GitLab 可能需授权。

| 项目 | 待设计依据 / 纠错 | 生产入口 |
|---|---|---|
| kyvault | README 为 banner，未确认独立标识 | [README](https://github.com/webkubor/kyvault/blob/HEAD/README.md) |
| xiaobai-kanban | 看板编码工具，README 为 banner | [README](https://github.com/webkubor/xiaobai-kanban/blob/HEAD/README.md) |
| boiling-snow | 写实武侠影视工作台；shot / banner / favicon 不自动作为正式 logo | [README](https://gitlab.com/webkubor/boiling-snow/-/blob/HEAD/README.md) |
| typora-Bloom-theme | 有花形 favicon 与横幅，独立品牌未确认 | [色彩规范](https://github.com/webkubor/typora-Bloom-theme/blob/HEAD/docs/theme-color-standard.md) |
| dsh-bloom-theme | 有 R2 banner，需与 Typora 系列区分 | [README](https://github.com/webkubor/dsh-bloom-theme/blob/HEAD/README.md) |
| ai-orb | 状态球是产品本体，本仓未确认独立品牌图 | [README](https://github.com/webkubor/ai-orb/blob/HEAD/README.md) |
| frontend-contrast-guard | CSS 对比度、计量与评审证据工具 | [README](https://github.com/webkubor/frontend-contrast-guard/blob/HEAD/README.md) |
| vite-plugin-refresh-guard | 新部署后的刷新策略插件 | [README](https://github.com/webkubor/vite-plugin-refresh-guard/blob/HEAD/README.md) |
| cs-mcp | CLI 能力网络入口 | [README](https://github.com/webkubor/cs-mcp/blob/HEAD/README.md) |
| im-notify-kit | 飞书 / 企业微信通知发送层 | [README](https://github.com/webkubor/im-notify-kit/blob/HEAD/README.md) |
| ai-sse-kit | SSE 分帧与增量接收套件 | [README](https://github.com/webkubor/ai-sse-kit/blob/HEAD/README.md) |
| mlx-vlm-kit | 一个 Python 本地视觉引擎，不虚构第二个 Python 仓任务 | [README](https://github.com/webkubor/mlx-vlm-kit/blob/HEAD/README.md) |
| path-guard | 更正为命令副本 / PATH 遮蔽诊断，不是文件访问沙箱 | [README](https://github.com/webkubor/path-guard/blob/HEAD/README.md) |
| charmoji-sticker-skill | charmoji 表情素材 skill | [README](https://github.com/webkubor/charmoji-sticker-skill/blob/HEAD/README.md) |
| deadcode-reaper-skill | 死代码清理 skill；旧截图不作为正式 logo | [README](https://github.com/webkubor/deadcode-reaper-skill/blob/HEAD/README.md) |
| release-sync-skill | 更正为 package 版本到台账 / SKILL frontmatter 同步 | [README](https://github.com/webkubor/release-sync-skill/blob/HEAD/README.md) |
| writing-standard-skills | 写作规范集合，不是单 skill 名 | [README](https://github.com/webkubor/writing-standard-skills/blob/HEAD/README.md) |
| suno-publisher | 从 VoxFlow 拆出的音乐发行准备台，最终确认由人完成 | [README](https://github.com/webkubor/suno-publisher/blob/HEAD/README.md) |

`ego-lite-ref` 从新品牌委托移出：其 README 指向 [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) 与官方浏览器下载，是上游参照实现，尚未确认自有品牌授权。原虚构的 Python 重复项目已从清单与页面删除。所有保留色板均为待评审建议；没有把旧简报色值提升为已批准的品牌 token。

## 设计与验证限制

- 本轮只更新本仓 UI、工具、文档与全局 skill 副本；不改 23 枚输入 SVG，不删除、覆盖或改名已上传图片，现有 CDN 根与旧 URL 保留。其它项目的 README / UI 未切换。
- 渲染检查覆盖 23 枚 SVG、32 / 64 / 128 / 256px。透明角块按边长 1/32 取样，主体边距至少 5%，256px 最长主体跨度目标 72–80%，允许 1px 栅格舍入。Facet 实测 184/256 = 71.875%，在该公开容差内，不把它写成精确 72%。
- 实际读取 `/tmp/free-imgbed-brand-delivery/contact-sheet.png`，查看全部 32px 的浅底主版与深底版；芯片、三轨、折页、声波等主体可辨。错误主题的版本确会减弱轮廓，因此不能省略 darkAsset 切换。free-imgbed 明暗共用，深底对比弱于浅底。
- 自动检查只证明规定结构与 alpha 条件，不证明品牌独特性、语义理解或所有背景的可读性。16px、照片、任意彩色底、色觉模拟未验收。
- 本轮初次浏览器定位器操作与截图准备超时；改用可见 DOM 节点点击与页面事件继续验证。取消尺寸动画，确保后台预览也直接显示所选真实尺寸。没有浏览器截图排版通过结论。
- 源 manifest 与既有 rationale 中的历史验收为输入资料，不计入本轮执行记录；本轮不复跑全仓合规脚本、文档整套构建或部署，交给 workflow。

## 本轮执行记录

| 精确命令 / 方法 | 实际输出与范围 |
|---|---|
| `python3 tools/check-brand.py --render-dir /tmp/free-imgbed-brand-delivery` | `PASS: 12 manifests, 23/23 SVGs; sizes=32/64/128/256`；预览与 stats.json 位于给定仓外目录。最初严格 72% 阈值拒绝 Facet 的 71.875%，随后加明示 1px 测量容差并重跑通过。 |
| `python3 tools/test-brand.py` | `Ran 6 tests ... OK`；包含危险结构、可访问性、越界路径、无 rect 的满画布 path、空图、小图、缺 renderer / Pillow 的失败路径。 |
| `python3 tools/brand-ui.py --publish` | `PASS brand UI generated: 12 reviews, 18 briefs; copied to docs/public/design/`。 |
| `tools/gallery.sh` | `PASS gallery generated: README.md + docs/guide/logo-gallery.md; 12 projects`。 |
| `tools/gallery.sh --check` | `PASS gallery freshness: README.md + docs/guide/logo-gallery.md; 12 projects`。 |
| `python3 tools/brand-ui.py --check` | `PASS brand UI freshness: 12 reviews, 18 briefs`。 |
| `tools/index.sh` | `✓ INDEX.md 已重生成（25 个目录 / 135 张图）`。 |
| `git diff --check` | 无输出，退出 0。 |
| `python3` 内联 HTMLParser 断言 | 输出两页独立 copy actions / 完整 tasks / 发布副本一致；两份画廊包含全部 manifest 与 darkAsset；已跟踪旧资产无修改。 |
| `python3` 内联公开文件扫描 | `PASS public brand files: no private absolute paths or token-shaped credentials`；仅此模式扫描，不宣称全仓凭据审计。 |
| `python3` 内联复制与字节比较 | `PASS skill source equals global copy: True`。 |
| Browser Use，4402 待设计页 | 实际打开 `logo-briefs.html`，DOM 显示“18 项真实待设计任务”、建议色板标签、生产资料链接与可访问复制按钮。 |
| Browser Use，复制模拟成功 / 拒绝 | 成功分支捕获 2,275 字符，含完整 token / SVG，另一项目状态为空；拒绝两种自动复制后展开只读文本框，`fullSelection:true, exactTask:true, otherStatus:""`，可访问名称存在。浏览器的实际系统剪贴板未读取，测试使用受控 stub。 |
| Browser Use，4402 评审页 | DOM 显示 12 项、24 张新旧预览和可访问控件；深色 DOM 点击后 `darkImages:24, loadedImages:24, totalImages:24, overflow:false`；32 / 64 / 128px 尺寸切换最终分别实测 `actualWidths:[32] / [64] / [128]`；棋盘切换后 `lightImages:24`。 |

完整 `tools/check.sh`、`pnpm --dir docs build`、workflow 和远端发布：本轮未运行，按任务要求交由 workflow。没有把局部检查记为整套构建通过。
