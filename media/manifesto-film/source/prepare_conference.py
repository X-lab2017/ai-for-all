"""Retain the v3 performance and processing; speed each chapter exactly 10%."""
import hashlib,json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get('FILM_OUTPUT',str(ROOT.parent/'conference-v5-build')))
SOURCE=Path(os.environ.get('V3_SOURCE',str(OUT/'source-v3')))
story=json.loads(Path(__file__).with_name('story.json').read_text())
source=SOURCE/'narration.wav'
if not source.exists(): source=SOURCE/'narration.flac'
captions=json.loads((SOURCE/'captions.json').read_text())
offset=0; revised=[]; chapters=[]
for i,s in enumerate(story):
    # The opening gains a short musical lead-in; all other chapter starts stay put.
    lead=.45 if i==0 else 0
    duration=s['seconds']
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-af',
        f'atrim=start={offset}:duration={duration},asetpts=PTS-STARTPTS,aresample=48000,atempo=1.10,adelay={round(lead*1000)}|{round(lead*1000)},apad',
        '-t',str(duration),'-ar','48000','-ac','2','-c:a','pcm_s24le',str(OUT/f'segment-{i+1:02}.wav')],check=True)
    group=[c for c in captions if offset<=c['start']<offset+duration]
    for c in group:
        a=offset+lead+(c['start']-offset)/1.1
        b=offset+lead+(c['end']-offset)/1.1
        assert a<b<=offset+duration, (i,a,b)
        revised.append(dict(start=a,end=b,text=c['text']))
    chapters.append(dict(chapter=i+1,start=offset,seconds=duration,tempo=1.1,extra_lead=lead,last_caption_end=revised[-1]['end']))
    offset+=duration
assert offset==90
assert all(a['end']<=b['start']+1e-6 for a,b in zip(revised,revised[1:]))
(OUT/'captions.json').write_text(json.dumps(revised,ensure_ascii=False,indent=2))
(OUT/'audio-list.txt').write_text(''.join(f"file '{OUT/f'segment-{i+1:02}.wav'}'\n" for i in range(10)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'audio-list.txt'),'-c:a','pcm_s24le',str(OUT/'narration.wav')],check=True)
def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
srt='\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(revised))+'\n'
(OUT/'AI-for-All-conference-v5.zh-CN.srt').write_text(srt)
(ROOT/'media/manifesto-film/AI-for-All.zh-CN.srt').write_text(srt)
(OUT/'timing-review.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_commit='8c20b95',speech_tempo=1.10,chapters=chapters,captions=len(revised)),indent=2))
print('v3 voice retained; 10 chapters at 1.10x; 23 captions; 90 seconds.')
