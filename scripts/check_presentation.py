"""Check broken local assets, control targets and untrusted SVG content before publishing."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
import json,re

ROOT = Path(__file__).resolve().parents[1] / 'site' / 'presentation'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.scenes = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, a['id']
            self.ids.add(a['id'])
        if tag == 'section' and 'scene' in a.get('class', '').split():
            self.scenes.append(a['id'])
        if tag == 'img':
            assert 'alt' in a, 'Image missing alternative text'
        for key in ['src', 'href']:
            if key in a:
                self.links.append(a[key])

p = Page()
p.feed((ROOT / 'index.html').read_text())
assert p.scenes == ['manifesto', 'origins', 'open-models', 'forces', 'public-goods', 'evaluation', 'flywheels', 'practice', 'participate', 'panorama']
source = (ROOT / 'index.html').read_text()
story = json.loads(re.search(r'<script id="story-data" type="application/json">(.*?)</script>', source, re.S)[1])
assert [s['id'] for s in story] == p.scenes
assert sum(s['seconds'] for s in story) == 90
assert all(s['voice'] and s['notes'] for s in story)
assert len(re.findall(r'class="model-card"', source)) == 5
for name in ['阿里巴巴（Qwen）', '深度求索（DeepSeek）', '智谱 AI（GLM）', '月之暗面（Kimi）', '腾讯（混元 / Hunyuan）']:
    assert name in source and name in (ROOT / 'narrative.md').read_text(), name
for link in p.links:
    if link.startswith('#'):
        assert link[1:] in p.ids, link
    elif not link.startswith(('https:', 'http:')):
        assert (ROOT / link.split('#')[0].split('?')[0]).exists(), link
for asset in (ROOT / 'assets').glob('*.svg'):
    r = ET.fromstring(asset.read_bytes())
    for node in r.iter():
        assert node.tag.split('}')[-1] not in ('script', 'foreignObject'), asset
        assert not any(key.lower().startswith('on') for key in node.attrib), asset
print('PASS: 10 chapters, 90-second narrative, 5 model families, unique IDs, local assets and passive SVGs.')
