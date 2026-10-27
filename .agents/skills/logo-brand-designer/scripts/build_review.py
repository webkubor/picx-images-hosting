#!/usr/bin/env python3
"""Build an offline brand review from local assets; Python 3.9+, standard library only."""

import argparse
import base64
import hashlib
import html
import json
import math
import re
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path, PureWindowsPath

MAX_FILE = 8 * 1024 * 1024
TOKEN_NAMES = ("primary", "accent", "onLight", "onDark", "background")
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
TAGS = set("svg g path rect circle ellipse line polyline polygon defs clipPath mask "
           "linearGradient radialGradient stop use symbol title desc".split())
ATTRS = set("id role aria-label aria-labelledby aria-hidden viewBox width height x y "
            "cx cy r rx ry d points transform fill fill-opacity fill-rule stroke "
            "stroke-width stroke-opacity stroke-linecap stroke-linejoin stroke-miterlimit "
            "stroke-dasharray stroke-dashoffset opacity clip-path clip-rule mask maskUnits "
            "maskContentUnits gradientUnits gradientTransform spreadMethod offset stop-color "
            "stop-opacity x1 x2 y1 y2 fx fy fr href preserveAspectRatio vector-effect "
            "color display visibility overflow focusable version".split())
IDENT = r"[A-Za-z_][A-Za-z0-9_.:-]*"
LOCAL_URL = re.compile(r"url\(\s*(['\"]?)#(" + IDENT + r")\1\s*\)", re.I)
COLOR = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\Z")
LIMITATION = ("仅做结构检查；未解码/渲染像素，未验证透明度、留白、非空图、"
              "token 与实际颜色一致性或 32px 可辨性。需要另行真实渲染并目视验收。")


class ReviewError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewError(message)


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label} 必须是非空字符串")
    return value.strip()


def lines(value, label):
    if value is None:
        return []
    if isinstance(value, str):
        return [text(value, label)]
    require(isinstance(value, list), f"{label} 必须是字符串或字符串数组")
    return [text(item, label) for item in value]


def local_path(root, value, label):
    value = text(value, label)
    require(not Path(value).is_absolute() and not PureWindowsPath(value).drive
            and "\\" not in value and not re.match(r"^[A-Za-z][\w+.-]*:", value),
            f"{label} 只接受 manifest 目录内的相对路径")
    require(".." not in Path(value).parts, f"{label} 禁止 .. 路径逃逸")
    path = (root / value).resolve()
    require(path.is_relative_to(root), f"{label} 路径/符号链接逃逸 manifest 目录")
    require(path.is_file(), f"{label} 文件不存在：{value}")
    return path


def split_name(name):
    if name.startswith("{"):
        namespace, local = name[1:].split("}", 1)
        return namespace, local
    return "", name


