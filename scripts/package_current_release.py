"""Deterministic packages of the four approved editions, never legacy material."""
from pathlib import Path
import zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';HUB=SITE/'launch';OUT=HUB/'downloads'
def zipfiles(dest,files):
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,b in sorted(files.items()):
   i=zipfile.ZipInfo(name,date_time=(2026,10,11,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b)
def checksum(files):return ''.join(hashlib.sha256(b).hexdigest()+'  '+n+'\n' for n,b in sorted(files.items()))
# Current web presentation, with its shared UI assets and absolute cross-section links.
presentation={}
for p in (SITE/'presentation').rglob('*'):
 if p.is_file() and p.suffix in ['.html','.js','.css','.svg','.png','.jpg','.webp']:
  data=p.read_bytes()
  if p.suffix=='.html':
   import re
   s=data.decode();s=re.sub(r'href="\.\./((?:index|en)\.html|film/[^\"]*|launch/[^\"]*)',r'href="https://www.x-lab.info/ai-for-all/\1',s);data=s.encode()
  presentation['presentation/'+str(p.relative_to(SITE/'presentation'))]=data
for name in ['navigation.css','navigation.js','preferences.js','assets/brand.svg','assets/brand-dark.svg']:
 presentation[name]=(SITE/name).read_bytes()
presentation['README.txt']='打开 presentation/index.html（中文）或 presentation/en.html（English）。完整 13 章网页演示；外部链接与来源需联网。\nOpen either HTML file in a browser. External links and sources require internet access.\n'.encode()
zipfiles(OUT/'AI-for-All-Presentation.zip',presentation)
visuals={'visuals/'+p.name:p.read_bytes() for p in (HUB/'assets').iterdir() if p.suffix in ['.png','.svg']}
for name in ['NotoSansSC-Regular.ttf','NotoSansSC-SemiBold.ttf','OFL.txt']:
 visuals['fonts/'+name]=(ROOT/'media/manifesto-v5/assets'/name).read_bytes()
visuals['NOTICE.md']=(ROOT/'NOTICE.md').read_bytes()
visuals['README.txt']='视觉定稿 · 2026-10-11。cover-wide / share-square / share-poster / framework-strip 为已确认图稿；film-cover 为 V5 第 5 秒画面；panorama 为当前 13 章演示第 12 页；social-preview 为封面的适配版；manifesto-qr 指向宣言主站。SVG 编辑需安装随包 Noto Sans SC 字体。\n'.encode()
zipfiles(OUT/'AI-for-All-Visuals.zip',visuals)
files={
 '01-manifesto/AI-for-All-v1.2-ZH.md':(SITE/'AI-for-All-manifesto.md').read_bytes(),
 '01-manifesto/AI-for-All-v1.2-EN.md':(SITE/'AI-for-All-manifesto-EN.md').read_bytes(),
 '01-manifesto/AI-for-All-Manifesto-v1.2-Designed-ZH.pdf':(SITE/'downloads/AI-for-All-Manifesto-v1.2-Designed-ZH.pdf').read_bytes(),
 '03-film/AI-for-All-Manifesto-V5.mp4':(SITE/'film/AI-for-All-Manifesto-V5.mp4').read_bytes(),
 'NOTICE.md':(ROOT/'NOTICE.md').read_bytes()}
files.update({'02-presentation/'+n:b for n,b in presentation.items()})
for n in ['article.txt','companion.txt','AI-for-All-Publication.docx','AI-for-All-Publication.pdf']:files['04-publication/'+n]=(OUT/n).read_bytes()
files.update({'05-visuals/'+n:b for n,b in visuals.items()})
files['README.txt']='''AI 普惠宣言 · 正式发布资料 · 2026-10-11

01 宣言全文：v1.2 中英文 Markdown、中文设计版 PDF。
02 互动演示：已定稿 13 章中英文网页演示。打开 presentation/index.html；外部来源需联网。
03 宣言影片：V5，104.4 秒，1080p / 30fps，中文屏幕文字，纯音乐，无旁白。
04 宣言推文：2026-10-11 用户确认定稿的中文长文及配套转发文案。
05 视觉素材：封面、分享卡、二维码海报、框架概览、V5 影片封面、当前全景图、网页分享图、独立主站二维码。

主站：https://www.x-lab.info/ai-for-all/
演示：https://www.x-lab.info/ai-for-all/presentation/
影片：https://www.x-lab.info/ai-for-all/film/
推文：https://www.x-lab.info/ai-for-all/launch/article.html?lang=zh
发布资料：https://www.x-lab.info/ai-for-all/launch/

本包只含四项新定稿及配套视觉，不含讲稿、旧 PPT、旧影片或旧框架图。
素材使用遵循 NOTICE.md；字体许可见随包 OFL.txt。
'''.encode()
files['SHA256SUMS.txt']=checksum(files).encode();zipfiles(OUT/'AI-for-All-Release-2026-10-11.zip',files)
checks={p.name:p.read_bytes() for p in OUT.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt'}
(OUT/'SHA256SUMS.txt').write_text(checksum(checks))
print('Packaged four approved editions, web presentation and new visuals')
