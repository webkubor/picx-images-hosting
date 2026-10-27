#!/usr/bin/env bash
# 素材合规检查，本地与 CI 同一套（tools/check.sh）：
#   1) 尺寸红线：图片 ≤ 2MB，视频 ≤ 10MB（jsDelivr 上限 20MB，留余量）
#   2) 重复检测：全仓 MD5 相同的文件即失败（防 brand/concert 式互相拷贝复发）
#   3) INDEX 新鲜度：与实际目录比对，过期即失败
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

IMG_MAX=$((2 * 1024 * 1024))
VID_MAX=$((10 * 1024 * 1024))
EXTS='avif|png|jpg|jpeg|webp|gif|svg|bmp|mp4|mov|webm'
VID_RE='\.(mp4|mov|webm)$'

if command -v md5sum >/dev/null 2>&1; then hash() { md5sum "$1" | cut -d' ' -f1; }
else hash() { md5 -q "$1"; }; fi
size() { wc -c < "$1" | tr -d ' '; }

fail=0
tmp=$(mktemp); trap 'rm -f "$tmp"' EXIT

echo "== 尺寸红线 =="
n_assets=0
while IFS= read -r f; do
  n_assets=$((n_assets + 1))
  sz=$(size "$f")
  if echo "$f" | grep -iqE "$VID_RE"; then max=$VID_MAX; label=视频; else max=$IMG_MAX; label=图片; fi
  if [ "$sz" -gt "$max" ]; then
    echo "✗ $f — $label $(($sz / 1024 / 1024))MB 超过 $((max / 1024 / 1024))MB 红线（tools/add.sh 压缩，或转存 U 盘/R2）"
    fail=1
  fi
done < <(find . -type f -not -path './.git/*' -not -path '*/node_modules/*' | grep -iE "\.($EXTS)$")
echo "  $n_assets 个素材通过尺寸检查"

echo "== 重复检测 =="
n_dup=0
while IFS= read -r f; do
  printf '%s\t%s\n' "$(hash "$f")" "$f" >> "$tmp"
done < <(find . -type f -not -path './.git/*' -not -path '*/node_modules/*' | grep -iE "\.($EXTS)$")
while IFS= read -r line; do
  echo "✗ $line 内容重复"
  n_dup=$((n_dup + 1)); fail=1
done < <(sort "$tmp" | awk -F'\t' 'seen[$1]++ { print $2 }')
[ "$n_dup" -eq 0 ] && echo "  无重复文件"

echo "== INDEX 新鲜度 =="
# 记录重生成前的内容指纹，跑完 index.sh 再比：变了说明索引原本过期
BEFORE=$(grep '^- ' INDEX.md 2>/dev/null | md5sum | cut -d' ' -f1 || echo none)
tools/index.sh >/dev/null
AFTER=$(grep '^- ' INDEX.md 2>/dev/null | md5sum | cut -d' ' -f1 || echo none)
if [ "$BEFORE" = "$AFTER" ]; then
  echo "  INDEX.md 与目录一致"
else
  echo "✗ INDEX.md 落后于实际目录，已自动重生成 —— 请把 INDEX.md 一并提交"
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "✗ 检查未通过" >&2
  exit 1
fi
echo "✓ 全部通过"