def check_svg(data, label):
    try:
        source = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ReviewError(f"{label} SVG 必须是 UTF-8") from exc
    require(not re.search(r"<!\s*(?:DOCTYPE|ENTITY)|<\?(?!xml\s)", source, re.I),
            f"{label} 禁止 DTD、实体和处理指令")
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        raise ReviewError(f"{label} 无效 SVG XML：{exc}") from exc
    require(root.tag == f"{{{SVG_NS}}}svg", f"{label} 根节点必须是标准 SVG 命名空间 svg")
    ids, refs = {}, []
    for node in root.iter():
        namespace, tag = split_name(node.tag)
        require(namespace == SVG_NS and tag in TAGS,
                f"{label} 禁止元素 {tag}（脚本、位图、字体、filter、style/动画等不支持）")
        require(tag in ("title", "desc") or not (node.text or "").strip(),
                f"{label} 文字只能出现在 title/desc；可见文字请路径化")
        require(not (node.tail or "").strip(), f"{label} 禁止游离文字")
        node_id = node.get("id")
        if node_id:
            require(re.fullmatch(IDENT, node_id) and node_id not in ids,
                    f"{label} id 无效或重复：{node_id}")
            ids[node_id] = node
        for key, value in node.attrib.items():
            ns, attr = split_name(key)
            require((not ns or (ns == XLINK_NS and attr == "href")) and attr in ATTRS,
                    f"{label} 禁止属性 {key}（含事件、style、字体、filter、外部资源）")
            require(not any(part in value.lower() for part in ("\\", "/*", "*/", "@", "expression(", "var(")),
                    f"{label} 禁止 CSS 转义/动态资源")
            if attr == "href":
                require(re.fullmatch("#" + IDENT, value), f"{label} href 只允许内部 #id 引用")
                refs.append(value[1:])
            elif re.search(r"url\s*\(", value, re.I):
                match = LOCAL_URL.fullmatch(value)
                require(match is not None, f"{label} url() 只允许单个内部 #id 引用")
                refs.append(match.group(2))
            elif re.search(r"(?:https?:|data:|javascript:|file:|//)", value, re.I):
                require(attr == "aria-label", f"{label} 禁止外部资源：{attr}")
    require(all(ref in ids for ref in refs), f"{label} 含未定义的内部引用")
    # Reject recursive <use>, including recursion through ancestor groups/defs.
    visiting, visited = set(), set()

    def walk(node):
        identity = id(node)
        require(identity not in visiting, f"{label} 内部引用形成循环")
        if identity in visited:
            return
        visiting.add(identity)
        for child in node:
            walk(child)
        for key, value in node.attrib.items():
            attr = split_name(key)[1]
            if attr == "href":
                walk(ids[value[1:]])
            else:
                match = LOCAL_URL.fullmatch(value)
                if match:
                    walk(ids[match.group(2)])
        visiting.remove(identity)
        visited.add(identity)

    walk(root)
    try:
        box = [float(item) for item in re.split(r"[\s,]+", root.get("viewBox", "").strip())]
    except ValueError as exc:
        raise ReviewError(f"{label} 无效 viewBox") from exc
    require(len(box) == 4 and all(math.isfinite(n) for n in box)
            and box[2] > 0 and box[2] == box[3], f"{label} viewBox 必须为正方形")
    if root.get("width") is not None and root.get("height") is not None:
        dimension = r"\s*(\d+(?:\.\d+)?)(px|pt|pc|mm|cm|in|%)?\s*"
        width = re.fullmatch(dimension, root.get("width"))
        height = re.fullmatch(dimension, root.get("height"))
        require(width and height and float(width[1]) > 0
                and float(width[1]) == float(height[1]) and width[2] == height[2],
                f"{label} width/height 必须为同单位的正方形")
    title = root.find(f"{{{SVG_NS}}}title")
    require(title is not None and "".join(title.itertext()).strip(), f"{label} 缺少非空 title")
    labelled = root.get("aria-labelledby", "").split()
    named = bool(root.get("aria-label", "").strip()) or bool(labelled)
    if labelled:
        require(all(ref in ids and split_name(ids[ref].tag)[1] in ("title", "desc")
                    and "".join(ids[ref].itertext()).strip() for ref in labelled),
                f"{label} aria-labelledby 必须引用有效文字节点")
    require(root.get("role") == "img" and named, f"{label} 需要 role=img 及非空 aria 名称")
    return source, {"format": "SVG", "viewBox": box, "checks": "正方形、title/aria、静态安全子集及内部引用通过"}


