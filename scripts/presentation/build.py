from pathlib import Path
import json, math, re, html
from geometry import vision_art, network_art, growth_art

ROOT=Path(__file__).parent
OUT=ROOT.parents[1]/'site/presentation'
def svg(s,label,view='0 0 600 540'):
 return f'<svg viewBox="{view}" role="img" aria-label="{label}">{s}</svg>'
def text(x,y,t,cls='label'):
 return f'<text x="{x}" y="{y}" class="{cls}">{t}</text>'
def circle(cx,cy,r):return f'M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0'
def loop(path,id,count=3,guide=False):
 return f'<path id="{id}" class="trace" d="{path}"/>'+''.join(f'<circle class="traveler bead-{i%3}" r="{4+i%2}" data-track="{id}" data-phase="{i/count}" data-period="{32000+i*3000}"/>'for i in range(count))
def art(s,label,view='0 0 600 540'):
 return '<div class="art motion-area">'+svg(s,label,view)+'</div>'
def buttons(items,kind='step'):
 return '<div class="choices">'+''.join(f'<button data-{kind}="{i}" aria-pressed="{str(i==0).lower()}"><span>0{i+1}</span>{x}</button>'for i,x in enumerate(items))+'</div>'
def head(k,t,sub):return f'<div class="eyebrow">{k}</div><h2>{t}</h2><p class="subtitle">{sub}</p>'
def detail(title,body):return f'<div class="detail" aria-live="polite"><h3>{title}</h3><p>{body}</p></div>'

LFX='https://insights.linuxfoundation.org/project/korg/contributors?timeRange=past365days&start=2025-10-10&end=2026-10-10'
LINUX='https://www.linuxfoundation.org/blog/celebrating-35-years-of-linux-the-open-source-engine-powering-three-decades-of-global-innovation-and-infrastructure'
ATOM='https://www.atomproject.ai/'
REPORT='https://arxiv.org/html/2604.07190v2'
OFFICIAL='https://www.x-lab.info/ai-for-all/'
REPO='https://github.com/X-lab2017/ai-for-all'
sources={
 'linux': [{'label':'Linux Foundation · 35 周年报告摘要（2026-10-06）','url':LINUX,'note':'TOP500 全部 500 台超级计算机；每 8–9 周发布新版本；平均每小时近 10 次变更。均为该报告发布时的描述。'}, {'label':'LFX Insights · 用户指定贡献面板','url':LFX,'note':'指定区间为 2025-10-10 至 2026-10-10。本次动态数据未完整返回，未引用该区间的贡献人数、机构数或排名；保留原链接供查阅。'}],
 'models':[{'label':'ATOM Project · 开放模型观察','url':ATOM,'note':'背景与项目入口。开放模型包含不同开放程度的模型，各模型版本许可分别适用。'}, {'label':'The ATOM Report · v2（2026-05-25），§2–3','url':REPORT,'note':'下载：截至 2026 年 3 月，所跟踪 Hugging Face 模型累计中国 11.5 亿、美国 7.23 亿、欧洲 1.63 亿。衍生模型：2026 年 2 月新增衍生模型中，中国基础模型占 70%。按发布机构总部归属；样本覆盖有限，下载不等于独立用户或实际使用量。'}],
 'manifesto':[{'label':'AI 普惠宣言 · v1.2 正式全文','url':OFFICIAL,'note':'本演示为审定宣言的讲述性摘要。飞轮结构与角色表述以正式正文为准。'}]
}
slides=[]
def add(id,title,body,notes,theme='light',source='manifesto',seconds=12,steps=None):
 slides.append(dict(id=id,title=title,body=body,notes=notes,theme=theme,source=source,seconds=seconds,steps=steps or []))

