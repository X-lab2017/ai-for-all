"""Prepare measured English speech, retain room for the closing panorama."""
import json,os,subprocess
from pathlib import Path
OUT=Path(os.environ['RELEASE_BUILD'])/'en'
story=json.loads(Path(__file__).with_name('english-story.json').read_text());offset=0;timing=[]
for i,s in enumerate(story,1):
 p=OUT/f'raw-{i:02}.wav';d=float(subprocess.check_output(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',str(p)]))
 lead=.45 if i==1 else .2
 speed=max(1.03,d/(s['seconds']-lead-.4))
 if speed>1.18:raise RuntimeError(f'Chapter {i} needs a shorter script: duration {d}, tempo {speed}')
 spoken=OUT/f'spoken-{i:02}.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-af',f'atempo={speed}','-ar','48000','-ac','2',str(spoken)],check=True)
 sd=float(subprocess.check_output(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',str(spoken)]))
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(spoken),'-af',f'adelay={int(lead*1000)}|{int(lead*1000)},apad','-t',str(s['seconds']),str(OUT/f'segment-{i:02}.wav')],check=True)
 timing.append(dict(chapter=i,start=offset,delay=lead,raw_seconds=d,spoken_seconds=sd,speed=speed));offset+=s['seconds']
(OUT/'timing.json').write_text(json.dumps(timing,indent=2))
(OUT/'audio-list.txt').write_text(''.join(f"file '{OUT/f'segment-{i:02}.wav'}'\n" for i in range(1,11)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'audio-list.txt'),'-af','highpass=f=65,equalizer=f=160:t=q:w=0.8:g=1.5,equalizer=f=300:t=q:w=1:g=-1,acompressor=threshold=0.125:ratio=2.5:attack=15:release=160:makeup=1,loudnorm=I=-17:TP=-2:LRA=9','-ar','48000',str(OUT/'narration.wav')],check=True)
print(json.dumps(timing,indent=2))