def raster_size(data, suffix, label):
    if suffix == ".png":
        require(len(data) >= 33 and data[:8] == b"\x89PNG\r\n\x1a\n"
                and data[8:16] == b"\0\0\0\rIHDR", f"{label} 无效 PNG 头")
        return struct.unpack(">II", data[16:24])
    require(len(data) >= 20 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
            and int.from_bytes(data[4:8], "little") + 8 == len(data), f"{label} 无效 WebP 头")
    offset = 12
    while offset + 8 <= len(data):
        tag = data[offset:offset + 4]
        length = int.from_bytes(data[offset + 4:offset + 8], "little")
        chunk = data[offset + 8:offset + 8 + length]
        require(len(chunk) == length, f"{label} WebP chunk 截断")
        if tag == b"VP8X" and length == 10:
            return (int.from_bytes(chunk[4:7], "little") + 1,
                    int.from_bytes(chunk[7:10], "little") + 1)
        if tag == b"VP8L" and length >= 5 and chunk[0] == 0x2f:
            bits = int.from_bytes(chunk[1:5], "little")
            return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
        if tag == b"VP8 " and length >= 10 and chunk[3:6] == b"\x9d\x01\x2a":
            width, height = struct.unpack("<HH", chunk[6:10])
            return width & 0x3fff, height & 0x3fff
        offset += 8 + length + (length % 2)
    raise ReviewError(f"{label} 缺少 WebP 尺寸头")


def load_asset(root, value, label):
    path = local_path(root, value, label)
    require(path.stat().st_size <= MAX_FILE, f"{label} 超过 8 MiB")
    data = path.read_bytes()
    suffix = path.suffix.lower()
    require(suffix in (".svg", ".png", ".webp"), f"{label} 仅支持 SVG/PNG/WebP")
    svg = None
    if suffix == ".svg":
        svg, checks = check_svg(data, label)
        mime = "image/svg+xml"
    else:
        width, height = raster_size(data, suffix, label)
        require(width > 0 and width == height, f"{label} 位图必须为正方形")
        checks = {"format": suffix[1:].upper(), "width": width, "height": height,
                  "checks": "文件头及正方尺寸通过；位图不适用 SVG title/aria 检查，不能替代最终 SVG"}
        mime = "image/" + suffix[1:]
    return {"path": value, "filename": path.name, "mime": mime, "svg": svg,
            "dataUri": f"data:{mime};base64," + base64.b64encode(data).decode("ascii"),
            "sha256": hashlib.sha256(data).hexdigest(), "validation": checks,
            "limitation": LIMITATION}


def load_sources(project, root):
    result = []
    for field in ("sourceFiles", "sources"):
        values = project.get(field, [])
        if isinstance(values, str):
            values = [values]
        require(isinstance(values, list), f"{field} 必须是数组或字符串")
        for item in values:
            if isinstance(item, str):
                value, label = item, item
            else:
                require(isinstance(item, dict), f"{field} 条目必须是字符串或对象")
                value = item.get("url") or item.get("path")
                label = item.get("label") or value
            value, label = text(value, field), text(label, field + ".label")
            if re.match(r"^https?://[^\s]+$", value, re.I):
                result.append({"label": label, "value": value, "url": value})
            else:
                local_path(root, value, field)
                result.append({"label": label, "value": value, "url": None})
    return result


def load_manifest(path):
    require(path.stat().st_size <= MAX_FILE, "manifest 超过 8 MiB")
    manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    require(isinstance(manifest, dict), "manifest 必须是 JSON 对象")
    projects = manifest.get("projects")
    require(isinstance(projects, list) and bool(projects), "projects 必须为非空数组")
    root, records, seen = path.parent.resolve(), [], set()
    for project in projects:
        require(isinstance(project, dict), "project 必须是对象")
        name = text(project.get("name") or project.get("id"), "project.name/id")
        ident = text(project.get("id") or name, "project.id/name")
        require(ident not in seen, f"project id 重复：{ident}")
        seen.add(ident)
        tokens = project.get("tokens")
        require(isinstance(tokens, dict), f"{ident}.tokens 必须是对象")
        require(all(key in tokens for key in TOKEN_NAMES), f"{ident}.tokens 缺少必填 token")
        for key, value in tokens.items():
            require(isinstance(value, str) and (COLOR.fullmatch(value)
                    or (key == "background" and value == "transparent")),
                    f"{ident}.tokens.{key} 需要 hex（background 也可为 transparent）")
        token_sources = project.get("tokenSources", {})
        require(isinstance(token_sources, dict), f"{ident}.tokenSources 必须是对象")
        for key, value in token_sources.items():
            text(value, f"tokenSources.{key}")
        assets = {"asset": load_asset(root, project.get("asset"), ident + ".asset")}
        for key in ("darkAsset", "oldAsset"):
            assets[key] = load_asset(root, project[key], ident + "." + key) if project.get(key) is not None else None
        records.append({"id": ident, "name": name, "tokens": tokens,
                        "tokenSources": {key: token_sources.get(key, "未标注来源，未核验") for key in tokens},
                        "rationale": lines(project.get("rationale"), "rationale"),
                        "userDecisions": lines(project.get("userDecisions"), "userDecisions"),
                        "recommendations": lines(project.get("recommendations"), "recommendations"),
                        "sources": load_sources(project, root), "assets": assets})
    return {"manifest": manifest, "projects": records, "limitation": LIMITATION}


