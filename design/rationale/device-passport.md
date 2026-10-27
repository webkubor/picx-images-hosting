# device-passport · mark v3

本次用「硬件芯片内两条完全相同的签名」表达设备状态的时间一致性。此寓意是本次设计解释，不是旧图注释或项目已有品牌宣言。

**形态。** 源仓 `README.md:48–59` 提出硬件状态不随时间任意变化、状态不可互相矛盾等核心概念；`:165–174` 进一步描述固定 seed 在不同时间复现同一设备。旧 `assets/logo.svg:221–271` 已有芯片和总线几何，取这部分可辨元素重做为粗轮廓、八根引脚和两条同色阶梯签名。两签名完全相同，避免被理解为两个不同设备。去掉 `assets/logo.svg:118` 的背板、`:150–208` 的盾牌、轨道、发光与微刻线；没有把旧复杂徽章简单去底。标识本身不作安全认证或官方护照的承诺。

**配色依据。** 主色/onLight `#047857` 直接来自 `assets/logo.svg:62–67` 的 emeraldBeam 绿色停靠色，选择这一已有深翠绿是为浅底保留清晰轮廓。accent/onDark `#34D399` 来自 `assets/logo.svg:32–37` 的 shieldLaser 绿色停靠色。两色均有源图依据，但把它们定义为浅底/深底品牌前景是本次新规范，不是按色值出现次数推算主色。源图中的青蓝与金色没有一同塞进新图；每版保持单色，让两条签名表达同一性。`brand/device-passport.json` 的 accent 是主题替代色，不代表第二种状态。

**小尺寸与主题使用。** 主体包围盒 `(32,32)–(224,224)`，跨度 192/256＝75%，两条阶梯之间留出透明负空间。`device-passport/mark-v3.svg` 用于浅底；`device-passport/mark-v3-dark.svg` 用于深底，画布都透明。主色对白底 5.48:1，深底色对 `#0D1117` 为 9.84:1。已在 256、144、64、32px 实际渲染，并在 `#FFFFFF`、`#F5F1EB`、`#0D1117`、`#1D1D21` 四种背景的合成图中目视检查。32px 芯片外轮廓、引脚和两条同形签名可辨；仅凭图形不能读出完整产品功能。矢量 viewBox 的 256 是坐标，不代表有限分辨率；16px、纹理和彩色底未验证。

**已运行验收。** `python3 /tmp/brand-tools-v3.17efpp/validate.py` 输出主版 `structure=PASS alpha=PASS negative-space=PASS bbox=(32, 32, 224, 224) span=75.0000% sizes=256/144/64/32 bytes=929`，dark 版同检查通过、928 bytes，JSON `exact-contract/source-files/paths=PASS`。其中实际执行 `rsvg-convert -w 32 -h 32 -o /tmp/brand-tools-v3.17efpp/device-passport/final-32.png device-passport/mark-v3.svg`，并分别执行 dark 与其余三种尺寸。脚本检查只含 svg/title/desc/path，无字体、位图、滤镜、脚本、渐变和铺底；检测角落及芯片内部负空间 alpha 为0。临时 `/tmp/brand-tools-v3.17efpp/review.png`、`/tmp/brand-tools-v3.17efpp/final-review.png` 均已实际读取目视，未将仅解析成功记为视觉通过。

**交付路径。** `device-passport/mark-v3.svg`；`device-passport/mark-v3-dark.svg`；`brand/device-passport.json`；`design/rationale/device-passport.md`。旧 `device-passport/logo.svg` 完整保留。

**导入与局限。** 原版 `tools/add.sh` 在仓外隔离仓调用，命令 `/tmp/brand-tools-v3.17efpp/import-repo/tools/add.sh /tmp/brand-tools-v3.17efpp/device-passport/mark-v3.svg device-passport`（dark 同方式）成功输出 `✓ device-passport/mark-v3.svg (0KB)`。脚本 `:101–102` 因 `sips` 返回 `256.000` 发出 `integer expected`，进程退出0；实际 SVG 尺寸、透明度与大小另行通过检查。处理结果只写本次指定路径，隔离了 add.sh 自动重写 INDEX 的行为。未执行全仓 `tools/check.sh`、gallery、完整构建、浏览器、远端连通性；没有 museav/付费出图，未更新 README、HTML 或巡检入口。`ready` 为本地设计交付状态，不代表部署或推广入口已更新。
