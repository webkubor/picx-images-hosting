# wallpaper-generator mark-v3

## 形态

四个裁切角框住一段地平线与山形，表达在不同设备画幅中取景和调整壁纸构图。它把现有“圆环加星”的通用宇宙意象改为产品实际提供的裁切与多设备适配；裁切角的含义是本次设计解释。

## 配色依据

源仓 `src/styles/theme.scss` 将 `#9AA7A1` 命名为 sage 并指定为 primary，将 `#C4B2A3` 命名为 clay，并把浅主题 ink 定义为 `#3F3A36`、深主题 ink 定义为 `#E6E0D8`。浅底版用 ink 作主体、sage 作山体、clay 作日轮；深底版只将前景改为深主题 ink，保留同一山形与日轮。其中日轮有意沿用浅主题 clay `#C4B2A3`；原生深主题 clay 实为 `#B29F91`（同文件 :31），因此这不是逐项复刻原生深主题。两份 ink 均为源仓 token，不另造品牌颜色。

## 小尺寸与主题使用

外框仍按 1.05 倍放大，线宽 14 缩放后为 14.7 单位；256px 实际渲染主体包围盒为 `(34,31)–(222,223)`，最长跨度 75%。本轮移除场景的二次放大，将山脚收窄为 x=65–191，再由外层统一变换。将外框与场景分别渲染到 1024px alpha mask，两版重叠像素均为 0；外框 mask 向四周扩张 32px（8 个 viewBox 单位）后仍与场景无交集。本轮实际查看 144px、真实 32px 及其像素放大预览，裁切角、山体与日轮间保留透明间隙。透明画布不铺底。浅色主题用 `mark-v3.svg`，深色主题用 `mark-v3-dark.svg`；本轮查看背景为 #FFFFFF 与 #0D1117，未将结果扩展为任意背景通过。

## 交付路径

- 浅底 SVG：`wallpaper-generator/mark-v3.svg`
- 深底 SVG：`wallpaper-generator/mark-v3-dark.svg`
- token：`brand/wallpaper-generator.json`
- 本说明：`design/rationale/wallpaper-generator.md`
- 保留旧路径：`wallpaper-generator/logo.svg`

## 局限

符号突出壁纸取景，不描绘模板保存、文字水印或导出等次级能力。源仓主题同样把 ink 用作不同背景上的文字色；这里将它用于纯 SVG 前景，背景仍完全透明。复杂照片背景上的局部区域可能降低标识可读性，应通过实际版面留白来处理。