add('manifesto','AI 普惠宣言','''<div class="cover-orbits motion-area">'''+svg(loop('M160 250 C160 40 1440 40 1440 250 C1440 460 160 460 160 250','cover-orbit',7),'围绕共同愿景缓慢运行的光点','0 0 1600 500')+'''</div><div class="cover-copy"><div class="eyebrow">A I &nbsp; F O R &nbsp; A L L</div><h1>AI 普惠宣言</h1><div class="gold-rule"></div><p class="cover-sub">让 AI 用得起，更用得好。</p><p class="cover-small">让更多人参与创造，共享技术进步的成果。</p><div class="cover-framework">一心普惠 <i>·</i> 二力相生 <i>·</i> 三重飞轮 <i>·</i> 万千可能 <i>·</i> 生生不息</div></div>''',
 '开场先停留，让观众看见宣言标题。我们的共同主张是：让 AI 用得起，更用得好。接下来用两个开放协作的故事引入，再讲清愿景、力量和持续运转的机制。',theme='dark',seconds=10)

linux_visual='<g class="linux-halo">'+''.join(f'<circle class="orbit" cx="300" cy="240" r="{r}"/>'for r in [105,168,224])+loop(circle(300,240,168),'linux-loop',6)+loop(circle(300,240,224),'linux-outer',5)+'</g>'
linux_visual+='<circle class="kernel-core" cx="300" cy="240" r="91"/>'+text(300,225,'Linux','kernel-name')+text(300,265,'KERNEL','tiny')
for x,y,name in [(300,45,'开发者'),(501,240,'企业'),(300,452,'使用者'),(99,240,'维护者')]:
 linux_visual+=f'<circle class="small-ball" cx="{x}" cy="{y}" r="37"/>'+text(x,y+6,name,'label')
regions=[('美国','258','26%','642','7%'),('德国','83','8%','236','3%'),('中国','44','4%','214','2%'),('英国','35','3%','122','1%'),('法国','31','3%','','')]
orgrows=[('美国',258,'26%'),('德国',83,'8%'),('中国',44,'4%'),('英国',35,'3%'),('法国',31,'3%')]
conrows=[('美国',642,'7%'),('德国',236,'3%'),('印度',219,'2%'),('中国',214,'2%'),('英国',122,'1%')]
def region_table(rows,kind):
 return '<table class="region-table"><thead><tr><th>地区</th><th>'+kind+'</th><th>占比</th></tr></thead><tbody>'+''.join(f'<tr><td>{n}</td><td>{v:,}</td><td>{pct}</td></tr>'for n,v,pct in rows)+'</tbody></table>'
linux_data='<div class="linux-data"><div class="eyebrow">LINUX KERNEL · GLOBAL COLLABORATION</div><div class="lfx-tabs" role="tablist" aria-label="全球协作数据"><button id="lfx-tab-0" role="tab" data-lfx="0" aria-selected="true" aria-controls="lfx-panel-0">组织</button><button id="lfx-tab-1" role="tab" data-lfx="1" aria-selected="false" aria-controls="lfx-panel-1" tabindex="-1">贡献者</button></div><div id="lfx-panel-0" role="tabpanel" aria-labelledby="lfx-tab-0">'+region_table(orgrows,'组织数')+'</div><div id="lfx-panel-1" role="tabpanel" aria-labelledby="lfx-tab-1" hidden>'+region_table(conrows,'贡献者数')+'</div><p class="source-line">LFX Insights 截图 · 所示地区摘录，非全球总量</p><div class="linux-proof"><div><b>500 / 500</b><span>TOP500 超级计算机</span></div><div><b>8–9 周</b><span>新版本发布周期</span></div></div></div>'
linux_cover=f'<figure class="report-cover"><a href="https://www.linuxfoundation.org/research/35-years-of-linux" target="_blank" rel="noopener"><img src="assets/linux-report-cover.png" alt="Linux Foundation《35 Years of Linux》报告封面，2026 年 10 月"></a><figcaption>Linux Foundation Research · October 2026<br><a href="https://www.linuxfoundation.org/research/35-years-of-linux" target="_blank" rel="noopener">阅读 35 周年报告 ↗</a></figcaption></figure>'
add('linux','Linux 35 年',head('01 / 开放的故事','Linux 35 年','从个人项目，到全球组织与开发者共同维护的基础。')+'<div class="linux-evidence">'+linux_data+linux_cover+'</div>',
 'Linux 诞生于 1991 年，2026 年迎来 35 周年。左侧根据用户提供的 LFX Insights 地域分布截图，分别列出组织与贡献者数据。例如美国 258 家组织、642 名贡献者；中国 44 家组织、214 名贡献者。两个视角的地区列表不同，不能混作统一排名。截图未显示完整筛选条件与全球总量，因此只展示原图所示数值及占比，不以百分比反推总人数，也不将地域占比等同于贡献量占比。右侧为 2026 年 10 月 Linux Foundation 报告封面。报告称 TOP500 全部使用 Linux，内核每 8–9 周发布新版本。故事的重点是长期协作与共同维护。',source='linux',seconds=16)
