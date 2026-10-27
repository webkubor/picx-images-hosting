#!/usr/bin/env bash
# 批量迁移：把某仓库 README 里的「本地相对路径素材」上传到图床，并把引用改成 CDN 直链。
#
#   tools/migrate-assets.sh <项目仓库目录> [--dir <图床目标子目录>] [--apply]
#
# 默认 dry-run（只打印将要发生什么）；加 --apply 才真正上传 + 改写 README。
# 策略：
#   - 扫描 README*.md 里的 ![](相对路径) 与 <img src="相对路径"> / srcset
#   - 跳过徽章（shields.io / badge）与外部绝对 URL
#   - 素材上传到图床 <图床目标子目录>/<原文件名>，压缩由 tools/add.sh 负责
#   - 引用改写为 https://cdn.jsdelivr.net/gh/<图床仓>@<分支>/<路径>
#   - README 里的本地文件保留（不删），只改引用 —— 回滚成本低
set -euo pipefail

REPO_DIR=${1:-.}
APPLY=0; TARGET_DIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dir) TARGET_DIR=$2; shift 2 ;;
    --apply) APPLY=1; shift ;;
    *) shift ;;
  esac
done
[ -d "$REPO_DIR" ] || { echo "✗ 目录不存在: $REPO_DIR" >&2; exit 1; }
cd "$REPO_DIR"

IMG_BED_REPO=${IMG_BED_REPO:-/Users/webkubor/dev/ops/picx-images-hosting}
IMG_BED_BRANCH=${IMG_BED_BRANCH:-main}
IMG_BED_GH=${IMG_BED_GH:-webkubor/free-imgbed}
[ -d "$IMG_BED_REPO" ] || { echo "✗ 找不到图床仓库: ${IMG_BED_REPO}（用 IMG_BED_REPO= 指定）" >&2; exit 1; }
TARGET_DIR=${TARGET_DIR:-$(basename "$REPO_DIR")}
BASE_URL="https://cdn.jsdelivr.net/gh/$IMG_BED_GH@$IMG_BED_BRANCH"

# 收集 README 里的相对路径素材引用
REFS=()
while IFS= read -r _r; do REFS+=("$_r"); done < <(
  grep -rhoE --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.vitepress \
    --exclude-dir=target --exclude-dir=.git --exclude-dir=build --exclude-dir=out '(!\[[^]]*\]\(|src="|srcset=")[^")> ]+\.(png|jpe?g|webp|gif|svg|bmp|mp4|mov|webm|avif)' \
    --include='README*.md' . 2>/dev/null \
  | sed -E 's/^(!\[[^]]*\]\(|src="|srcset=")//' \
  | sed -E 's#^\./##' | sed -E 's#^\.github/#docs/.github/#' | sort -u
)

[ ${#REFS[@]} -eq 0 ] && { echo "↳ 没有相对路径素材引用"; exit 0; }
echo "发现 ${#REFS[@]} 个相对路径素材引用（目标目录: ${TARGET_DIR}）"

UPLOADED=0; SKIPPED=0
for rel in "${REFS[@]}"; do
  case "$rel" in
    http*|//*|data:*|mailto:*) SKIPPED=$((SKIPPED+1)); continue ;;
  esac
  SRC=""
  for cand in "$rel" "docs/$rel" "docs/public/$rel" "$(dirname "$0")/../../$rel"; do
    [ -f "$cand" ] && { SRC="$cand"; break; }
  done
  if [ -z "$SRC" ]; then
    printf "  ⚠ 找不到文件，跳过: %s\n" "$rel"; SKIPPED=$((SKIPPED+1)); continue
  fi
  NEWREL="$TARGET_DIR/$(basename "$rel")"
  printf "  → %s  ⇒  %s\n" "$rel" "$NEWREL"
  if [ "$APPLY" = 1 ]; then
    ABS_SRC=$(cd "$(dirname "$SRC")" && pwd -P)/$(basename "$SRC")
    ( cd "$IMG_BED_REPO" && tools/add.sh "$ABS_SRC" "$TARGET_DIR" >/dev/null )
    UPLOADED=$((UPLOADED+1))
  fi
done

if [ "$APPLY" = 1 ]; then
  echo "已上传 $UPLOADED 个（跳过 $SKIPPED 个）"
  # 自动改写 README 引用：相对路径 → CDN 直链
  python3 - "$TARGET_DIR" "$BASE_URL" "$IMG_BED_REPO" <<'PY'
import os, re, sys, glob
target, base, bed = sys.argv[1], sys.argv[2], sys.argv[3]
exts = r'(?:png|jpe?g|webp|gif|svg|bmp|mp4|mov|webm|avif)'
changed = []
for f in glob.glob('README*.md') + glob.glob('docs/README*.md'):
    if not os.path.isfile(f): continue
    s = open(f).read(); orig = s
    def repl(m):
        pre, path = m.group(1), m.group(2)
        if path.startswith(('http', '//', 'data:')): return m.group(0)
        # 图床侧实际文件名（png 可能被压成 webp）
        stem = os.path.splitext(os.path.basename(path))[0]
        for ext in ('webp', 'png', 'jpg', 'jpeg', 'svg', 'gif', 'avif', 'mp4'):
            if os.path.isfile(os.path.join(bed, target, f'{stem}.{ext}')):
                return f'{pre}{base}/{target}/{stem}.{ext}'
        return m.group(0)
    s = re.sub(r'(!\[[^\]]*\]\(|src="|srcset=")([^")> ]+\.' + exts + ')', repl, s)
    if s != orig:
        open(f, 'w').write(s); changed.append(f)
for c in changed: print('  ✓ 已改写引用:', c)
if not changed: print('  （无 README 需改写）')
PY
else
  echo "（dry-run，加 --apply 实际上传并改写引用）"
fi
