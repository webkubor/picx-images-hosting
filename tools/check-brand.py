#!/usr/bin/env python3
"""Validate brand/*.json and render their SVGs. Requires rsvg-convert + Pillow.

python3 tools/check-brand.py --render-dir /tmp/free-imgbed-brand
Exit 1: contract/asset failure; exit 2: missing rendering dependency.
Previews and stats.json are written only to --render-dir (otherwise a temp dir).
"""

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
FIELDS = {"id", "name", "sourceRepo", "sourceFiles", "oldAsset", "asset", "darkAsset",
          "tokens", "rationale", "status"}
TOKEN_FIELDS = {"primary", "accent", "onLight", "onDark", "background"}
HEX = re.compile(r"#[0-9a-fA-F]{6}\Z")
# Basic geometry and local gradients/masks are allowed; executable/foreign/font/
# raster/filter elements are rejected by this allowlist, not a rect heuristic.
ELEMENTS = {"svg", "title", "desc", "g", "defs", "path", "rect", "circle", "ellipse",
            "line", "polyline", "polygon", "linearGradient", "radialGradient", "stop",
            "clipPath", "mask", "use"}
SVG_NS = "http://www.w3.org/2000/svg"
SIZES = (32, 64, 128, 256)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def relative_path(value):
    require(isinstance(value, str) and bool(value), "path must be a nonempty string")
    p = PurePosixPath(value)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in value
            and not any(c in value for c in (":", "~", "?", "#"))
            and p.as_posix() == value, f"unsafe repository-relative path: {value}")
    return p


def local_asset(value):
    relative_path(value)
    p = (ROOT / value).resolve()
    require(p.is_relative_to(ROOT) and p.is_file(), f"missing or escaping asset: {value}")
    require(p.stat().st_size <= 2 * 1024 * 1024, f"asset exceeds 2 MiB: {value}")
    return p


