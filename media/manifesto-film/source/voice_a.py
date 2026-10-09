"""Extend the user-selected synthetic A voice to the complete film.

Inputs: reference-A.wav (original Qwen VoiceDesign audition, not a real person).
Retain raw takes for exact restoration; regeneration can differ across runtimes.
"""
import hashlib,json,os,subprocess,time
from pathlib import Path
import torch,soundfile as sf
from qwen_tts import Qwen3TTSModel

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get('FILM_OUTPUT',str(ROOT.parent/'final-a-build')))
OUT.mkdir(exist_ok=True,parents=True)
REFERENCE_TEXT='分享一个需要，贡献一个工具，开放一个场景。让技术，成为机会！让创造，惠及更多人！加入我们。现在——就一起行动！'
EXPECTED='2c9c48caf95b73145b20001e31c32a90dc5dad030be0418970bd6141e374a25a'

if __name__=='__main__':
 ref=OUT/'reference-A.wav'
 assert hashlib.sha256(ref.read_bytes()).hexdigest()==EXPECTED,'Use the approved A voice reference.'
 story=json.loads(Path(__file__).with_name('story.json').read_text())
 torch.set_num_threads(int(os.environ.get('FILM_CPU_THREADS','8')))
 torch.set_num_interop_threads(1)
 print('Loading local Qwen Base model',flush=True)
 model=Qwen3TTSModel.from_pretrained(str(OUT/'qwen-base-model'),device_map='cpu',
                  dtype=torch.bfloat16,attn_implementation='sdpa')
 print('Encoding approved A voice reference',flush=True)
 prompt=model.create_voice_clone_prompt(ref_audio=str(ref),ref_text=REFERENCE_TEXT,x_vector_only_mode=False)
 for i,s in enumerate(story[:8],1):
  target=OUT/f'raw-{i:02}.wav'
  if target.exists():
   print(i,'using retained take',flush=True);continue
  print(i,'generating',flush=True);started=time.monotonic()
  torch.manual_seed(20261009+i)
  wavs,sr=model.generate_voice_clone(text=s['voice'],language='Chinese',voice_clone_prompt=prompt,
                  non_streaming_mode=True,max_new_tokens=360)
  sf.write(str(target),wavs[0],sr)
  d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(target)]))
  print(i,'raw seconds',d,'at 1.15x',round(d/1.15,3),'generation seconds',round(time.monotonic()-started),flush=True)
 # Preserve the user's exact selected performance in the closing two chapters.
 for i,start,duration in [(9,0,5.58),(10,5.58,11.06)]:
  target=OUT/f'raw-{i:02}.wav'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(ref),'-ss',str(start),'-t',str(duration),
                  '-c:a','pcm_s16le',str(target)],check=True)
 print('All ten raw chapters ready.',flush=True)
