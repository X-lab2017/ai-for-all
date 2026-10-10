"""Create the v1.2 Chinese reading edition from the canonical web Markdown.

Usage: python3 scripts/pdf/build_designed.py --fonts DIR --output FILE
Requires reportlab, svglib, and NotoSansSC-{Regular,SemiBold}.ttf in DIR.
"""
from pathlib import Path
import argparse, re, math, io, sys
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--fonts',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
for name,weight in [('CN','Regular'),('CNB','SemiBold')]:pdfmetrics.registerFont(TTFont(name,str(args.fonts/f'NotoSansSC-{weight}.ttf')))
pdfmetrics.registerFontFamily('CN',normal='CN',bold='CNB',italic='CN',boldItalic='CNB')
W,H=595.276,841.89; M=48; IW=W-2*M
PAPER='#f7f6ef';INK='#173b31';MUTED='#617369';LINE='#d2d8c9';PALE='#eeeee3';LIME='#c5e79c';FOREST='#143b30'
args.output.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(args.output),pagesize=(W,H),pageCompression=1)
c.setTitle('AI 普惠宣言 | v1.2 设计阅读版');c.setAuthor('X-lab AI 开放实验室');c.setSubject('让 AI 用得起，更用得好。')
c.setViewerPreference('DisplayDocTitle','true')
blocks=(ROOT/'site/AI-for-All-manifesto.md').read_text().strip().split('\n\n')
intro=[];sections=[]
for b in blocks[3:]:
 if b.startswith('## '):sections.append({'title':b[3:],'blocks':[]})
 elif sections:sections[-1]['blocks'].append(b)
 else:intro.append(b)
page_no=0;dark=False
def color(v):return HexColor(v)
def txt(s,x,y,size=11,fill=None,bold=False,align='left'):
 c.setFillColor(color(fill or (PAPER if dark else INK)));c.setFont('CNB' if bold else 'CN',size)
 getattr(c,{'left':'drawString','center':'drawCentredString','right':'drawRightString'}[align])(x,H-y-size*.85,s)
def line(x,y,xx,yy,fill=LINE,width=.7):
 c.setStrokeColor(color(fill));c.setLineWidth(width);c.line(x,H-y,xx,H-yy)
def circle(x,y,r,stroke=LINE,fill=None,width=.8):
 c.setStrokeColor(color(stroke));c.setLineWidth(width)
 if fill:c.setFillColor(color(fill))
 c.circle(x,H-y,r,stroke=1,fill=bool(fill))
def box(x,y,w,h,fill=PALE,r=0):
 c.setFillColor(color(fill));c.roundRect(x,H-y-h,w,h,r,stroke=0,fill=1)
def para(s,x,y,w,size=11,leading=19,fill=None,after=11):
 s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(s))
 st=ParagraphStyle('p',fontName='CN',fontSize=size,leading=leading,textColor=color(fill or (PAPER if dark else INK)),wordWrap='CJK',splitLongWords=False)
 p=Paragraph(s,st);_,h=p.wrap(w,1000)
 assert y+h< H-44,(page_no,y,h,s[:30])
 p.drawOn(c,x,H-y-h);return y+h+after
def paras(bs,x,y,w,size=11,leading=19):
 for b in bs:y=para(b,x,y,w,size,leading)
 return y
def svg(path,x,y,w,h):
 d=svg2rlg(str(path));scale=min(w/d.width,h/d.height);d.scale(scale,scale);renderPDF.draw(d,c,x,H-y-d.height*scale)
