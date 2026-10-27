#!/usr/bin/env bash
# 统一压缩上传入口：tools/add.sh [-k] [--avif] <图片|视频> [目标目录]
#   -k, --keep-format  保原格式优化（不转现代格式）；og.* 社交卡自动走此路径
#   --avif             转 AVIF 代替 WebP（再小 20-30%，需 brew install libavif）
# 红线：图片 ≤ 2MB、视频 ≤ 10MB；先压缩后进仓；同名即拒绝（外链绑死路径）。
# 压缩管线（透明度安全）：
#   透明 PNG → 无损 WebP/AVIF（alpha 逐位保留）
#   不透明 png/jpg → 有损 WebP q80 -mt -sharp_yuv（图形边缘锐化）
#   og.* / -k → 原格式内优化（oxipng/optipng 无损；pngquant 有损量化兜底，alpha 保留）
# 推广素材建议落 <项目名>/，命名 logo.* banner.* og.* demo.gif + demo.mp4 shot-*.png
set -euo pipefail

IMG_MAX=$((2 * 1024 * 1024))
VID_MAX=$((10 * 1024 * 1024))
CONVERT_THRESHOLD=$((100 * 1024))
MAX_SIDE=2560
WEBP_Q=80
AVIF_Q=60

die() { echo "✗ $*" >&2; exit 1; }
note() { echo "↳ $*"; }

KEEP_FORMAT=0; USE_AVIF=0; ARGS=()
for a in "$@"; do
  case "$a" in
    -k|--keep-format) KEEP_FORMAT=1 ;;
    --avif) USE_AVIF=1 ;;
    *) ARGS+=("$a") ;;
  esac
done
[ ${#ARGS[@]} -ge 1 ] || die "用法: tools/add.sh [-k] [--avif] <图片|视频> [目标目录]（默认 temp/YYYY-MM/，推广素材建议 <项目名>/）"
SRC=${ARGS[0]}
DEST_DIR=${ARGS[1]:-"temp/$(date +%Y-%m)"}
[ -f "$SRC" ] || die "文件不存在: $SRC"

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || die "请在仓库内运行"
cd "$REPO_ROOT"

BASE=${SRC##*/}
NAME="${BASE%.*}"; EXT="${BASE##*.}"
case "$EXT" in
  png|jpg|jpeg|webp|gif|svg|bmp|avif) KIND=img ;;
  mp4|mov|webm) KIND=vid ;;
  *) die "不支持的类型: $EXT" ;;
esac
MAX=$([ "$KIND" = vid ] && echo "$VID_MAX" || echo "$IMG_MAX")

case "$NAME" in og|og-*|og_*) KEEP_FORMAT=1 ;; esac  # og 社交卡：部分抓取器不认 WebP/AVIF

has_alpha() {
  if command -v sips >/dev/null 2>&1; then
    [ "$(sips -g hasAlpha "$1" 2>/dev/null | awk '/hasAlpha/{print tolower($2)}')" = yes ]
  else
    file -b "$1" | grep -qiE 'alpha|rgba'
  fi
}
bytes() { wc -c < "$1" | tr -d ' '; }

# 尝试 WebP：无损(有alpha)/有损+图形锐化(无alpha)，不更小则放弃
convert_webp() {
  command -v cwebp >/dev/null 2>&1 || { note "未安装 cwebp（brew install webp），跳过压缩"; return 1; }
  if has_alpha "$CUR"; then
    FLAVOR=(-lossless -z 9 -mt); note "检测到透明通道 → 无损 WebP（alpha 逐位保留）"
  else
    FLAVOR=(-q "$WEBP_Q" -mt -sharp_yuv); note "不透明图 → 有损 WebP q${WEBP_Q}（-mt -sharp_yuv 图形锐化）"
  fi
  if cwebp "${FLAVOR[@]}" "$CUR" -o "$WORK/$NAME.webp" 2>/dev/null &&
     [ "$(bytes "$WORK/$NAME.webp")" -lt "$(bytes "$CUR")" ]; then
    CUR="$WORK/$NAME.webp"; EXT=webp
  else
    note "WebP 未更小，保留原格式"
  fi
}

