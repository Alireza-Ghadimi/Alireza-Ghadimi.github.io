#!/usr/bin/env python3
"""Validate the two built profiles and their local links before publication."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids, self.resumes = [], [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for name in ('href', 'src'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag == 'a' and 'download' in attrs:
            self.resumes.append(attrs['href'])

for relative in ('index.html', 'full-profile/index.html', 'credits.html', 'full-profile/credits.html'):
    path = ROOT / relative
    source = path.read_text()
    page = Page(source)
    assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {relative}'
    assert 'beyond kernel dynamics' not in source.lower()
    if relative in ('index.html', 'credits.html'):
        assert 'huawei' not in source.lower() and 'openjiuwen' not in source.lower()
    for value in page.links:
        url = urlsplit(value)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            assert not url.fragment or url.fragment in page.ids, f'Missing anchor {value}'
            continue
        target = (path.parent / unquote(url.path)).resolve()
        assert target.is_relative_to(ROOT), f'Path outside site: {value}'
        assert target.exists(), f'Missing asset {relative}: {value}'
    if relative.endswith('index.html'):
        expected = 'Alireza-Ghadimi-Resume-Full.pdf' if relative.startswith('full-profile') else 'Alireza-Ghadimi-Resume.pdf'
        assert len(page.resumes) == 2 and all(expected in url for url in page.resumes)
        assert len([i for i in page.ids if i.startswith('case-')]) == 15
        if relative.startswith('full-profile'):
            assert 'Huawei' in source and 'OpenJiuwen' in source

for full in (False, True):
    path = ROOT / 'assets' / ('Alireza-Ghadimi-Resume-Full.pdf' if full else 'Alireza-Ghadimi-Resume.pdf')
    content = subprocess.check_output(['pdftotext', str(path), '-'], text=True).lower()
    assert 'beyond kernel dynamics' not in content
    assert ('huawei' in content) == full
    assert ('openjiuwen' in content) == full

portrait = ROOT / 'assets/alireza-portrait-original.jpg'
assert hashlib.sha256(portrait.read_bytes()).hexdigest() == 'd9065603cb2be55e47de50556cba435f8ebe1b0ba02e5faaacbc783d7d9406ea'
data = json.loads((ROOT / 'content/portfolio.json').read_text())
assert len(data['categories']) == 6 and len(data['projects']) == 15
assert len(set(p['id'] for p in data['projects'])) == 15
print('PASS: both profiles, 15 case studies, local links, matching résumés, exclusions, and original portrait.')
