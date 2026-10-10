"""Create a current-materials package without relabelling legacy binaries."""
from pathlib import Path
import zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';OUT=SITE/'launch/downloads'
files={
'manifesto/AI-for-All-v1.2-ZH.md':SITE/'AI-for-All-manifesto.md',
'manifesto/AI-for-All-v1.2-EN.md':SITE/'AI-for-All-manifesto-EN.md',
'manifesto/AI-for-All-Manifesto-v1.2-Designed-ZH.pdf':SITE/'downloads/AI-for-All-Manifesto-v1.2-Designed-ZH.pdf',
'film/AI-for-All-Manifesto-V5.mp4':SITE/'film/AI-for-All-Manifesto-V5.mp4',
'film/AI-for-All-Manifesto-V5-Source.zip':SITE/'film/AI-for-All-Manifesto-V5-Source.zip',
'presentation/notes-ZH.md':SITE/'presentation/narrative.md',
'qr/AI-for-All-Launch-QR.png':OUT/'AI-for-All-Launch-QR.png',
'qr/AI-for-All-Launch-QR.svg':OUT/'AI-for-All-Launch-QR.svg',
'NOTICE.md':ROOT/'NOTICE.md'}
readme='''# AI 普惠宣言 · 当前发布资料 / Current release materials

2026-10-10 · Manifesto v1.2 / Film V5

当前正文为 v1.2；影片 V5 为 104.4 秒、纯音乐、中文屏幕文字、无旁白。
The current film has Chinese on-screen text and no narration. No English-dubbed V5 is included.

主站 / Manifesto: https://www.x-lab.info/ai-for-all/
English: https://www.x-lab.info/ai-for-all/en.html
影片 / Film: https://www.x-lab.info/ai-for-all/film/
13 章网页演示 / 13-chapter web presentation: https://www.x-lab.info/ai-for-all/presentation/
English presentation: https://www.x-lab.info/ai-for-all/presentation/en.html
发布资料 / Release hub: https://www.x-lab.info/ai-for-all/launch/

PDF 为中文设计版；英文当前正文见 Markdown 或官网。演示为在线网页，本包提供讲述稿与访问链接。
The PDF is Chinese; current English text is in Markdown and online. The presentation is online; notes and links are included.

旧版 PPT、90 秒配音影片、英文 PDF、现场文稿和双飞轮全景仅保留在 v1.1 历史归档，不在本包中。
Legacy PowerPoints, narrated films, English PDF, event scripts and two-cycle diagrams are archived separately, not included here.

音乐与品牌使用范围见 NOTICE.md。Production source does not grant music reuse rights.
'''
data={n:p.read_bytes() for n,p in files.items()};data['README.txt']=readme.encode();checks=''.join(hashlib.sha256(b).hexdigest()+'  '+n+'\n' for n,b in data.items());data['SHA256SUMS.txt']=checks.encode()
with zipfile.ZipFile(OUT/'AI-for-All-v1.2-V5-Release.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in data.items():
  info=zipfile.ZipInfo('AI-for-All-v1.2-V5/'+n,date_time=(2026,10,10,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b)
(OUT/'SHA256SUMS-v1.2-V5.txt').write_text(checks+'\n# Package\n'+hashlib.sha256((OUT/'AI-for-All-v1.2-V5-Release.zip').read_bytes()).hexdigest()+'  AI-for-All-v1.2-V5-Release.zip\n')
print('Current release package built')