STYLE = """
:root {color-scheme:light; font:15px/1.55 system-ui,sans-serif;color:#18212f;background:#f1f4f8}
* {box-sizing:border-box} [hidden] {display:none!important} body {margin:0} main {max-width:1160px;margin:auto;padding:28px 20px}
h1 {font-size:28px;margin:0 0 10px} h2 {font-size:23px} h3 {font-size:17px;margin:18px 0 8px}
p {margin:8px 0} button,a.download {font:inherit;border:1px solid #9ca9b9;border-radius:7px;background:#fff;color:#172534;padding:7px 12px;cursor:pointer;text-decoration:none}
button:hover,a.download:hover {background:#e8eef5} button:focus-visible,a:focus-visible,textarea:focus-visible {outline:3px solid #147aab;outline-offset:2px}
button[aria-pressed="true"] {background:#183d64;color:white;border-color:#183d64}
.controls,.actions,.tokens {display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0}
.notice {border-left:4px solid #b77812;background:#fff8e7;padding:12px 16px}
.project {background:#fff;border:1px solid #cbd3df;border-radius:12px;margin:24px 0;padding:22px;overflow-wrap:anywhere}
.preview-grid {display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:14px;margin:16px 0}
figure {margin:0} .canvas {min-height:190px;display:flex;align-items:center;justify-content:center;border:1px solid #a9b2c0;border-radius:8px;background:#fff}
.canvas[data-bg="dark"] {background:#0d1117}
.canvas[data-bg="checker"] {background-color:#fff;background-image:conic-gradient(#d3d8de 25%,transparent 0 50%,#d3d8de 0 75%,transparent 0);background-size:20px 20px}
.canvas img {width:32px;height:32px;object-fit:contain} figcaption {margin-top:6px;color:#4c596a}
.token {border:1px solid #d2dae4;border-radius:6px;padding:6px 10px} .swatch {display:inline-block;width:16px;height:16px;border:1px solid #8795a6;vertical-align:middle;margin-right:7px}
small,.muted {color:#4c596a} .evidence {font-size:13px;margin:4px 0 12px}
pre,textarea {font:13px/1.5 ui-monospace,monospace;background:#f6f8fb;border:1px solid #c3cedc;border-radius:6px;padding:12px;max-width:100%}
pre {white-space:pre-wrap;overflow-wrap:anywhere;max-height:360px;overflow:auto} textarea {display:block;width:100%;min-height:85px}
.status {min-height:1.6em;color:#294a32} .manual {min-height:200px} .checks {padding-left:22px} a {color:#155c96}
@media(max-width:560px) {main {padding:18px 12px}.project {padding:14px} h1 {font-size:24px}}
"""