sources['linux'][1]['note']='依据用户于 2026-10-10 提供的两张 LFX 地域分布截图转录。组织：美国 258（26%）、德国 83（8%）、中国 44（4%）、英国 35（3%）、法国 31（3%）。贡献者：美国 642（7%）、德国 236（3%）、印度 219（2%）、中国 214（2%）、英国 122（1%）。截图未含完整筛选条件与全球总量；不反推总量，不将地域占比解释为贡献活动占比。原链接保留用户指定年度区间，截图数据不作为该区间已独立核验的统计。'
sources['linux'] += [{'label':'原始截图 · 组织地域分布','url':'assets/lfx-organizations.png','note':'用户提供截图，保留原图便于核对。'},{'label':'原始截图 · 贡献者地域分布','url':'assets/lfx-contributors.png','note':'用户提供截图，保留原图便于核对。'}]

model_logos=''.join(f'<div class="model-logo"><img src="assets/{f}" alt="{name}"><span>{zh}<small>{name}</small></span></div>'for f,zh,name in [('qwen.png','阿里巴巴','Qwen'),('deepseek.svg','深度求索','DeepSeek'),('glm.svg','智谱 AI','GLM'),('kimi.png','月之暗面','Kimi'),('hunyuan.png','腾讯','混元 Hunyuan')])
bars=''.join(f'<div class="bar-row"><span>{name}</span><div class="bar-track"><i style="width:{val/11.5*100}%"></i></div><b>{val:g}<small> 亿</small></b></div>'for name,val in [('中国',11.5),('美国',7.23),('欧洲',1.63)])
add('models','开放模型的力量',head('02 / 开放的故事','开放模型的力量','中国贡献，正在成为全球开发者再创造的基础。')+f'<div class="model-layout"><div class="chart"><div class="chart-title">所跟踪模型的累计下载量 <span>截至 2026.03</span></div>{bars}<p class="source-line">Hugging Face · ATOM 所跟踪样本 · 按发布机构总部归属</p></div><div class="derivative"><b>70<span>%</span></b><h3>新增衍生模型<br>基于中国模型</h3><p>2026 年 2 月 · ATOM 样本</p></div></div><div class="model-strip">{model_logos}</div><p class="footnote">代表性模型系列示意，不构成排名。开放程度与许可因版本而异；下载量不等于使用人数。来源：ATOM Report v2，2026-05-25。</p>',
 '这一页聚焦中国模型对开放生态的贡献。ATOM 报告跟踪的 Hugging Face 样本显示，截至 2026 年 3 月，中国机构模型累计下载约 11.5 亿；2026 年 2 月新增衍生模型中，70% 基于中国模型。这里按模型发布机构总部归属，不是下载用户的国籍。下载与衍生模型反映采用和再创造的线索，不直接等于使用人数，也不代表所有渠道。下方展示五个代表性模型系列，不是排行榜。过渡：能力开放带来了机会，如何把机会转化为普惠？',source='models',seconds=16)

