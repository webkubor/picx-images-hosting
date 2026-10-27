#!/usr/bin/env bash
# 生成 README 里的「项目 logo 墙」：仓库里每个项目的标识直接以图片形式内嵌。
# 用法: tools/gallery.sh [--check]
#   --check  只校验 README 中的图床区与实际资产是否一致（不一致返回 1），供 CI 使用
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

README_FILE=README.md
START='<!-- logo-gallery:start -->'
END='<!-- logo-gallery:end -->'
BASE="https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main"
SKIP_DIRS='docs tools web blog temp .git node_modules'

# 规范标识覆盖：某些目录的主标识不是按通用规则选出的
declare -A OVERRIDE=(
  [scorecard]="scorecard/logo-v2.svg"   # logo.svg 是过渡版本，正式标识为 v2
)

pick() {
  local d=$1
  if [ -n "${OVERRIDE[$d]:-}" ] && [ -f "${OVERRIDE[$d]}" ]; then
    echo "${OVERRIDE[$d]}"; return 0
  fi
  for c in logo.svg logo-v2.svg logo.png logo.webp icon.svg logo-icon.webp logo-icon.png; do
    [ -f "$d/$c" ] && { echo "$d/$c"; return 0; }
  done
  return 1
}

build() {
  echo "$START"
  echo
  echo "## 🖼 项目 logo 墙"
  echo
  echo "仓库里各项目的标识，按项目归档；深浅两版用 \`<picture>\` 按系统主题自动切换。"
  echo
  echo "| 项目 | 标识 | 文件 |"
  echo "|---|---|---|"
  for d in */; do
    d=${d%/}
    case " $SKIP_DIRS " in *" $d "*) continue ;; esac
    main=$(pick "$d") || continue
    if [ -f "$d/logo-dark.svg" ]; then
      cell="<picture><source media=\"(prefers-color-scheme: dark)\" srcset=\"$BASE/$d/logo-dark.svg\"><img src=\"$BASE/$main\" width=\"120\" alt=\"$d logo\"></picture>"
    else
      cell="<img src=\"$BASE/$main\" width=\"120\" alt=\"$d logo\">"
    fi
    printf '| %s | %s | `%s` |\n' "$d" "$cell" "$main"
  done
  echo
  echo "$END"
}

BODY=$(build | grep -E '^\| ' | grep -v '^| 项目 ' | grep -v '^|---' || true)

if [ "${1:-}" = "--check" ]; then
  CURRENT=$(sed -n "/$START/,/$END/p" "$README_FILE" | grep -E '^\| ' | grep -v '^| 项目 ' | grep -v '^|---' || true)
  if [ "$CURRENT" = "$BODY" ]; then
    echo "✓ README logo 墙与仓库资产一致"
    exit 0
  fi
  echo "✗ README logo 墙已过期，运行 tools/gallery.sh 后一并提交" >&2
  exit 1
fi

GEN=$(mktemp); OUT=$(mktemp); trap 'rm -f "$GEN" "$OUT"' EXIT
build > "$GEN"
if grep -qF "$START" "$README_FILE"; then
  awk -v s="$START" -v e="$END" -v f="$GEN" '
    $0 == s { while ((getline line < f) > 0) print line; skip = 1; next }
    $0 == e { skip = 0; next }
    !skip { print }
  ' "$README_FILE" > "$OUT"
else
  { cat "$README_FILE"; echo; cat "$GEN"; } > "$OUT"
fi
mv "$OUT" "$README_FILE"
echo "✓ README logo 墙已更新"
