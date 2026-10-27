# SuperCLI mark-v3

## 形态

直接复用源仓正式的折返 S 路径和右下短横光标，没有另造终端框或工具列表图标。路径等比放大 4.85 倍，让原有 64 单位符号在 256 画布中占约 72–74%，不改变字形关系。

## 配色依据

`brand.html` 明确规定折返 S、输入光标和品牌蓝 `#002FA7`；源仓同时提供深色单色路径 `#19191D` 与浅色单色路径 `#EEF1F7`。本交付浅底采用规范品牌蓝，深底采用既有浅色标记。`accent` 记录源单色资产的正文色，并不额外画入几何。

## 小尺寸与主题使用

透明画布、无字形字体依赖；32px 预览中折返 S 仍是主体，短横光标保留约 1.5px 的可见厚度。浅底加载 `supercli/mark-v3.svg`，深底加载 `supercli/mark-v3-dark.svg`。浅色几何在白底对比度约 10.69:1，深色几何在 #0D1117 上约 16.73:1。

## 交付路径

- 浅底 SVG：`supercli/mark-v3.svg`
- 深底 SVG：`supercli/mark-v3-dark.svg`
- token：`brand/supercli.json`
- 本说明：`design/rationale/supercli.md`
- 保留旧路径：`supercli/logo.svg` 与 `supercli/logo-dark.svg`

## 局限

小光标是正式符号的一部分，在极低分辨率下比 S 更容易丢失；本次保证在 32px 栅格预览下可见，不承诺 16px 仍可辨。几何来自 SuperCLI 自有设计规范，仍需按源仓品牌文件的许可和项目流程使用。
