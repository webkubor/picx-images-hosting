#!/usr/bin/env bash
# 重生成 INDEX.md：按顶层目录统计图片数（tools/index.sh）
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

EXTS='png|jpg|jpeg|webp|gif|svg|bmp|mp4|mov'
tmp=$(mktemp)
total=0; dirs=0
for d in */; do
  n=$(find "$d" -type f -not -path '*/node_modules/*' | grep -icE "\.($EXTS)$" || true)
  if [ "$n" -gt 0 ]; then
    echo "- [${d%/}/](${d%/}/) — $n images"
    total=$((total + n)); dirs=$((dirs + 1))
  fi
done > "$tmp.raw"
sort "$tmp.raw" > "$tmp.list"
rm -f "$tmp.raw"

{
  echo "# Image Index"
  echo
  echo "> 快照: $(date -u '+%Y-%m-%d %H:%M UTC') ｜ $dirs directories, $total images ｜ 由 tools/index.sh 生成，勿手工编辑"
  echo
  cat "$tmp.list"
} > "$tmp"
mv "$tmp" INDEX.md
rm -f "$tmp.list"
echo "✓ INDEX.md 已重生成（$dirs 个目录 / $total 张图）"
