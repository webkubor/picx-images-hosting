# Scorecard · mark v3

本次设计沿用近期的「雷达包络＋勾选」识别，不回退为历史 GitHub 账户管理图形。形态及色彩角色分配是本次设计解释，不能当作项目历史品牌寓意。

**形态。** 源仓 `public/logo.svg:5–9` 与本仓 `scorecard/logo-v2.svg:5–9` 的不规则雷达面和勾选保留为核心。新版放大为实色包络，以粗开口量环代替两圈细圆、轴线和透明细节，形成单一评估仪表。所有可见形状均为手写填充路径，画布和量环间隙透明。包络的转折不表示固定维度数：源仓 `README.md:12–24`、`:50–58` 分别定义 GitHub、npm、网页、个人与 GEO 的不同对象和维度。本图不是认证章，也不代表全部指标通过。

**配色依据。** 源仓 `src/styles/global.css:11–15` 明确把 `#58A6FF` 定为晴空蓝主题色，新主色对齐这一现役界面规范。旧雷达 `#6CCDBC` 绿边和 `#5AD3BE` 透明面（`public/logo.svg:8`）不再承担主色，这是本次决定，不能称为精确沿用旧绿。浅底量环与勾选 `#0D1117` 来自同 CSS `:3`；深底量环 `#E6EDF3` 来自 `:8`。深底版内部勾选仍用 `#0D1117`，使其与蓝面保持 7.49:1 的色对比。`brand/scorecard.json` 中 `onLight/onDark` 指主题轮廓前景，不是背景；两版画布均透明。

**小尺寸与主题使用。** 主体渲染包围盒为 `(32,31)–(223,224)`，最长 193/256＝75.39%；viewBox 是矢量坐标，不是像素清晰度。浅底用 `scorecard/mark-v3.svg`，深底用 `scorecard/mark-v3-dark.svg`。两版已分别渲染为 256、144、64、32px，并在白色 `#FFFFFF`、暖浅色 `#F5F1EB`、深色 `#0D1117`、炭灰 `#1D1D21` 合成图中目视检查。32px 可见不规则面、勾选和量环；主版放深底会丢量环，应切换 dark 版。晴空蓝对白色为 2.53:1，依靠深轮廓与勾选维持小尺寸识别；该比例不能当作正文文字通过对比要求的结论。彩色或纹理背景未验证，16px 未验证。

**已运行验收。** 命令 `python3 /tmp/brand-tools-v3.17efpp/validate.py` 输出：主版 `structure=PASS alpha=PASS negative-space=PASS bbox=(32, 31, 223, 224) span=75.3906% sizes=256/144/64/32 bytes=661`，dark 版相同检查通过、660 bytes，JSON 的 `exact-contract/source-files/paths=PASS`。脚本对每版执行 `rsvg-convert -w 32 -h 32 -o /tmp/brand-tools-v3.17efpp/scorecard/final-32.png scorecard/mark-v3.svg` 等全部四种尺寸命令；检查 SVG 只含 svg/title/desc/path、无位图/字体/滤镜/脚本/渐变/铺底，像素边角和量环负空间为透明，主体跨度满足 72%–80%。实际目视读取临时预览 `/tmp/brand-tools-v3.17efpp/review.png` 和 `/tmp/brand-tools-v3.17efpp/final-review.png`；预览是仓外验收产物，不是交付 SVG 替代。

**交付路径。** 主版 `scorecard/mark-v3.svg`；深底版 `scorecard/mark-v3-dark.svg`；token 与来源 `brand/scorecard.json`；本说明 `design/rationale/scorecard.md`。旧 `scorecard/logo.svg`、`scorecard/logo-v2.svg` 保留。

**导入与局限。** SVG 先暂存仓外，调用隔离仓中的原版脚本 `/tmp/brand-tools-v3.17efpp/import-repo/tools/add.sh /tmp/brand-tools-v3.17efpp/scorecard/mark-v3.svg scorecard`（dark 版同方式），再将脚本输出以不存在才创建的方式放入指定路径。脚本输出 `✓ scorecard/mark-v3.svg (0KB)`；其 `tools/add.sh:101–102` 对 `sips` 返回的 `256.000` 发出 `integer expected` 提示，但进程退出 0，另行实际渲染和结构检查通过。隔离方式避免 `tools/add.sh:140` 改写本仓 INDEX。没有运行会改 INDEX 的全仓 `tools/check.sh`、gallery、完整构建或浏览器实测；没有调用 museav 或付费模型，没有检查远端 URL，也未接入 README、HTML、画廊或巡检入口。`ready` 只表示本地三件套设计与上述渲染验收完成，不表示已经发布或接入。