JAVASCRIPT = r"""
const DATA = __PAYLOAD__;
const root = document.getElementById('projects');
const bgButtons = [...document.querySelectorAll('[data-background]')];
const sizeButtons = [...document.querySelectorAll('[data-size]')];
let background = 'light', size = 32;
function el(tag, value, className) {
  const node = document.createElement(tag);
  if (value !== undefined) node.textContent = value;
  if (className) node.className = className;
  return node;
}
function button(label, action) {
  const b = el('button', label); b.type = 'button'; b.addEventListener('click', action); return b;
}
function download(label, filename, content, type) {
  const a = el('a', label, 'download'); a.download = filename;
  a.href = 'data:' + type + ';base64,' + btoa(Array.from(new TextEncoder().encode(content), b => String.fromCharCode(b)).join(''));
  return a;
}
function jsonDownload(label, filename, data) {
  return download(label, filename, JSON.stringify(data, null, 2), 'application/json');
}
function list(parent, title, values, empty) {
  parent.append(el('h3', title));
  if (!values.length) {parent.append(el('p', empty, 'muted')); return;}
  const ul = el('ul'); values.forEach(value => ul.append(el('li', value))); parent.append(ul);
}
function assetTask(label, asset) {
  if (!asset) return label + '：无';
  return label + '：' + asset.path + '\nSHA-256: ' + asset.sha256 + '\n' +
    (asset.svg !== null ? '完整 SVG：\n' + asset.svg : '完整位图 data URI（不能替代最终 SVG）：\n' + asset.dataUri);
}
function fullTask(p, note) {
  return [
    '请依据以下完整资料继续处理品牌标识，并保留离线评审页和真实截图。',
    '项目：' + p.name + ' (' + p.id + ')',
    '先调用当次环境能力发现/工具帮助，再按授权选择工具及模型；不得把复制任务当成已调用。',
    '用户已给定/确认（仅来自 manifest.userDecisions；空白不代表批准）：\n' + (p.userDecisions.join('\n') || '未记录'),
    '建议（未获用户确认）：\n' + (p.recommendations.join('\n') || '未记录'),
    '本页补充（建议，待用户确认）：\n' + (note.trim() || '无'),
    'Design tokens：\n' + JSON.stringify(p.tokens, null, 2),
    'Token 来源（来源分类按记录，不代表已经核验）：\n' + JSON.stringify(p.tokenSources, null, 2),
    '理念（按输入记录；未经说明不得当成用户决策或历史事实）：\n' + (p.rationale.join('\n') || '未记录'),
    '生产来源（未联网验证）：\n' + (p.sources.map(s => s.label + ' — ' + s.value).join('\n') || '未记录'),
    ...Object.entries(p.assets).map(([key, value]) => assetTask(key, value)),
    '结构检查：\n' + JSON.stringify(Object.fromEntries(Object.entries(p.assets).filter(([,a]) => a).map(([k,a]) => [k,a.validation])), null, 2),
    '验证边界：' + DATA.limitation,
    '交付：token + 来源、理念、完整 SVG、review.html、manifest JSON；截图保存到交付目录 screenshots/。',
    '真实渲染浅底 #FFFFFF / 深底 #0D1117 / 棋盘的 32px，查看 64/128px；说明实际测试范围、截图来源及未做项。',
    '原始 manifest（相对路径以原 manifest 目录为根；上文已附实际素材）：\n' + JSON.stringify(DATA.manifest, null, 2)
  ].join('\n\n');
}
async function copyTask(content, status, fallback) {
  status.textContent = '正在复制…'; fallback.hidden = true;
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try { await navigator.clipboard.writeText(content); status.textContent = '完整任务已复制。'; return; }
      catch (_) { /* file:// or permissions may require the explicit fallback below. */ }
    }
    fallback.value = content; fallback.hidden = false; fallback.focus(); fallback.select();
    if (!document.execCommand('copy')) throw new Error('copy returned false');
    fallback.hidden = true; status.textContent = '完整任务已复制。';
  } catch (_) {
    fallback.value = content; fallback.hidden = false; fallback.focus(); fallback.select();
    status.textContent = '自动复制失败。请在下方选中完整任务并手动复制；尚未复制成功。';
  }
}
const downloadBar = document.getElementById('downloads');
downloadBar.append(jsonDownload('下载完整 JSON（含内嵌素材）', 'brand-review-bundle.json', DATA),
  jsonDownload('下载原 manifest', 'manifest.json', DATA.manifest));
const views = [];
DATA.projects.forEach((p, index) => {
  const section = el('article', undefined, 'project'); section.append(el('h2', p.name));
  section.append(el('p', 'ID: ' + p.id, 'muted'));
  const grid = el('div', undefined, 'preview-grid');
  const next = el('figure'), nextCanvas = el('div', undefined, 'canvas'); nextCanvas.dataset.bg = background;
  const nextImg = el('img'); nextImg.alt = p.name + ' 新标识'; nextCanvas.append(nextImg);
  const caption = el('figcaption'); next.append(nextCanvas, caption); grid.append(next);
  let oldImg = null, oldCanvas = null;
  if (p.assets.oldAsset) {
    const old = el('figure'); oldCanvas = el('div', undefined, 'canvas'); oldCanvas.dataset.bg = background;
    oldImg = el('img'); oldImg.alt = p.name + ' 旧标识'; oldImg.src = p.assets.oldAsset.dataUri;
    oldCanvas.append(oldImg); old.append(oldCanvas, el('figcaption', '旧图（对照，不推定为已批准规范）')); grid.append(old);
  } else grid.append(el('p', '首次设计 / 未提供旧图', 'muted'));
  section.append(grid);
  views.push({p, nextImg, nextCanvas, caption, oldImg, oldCanvas});
  section.append(el('h3', 'Design tokens 与来源'));
  const tokens = el('div', undefined, 'tokens');
  Object.entries(p.tokens).forEach(([key, value]) => {
    const item = el('div', undefined, 'token');
    const swatch = el('span', undefined, 'swatch');
    // Only values validated as hex/transparent are applied as CSS.
    if (/^#(?:[a-f\d]{3}|[a-f\d]{4}|[a-f\d]{6}|[a-f\d]{8})$/i.test(value) || value === 'transparent') swatch.style.backgroundColor = value;
    item.append(swatch, el('strong', key + ': ' + value), el('p', p.tokenSources[key], 'evidence')); tokens.append(item);
  }); section.append(tokens);
  list(section, '设计理念（按输入记录）', p.rationale, '未记录理念');
  list(section, '用户给定 / 已确认', p.userDecisions, '未记录用户决策；不能推定为批准');
  list(section, '本次建议（待用户确认）', p.recommendations, '未记录建议');
  section.append(el('h3', '生产资料与来源（构建时未联网核验）'));
  const sources = el('ul');
  p.sources.forEach(s => {
    const li = el('li');
    if (s.url) {const a = el('a', s.label + ' — ' + s.value); a.href = s.url; a.target = '_blank'; a.rel = 'noopener noreferrer'; li.append(a);}
    else li.textContent = s.label + ' — ' + s.value + '（manifest 相对路径，不随 HTML 分发）';
    sources.append(li);
  });
  section.append(p.sources.length ? sources : el('p', '未记录来源，未核验', 'muted'));
  const actions = el('div', undefined, 'actions');
  Object.entries(p.assets).forEach(([key, asset]) => {
    if (!asset) return;
    const a = el('a', '下载 ' + key + ' · ' + asset.filename, 'download');
    a.href = asset.dataUri; a.download = asset.filename; actions.append(a);
    const detail = el('details'); detail.append(el('summary', key + ' · 结构检查 / 实际素材'));
    detail.append(el('p', JSON.stringify(asset.validation)), el('p', asset.limitation, 'muted'));
    if (asset.svg !== null) detail.append(el('pre', asset.svg));
    section.append(detail);
  });
  section.append(actions);
  const noteId = 'review-note-' + index;
  const label = el('label', '评审补充（本次建议，待用户确认；刷新前请复制保存）'); label.htmlFor = noteId;
  const note = el('textarea'); note.id = noteId;
  const fallback = el('textarea', undefined, 'manual'); fallback.hidden = true; fallback.readOnly = true;
  fallback.setAttribute('aria-label', '自动复制失败时的完整任务');
  const status = el('p', '', 'status'); status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
  section.append(label, note, button('复制完整任务（含实际素材）', () => copyTask(fullTask(p, note.value), status, fallback)), status, fallback);
  root.append(section);
});
function refresh() {
  views.forEach(v => {
    const dark = background === 'dark' && v.p.assets.darkAsset;
    const asset = dark || v.p.assets.asset;
    v.nextImg.src = asset.dataUri; v.nextImg.width = v.nextImg.height = size;
    v.nextImg.style.width = v.nextImg.style.height = size + 'px'; v.nextCanvas.dataset.bg = background;
    v.caption.textContent = '新图 · ' + (dark ? '独立深底版' : '主版本') + ' · ' + size + 'px';
    if (v.oldImg) {v.oldImg.style.width = v.oldImg.style.height = size + 'px'; v.oldCanvas.dataset.bg = background;}
  });
  bgButtons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.background === background)));
  sizeButtons.forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.size) === size)));
}
bgButtons.forEach(b => b.addEventListener('click', () => {background = b.dataset.background; refresh();}));
sizeButtons.forEach(b => b.addEventListener('click', () => {size = Number(b.dataset.size); refresh();}));
refresh();
"""