def page(title=None,chapter=None,is_dark=False):
 global page_no,dark
 if page_no:c.showPage()
 page_no+=1;dark=is_dark;box(0,0,W,H,FOREST if dark else PAPER)
 svg(ROOT/('site/assets/brand-dark.svg' if dark else 'site/assets/brand.svg'),M,21,99,43)
 txt('AI FOR ALL  /  MANIFESTO',W-M,38,8,LIME if dark else MUTED,align='right')
 line(M,72,W-M,72,'#527063' if dark else LINE)
 txt('X-LAB AI  ·  v1.2  ·  2026.10.10',M,H-32,7.5,LIME if dark else MUTED)
 txt(f'{page_no:02d} / 09',W-M,H-32,8,LIME if dark else MUTED,align='right')
 if title:
  key='p'+str(page_no);c.bookmarkPage(key);c.addOutlineEntry(title,key,0,False)
  if chapter:txt(chapter,M,99,9,LIME if dark else MUTED)
  txt(title,M,123,29,bold=True)
def orbit(x,y,r=125,labels=True):
 for k in [.44,.7,1,1.23]:circle(x,y,r*k,'#76957d' if dark else '#a1af96',width=.5)
 for i,t in enumerate(['一','二','三','万','生']):
  a=-math.pi/2+i*math.tau/5;xx=x+r*math.cos(a);yy=y+r*math.sin(a)
  circle(xx,yy,15,'#8ca782',FOREST if dark else PAPER);txt(t,xx,yy-8,16,LIME if dark else INK,align='center')
  a+=.35;circle(x+r*.7*math.cos(a),y+r*.7*math.sin(a),2.4,LIME if dark else INK,LIME if dark else INK)
 svg(ROOT/'site/assets/brand-symbol.svg',x-25,y-42,50,63)
 txt('AI FOR ALL',x,y+31,14,LIME if dark else INK,bold=True,align='center')
def vision(x,y,r=92):
 circle(x,y,r,'#a1b197')
 for i,t in enumerate(['开发者','社会大众','全球南方']):
  a=-math.pi/2+i*math.tau/3;xx=x+r*math.cos(a);yy=y+r*math.sin(a)
  circle(xx,yy,26,'#a1b197','#e3ead7');txt(t,xx,yy-6,10,align='center')
  if i==0:
   circle(xx,yy,47,'#a1b197',width=.5)
   for j,n in enumerate(['Learner','Builder','Engineer']):
    aa=-math.pi/2+j*math.tau/3;xxx=xx+47*math.cos(aa);yyy=yy+47*math.sin(aa)
    circle(xxx,yyy,2,INK,INK);txt(n,xxx,yyy+5,6.7,MUTED,align='center')
 circle(x,y,39,'#a1b197','#d8e5c4');txt('AI 普惠',x,y-12,16,bold=True,align='center');txt('共同目标',x,y+12,8,MUTED,align='center')
def forces(x,y,r=79):
 for xx in [x-r*.62,x+r*.62]:circle(xx,y,r,'#819a76',width=1.1)
 txt('开源之力',x-r*.87,y-15,13,bold=True,align='center');txt('降低门槛',x-r*.87,y+9,9,MUTED,align='center')
 txt('开发者之力',x+r*.87,y-15,13,bold=True,align='center');txt('拓展价值',x+r*.87,y+9,9,MUTED,align='center')
 txt('项目',x,y-17,9,MUTED,align='center');txt('社区',x,y+4,9,MUTED,align='center')
 line(x,y+r,x,y+r+22,'#819a76');txt('数字公共品',x,y+r+28,10,align='center')
def wheel(x,y,r,title,steps):
 fg=LIME if dark else INK;stroke='#799879' if dark else '#92a184';bg=FOREST if dark else PAPER
 circle(x,y,r,stroke);circle(x,y,r*.53,stroke,width=.4)
 txt(title,x,y-8,15,fg,bold=True,align='center')
 for i,t in enumerate(steps):
  a=-math.pi/2+i*math.tau/len(steps);xx=x+r*math.cos(a);yy=y+r*math.sin(a)
  box(xx-32,yy-13,64,26,bg,13);line(xx-22,yy+14,xx+22,yy+14,stroke,.5);txt(t,xx,yy-5,9,fg,align='center')
  a+=math.pi/len(steps);xx=x+r*math.cos(a);yy=y+r*math.sin(a);circle(xx,yy,2.5,fg,fg)
