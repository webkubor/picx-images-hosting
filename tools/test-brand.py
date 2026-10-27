#!/usr/bin/env python3
"""Focused regression checks for the SVG validator's failure paths.
Run: python3 tools/test-brand.py (requires rsvg-convert + Pillow).
"""
import base64
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('brandcheck', ROOT / 'tools/check-brand.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class BrandFailureCases(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix='brand-regression-')
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.manifest = check.load_manifests()[0]
        self.svg = (ROOT / self.manifest['asset']).read_text()

    def reject_structure(self, text):
        path = self.root / 'fixture.svg'
        path.write_text(text)
        with self.assertRaises(ValueError):
            check.svg_structure(path, self.manifest, 'onLight')

    def test_executable_and_foreign_resources(self):
        for name, body in {
            'script': '<script>alert(1)</script>',
            'external': '<use href="https://example.com/x.svg#x"/>',
            'font': '<text>bad</text>',
            'bitmap': '<image href="data:image/png;base64,eA=="/>',
            'filter': '<filter id="f"/>',
            'event': '<path onclick="alert(1)" d="M0 0H10"/>',
            'stylesheet': '<style>@import "https://example.com/a.css";</style>',
            'broken-reference': '<use href="#missing"/>',
        }.items():
            with self.subTest(name=name):
                self.reject_structure(self.svg.replace('</svg>', body + '</svg>'))

    def test_square_and_accessible_name(self):
        mutations = [self.svg.replace('0 0 256 256', '0 0 256 200'),
                     self.svg.replace('aria-label="Chat Mood Gen 聊天画幅"', ''),
                     self.svg.replace('<title>Chat Mood Gen 聊天画幅</title>', ''),
                     self.svg.replace('role="img"', 'role="presentation"'),
                     self.svg.replace('aria-label=', 'aria-labelledby="" aria-label=')]
        for text in mutations:
            with self.subTest(text=text[:100]):
                self.reject_structure(text)

    def test_escaping_paths(self):
        for value in ('../secret.svg', '/tmp/a.svg', 'project/../a.svg', 'https://example.com/a.svg'):
            with self.subTest(path=value), self.assertRaises(ValueError):
                check.relative_path(value)

    def test_real_alpha_rejects_full_path_empty_and_tiny_art(self):
        from PIL import Image
        for name, body in {
            'path-background': '<path fill="#178A35" d="M0 0H256V256H0Z"/>',
            'empty': '',
            'tiny': '<path fill="#178A35" d="M125 125H131V131H125Z"/>',
        }.items():
            with self.subTest(name=name):
                path = self.root / (name + '.svg')
                path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">' + body + '</svg>')
                folder = self.root / name
                folder.mkdir()
                with self.assertRaises(ValueError):
                    check.render_asset(path, folder, Image)

    def test_missing_renderer_is_nonzero_with_failed_json(self):
        env = os.environ.copy()
        env['PATH'] = str(self.root / 'no-bin')
        folder = self.root / 'missing-renderer'
        run = subprocess.run([sys.executable, str(ROOT / 'tools/check-brand.py'), '--render-dir', str(folder)], env=env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn('rsvg-convert', run.stderr)
        self.assertFalse(json.loads((folder / 'stats.json').read_text())['ok'])

    def test_missing_pillow_is_nonzero(self):
        # Isolate Python from site-packages while preserving the CLI renderer.
        run = subprocess.run([sys.executable, '-S', str(ROOT / 'tools/check-brand.py'), '--render-dir', str(self.root / 'missing-pillow')], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn('Pillow', run.stderr)


class BrandDeliveryCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = {}
        for name in ('brand-ui', 'gallery'):
            spec = importlib.util.spec_from_file_location(name, ROOT / f'tools/{name}.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cls.modules[name] = module

    def test_brief_ids_preserve_production_repo_mapping(self):
        ui = self.modules['brand-ui']
        data = ui.load_briefs()
        typora = next(p for p in data['projects'] if p['id'] == 'typora-bloom-theme')
        self.assertEqual(typora['repo'], 'https://github.com/webkubor/typora-Bloom-theme')
        text = ui.briefs_page(data)
        for expected in ('typora-Bloom-theme → typora-bloom-theme',
                         'brand/typora-bloom-theme.json', 'id 填 typora-bloom-theme',
                         'sourceRepo 填 webkubor/typora-Bloom-theme',
                         '导入 typora-bloom-theme/'):
            self.assertIn(expected, text)
        self.assertNotIn('brand/typora-Bloom-theme.json', text)
        typora['id'] = 'typora-Bloom-theme'
        from unittest.mock import patch
        with patch.object(ui.json, 'loads', return_value=data), self.assertRaises(ValueError):
            ui.load_briefs()

    def test_site_gallery_uses_root_theme_and_readme_uses_system(self):
        gallery = self.modules['gallery']
        site = gallery.build(site_theme=True)
        readme = gallery.build()
        self.assertNotIn('prefers-color-scheme', site)
        self.assertIn('.dark .brand-gallery-light', site)
        self.assertIn('.dark .brand-gallery-dark', site)
        self.assertIn('prefers-color-scheme: dark', readme)
        for _, asset, dark in gallery.entries():
            self.assertIn(asset, site)
            if dark:
                self.assertIn(f'class="brand-gallery-dark" src="{gallery.BASE}{dark}"', site)

    def test_local_downloads_match_all_manifest_bytes_and_delivery_is_embedded(self):
        ui = self.modules['brand-ui']
        manifests = check.load_manifests()
        review = ui.review_page(manifests)

        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.downloads = []
                self.delivery = False

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'a' and 'download' in attrs:
                    self.downloads.append(attrs)
                if attrs.get('id') == 'delivery':
                    self.delivery = True

        links = Links()
        links.feed(review)
        assets = [m[key] for m in manifests for key in ('asset', 'darkAsset') if m[key]]
        self.assertEqual(len(links.downloads), len(assets))
        for link, asset in zip(links.downloads, assets):
            self.assertEqual(link['download'], Path(asset).name)
            self.assertTrue(link['href'].startswith('data:image/svg+xml;base64,'))
            self.assertEqual(base64.b64decode(link['href'].split(',', 1)[1]), (ROOT / asset).read_bytes())
            self.assertNotIn(ui.CDN + asset, review)
        for page in (review, ui.briefs_page(ui.load_briefs())):
            self.assertIn('href="#delivery"', page)
            self.assertIn(ui.E((ROOT / 'design/DELIVERY.md').read_text()), page)
        self.assertTrue(links.delivery)


if __name__ == '__main__':
    unittest.main(verbosity=2)
