#!/usr/bin/env python3
"""Generate design review/brief HTML from manifests; copy outputs for VitePress.

python3 tools/brand-ui.py             # regenerate canonical design/*.html
python3 tools/brand-ui.py --publish   # regenerate + copy to docs/public/design/
python3 tools/brand-ui.py --check     # compare both HTML sources, no mutation
HTML is self-contained: preview bytes are derived from repository assets.
"""
import argparse
import base64
import html
import importlib.util
import json
import mimetypes
import re
import shutil
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_brand", ROOT / "tools/check-brand.py")
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
E = html.escape

CSS = """
:root{color-scheme:light;--paper:#f5f4f0;--card:#fff;--ink:#20252b;--dim:#55606b;--line:#d7dcd9;--accent:#185d51;--soft:#e7eee9}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}a{color:var(--accent);text-underline-offset:3px}button,select{font:inherit}button,select,summary{cursor:pointer}button:focus-visible,a:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #047857;outline-offset:4px}header,main,footer{max-width:1440px;margin:auto;padding:24px clamp(16px,4vw,56px)}header{padding-top:48px;padding-bottom:12px}nav{display:flex;flex-wrap:wrap;gap:20px}h1{font-size:clamp(28px,4vw,48px);line-height:1.2;letter-spacing:-.03em;margin:24px 0 14px}h2{font-size:20px;line-height:1.3;margin:0}h3{font-size:15px;margin:12px 0 4px}p{margin:8px 0 14px}.eyebrow{font:12px/1.4 ui-monospace,monospace;color:var(--accent);letter-spacing:.12em}.lede{max-width:900px;color:var(--dim);font-size:16px}.toolbar{position:sticky;top:0;z-index:2;background:var(--paper);border-block:1px solid var(--line);padding:12px 0;display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:24px}fieldset{display:flex;gap:8px;border:0;margin:0;padding:0;flex-wrap:wrap}legend{float:left;margin-right:12px;font-weight:600}fieldset label,select{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:6px 10px}fieldset label:has(input:checked){border-color:var(--accent);background:var(--soft)}input{accent-color:var(--accent)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:24px}.card{min-width:0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px}.card-head{display:flex;justify-content:space-between;gap:12px;align-items:start}.tag{font-size:12px;white-space:nowrap;padding:3px 9px;border:1px solid var(--line);border-radius:20px;color:var(--dim)}.meta{font-size:13px;color:var(--dim);margin:8px 0 16px;overflow-wrap:anywhere}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0}.preview{min-width:0}.preview figcaption{font-size:12px;color:var(--dim);padding:6px 0}.preview{margin:0}.stage{height:176px;display:flex;align-items:center;justify-content:center;border:1px solid #c7cdc9;border-radius:8px;overflow:hidden;background:#fff}.stage img{width:var(--size,64px);height:var(--size,64px);object-fit:contain}.stage[data-bg=dark]{background:#0d1117;border-color:#30363d}.stage[data-bg=checkerboard]{background-color:#fff;background-image:linear-gradient(45deg,#d1d5db 25%,transparent 25%),linear-gradient(-45deg,#d1d5db 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d1d5db 75%),linear-gradient(-45deg,transparent 75%,#d1d5db 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}.palette{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.swatch{display:flex;align-items:center;gap:7px;border:1px solid var(--line);padding:4px 7px;border-radius:5px;font-size:12px}.chip{width:16px;height:16px;border-radius:3px;border:1px solid #8b949e}code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}code{font-size:.9em}pre{font-size:12px;line-height:1.7;background:#f5f6f4;border:1px solid var(--line);padding:16px;border-radius:6px;white-space:pre-wrap;overflow-wrap:anywhere;max-height:420px;overflow:auto}.manual-copy{display:block;width:100%;margin-top:12px;padding:14px;font:12px/1.65 ui-monospace,monospace;border:2px solid var(--accent);border-radius:6px;resize:vertical}.rationale{font-size:14px}.sources{font-size:13px;display:flex;flex-wrap:wrap;gap:8px 16px;overflow-wrap:anywhere}.copy-row{display:flex;align-items:center;gap:12px;margin-top:18px;flex-wrap:wrap}.copy{background:var(--accent);color:#fff;border:1px solid var(--accent);padding:9px 14px;border-radius:6px;font-weight:600}.copy:disabled{opacity:.65;cursor:wait}.status{color:var(--accent);font-size:13px;min-height:22px}.notice{background:var(--soft);border-left:3px solid var(--accent);padding:14px 18px;margin:16px 0}.excluded{margin-top:28px}details{margin-top:14px}summary{color:var(--accent);font-size:13px}footer{font-size:13px;color:var(--dim);border-top:1px solid var(--line)}.skip{position:absolute;top:-80px;left:16px;background:white;padding:8px;z-index:5}.skip:focus{top:8px}@media(max-width:600px){.card{padding:16px}.stage{height:156px}.toolbar{position:static}.card-head{display:block}.tag{display:inline-block;margin-top:8px}}
"""
SCRIPT = """
// Each button owns its busy state, live region and fallback selection.
document.querySelectorAll('.copy').forEach(button => {
  button.addEventListener('click', async () => {
    if (button.disabled) return;
    const box = document.getElementById(button.dataset.target);
    const status = document.getElementById(button.dataset.status);
    button.disabled = true; button.setAttribute('aria-busy', 'true');
    status.textContent = '正在复制…';
    let ok = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(box.textContent); ok = true;
      }
    } catch (_) { /* Permission failure uses selection-based fallback. */ }
    if (!ok) {
      const area = document.createElement('textarea');
      area.value = box.textContent; area.readOnly = true;
      area.setAttribute('aria-label', '临时复制文本');
      area.style.cssText = 'position:fixed;left:0;top:0;opacity:0';
      document.body.appendChild(area); area.select();
      area.setSelectionRange(0, area.value.length);
      try { ok = document.execCommand('copy'); } catch (_) { ok = false; }
      area.remove(); button.focus();
    }
    if (ok) {
      status.textContent = '已复制完整任务 ✓'; button.textContent = '再次复制';
    } else {
      const details = box.closest('details'); details.open = true;
      let manual = details.querySelector('.manual-copy');
      if (!manual) {
        manual = document.createElement('textarea');
        manual.className = 'manual-copy'; manual.readOnly = true; manual.rows = 12;
        manual.setAttribute('aria-label', button.getAttribute('aria-label').replace('复制 ', '') + '，手动复制文本');
        details.appendChild(manual);
      }
      manual.value = box.textContent; manual.focus(); manual.select();
      manual.setSelectionRange(0, manual.value.length);
      status.textContent = '自动复制不可用，任务已选中，请按 Cmd/Ctrl+C';
      button.textContent = '重试复制';
    }
    button.disabled = false; button.removeAttribute('aria-busy');
  });
});
const sizeControl = document.getElementById('size');
if (sizeControl) sizeControl.addEventListener('change', () => {
  document.documentElement.style.setProperty('--size', sizeControl.value + 'px');
  document.getElementById('preview-status').textContent = '预览尺寸 ' + sizeControl.value + ' × ' + sizeControl.value + ' px';
});
document.querySelectorAll('input[name=background]').forEach(input => {
  input.addEventListener('change', () => {
    const dark = input.value === 'dark';
    document.querySelectorAll('.stage').forEach(stage => stage.dataset.bg = input.value);
    document.querySelectorAll('img[data-light]').forEach(img => {
      img.src = dark ? img.dataset.dark : img.dataset.light;
      img.alt = img.dataset.name + (dark ? '，深底版本' : '，浅底版本');
    });
    document.getElementById('preview-status').textContent = input.value === 'checkerboard'
      ? '棋盘背景使用浅底版；透明区域应透出棋盘' : (dark ? '深背景，已加载深底版本' : '浅背景，已加载浅底版本');
  });
});
"""


