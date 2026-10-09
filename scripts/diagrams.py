"""Canonical bilingual diagram data and accessible, dependency-free SVG/HTML exports."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
def L(zh,en):return {'zh':zh,'en':en}
def N(id,zh,en,subzh,suben,detailzh,detailen,desktop,mobile,kind='normal',group=''):
 return dict(id=id,title=L(zh,en),sub=L(subzh,suben),detail=L(detailzh,detailen),desktop=desktop,mobile=mobile,kind=kind,group=group)
def E(fr,to,path,kind='arrow',group=''):return dict(fr=fr,to=to,path=path,kind=kind,group=group)
DIAGRAMS=[]
DIAGRAMS.append(dict(id='inclusion-views',label=L('三重普惠','THREE PERSPECTIVES'),title=L('从不同视角，看见真实需要','Understand needs through different perspectives'),summary=L('开发者、大众与全球南方，提供三个相互补充的普惠视角。','Developers, the wider public and the Global South offer complementary perspectives on inclusion.'),note=L('三个视角相互补充，不是先后阶段。','Complementary perspectives, not sequential stages.'),default='shared',height={'desktop':340,'mobile':580},nodes=[
 N('developers','开发者普惠','Developers','学习 · 创造 · 协作','Learn · Create · Collaborate','支持专业工程师，也为初学者提供入口。关注学习机会、实践能力与协作体验，让更多人能够参与公共品的创造。','Support professional engineers and give beginners an entry point. Attend to learning opportunities, practical capability and collaboration.',[20,25,280,120],[25,20,310,100]),
 N('public','大众普惠','The wider public','可用的成果 · 实际的帮助','Useful results · Real help','从使用者的需要出发，检查公共品及其应用是否易于理解、负担和使用，是否帮助人们学习、工作与改善处境。','Start with users’ needs. Examine whether public goods and their applications are understandable, affordable and useful in people’s lives.',[340,25,280,120],[25,150,310,100]),
 N('south','全球南方普惠','The Global South','地域视角 · 本地实践','Regional perspectives · Local practice','关注不同地区的语言、资源条件与发展机会，与当地伙伴共同理解需求、探索适合的实践，拓展普惠的地域视角。','Attend to languages, resource conditions and development opportunities. Work with local partners to understand needs and explore appropriate practice.',[660,25,280,120],[25,280,310,100]),
 N('shared','更多人的机会与能力','More opportunity and capability','AI 普惠的共同目标','The shared goal of AI for All','三个视角共同帮助我们判断谁获得了什么帮助、哪些需要仍未被回应。不同视角可以重叠，不代表三类互斥人群。','Together, these perspectives help examine who benefits and which needs remain unmet. They may overlap; they are not exclusive groups.',[210,220,540,100],[25,450,310,110],'accent')],edges={'desktop':[E('developers','shared','M160 145 V182 H480 V220','line'),E('public','shared','M480 145 V220','line'),E('south','shared','M800 145 V182 H480','line')],'mobile':[E('developers','shared','M25 70 H10 V430 H180 V450','line'),E('public','shared','M25 200 H10','line'),E('south','shared','M25 330 H10','line')]},labels=[]))
DIAGRAMS.append(dict(id='goal-path',label=L('一个目标','ONE GOAL'),title=L('AI 经由数字公共品，走向普惠','Connect AI to inclusion through public goods'),summary=L('AI 能力形成数字公共品，经采用和本地化，让更多人实际受益。','AI enables digital public goods; adoption and local adaptation turn them into real benefit.'),note=L('实际受益需要应用与证据来检验。','Real benefit needs adoption and evidence.'),default='dpg',height={'desktop':320,'mobile':640},nodes=[
 N('ai','AI 能力','AI capabilities','技术与人的创造','Technology and human creativity','以开放技术和开发者创造力为起点，将 AI 能力用于真实问题，形成可以分享、改进与维护的成果。','Start with open technology and developer creativity, applying AI to real problems and producing work people can share, improve and maintain.',[20,70,200,120],[40,20,280,100]),
 N('dpg','数字公共品','Digital public goods','DPG · 可共享、可复用','DPGs · Shareable and reusable','公共品承载可以持续共享的软件、AI 系统、数据与知识。关注开放许可、复用条件、公共价值与负责任的使用。','Public goods carry shareable software, AI systems, data and knowledge. Attend to open licensing, reuse, public value and responsible use.',[260,70,200,120],[40,175,280,100],'accent'),
 N('adoption','采用与本地化','Adoption and adaptation','走进真实场景','Use in real settings','维护、文档、服务与本地化帮助公共品进入实际使用。根据语言、成本与场景改进，让开放成果成为可用的帮助。','Maintenance, documentation, services and local adaptation enable real use. Respond to languages, costs and contexts so open resources become useful.',[500,70,200,120],[40,330,280,100]),
 N('benefit','AI 普惠','AI for All','更多人学习、创造与受益','More people learn, create and benefit','通过参与者体验和实际变化检验成效。关注谁获得帮助、是否形成能力，以及哪些需要仍未被回应，并将反馈带回公共品改进。','Examine experience and actual changes: who receives help, what capabilities grow and which needs remain unmet. Feed this evidence back into improvement.',[740,70,200,120],[40,485,280,110],'accent')],edges={'desktop':[E('ai','dpg','M220 130 H252'),E('dpg','adoption','M460 130 H492'),E('adoption','benefit','M700 130 H732'),E('benefit','dpg','M840 190 V265 H360 V198','feedback')],'mobile':[E('ai','dpg','M180 120 V167'),E('dpg','adoption','M180 275 V322'),E('adoption','benefit','M180 430 V477'),E('benefit','dpg','M40 540 H15 V225 H32','feedback')]},labels=[('desktop',590,253,'使用反馈与持续改进','Feedback and improvement')]))
DIAGRAMS.append(dict(id='dual-forces',label=L('两股力量','TWO FORCES'),title=L('开源降低门槛，创造带来价值','Open source lowers barriers; people create value'),summary=L('开源之力与开发者之力相互促进，共同创造和维护数字公共品。','Open source and developers reinforce each other to create and maintain digital public goods.'),note=L('“×”表达相互促进的理念，不是定量公式。','“×” expresses mutual reinforcement, not a quantitative formula.'),default='commons',height={'desktop':420,'mobile':590},nodes=[
 N('open','开源之力','Open source','用得起\nAI Infra · AI Model · AI Agent','Affordable access\nAI Infra · AI Model · AI Agent','开放的技术、知识和文档降低进入门槛。清晰许可、持续维护和实际使用成本，共同影响技术能否被长期获取与复用。','Open technology, knowledge and documentation lower barriers. Clear licensing, maintenance and real costs shape sustained access and reuse.',[40,40,365,155],[25,20,310,150]),
 N('people','开发者之力','Developers','用得好\nAI Learner · AI Builder · AI Engineer','Capable use\nAI Learner · AI Builder · AI Engineer','学习、作品、协作和反馈连接成长。支持不同阶段的人发展技术能力、判断力与责任意识，把工具用于有意义的问题。','Learning, useful work, collaboration and feedback support growth. Develop technical skills, judgment and responsibility through meaningful problems.',[555,40,365,155],[25,220,310,150]),
 N('commons','共同创造与维护','Create and maintain together','让数字公共品持续丰富','Enrich digital public goods','项目与社区让两股力量相遇。更多人的参与带来工具、知识与维护力量，改善开放技术，又为新的学习和创造提供基础。','Projects and communities bring both forces together. More participants contribute tools, knowledge and maintenance, improving the foundations for further learning and creation.',[245,285,470,110],[25,460,310,110],'accent')],edges={'desktop':[E('open','commons','M222 195 V240 H480 V277'),E('people','commons','M737 195 V240 H480','line'),E('commons','open','M245 340 H75 V203','feedback')],'mobile':[E('open','commons','M335 95 H350 V410 H180 V452'),E('people','commons','M180 370 V452'),E('commons','open','M25 515 H10 V95 H17','feedback')]},labels=[('desktop',480,130,'×','×'),('mobile',180,205,'×','×')]))
DIAGRAMS.append(dict(id='evaluation-core',label=L('一个内核','ONE SHARED CORE'),title=L('让贡献可见，让行动有据','Make contributions visible and actions accountable'),summary=L('平台、数据、基准与理论共同支持数据与评价内核。','Platforms, data, benchmarks and research jointly support the data and evaluation core.'),note=L('四类工作协同配合，不是先后流程。','Four complementary roles, not a fixed sequence.'),default='core',height={'desktop':460,'mobile':640},nodes=[
 N('platform','评价平台','Platforms','连接参与者与实践\nOpenShare','Connect people and practice\nOpenShare','平台连接贡献、能力和资源需求，让识别结果能够进入实践。OpenShare 提供开发者经济生态的探索入口。','Platforms connect contributions, capabilities and resource needs so insights can inform practice. OpenShare explores a developer economic ecosystem.',[25,30,295,130],[15,20,155,140]),
 N('data','评价数据','Data','提供可追溯的证据\nOpenDigger','Traceable evidence\nOpenDigger','OpenDigger 汇集开源相关数据并生产指标，为理解协作、社区和生态提供基础。数据需要解释覆盖范围、时间口径与局限。','OpenDigger brings together open-source data and produces metrics for understanding collaboration and communities. Coverage, time periods and limitations need explanation.',[640,30,295,130],[190,20,155,140]),
 N('core','数据与评价','Data and evaluation','识别贡献 · 支持成长 · 检验效果','Recognize · Support · Examine','共同内核连接证据与行动。评价应服务于人的成长，尊重多种贡献和知情选择，允许质疑、纠错与持续改进。','The shared core connects evidence with action. Evaluation serves human development, respects varied contributions and informed choice, and remains open to correction.',[320,185,320,100],[40,240,280,120],'accent'),
 N('methods','评价方法与基准','Methods and benchmarks','解释贡献与发展\nOpenRank / OSIDX','Interpret contribution and development\nOpenRank / OSIDX','OpenRank 从协作网络分析贡献与影响力；OSIDX 的发展指数工作拓展生态观察。方法需要结合场景解释，不能把单一指标当作全部价值。','OpenRank examines contribution and influence through collaboration networks; OSIDX work extends ecosystem observation. Interpret methods in context, beyond a single metric.',[25,335,295,100],[15,460,155,150]),
 N('research','评价理论与研究','Evaluation research','检验方法本身\nBenchCouncil','Examine the methods\nBenchCouncil','参考 BenchCouncil 等评价科学研究，明确评价对象、方法和证据，持续检验评价的有效性与局限。','Draw on evaluation science, including BenchCouncil research, to clarify objects, methods and evidence and examine validity and limitations.',[640,335,295,100],[190,460,155,150])],edges={'desktop':[E('platform','core','M320 95 H365 V185','line'),E('data','core','M640 95 H595 V185','line'),E('methods','core','M320 385 H365 V285','line'),E('research','core','M640 385 H595 V285','line')],'mobile':[E('platform','core','M92 160 V200 H130 V240','line'),E('data','core','M268 160 V200 H230 V240','line'),E('methods','core','M92 460 V410 H130 V360','line'),E('research','core','M268 460 V410 H230 V360','line')]},labels=[]))
# Both cycles preserve the reviewed causal links; all arrows close back into practice.
cycle_nodes=[]
left=[('practice','贡献与实践数据','Practice data','观察真实协作','Observe collaboration','记录贡献、协作与实践，说明数据来源与覆盖范围。','Record contributions, collaboration and practice, with clear sources and coverage.'),('evaluate','多维评价','Multidimensional evaluation','解释贡献与局限','Interpret contributions','结合多种证据解释贡献，说明方法与局限。','Interpret contributions through varied evidence and explain methodological limits.'),('visible','贡献与成长可见','Visible contribution','看见成长路径','Make growth visible','让贡献与成长更容易被理解，为支持和参与提供依据。','Make contributions and growth understandable to inform support and participation.'),('talent','人才参与与成长','Participation and growth','吸引并支持参与','Attract and support people','吸引更多人参与，通过学习、协作和真实问题支持成长。','Attract participation and support growth through learning, collaboration and real problems.'),('supply','供给与应用改善','Better goods and use','公共品走向应用','Improve public goods','将成长转化为可维护的公共品与可用的应用，回应使用者需要。','Turn growth into maintainable public goods and usable applications that address needs.'),('feedback','新的贡献与效果','New evidence','带回实践数据','Return to practice data','把新的贡献、采用体验与受益变化带回数据与评价。','Return new contributions, adoption experience and observed outcomes to evaluation.')]
right=[('invest','企业与机构投入','Resource investment','资源支持实践','Resources for practice','企业与机构按明确条件投入技术、资金、实践机会等资源。','Businesses and institutions contribute technology, funding or opportunities under clear conditions.'),('match','贡献识别与匹配','Recognize and match','理解能力与需求','Understand needs','识别贡献与资源需求，在参与者自主选择的基础上匹配支持。','Understand contributions and resource needs, matching support with participants’ informed choice.'),('support','支持开发者\n与公共品','Support people and goods','连接资源与创造','Connect resources to creation','把资源投入学习、创造、维护与应用，让支持进入真实实践。','Direct resources to learning, creation, maintenance and adoption.'),('value','公共价值\n与合作回报','Public and partner value','观察实际变化','Observe actual changes','关注公共受益，以及人才合作、技术应用和生态洞察等合理回报。','Examine public benefit and reasonable partner benefits such as talent collaboration, adoption and insights.'),('evidence','投入效果核验','Examine outcomes','用证据支持判断','Evidence for decisions','结合证据与反馈核验投入效果，解释局限，不预设必然回报。','Examine effects with evidence and feedback, explain limitations and avoid assuming guaranteed returns.'),('reinvest','持续投入','Continued support','改进下一轮支持','Improve future support','根据实际价值和效果证据改进资源安排，让支持能够持续。','Use evidence of value and outcomes to improve resource decisions and sustain support.')]
positions=[(0,0),(245,0),(245,135),(245,270),(0,270),(0,135)]
mobile_positions=[(0,0),(175,0),(175,120),(175,240),(0,240),(0,120)]
for group,items,dx,my in [('growth',left,20,50),('value',right,510,495)]:
 for i,t in enumerate(items):
  id,zh,en,sz,se,dz,de=t;x,y=positions[i];mx,yy=mobile_positions[i]
  cycle_nodes.append(N(id,zh,en,sz,se,dz,de,[dx+x,70+y,215,105],[15+mx,my+yy,155,100],group=group))
cycle_nodes.append(N('shared-core','数据与评价','Data and evaluation','资源支持成长，价值证据支持投入','Resources support growth; evidence informs investment','两个飞轮共享证据与评价。资源支持人才与供给，人才与供给创造价值，效果证据帮助改进下一轮投入。','Both cycles share evidence and evaluation. Resources support people and supply; people create value; evidence helps improve the next round of investment.',[250,510,460,100],[20,890,320,115],'accent'))
cycle_edges={'desktop':[],'mobile':[]}
for mode in cycle_edges:
 for group,items in [('growth',left),('value',right)]:
  ids=[n[0] for n in items]
  ns=[next(n for n in cycle_nodes if n['id']==id) for id in ids]
  for i in range(6):
   a=ns[i][mode];b=ns[(i+1)%6][mode];x,y,w,h=a;X,Y,W,H=b
   if Y==y:
    path=f'M{x+w if X>x else x} {y+h/2} H{X-7 if X>x else X+W+7}'
   else:path=f'M{x+w/2} {y+h if Y>y else y} V{Y-7 if Y>y else Y+H+7}'
   cycle_edges[mode].append(E(ids[i],ids[(i+1)%6],path,'arrow',group))
cycle_edges['desktop'] += [E('shared-core','supply','M350 510 V480 H127 V445','line'),E('shared-core','evidence','M610 510 V480 H617 V445','line')]
cycle_edges['mobile'] += [E('shared-core','feedback','M20 945 H6 V220 H15','line'),E('shared-core','support','M340 945 H354 V665 H345','line')]
DIAGRAMS.append(dict(id='twin-flywheels',label=L('两个飞轮','TWO REINFORCING CYCLES'),title=L('让成长与投入，形成持续循环','Connect growth and resources in reinforcing cycles'),summary=L('人才与供给、资源与价值形成两个闭环，共用数据与评价内核。','People and supply, resources and value form two closed cycles around a shared data and evaluation core.'),note=L('关系需要在实践中检验，成效由证据说明。','Test these relationships in practice; explain outcomes with evidence.'),default='shared-core',height={'desktop':640,'mobile':1030},nodes=cycle_nodes,edges=cycle_edges,labels=[('desktop',250,32,'评价内核运转','People and supply'),('desktop',740,32,'生态价值再生','Resources and value'),('mobile',180,25,'评价内核运转','People and supply'),('mobile',180,470,'生态价值再生','Resources and value')]))

def esc(s):return html.escape(str(s),quote=True)
def wrap(text,width,fontsize):
 def units(t):return sum(1 if ord(c)>255 else .56 for c in t)*fontsize
 lines=[]
 for part in text.split('\n'):
  if units(part)<=width:lines.append(part);continue
  words=part.split() if ' ' in part else list(part);space=' ' if ' ' in part else ''
  buf=''
  for word in words:
   test=buf+space+word if buf else word
   if units(test)>width and buf:lines.append(buf);buf=word
   else:buf=test
  if buf:lines.append(buf)
 return lines

def svg(d,lang,mobile=False,export=False):
 mode='mobile' if mobile else 'desktop';w=360 if mobile else 980;h=d['height'][mode];pad=110 if export else 0;total=h+pad+(75 if export else 0);prefix=d['id']+'-'+lang+'-'+mode
 role='role="img" aria-labelledby="title desc"' if export else 'aria-hidden="true"'
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {total}" width="{w}" height="{total}" class="concept-svg" {role}>',f'<title id="{("title" if export else prefix+"-title")}">{esc(d["title"][lang])}</title><desc id="{("desc" if export else prefix+"-desc")}">{esc(d["summary"][lang])}</desc>',f'<defs><marker id="{prefix}-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L6 3.5 L0 7" fill="none" stroke="#708d81" stroke-width="1.2"/></marker></defs>','<rect width="100%" height="100%" fill="#ffffff"/>']
 if export:
  out += [f'<text x="20" y="27" font-family="Arial,sans-serif" font-size="12" letter-spacing="2" fill="#567467">X-LAB AI / AI FOR ALL / v1.1</text>',f'<text x="20" y="66" font-family="Arial,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="28" font-weight="600" fill="#143a2c">{esc(d["title"][lang])}</text>',f'<path d="M20 88 H960" stroke="#dce5df"/>']
 out.append(f'<g transform="translate(0,{pad})">')
 for ed in d['edges'][mode]:
  attrs=f' class="concept-edge" data-from="{ed["fr"]}" data-to="{ed["to"]}" data-group="{ed["group"]}"'
  out.append(f'<path{attrs} d="{ed["path"]}" fill="none" stroke="#8aa497" stroke-width="1.5"'+('' if ed['kind']=='line' else f' marker-end="url(#{prefix}-arrow)"')+(' stroke-dasharray="5 5"' if ed['kind']=='feedback' else '')+'/>')
 for m,x,y,zh,en in d.get('labels',[]):
  if m==mode:out.append(f'<text x="{x}" y="{y}" font-family="Arial,Source Han Sans SC,sans-serif" text-anchor="middle" font-size="{30 if zh=="×" else 15}" fill="#547464">{esc(zh if lang=="zh" else en)}</text>')
 for n in d['nodes']:
  x,y,nw,nh=n[mode];small=nw<180;fs=(17 if small else 22) if lang=='zh' else (15 if small else 19);subfs=(12 if small else 14) if lang=='zh' else (11.5 if small else 13)
  title=wrap(n['title'][lang],nw-24,fs);subs=wrap(n['sub'][lang],nw-24,subfs)
  lineh=fs+5;subh=subfs+5;block=len(title)*lineh+len(subs)*subh+5;ty=y+(nh-block)/2+fs
  out.append(f'<g class="concept-node" data-node="{n["id"]}" data-group="{n["group"]}"><rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="6" fill="{("#f1f8e9" if n["kind"]=="accent" else "#fff")}" stroke="{("#75a34d" if n["kind"]=="accent" else "#a1b5a9")}" stroke-width="1.4"/>')
  for t in title:
   out.append(f'<text x="{x+nw/2}" y="{ty}" text-anchor="middle" font-family="Arial,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="{fs}" font-weight="600" fill="#173b2b">{esc(t)}</text>');ty+=lineh
  ty+=4
  for t in subs:
   out.append(f'<text x="{x+nw/2}" y="{ty}" text-anchor="middle" font-family="Arial,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="{subfs}" fill="#567063">{esc(t)}</text>');ty+=subh
  out.append('</g>')
 out.append('</g>')
 if export:out.append(f'<path d="M20 {total-62} H960" stroke="#dce5df"/><text x="20" y="{total-36}" font-family="Arial,Source Han Sans SC,sans-serif" font-size="14" fill="#526d60">{esc(d["note"][lang])}</text><text x="20" y="{total-13}" font-family="Arial,sans-serif" font-size="11" fill="#718a7b">www.x-lab.info/ai-for-all/</text>')
 out.append('</svg>');return '\n'.join(out)

def figure(d,lang):
 legacy={'dual-forces':'access-capability','goal-path':'path-to-benefit','twin-flywheels':'learning-loop'}.get(d['id'])
 hint='点选节点，查看关系与解释。' if lang=='zh' else 'Select a node to explore its role and connections.'
 out=[f'<figure class="concept" id="{d["id"]}" aria-labelledby="{d["id"]}-heading"><figcaption><span class="concept-index">{esc(d["label"][lang])}</span><h3 id="{d["id"]}-heading">{esc(d["title"][lang])}</h3></figcaption><p class="concept-hint">{hint}</p>']
 if legacy:out.insert(0,f'<span class="anchor-alias" id="{legacy}" aria-hidden="true"></span>')
 out.append(f'<p class="visually-hidden">{esc(d["summary"][lang])}</p>')
 if d['id']=='twin-flywheels':
  out.append('<div class="cycle-controls" role="group" aria-label="'+('突出飞轮' if lang=='zh' else 'Highlight a cycle')+'">')
  for key,zh,en in [('all','查看双飞轮','Both cycles'),('growth','人才与供给','People and supply'),('value','资源与价值','Resources and value')]:out.append(f'<button type="button" data-cycle="{key}" aria-pressed="{str(key=="all").lower()}">{zh if lang=="zh" else en}</button>')
  out.append('</div>')
 for mobile in [False,True]:
  mode='mobile' if mobile else 'desktop';w=360 if mobile else 980
  out.append(f'<div class="concept-canvas concept-{mode}">{svg(d,lang,mobile)}<div class="concept-controls" role="group" aria-label="{esc(d["title"][lang])}">')
  for n in d['nodes']:
   x,y,nw,nh=n[mode];style=f'left:{100*x/w:.5f}%;top:{100*y/d["height"][mode]:.5f}%;width:{100*nw/w:.5f}%;height:{100*nh/d["height"][mode]:.5f}%'
   out.append(f'<button type="button" class="concept-hit" data-select="{n["id"]}" style="{style}" aria-pressed="{str(n["id"]==d["default"]).lower()}" aria-controls="{d["id"]}-detail"><span class="visually-hidden">{esc(n["title"][lang])}</span></button>')
  out.append('</div></div>')
 default=next(n for n in d['nodes'] if n['id']==d['default'])
 out.append(f'<div class="concept-detail" id="{d["id"]}-detail" role="status" aria-live="polite" aria-atomic="true"><strong>{esc(default["title"][lang])}</strong><p>{esc(default["detail"][lang])}</p></div>')
 out.append(f'<div class="concept-foot"><span>{esc(d["note"][lang])}</span><div><a href="assets/diagrams/{d["id"]}-{lang}.svg" download>SVG ↓</a><a href="assets/diagrams/{d["id"]}-{lang}.png" download>PNG ↓</a></div></div>')
 data={'default':d['default'],'nodes':{n['id']:{'title':n['title'][lang],'detail':n['detail'][lang]} for n in d['nodes']}}
 out.append('<script type="application/json" class="concept-data">'+json.dumps(data,ensure_ascii=False).replace('</',r'<\/')+'</script></figure>')
 return '\n'.join(out)
def export_all():
 dst=ROOT/'site/assets/diagrams';dst.mkdir(parents=True,exist_ok=True)
 for d in DIAGRAMS:
  for lang in ['zh','en']:(dst/f'{d["id"]}-{lang}.svg').write_text(svg(d,lang,export=True))
if __name__=='__main__':export_all()