vision_steps=[['面向开发者','支持学习者积累能力、构建者完成应用、工程师保障可靠运行。'],['面向社会大众','让技术进入工作与生活，让更多人能够参与、能够使用、能够受益。'],['面向全球南方','尊重当地语言、资源条件与实践经验，与当地伙伴共同建设适宜的方案。']]
add('vision','一心普惠',head('一 / 共同愿景','一心普惠','让 AI 用得起，更用得好。')+'<div class="split"><div class="copy"><p class="large-copy">降低获取与使用成本，<br>提升理解、判断与创造能力。</p>'+buttons(['开发者','社会大众','全球南方'])+detail(*vision_steps[0])+'<p class="small-note">三个互补视角，共同指向以人为本的 AI 普惠。</p></div>'+art(vision_art(),'AI 普惠完整中心球与三个视角及角色卫星','0 0 640 640')+'</div>',
 '我们坚持以人为本。用得起是降低技术获取和持续使用的成本；用得好是增强理解、判断和创造的能力。三个视角互相补充：开发者、社会大众和全球南方。可点选左侧视角展开说明；中心始终保持完整，象征共同目标。',steps=vision_steps)

forces='<defs><clipPath id="overlap"><circle cx="218" cy="250" r="137"/></clipPath></defs><circle class="lens" cx="382" cy="250" r="137" clip-path="url(#overlap)"/>'+loop(circle(218,250,137),'force-open',4)+loop(circle(382,250,137),'force-people',4)+text(182,239,'开源之力')+text(182,271,'降低门槛','tiny')+text(418,239,'开发者之力')+text(418,271,'拓展价值','tiny')+text(300,242,'项目','tiny')+text(300,267,'社区','tiny')+'<path class="spoke" d="M300 390V429"/><rect class="small-ball" x="224" y="429" width="152" height="49" rx="25"/>'+text(300,461,'数字公共品')
forces_steps=[['开源之力','清晰许可、易懂文档、可复用成果与持续维护，让更多人能够进入。'],['开发者之力','学习、判断、实践与协作，把可获得的技术转化为有用的成果。'],['共同成果','通过复用、推广和本地化，让数字公共品成为广泛可及的实际帮助。']]
add('forces','二力相生',head('二 / 相互促进','二力相生','以开源降低门槛，以创造拓展可能。')+'<div class="split"><div class="copy">'+buttons(['开放','创造','共享成果'])+detail(*forces_steps[0])+'<div class="pathway"><span>AI 能力</span><i>→</i><span>数字公共品</span><i>→</i><span>AI 普惠</span></div><p class="small-note">开放支持创造，创造丰富开放。</p></div>'+art(forces,'开源与开发者两股力量交汇于项目与社区')+'</div>',
 '两股力量不是各自独立的口号。开放让技术更容易获得和复用，开发者通过学习、判断与实践，让它回应真实需要。二者在项目和社区中相遇，形成开放共享的软件、数据、知识和方案，再经过复用与本地化转化为实际帮助。',steps=forces_steps)

overview=''
for k,(cx,cy,title,desc,target) in enumerate([(300,148,'数据','证据 · 判断',7),(156,390,'人才','能力 · 创造',8),(444,390,'价值','资源 · 持续',9)]):
 overview+=loop(circle(cx,cy,102),f'overview-{k}',3)
 overview+=f'<a href="#s{target}" aria-label="展开{title}飞轮"><circle class="wheel-core" cx="{cx}" cy="{cy}" r="75"/>'+text(cx,cy-5,title+'飞轮','center')+text(cx,cy+26,desc,'tiny')+'</a>'
