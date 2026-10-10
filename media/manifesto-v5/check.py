import subprocess,json
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import zxingcpp
p=Path(__file__).parent;video=p/'AI-for-All-Manifesto-V5.mp4';cuts=[7,17.5,27,34,38,46.5,55,63.67,69.53,77.83,87.3,94.7]
# Whole-file decode and frame-to-frame luminance continuity across all cuts.
proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-vf','scale=320:180','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
diffs=[];prev=None
while True:
 raw=proc.stdout.read(320*180*3)
 if not raw:break
 assert len(raw)==320*180*3
 a=np.frombuffer(raw,np.uint8).astype(np.int16)
 if prev is not None:diffs.append(float(np.abs(a-prev).mean()))
 prev=a
err=proc.stderr.read().decode();assert proc.wait()==0 and not err,err
cutstats={str(c):round(max(diffs[max(0,int(c*30)-3):int((c+1)*30)]),3) for c in cuts}
print('Transition maximum adjacent-frame RGB changes /255:',cutstats)
# Export representative frames of every transition, not only steady scenes.
out=Image.new('RGB',(1280,12*205),'#ddd');d=ImageDraw.Draw(out)
for i,c in enumerate(cuts):
 for j,offset in enumerate([-.033,.25,.5,1.0]):
  t=c+offset;f=p/'preview'/f'transition-{i+1:02}-{j}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(f)],check=True)
  im=Image.open(f);im.thumbnail((320,180));out.paste(im,(j*320,i*205));d.text((j*320+5,i*205+183),f'{t:.2f}s',fill='black')
out.save(p/'preview/transitions.png')
f=p/'preview/ending.png';subprocess.run(['ffmpeg','-v','error','-y','-ss','100','-i',str(video),'-frames:v','1',str(f)],check=True)
qr=[r.text for r in zxingcpp.read_barcodes(Image.open(f))];assert 'https://www.x-lab.info/ai-for-all/' in qr
r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels','-of','json',str(video)],capture_output=True,text=True,check=True)
report={'media':json.loads(r.stdout),'transition_max_mean_pixel_changes':cutstats,'full_decode':'passed','qr':qr};(p/'quality.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['media']))
