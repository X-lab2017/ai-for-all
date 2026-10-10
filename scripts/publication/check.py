from pathlib import Path
from html.parser import HTMLParser
import re,xml.etree.ElementTree as ET
ROOT=Path.cwd();SITE=ROOT/'site'
class CurrentPage(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.reading=False;self.text=[]
 def handle_starttag(self,t,a):
  d=dict(a);self.tags.append((t,d))
  if t=='article' and d.get('class')=='reading-prose':self.reading=True
 def handle_endtag(self,t):
  if t=='article':self.reading=False
 def handle_data(self,s):
  if self.reading:self.text.append(s)
s=(SITE/'index.html').read_text();p=CurrentPage();p.feed(s);ids=[d['id']for _,d in p.tags if 'id'in d];assert len(ids)==len(set(ids))
for _,d in p.tags:
 for key in ['data-track','aria-controls','aria-labelledby']:
  if key in d:assert all(v in ids for v in d[key].split()),d
 for key in ['href','src']:
  v=d.get(key,'')
  if v.startswith('#'):assert v[1:]in ids,v
  elif v and not re.match(r'^[a-z]+:',v):assert (SITE/v.split('#')[0].split('?')[0]).exists(),v
assert all(x in ids for x in ['vision','forces','wheels','possibilities','renewal','fulltext','manifesto'])
assert sum('data-perspective'in d for _,d in p.tags)==3
assert sum('data-satellite'in d for _,d in p.tags)==3
assert sum(d.get('data-track','').startswith('network-')for _,d in p.tags)==12
assert sum(d.get('data-track','').startswith('growth-')for _,d in p.tags)==12
for v in re.findall(r'<svg.*?</svg>',s,re.S):ET.fromstring(v)
body=(ROOT/'README.md').read_text().split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0].strip()
for para in body.split('\n\n'):assert re.sub(r'^#{1,3} ','',para.replace('**',''))in ''.join(p.text)
assert body in (SITE/'AI-for-All-manifesto.md').read_text()
assert '正式发布建议稿' not in s
print('PASS: current v1.2 chapters, canonical text, download, SVGs, local links, controls and geometry counts.')
