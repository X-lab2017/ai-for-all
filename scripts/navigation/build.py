"""Shared navigation for the current manifesto, film, presentation and archive."""
from pathlib import Path
import re,shutil
ROOT=Path(__file__).resolve().parents[2];SITE=ROOT/'site'
for ext in ['css','js']:shutil.copyfile(Path(__file__).with_name('navigation.'+ext),SITE/('navigation.'+ext))
for section,folder in [('manifesto',''),('film','film/'),('presentation','presentation/'),('resources','launch/')]:
 for en in [False,True]:
  filename='en.html' if en else 'index.html';p=SITE/folder/filename;s=p.read_text();prefix='../' if folder else '';lang='en' if en else 'zh';t=lambda a,b:b if en else a
  old=re.search(r'<header\b.*?</header>',s,re.S).group(0)
  def extract(tag,id):
   m=re.search(fr'<{tag}\b[^>]*\bid="{id}"[^>]*>.*?</{tag}>',old,re.S);return m.group(0) if m else ''
  language=extract('a','language') or f'<a id="language" href="{("index.html?lang=zh" if en else "en.html?lang=en")}" lang="{("zh" if en else "en")}">{t("English","中文")}</a>'
  language=re.sub(r' class="[^"]*"','',language)
  theme=extract('button','theme') or f'<button id="theme" type="button">{t("切换主题","Switch theme")}</button>'
  motion=extract('button','motion')
  home=prefix+('en.html?lang=en' if en else 'index.html?lang=zh')
  items=[('manifesto',home,t('宣言正文','Manifesto')),('film',prefix+'film/'+('en.html' if en else 'index.html')+'?lang='+lang,t('宣言影片','Film')),('presentation',prefix+'presentation/'+('en.html' if en else 'index.html')+'?lang='+lang,t('互动演示','Presentation')),('resources',prefix+'launch/'+('en.html' if en else 'index.html')+'?lang='+lang,t('发布资料','Resources'))]
  items=[item for item in items if item[0]!='resources']
  links=''.join(f'<a href="{url}"'+(' aria-current="page"' if key==section else '')+f'>{name}</a>' for key,url,name in items)
  settings=f'<details class="nav-settings"><summary>{t("显示设置","Display")}<span aria-hidden="true">⌄</span></summary><div class="nav-settings-panel">{theme}{motion}</div></details>'
  brand=f'<a class="nav-brand" href="{home}" aria-label="{t("AI 普惠宣言首页","AI for All home")}"><img class="nav-logo-light" src="{prefix}assets/brand.svg" alt="X-lab AI" width="132" height="40"><img class="nav-logo-dark" src="{prefix}assets/brand-dark.svg" alt="" width="132" height="40"></a>'
  page_number='<b id="page-number" class="nav-page-number">01 / 13</b>' if section=='presentation' else ''
  header=f'<header class="unified-header" data-section="{section}">{brand}<nav class="primary-nav" aria-label="{t("主要内容","Main navigation")}">{links}</nav><div class="nav-utilities">{language}{settings}{page_number}</div></header>'
  s=s.replace(old,header,1)
  if 'navigation.css' not in s:s=s.replace('</head>',f'<link rel="stylesheet" href="{prefix}navigation.css"></head>')
  if 'navigation.js' not in s:s=s.replace('</body>',f'<script src="{prefix}navigation.js"></script></body>')
  s=re.sub(r'<body([^>]*)>',fr'<body\1 data-navigation-section="{section}">',s,count=1) if 'data-navigation-section=' not in s else s
  if section=='resources':
   if '../preferences.js' not in s:s=s.replace('</head>','<script src="../preferences.js"></script></head>')
  if section=='manifesto':
   actions=f'<div class="hero-actions"><a class="primary" href="#fulltext">{t("阅读完整宣言","Read the manifesto")} ↓</a><a class="text-link" href="{items[1][1]}">{t("观看宣言影片","Watch the film")} →</a><a class="text-link" href="{items[2][1]}">{t("进入互动演示","Explore the presentation")} →</a></div>'
   s=re.sub(r'<div class="hero-actions">.*?</div>',lambda _:actions,s,count=1,flags=re.S)
  if section!='presentation':
   footer=f'<nav class="resource-nav" aria-label="{t("相关内容","Related content")}">{links}<a href="https://github.com/X-lab2017/ai-for-all/blob/main/CONTRIBUTING.md">{t("参与共建","Contribute")} ↗</a></nav>'
   s=re.sub(r'<nav class="resource-nav".*?</nav>','',s,flags=re.S)
   s=s.replace('</footer>',footer+'</footer>',1)
  p.write_text(s)
print('Shared navigation built: 4 sections × 2 languages')