def load_manifests(root=ROOT):
    """Shared loader for gallery and review generator; never infer a replacement."""
    paths = sorted((root / "brand").glob("*.json"))
    require(bool(paths), "no brand/*.json manifests")
    result = []
    seen = set()
    for path in paths:
        d = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(d, dict) and set(d) == FIELDS, f"{path.name}: exact fields must be {sorted(FIELDS)}")
        require(isinstance(d["id"], str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", d["id"]), "invalid id")
        require(d["id"] == path.stem and d["id"] not in seen, "id must match unique manifest filename")
        seen.add(d["id"])
        for key in ("name", "rationale"):
            require(isinstance(d[key], str) and bool(d[key].strip()), f"{path.name}: empty {key}")
        require(isinstance(d["sourceRepo"], str) and re.fullmatch(r"[\w.-]+/[\w.-]+", d["sourceRepo"]), "sourceRepo must be owner/repo")
        require(isinstance(d["sourceFiles"], list) and bool(d["sourceFiles"]), "sourceFiles must be a nonempty list")
        for source in d["sourceFiles"]:
            relative_path(source)  # Remote production files need not live in this asset repo.
        require(len(set(d["sourceFiles"])) == len(d["sourceFiles"]), "duplicate sourceFiles")
        require(d["status"] in {"draft", "ready", "review"}, "invalid status")
        t = d["tokens"]
        require(isinstance(t, dict) and set(t) == TOKEN_FIELDS, "invalid token contract")
        require(t["background"] == "transparent", "tokens.background must be transparent")
        require(all(isinstance(t[k], str) and HEX.fullmatch(t[k]) for k in TOKEN_FIELDS - {"background"}), "tokens must use six-digit hex")
        local_asset(d["oldAsset"])
        for key in ("asset", "darkAsset"):
            if key == "darkAsset" and d[key] is None:
                require(t["onLight"].lower() == t["onDark"].lower(), "null darkAsset needs identical theme foregrounds")
                continue
            p = local_asset(d[key])
            require(p.suffix == ".svg" and PurePosixPath(d[key]).parts[0] == d["id"], "new SVG must be in its project directory")
            require(d[key] != d["oldAsset"], "new asset must preserve old path")
        require(d["darkAsset"] != d["asset"], "use null for a shared theme asset")
        result.append(d)
    return result


def svg_structure(path, manifest, theme):
    text = path.read_text(encoding="utf-8")
    require(not re.search(r"<!DOCTYPE|<!ENTITY|<\?xml-stylesheet", text, re.I), "XML entities/stylesheets are forbidden")
    svg = ET.fromstring(text)
    require(svg.tag == f"{{{SVG_NS}}}svg", "root must be namespaced svg")
    vb = [float(n) for n in re.split(r"[\s,]+", svg.get("viewBox", "").strip()) if n]
    require(len(vb) == 4 and all(math.isfinite(v) for v in vb) and vb[2] > 0 and vb[2] == vb[3], "viewBox must be a finite positive square")
    require(svg.get("role") == "img" and svg.get("aria-hidden") != "true", "SVG needs exposed role=img")
    ids = {}
    for el in svg.iter():
        if el.get("id"):
            require(el.get("id") not in ids, "duplicate SVG id")
            ids[el.get("id")] = el
    titles = [el for el in svg if el.tag == f"{{{SVG_NS}}}title" and "".join(el.itertext()).strip()]
    require(bool(titles), "SVG needs a nonempty title")
    labelled = svg.get("aria-labelledby", "").split()
    require(bool(svg.get("aria-label", "").strip()) or bool(labelled), "SVG needs an accessible name")
    require(svg.get("aria-labelledby") is None or bool(labelled), "aria-labelledby must not be empty")
    for ref in labelled:
        require(ref in ids and bool("".join(ids[ref].itertext()).strip()), f"broken aria-labelledby: {ref}")
    colors = set()
    refs = []
    for el in svg.iter():
        require(el.tag.startswith(f"{{{SVG_NS}}}") and el.tag.split("}")[-1] in ELEMENTS, f"forbidden SVG element: {el.tag}")
        for attr, value in el.attrib.items():
            key = attr.split("}")[-1].lower()
            require(not key.startswith("on") and key not in {"style", "filter", "class", "base"}
                    and not key.startswith("font"), f"forbidden SVG attribute: {attr}")
            if key == "href":
                require(value.startswith("#") and len(value) > 1, "only local fragment references are allowed")
                refs.append(value[1:])
            require(not re.search(r"(?:https?:|data:|javascript:|file:|@import|@font-face)", value, re.I), "external/embedded resource forbidden")
            for ref in re.findall(r"url\((.*?)\)", value, re.I):
                ref = ref.strip(" \"'")
                require(ref.startswith("#"), "only local url(#id) references allowed")
                refs.append(ref[1:])
            if key in {"fill", "stroke", "stop-color"}:
                require(value == "none" or HEX.fullmatch(value) or re.fullmatch(r"url\(#[\w.-]+\)", value), "paint must be an explicit hex, none or local gradient")
                if HEX.fullmatch(value):
                    colors.add(value.upper())
    for ref in refs:
        require(ref in ids, f"missing local SVG reference: {ref}")
    require(manifest["tokens"][theme].upper() in colors, f"{theme} token not painted in SVG")
    documented = {c.upper() for c in re.findall(r"#[0-9a-fA-F]{6}\b", json.dumps(manifest["tokens"]) + manifest["rationale"])}
    require(colors <= documented, f"undocumented SVG colors: {sorted(colors - documented)}")
    return {"viewBox": vb, "colors": sorted(colors), "bytes": path.stat().st_size}


def render_asset(path, output, Image):
    renders = {}
    for size in SIZES:
        target = output / f"{size}.png"
        cmd = ["rsvg-convert", "--width", str(size), "--height", str(size), "--output", str(target), str(path)]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
        with Image.open(target) as source:
            require(source.mode == "RGBA", "render has no RGBA alpha channel")
            image = source.copy()
        alpha = image.getchannel("A")
        bbox = alpha.getbbox()
        require(bbox is not None, f"empty SVG at {size}px")
        total = size * size
        hist = alpha.histogram()
        coverage = (total - hist[0]) / total
        require(0.01 <= coverage <= 0.85, f"empty or filled canvas at {size}px (coverage={coverage:.3f})")
        corner = max(1, size // 32)
        boxes = [(0, 0, corner, corner), (size-corner, 0, size, corner),
                 (0, size-corner, corner, size), (size-corner, size-corner, size, size)]
        require(all(alpha.crop(box).getextrema()[1] == 0 for box in boxes), f"nontransparent corner patch at {size}px")
        margins = [bbox[0] / size, bbox[1] / size, (size-bbox[2]) / size, (size-bbox[3]) / size]
        require(min(margins) >= 0.05, f"alpha touches canvas safety boundary at {size}px")
        span = max(bbox[2]-bbox[0], bbox[3]-bbox[1]) / size
        # 256px is the measurement grid; smaller grids include antialias rounding.
        if size == 256:
            # Permit one raster pixel of measurement rounding at either threshold.
            require(0.72 - 1/256 <= span <= 0.80 + 1/256, f"subject span outside 72–80% (±1px): {span:.4f}")
            require(abs(margins[0]-margins[2]) <= 0.08 and abs(margins[1]-margins[3]) <= 0.08, "unbalanced transparent margins")
        for name, color in (("light", "#FFFFFF"), ("dark", "#0D1117")):
            base = Image.new("RGBA", image.size, color)
            Image.alpha_composite(base, image).convert("RGB").save(output / f"{size}-{name}.png")
        checker = Image.new("RGBA", image.size, "#FFFFFF")
        block = max(2, size // 16)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(checker)
        for y in range(0, size, block):
            for x in range(0, size, block):
                if (x // block + y // block) % 2:
                    draw.rectangle((x, y, x+block-1, y+block-1), fill="#D1D5DB")
        Image.alpha_composite(checker, image).convert("RGB").save(output / f"{size}-checkerboard.png")
        renders[str(size)] = {"alphaBBox": list(bbox), "span": round(span, 6), "margins": margins,
                              "coverage": round(coverage, 6), "alphaExtrema": list(alpha.getextrema()),
                              "transparentPixels": hist[0], "partialAlphaPixels": sum(hist[1:255]),
                              "cornerPatch": corner, "transparentCorners": True}
    return renders


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-dir", type=Path)
    args = parser.parse_args()
    output = args.render_dir or Path(tempfile.mkdtemp(prefix="free-imgbed-brand-"))
    require(not output.resolve().is_relative_to(ROOT), "render-dir must be outside the repository (no duplicate preview assets)")
    output.mkdir(parents=True, exist_ok=True)
    missing = []
    if not shutil.which("rsvg-convert"):
        missing.append("rsvg-convert (librsvg2-bin / brew install librsvg)")
    try:
        from PIL import Image, __version__ as pillow_version
    except ImportError:
        missing.append("Pillow (python3 -m pip install Pillow)")
    report = {"ok": False, "sizes": list(SIZES), "assets": [], "errors": [],
              "visualReview": "not automated: inspect 32px light/dark previews for recognition"}
    if missing:
        report["errors"] = ["missing dependency: " + item for item in missing]
        (output / "stats.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print("\n".join(report["errors"]), file=sys.stderr)
        return 2
    report["renderer"] = subprocess.check_output(["rsvg-convert", "--version"], text=True).strip()
    report["pillow"] = pillow_version
    try:
        manifests = load_manifests()
        report["manifestCount"] = len(manifests)
    except (ValueError, OSError, TypeError) as exc:
        report["errors"].append(str(exc))
        manifests = []
    for manifest in manifests:
        for key, theme in (("asset", "onLight"), ("darkAsset", "onDark")):
            if manifest[key] is None:
                continue
            entry = {"id": manifest["id"], "variant": key, "path": manifest[key], "ok": False}
            try:
                path = local_asset(manifest[key])
                entry.update(svg_structure(path, manifest, theme))
                folder = output / manifest["id"] / key
                folder.mkdir(parents=True, exist_ok=True)
                entry["renders"] = render_asset(path, folder, Image)
                entry["ok"] = True
            except (ValueError, OSError, TypeError, ET.ParseError, subprocess.SubprocessError) as exc:
                entry["error"] = str(exc)
                report["errors"].append(f"{manifest[key]}: {exc}")
            report["assets"].append(entry)
    report["ok"] = not report["errors"] and bool(manifests)
    (output / "stats.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for err in report["errors"]:
        print("FAIL " + err, file=sys.stderr)
    print(f"{'PASS' if report['ok'] else 'FAIL'}: {len(manifests)} manifests, "
          f"{sum(a['ok'] for a in report['assets'])}/{len(report['assets'])} SVGs; sizes=32/64/128/256")
    print(f"Previews + JSON: {output}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
