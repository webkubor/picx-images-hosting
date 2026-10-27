#!/usr/bin/env python3
"""Read-only audit of public project logo assets in free-imgbed.

Usage: python3 tools/audit-brand.py [--json]
"""

import argparse
import hashlib
import json
import re
import struct
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".avif"}
LOGO_NAMES = re.compile(r"(?:logo|icon|favicon|avatar|brand)", re.I)
SVG_VIEWBOX = re.compile(r'\bviewBox=["\']\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)')
SVG_IDENTITY = re.compile(r'(?:aria-label|<title)[^>]*', re.I)


def dimensions(path):
    if path.suffix == ".svg":
        match = SVG_VIEWBOX.search(path.read_text(errors="replace"))
        return [int(float(match[1])), int(float(match[2]))] if match else None
    if path.suffix == ".png":
        with path.open("rb") as stream:
            header = stream.read(24)
        if header[:8] == b"\x89PNG\r\n\x1a\n":
            return list(struct.unpack(">II", header[16:24]))
    return None


def audit():
    groups = defaultdict(list)
    assets = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_dir() or path.name in {"docs", "tools", "web", ".git"}:
            continue
        for image in path.rglob("*"):
            if not image.is_file() or image.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            if not LOGO_NAMES.search(image.name):
                continue
            relative = image.relative_to(ROOT).as_posix()
            digest = hashlib.sha256(image.read_bytes()).hexdigest()
            groups[digest].append(relative)
            notes = []
            size = dimensions(image)
            if size and image.suffix == ".png" and min(size) < 256:
                notes.append("bitmap-under-256px")
            if image.name.lower().startswith(("icon", "favicon")):
                notes.append("name-needs-review")
            if image.suffix == ".svg":
                text = image.read_text(errors="replace")
                labels = SVG_IDENTITY.findall(text)
                if labels and any(other in " ".join(labels).lower() for other in ("gham", "scorecard")):
                    notes.append("verify-svg-brand-label")
            assets.append({"path": relative, "size": image.stat().st_size,
                           "dimensions": size, "sha256": digest, "notes": notes})
    return {"assets": assets,
            "duplicates": [paths for paths in groups.values() if len(paths) > 1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable audit")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(f"Brand assets: {len(report['assets'])}")
    for asset in report["assets"]:
        size = f"{asset['size']} bytes"
        dims = f" {asset['dimensions'][0]}x{asset['dimensions'][1]}" if asset["dimensions"] else ""
        notes = f" [{', '.join(asset['notes'])}]" if asset["notes"] else ""
        print(f"  {asset['path']}: {size}{dims}{notes}")
    print(f"Duplicate sets: {len(report['duplicates'])}")
    for paths in report["duplicates"]:
        print("  " + " = ".join(paths))


if __name__ == "__main__":
    main()