overview='<path class="spoke" d="M300 240L206 316 M249 390H351 M395 306L345 231"/>'+overview
add('flywheels','三重飞轮',head('三 / 运行机制','三重飞轮','以数据支撑判断，以人才推动创造，以价值促进投入。')+'<div class="split"><div class="copy"><p class="large-copy">连接证据、能力与资源，<br>让每一轮实践支持下一轮。</p><div class="wheel-links"><a href="#s7"><b>01 数据飞轮</b><span>为评价与决策提供依据 ↗</span></a><a href="#s8"><b>02 人才飞轮</b><span>将资源转化为能力与成果 ↗</span></a><a href="#s9"><b>03 价值飞轮</b><span>为持续创造争取支持 ↗</span></a></div></div>'+art(overview,'数据、人才与价值三个飞轮互相支撑，可点击展开')+'</div>',
 '先看关系，再看环节。数据帮助判断，人才完成创造，价值回馈争取持续支持。三个飞轮相互依赖；我们以实践检验循环，并随新证据改进。点击任一飞轮可进入详解，也可以继续按顺序讲述。',theme='dark')

wheel_sets=[
 ('data','数据飞轮','让评价有据可依。',['数据采集','基准建设','平台支撑','评价应用'],['OpenDigger','OSIDX','OpenShare','贡献 · 协作 · 效果'],[
 ['数据采集 · OpenDigger','从开源实践中持续采集数据与指标，保留可追溯的证据。'],['基准建设 · OSIDX','完善指标、指数与基准探索，让评价有可解释的参照。'],['平台支撑 · OpenShare','通过平台连接数据、方法与实践，逐步贯通评价工作。'],['评价应用 · 反馈改进','服务贡献识别、协作分析和效果检验，让发现的问题反馈到下一轮采集。']], '评价反馈，改进数据采集。'),
 ('talent','人才飞轮','让贡献被看见，让成长有回响。',['贡献评价','成长可见','人才汇聚','供给改善','普惠增进'],['多维证据','反馈认可','回馈激励','创造维护','切实帮助'],[
 ['贡献评价','尊重代码、文档、测试、教学、翻译、维护与社区协作等多样贡献。'],['成长可见','让参与者获得反馈、认可与实践机会，看见自身成长。'],['人才汇聚','以合理回馈与激励吸引更多人参与，支持贡献者持续成长。'],['供给改善','通过学习、创造与维护，提高数字公共品的质量与可用性。'],['普惠增进','让更多人获得切实帮助，将新的贡献与成效纳入下一轮评价。']], '新的贡献与成效，进入下一轮评价。'),
 ('value','价值飞轮','让投入形成可验证的回报。',['资源投入','贡献识别','价值回馈','成效验证'],['Token · 资金 · 岗位','OpenRank + 实践证据','人才 · 洞察 · 公共价值','支持下一轮投入'],[
 ['资源投入','企业与机构提供模型调用额度、资金、岗位和实践机会，并明确合作责任。'],['贡献识别','结合 OpenRank 与多维实践证据，完善贡献核算、人才识别和资源匹配。'],['价值回馈','围绕人才连接、生态洞察与公共价值形成合作回馈，并明确适用条件。'],['成效验证','以具体情境与实践结果检验投入成效，为下一轮持续支持提供依据。']], '验证成效，支持下一轮投入。')]
for w,(id,title,sub,st,short,ds,feedback)in enumerate(wheel_sets):
 a=loop(circle(300,270,182),f'wheel-{w}',5)+f'<circle class="orbit" cx="300" cy="270" r="110"/>'+text(300,258,title,'center')+text(300,291,['证据与判断','能力与创造','资源与持续'][w],'tiny')
 for j,(s,sm) in enumerate(zip(st,short)):
  angle=-math.pi/2+j*math.tau/len(st);x=300+182*math.cos(angle);y=270+182*math.sin(angle)
  a+=f'<g class="stage-node {"selected" if j==0 else ""}" data-stage="{j}"><circle cx="{x}" cy="{y}" r="51"/>'+text(x,y+2,s,'label')+text(x,y+24,f'0{j+1}','tiny')+'</g>'
 add(id,title,head(f'三 / 飞轮 0{w+1}',title,sub)+'<div class="split"><div class="copy">'+buttons(st)+detail(*ds[0])+f'<p class="feedback">↻ {feedback}</p><a class="back-link" href="#s6">返回三重飞轮总览 ↗</a></div>'+art(a,title+'闭环，各环节可通过左侧按钮展开')+'</div>',
 '沿闭环依次讲述：'+' → '.join(st)+'。'+feedback+' '+' '.join(x[0]+'：'+x[1]for x in ds)+(' 评价帮助人成长，不以单一分数定义人的价值。'if w==1 else ''),theme='dark',seconds=16,steps=ds)

