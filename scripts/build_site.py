#!/usr/bin/env python3
"""Build both languages from canonical Markdown; Python standard library only."""
from pathlib import Path
import re,html,hashlib
from diagrams import DIAGRAMS,figure,export_all
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';REPO='https://github.com/X-lab2017/ai-for-all';URL='https://www.x-lab.info/ai-for-all/'
ANCHORS=['goal','path','forces','core','cycles','commitments']
NAV={'zh':['目标与对象','主张与路径','两股力量','共同内核','两个飞轮','行动与邀请'],'en':['Goal and people','Proposition and path','Two forces','Shared core','Two cycles','Commitments']}
def e(s):return html.escape(str(s),quote=True)
def inline(s):
 s=e(s);s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 def link(m):
  target=html.unescape(m[2])
  if not target.startswith(('https://','http://','#')):target=REPO+'/blob/main/'+target.removeprefix('../')
  return '<a href="'+e(target)+'">'+m[1]+'</a>'
 return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
def render(s,lang='zh',anchored=False):
 s=re.sub(r'<!-- diagram:start:([a-z-]+) -->.*?<!-- diagram:end -->',lambda m:'\n@@diagram:'+m[1]+'\n',s,flags=re.S)
 out=[];paragraph=[];li=[];heading=0
 def flush():
  if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
  if li:out.append('<ul>'+''.join('<li>'+inline(t)+'</li>' for t in li)+'</ul>');li.clear()
 for line in s.splitlines():
  if not line.strip():flush();continue
  if line.startswith('@@diagram:'):
   flush();d=next(d for d in DIAGRAMS if d['id']==line.split(':',1)[1]);out.append(figure(d,lang))
  elif line.startswith('#'):
   flush();level=min(len(line)-len(line.lstrip('#')),4)
   if level==1:continue
   aid=''
   if level==2 and anchored:aid=f' id="{ANCHORS[heading]}"';heading+=1
   out.append(f'<h{level}{aid}>'+inline(line[level:].strip())+f'</h{level}>')
  elif line.startswith('- '):
   if paragraph:flush()
   li.append(line[2:])
  elif line.startswith('<!--'):continue
  else:
   if li:flush()
   paragraph.append(line)
 flush();return '\n'.join(out)
def body(path):return (ROOT/path).read_text().split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0]
export_all()
for lang in ['zh','en']:
 zh=lang=='zh';filename='index.html' if zh else 'en.html';title='AI 普惠宣言' if zh else 'AI for All Manifesto';subtitle='让 AI 用得起，更用得好' if zh else 'Make AI affordable and useful';intro='以数据与评价为内核，让开源之力与开发者之力相互促进，通过数字公共品走向 AI 普惠。' if zh else 'Open source and developer creativity, connected by data and evaluation. A path to AI for All through digital public goods.'
 text=body('README.md' if zh else 'translations/en.md');progress=(ROOT/('PROGRESS.md' if zh else 'translations/progress.en.md')).read_text()
 links=''.join(f'<a href="#{a}">{i+1:02d}　{e(n)}</a>' for i,(a,n) in enumerate(zip(ANCHORS,NAV[lang])))
 fw=[('goal-path','一个目标','AI 普惠','One goal','AI for All'),('dual-forces','两股力量','开源 × 开发者','Two forces','Open source × Developers'),('evaluation-core','一个内核','数据与评价','One core','Data and evaluation'),('twin-flywheels','两个飞轮','成长与持续投入','Two cycles','Growth and resources'),('inclusion-views','三重普惠','多样的受益视角','Three perspectives','Diverse needs')]
 framework=''.join(f'<a href="#{id}"><span>{z if zh else en}</span><strong>{z2 if zh else en2}</strong></a>' for id,z,z2,en,en2 in fw)
 formula='<span class="formula-result">AI 普惠</span><span class="formula-symbol">=</span><span class="formula-part">技术的普惠性<small>用得起</small></span><span class="formula-symbol">×</span><span class="formula-part">开发者的创造力<small>用得好</small></span>' if zh else '<span class="formula-result">AI for All</span><span class="formula-symbol">=</span><span class="formula-part">Accessible technology<small>Affordable access</small></span><span class="formula-symbol">×</span><span class="formula-part">Developer creativity<small>Capable use</small></span>'
 page=f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · X-lab AI</title><meta name="description" content="{intro}"><meta property="og:type" content="website"><meta property="og:title" content="{title} · X-lab AI"><meta property="og:description" content="{intro}"><meta property="og:url" content="{URL+filename}"><meta property="og:image" content="{URL}assets/social-preview.png"><meta name="twitter:card" content="summary_large_image"><link rel="canonical" href="{URL+filename}"><link rel="alternate" hreflang="zh-CN" href="{URL}index.html"><link rel="alternate" hreflang="en" href="{URL}en.html"><link rel="icon" href="assets/XlabAI_Symbol_ColorLight.svg"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="diagrams.css"></head>
