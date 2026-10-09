"""Preserve v3 Heroic Age edit and balance, duck against the 1.10x voice."""
import json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get('FILM_OUTPUT',str(ROOT.parent/'conference-v5-build')))
def ff(args):subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)
filters=('[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[voice][key];'
 '[1:a]atrim=start=7:duration=90,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=10000,'
 'loudnorm=I=-24:TP=-6:LRA=7,afade=t=in:d=0.8,afade=t=out:st=88.5:d=1.5,'
 "volume='if(lt(t,16),0.72,if(lt(t,51),0.9,if(lt(t,78),1.1,1.35)))':eval=frame,"
 'aformat=sample_rates=48000:channel_layouts=stereo[music];'
 '[music][key]sidechaincompress=threshold=0.04:ratio=2.2:attack=45:release=400:makeup=1[bed];'
 '[voice][bed]amix=inputs=2:normalize=0:duration=first,aresample=48000[mix]')
ff(['-i',str(OUT/'narration.wav'),'-i',str(OUT/'Heroic-Age.mp3'),'-filter_complex',filters,'-map','[mix]',
    '-t','90','-c:a','pcm_s24le',str(OUT/'premaster.wav')])
scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(OUT/'premaster.wav'),'-af',
    'loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
s=json.loads(scan.stderr[scan.stderr.rfind('{'):])
norm=('loudnorm=I=-16:TP=-2:LRA=9:linear=true:'
 f'measured_I={s["input_i"]}:measured_TP={s["input_tp"]}:measured_LRA={s["input_lra"]}:'
 f'measured_thresh={s["input_thresh"]}:offset={s["target_offset"]}')
credit='Heroic Age — Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/; excerpt, equalization, ducking, mix.'
ff(['-i',str(OUT/'premaster.wav'),'-af',norm,'-ar','48000','-ac','2','-c:a','pcm_s24le',
    '-metadata','comment='+credit,str(OUT/'AI-for-All-EN-master.wav')])
ff(['-i',str(OUT/'AI-for-All-90s-visual.mp4'),'-i',str(OUT/'AI-for-All-EN-master.wav'),
    '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-t','90','-movflags','+faststart',
    '-metadata','title=AI for All — English Conference Film',
    '-metadata','comment='+credit+' AI voice: local Qwen3-TTS Base, English, using synthetic v3 voice as reference. Chapter pacing is measured.',
    str(OUT/'AI-for-All-90s-EN.mp4')])
print('English release mix complete: Heroic Age, 90 seconds.')
