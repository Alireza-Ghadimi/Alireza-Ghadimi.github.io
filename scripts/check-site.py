#!/usr/bin/env python3
"""Validate the public homepage, its legacy links and its published assets."""
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
        for name in ('href', 'src', 'data-gif', 'data-poster'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag == 'a' and 'download' in attrs:
            self.resumes.append(attrs['href'])

pages = {'index.html', 'credits.html', 'animated/index.html', 'animated/credits.html'}
published_pages = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.html') if '.git' not in p.parts}
assert published_pages == pages, f'Unexpected or missing public pages: {published_pages ^ pages}'
for relative in sorted(pages):
    path = ROOT / relative
    source = path.read_text()
    page = Page(source)
    assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {relative}'
    assert 'beyond kernel dynamics' not in source.lower()
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
    if relative == 'index.html':
        assert len(page.resumes) == 2
        assert all(urlsplit(url).path == 'assets/Alireza-Ghadimi-Resume.pdf' for url in page.resumes)
        assert len([i for i in page.ids if i.startswith('case-')]) == 15
        assert source.count('class="project-motion"') == 15
        assert 'id="motion-toggle"' not in source and 'noindex' not in source
        assert '<link rel="canonical" href="https://alireza-ghadimi.github.io/">' in source
    elif relative.startswith('animated/'):
        destination = '../' if relative.endswith('/index.html') else '../credits.html'
        assert destination in page.links
        assert f'content="0; url={destination}"' in source

resume = ROOT / 'assets/Alireza-Ghadimi-Resume.pdf'
assert set(ROOT.rglob('*.pdf')) == {resume}, 'Only the public résumé may be included.'
# This is the previously reviewed, employer-neutral PDF. Review and update the
# checksum when deliberately replacing the résumé.
assert hashlib.sha256(resume.read_bytes()).hexdigest() == '89367397e36b13a90682672c63134b3719ab3107391fea9f774c0dc1301c47dc'
content = subprocess.check_output(['pdftotext', str(resume), '-'], text=True)
assert 'beyond kernel dynamics' not in content.lower()

portrait = ROOT / 'assets/alireza-portrait-original.jpg'
assert hashlib.sha256(portrait.read_bytes()).hexdigest() == 'd9065603cb2be55e47de50556cba435f8ebe1b0ba02e5faaacbc783d7d9406ea'
data = json.loads((ROOT / 'content/portfolio.json').read_text())
assert len(data['categories']) == 6 and len(data['projects']) == 15
assert len(set(p['id'] for p in data['projects'])) == 15
motion = ROOT / 'assets/project-motion'
manifest = json.loads((motion / 'manifest.json').read_text())
assert set(manifest) == {p['id'] for p in data['projects']}
for item in manifest.values():
    gif = motion / item['gif']
    assert gif.read_bytes().startswith(b'GIF89a')
    assert gif.stat().st_size == item['bytes']
    assert (motion / item['poster']).exists()
    assert item['frames'] == 48 and (item['width'], item['height']) == (600, 260)
print('PASS: public animated homepage, 15 case studies and GIFs, local links, legacy redirects, public résumé, and original portrait.')
