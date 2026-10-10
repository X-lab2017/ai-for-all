"""Publication boundary: keep unaligned release materials in Git, off the website."""
from pathlib import Path
import shutil,re
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'site';OUT=ROOT/'.publish-site'
if OUT.exists():shutil.rmtree(OUT)
shutil.copytree(SOURCE,OUT,ignore=lambda directory,names:['launch'] if Path(directory)==SOURCE else [])
# Historical main pages also must not advertise the suspended release area.
for p in OUT.rglob('*.html'):
 s=p.read_text()
 s=re.sub(r'''<a\b[^>]*href=["']([^"']*)["'][^>]*>.*?</a>''',lambda m:'' if 'launch/' in m[1] else m[0],s,flags=re.S)
 p.write_text(s)
launch=OUT/'launch';launch.mkdir()
for en in [False,True]:
 t=lambda z,e:e if en else z;home='../en.html?lang=en' if en else '../index.html?lang=zh';filename='en.html' if en else 'index.html'
 page=f'''<!doctype html><html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>{t('发布资料暂未开放','Release materials temporarily unavailable')}</title><script src="../preferences.js"></script><link rel="stylesheet" href="../manifesto.css"><style>main{{max-width:760px;margin:14vh auto;padding:32px}}h1{{font-size:clamp(28px,5vw,44px);line-height:1.3}}p{{line-height:1.8;color:var(--muted)}}nav{{display:flex;gap:26px;flex-wrap:wrap;margin-top:36px}}nav a{{text-decoration:underline;text-underline-offset:6px}}</style></head><body><main><p>X-LAB AI · AI FOR ALL</p><h1>{t('发布资料暂未开放','Release materials temporarily unavailable')}</h1><p>{t('资料正在统一与校对，完成后将重新开放。您可以继续阅读宣言、观看影片或浏览互动演示。','The materials are being aligned and reviewed. Meanwhile, you can read the manifesto, watch the film or explore the presentation.')}</p><nav><a href="{home}">{t('宣言正文','Manifesto')}</a><a href="../film/{filename}?lang={'en' if en else 'zh'}">{t('宣言影片','Film')}</a><a href="../presentation/{filename}?lang={'en' if en else 'zh'}">{t('互动演示','Presentation')}</a></nav></main></body></html>'''
 (launch/filename).write_text(page)
assert sorted(p.name for p in launch.iterdir())==['en.html','index.html']
for folder in ['', 'film/', 'presentation/']:
 for filename in ['index.html','en.html']:
  s=(OUT/folder/filename).read_text();assert not re.search(r'href=["\'][^"\']*launch/',s),(folder,filename)
print('Public site staged: release column, archive pages and downloads withheld; source retained')
