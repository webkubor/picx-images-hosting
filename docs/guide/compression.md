# 压缩管线（透明度安全）

| 输入 | 处理 | 透明度 |
|---|---|---|
| 带 alpha 的 PNG | 无损 WebP（`cwebp -lossless -z9`），不更小则放弃 | **逐位保留**（实测往返一致） |
| 不透明 png/jpg | 有损 WebP q80 `-mt -sharp_yuv`（图形边缘锐化） | 无透明，不涉及 |
| `--avif` | AVIF 代替 WebP（再小 20-30%）；透明走无损 | 逐位保留（实测像素全等） |
| `og.*` / `-k` | 原格式内优化：oxipng / optipng 无损优先 | 保留 |

## 设计要点

- **先检测再分派**：`sips -g hasAlpha` 判断透明通道，透明图绝不走有损，logo 边缘不发毛
- **不更小就放弃**：每次转换都对比前后体积，转换无收益则保留原格式，永不越压越大
- **超红线拒绝**：处理完仍超 2MB（图）/10MB（视频）直接退出，提示转存 U 盘或 R2
- **og 社交卡例外**：`og.*` 自动保原格式 —— 部分社交平台抓取器对 WebP/AVIF 兼容性差

## 依赖

```bash
brew install webp          # 必需（cwebp）
brew install libavif       # 可选（--avif）
brew install oxipng pngquant  # 可选（保格式优化；pngquant 为有损量化兜底，alpha 保留）
```