scenes=[['学习 · 积累能力','让初学者通过开放课程、工具与实践获得能力。'],['工作 · 改善协作','让开发者和组织复用成果，回应真实工作需要。'],['社区 · 共同维护','让知识与工具在分享、反馈和维护中持续改善。'],['本地实践 · 适宜方案','与当地伙伴共同回应语言、文化和公共服务需求。']]
add('possibilities','万千可能',head('万 / 多样实践','万千可能','让开放共享的成果，回应千差万别的需要。')+'<div class="split"><div class="copy"><p class="large-copy">同一份公共成果，<br>可以成为许多人的新起点。</p>'+buttons(['学习','工作','社区','本地实践'])+detail(*scenes[0])+'<p class="small-note">场景为实践方向示意，实际成效需持续检验。</p></div>'+art(network_art(loop),'连通的数字公共品网络，流动节点连接学习、工作、社区与本地实践')+'</div>',
 '选择场景可以突出它与整体网络的联系。成果只有进入具体场景，才能检验是否负担得起、理解得了、使用得好。这里展示的是实践方向，而不是宣称已经完成的案例。要关注谁获得帮助，也关注谁仍因语言、资源或使用障碍而未能受益。',steps=scenes)

growth_steps=[['立足需求，开展实践','明确行动目标、服务对象与支持范围，开放资源和参与机会。'],['公开记录，积累证据','区分计划、试点和已完成事项，记录贡献、投入与受益变化。'],['多方参与，检验成效','结合数据、使用者反馈与专业判断，公开问题并支持纠错。'],['总结经验，持续改进','让新证据、新贡献和新成效回到三个飞轮，让经验回到行动。']]
add('renewal','生生不息',head('生 / 持续演化','生生不息','让每一轮实践，成为下一轮的起点。')+'<div class="split"><div class="copy">'+buttons(['实践','记录','检验','改进'])+detail(*growth_steps[0])+'<p class="feedback">经验回到行动，有用的成果得到持续维护。</p><button class="text-button" data-regrow>重新观察生长 ↻</button></div>'+art(growth_art(loop),'从实践生根，经记录、检验到改进的生长树')+'</div>',
 '生生不息意味着有组织地学习和改进。实践明确需要，记录积累证据，多方参与检验，总结经验回到下一轮。树的枝叶会逐步生长，沿枝流动表示经验与资源的循环。点“重新观察生长”可重播。',steps=growth_steps)

def mini(kind):
 if kind==0:s='<circle cx="60" cy="50" r="32"/><circle class="solid" cx="60" cy="50" r="13"/><circle class="solid" cx="60" cy="18" r="5"/><circle class="solid" cx="32" cy="67" r="5"/><circle class="solid" cx="88" cy="67" r="5"/>'
 elif kind==1:s='<circle cx="43" cy="50" r="28"/><circle cx="77" cy="50" r="28"/><circle class="solid" cx="43" cy="22" r="4"/><circle class="solid" cx="77" cy="78" r="4"/>'
 elif kind==2:s=''.join(f'<circle cx="{x}" cy="{y}" r="23"/><circle class="solid" cx="{x}" cy="{y-23}" r="4"/>'for x,y in [(60,29),(34,70),(86,70)])
 elif kind==3:
  pts=[(60,50),(17,29),(38,10),(91,19),(105,60),(80,86),(22,78)]
  s=''.join(f'<path d="M60 50L{x} {y}"/><circle class="solid" cx="{x}" cy="{y}" r="4"/>'for x,y in pts)+ '<path d="M17 29L38 10 91 19 105 60 80 86 22 78Z"/>'
 else:s='<path d="M60 90V22M60 70L23 39M60 56L96 28M60 38L44 14"/>'+''.join(f'<circle class="solid" cx="{x}" cy="{y}" r="5"/>'for x,y in [(23,39),(96,28),(44,14),(60,22)])
 return svg(s,'','0 0 120 100')
