"""Apply the requested 15% faster delivery, without raising voice pitch."""
import json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get('FILM_OUTPUT',str(ROOT.parent/'final-a-build')))
SPEED=1.15
story=json.loads(Path(__file__).with_name('story.json').read_text())
timing=[];offset=0
for i,s in enumerate(story,1):
 raw=OUT/f'raw-{i:02}.wav'
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(raw)]))
 spoken=OUT/f'spoken-{i:02}.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-af',f'atempo={SPEED}',
                 '-ar','48000','-ac','1',str(spoken)],check=True)
 actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(spoken)]))
 delay=.28
 if actual+delay>s['seconds']-.12:
  raise RuntimeError(f'Chapter {i} needs {actual+delay:.2f}s, available {s["seconds"]}s. Adjust chapter allocation; do not cut words or change speed.')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(spoken),'-af',f'adelay={round(delay*1000)},apad',
                  '-t',str(s['seconds']),'-ar','48000','-ac','2',str(OUT/f'segment-{i:02}.wav')],check=True)
 timing.append({'chapter':i,'start':offset,'seconds':s['seconds'],'delay':delay,'raw_seconds':duration,
                'spoken_seconds':actual,'speed':SPEED})
 offset+=s['seconds']
assert offset==90,offset
(OUT/'timing.json').write_text(json.dumps(timing,indent=2))
(OUT/'segments.txt').write_text(''.join(f"file '{OUT/f'segment-{i:02}.wav'}'\n" for i in range(1,11)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'segments.txt'),'-af',
 'highpass=f=70,equalizer=f=175:t=q:w=0.8:g=1,equalizer=f=290:t=q:w=1:g=-1,acompressor=threshold=0.18:ratio=1.7:attack=18:release=180,loudnorm=I=-18:TP=-3:LRA=11',
 '-ar','48000','-ac','2',str(OUT/'narration.wav')],check=True)
print(json.dumps(timing,indent=2))
