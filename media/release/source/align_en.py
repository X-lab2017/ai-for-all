"""Local ASR check and approximate caption alignment to authored English text."""
import json,os,re,difflib,subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
OUT=Path(os.environ['RELEASE_BUILD'])/'en'
story=json.loads(Path(__file__).with_name('english-story.json').read_text());timing=json.loads((OUT/'timing.json').read_text())
model=WhisperModel(os.environ['LOCAL_ASR_MODEL'],device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
norm=lambda s:''.join(c for c in s.lower() if c.isalnum())
caps=[];review=[]
for i,(s,tm) in enumerate(zip(story,timing),1):
 cache=OUT/f'asr-{i:02}.json'
 if cache.exists():parts=json.loads(cache.read_text())
 else:
  a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(OUT/f'spoken-{i:02}.wav'),'-ar','16000','-ac','1','-f','f32le','-']),np.float32)
  segs,_=model.transcribe(a,language='en',beam_size=5,word_timestamps=True,vad_filter=False)
  parts=[dict(text=seg.text,words=[dict(text=w.word,start=w.start,end=w.end) for w in seg.words]) for seg in segs]
  cache.write_text(json.dumps(parts,indent=2))
 found='';starts=[];ends=[]
 for part in parts:
  for w in part['words']:
   n=norm(w['text'])
   for j,c in enumerate(n):found+=c;starts.append(w['start']+(w['end']-w['start'])*j/len(n));ends.append(w['start']+(w['end']-w['start'])*(j+1)/len(n))
 target=norm(s['voice']);m=difflib.SequenceMatcher(None,target,found,autojunk=False);ta=np.full(len(target),np.nan);tb=ta.copy()
 for a,b,n in m.get_matching_blocks():
  for j in range(n):ta[a+j]=starts[b+j];tb[a+j]=ends[b+j]
 known=np.flatnonzero(np.isfinite(ta))
 if len(known)<len(target)*.6:raise RuntimeError(f'Chapter {i}: speech requires review')
 ta=np.interp(np.arange(len(target)),known,ta[known]);tb=np.interp(np.arange(len(target)),known,tb[known])
 chunks=re.findall(r'[^.!?]+[.!?]?',s['voice']);lines=[]
 for chunk in chunks:
  chunk=chunk.strip()
  if len(chunk)>100:
   words=chunk.split();cur=''
   for w in words:
    if len(cur+' '+w)>85:lines.append(cur);cur=''
    cur+=((' ' if cur else '')+w)
   if cur:lines.append(cur)
  elif chunk:lines.append(chunk)
 pos=0
 for line in lines:
  n=len(norm(line));start=ta[pos];end=tb[pos+n-1];pos+=n
  caps.append(dict(start=round(tm['start']+tm['delay']+max(0,start-.04),3),end=round(tm['start']+tm['delay']+min(tm['spoken_seconds'],max(end,start+.3)+.1),3),text=line))
 row=dict(chapter=i,authored=s['voice'],recognized=''.join(p['text'] for p in parts),character_match=round(m.ratio(),3));review.append(row);print(json.dumps(row),flush=True)
for a,b in zip(caps,caps[1:]):a['end']=min(a['end'],b['start']-.01)
(OUT/'captions.json').write_text(json.dumps(caps,indent=2));(OUT/'speech-review.json').write_text(json.dumps(review,indent=2))