# 尝试 AVIF：比 WebP 再小 ~20-30%，全现代浏览器支持
convert_avif() {
  if ! command -v avifenc >/dev/null 2>&1; then
    note "未安装 avifenc（brew install libavif），回退 WebP"; convert_webp; return
  fi
  if has_alpha "$CUR"; then
    AFLAGS=(--lossless -j all); note "透明图 → 无损 AVIF（alpha 保留）"
  else
    AFLAGS=(-q "$AVIF_Q" -j all); note "不透明图 → 有损 AVIF q$AVIF_Q"
  fi
  if avifenc "${AFLAGS[@]}" "$CUR" "$WORK/$NAME.avif" >/dev/null 2>&1 &&
     [ "$(bytes "$WORK/$NAME.avif")" -lt "$(bytes "$CUR")" ]; then
    CUR="$WORK/$NAME.avif"; EXT=avif
  else
    note "AVIF 未更小或编码失败，保留原格式"
  fi
}

mkdir -p "$DEST_DIR"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
cp "$SRC" "$WORK/$BASE"
CUR="$WORK/$BASE"

if [ "$KIND" = img ]; then
  if command -v sips >/dev/null 2>&1; then
    read -r W H <<<"$(sips -g pixelWidth -g pixelHeight "$CUR" 2>/dev/null | awk '/pixel/{print $2}' | tr '\n' ' ')"
    if [ "${W:-0}" -gt "$MAX_SIDE" ] || [ "${H:-0}" -gt "$MAX_SIDE" ]; then
      sips -Z "$MAX_SIDE" "$CUR" >/dev/null
      note "长边 ${W}x${H} 超过 ${MAX_SIDE}px，已等比缩小"
    fi
  fi

  case "$EXT" in
    png|jpg|jpeg)
      if [ "$(bytes "$CUR")" -le "$CONVERT_THRESHOLD" ]; then
        note "小于 100KB，跳过压缩"
      elif [ "$KEEP_FORMAT" = 1 ]; then
        if command -v oxipng >/dev/null 2>&1; then
          oxipng -q -o 2 "$CUR" && note "oxipng 无损优化完成"
        elif command -v optipng >/dev/null 2>&1; then
          optipng -quiet -o2 "$CUR" && note "optipng 无损优化完成"
        elif command -v pngquant >/dev/null 2>&1 && [ "$EXT" = png ]; then
          pngquant --force --output "$CUR" --speed 1 "$CUR" 2>/dev/null && note "pngquant 量化完成（有损调色板法，alpha 保留）"
        else
          note "保原格式优化需任一: brew install oxipng / optipng / pngquant（未安装，跳过）"
        fi
      elif [ "$USE_AVIF" = 1 ]; then
        convert_avif
      else
        convert_webp
      fi ;;
  esac
fi

SIZE=$(bytes "$CUR")
[ "$SIZE" -le "$MAX" ] || die "处理后 $(($SIZE / 1024 / 1024))MB 超过 $((MAX / 1024 / 1024))MB 红线。原图放 U 盘(AI素材资源)或 R2，不进本仓。"

DEST="$DEST_DIR/$NAME.$EXT"
[ -e "$DEST" ] && die "目标已存在: ${DEST}（外链绑死路径，禁止覆盖）"
mv "$CUR" "$DEST"
echo "✓ $DEST  ($(( SIZE / 1024 ))KB)"

BASE_URL="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main"
echo "  $BASE_URL/$DEST"
tools/index.sh >/dev/null 2>&1 || true
echo "下一步: git add \"$DEST\" INDEX.md && git commit -m 'upload: $DEST' && git push"
