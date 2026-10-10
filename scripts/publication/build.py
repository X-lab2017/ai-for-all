from pathlib import Path
import json, re, html, math, shutil, hashlib
from i18n import translate_page
from geometry import vision_art, network_art, growth_art, panorama
H=Path(__file__).resolve().parent
ROOT=H.parents[1]; OUT=ROOT/'site'; OUT.mkdir(exist_ok=True)
raw=(ROOT/'README.md').read_text()
body=raw.split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0].strip()
texts=['**让 AI 用得起，更用得好**','X-lab AI 开放实验室 · v1.2 · 2026 年 10 月 10 日']+body.split('\n\n')
blocks=[{'id':'text-'+hashlib.sha256(t.encode()).hexdigest()[:16],'markdown':t}for t in texts if t.strip()]
def inline(s):
 return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',html.escape(s))
def para(b):
 return f'<p data-source="{b["id"]}">{inline(b["markdown"])}</p>'
sections=[]; intro=[]
for b in blocks[2:]:
 if b['markdown'].startswith('## '): sections.append({'title':b['markdown'][3:],'blocks':[]})
 elif sections: sections[-1]['blocks'].append(b)
 else:intro.append(b)
ids=['vision','forces','wheels','possibilities','renewal']; glyphs=['一','二','三','万','生']
def svg(body,label,view='0 0 600 540'):
 return f'<svg viewBox="{view}" role="img" aria-label="{label}">{body}</svg>'
def text(x,y,label,cls=''):
 return f'<text x="{x}" y="{y}" class="{cls}">{label}</text>'
def loop(path,id,count=3,guide=False):
 beads=''.join(f'<circle class="traveler bead-{i%3}" r="{[4.5,3,5.5][i%3]}" data-track="{id}" data-phase="{i/count:.4f}" data-period="{42000+i*11000}" aria-hidden="true"/>' for i in range(count))
 return f'<path id="{id}" class="trace {"motion-guide" if guide else ""}" d="{path}"/>'+beads
def circlepath(cx,cy,r):return f'M {cx-r} {cy} a {r} {r} 0 1 0 {r*2} 0 a {r} {r} 0 1 0 {-r*2} 0'
hero='<circle class="halo" cx="300" cy="280" r="200"/>'
for r in [90,145,200,248]:hero+=f'<circle class="orbit" cx="300" cy="280" r="{r}"/>'
hero+=loop(circlepath(300,280,200),'hero-track',4)+loop(circlepath(300,280,145),'hero-inner-track',3,True)+loop(circlepath(300,280,248),'hero-outer-track',4,True)
for i,(char,title) in enumerate(zip(glyphs,[s['title'] for s in sections])):
 a=-math.pi/2+i*math.tau/5;x=300+200*math.cos(a);y=280+200*math.sin(a)
 hero+=f'<a href="#{ids[i]}" aria-label="{title}"><circle class="hero-node" cx="{x}" cy="{y}" r="22"/>'+text(x,y+7,char,'hero-glyph')+'</a>'
hero+='<image href="assets/brand-symbol.svg" x="261" y="191" width="78" height="98"/>'+text(300,326,'AI FOR ALL','hero-word')+text(300,356,'共 同 的 愿 景','micro')
vision=vision_art()
forces='<defs><clipPath id="left-lens"><circle cx="218" cy="255" r="137"/></clipPath></defs><circle class="lens" cx="382" cy="255" r="137" clip-path="url(#left-lens)"/>'
forces+=loop(circlepath(218,255,137),'open-track')+loop(circlepath(382,255,137),'people-track')
forces+=text(187,250,'开源之力','label')+text(187,280,'降低门槛','tiny')+text(413,250,'开发者之力','label')+text(413,280,'拓展价值','tiny')+text(300,246,'项目','tiny')+text(300,272,'社区','tiny')
forces+='<path class="spoke" d="M300 394 V437"/><rect class="pill" x="225" y="437" width="150" height="46" rx="23"/>'+text(300,466,'数字公共品','label')
wheel_groups=[]; tail=[]
for b in sections[2]['blocks'][2:]:
 if b['markdown'].startswith('### '):wheel_groups.append({'title':b['markdown'][4:],'blocks':[]})
 elif len(wheel_groups)==3 and b['markdown'].startswith('三个飞轮'):tail.append(b)
 elif wheel_groups:wheel_groups[-1]['blocks'].append(b)