<body><a class="skip" href="#manifesto">{'跳至宣言' if zh else 'Skip to manifesto'}</a>
<header><a href="index.html"><img src="assets/XlabAI_Horizontal_ColorDark.svg" alt="X-lab AI" width="155" height="42"></a><nav aria-label="{'主导航' if zh else 'Main navigation'}"><a href="#manifesto">{'宣言' if zh else 'Manifesto'}</a><a href="#practice">{'实践' if zh else 'Practice'}</a><a href="{'en.html' if zh else 'index.html'}" lang="{'en' if zh else 'zh-CN'}">{'EN' if zh else '中文'}</a><a href="{REPO}">GitHub</a></nav></header>
<main><section class="hero"><div class="hero-inner"><div class="kicker">X-LAB AI / A PUBLIC COMMITMENT</div><h1>{title}</h1><p class="hero-subtitle">{subtitle}</p><p class="hero-description">{intro}</p><p class="hero-path">AI <span>→</span> DPG {"（数字公共品）" if zh else "(digital public goods)"} <span>→</span> {"AI 普惠" if zh else "AI for All"}</p><div class="hero-meta"><a class="button" href="#manifesto">{'阅读宣言' if zh else 'Read the manifesto'} <span aria-hidden="true">↓</span></a><span>v1.1 · 2026.10.09 · {'长期愿景与行动承诺' if zh else 'A long-term vision and commitment'}</span></div><div class="hero-formula">{formula}</div><p class="formula-note">{'相互促进的理念表达，成效由实践检验。' if zh else 'A statement of mutual reinforcement. Outcomes are tested in practice.'}</p></div></section>
<nav class="framework" aria-label="{'五要素框架' if zh else 'Five elements'}">{framework}</nav>
<section class="reading" id="manifesto"><aside><div class="kicker">THE MANIFESTO</div><h2>{'共同的方向，<br>公开的承诺。' if zh else 'A shared direction.<br>A public commitment.'}</h2><p>{'一个目标，通过数字公共品<br>连接创造与受益。' if zh else 'Connect creation and public benefit through digital public goods.'}</p><nav class="contents" aria-label="{'正文目录' if zh else 'Contents'}">{links}</nav><a class="source" href="{REPO}/blob/main/{'README.md' if zh else 'translations/en.md'}">{'查看原文与修订' if zh else 'Source and revisions'} ↗</a><br><button class="print-button" type="button" data-print>{'打印 / 另存为 PDF' if zh else 'Print / Save as PDF'}</button></aside><article>{render(text,lang,True)}</article></section>
<section class="practice" id="practice"><div class="practice-inner"><div class="kicker">FROM VISION TO PRACTICE</div><div class="section-intro"><h2>{'实践基础与行动进展' if zh else 'Foundations and progress'}</h2><p>{'从已有的数据、方法与社区出发，用公开记录连接愿景与行动。' if zh else 'Build on existing data, methods and communities, connecting vision and action through public records.'}</p></div><div class="practice-content">{render(progress,lang)}</div></div></section>
<section class="join" id="join"><div class="join-inner"><div class="kicker">BUILD TOGETHER</div><h2>{'每一个问题，<br>都可以成为参与的开始。' if zh else 'Participation can begin<br>with a question.'}</h2><p>{'分享需要、贡献经验、提出不同意见。与我们共同建设可共享的成果，让更多人获得使用 AI 的机会与能力。' if zh else 'Share needs, contribute experience and challenge assumptions. Build shareable results that help more people access AI and develop the capability to use it.'}</p><div class="join-links"><a class="button" href="{REPO}/issues/new/choose">{'提出建议或行动' if zh else 'Share feedback or an action'} ↗</a><a href="{REPO}/blob/main/CONTRIBUTING.md">{'参与指南' if zh else 'Participation guide'}</a><a href="{REPO}/tree/main/site/assets/diagrams">{'五幅图解下载' if zh else 'Download the diagrams'}</a></div></div></section></main>
<footer><strong>X-lab AI · AI for All</strong><div><a href="{REPO}/blob/main/SOURCES.md">{'术语与来源' if zh else 'Sources'}</a><a href="{REPO}/blob/main/CHANGELOG.md">{'版本记录' if zh else 'Changelog'}</a><a href="{REPO}/blob/main/NOTICE.md">{'许可说明' if zh else 'Permissions'}</a><a href="https://github.com/X-lab2017/xlab-ai-brand">{'品牌资源' if zh else 'Brand resources'}</a></div><p>{'以开放连接智慧，以 AI 拓展认知。' if zh else 'Connect knowledge through openness. Expand understanding with AI.'}</p></footer><script src="diagrams.js?v={hashlib.sha256((SITE/'diagrams.js').read_bytes()).hexdigest()[:12]}" defer></script></body></html>'''
 (SITE/filename).write_text(page)
# Code-native social card: typography and a precise path, no generated illustration.
(SITE/'assets/social-preview.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#10281f"/><g font-family="Arial,Source Han Sans SC,sans-serif"><text x="80" y="95" fill="#b2e76b" font-size="21" letter-spacing="4">X-LAB AI / AI FOR ALL</text><text x="75" y="250" fill="white" font-size="94" font-weight="600">AI 普惠宣言</text><text x="80" y="332" fill="#b2e76b" font-size="40">让 AI 用得起，更用得好</text><path d="M80 400 H1120" stroke="#4d6552"/><text x="80" y="484" fill="white" font-size="32">AI → DPG（数字公共品）→ AI 普惠</text><text x="80" y="565" fill="#a6b9a5" font-size="19">一个目标 · 两股力量 · 一个内核 · 两个飞轮 · 三重普惠</text></g></svg>''')
print('Built v1.1 Chinese and English pages and five bilingual SVG diagrams.')
