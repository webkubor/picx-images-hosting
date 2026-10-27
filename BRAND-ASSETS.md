# 品牌资产清单

本表记录 `~/dev` 自有项目 README 所用的项目标识及其质量边界。`logo.*` 只用于确认属于该项目、适合在 README 展示的图；banner、截图、favicon 不自动冒充 logo。图床中的既有 URL 不改名，跨项目相同素材只留一份。

| 项目 | 图床中的标识 | 状态 | 来源与说明 |
|---|---|---|---|
| free-imgbed | `free-imgbed/logo.svg` | 正式 logo | 本仓矢量标识 |
| claude-usage-statusline | `claude-usage-statusline/logo.svg` | 正式 logo | 项目已有 128×128 SVG；README 原用 256×256 PNG，已改用 SVG |
| device-passport | `device-passport/logo.svg` | 正式 logo | 项目已有 256×256 SVG；README 的 banner 保持原样 |
| supercli | `supercli/logo.svg` + `supercli/logo-dark.svg` | 明暗两版正式字标 | 源自项目 `public/brand/supercli-wordmark*.svg`，用 `picture` 按主题切换 |
| facet | `facet/icon.svg` | 正式标识，现役路径 | 项目 256×256 SVG；与 `logo.svg` 内容相同，保留已被引用的 `icon.svg`，避免重复文件 |
| chat-mood-gen | `chat-mood-gen/logo.svg` | 正式 logo | 项目已有 256×256 SVG |
| wallpaper-generator | `wallpaper-generator/logo.svg` | 正式 logo | 项目已有 512×512 SVG |
| scorecard | `scorecard/logo.svg` | README 专用标识 | 按应用 `src/components/Icon.vue` 的开口评分环品牌几何重绘；项目原 `public/logo.svg` 与 GHAM 完全相同，尚未更改应用内部资源 |
| dsh-llm-hub | `dsh-llm-hub/logo.png` | 正式 logo | 项目已有 512×512 PNG；现役 banner 仍走 R2 |
| voxflow / voxcraft | `voxflow/logo-icon.webp` | 共享正式标识，现役路径 | 两个仓库原文件完全相同，只保留一份并共享 URL |
| reel-kit | `reel-kit/logo.svg` + `reel-kit/logo-light.svg` | 明暗两版字标 | 两份内容不同，README 使用 `picture` 按主题切换 |
| vite-plugin-agent-eyes | `blog/projects/vite-plugin-agent-eyes/logo.webp` | 现役 logo | 保留旧路径以维持外链 |

## 待设计或核验

- **Scorecard 应用资源**：`public/logo.svg` 与 GHAM 的 logo 逐字节相同，文件内还写着 `aria-label="GHAM"`。README 已有独立标识；站点内部原资源仍需在项目仓库里按组件和 favicon 一起修正。
- **Bloom for Typora**：项目仅有花形 favicon；README 目前展示 banner，需按主题品牌另行确定正式字标或 logo。
- **Kyvault / xiaobai-kanban / boiling-snow**：README 顶部现有 banner/宣传图，不能仅凭文件名或 alt 文本认定它们是 logo。
- **没有可确认标识的项目**：先保留文本标题或现有 banner；不自动生成相同模板的占位 logo。

后续新增：先核对项目源文件、视觉用途及名称；优先用合格 SVG。上传后记录在本表，README 引用改为新 URL 并验证可访问。U 盘原始素材不动，旧外链保持可用。
