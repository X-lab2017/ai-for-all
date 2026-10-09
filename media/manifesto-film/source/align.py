# Preserve authored punctuation; interpolate clause boundaries within measured speech groups.
import json,re,os
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=Path(os.environ.get('FILM_OUTPUT',str(root.parent/'video-build')))
raw=json.loads((out/'captions.json').read_text());story=json.loads(Path(__file__).with_name('story.json').read_text());final=[];offset=0
norm=lambda s:re.sub(r'[^\w]','',s)
for s in story:
 groups=[c for c in raw if offset<=c['start']<offset+s['seconds']];spans=[];n=0
 for c in groups:
  z=len(norm(c['text']));spans.append((n,n+z,c['start'],c['end']));n+=z
 clauses=re.findall(r'[^，。；]+[，。；]?',s['voice']);parts=[];cur=''
 for q in clauses:
  if len(cur+q)>26 and len(cur)>5:parts.append(cur);cur=''
  cur+=q
  if cur.endswith('。'):parts.append(cur);cur=''
 if cur:parts.append(cur)
 def tm(pos,end=False):
  for a,b,x,y in spans:
   if a<=pos<=b:return x+(y-x)*(pos-a)/max(1,b-a)
  return spans[-1][3]
 pos=0
 for p in parts:
  end=pos+len(norm(p));final.append({'start':tm(pos),'end':tm(end,True),'text':p});pos=end
 offset+=s['seconds']
(out/'captions.json').write_text(json.dumps(final,ensure_ascii=False,indent=2))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
srt='\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(final))+'\n'
(root/'media/manifesto-film/AI-for-All.zh-CN.srt').write_text(srt)
