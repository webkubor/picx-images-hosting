# dsh-llm-hub · mark v3

本次用三个目录插槽接入同一背板，中央留一个蓝色汇聚节点，表达多厂商模型目录及网关管理。它保留旧图的绿色识别，形态和新 token 是本次设计规范，不冒充项目已有品牌寓意。

**形态。** 源仓 `README.md:27–38` 定义模型目录、网关状态、余额及用量等管理能力。三个有透明开口的插槽共享一个分叉背板，组成单一整体；三口是小尺寸构图选择，不表示只支持三个厂商或只提供三项功能。旧 `docs/images/logo.png` 为深底同心圆与文字，新图不再采用圆环雷达，不与 Scorecard 使用同一套环形评估语言；不嵌入、自动描摹旧位图，不保留文字和辉光。

**配色依据及新建议。** 旧图含 ICC 色彩配置，不能直接将 RGB 通道当 CSS sRGB。用 Pillow 12.1.1 读取源图与图床旧图，二者 SHA256 都是 `c28dafffe64ac3a9df45db79eec111a844cf4f64a7a2cd370c66e3f89b469a67`。命令中的核心计算为 `ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(BytesIO(im.info['icc_profile'])), ImageCms.createProfile('sRGB'), outputMode='RGB')`；输出 `source profile: Google/Skia/0E983EAA5A1289650CB7C7F6821DF696`，中心 `(256,256)` 原始 RGB `(120,192,133)`，sRGB `(94,194,127)`。中心裁切 `crop((241,241,271,271)).getcolors(900)` 返回 `[(900,(94,194,127))]`，因此深底 token 使用 `#5EC27F`。这只是旧图平色核心的测量，不是全图辉光的统计，也不是源码既有 hex token。

浅底 primary/onLight `#287A43` 是本次建议的新色：保持测得核心绿约139°的色相并加深，以提高白底轮廓对比；必须明确它不是原图精确色值。新建议的白底对比实算为 5.31:1，深底版 `#5EC27F` 对 `#0D1117` 为 8.56:1。蓝节点 accent `#4C7EF3` 有源仓 `README.md:13` npm 徽章、`:23` 网关主题徽章依据，本次才将它分配到图形节点，白/深底对比为3.76:1/5.03:1。`lib/client.js:469`、`:486–495` 使用宿主标签/状态和套餐颜色，未把这些宿主/账单状态误称为项目主色。token 定义见 `brand/dsh-llm-hub.json`。

**小尺寸与主题使用。** 主体包围盒 `(30,30)–(226,226)`，196/256＝76.56%；三个插槽开口留有透明负空间。浅底用 `dsh-llm-hub/mark-v3.svg`，深底用 `dsh-llm-hub/mark-v3-dark.svg`。两版都在 256、144、64、32px 实际渲染，并在白 `#FFFFFF`、暖浅 `#F5F1EB`、深 `#0D1117`、炭灰 `#1D1D21` 合成图中目视检查。32px 能识别三口背板和中央蓝点，但不会传达账单、余额等全部功能。16px、纹理及其它色底未验证；viewBox 大小不决定矢量清晰度。

**已运行验收。** `python3 /tmp/brand-tools-v3.17efpp/validate.py` 输出主版 `structure=PASS alpha=PASS negative-space=PASS bbox=(30, 30, 226, 226) span=76.5625% sizes=256/144/64/32 bytes=902`，dark 版相同检查通过、901 bytes，JSON `exact-contract/source-files/paths=PASS`。实际执行的32px命令为 `rsvg-convert -w 32 -h 32 -o /tmp/brand-tools-v3.17efpp/dsh-llm-hub/final-32.png dsh-llm-hub/mark-v3.svg`，dark 和其余尺寸分别执行。结构只含 svg/title/desc/path；角落、三口内部与主体间隙实际 alpha=0，无实底、位图、字体、渐变、滤镜或脚本。已目视读取仓外 `/tmp/brand-tools-v3.17efpp/review.png` 及 `/tmp/brand-tools-v3.17efpp/final-review.png`。

**交付路径。** `dsh-llm-hub/mark-v3.svg`；`dsh-llm-hub/mark-v3-dark.svg`；`brand/dsh-llm-hub.json`；`design/rationale/dsh-llm-hub.md`。旧 `dsh-llm-hub/logo.png` 不改名、不覆盖、不删除。

**导入与局限。** 命令 `/tmp/brand-tools-v3.17efpp/import-repo/tools/add.sh /tmp/brand-tools-v3.17efpp/dsh-llm-hub/mark-v3.svg dsh-llm-hub`（dark 同方式）运行的是仓库原版脚本隔离副本，输出 `✓ dsh-llm-hub/mark-v3.svg (0KB)`，只将处理后的 SVG 安装到指定路径。脚本 `:101–102` 对 sips 的 `256.000` 提示 `integer expected`，退出0，实际尺寸由 rsvg-convert 另验。隔离避免 add.sh 的 INDEX 副作用。全仓 tools/check.sh、gallery、完整构建、浏览器和远端 URL 检查未运行；未调用 museav 或付费模型，未修改展示入口。`ready` 表示本地三件套与所述渲染通过，不表示旧图已被替换上线。