steps=[['数据采集','基准建设','平台支撑','评价应用'],['贡献评价','成长可见','人才汇聚','供给改善','普惠增进'],['资源投入','贡献识别','价值回馈','成效验证']]
wheel_arts=[]
for w,g in enumerate(wheel_groups):
 art=f'<circle class="orbit fine" cx="300" cy="270" r="112"/>'+loop(circlepath(300,270,183),f'wheel-track-{w}')+text(300,263,g['title'],'center')+text(300,294,['证据 · 判断','能力 · 创造','资源 · 持续'][w],'tiny')
 for j,label in enumerate(steps[w]):
  a=-math.pi/2+j*math.tau/len(steps[w]);x=300+183*math.cos(a);y=270+183*math.sin(a)
  art+=f'<g class="stage stage-{j}"><rect x="{x-67}" y="{y-29}" width="134" height="58" rx="29"/>'+text(x,y+7,label,'label')+'</g>'
 wheel_arts.append(svg(art,g['title']+'循环图'))
network=network_art(loop)
renew=growth_art(loop)
def artblock(art,label,caption,view="0 0 600 540") :
 return f'<figure class="art motion-area">{svg(art,label,view)}<figcaption>{caption}</figcaption></figure>'
def prose(bs):return ''.join(para(b)for b in bs)
def heading(i):return f'<div class="chapter-heading"><span class="chapter-number">{glyphs[i]}</span><div><span class="eyebrow">CHAPTER 0{i+1}</span><h2>{sections[i]["title"]}</h2></div></div>'
def lead(i):return para(sections[i]['blocks'][0])
nav=''.join(f'<a href="#{id}"><span>{glyphs[i]}</span>{sections[i]["title"]}</a>'for i,id in enumerate(ids))
chapters=f'<section id="vision" class="chapter shell">{heading(0)}<div class="chapter-grid"><div class="prose">{prose(sections[0]["blocks"])}</div>{artblock(vision,"AI 普惠中心球，三个视角球体公转，Learner、Builder、Engineer 围绕开发者公转","01 / 同一愿景，多重视角","0 0 640 640")}</div></section>'
chapters+=f'<section id="forces" class="chapter pale"><div class="shell">{heading(1)}<div class="chapter-grid"><div class="prose">{prose(sections[1]["blocks"])}</div><div>{artblock(forces,"开源与开发者两股力量交汇于项目与社区，共建数字公共品","02 / 开放支持创造，创造丰富开放")}<div class="pathway"><span>AI 能力</span><i>→</i><span>数字公共品</span><i>→</i><span>AI 普惠</span></div></div></div></div></section>'
tabs=''.join(f'<button class="wheel-tab" id="tab-{i}" data-wheel="{i}" type="button" aria-controls="wheel-{i}"><span>0{i+1}</span>{g["title"]}<small>{["证据","人才","资源"][i]}</small></button>'for i,g in enumerate(wheel_groups))
panels=''
for i,g in enumerate(wheel_groups):
 panels+=f'<article class="wheel-panel" id="wheel-{i}" aria-labelledby="wheel-title-{i}"><figure class="art motion-area">{wheel_arts[i]}<figcaption>{len(steps[i])} 个环节 · 反馈进入下一轮</figcaption></figure><div class="wheel-copy prose"><h3 id="wheel-title-{i}">{g["title"]}</h3>{prose(g["blocks"])}</div></article>'
