#!/usr/bin/env bash
# 重生成 INDEX.md：目录内容无变化时不动文件（幂等，供 CI 判新鲜度）
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

EXTS='avif|png|jpg|jpeg|webp|gif|svg|bmp|mp4|mov|webm'
tmp=$(mktemp); trap 'rm -f "$tmp.body" "$tmp.out"' EXIT
total=0; dirs=0
for d in */; do
  n=$(find "$d" -type f -not -path '*/node_modules/*' | grep -icE "\.($EXTS)$" || true)
  if [ "$n" -gt 0 ]; then
    echo "- [${d%/}/](${d%/}/) — $n images"
    total=$((total + n)); dirs=$((dirs + 1))
  fi
done > "$tmp.body"
sort -o "$tmp.body" "$tmp.body"

if [ -f INDEX.md ] && diff -q <(grep '^- ' INDEX.md || true) "$tmp.body" >/dev/null 2>&1; then
  echo "✓ INDEX.md 内容无变化，跳过"
  exit 0
fi
{
  echo "# Image Index"
  echo
  echo "> 快照: $(date -u '+%Y-%m-%d %H:%M UTC') ｜ $dirs directories, $total images ｜ 由 tools/index.sh 生成，勿手工编辑"
  echo
  cat "$tmp.body"
} > "$tmp.out"
mv "$tmp.out" INDEX.md
echo "✓ INDEX.md 已重生成（$dirs 个目录 / $total 张图）"
