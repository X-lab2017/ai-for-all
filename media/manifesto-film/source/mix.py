"""Dialogue-first mix. Supply the credited music file in FILM_OUTPUT."""
import os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[3]
out=Path(os.environ.get('FILM_OUTPUT',str(root.parent/'video-build')))
# Crop source music to 90 seconds; keep narration central and duck music under speech.
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[voice][key];[1:a]atrim=start=7:duration=90,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=10000,loudnorm=I=-24:TP=-6:LRA=7,afade=t=in:d=0.8,afade=t=out:st=88.5:d=1.5,volume='if(lt(t,16),0.72,if(lt(t,51),0.9,if(lt(t,78),1.1,1.35)))':eval=frame,aformat=sample_rates=48000:channel_layouts=stereo[music];[music][key]sidechaincompress=threshold=0.04:ratio=2.2:attack=45:release=400:makeup=1[bed];[voice][bed]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-2:LRA=9,aresample=48000[mix]"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out/'narration.wav'),'-i',str(out/'Heroic-Age.mp3'),'-filter_complex',filters,'-map','[mix]','-t','90',str(out/'final-mix.wav')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out/'AI-for-All-90s-visual.mp4'),'-i',str(out/'final-mix.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-t','90','-movflags','+faststart',str(out/'AI-for-All-90s-conference-v3.mp4')],check=True)
