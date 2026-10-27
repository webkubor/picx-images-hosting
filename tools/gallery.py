#!/usr/bin/env python3
"""Generate one gallery block for README and VitePress. Standard library only."""
import argparse
import html
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/'
START = '<!-- logo-gallery:start -->'
END = '<!-- logo-gallery:end -->'
SKIP = {'docs', 'tools', 'web', 'blog', 'temp', 'node_modules', 'design', 'brand'}
TARGETS = ('README.md', 'docs/guide/logo-gallery.md')
spec = importlib.util.spec_from_file_location('check_brand', ROOT / 'tools/check-brand.py')
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


def entries():
    manifests = {m['id']: m for m in contract.load_manifests()}
    result = []
    for directory in sorted(ROOT.iterdir()):
        if not directory.is_dir() or directory.name.startswith('.') or directory.name in SKIP:
            continue
        id_ = directory.name
        if id_ in manifests:
            m = manifests[id_]
            result.append((id_, m['asset'], m['darkAsset']))
            continue
        # Legacy directories without a manifest retain their URLs and naming order.
        asset = next((directory / name for name in ('logo-v2.svg', 'logo.svg', 'logo.png',
                     'logo.webp', 'icon.svg', 'logo-icon.webp', 'logo-icon.png')
                      if (directory / name).is_file()), None)
        if asset:
            dark = directory / 'logo-dark.svg'
            result.append((id_, asset.relative_to(ROOT).as_posix(),
                           dark.relative_to(ROOT).as_posix() if dark.is_file() else None))
    missing = set(manifests) - {row[0] for row in result}
    if missing:
        raise ValueError('manifest project directories excluded or missing: ' + ', '.join(sorted(missing)))
    return result


def build(site_theme=False):
    behavior = ('文档随站内主题开关显示对应 `darkAsset`（以根元素 `.dark` 为准）'
                if site_theme else '深色主题用 `<picture>` 按系统偏好加载对应 `darkAsset`')
    lines = [START, '', '## 🖼 项目 logo 墙', '',
             f'优先展示 `brand/*.json` 指定的新符号；{behavior}。旧素材 URL 继续保留。', '']
    if site_theme:
        lines.extend(['<style>',
                      '.brand-gallery-dark { display: none !important; }',
                      '.dark .brand-gallery-light { display: none !important; }',
                      '.dark .brand-gallery-dark { display: inline-block !important; }',
                      '</style>', ''])
    lines.extend(['| 项目 | 标识 | 文件 |', '|---|---|---|'])
    for id_, asset, dark in entries():
        image = f'<img src="{BASE}{html.escape(asset)}" width="120" height="120" alt="{html.escape(id_)} logo">'
        if dark:
            if site_theme:
                image = image.replace('<img ', '<img class="brand-gallery-light" ', 1)
                image += f'<img class="brand-gallery-dark" src="{BASE}{html.escape(dark)}" width="120" height="120" alt="{html.escape(id_)} logo">'
            else:
                image = f'<picture><source media="(prefers-color-scheme: dark)" srcset="{BASE}{html.escape(dark)}">{image}</picture>'
        lines.append(f'| {id_} | {image} | `{asset}` |')
    lines.extend(['', END])
    return '\n'.join(lines)


def replace_block(text, block):
    if START not in text and END not in text:
        return text.rstrip() + '\n\n' + block + '\n'
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('gallery markers must appear exactly once')
    before, rest = text.split(START)
    _, after = rest.split(END)
    return before + block + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name in TARGETS:
        block = build(site_theme=name.startswith('docs/'))
        path = ROOT / name
        current = path.read_text(encoding='utf-8')
        updated = replace_block(current, block)
        if args.check:
            if START not in current or updated != current:
                stale.append(name)
        elif updated != current:
            path.write_text(updated, encoding='utf-8')
    if stale:
        print('FAIL gallery stale: ' + ', '.join(stale) + '; run tools/gallery.sh')
        return 1
    print(('PASS gallery freshness' if args.check else 'PASS gallery generated')
          + ': README.md + docs/guide/logo-gallery.md; ' + str(len(entries())) + ' projects')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
