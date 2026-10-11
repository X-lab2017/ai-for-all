"""Publish the approved V5 film and keep related navigation reproducible."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'; OUT=SITE/'film'; OUT.mkdir(exist_ok=True)
cuts=[0,7,17.5,27,34,38,46.5,55,63.666667,69.533333,77.833333,87.3,94.7]
zh=['共同愿景','完整主张','一心普惠','二力相生','数字公共品','数据飞轮','人才飞轮','价值飞轮','三飞轮同屏','万千可能','生生不息','五层全景','共建邀请']
en=['Shared vision','Our commitment','One shared purpose','Two forces','Digital public goods','Data flywheel','Talent flywheel','Value flywheel','Three flywheels together','Possibilities','Continuous renewal','Five-layer panorama','Join us']
for english in [False,True]:
 lang='en' if english else 'zh'; t=lambda a,b:b if english else a; home='../en.html?lang=en' if english else '../?lang=zh'
 chapters=''.join(f'<button type="button" data-time="{v}"><small>{int(v)//60:02}:{int(v)%60:02}</small> {label}</button>' for v,label in zip(cuts,en if english else zh))
 page=f'''<!doctype html><html lang="{'en' if english else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#143b30"><title>{t('AI 普惠宣言 · 影片 V5','AI for All · Film V5')}</title><meta name="description" content="{t('AI 普惠宣言 v1.2 审定影片：104.4 秒，纯音乐与几何叙事。','The approved v1.2 manifesto film: 104.4 seconds of music and geometric storytelling.')} "><link rel="canonical" href="https://www.x-lab.info/ai-for-all/film/{'en.html' if english else ''}"><script src="../preferences.js"></script><link rel="stylesheet" href="../manifesto.css"><link rel="stylesheet" href="film.css"></head><body><a class="skip" href="#main">{t('跳至影片','Skip to film')}</a><header class="site-header"><a class="brand" href="{home}"><img class="brand-light" src="../assets/brand.svg" alt="X-lab AI" width="146" height="44"><img class="brand-dark" src="../assets/brand-dark.svg" alt="" width="146" height="44"></a><div class="header-actions"><a href="{home}">{t('宣言主站','Manifesto')}</a><a href="../presentation/{'en.html' if english else ''}?lang={lang}">{t('互动演示','Presentation')}</a><a href="{'index.html?lang=zh' if english else 'en.html?lang=en'}">{t('English','中文')}</a><button id="theme" type="button" aria-pressed="false">{t('切换主题','Switch theme')}</button></div></header><main id="main" class="shell film-main"><span class="eyebrow">AI FOR ALL · MANIFESTO v1.2 / FILM V5</span><h1>{t('AI 普惠宣言','AI for All Manifesto')}</h1><p class="lead">{t('让 AI 用得起，更用得好。','Make AI affordable and useful.')}</p><p>{t('104.4 秒 · 1080p · 音乐与几何叙事 · 无旁白','104.4 seconds · 1080p · Music and geometric storytelling · Chinese on-screen text, no narration')}</p><video id="film" controls playsinline preload="metadata" poster="poster.jpg"><source src="AI-for-All-Manifesto-V5.mp4" type="video/mp4">{t('请下载 MP4 观看。','Download the MP4 to watch.')}</video><p id="play-status" role="status"></p><nav class="film-downloads" aria-label="{t('下载与阅读','Downloads and reading')}"><a class="primary" download href="AI-for-All-Manifesto-V5.mp4">{t('下载影片 MP4','Download MP4')} ↓</a><a href="AI-for-All-Manifesto-V5-Source.zip" download>{t('制作源文件','Production source')} ZIP ↓</a><a href="../downloads/AI-for-All-Manifesto-v1.2-Designed-ZH.pdf">{t('设计版 PDF','Designed PDF (Chinese)')} ↓</a><a href="SHA256SUMS.txt">SHA-256</a></nav><h2>{t('影片章节','Film chapters')}</h2><div class="film-chapters">{chapters}</div><section class="film-end"><h2>{t('共同把愿景，变成行动。','Turn our shared vision into action.')}</h2><a href="{home}#fulltext">{t('阅读完整宣言','Read the manifesto')} ↗</a><a href="https://github.com/X-lab2017/ai-for-all/blob/main/CONTRIBUTING.md">{t('参与共建','Contribute')} ↗</a><a href="https://github.com/X-lab2017/ai-for-all/issues/5">{t('完整创作记录','Creation history')} ↗</a></section><p class="film-credit">{t('配乐由项目委托方提供：《血色浪漫的片头曲伴奏》。第三方音乐、字体及品牌遵循各自权利与许可；公开源码不授予音乐再利用许可。','Music supplied by the project commissioner: “血色浪漫的片头曲伴奏”. Third-party music, fonts and branding retain their respective rights; source publication does not grant music reuse rights.')}</p></main><footer class="shell film-footer">X-lab AI · AI FOR ALL · v1.2 / V5</footer><script src="film.js"></script></body></html>'''
 (OUT/('en.html' if english else 'index.html')).write_text(page)
# Idempotently insert entrances after the existing generators have run.
for path,marker,target,label in [
 ('index.html','<div class="header-actions">','film/?lang=zh','宣言影片'),('en.html','<div class="header-actions">','film/en.html?lang=en','Manifesto film'),
 ('presentation/index.html','<div class="display-controls">','../film/?lang=zh','宣言影片'),('presentation/en.html','<div class="display-controls">','../film/en.html?lang=en','Manifesto film')]:
 p=SITE/path;s=p.read_text();link=f'<a class="utility-control film-entry" href="{target}">{label} ↗</a>'
 if 'film-entry' not in s:
  assert marker in s,path
  s=s.replace(marker,link+marker if marker=='</nav>' else marker+link,1)
 if path in ['index.html','en.html'] and 'film-hero-entry' not in s:
  s=s.replace('<div class="hero-actions">',f'<div class="hero-actions"><a class="text-link film-hero-entry" href="{target}">{label} ↗</a>',1)
 p.write_text(s)
files=['AI-for-All-Manifesto-V5.mp4','AI-for-All-Manifesto-V5-Source.zip']
(OUT/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256((OUT/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in files))
(OUT/'chapters.json').write_text(json.dumps([dict(start=s,zh=z,en=e) for s,z,e in zip(cuts,zh,en)],ensure_ascii=False,indent=2)+'\n')
print('V5 film pages, chapters and linked entrances built')

import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'scripts/navigation/build.py')],check=True)
