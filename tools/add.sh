#!/usr/bin/env bash
# 统一压缩上传入口：tools/add.sh <图片> [目标目录]
# 红线见 README「红线」：单文件 ≤ 2MB，先压缩后进仓，已存在同名即拒绝（外链绑死路径）。
set -euo pipefail

MAX_FINAL_BYTES=$((2 * 1024 * 1024))
CONVERT_THRESHOLD=$((100 * 1024))
MAX_SIDE=2560
WEBP_Q=80

die() { echo "✗ $*" >&2; exit 1; }

[ $# -ge 1 ] || die "用法: tools/add.sh <图片> [目标目录]（默认 temp/YYYY-MM/）"
SRC=$1
DEST_DIR=${2:-"temp/$(date +%Y-%m)"}
[ -f "$SRC" ] || die "文件不存在: $SRC"

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || die "请在仓库内运行"
cd "$REPO_ROOT"

case "${SRC##*.}" in
  png|jpg|jpeg|webp|gif|svg|mp4|mov) ;;
  *) die "不支持的类型: ${SRC##*.}" ;;
esac

mkdir -p "$DEST_DIR"
BASE=${SRC##*/}
NAME="${BASE%.*}"
EXT="${BASE##*.}"
[ -e "$DEST_DIR/$BASE" ] && die "目标已存在: $DEST_DIR/$BASE（外链绑死路径，禁止覆盖）"

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
cp "$SRC" "$WORK/$BASE"

# 长边超限先等比缩小
if command -v sips >/dev/null; then
  read -r W H <<<"$(sips -g pixelWidth -g pixelHeight "$WORK/$BASE" 2>/dev/null | awk '/pixel/{print $2}' | tr '\n' ' ')"
  if [ "${W:-0}" -gt "$MAX_SIDE" ] || [ "${H:-0}" -gt "$MAX_SIDE" ]; then
    sips -Z "$MAX_SIDE" "$WORK/$BASE" >/dev/null
    echo "↳ 长边 ${W}x${H} 超过 ${MAX_SIDE}px，已等比缩小"
  fi
fi

# >100KB 的 png/jpg 转 WebP，转换后不更小则放弃转换
CUR="$WORK/$BASE"
if [ "$EXT" != "webp" ] && [ "$EXT" != "svg" ] && [ "$(stat -f%z "$CUR")" -gt "$CONVERT_THRESHOLD" ]; then
  if command -v cwebp >/dev/null; then
    cwebp -quiet -q "$WEBP_Q" "$CUR" -o "$WORK/$NAME.webp" && \
      [ "$(stat -f%z "$WORK/$NAME.webp")" -lt "$(stat -f%z "$CUR")" ] && \
      { CUR="$WORK/$NAME.webp"; EXT=webp; echo "↳ 已转 WebP (q$WEBP_Q)"; } || echo "↳ WebP 未更小，保留原格式"
  else
    echo "⚠ 未安装 cwebp（brew install webp），跳过压缩" >&2
  fi
fi

SIZE=$(stat -f%z "$CUR")
[ "$SIZE" -le "$MAX_FINAL_BYTES" ] || die "压缩后仍 $(($SIZE / 1024))KB > 2MB 上限。大图请放 U 盘(AI素材资源)或 R2，不进本仓。"

DEST="$DEST_DIR/$NAME.$EXT"
mv "$CUR" "$DEST"
echo "✓ $DEST  ($(( SIZE / 1024 ))KB)"

BASE_URL="https://cdn.jsdelivr.net/gh/webkubor/picx-images-hosting@master"
echo "  $BASE_URL/$DEST"
[ -x tools/index.sh ] && tools/index.sh >/dev/null && echo "↳ INDEX.md 已重生成"
echo "下一步: git add \"$DEST\" INDEX.md && git commit -m 'upload: $DEST' && git push"
