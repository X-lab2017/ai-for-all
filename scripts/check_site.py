"""Check publication integrity: links, translations, graph closure and accessibility targets."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,sys,xml.etree.ElementTree as ET
from diagrams import DIAGRAMS,svg
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.controls=[];self.figures=0;self.data=[];self.in_data=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='figure':self.figures+=1
  if 'aria-controls' in a:self.controls.append(a['aria-controls'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
  if tag=='script' and a.get('type')=='application/json':self.in_data=True
 def handle_endtag(self,t):
  if t=='script':self.in_data=False
 def handle_data(self,s):
  if self.in_data:self.data.append(json.loads(s))
for name,lang in [('index.html','zh'),('en.html','en')]:
 p=Page();p.feed((SITE/name).read_text());assert p.figures==5,(name,p.figures)
 assert len(p.ids)==len(set(p.ids)),f'duplicate IDs in {name}'
 for target in p.controls:assert target in p.ids,(name,target)
 for link in p.links:
  if link.startswith('#'):assert link[1:] in p.ids,(name,link)
  elif not re.match(r'^[a-z]+:',link):assert (SITE/link.split('#')[0]).exists(),(name,link)
 assert len(p.data)==5
 for d in p.data:assert d['default'] in d['nodes']
 for old in ['access-capability','path-to-benefit','learning-loop']:assert old in p.ids
 for source in p.data:
  for node in source['nodes'].values():assert node['title'] and node['detail']
for d in DIAGRAMS:
 ids={n['id'] for n in d['nodes']}
 for mode,w in [('desktop',980),('mobile',360)]:
  for n in d['nodes']:
   x,y,nw,nh=n[mode];assert 0<=x<x+nw<=w and 0<=y<y+nh<=d['height'][mode],(d['id'],n['id'],mode)
  for edge in d['edges'][mode]:assert edge['fr'] in ids and edge['to'] in ids
 for lang in ['zh','en']:
  for mobile in [False,True]:ET.fromstring(svg(d,lang,mobile))
  p=SITE/'assets/diagrams'/f'{d["id"]}-{lang}'
  assert p.with_suffix('.svg').read_text()==svg(d,lang,export=True),'stale SVG'
  assert p.with_suffix('.png').read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
loop=next(d for d in DIAGRAMS if d['id']=='twin-flywheels')
for mode in ['desktop','mobile']:
 for group in ['growth','value']:
  edges=[e for e in loop['edges'][mode] if e['group']==group];pairs={e['fr']:e['to'] for e in edges};start=edges[0]['fr'];current=start;visited=set()
  while current not in visited:visited.add(current);current=pairs[current]
  assert current==start and len(visited)==6,(mode,group)
assert '三重普惠' in (ROOT/'README.md').read_text()
assert '全球南方贯穿' not in (ROOT/'README.md').read_text()
print('PASS: 2 languages, 5 diagrams, local assets, anchors, aria targets, 4 closed cycles, current SVG exports.')