def image_data(asset):
    path = ROOT / asset
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def download_link(asset, label=None):
    """Download the same local bytes as the preview, without requiring a release."""
    return (f'<a href="{image_data(asset)}" download="{E(Path(asset).name)}">'
            f'{E(label or asset)}</a>')


def load_briefs():
    data = json.loads((ROOT / 'design/briefs.json').read_text())
    seen = set()
    for project in data['projects']:
        id_ = project['id']
        contract.require(isinstance(id_, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', id_),
                         f'invalid brief manifest id: {id_}')
        contract.require(id_ not in seen, f'duplicate brief manifest id: {id_}')
        seen.add(id_)
        repo = urlsplit(project['repo'])
        if id_ == 'typora-bloom-theme':
            contract.require(repo.path == '/webkubor/typora-Bloom-theme',
                             'typora-bloom-theme must map to the production repository')
        contract.require(repo.scheme == 'https' and repo.hostname in {'github.com', 'gitlab.com'}
                         and re.fullmatch(r'/[\w.-]+(?:/[\w.-]+)?', repo.path)
                         and not repo.query and not repo.fragment, f'invalid production repo: {project["repo"]}')
    return data


def source_link(repo, file):
    base = repo if repo.startswith("https://") else "https://github.com/" + repo
    return base + ("/-/blob/HEAD/" if "gitlab.com" in base else "/blob/HEAD/") + quote(file, safe="/")


def sources(repo, files):
    return '<div class="sources">' + ' '.join(f'<a href="{E(source_link(repo, f))}">{E(f)}</a>' for f in files) + '</div>'


def swatches(tokens):
    return '<div class="palette">' + ''.join(f'<span class="swatch"><i class="chip" style="background:{E(c)}" aria-hidden="true"></i>{E(k)} <code>{E(c)}</code></span>' for k, c in tokens.items() if c != "transparent") + '</div>'


def copy_task(id_, name, prompt):
    return f'''<div class="copy-row"><button type="button" class="copy" data-target="task-{id_}" data-status="status-{id_}" aria-label="复制 {E(name)} 的完整设计任务" aria-describedby="status-{id_}">复制完整任务</button><span class="status" id="status-{id_}" role="status" aria-live="polite" aria-atomic="true"></span></div>
<details><summary>查看完整任务 · token + 理念 + SVG</summary><pre id="task-{id_}" tabindex="0" aria-label="{E(name)} 完整设计任务">{E(prompt)}</pre></details>'''


def shell(title, intro, content, review=False):
    toolbar = '''<div class="toolbar" aria-label="预览设置"><fieldset><legend>背景</legend>
<label><input type="radio" name="background" value="light" checked> Light</label>
<label><input type="radio" name="background" value="dark"> Dark</label>
<label><input type="radio" name="background" value="checkerboard"> Checkerboard</label></fieldset>
<label for="size">尺寸</label><select id="size" aria-label="Logo 预览尺寸"><option value="32">32 × 32</option><option value="64" selected>64 × 64</option><option value="128">128 × 128</option></select>
<span id="preview-status" class="meta" role="status" aria-live="polite">64 × 64 px · 浅底版本</span></div>''' if review else ''
    delivery = (ROOT / 'design/DELIVERY.md').read_text(encoding='utf-8')
    delivery_section = ('<section id="delivery" class="excluded"><h2>交付说明 · 本地内嵌副本</h2>'
                        '<p>由 design/DELIVERY.md 生成；远端发布状态以说明中的记录为准。</p>'
                        f'<pre tabindex="0" aria-label="完整交付说明">{E(delivery)}</pre></section>')
    return f'''<!doctype html>
<!-- Generated by tools/brand-ui.py; edit brand/*.json or design/briefs.json, then regenerate. -->
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{E(title)} · free-imgbed</title><style>{CSS}</style></head>
<body><a class="skip" href="#content">跳至项目列表</a><header><nav aria-label="品牌交付导航"><a href="logo-review.html">现役标识评审</a><a href="logo-briefs.html">待设计任务</a><a href="screenshots/index.html">验收截图</a><a href="#delivery">交付说明</a><a href="https://github.com/webkubor/free-imgbed">素材仓库</a></nav><p class="eyebrow">FREE-IMGBED / BRAND WORKSPACE</p><h1>{E(title)}</h1><p class="lede">{E(intro)}</p></header><main id="content">{toolbar}{content}{delivery_section}</main><footer>来源：brand/*.json、design/briefs.json 与仓内资产。HTML 由 tools/brand-ui.py 生成；docs/public/design 在开发与构建前复制。复制按钮仅在本机复制任务，尚未向任何模型发送。</footer><script>{SCRIPT}</script></body></html>
'''


def review_page(manifests):
    cards = []
    for m in manifests:
        light = image_data(m["asset"])
        dark = image_data(m["darkAsset"] or m["asset"])
        svg = (ROOT / m["asset"]).read_text()
        dark_svg = (ROOT / m["darkAsset"]).read_text() if m["darkAsset"] else "与浅底版共用同一 SVG。"
        prompt = f'''任务：评审或继续完善 {m['name']} 的版本化品牌标识。
生产仓库：https://github.com/{m['sourceRepo']}
生产资料：
''' + '\n'.join(source_link(m['sourceRepo'], f) for f in m['sourceFiles']) + f'''
现役标识：{m['asset']} / {m['darkAsset'] or '共用浅底版'}
用户已给 token 时以用户为准；下列 token 是本次交付约定，来源与新建议的区别见理念，不可冒称历史规范。
Design token：
{json.dumps(m['tokens'], ensure_ascii=False, indent=2)}
设计理念与选色证据（manifest 记录）：
{m['rationale']}
完整浅底 SVG：
{svg}
完整深底 SVG：
{dark_svg}
交付要求：设计 token + 理念说明 + SVG 三件套。1:1 正方 viewBox、透明画布；无需字体、位图、脚本、外链与 filter。保留合理留白，32/64/128px 检查，32px 在 #FFFFFF 和 #0D1117 背景上实际渲染并观察。无 rect 不足以证明透明，需检查 alpha 边角与边界。新增或替换标识时确认使用方已迁移，图床只保留每项目现役 logo（必要的深浅主题成对文件）；移除弃用版本。运行 python3 tools/check-brand.py --render-dir /tmp/free-imgbed-brand，再刷新 tools/gallery.sh 与 python3 tools/brand-ui.py。自动像素检查不代替可辨识度的目视结论；只报告实际执行结果。
'''
        cards.append(f'''<article class="card" aria-labelledby="name-{m['id']}"><div class="card-head"><h2 id="name-{m['id']}">{E(m['name'])}</h2><span class="tag">manifest: {E(m['status'])}</span></div><p class="meta">{E(m['id'])} · 符号版 / 透明 SVG · ready 为本地资料状态</p>
<div class="comparison"><figure class="preview"><div class="stage" data-bg="light"><img src="{light}" data-light="{light}" data-dark="{dark}" data-name="{E(m['name'])} 现役标识" alt="{E(m['name'])} 现役标识，浅底版本" width="64" height="64"></div><figcaption>浅底版本<br>{download_link(m['asset'])}</figcaption></figure>
<figure class="preview"><div class="stage" data-bg="dark"><img src="{dark}" data-light="{light}" data-dark="{dark}" data-name="{E(m['name'])} 现役标识" alt="{E(m['name'])} 现役标识，深底版本" width="64" height="64"></div><figcaption>{'深底版本<br>' + download_link(m['darkAsset'], '深底 SVG') if m['darkAsset'] else '明暗共用同一 SVG'}</figcaption></figure></div>
{swatches(m['tokens'])}<h3>来源与本次理念</h3><p class="rationale">{E(m['rationale'])}</p>{sources(m['sourceRepo'], m['sourceFiles'])}<p class="meta">证据按 manifest 原文展示；其中历史渲染记录不算本次执行。</p>{copy_task(m['id'],m['name'],prompt)}</article>''')
    return shell(f"{len(manifests)} 项现役标识", "查看现役标识的浅底与深底版本，切换背景和真实像素尺寸。选色理由保留“既有色 / 本次派生色”的区别。", '<div class="grid">' + ''.join(cards) + '</div>', True)


def briefs_page(data):
    cards = []
    for p in data['projects']:
        source_repo = urlsplit(p['repo']).path.strip('/')
        production_name = source_repo.rsplit('/', 1)[-1]
        token = {"primary": p['suggestedColors'][0], "accent": p['suggestedColors'][1],
                 "onLight": p['suggestedColors'][2], "onDark": None, "background": "transparent"}
        prompt = f'''为开源项目「{production_name}」设计独立 logo。请先读取生产资料，不要声称已经向其它模型转交。
生产仓库：{p['repo']}
生产仓名 → 本仓规范 id：{production_name} → {p['id']}（manifest 文件名和 id 使用规范 id；当目录名不同于规范 id 时，在 manifest 记录 dir 为实际资产目录）。
manifest sourceRepo：{source_repo}
资料：
''' + '\n'.join(source_link(p['repo'], f) for f in p['sourceFiles']) + f'''
项目定位：{p['description']}
调性建议：{p['tone']}
现有素材与边界：{p['assetNote']}
形态研究方向（建议，不是既有品牌寓意）：{p['direction']}
选色证据状态：{data['palettePolicy']}
候选 design token（待核验与修订，onDark 尚未确定，不可当成批准规范直接投产）：
{json.dumps(token, ensure_ascii=False, indent=2)}
完整交付要求：
1. 设计 token：列 primary / accent / onLight / onDark 的准确六位 hex、透明背景、1:1 网格及留白规则。区分用户给定值、源码既有值、旧素材取样值与本次建议；提供生产文件链接和行号。无法访问的资料明确记为未核验，不能虚构品牌证据。
2. 设计理念：1–3 句解释形态如何联系产品、为何选色；新解释不能冒充旧作者意图。优先遵循用户的 token、理念和已有 SVG；有冲突时明确记录取舍。
3. 完整 SVG：交付可直接保存的代码，正方 viewBox，透明画布，有 title、role=img 和 aria-label 或有效 aria-labelledby；不依赖脚本、字体、位图、外链或 filter。可使用路径化字母与基础几何，风格随用户要求，不套通用禁令。
4. 深浅主题：若前景不能同时适配，另交 darkAsset；在 #FFFFFF 和 #0D1117 上实际渲染 32px，并附 64/128px 预览。检查 alpha 角块、边界、主体留白和空图，不能仅搜索 rect 判透明。报告实际检查与未覆盖范围。
5. 落仓：新增 brand/{p['id']}.json，id 填 {p['id']}，sourceRepo 填 {source_repo}；填写 name、sourceFiles、asset、darkAsset、tokens、rationale、status。asset / darkAsset 路径统一放入 {p['id']}/；若现有生产目录名不同（如 typora 使用 typora-Bloom-theme），继续用该目录并填写 manifest 的 dir 字段。每项目只保留现役 logo 与必要的深底版本；更新使用方引用后移除弃用 logo，并刷新画廊与评审页。
本任务是新设计委托，没有已完成 SVG 可附；请以完整 SVG 成品结束，不只返回位图、提示词或外部下载占位链接。
'''
        cards.append(f'''<article class="card" aria-labelledby="name-{E(p['id'])}"><div class="card-head"><h2 id="name-{E(p['id'])}">{E(p['id'])}</h2><span class="tag">待设计 / 品牌未确认</span></div><p>{E(p['description'])}</p><p class="meta">{E(p['assetNote'])}</p><h3>建议色板 · 非既有品牌</h3>{swatches({f'候选 {i+1}': c for i,c in enumerate(p['suggestedColors'])})}<p class="rationale">{E(p['direction'])}</p><h3>生产资料</h3>{sources(p['repo'],p['sourceFiles'])}{copy_task(p['id'],p['id'],prompt)}</article>''')
    excluded = '<aside class="notice excluded"><h2>不列入新设计委托</h2>' + ''.join(f'<p><a href="{E(p["source"])}">{E(p["id"])}</a>：{E(p["reason"])}</p>' for p in data['excluded']) + '</aside>'
    return shell(f"{len(cards)} 项真实待设计任务", "只列本地生产仓库与 README 已核对、且本仓尚无确认独立标识的项目。此处是可复制的设计委托，尚未向任何用户模型发送。", '<div class="notice">' + E(data['palettePolicy']) + '</div><div class="grid">' + ''.join(cards) + '</div>' + excluded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    parser.error('--check cannot publish') if args.check and args.publish else None
    manifests = contract.load_manifests()
    briefs = load_briefs()
    outputs = {'logo-review.html': review_page(manifests), 'logo-briefs.html': briefs_page(briefs)}
    stale = []
    for name, text in outputs.items():
        path = ROOT / 'design' / name
        if args.check:
            if not path.is_file() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(text, encoding='utf-8')
    if stale:
        print('FAIL stale brand UI: ' + ', '.join(stale))
        return 1
    if args.publish:
        dest = ROOT / 'docs/public/design'
        dest.mkdir(parents=True, exist_ok=True)
        for name in outputs:
            shutil.copyfile(ROOT / 'design' / name, dest / name)
        screenshots = ROOT / 'design/screenshots'
        if screenshots.is_dir():
            shutil.copytree(screenshots, dest / 'screenshots', dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('*.md'))
            stale_readme = dest / 'screenshots/README.md'
            if stale_readme.is_file():
                stale_readme.unlink()
    print(f"PASS brand UI {'freshness' if args.check else 'generated'}: {len(manifests)} reviews, {len(briefs['projects'])} briefs" + ('; copied to docs/public/design/' if args.publish else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