panels=''.join(f'<a class="pan-item" href="#s{n}">{mini(i)}<span class="pan-glyph">{g}</span><h3>{t}</h3><p>{d}</p></a>'for i,(n,g,t,d)in enumerate([(4,'一','一心普惠','共同愿景'),(5,'二','二力相生','开放 × 创造'),(6,'三','三重飞轮','数据 · 人才 · 价值'),(10,'万','万千可能','回应多样需要'),(11,'生','生生不息','实践 · 反馈 · 演化')]))
add('panorama','全景总结','<div class="eyebrow centered">全景 / 从愿景到行动</div>'+f'<div class="panorama">{panels}</div><div class="pan-summary"><h2>五层相连，就是 AI 普惠的全景。</h2><p>以共同愿景凝聚两股力量，以三重飞轮孕育万千可能。</p></div><div class="pan-return"><span>←</span> 持续实践与反馈，让整个体系不断完善 <span>↵</span></div><p class="pan-close">让 AI 用得起，更用得好。</p><p class="small-note centered">点选任一层，回到对应章节。</p>',
 '此处给观众完整的停留时间。以一个共同愿景凝聚两股力量，以三个飞轮连接证据、能力和资源，孕育多样实践，再通过反馈持续改进。五层是一个相互联系的整体。可以点击任一层回到相应章节回答问题。',theme='dark',seconds=16)

add('invitation','参与共建邀请',head('邀请 / 从一次行动开始','共同把愿景，变成行动。','让不同背景的人，在共同创造中拓展可能。')+f'''<div class="invites"><a href="{REPO}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener"><span>01 / 开发者</span><h3>贡献工具与知识</h3><p>代码、文档、教学、翻译与维护。<br>从一次具体贡献开始。</p><b>查看参与指南 ↗</b></a><a href="{REPO}/issues/new/choose" target="_blank" rel="noopener"><span>02 / 企业与机构</span><h3>提供资源与机会</h3><p>模型调用额度、资金、岗位与场景。<br>提出可持续的合作方式。</p><b>提出合作建议 ↗</b></a><a href="{REPO}/issues/new/choose" target="_blank" rel="noopener"><span>03 / 社区与伙伴</span><h3>连接真实需求</h3><p>分享经验，组织实践，带回反馈。<br>共同建设适宜的解决方案。</p><b>分享需要与实践 ↗</b></a></div><div class="invitation-bottom"><div><strong>现在，就一起行动。</strong><a href="{OFFICIAL}" target="_blank" rel="noopener">www.x-lab.info/ai-for-all/ ↗</a></div><div class="qr-wrap"><img src="assets/join-qr.svg" alt="扫码访问 AI 普惠宣言官网"><span>阅读宣言<br>参与共建</span></div></div>''',
 '最后把邀请说清楚：开发者贡献工具与知识，企业和机构提供资源与实践机会，社区及各地区伙伴连接真实需要和使用反馈。扫码进入正式宣言网站，也可以打开参与指南或提交公开建议。不要把页面上的邀请表述为已经达成的合作。',theme='dark',seconds=14)

