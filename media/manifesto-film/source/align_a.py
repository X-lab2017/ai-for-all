"""Check rendered speech with ASR and map authored subtitles to measured words.

Character matching bridges ASR spelling differences in names and homophones;
it is an estimate, not forced phoneme alignment. Inspect the review report.
"""
import difflib,json,os,subprocess,unicodedata
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
from opencc import OpenCC
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get('FILM_OUTPUT',str(ROOT.parent/'final-a-build')))
story=json.loads(Path(__file__).with_name('story.json').read_text())
timing=json.loads((OUT/'timing.json').read_text())
LINES=[
 ['让 AI 用得起，更用得好！','让每个人，都有创造未来的机会。'],
 ['三十五年，Linux 让我们看见：','开放协作，能够创造共同的基础。'],
 ['今天，Qwen、DeepSeek、GLM、Kimi 与混元，','正打开更多创造的可能。'],
 ['开源，降低门槛。','开发者，放大创造！','让技术，走进真实的生活。'],
 ['把创造变成共享的数字公共品。','让开放的成果，经过维护与采用，','成为真正的帮助。'],
 ['让贡献被看见，让支持有依据！','用数据与评价，','让每一步行动经得起检验。'],
 ['让贡献带来成长，让投入支持创造。','用数据与评价连接双轮，','让每一次行动，都推动下一次前进！'],
 ['从 OpenDigger、OpenRank 到 OpenShare，','把愿景落到实践，用行动检验承诺。'],
 ['分享一个需要，','贡献一个工具，','开放一个场景。'],
 ['让技术，成为机会！','让创造，惠及更多人！','加入我们。','现在——就一起行动！'],
]
_simplify=OpenCC('t2s')
def norm(s):
 s=_simplify.convert(unicodedata.normalize('NFKC',s)).lower().replace('35','三十五')
 return ''.join(c for c in s if c.isalnum())
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'

if __name__=='__main__':
 model=WhisperModel(os.environ.get('FILM_ASR_MODEL','small'),device='cpu',compute_type='int8',
    cpu_threads=int(os.environ.get('FILM_ASR_THREADS','6')),
    download_root=os.environ.get('FILM_ASR_CACHE',str(OUT/'asr-model')))
 captions=[];review=[]
 for i,(s,tm,lines) in enumerate(zip(story,timing,LINES),1):
  assert norm(''.join(lines))==norm(s['voice']),(i,lines,s['voice'])
  cache=OUT/f'asr-{i:02}.json'
  if cache.exists():parts=json.loads(cache.read_text())
  else:
   a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(OUT/f'spoken-{i:02}.wav'),'-ar','16000','-ac','1','-f','f32le','-']),np.float32)
   segs,_=model.transcribe(a,language='zh',beam_size=5,word_timestamps=True,vad_filter=False)
   parts=[{'text':seg.text,'words':[{'text':w.word,'start':w.start,'end':w.end,'p':w.probability} for w in seg.words]} for seg in segs]
   cache.write_text(json.dumps(parts,ensure_ascii=False,indent=2))
  found='';starts=[];ends=[]
  for p in parts:
   for w in p['words']:
    word=norm(w['text'])
    for j,ch in enumerate(word):
     found+=ch;starts.append(w['start']+(w['end']-w['start'])*j/len(word))
     ends.append(w['start']+(w['end']-w['start'])*(j+1)/len(word))
  target=norm(s['voice']);match=difflib.SequenceMatcher(None,target,found,autojunk=False)
  ta=np.full(len(target),np.nan);tb=np.full(len(target),np.nan)
  for a,b,n in match.get_matching_blocks():
   for j in range(n):ta[a+j]=starts[b+j];tb[a+j]=ends[b+j]
  known=np.flatnonzero(np.isfinite(ta))
  if len(known)<max(3,len(target)*.4):raise RuntimeError(f'Chapter {i}: insufficient transcript match, inspect audio.')
  ta=np.interp(np.arange(len(target)),known,ta[known]);tb=np.interp(np.arange(len(target)),known,tb[known])
  cursor=0;offset=tm['start']+tm['delay']
  for line in lines:
   n=len(norm(line));start=float(ta[cursor]);end=float(tb[cursor+n-1]);cursor+=n
   captions.append({'start':round(offset+max(0,start-.04),3),
    'end':round(offset+min(tm['spoken_seconds'],max(end,start+.25)+.10),3),'text':line})
  row={'chapter':i,'authored':s['voice'],'recognized':''.join(p['text'] for p in parts),
       'character_match':round(match.ratio(),3),'speed':tm['speed']}
  review.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
 for i in range(len(captions)-1):captions[i]['end']=min(captions[i]['end'],captions[i+1]['start']-.01)
 (OUT/'captions.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2))
 (OUT/'speech-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
 srt='\n\n'.join(f'{i}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(captions,1))+'\n'
 (ROOT/'media/manifesto-film/AI-for-All.zh-CN.srt').write_text(srt)
 (OUT/'AI-for-All-A-v4.zh-CN.srt').write_text(srt)
