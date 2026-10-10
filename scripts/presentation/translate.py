from pathlib import Path
from html.parser import HTMLParser
import json,re,html
R=Path(__file__).parent

def build_english(out):
 d=json.loads((R/'translations.json').read_text());missing=set()
 def t(s):
  if not re.search('[\u4e00-\u9fff]',s):return s
  key=s.strip()
  if key not in d:missing.add(key);return s
  return s[:len(s)-len(s.lstrip())]+d[key]+s[len(s.rstrip()):]
 class Translator(HTMLParser):
  def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
  def handle_starttag(self,tag,attrs):
   a=[]
   for k,v in attrs:
    if v is None:a.append(k);continue
    if k in ['alt','title','aria-label','content']:v=t(v)
    if tag=='html'and k=='lang':v='en'
    if tag=='script'and k=='src'and v=='data.js':v='data-en.js'
    if tag=='a'and k=='href'and v=='en.html':v='index.html'
    if tag=='a'and k=='href'and v=='../?lang=zh':v='../en.html?lang=en'
    a.append(k+'="'+html.escape(v,quote=True)+'"')
   self.parts.append('<'+tag+(' '+' '.join(a)if a else '')+'>')
  def handle_endtag(self,tag):self.parts.append('</'+tag+'>')
  def handle_data(self,s):self.parts.append(html.escape(t(s),quote=False))
  def handle_decl(self,s):self.parts.append('<!'+s+'>')
 p=Translator();p.feed((out/'index.html').read_text());s=''.join(p.parts).replace('◎ English','◎ 中文')
 # English download figures use billions, retaining the original values exactly.
 for old,new in [('11.5','1.15'),('7.23','0.723'),('1.63','0.163')]:s=s.replace('<b>'+old+'<small> ×100M</small>','<b>'+new+'<small> B</small>')
 def wrap(m):
  attrs,txt=m.groups();limit=10 if 'perspective-text'in attrs else 16
  if len(txt)<=limit or ' 'not in txt:return m[0]
  if not any(x in attrs for x in ['class="label"','perspective-text','class="center"','class="tiny"','network-subtitle','growth-subtitle']):return m[0]
  x=re.search(r'x="([^"]+)"',attrs)[1];y=float(re.search(r'y="([^"]+)"',attrs)[1]);words=txt.split();cut=min(range(1,len(words)),key=lambda i:abs(len(' '.join(words[:i]))-len(' '.join(words[i:]))))
  return f'<text{attrs}><tspan x="{x}" y="{y-7}">{" ".join(words[:cut])}</tspan><tspan x="{x}" y="{y+10}">{" ".join(words[cut:])}</tspan></text>'
 s=re.sub(r'<text([^>]*)>([^<]+)</text>',wrap,s)
 raw=(out/'data.js').read_text();deck=json.loads(raw.split('window.DECK=')[1].split(';\nwindow.SOURCES=')[0]);src=json.loads(raw.split('window.SOURCES=')[1].rstrip(';'))
 notes=json.loads((R/'en-notes.json').read_text())
 for i,item in enumerate(deck):
  item['title']=t(item['title']);item['notes']=notes[i];item['steps']=[[t(v)for v in pair]for pair in item['steps']]
 es=json.loads((R/'en-sources.json').read_text())
 for k,items in es.items():
  for i,item in enumerate(items):item['url']=src[k][i]['url']
  if k=='manifesto':items[0]['url']='https://www.x-lab.info/ai-for-all/en.html'
 if missing:raise ValueError('Untranslated strings: '+str(sorted(missing)))
 (out/'en.html').write_text(s)
 (out/'data-en.js').write_text('window.DECK='+json.dumps(deck,ensure_ascii=False)+';\nwindow.SOURCES='+json.dumps(es,ensure_ascii=False)+';')
 print('English slides, diagram labels, notes and sources built.')
if __name__=='__main__':build_english(R.parents[1]/'site/presentation')
