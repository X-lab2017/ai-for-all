#!/usr/bin/env python3
"""Build the bilingual launch hub from checked-in assets. Standard library only."""
from pathlib import Path
import html, json, re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site/launch'
URL='https://www.x-lab.info/ai-for-all/launch/'
REPO='https://github.com/X-lab2017/ai-for-all'
e=lambda s:html.escape(str(s),quote=True)
rows={
'zh':[
 ('宣言全文','目标、框架与行动承诺。中文为权威版本。',[('中文 PDF','AI-for-All-Manifesto-ZH.pdf'),('English PDF','AI-for-All-Manifesto-EN.pdf')]),
 ('大会演示','中英文各 10 页，含逐页讲述备注。',[('中文 PPT','AI-for-All-Conference-ZH.pptx'),('English PPT','AI-for-All-Conference-EN.pptx')]),
 ('现场文稿','主持人引入词、约两分钟致辞、扫码邀请与播放说明。',[('Word','AI-for-All-Conference-Handbook.docx'),('PDF','AI-for-All-Conference-Handbook.pdf')]),
 ('框架全景','保留五个部分及双飞轮关系，供投屏与分享。',[('中文 PNG','AI-for-All-Panorama-ZH.png'),('EN PNG','AI-for-All-Panorama-EN.png'),('双语 PDF','AI-for-All-Panoramas.pdf')]),
 ('固定入口二维码','下载后可用于会场屏幕、议程和印刷物。',[('PNG','AI-for-All-Launch-QR.png'),('SVG','AI-for-All-Launch-QR.svg'),('投屏 PDF','AI-for-All-Launch-QR-Display.pdf')]),
 ('字幕与署名','三版字幕文件、音视频署名和素材说明。',[('字幕 ZIP','AI-for-All-Captions.zip'),('署名 TXT','CREDITS.txt')]),
],
'en':[
 ('The full manifesto','Goals, framework and commitments. The Chinese text is authoritative.',[('中文 PDF','AI-for-All-Manifesto-ZH.pdf'),('English PDF','AI-for-All-Manifesto-EN.pdf')]),
 ('Conference slides','Ten slides per language, with speaker notes.',[('中文 PPT','AI-for-All-Conference-ZH.pptx'),('English PPT','AI-for-All-Conference-EN.pptx')]),
 ('Speaking scripts','Host introductions, two-minute remarks, closing invitation and playback guide.',[('Word','AI-for-All-Conference-Handbook.docx'),('PDF','AI-for-All-Conference-Handbook.pdf')]),
 ('The full framework','Five connected elements and both reinforcing cycles.',[('中文 PNG','AI-for-All-Panorama-ZH.png'),('EN PNG','AI-for-All-Panorama-EN.png'),('Bilingual PDF','AI-for-All-Panoramas.pdf')]),
 ('One link to participate','A reusable code for event screens, programmes and print.',[('PNG','AI-for-All-Launch-QR.png'),('SVG','AI-for-All-Launch-QR.svg'),('Screen PDF','AI-for-All-Launch-QR-Display.pdf')]),
 ('Captions and credits','Subtitle files for all three films, attribution and source notes.',[('Captions ZIP','AI-for-All-Captions.zip'),('Credits TXT','CREDITS.txt')]),
]}
for lang in ['zh','en']:
    zh=lang=='zh'
    def t(z,en):return z if zh else en
    title=t('AI 普惠宣言','AI for All Manifesto')
    desc=t('让 AI 用得起，更用得好。观看宣言、下载大会材料，加入共建。','Make AI affordable and useful. Watch the manifesto, download the materials and take part.')
    videos=[('ZH','中文定稿版','Chinese original','zh'),('Bilingual','中英字幕版','Chinese + English captions','zh'),('EN','英文配音版','English film','en')]
    default='ZH' if zh else 'EN'
    buttons=''.join(f'<button type="button" data-video="downloads/AI-for-All-90s-{key}.mp4" data-poster="assets/cover-{poster}.jpg" data-label="{e(t(z,en))}" aria-pressed="{str(key==default).lower()}">{e(t(z,en))}</button>' for key,z,en,poster in videos)
    dl=''.join('<div class="download-row"><strong>'+e(name)+'</strong><p>'+e(desc)+'</p><div class="download-links">'+''.join(f'<a href="downloads/{f}" download>{e(label)}</a>' for label,f in links)+'</div></div>' for name,desc,links in rows[lang])
    # These links only prepare an Issue. Visitors choose whether to submit it.
    roledefs=[
      ('提出真实需要','Share a real need','说明谁遇到了什么问题，留下一个可讨论的起点。','Describe who faces a problem and what currently makes it difficult.',REPO+'/issues/new?template='+('01-manifesto-feedback.md' if zh else '04-participate-en.md')),
      ('贡献工具与经验','Contribute tools and experience','代码、文档、教学、翻译和实践案例，都能成为贡献。','Code, documentation, teaching, translation and practical cases can all contribute.',REPO+'/blob/main/'+('CONTRIBUTING.md' if zh else 'translations/contributing.en.md')),
      ('开启实践合作','Explore practical collaboration','提出一个应用场景或资源支持想法，共同明确下一步。','Propose a practical setting or resources, then work together to define a next step.',REPO+'/issues/new?template='+('02-action-proposal.md' if zh else '04-participate-en.md')),
    ]
    # Use the existing chooser for Chinese, keeping template filenames authoritative.
    roledefs=[(*v[:4],REPO+'/issues/new/choose' if zh and i!=1 else v[4]) for i,v in enumerate(roledefs)]
    roles=''.join(f'<article class="role"><span class="num">0{i+1}</span><h3>{e(t(z,en))}</h3><p>{e(t(zd,end))}</p><a href="{e(href)}">{t("从这里开始","Start here")} ↗</a></article>' for i,(z,en,zd,end,href) in enumerate(roledefs))
    page=f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#102c25"><title>{title} · {t('正式发布包','Launch materials')} · X-lab AI</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{URL}assets/cover-{lang}.jpg"><meta property="og:url" content="{URL+('' if zh else 'en.html')}"><meta name="twitter:card" content="summary_large_image"><link rel="canonical" href="{URL+('' if zh else 'en.html')}"><link rel="alternate" hreflang="zh-CN" href="{URL}"><link rel="alternate" hreflang="en" href="{URL}en.html"><link rel="icon" href="../assets/XlabAI_Symbol_ColorLight.svg"><link rel="stylesheet" href="style.css?v=release-1"><script src="app.js?v=release-1" defer></script></head>
