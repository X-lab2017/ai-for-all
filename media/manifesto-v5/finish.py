"""Mix the instrumental score and export the 104.4-second director's cut."""
import json
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
music = root / 'assets/user-score.mp3'
base = 'apad=whole_dur=104.4,atrim=duration=104.4,afade=t=in:d=0.15,afade=t=out:st=102.8:d=1.6'
measure = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(music), '-af', base + ',loudnorm=I=-16:TP=-1.5:LRA=14:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, check=True)
stats = json.loads(re.findall(r'\{[^{}]+\}', measure.stderr)[-1])
norm = f"loudnorm=I=-16:TP=-1.5:LRA=14:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true:print_format=json"
subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', str(music), '-af', base + ',' + norm, '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', str(root / 'music-master.wav')], check=True)
subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', str(root / 'visual.mp4'), '-i', str(root / 'music-master.wav'), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-t', '104.4', '-movflags', '+faststart', '-metadata', 'title=AI 普惠宣言 — 流畅精修版 V5', '-metadata', 'artist=X-lab AI', '-metadata', 'comment=Music: user-supplied instrumental recording. Original tempo and pitch; edge fades and loudness normalization.', str(root / 'AI-for-All-Manifesto-V5.mp4')], check=True)