def network(x,y,r):
 pts=[(x,y)]+[(x+r*math.sqrt(j/74)*math.cos(j*2.399963),y+r*.82*math.sqrt(j/74)*math.sin(j*2.399963)) for j in range(1,74)]
 for i in range(1,len(pts)):
  for j in sorted(range(i),key=lambda j:math.dist(pts[i],pts[j]))[:2]:line(*pts[i],*pts[j],'#aab89e',.5)
 for i,(xx,yy) in enumerate(pts):circle(xx,yy,2 if i%7 else 3.1,'#819a76','#819a76')
 circle(x,y,43,LINE,PAPER);txt('数字公共品',x,y-13,13,bold=True,align='center');txt('共享 · 复用 · 共创',x,y+11,8,MUTED,align='center')
 for xx,yy,t in [(x-135,y-90,'学习'),(x+141,y-45,'工作'),(x+30,y+112,'社区'),(x-144,y+53,'本地实践')]:
  box(xx-27,yy-10,54,20,PAPER,10);txt(t,xx,yy-4,9,align='center')
def growth(x,y,w,h):
 sys.path.insert(0,str(ROOT/'scripts/publication'));from geometry import growth_art
 s=growth_art(lambda *a,**k:'')
 css='text{font-family:CN;fill:#173b31;text-anchor:middle}.label{font-size:20px}.growth-subtitle{font-size:14px}.caption{font-size:16px}.growth-base{fill:none;stroke:#d2d8c9;stroke-width:4px}.growth-line{fill:none;stroke:#69875e;stroke-width:2.2px}.growth-label circle{fill:#f7f6ef;stroke:#92a184;stroke-width:1px}.growth-bud circle{fill:#69875e}.bud-aura{fill:#e0e8d1}.growth-leaf{fill:#8ca774}'
 s='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="550"><style>'+css+'</style>'+s+'</svg>'
 d=svg2rlg(io.BytesIO(s.encode()));scale=min(w/600,h/550);d.scale(scale,scale);renderPDF.draw(d,c,x,H-y-550*scale)

# 01 / Cover
page(is_dark=True);c.bookmarkPage('cover');c.addOutlineEntry('AI 普惠宣言','cover',0,False)
txt('OPENNESS FOR EVERYONE',M,102,9,LIME)
txt('AI 普惠宣言',M,143,43,bold=True)
txt('让 AI 用得起，更用得好',M,211,19,LIME)
orbit(W/2,459,137)
txt('一心普惠 · 二力相生 · 三重飞轮',W/2,671,13,LIME,align='center')
txt('万千可能 · 生生不息',W/2,700,13,LIME,align='center')
txt('X-lab AI 开放实验室',M,758,10)
txt('设计阅读版 / v1.2',W-M,758,9,LIME,align='right')

# 02 / Preface and clickable contents
page('共同的方向，公开的承诺。','PRELUDE / 序言')
y=paras(intro,M,192,IW,12,22)
txt('阅读路径',M,y+18,13,bold=True);line(M,y+48,W-M,y+48)
targets=[3,4,5,7,8]
for i,(sec,pn) in enumerate(zip(sections,targets)):
 yy=y+65+i*40;txt(f'0{i+1}',M,yy,10,MUTED);txt(sec['title'],M+45,yy-2,15,bold=True);txt(f'{pn:02d}',W-M,yy,10,MUTED,align='right')
 c.linkRect('',f'p{pn}',(M,H-yy-24,W-M,H-yy+3),relative=0,thickness=0)
txt(blocks[2],M,726,9,MUTED)
txt('正文与正式网站 v1.2 一致；几何图形延续主站与互动演示。',M,751,8.5,MUTED)

# 03 / Vision
page('一心普惠','01 / A SHARED VISION')
para(sections[0]['blocks'][0],M,182,220,17,27)
paras(sections[0]['blocks'][1:3],M,252,225,10.5,18)
vision(422,318,82)
line(M,452,W-M,452)
y=paras(sections[0]['blocks'][3:],M,478,IW,11,19)

