# claude-usage-statusline · mark v3

本次保留三条不同填充量的状态轨，用纯色分段代替渐变，以「平静到警戒」表达用量与限额。图形是本次设计解释和规范，不是 Anthropic 官方标志。

**形态。** 源仓 `README.md:7–9` 定义的是在一行状态栏查看消耗、上下文与限额；`:24` 明确非官方项目。`assets/logo.svg:16–28` 的三条用量轨是已有识别元素，新版保留并将轨道转为有透明余量的粗轮廓，不只是去掉背板。三轨按填充长度递增，保留空白终点；轨与轨之间留较大透明间距，使32px仍读成三个读数。三条轨是符号表达，不是三项真实数值截图；不使用 Claude 商标图形。

**配色依据。** `scripts/statusline.py:47–58` 明定每个主题都遵守左边平静、右边告警；default 的 sage `#74B388`、amber `#D1B566`、orange `#DE8A5F`、coral `#D65D5D` 分别定位0/55/80/100。新版 primary 取 sage，accent 取 coral，amber 是中段辅助色；为了小尺寸清晰，省略橙色节点，将连续渐变简化为三段纯色。琥珀大约从填充起点的55%位置开始，珊瑚从约80%开始，表达提前可见的警戒区，不宣称精确还原运行时色带采样。没有把 README 上 Claude 徽章的 `#D97757` 当项目主色。

onLight 轮廓 `#3A3A42` 来自 `assets/logo.svg:19` 的旧轨道色；onDark `#C6C6CE` 来自 `scripts/statusline.py:58` 的 mono 80%节点。本次将该现有浅灰借作深底轮廓 token，这是新标识规范，不修改脚本默认主题。`brand/claude-usage-statusline.json` 的固定 tokens 契约仅列主色/强调色/主题前景；第三辅助色 `#D1B566` 在该 JSON 的 rationale、此说明和 SVG 中明确记录。

**小尺寸与主题使用。** 主体包围盒 `(32,32)–(224,224)`，192/256＝75%。浅底使用 `claude-usage-statusline/mark-v3.svg`，深底使用 `claude-usage-statusline/mark-v3-dark.svg`；画布、轨道余量和行间均透明。两版分别在 256、144、64、32px 实际渲染，已在 `#FFFFFF`、`#F5F1EB`、`#0D1117`、`#1D1D21` 四底合成图中目视检查，32px 三轨、不同长度及末端 coral 可辨。8单位的粗轨折合32px约1px，仍可见；更小尺寸未验证。sage/amber 对白底仅2.46:1/2.00:1，因此应保持11.27:1的深灰轮廓，不能将这些浅色当小字单独使用。深底轮廓对 `#0D1117` 为11.15:1。色觉差异未做专门模拟，识别也依靠填充长度；任意彩色或纹理底未验证。128或256的 viewBox 都可无限缩放，此次扩大坐标是便于共同网格，不代表旧图低清。

**已运行验收。** `python3 /tmp/brand-tools-v3.17efpp/validate.py` 输出主版 `structure=PASS alpha=PASS negative-space=PASS bbox=(32, 32, 224, 224) span=75.0000% sizes=256/144/64/32 bytes=1130`，dark 版相同检查通过、1129 bytes，JSON `exact-contract/source-files/paths=PASS`。实际32px命令为 `rsvg-convert -w 32 -h 32 -o /tmp/brand-tools-v3.17efpp/claude-usage-statusline/final-32.png claude-usage-statusline/mark-v3.svg`，dark 与其余三种尺寸分别执行。检查 SVG 仅含 svg/title/desc/path，无铺底/位图/字体/滤镜/渐变/脚本；像素边角和轨道余量 alpha=0。已实际读取仓外 `/tmp/brand-tools-v3.17efpp/review.png` 及 `/tmp/brand-tools-v3.17efpp/final-review.png`，不是只凭文件存在或可解析判定通过。

**交付路径。** `claude-usage-statusline/mark-v3.svg`；`claude-usage-statusline/mark-v3-dark.svg`；`brand/claude-usage-statusline.json`；`design/rationale/claude-usage-statusline.md`。旧 `claude-usage-statusline/logo.svg` 保留原路径原内容。

**导入与局限。** 命令 `/tmp/brand-tools-v3.17efpp/import-repo/tools/add.sh /tmp/brand-tools-v3.17efpp/claude-usage-statusline/mark-v3.svg claude-usage-statusline`（dark 同方式）在仓外运行原版脚本隔离副本，输出 `✓ claude-usage-statusline/mark-v3.svg (1KB)`，再将结果只安装到授权路径。脚本 `:101–102` 读取到 sips 的 `256.000` 并提示 `integer expected`，退出0，另行渲染检查实际尺寸通过。隔离避免自动写本仓 INDEX；未运行全仓 tools/check.sh、gallery、完整构建、浏览器或远端连通性，也未调用 museav/付费模型。未更新 README、HTML 或巡检展示入口。`ready` 仅为本地设计与已列验收完成，不表示已发布或已接入。
