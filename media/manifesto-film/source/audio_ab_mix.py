"""25-second auditions: edit on measured silence, preserve natural pitch/rate.

Inputs in FILM_OUTPUT: voice-{A,B}-raw.wav, Reign.mp3, Americana.mp3.
The cuts below correspond ONLY to the retained 2026-10-09 voice takes.
"""
import json, os, subprocess
from pathlib import Path
import numpy as np

OUT = Path(os.environ.get('FILM_OUTPUT', str(Path(__file__).resolve().parents[4] / 'audio-ab-build')))
SR, LENGTH = 48000, 25
STARTS = [1.0, 3.4, 5.8, 8.3, 12.2, 16.5, 19.0, 20.7]
TEXTS = ['分享一个需要', '贡献一个工具', '开放一个场景', '让技术，成为机会！',
         '让创造，惠及更多人！', '加入我们。', '现在——', '就一起行动！']
CONFIG = {
    'A': {'cuts':[0,1.9,3.87,5.58,8.72,12.06,13.59,14.99,16.64],
          'music':'Reign', 'music_start':101.2, 'name':'庄严磅礴'},
    'B': {'cuts':[0,1.31,2.87,4.58,7.51,10.29,11.61,12.80,14.24],
          'music':'Americana', 'music_start':155, 'name':'昂扬共创'},
}
def ff(args):
    return subprocess.run(['ffmpeg','-v','error','-y']+args, check=True)

def master(key, cfg):
    data = np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',
        str(OUT/f'voice-{key}-raw.wav'),'-ar',str(SR),'-ac','1','-f','f32le','-']), np.float32)
    timeline = np.zeros(SR*LENGTH, np.float32)
    captions=[]
    for i,(a,b) in enumerate(zip(cfg['cuts'],cfg['cuts'][1:])):
        clip=data[round(a*SR):round(b*SR)].copy()
        n=min(192,len(clip)//2)
        clip[:n]*=np.linspace(0,1,n);clip[-n:]*=np.linspace(1,0,n)
        start=round(STARTS[i]*SR)
        assert i==7 or STARTS[i]+len(clip)/SR<=STARTS[i+1]
        timeline[start:start+len(clip)]+=clip
        captions.append({'start':STARTS[i], 'end':STARTS[i]+len(clip)/SR,
                         'text':TEXTS[i]})
    raw=OUT/f'voice-{key}-edit.f32';timeline.tofile(raw)
    voice=OUT/f'voice-{key}-directed.wav'
    ff(['-f','f32le','-ar',str(SR),'-ac','1','-i',str(raw),'-af',
        'highpass=f=70,equalizer=f=175:t=q:w=0.8:g=1,equalizer=f=290:t=q:w=1:g=-1,acompressor=threshold=0.18:ratio=1.7:attack=18:release=180,loudnorm=I=-18:TP=-3:LRA=11',
        '-ar',str(SR),'-ac','2',str(voice)])
    # Respect the recorded musical crescendo; modest ducking protects speech.
    filt=(f'[0:a]asplit=2[v][key];[1:a]atrim=start={cfg["music_start"]}:duration=25,'
          'asetpts=PTS-STARTPTS,highpass=f=70,equalizer=f=2300:t=q:w=0.6:g=-2,'
          'loudnorm=I=-21:TP=-4:LRA=14,afade=t=in:d=0.65,afade=t=out:st=23.2:d=1.8,'
          'aformat=sample_rates=48000:channel_layouts=stereo[m];'
          '[m][key]sidechaincompress=threshold=0.045:ratio=3:attack=25:release=270[bed];'
          '[v][bed]amix=inputs=2:duration=first:normalize=0[out]')
    pre=OUT/f'mix-{key}-premaster.wav'
    ff(['-i',str(voice),'-i',str(OUT/(cfg['music']+'.mp3')),'-filter_complex',filt,'-map','[out]',
        '-t','25','-ar',str(SR),str(pre)])
    scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(pre),'-af',
        'loudnorm=I=-16:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    stats=json.loads(scan.stderr[scan.stderr.rfind('{'):])
    norm=('loudnorm=I=-16:TP=-2:LRA=11:linear=true:'
          f'measured_I={stats["input_i"]}:measured_TP={stats["input_tp"]}:'
          f'measured_LRA={stats["input_lra"]}:measured_thresh={stats["input_thresh"]}:'
          f'offset={stats["target_offset"]}')
    credit=f'{cfg["music"]} — Kevin MacLeod (incompetech.com), CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; excerpt / edit / mix'
    ff(['-i',str(pre),'-af',norm,'-ar',str(SR),'-c:a','pcm_s24le','-metadata','comment='+credit,
        str(OUT/f'AI-for-All-{key}-master.wav')])
    (OUT/f'captions-{key}.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2))
    print(key,'mastered',cfg['music'], 'last voice ends',round(captions[-1]['end'],2),flush=True)

if __name__=='__main__':
    for key,cfg in CONFIG.items(): master(key,cfg)
