#!/usr/bin/env python3
"""Build the bilingual static site from canonical Markdown using only Python stdlib."""
from pathlib import Path
import html,re
from diagrams import DIAGRAMS, figure, export_all
export_all()
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
REPO='https://github.com/X-lab2017/ai-for-all'
def inline(s):
 s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
 def link(m):
  target=html.unescape(m[2])
  if not target.startswith(('https://','http://','#')):
   target=REPO+'/blob/main/'+target.removeprefix('../')
  return '<a href="'+html.escape(target,quote=True)+'">'+m[1]+'</a>'
 return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
def render(s, lang="zh"):
 s=re.sub(r"<!-- diagram:start:([a-z-]+) -->.*?<!-- diagram:end -->",lambda m:"\n@@diagram:"+m[1]+"\n",s,flags=re.S)
 out=[];paragraph=[]
 def flush():
  if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
 for line in s.splitlines():
  if not line.strip():flush();continue
  if line.startswith('@@diagram:'):
   flush();key=line.split(':',1)[1];out.append(figure(next(d for d in DIAGRAMS if d['id']==key),lang))
  elif line.startswith('#'):
   flush();level=min(len(line)-len(line.lstrip('#')),4);out.append(f'<h{level}>'+inline(line[level:].strip())+f'</h{level}>')
  elif line.startswith('- '):flush();out.append('<p class="list-item">'+inline(line[2:])+'</p>')
  else:paragraph.append(line)
 flush();return '\n'.join(out)
def body(path):
 s=(ROOT/path).read_text();return s.split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0]
for lang in ['zh','en']:
 zh=lang=='zh';title='让 AI 用得起，<br><em>更用得好。</em>' if zh else 'Open possibilities.<br><em>Grow capabilities.</em>'
 intro='以开源降低门槛，以成长释放创造力。' if zh else 'Lower barriers through open source. Unlock creativity through growth.'
 text=body('README.md' if zh else 'translations/en.md')
 progress=render((ROOT/'PROGRESS.md').read_text()) if zh else '<h2>Open manifesto co-creation</h2><p>The repository and launch issue are open. Everyone is welcome to contribute feedback, propose actions and share experience. No prior contribution or score is required.</p><p>Resource support will be announced only after availability, conditions and responsibilities are confirmed.</p><p><a href="'+REPO+'/blob/main/PROGRESS.md">Read the full progress record in Chinese</a></p>'
 page=f'''<!doctype html><html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{'X-lab AI 普惠行动' if zh else 'X-lab AI · AI for All'}</title><meta name="description" content="{intro}"><link rel="icon" href="assets/XlabAI_Symbol_ColorLight.svg"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="diagrams.css"></head><body>
<a class="skip" href="#manifesto">{'跳至宣言' if zh else 'Skip to manifesto'}</a>
<header><a href="index.html"><img src="assets/XlabAI_Horizontal_ColorDark.svg" alt="X-lab AI 开放实验室"></a><nav><a href="#manifesto">{'宣言' if zh else 'Manifesto'}</a><a href="#action">{'行动' if zh else 'Action'}</a><a href="{'en.html' if zh else 'index.html'}">{'EN' if zh else '中文'}</a><a href="{REPO}">GitHub</a></nav></header>
<main><section class="hero"><div class="kicker">X-LAB AI / AI FOR ALL</div><h1>{title}</h1><p class="intro">{intro}</p><div class="hero-bottom"><span>{'AI 普惠宣言 · 长期愿景与行动承诺' if zh else 'A long-term vision and a commitment to action'}</span><a class="button" href="#manifesto">{'阅读宣言' if zh else 'Read the manifesto'}</a></div></section>
<div class="statement"><span>01 / OPEN TECHNOLOGY</span><strong>{'降低进入门槛' if zh else 'Lower barriers'}</strong><span>02 / HUMAN CAPABILITY</span><strong>{'支持人的成长' if zh else 'Support growth'}</strong></div>
<section class="reading" id="manifesto"><aside><div class="kicker">THE MANIFESTO</div><h2>{'共同的方向，<br>公开的承诺。' if zh else 'A shared direction.<br>A public commitment.'}</h2><p>v1.0 · {'正式版' if zh else 'Release'}<br>2026.10.08</p><a href="{REPO}/blob/main/{'README.md' if zh else 'translations/en.md'}">{'查看原文与修订' if zh else 'Source and revisions'}</a></aside><article>{render(text,lang)}</article></section>
<section class="action" id="action"><div class="kicker">FROM VISION TO PRACTICE</div><div class="action-grid"><div><h2>{'让实践，<br>检验承诺。' if zh else 'Let practice<br>test the promise.'}</h2><p>{'第一项行动：宣言公开共建。' if zh else 'Our first action: open manifesto co-creation.'}</p></div><div class="progress">{progress}</div></div></section>
<section class="join"><div class="kicker">BUILD TOGETHER</div><h2>{'每一个问题，<br>都可以成为参与的开始。' if zh else 'Participation can begin<br>with a question.'}</h2><p>{'分享困难、贡献经验、提出不同意见，帮助我们把愿景变成可检验的行动。' if zh else 'Share difficulties, contribute experience and challenge assumptions. Help turn a vision into actions we can examine.'}</p><div class="join-links"><a class="button" href="{REPO}/issues/new/choose">{'提出建议或行动' if zh else 'Share feedback or an action'}</a><a href="{REPO}/blob/main/CONTRIBUTING.md">{'参与指南' if zh else 'Participation guide (Chinese)'}</a></div></section></main>
<footer><strong>X-lab AI · AI for All</strong><div><a href="https://github.com/X-lab2017/xlab-ai-brand">{'品牌资源' if zh else 'Brand resources'}</a><a href="{REPO}/blob/main/NOTICE.md">{'许可说明' if zh else 'Permissions'}</a><a href="{REPO}/issues">{'讨论与反馈' if zh else 'Discussion'}</a></div><p>{'以开放连接智慧，以 AI 拓展认知。' if zh else 'Connect knowledge through openness. Expand understanding with AI.'}</p></footer><script src="diagrams.js" defer></script></body></html>'''
 (SITE/('index.html' if zh else 'en.html')).write_text(page)
print('Built Chinese and English pages from canonical documents.')