# 04 / Open source and developers
page('二力相生','02 / TWO REINFORCING FORCES')
para(sections[1]['blocks'][0],M,181,IW,16,25)
forces(W/2,309,70)
y=paras(sections[1]['blocks'][1:],M,430,IW,10.5,18)

# 05 / Three cycles and data
page('三重飞轮','03 / EVIDENCE · PEOPLE · VALUE',True)
y=paras(sections[2]['blocks'][:2],M,183,IW,11,20)
for i,(title,sub) in enumerate([('数据','支撑判断'),('人才','推动创造'),('价值','促进投入')]):
 x=133+i*164;circle(x,380,45,'#75906f');circle(x,380,34,'#75906f',width=.4);txt(title,x,361,19,LIME,bold=True,align='center');txt(sub,x,390,9,PAPER,align='center')
 if i<2:txt('↔',x+81,368,18,LIME,align='center')
line(M,459,W-M,459,'#527063')
wheel(166,623,86,'数据飞轮',['数据采集','基准建设','平台支撑','评价应用'])
txt('数据飞轮',306,492,18,LIME,bold=True)
paras(sections[2]['blocks'][3:5],306,535,241,10.5,19)

# 06 / Talent and value cycles
page('让创造与投入相互促进','03 / TALENT & VALUE',True)
wheel(155,287,82,'人才飞轮',['贡献评价','成长可见','人才汇聚','供给改善','普惠增进'])
paras(sections[2]['blocks'][6:8],290,189,257,10.2,18)
line(M,440,W-M,440,'#527063')
wheel(155,568,82,'价值飞轮',['资源投入','贡献识别','价值回馈','成效验证'])
paras(sections[2]['blocks'][9:11],290,467,257,10.2,18)
paras(sections[2]['blocks'][11:],M,711,IW,10,17)

# 07 / Possibilities
page('万千可能','04 / A WORLD OF POSSIBILITIES')
para(sections[3]['blocks'][0],M,183,IW,16,25)
network(W/2,375,172)
line(M,521,W-M,521)
paras(sections[3]['blocks'][1:],M,552,IW,11.5,21)

# 08 / Renewal
page('生生不息','05 / CONTINUOUS RENEWAL')
para(sections[4]['blocks'][0],M,181,IW,16,25)
growth(118,199,360,305)
paras(sections[4]['blocks'][1:-2],M,506,IW,11,19)

# 09 / Panorama and invitation
page('五层相连，就是 AI 普惠的全景。','FROM VISION TO PRACTICE')
labels=[('一','一心普惠','让 AI 用得起，更用得好。'),('二','二力相生','以开源降低门槛，以创造拓展可能。'),('三','三重飞轮','数据 · 人才 · 价值'),('万','万千可能','共享成果，连接多样实践。'),('生','生生不息','让每一轮实践，成为下一轮的起点。')]
line(77,222,77,488,'#94a583',1)
for i,(g,t,sub) in enumerate(labels):
 yy=222+i*67;circle(77,yy,21,'#a5b295',PALE);txt(g,77,yy-10,21,align='center');txt(t,118,yy-17,17,bold=True);txt(sub,118,yy+10,10,MUTED)
y=para(sections[4]['blocks'][-2],M,541,IW,11,20)
y=para(sections[4]['blocks'][-1],M,y+5,IW,14,25)
box(M,708,IW,56,INK,3);txt('阅读宣言',M+18,726,11,PAPER,bold=True);txt('观看互动演示',M+145,726,11,PAPER,bold=True);txt('参与共建',M+315,726,11,PAPER,bold=True)
for x,w,url in [(M,120,'https://www.x-lab.info/ai-for-all/?lang=zh'),(M+127,164,'https://www.x-lab.info/ai-for-all/presentation/?lang=zh'),(M+297,200,'https://github.com/X-lab2017/ai-for-all/issues')]:c.linkURL(url,(x,H-764,x+w,H-708),relative=0,thickness=0)
c.save();print(f'Created {page_no} pages: {args.output}')
