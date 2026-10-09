"""Local English narration using the approved v3 synthetic voice as reference."""
import os,json,time,subprocess,hashlib
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
import torch,soundfile as sf
from qwen_tts import Qwen3TTSModel
OUT=Path(os.environ['RELEASE_BUILD'])/'en';OUT.mkdir(parents=True,exist_ok=True)
MODEL=Path(os.environ['QWEN_LOCAL_MODEL'])
REF=OUT/'reference-v3.wav'
SOURCE=Path(os.environ['V3_REFERENCE_SOURCE'])
REF_TEXT='让 AI 用得起，更用得好！让每个人，都有创造未来的机会。'
story=json.loads(Path(__file__).with_name('english-story.json').read_text())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(SOURCE),'-ss','0.2','-t','6.1','-ar','24000','-ac','1',str(REF)],check=True)
torch.set_num_threads(8);torch.set_num_interop_threads(1)
print('Loading offline model',flush=True)
m=Qwen3TTSModel.from_pretrained(str(MODEL),device_map='cpu',dtype=torch.bfloat16,attn_implementation='sdpa')
prompt=m.create_voice_clone_prompt(ref_audio=str(REF),ref_text=REF_TEXT,x_vector_only_mode=False)
for i,s in enumerate(story,1):
 p=OUT/f'raw-{i:02}.wav'
 if p.exists():print(i,'retained',flush=True);continue
 torch.manual_seed(20261019+i);start=time.monotonic();print(i,'generating',flush=True)
 wav,sr=m.generate_voice_clone(text=s['voice'],language='English',voice_clone_prompt=prompt,non_streaming_mode=True,max_new_tokens=440)
 sf.write(p,wav[0],sr)
 print(i,len(wav[0])/sr,'seconds; generation',round(time.monotonic()-start),flush=True)
(OUT/'voice-provenance.json').write_text(json.dumps(dict(model='Qwen/Qwen3-TTS-12Hz-1.7B-Base',revision='fd4b254389122332181a7c3db7f27e918eec64e3',reference='v3 synthetic voice, not a real person',reference_text=REF_TEXT,reference_sha256=hashlib.sha256(REF.read_bytes()).hexdigest(),language='English',seed_base=20261019,offline=True),ensure_ascii=False,indent=2))
