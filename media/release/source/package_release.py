"""Write portable subtitle files and the complete offline release ZIP."""
from pathlib import Path
import json, zipfile, hashlib
ROOT=Path(__file__).resolve().parents[3]
S=Path(__file__).parent
OUT=ROOT/'site/launch/downloads'

def ts(n,sep):
    ms=round(n*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
    return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'
for key in ['ZH','EN','Bilingual']:
    rows=json.loads((S/f'captions-{key}.json').read_text())
    for ext,sep in [('srt',','),('vtt','.')]:
        pieces=['WEBVTT\n'] if ext=='vtt' else []
        for i,r in enumerate(rows):
            assert 0<=r['start']<r['end']<=90
            if i:assert rows[i-1]['end']<=r['start']+.001
            text=r['text']+('\n'+r['en'] if key=='Bilingual' else '')
            pieces.append(f'{i+1}\n{ts(r["start"],sep)} --> {ts(r["end"],sep)}\n{text}\n')
        (OUT/f'AI-for-All-90s-{key}.{ext}').write_text('\n'.join(pieces))
with zipfile.ZipFile(OUT/'AI-for-All-Captions.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):
        if f.suffix in ['.srt','.vtt']:z.write(f,f.name)

credits='''AI FOR ALL MANIFESTO - RELEASE 1
X-lab AI - 9 October 2026
https://www.x-lab.info/ai-for-all/launch/

MUSIC
"Heroic Age" - Kevin MacLeod (incompetech.com)
Licensed under Creative Commons Attribution 4.0
https://creativecommons.org/licenses/by/4.0/
Source: https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100848
Changes: excerpt (00:07-01:37), equalization, ducking, level changes and mix.
Keep this attribution with public redistributions of the films.
The original production record includes a past automated copyright claim report:
https://incompetech.com/wordpress/2025/04/whats-going-on-with-spotify/

AI NARRATION
Chinese: approved conference-v5 soundtrack, based on Microsoft synthetic voice
zh-CN-YunjianNeural. Narration is 1.10 times the speed in conference-v3.
English: locally generated Qwen/Qwen3-TTS-12Hz-1.7B-Base, using the synthetic
v3 voice as a reference. No real person's voice was supplied or impersonated.
Generation and timing records: media/release/source/ in the repository.
The English version uses measured chapter pacing, not a claim of a uniform
ten-percent speed change relative to a pre-existing English recording.
The prior production note requires the producer to confirm the original
Chinese speech service's use terms for the intended event and distribution.
This package does not grant rights beyond the respective source terms.

VISUALS
X-lab AI brand: https://github.com/X-lab2017/xlab-ai-brand
Linux anniversary and the five model identities retain their original sources:
https://www.x-lab.info/ai-for-all/presentation/assets/SOURCES.md
The examples do not indicate sponsorship, partnership or endorsement.

CONTENT AND BRAND PERMISSIONS
Manifesto, translations and diagrams: X-lab AI.
No blanket open-content license is granted by this release package.
https://github.com/X-lab2017/ai-for-all/blob/main/NOTICE.md
Original website code and generation scripts: MIT, see LICENSE-CODE.

SPEAKING MATERIALS
The Chinese manifesto is authoritative. Speaking scripts are event adaptations.
The package does not announce that a named conference has taken place or
that any conference organizer or international organization endorses it.
'''
(OUT/'CREDITS.txt').write_text(credits)
(OUT/'README.txt').write_text('''AI 普惠宣言正式发布包 / AI for All Launch Package
Release 1 - 2026-10-09
统一入口 / Launch page: https://www.x-lab.info/ai-for-all/launch/
English: https://www.x-lab.info/ai-for-all/launch/en.html

先阅读 AI-for-All-Conference-Handbook.pdf 或可编辑 Word 版本。
Start with AI-for-All-Conference-Handbook.pdf or the editable Word edition.

影片 / FILMS
AI-for-All-90s-ZH.mp4: 已定稿 conference-v5，中文配音及字幕。
AI-for-All-90s-Bilingual.mp4: 中文画面和配音，中英双语字幕。
AI-for-All-90s-EN.mp4: 英文画面、配音与字幕。
All three: 90 seconds, 1920 x 1080, 30 fps, H.264/AAC stereo.
Subtitles are burned in. Sidecar SRT and VTT are for adaptation.

演示 / PRESENTATIONS
AI-for-All-Conference-ZH.pptx and AI-for-All-Conference-EN.pptx
10 slides each, with editable text/diagrams and speaker notes.
The font is Source Han Sans SC. Install it if your system substitutes fonts.
https://github.com/adobe-fonts/source-han-sans
AI-for-All-Panoramas.pdf provides a portable framework display.

宣言 / MANIFESTO
AI-for-All-Manifesto-ZH.pdf and AI-for-All-Manifesto-EN.pdf
The full v1.1 manifesto, including five diagrams. Chinese is authoritative.

会场邀请 / PARTICIPATION
AI-for-All-Launch-QR-Display.pdf: widescreen bilingual invitation.
AI-for-All-Launch-QR.png / .svg: fixed launch-page QR code.
The page provides download and participation routes. Opening it sends no
registration. Posting a proposal on GitHub requires an account.

Copy the package to the venue computer before the event. Play the selected
film through its closing music, then show the panorama or QR display.
Keep CREDITS.txt and NOTICE.md with any redistribution of this package.
SHA256SUMS.txt records the file checksums.
''')
for filename in ['NOTICE.md','LICENSE-CODE']:
    (OUT/filename).write_bytes((ROOT/filename).read_bytes())
files=sorted(f for f in OUT.iterdir() if f.is_file() and f.name not in ['AI-for-All-Launch-Package.zip','SHA256SUMS.txt'])
(OUT/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in files))
with zipfile.ZipFile(OUT/'AI-for-All-Launch-Package.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files+[OUT/'SHA256SUMS.txt']:z.write(f,'AI-for-All-Launch-Package/'+f.name)
print('Packaged',len(files)+1,'files.')