def build_html(data):
    payload = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    script = JAVASCRIPT.replace("__PAYLOAD__", payload)
    digest = base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")
    csp = ("default-src 'none'; img-src data:; style-src 'unsafe-inline'; "
           f"script-src 'sha256-{digest}'; connect-src 'none'; font-src 'none'; "
           "object-src 'none'; base-uri 'none'; form-action 'none'")
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{html.escape(csp, quote=True)}">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>品牌标识 · 离线评审</title>
<style>{STYLE}</style></head><body><main>
<h1>品牌标识 · 离线评审</h1><p>素材已内嵌，无网络依赖。外部来源链接仅供人工核验。</p>
<p class="notice">{html.escape(LIMITATION)} 本页不是渲染验收报告。截图须另存到交付目录 screenshots/ 并注明来源、背景、尺寸和测试范围。</p>
<div class="controls" role="group" aria-label="预览背景">
<button type="button" data-background="light">浅底 #FFFFFF</button>
<button type="button" data-background="dark">深底 #0D1117</button>
<button type="button" data-background="checker">棋盘</button></div>
<div class="controls" role="group" aria-label="预览尺寸">
<button type="button" data-size="32">32px</button><button type="button" data-size="64">64px</button><button type="button" data-size="128">128px</button></div>
<div class="actions" id="downloads"></div><noscript>本页需启用 JavaScript 才能切换预览、下载和复制。所有逻辑均已内嵌。</noscript>
<div id="projects"></div></main><script>{script}</script></body></html>"""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path, help="JSON; local paths are relative to its directory")
    parser.add_argument("--out", required=True, type=Path, help="standalone .html output (existing assets are never overwritten)")
    args = parser.parse_args(argv)
    temporary = None
    try:
        manifest_path = args.manifest.resolve(strict=True)
        output = args.out.resolve()
        require(output.suffix.lower() == ".html", "--out 必须为 .html")
        require(not args.out.is_symlink(), "--out 不允许符号链接")
        require(output != manifest_path, "不能覆盖 manifest")
        data = load_manifest(manifest_path)
        protected = {local_path(manifest_path.parent, asset["path"], "asset")
                     for project in data["projects"] for asset in project["assets"].values() if asset}
        protected.update(local_path(manifest_path.parent, source["value"], "source")
                         for project in data["projects"] for source in project["sources"] if source["url"] is None)
        require(output not in protected, "不能覆盖输入素材或来源文件")
        result = build_html(data)
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent,
                                         prefix=".brand-review-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(result)
        temporary.replace(output)
        print(f"OK: {len(data['projects'])} project(s) -> {output}")
        print("结构校验通过。" + LIMITATION)
        return 0
    except (OSError, ValueError, RecursionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