chapters+=f'<section id="wheels" class="chapter forest"><div class="shell">{heading(2)}<div class="wheel-intro prose">{prose(sections[2]["blocks"][:2])}</div><div class="wheel-tabs" aria-label="选择飞轮">{tabs}</div><div class="wheel-panels">{panels}</div><div class="coupling prose">{prose(tail)}</div></div></section>'
network_buttons=''.join(f'<button type="button" data-cluster="{i}" aria-pressed="false">{v}</button>'for i,v in enumerate(['学习','工作','社区','本地实践']))
chapters+=f'<section id="possibilities" class="chapter shell">{heading(3)}<div class="chapter-grid"><div class="prose">{prose(sections[3]["blocks"])}</div><div class="network-figure">{artblock(network,"多样实践交织为一个连续、连通的公共品网络","04 / 共享成果，连接多样实践")}<div class="network-options" aria-label="突出实践社群">{network_buttons}</div><p class="interaction-hint">点选场景，查看它与公共品的连接</p></div></div></section>'
last=sections[4]['blocks'];mainlast=last[:-2];closing=last[-2:]
chapters+=f'<section id="renewal" class="chapter pale"><div class="shell">{heading(4)}<div class="chapter-grid"><div class="prose">{prose(mainlast)}</div>{artblock(renew,"实践如种子生根，记录和检验形成枝干，改进带来新芽，经验回流根部","05 / 从实践生长，在反馈中演化")}</div></div></section>'
architecture=panorama()
full=''.join(f'<h{len(b["markdown"])-len(b["markdown"].lstrip("#"))}>{inline(b["markdown"].lstrip("# "))}</h{len(b["markdown"])-len(b["markdown"].lstrip("#"))}>' if b['markdown'].startswith('#') else '<p>'+inline(b['markdown'])+'</p>'for b in blocks)
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="AI 普惠宣言：让 AI 用得起，更用得好。一心普惠，二力相生，三重飞轮，万千可能，生生不息。"><link rel="canonical" href="https://www.x-lab.info/ai-for-all/"><meta property="og:title" content="AI 普惠宣言 · X-lab AI"><meta property="og:description" content="一心普惠，二力相生，三重飞轮，万千可能，生生不息。"><meta property="og:url" content="https://www.x-lab.info/ai-for-all/"><meta name="theme-color" content="#173b31"><title>AI 普惠宣言 · X-lab AI</title><link rel="icon" href="assets/brand-symbol.svg" type="image/svg+xml"><script src="preferences.js"></script><link rel="alternate" hreflang="zh-CN" href="https://www.x-lab.info/ai-for-all/"><link rel="alternate" hreflang="en" href="https://www.x-lab.info/ai-for-all/en.html"><link rel="stylesheet" href="manifesto.css"></head><body><a class="skip" href="#main">跳至正文</a><div class="progress" aria-hidden="true"></div><header class="site-header"><a class="brand" href="#top" aria-label="X-lab AI 首页"><img class="brand-light" src="assets/brand.svg" alt="X-lab AI" width="146" height="44"><img class="brand-dark" src="assets/brand-dark.svg" alt="" aria-hidden="true" width="146" height="44"></a><span class="header-title">AI 普惠宣言</span><div class="header-actions"><a class="header-presentation utility-control" href="presentation/?lang=zh">互动演示 <span aria-hidden="true">↗</span></a><a class="header-read" href="#fulltext">阅读全文</a><a id="language" class="utility-control" href="en.html?lang=en" data-language="en" aria-label="切换语言"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><span>English</span></a><button id="theme" class="utility-control" type="button" aria-pressed="false" aria-label="切换为深色模式"><svg class="icon-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14A9 9 0 0 1 10 4a8 8 0 1 0 10 10Z"/></svg><svg class="icon-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/></svg><span>深色</span></button><button id="motion" type="button" aria-pressed="false">暂停动效</button></div></header><main id="main"><section class="hero" id="top"><div class="shell hero-grid"><div class="hero-copy"><span class="eyebrow">X-LAB AI · MANIFESTO</span><h1>AI 普惠宣言</h1><div class="hero-statement">让 AI 用得起，<em>更用得好。</em></div><p class="hero-description">{inline(intro[0]['markdown'])}</p><div class="hero-actions"><a class="primary" href="#vision">走进宣言 <span>↗</span></a><a class="text-link" href="#fulltext">阅读完整文本 ↓</a></div></div><figure class="hero-art motion-area">{svg(hero,'一、二、三、万、生围绕 X-lab AI 共同愿景的五层架构','0 0 600 560')}<figcaption>AI FOR ALL · OPENNESS FOR EVERYONE</figcaption></figure></div><div class="shell hero-bottom"><span>一心普惠 · 二力相生 · 三重飞轮 · 万千可能 · 生生不息</span><span>2026 / 10 / 10</span></div></section><nav class="chapter-nav" aria-label="宣言章节"><div class="shell">{nav}</div></nav><section class="preface shell"><span class="eyebrow">OUR SHARED COMMITMENT</span><div class="prose">{prose(intro[1:])}</div></section>{chapters}<section class="closing forest"><div class="shell"><span class="eyebrow">FROM VISION TO PRACTICE</span><h2>五层相连，<br>就是 AI 普惠的全景。</h2><nav class="panorama" aria-label="五层全景架构">{architecture}</nav><div class="closing-copy prose">{prose(closing)}</div><div class="closing-actions"><a class="primary" href="https://github.com/X-lab2017/ai-for-all/issues" target="_blank" rel="noopener noreferrer">参与宣言共建 ↗</a><a class="text-link" href="#fulltext">阅读与保存全文 ↓</a></div></div></section><section class="fulltext shell" id="fulltext"><span id="manifesto"></span><div class="reading-head"><div><span class="eyebrow">THE FULL MANIFESTO</span><h2>宣言全文</h2></div><div class="reading-actions"><a class="designed-pdf" href="downloads/AI-for-All-Manifesto-v1.2-Designed-ZH.pdf" download>下载设计版 PDF ↓</a><a href="AI-for-All-manifesto.md" download>Markdown 原文 ↓</a><button type="button" id="print">打印 / 存为 PDF</button></div></div><details><summary>展开完整宣言 <span>＋</span></summary><article class="reading-prose"><h2>AI 普惠宣言</h2>{full}</article></details></section></main><footer class="shell"><a href="v1.1.html">v1.1 历史版</a><a href="en-v1.1.html">English · v1.1</a><a href="presentation/">互动演示 · v1.2</a><a href="presentation-v1.1/">互动演示 · v1.1</a><a href="launch/">大会材料 · v1.1</a><span>X-lab AI 开放实验室</span><span>让 AI 用得起，更用得好</span><a href="#top">回到顶部 ↑</a></footer><script src="manifesto.js"></script></body></html>'''
(OUT/'index.html').write_text(page)
(OUT/'en.html').write_text(translate_page(page))
(OUT/'assets').mkdir(exist_ok=True)
shutil.copy(ROOT/'site/assets/XlabAI_Horizontal_ColorLight.svg',OUT/'assets/brand.svg')
shutil.copy(ROOT/'site/assets/XlabAI_Symbol_ColorLight.svg',OUT/'assets/brand-symbol.svg')
shutil.copy(ROOT/'site/assets/XlabAI_Horizontal_ColorDark.svg',OUT/'assets/brand-dark.svg')
shutil.copy(H/'preferences.js',OUT/'preferences.js')
for f,target in [('style.css','manifesto.css'),('app.js','manifesto.js')]:shutil.copy(H/f,OUT/target)
(OUT/'AI-for-All-manifesto.md').write_text('# AI 普惠宣言\n\n'+'\n\n'.join(b['markdown']for b in blocks)+'\n')
print(f'Built v1.2 publication from {len(blocks)} canonical README blocks.')

english=(ROOT/'translations/en.md').read_text();english_body=english.split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0].strip()
(OUT/'AI-for-All-manifesto-EN.md').write_text('# AI for All Manifesto\n\n**Make AI affordable and useful**\n\nX-lab AI Open Laboratory · v1.2 · 10 October 2026\n\n'+english_body+'\n')