<body><a class="skip" href="#film">{t('跳至宣言影片','Skip to the film')}</a><div class="wrap"><header class="header"><a class="brand" href="../{'index.html' if zh else 'en.html'}"><img src="../assets/XlabAI_Horizontal_ColorDark.svg" alt="X-lab AI" width="155" height="48"></a><nav aria-label="{t('主导航','Main navigation')}"><a class="optional" href="#materials">{t('下载材料','Materials')}</a><a href="#join">{t('参与共建','Participate')}</a><a href="{'en.html' if zh else 'index.html'}" lang="{'en' if zh else 'zh-CN'}">{t('English','中文')}</a></nav></header>
<main><section class="hero"><div><div class="kicker">X-LAB AI / A PUBLIC COMMITMENT</div><h1>{title}</h1><p class="lead">{t('让 AI 用得起，更用得好。','Make AI affordable and useful.')}</p><p>{t('从开放的技术，到更多人的创造。观看宣言、带走材料，选择一个属于你的参与起点。','Open technology creates opportunities for more people to build. Watch the manifesto, explore the materials and choose your starting point.')}</p><div class="actions"><a class="button primary" href="#film">{t('观看 90 秒宣言','Watch the 90-second film')} ↓</a><a class="button" href="#join">{t('加入共建','Take part')} ↗</a></div></div><aside class="qr"><img src="downloads/AI-for-All-Launch-QR.png" alt="{t('扫码打开统一发布与参与入口','Scan to open the launch and participation page')}" width="175" height="175"><span>{t('一个入口，连接愿景与行动','One link from vision to action')}</span><br><a href="downloads/AI-for-All-Launch-QR.svg" download>{t('下载二维码','Download the code')}</a></aside></section>
<section class="video-section" id="film"><div class="section-head"><div><div class="kicker">THE MANIFESTO FILM</div><h2>{t('一份长期的行动邀请','An invitation to act')}</h2></div><p class="meta">90 {t('秒','seconds')} · 1080p · 16:9</p></div><div class="modes" role="group" aria-label="{t('选择影片版本','Choose a film version')}">{buttons}</div><div class="player"><video controls playsinline preload="metadata" poster="assets/cover-{lang}.jpg" src="downloads/AI-for-All-90s-{default}.mp4" aria-label="{e(title)}">{t('请下载影片后播放。','Please download the film to watch it.')}</video><div class="player-meta"><span id="current-version">{t('中文定稿版','English film')}</span><a id="download-video" href="downloads/AI-for-All-90s-{default}.mp4" download>{t('下载当前影片','Download this film')} ↓</a></div></div><p id="video-error" class="small" hidden>{t('当前浏览器未能播放，可使用上方下载链接观看。','Your browser could not play this file. Use the download link above to watch it.')}</p><p class="small">{t('英文版包含英文配音与画面；中英字幕版保留中文配音和画面。人声均为 AI 合成。','The English edition has English narration and visuals. The bilingual edition retains Chinese narration and visuals. All narration is AI generated.')}</p></section></main></div>
<section class="paper" id="materials"><div class="wrap"><div class="section-head"><div><div class="kicker">CONFERENCE MATERIALS</div><h2>{t('把宣言带到现场','Bring the manifesto to your event')}</h2><p class="meta">{t('正式发布包 · 2026 年 10 月 9 日','Launch package · 9 October 2026')}</p></div><a class="button primary" href="downloads/AI-for-All-Launch-Package.zip" download>{t('下载完整发布包','Download the full package')} ↓</a></div><div class="download-list">{dl}</div><div class="actions"><a class="button" href="../{'index.html' if zh else 'en.html'}#manifesto">{t('在线阅读宣言','Read the manifesto online')} ↗</a><a class="button" href="../presentation-v1.1/#manifesto">{t('打开互动演示','Interactive presentation (Chinese)')} ↗</a></div></div></section>
<div class="wrap"><section class="panorama" id="framework"><div class="kicker">THE COMPLETE FRAMEWORK</div><h2>{t('一个完整框架，一份共同承诺','A shared framework for action')}</h2><p class="meta">{t('一个目标 · 两股力量 · 一个内核 · 两个飞轮 · 三重普惠','One goal · Two forces · One core · Two cycles · Three perspectives')}</p><img src="assets/panorama-{lang}.jpg" alt="{t('AI 普惠完整框架：开源与开发者相互促进，成长与投入双飞轮共用数据评价内核，面向开发者、大众和全球南方。','The full AI for All framework: open source and developers, growth and resource cycles sharing a data and evaluation core, with developer, public and Global South perspectives.')}" width="1600" height="900" loading="lazy"><div class="actions"><a href="downloads/AI-for-All-Panorama-{lang.upper()}.png" download>{t('下载全景图','Download the framework')} ↓</a></div></section>
<section class="join" id="join"><div class="kicker">BUILD TOGETHER</div><h2>{t('从一个真实问题开始','Start with a real need')}</h2><p>{t('无论你正在学习、构建工具，还是希望提供应用场景，都可以参与。基础参与不需要已有贡献分数。','Whether you are learning, building a tool or offering a practical setting, you can take part. No prior contribution score is needed to begin.')}</p><div class="roles">{roles}</div><p class="small">{t('参与讨论和提交建议需要 GitHub 账号。提案公开可见；具体合作与资源条件由双方后续明确。','A GitHub account is needed to post a contribution or proposal. Proposals are public. Partnership and resource conditions are agreed in subsequent discussion.')}</p><div class="actions"><a href="{REPO}/issues">{t('查看已有讨论','Browse existing discussions')} ↗</a></div></section>
<details><summary>{t('署名与材料使用说明','Attribution and use of materials')}</summary><p>Music: “Heroic Age” — Kevin MacLeod (incompetech.com). <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Excerpt, equalization, ducking and mix.</p><p>{t('宣言、图解、名称与标识的使用范围见仓库许可说明。第三方材料遵循各自许可；影片已保留音乐署名。','Consult the repository notice for manifesto, diagram and brand reuse terms. Third-party materials retain their own terms. Music attribution remains in each film.')} <a href="downloads/CREDITS.txt">{t('完整署名','Full credits')}</a> · <a href="{REPO}/blob/main/NOTICE.md">{t('许可说明','Permissions')}</a></p></details>
<footer><span>X-lab AI · AI for All</span><div class="credits-links"><a href="{REPO}">GitHub</a><a href="{REPO}/blob/main/PROGRESS.md">{t('公开进展','Public progress')}</a><a href="{REPO}/blob/main/CHANGELOG.md">{t('版本记录','Changelog')}</a></div></footer></div></body></html>'''
    notice=t('本页视频、PPT、PDF 及全景图对应 v1.1（2026-10-09）。当前中文宣言已更新至 v1.2。','These films, slides, PDFs and diagrams are v1.1 materials (2026-10-09). The current Chinese manifesto is v1.2.')
    page=page.replace('<body>','<body><aside style="padding:16px 24px;text-align:center;background:#e8eddc;color:#173b31">'+notice+' <a href="../index.html">'+t('阅读当前宣言 →','Read the current manifesto →')+'</a></aside>',1)
    (OUT/('index.html' if zh else 'en.html')).write_text(page)

def inline(s):
    s=e(s.replace("’", "'").replace("‘", "'"))
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',s)
for lang,source in [('zh','versions/v1.1.zh.md'),('en','versions/v1.1.en.md')]:
    raw=(ROOT/source).read_text().split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0]
    parts=re.split(r'^## ',raw.strip(),flags=re.M)[1:]
    sections=[]
    for part in parts:
        heading,body=part.split('\n',1)
        body=re.sub(r'<!-- diagram:start:([a-z-]+) -->.*?<!-- diagram:end -->',lambda m:'\n\n@@'+m[1]+'\n\n',body,flags=re.S)
        content=''
        for para in body.strip().split('\n\n'):
            if para.startswith('@@'):content+=f'<img src="../assets/diagrams/{para[2:]}-{lang}.svg" alt="{e(heading)}">'
            elif para.strip():content+='<p>'+inline(para.strip())+'</p>'
        sections.append(f'<section class="manifesto-section"><h2>{e(heading)}</h2>{content}</section>')
    title='AI 普惠宣言' if lang=='zh' else 'AI for All Manifesto'
    tagline='让 AI 用得起，更用得好' if lang=='zh' else 'Make AI affordable and useful'
    foot='中文正文为权威版本。' if lang=='zh' else 'The Chinese text is authoritative.'
    page=f'''<!doctype html><html lang="{'zh-CN' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><title>{title}</title><link rel="stylesheet" href="print.css"></head><body class="manifesto"><header><img src="../assets/XlabAI_Horizontal_ColorLight.svg" alt="X-lab AI"><h1>{title}</h1><p class="tagline">{tagline}</p><p class="edition">X-lab AI · v1.1 · 2026-10-09</p></header>{''.join(sections)}<footer><p>{foot} <a href="{URL}">{URL}</a></p><p>Sources and permissions: {REPO}/blob/main/NOTICE.md</p></footer></body></html>'''
    (OUT/f'manifesto-{lang}.html').write_text(page)

(OUT/'qr-display.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AI for All · Participate</title><link rel="stylesheet" href="print.css"></head><body class="qr-display"><main><img class="qr-brand" src="../assets/XlabAI_Horizontal_ColorDark.svg" alt="X-lab AI"><div class="qr-layout"><div><p class="qr-kicker">AI FOR ALL / BUILD TOGETHER</p><h1>让愿景成为行动</h1><h2>Turn a shared vision<br>into action</h2><p class="qr-actions">阅读宣言 · 下载材料 · 参与共建<br>Read. Explore. Contribute.</p></div><div class="qr-box"><img src="downloads/AI-for-All-Launch-QR.png" alt="Scan to participate"><p>扫码了解与参与<br>Scan to take part</p></div></div><p class="qr-url">www.x-lab.info/ai-for-all/launch/</p></main></body></html>''')
(OUT/'panoramas.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>AI for All Framework</title><link rel="stylesheet" href="print.css"></head><body class="panoramas"><img src="downloads/AI-for-All-Panorama-ZH.png" alt="中文全景"><img src="downloads/AI-for-All-Panorama-EN.png" alt="English framework"></body></html>''')
print('Built bilingual release hub, manifesto print editions and event display pages.')
