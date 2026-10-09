"""Check broken local assets, control targets and untrusted SVG content before publishing."""
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

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
            assert a.get('alt'), 'Image missing alternative text'
        for key in ['src', 'href']:
            if key in a:
                self.links.append(a[key])

p = Page()
p.feed((ROOT / 'index.html').read_text())
assert p.scenes == ['origins', 'flywheels', 'panorama']
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
print('PASS: three scenes, unique IDs, local assets, descriptive images, passive SVG assets.')
