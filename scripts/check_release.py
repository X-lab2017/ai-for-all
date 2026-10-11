"""Validate the actual new release and guard against reintroducing old editions."""
from html.parser import HTMLParser
from pathlib import Path
import re,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';HUB=SITE/'launch'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='img':assert 'alt' in a
  for k in ['src','href']:
   if k in a:self.links.append(a[k])
for f in HUB.glob('*.html'):
 p=Page();s=f.read_text();p.feed(s);assert len(p.ids)==len(set(p.ids)),f
 for link in p.links:
  if link.startswith('#'):assert link[1:] in p.ids,(f,link)
  elif not re.match(r'^[a-z]+:',link):
   target=(f.parent/link.split('#')[0].split('?')[0]).resolve();assert target.is_relative_to(SITE.resolve()) and target.exists(),(f,link)
 assert not any(x in s for x in ['90s-','Conference-','archive-v1.1','双飞轮','10 页','讲述稿','Draft']),f
 if f.name in ['index.html','en.html']:
  assert all(x in p.ids for x in ['manifesto','presentation','film','article','visuals'])
  assert '../film/AI-for-All-Manifesto-V5.mp4' in p.links
out=HUB/'downloads'
for line in (out/'SHA256SUMS.txt').read_text().splitlines():
 digest,name=line.split('  ',1);assert hashlib.sha256((out/name).read_bytes()).hexdigest()==digest,name
with zipfile.ZipFile(out/'AI-for-All-Release-2026-10-11.zip') as z:
 assert z.testzip() is None
 for line in z.read('SHA256SUMS.txt').decode().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
 assert not any(any(x in n for x in ['90s-','Conference-','v1.1','narrative.md','notes-ZH','Draft','.pptx']) for n in z.namelist())
 assert z.read('04-publication/article.txt')==(ROOT/'publication/article.txt').read_bytes()
 assert z.read('03-film/AI-for-All-Manifesto-V5.mp4')==(SITE/'film/AI-for-All-Manifesto-V5.mp4').read_bytes()
 assert '02-presentation/presentation/index.html' in z.namelist()
for n in ['cover-wide','share-square','share-poster','framework-strip','film-cover','panorama','social-preview','manifesto-qr']:
 assert (HUB/'assets'/f'{n}.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),n
print('PASS: four approved editions, current visuals, links, text identity and complete package checksums')
