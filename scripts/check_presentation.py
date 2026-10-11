"""Check the approved current bilingual presentation."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, subprocess, sys, xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'site/presentation'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags = []
    def handle_starttag(self, tag, attrs): self.tags.append((tag, dict(attrs)))
for page, data in [('index.html', 'data.js'), ('en.html', 'data-en.js')]:
    source = (DECK / page).read_text()
    parser = Page(); parser.feed(source)
    ids = [a['id'] for _, a in parser.tags if 'id' in a]
    assert len(ids) == len(set(ids)), page
    slides = [a for t, a in parser.tags if t == 'section' and 'slide' in a.get('class', '').split()]
    assert [s['id'] for s in slides] == [f's{i}' for i in range(1, 14)]
    for tag, attrs in parser.tags:
        if tag == 'img': assert 'alt' in attrs
        for key in ['aria-controls', 'aria-labelledby', 'data-track']:
            if key in attrs: assert all(x in ids for x in attrs[key].split()), attrs
        for key in ['href', 'src']:
            link = attrs.get(key, '')
            if link.startswith('#'): assert link[1:] in ids, link
            elif link and not re.match(r'^[a-z]+:', link):
                assert (DECK / link.split('#')[0].split('?')[0]).exists(), link
    for svg in re.findall(r'<svg.*?</svg>', source, re.S): ET.fromstring(svg)
    raw = (DECK / data).read_text()
    story = json.loads(raw.split('window.DECK=')[1].split(';\nwindow.SOURCES=')[0])
    assert len(story) == 13 and sum(s['seconds'] for s in story) == 180
    assert all(s['notes'] and s['title'] for s in story)
    assert all(x in ids for x in ['language', 'theme', 'lfx-tab-0', 'lfx-tab-1'])
    assert source.index('class="panorama"', source.index('id="s12"')) < source.index('class="pan-summary"')
    for value in ['258', '642', '219', 'linux-report-cover.png']: assert value in source
    assert '<html lang="en">' in source if page == 'en.html' else '<html lang="zh-CN">' in source
for name, master in [('logo-light.svg', 'ColorLight'), ('logo-dark.svg', 'ColorDark')]:
    assert (DECK/'assets'/name).read_bytes() == (ROOT/'site/assets'/f'XlabAI_Horizontal_{master}.svg').read_bytes()
for name, master in [('brand.svg', 'ColorLight'), ('brand-dark.svg', 'ColorDark')]:
    assert (ROOT/'site/assets'/name).read_bytes() == (ROOT/'site/assets'/f'XlabAI_Horizontal_{master}.svg').read_bytes()
for svg in (DECK/'assets').glob('*.svg'):
    for node in ET.fromstring(svg.read_bytes()).iter():
        assert node.tag.split('}')[-1] not in ['script', 'foreignObject']
        assert not any(k.lower().startswith('on') for k in node.attrib)
for js in DECK.glob('*.js'): subprocess.run(['node', '--check', str(js)], check=True)
print('PASS: bilingual 13 chapters, 180-second tour, data, panorama, local assets, SVGs, theme logos, JavaScript syntax.')
