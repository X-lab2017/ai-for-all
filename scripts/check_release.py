"""Check release asset coverage, captions and the offline package before deployment."""
from html.parser import HTMLParser
from pathlib import Path
import json,zipfile,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
HUB=SITE/'launch'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.versions=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if t=='img':assert 'alt' in a
        for k in ['src','href','data-video','data-poster']:
            if k in a:self.links.append(a[k])
        if 'data-video' in a:self.versions.append(a['data-video'])
for f in HUB.glob('*.html'):
    p=Page();p.feed(f.read_text());assert len(p.ids)==len(set(p.ids)),f
    for link in p.links:
        if link.startswith('#'):assert link[1:] in p.ids,(f,link)
        elif not re.match(r'^[a-z]+:',link):
            target=(f.parent/link.split('#')[0].split('?')[0]).resolve()
            assert target.is_relative_to(SITE.resolve()) and target.exists(),(f,link)
    if f.name in ['archive-v1.1.html','archive-v1.1-en.html']:assert len(p.versions)==3
    if f.name in ['index.html','en.html']:
        assert len(p.versions)==0
        assert '../film/AI-for-All-Manifesto-V5.mp4' in p.links
        assert 'downloads/AI-for-All-v1.2-V5-Release.zip' in p.links
        assert not any('90s-' in x or 'presentation-v1.1' in x for x in p.links)
for lang in ['ZH','EN','Bilingual']:
    rows=json.loads((ROOT/f'media/release/source/captions-{lang}.json').read_text())
    for i,r in enumerate(rows):
        assert 0<=r['start']<r['end']<=90
        if i:assert rows[i-1]['end']<=r['start']+.001
    assert (HUB/f'downloads/AI-for-All-90s-{lang}.mp4').stat().st_size>1_000_000
out=HUB/'downloads'
for line in (out/'SHA256SUMS.txt').read_text().splitlines():
    digest,name=line.split('  ',1)
    assert hashlib.sha256((out/name).read_bytes()).hexdigest()==digest,name
with zipfile.ZipFile(out/'AI-for-All-Launch-Package.zip') as z:
    assert z.testzip() is None
    for line in (out/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256(z.read('AI-for-All-Launch-Package/'+name)).hexdigest()==digest,name
print('PASS: launch links, 3 video versions, captions, checksums and offline package.')

with zipfile.ZipFile(out/'AI-for-All-v1.2-V5-Release.zip') as z:
    assert z.testzip() is None
    checks=z.read('AI-for-All-v1.2-V5/SHA256SUMS.txt').decode()
    for line in checks.splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256(z.read('AI-for-All-v1.2-V5/'+name)).hexdigest()==digest,name
    assert not any('90s-' in n or n.endswith('.pptx') for n in z.namelist())
print('PASS: current v1.2/V5 hub and package, with legacy assets isolated')
