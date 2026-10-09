"""90-second Reign edit and dialogue-first final mix for the selected A voice."""
import json,os,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(os.environ.get('FILM_OUTPUT',str(ROOT.parent/'final-a-build')))
def ff(args):return subprocess.run(['ffmpeg','-v','error','-y']+args,check=True)

# Two musical statements: opening piano into orchestra, then the final swell.
# 56 + 36 - 2 second equal-power crossfade = exactly 90 seconds.
music=('[0:a]asplit=2[a][b];[a]atrim=start=84:end=140,asetpts=PTS-STARTPTS[a1];'
       '[b]atrim=start=104:end=140,asetpts=PTS-STARTPTS[b1];'
       '[a1][b1]acrossfade=d=2:c1=qsin:c2=qsin,'
       'highpass=f=70,equalizer=f=2300:t=q:w=0.6:g=-2,'
       'loudnorm=I=-21:TP=-4:LRA=14,afade=t=in:d=1.1,afade=t=out:st=88:d=2,'
       'aresample=48000[m]')
ff(['-i',str(OUT/'Reign.mp3'),'-filter_complex',music,'-map','[m]','-t','90',str(OUT/'music-edit.wav')])
mix=('[0:a]asplit=2[v][key];[1:a][key]sidechaincompress=threshold=0.045:ratio=3:attack=25:release=270[bed];'
     '[v][bed]amix=inputs=2:duration=first:normalize=0[out]')
ff(['-i',str(OUT/'narration.wav'),'-i',str(OUT/'music-edit.wav'),'-filter_complex',mix,'-map','[out]',str(OUT/'premaster.wav')])
scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(OUT/'premaster.wav'),'-af',
 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
s=json.loads(scan.stderr[scan.stderr.rfind('{'):])
norm=('loudnorm=I=-16:TP=-2:LRA=11:linear=true:'
 f'measured_I={s["input_i"]}:measured_TP={s["input_tp"]}:measured_LRA={s["input_lra"]}:'
 f'measured_thresh={s["input_thresh"]}:offset={s["target_offset"]}')
credit='Reign — Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/; excerpts, crossfade, equalization, ducking, mix.'
ff(['-i',str(OUT/'premaster.wav'),'-af',norm,'-ar','48000','-ac','2','-c:a','pcm_s24le',
    '-metadata','comment='+credit,str(OUT/'AI-for-All-A-v4-master.wav')])
ff(['-i',str(OUT/'AI-for-All-90s-visual.mp4'),'-i',str(OUT/'AI-for-All-A-v4-master.wav'),
    '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-t','90','-movflags','+faststart',
    '-metadata','title=AI for All — Conference A v4',
    '-metadata','comment='+credit+' AI voice: original synthetic A voice, Qwen3-TTS. Speech tempo 1.15x.',
    str(OUT/'AI-for-All-90s-A-v4.mp4')])
print('Final A v4 mix and video complete.')
