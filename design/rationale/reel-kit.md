# reel-kit · mark v3

- **形态**：从源仓 `docs/logo.svg:3-12` 的卷轴抽出同心轮与四个穿孔，统一加粗至可见线条，不带原横字标的 text。对应短视频合成引擎（`README.md:18-22`），几何继承旧卷轴，不做片头播放按钮。
- **配色依据**：`README.md:48-53` 与 `docs/style.css:1-5` 直接命名主色 Reel 红 `#CC584D`、浅红 `#E6A5A0`；前者浅底，后者暗底，无新立任意品牌主色。
- **小尺寸与主题**：256 方形画布；视觉范围约 33–223，14 单位轮廓，穿孔以 22 单位直径放大。32px 两种底色已实际渲染可辨；更小 favicon 尺寸未验证。主版在浅底、dark 版在深底，透明负空间不会被底板封住。
- **交付**：`reel-kit/mark-v3.svg`、`reel-kit/mark-v3-dark.svg`；token 见 `brand/reel-kit.json`。旧 `reel-kit/logo.svg` 与 `reel-kit/logo-light.svg` 作为横向字标仍保留；README 的主题切换暂仍引用旧版，本轮不改展示入口或验证远端。
