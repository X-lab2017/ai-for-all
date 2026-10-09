"""Dialogue-first mix. Supply the credited music file in FILM_OUTPUT."""
import os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[3]
out=Path(os.environ.get('FILM_OUTPUT',str(root.parent/'video-build')))
# Crop source music to 90 seconds; keep narration central and duck music under speech.
filters='[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[voice][key];[1:a]atrim=start=30:duration=90,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=6500,loudnorm=I=-29:TP=-9:LRA=7,afade=t=in:d=2.5,afade=t=out:st=86:d=4,aformat=sample_rates=48000:channel_layouts=stereo[music];[music][key]sidechaincompress=threshold=0.035:ratio=3:attack=100:release=850:makeup=1[bed];[voice][bed]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-18:TP=-2:LRA=9,aresample=48000[mix]'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out/'narration.wav'),'-i',str(out/'Light-Awash.mp3'),'-filter_complex',filters,'-map','[mix]','-t','90',str(out/'final-mix.wav')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out/'AI-for-All-90s-visual.mp4'),'-i',str(out/'final-mix.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-t','90','-movflags','+faststart',str(out/'AI-for-All-90s-1080p-audio-v2.mp4')],check=True)