assert len(slides)==13
header='<header><a href="#s1" aria-label="回到封面"><img class="logo-light" src="assets/logo-light.svg" alt="X-lab AI"><img class="logo-dark" src="assets/logo-dark.svg" alt="X-lab AI"></a><span>AI FOR ALL <i>/</i> X-LAB AI</span><span class="edition">v1.2 · 互动演示</span><div class="display-controls"><a id="language" href="en.html" aria-label="切换为英文">◎ English</a><button id="theme" aria-label="切换主题">◐ 随章节</button></div><b id="page-number">01 / 13</b></header>'
sections=''.join(f'<section class="slide {s["id"]}" id="s{i+1}" data-theme="{s["theme"]}" data-index="{i}" aria-label="第 {i+1} 页：{s["title"]}" {"hidden" if i else ""}>{s["body"]}</section>'for i,s in enumerate(slides))
nav=''.join(f'<button data-go="{i}" aria-label="第 {i+1} 页 {s["title"]}" title="{s["title"]}">{i+1:02}</button>'for i,s in enumerate(slides))
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#102f27"><meta name="description" content="AI 普惠宣言 v1.2 · 13 章在线互动演示。从 Linux 35 年、开放模型的力量，到五层普惠全景与共建邀请。"><title>AI 普惠宣言 · 13 章互动演示</title><script src="preferences.js"></script><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="updates.css"></head><body><a class="skip" href="#slides">跳至演示内容</a><main class="stage" data-theme="dark">{header}<div id="slides">{sections}</div><div class="slide-baseline"><span id="chapter-label">AI 普惠宣言</span><span>让 AI 用得起，更用得好。</span></div></main><footer class="controls"><div class="page-controls"><button id="previous" aria-label="上一页">←</button><button id="next" aria-label="下一页">→</button><span id="counter">01 / 13</span></div><nav class="dots" aria-label="选择章节">{nav}</nav><div class="utilities"><button id="autoplay" aria-pressed="false">▷ 自动导览</button><button id="motion" aria-pressed="false">暂停动效</button><button id="notes">讲述 / 来源</button><button id="contents">目录</button><button id="fullscreen" aria-label="全屏演示">⛶</button></div><div class="play-progress"><i></i></div></footer><div class="hint" id="hint">← → 翻页 · F 全屏 · N 讲述提示 · 空格自动导览</div><dialog id="info"><div class="dialog-head"><h2 id="info-title">讲述与来源</h2><button data-close aria-label="关闭">×</button></div><div id="info-body"></div></dialog><dialog id="toc"><div class="dialog-head"><h2>演示目录</h2><button data-close aria-label="关闭">×</button></div><div class="toc-grid">{''.join(f'<button data-go="{i}"><span>{i+1:02}</span>{s["title"]}</button>'for i,s in enumerate(slides))}</div><p>13 章 · 自动导览约 {sum(s['seconds']for s in slides)} 秒 · 可随时暂停探索</p></dialog><div id="announcement" class="sr-only" aria-live="polite"></div><script src="data.js"></script><script src="app.js"></script></body></html>'''
(OUT/'index.html').write_text(page)
(OUT/'data.js').write_text('window.DECK='+json.dumps([{k:v for k,v in s.items()if k!='body'}for s in slides],ensure_ascii=False)+';\nwindow.SOURCES='+json.dumps(sources,ensure_ascii=False)+';')
(ROOT/'NARRATIVE.md').write_text('# AI 普惠宣言 v1.2 · 13 章互动演示\n\n'+ '\n\n'.join(f'## {i+1}. {s["title"]}\n\n{s["notes"]}'for i,s in enumerate(slides)))
(ROOT/'SOURCES.md').write_text('# 来源与使用口径\n\n核验日期：2026-10-10\n\n'+ '\n\n'.join(f'## {x["label"]}\n\n{x["url"]}\n\n{x["note"]}'for a in sources.values()for x in a)+'\n\n首屏构图与背景参考用户上传的《AI 普惠宣言(1).pptx》第一页；模型标志沿用既有发布材料，仅作识别。正文与图解依据 v1.2 审定稿。\n')
print(f'Built {len(slides)} slides, {sum(s["seconds"] for s in slides)} second tour')

from translate import build_english
build_english(OUT)
