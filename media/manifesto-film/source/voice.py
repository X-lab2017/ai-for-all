import asyncio,json,os,ssl,subprocess
from pathlib import Path
import edge_tts,edge_tts.communicate
edge_tts.communicate._SSL_CTX=ssl.create_default_context()
root=Path(__file__).resolve().parents[3]
out=Path(os.environ.get('FILM_OUTPUT',str(root.parent/'video-build')));out.mkdir(exist_ok=True)
story=json.loads(Path(__file__).with_name('story.json').read_text())
captions=[]
async def main():
 offset=0
 for i,s in enumerate(story):
  p=out/f'voice-{i+1}.mp3'
  events=[]
  with p.open('wb') as audio:
   async for event in edge_tts.Communicate(s['voice'],'zh-CN-YunxiNeural',rate='+5%',boundary='WordBoundary').stream():
    if event['type']=='audio': audio.write(event['data'])
    elif event['type']=='WordBoundary': events.append(event)
  d=float(subprocess.check_output(['ffprobe','-v','quiet','-show_entries','format=duration','-of','csv=p=0',str(p)]))
  speed=max(1,d/(s['seconds']-.6))
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-af',f'atempo={speed},adelay=200|200,apad','-t',str(s['seconds']),'-ar','48000','-ac','2',str(out/f'segment-{i+1}.wav')],check=True)
  cur=''; begin=None; end=0
  for e in events:
   if begin is None: begin=e['offset']/1e7
   cur+=e['text'];end=(e['offset']+e['duration'])/1e7
   if len(cur)>=22:
    captions.append({'start':offset+.2+begin/speed,'end':offset+.2+end/speed,'text':cur});cur='';begin=None
  if cur: captions.append({'start':offset+.2+begin/speed,'end':offset+.2+end/speed,'text':cur})
  offset+=s['seconds']
  (out/'captions.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2))
  print(i+1,round(d,2),round(speed,3),flush=True)
 (out/'audio-list.txt').write_text(''.join(f"file '{out/f'segment-{i+1}.wav'}'\n" for i in range(10)))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(out/'audio-list.txt'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11',str(out/'narration.wav')],check=True)
asyncio.run(main())
