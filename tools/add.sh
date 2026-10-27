#!/usr/bin/env bash
# 统一压缩上传入口：tools/add.sh <图片|视频> [目标目录]
# 红线：图片 ≤ 2MB、视频 ≤ 10MB；先压缩后进仓；同名即拒绝（外链绑死路径）。
# 推广素材建议落 <项目名>/，命名 logo.* banner.* og.* demo.gif + demo.mp4 shot-*.png
set -euo pipefail

IMG_MAX=$((2 * 1024 * 1024))
VID_MAX=$((10 * 1024 * 1024))
CONVERT_THRESHOLD=$((100 * 1024))
MAX_SIDE=2560
WEBP_Q=80

die() { echo "✗ $*" >&2; exit 1; }

[ $# -ge 1 ] || die "用法: tools/add.sh <图片|视频> [目标目录]（默认 temp/YYYY-MM/，推广素材建议 <项目名>/）"
SRC=$1
DEST_DIR=${2:-"temp/$(date +%Y-%m)"}
[ -f "$SRC" ] || die "文件不存在: $SRC"

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || die "请在仓库内运行"
cd "$REPO_ROOT"

BASE=${SRC##*/}
NAME="${BASE%.*}"; EXT="${BASE##*.}"
case "$EXT" in
  png|jpg|jpeg|webp|gif|svg|bmp) KIND=img ;;
  mp4|mov|webm) KIND=vid ;;
  *) die "不支持的类型: $EXT" ;;
esac
MAX=$([ "$KIND" = vid ] && echo "$VID_MAX" || echo "$IMG_MAX")

mkdir -p "$DEST_DIR"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
cp "$SRC" "$WORK/$BASE"
CUR="$WORK/$BASE"

# 图片：长边超限先等比缩小；>100KB 的 png/jpg 转 WebP，不更小则放弃
if [ "$KIND" = img ]; then
  if command -v sips >/dev/null; then
    read -r W H <<<"$(sips -g pixelWidth -g pixelHeight "$CUR" 2>/dev/null | awk '/pixel/{print $2}' | tr '\n' ' ')"
    if [ "${W:-0}" -gt "$MAX_SIDE" ] || [ "${H:-0}" -gt "$MAX_SIDE" ]; then
      sips -Z "$MAX_SIDE" "$CUR" >/dev/null
      echo "↳ 长边 ${W}x${H} 超过 ${MAX_SIDE}px，已等比缩小"
    fi
  fi
  case "$EXT" in
    png|jpg|jpeg)
      if [ "$(wc -c < "$CUR" | tr -d ' ')" -gt "$CONVERT_THRESHOLD" ]; then
        if command -v cwebp >/dev/null; then
          cwebp -quiet -q "$WEBP_Q" "$CUR" -o "$WORK/$NAME.webp" && \
            [ "$(wc -c < "$WORK/$NAME.webp" | tr -d ' ')" -lt "$(wc -c < "$CUR" | tr -d ' ')" ] && \
            { CUR="$WORK/$NAME.webp"; EXT=webp; echo "↳ 已转 WebP (q$WEBP_Q)"; } || echo "↳ WebP 未更小，保留原格式"
        else
          echo "⚠ 未安装 cwebp（brew install webp），跳过压缩" >&2
        fi
      fi ;;
  esac
fi

SIZE=$(wc -c < "$CUR" | tr -d ' ')
[ "$SIZE" -le "$MAX" ] || die "处理后 $(($SIZE / 1024 / 1024))MB 超过 $((MAX / 1024 / 1024))MB 红线。原图放 U 盘(AI素材资源)或 R2，不进本仓。"

DEST="$DEST_DIR/$NAME.$EXT"
[ -e "$DEST" ] && die "目标已存在: $DEST（外链绑死路径，禁止覆盖）"
mv "$CUR" "$DEST"
echo "✓ $DEST  ($(( SIZE / 1024 ))KB)"

BASE_URL="https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master"
echo "  $BASE_URL/$DEST"
tools/index.sh >/dev/null 2>&1 || true
echo "下一步: git add \"$DEST\" INDEX.md && git commit -m 'upload: $DEST' && git push"
