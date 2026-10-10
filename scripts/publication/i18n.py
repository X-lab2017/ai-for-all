"""Static English edition with explicit, checked text coverage."""
from html.parser import HTMLParser
from pathlib import Path
import html,re
ROOT=Path(__file__).resolve().parents[2]

def source_blocks(path):
 raw=path.read_text();body=raw.split('<!-- manifesto:start -->')[1].split('<!-- manifesto:end -->')[0].strip()
 return body.split('\n\n')

def fragments(s):
 s=re.sub(r'^#{1,3} ','',s)
 return [v.strip() for v in re.split(r'\*\*',s)if v.strip()]

UI={
'AI 普惠宣言':'AI for All Manifesto','让 AI 用得起，更用得好':'Make AI affordable and useful','X-lab AI 开放实验室 · v1.2 · 2026 年 10 月 10 日':'X-lab AI Open Laboratory · v1.2 · 10 October 2026',
'一':'1','二':'2','三':'3','万':'∞','生':'↻','共 同 的 愿 景':'A SHARED VISION',
'AI 普惠':'AI for All','共同目标':'Shared purpose','开发者':'Developers','社会大众':'The public','全球南方':'Global South',
'开源之力':'Open source','降低门槛':'Lower barriers','开发者之力':'Developers','拓展价值':'Create value','项目':'Projects','社区':'Community','数字公共品':'Digital public goods',
'AI 能力':'AI capabilities','数据采集':'Collect data','基准建设':'Build benchmarks','平台支撑':'Platform support','评价应用':'Apply evaluation',
'贡献评价':'Evaluate contributions','成长可见':'Visible growth','人才汇聚':'Gather talent','供给改善':'Improve supply','普惠增进':'Broaden benefits',
'资源投入':'Commit resources','贡献识别':'Recognize contributions','价值回馈':'Return value','成效验证':'Verify outcomes',
'证据 · 判断':'Evidence · Judgment','能力 · 创造':'Capability · Creation','资源 · 持续':'Resources · Continuity','证据':'Evidence','人才':'Talent','资源':'Resources',
'学习':'Learning','工作':'Work','本地实践':'Local practice','共享 · 复用 · 共创':'Share · Reuse · Create',
'实践':'Practice','记录':'Document','检验':'Evaluate','改进':'Improve','立足需求':'Real needs','积累证据':'Build evidence','多方参与':'Many perspectives','持续演化':'Keep evolving',
'经验回到根部，推动下一轮生长':'Experience returns to the roots, enabling new growth',
'跳至正文':'Skip to content','X-lab AI 首页':'X-lab AI home','阅读全文':'Read the manifesto','暂停动效':'Pause motion','深色':'Dark','切换为深色模式':'Switch to dark mode','切换语言':'Switch language',
'让 AI 用得起，':'Make AI affordable, ','更用得好。':'and useful.','走进宣言':'Explore the manifesto','阅读完整文本 ↓':'Read the full text ↓',
'一心普惠 · 二力相生 · 三重飞轮 · 万千可能 · 生生不息':'One vision · Two forces · Three flywheels · Possibilities · Renewal',
'宣言章节':'Manifesto chapters','01 / 同一愿景，多重视角':'01 / One vision, complementary perspectives','02 / 开放支持创造，创造丰富开放':'02 / Openness and creativity reinforce each other',
'4 个环节 · 反馈进入下一轮':'4 stages · Feedback begins the next cycle','5 个环节 · 反馈进入下一轮':'5 stages · Feedback begins the next cycle',
'选择飞轮':'Choose a flywheel','突出实践社群':'Highlight a practice community','04 / 共享成果，连接多样实践':'04 / Shared results connect diverse practices',
'点选场景，查看它与公共品的连接':'Choose a context to highlight its public-goods connections','05 / 从实践生长，在反馈中演化':'05 / Grow through practice, evolve through feedback',
'五层相连，':'Five connected layers.','就是 AI 普惠的全景。':'One vision of AI for All.','五层全景架构':'The five-layer framework',
'一 / 一心普惠':'1 / One Shared Vision','开发者 · 社会大众 · 全球南方':'Developers · The public · The Global South',
'学习者 Learner · 构建者 Builder · 工程师 Engineer':'AI Learner · AI Builder · AI Engineer','共同目标：让 AI 用得起，更用得好':'Our shared goal: make AI affordable and useful',
'二 / 二力相生':'2 / Two Reinforcing Forces','开源之力 × 开发者之力':'Open source × Developer creativity','在项目与社区中共同创造':'Create together in projects and communities',
'AI 能力 → 数字公共品':'AI capabilities → Digital public goods','三 / 三重飞轮':'3 / Three Flywheels','以数据支撑判断':'Data informs judgment','以人才推动创造':'Talent drives creation','以价值促进投入':'Value encourages investment',
'证据、能力与资源相互支持，实践反馈推动下一轮改进。':'Evidence, capabilities and resources reinforce one another; feedback guides the next cycle.',
'共享 · 复用 · 推广 · 本地化':'Share · Reuse · Adopt · Localize','万 / 万千可能':'∞ / Countless Possibilities','学习 · 工作 · 社区 · 本地实践':'Learning · Work · Community · Local practice',
'多样实践相互连接，让数字公共品增进普惠':'Connected practices turn digital public goods into wider benefits','生 / 生生不息':'↻ / Continuous Renewal','实践 → 记录 → 检验 → 改进':'Practice → Document → Evaluate → Improve',
'从实践生长，在反馈中演化。':'Grow through practice. Evolve through feedback.','新的证据、贡献与成效，回到三个飞轮。':'New evidence, contributions and outcomes return to the three flywheels.',
'参与宣言共建 ↗':'Help shape the manifesto ↗','阅读与保存全文 ↓':'Read and save the full text ↓','宣言全文':'The Full Manifesto','下载文本 ↓':'Download text ↓','打印 / 存为 PDF':'Print / Save as PDF','展开完整宣言':'Expand the full manifesto',
'v1.1 历史版':'Chinese archive · v1.1','大会材料 · v1.1':'Conference materials · v1.1','X-lab AI 开放实验室':'X-lab AI Open Laboratory','回到顶部 ↑':'Back to top ↑',
'一、二、三、万、生围绕 X-lab AI 共同愿景的五层架构':'Five layers around the shared X-lab AI vision',
'AI 普惠中心球，三个视角球体公转，Learner、Builder、Engineer 围绕开发者公转':'AI for All at the center, with three perspectives in orbit and Learner, Builder and Engineer around developers',
'开源与开发者两股力量交汇于项目与社区，共建数字公共品':'Open source and developers meet in projects and communities to build digital public goods',
'数据飞轮循环图':'Data flywheel cycle','人才飞轮循环图':'Talent flywheel cycle','价值飞轮循环图':'Value flywheel cycle',
'多样实践交织为一个连续、连通的公共品网络':'Diverse practices form one connected public-goods network',
'实践如种子生根，记录和检验形成枝干，改进带来新芽，经验回流根部':'Practice takes root; documentation and evaluation form branches; improvement brings new leaves and experience returns to the roots',
'AI 普惠宣言：让 AI 用得起，更用得好。一心普惠，二力相生，三重飞轮，万千可能，生生不息。':'AI for All Manifesto: make AI affordable and useful. One vision, two forces, three flywheels, countless possibilities and continuous renewal.',
'AI 普惠宣言 · X-lab AI':'AI for All Manifesto · X-lab AI','一心普惠，二力相生，三重飞轮，万千可能，生生不息。':'One shared vision, two reinforcing forces, three flywheels, countless possibilities and continuous renewal.'
}

def translate_page(page):
 mapping=dict(UI);zh=source_blocks(ROOT/'README.md');en=source_blocks(ROOT/'translations/en.md');assert len(zh)==len(en),(len(zh),len(en))
 for a,b in zip(zh,en):
  aa,bb=fragments(a),fragments(b);assert len(aa)==len(bb),(a,b)
  mapping.update(zip(aa,bb))
 missing=set()
 def tr(s):
  if not re.search(r'[\u4e00-\u9fff]',s):return s
  t=s.strip()
  if t not in mapping:missing.add(t);return s
  return s[:len(s)-len(s.lstrip())]+mapping[t]+s[len(s.rstrip()):]
 class Translator(HTMLParser):
  def __init__(self):super().__init__(convert_charrefs=True);self.out=[];self.stack=[]
  def handle_decl(self,d):self.out.append('<!'+d+'>')
  def handle_starttag(self,t,attrs):
   attrs=dict(attrs)
   if t=='html':attrs['lang']='en'
   for k in ['aria-label','alt','title','content']:
    if k in attrs:attrs[k]=tr(attrs[k])
   self.out.append('<'+t+''.join(' '+k+('="'+html.escape(v,quote=True)+'"'if v is not None else '')for k,v in attrs.items())+'>')
   if t not in ['meta','link','img','br','hr','input']:self.stack.append((t,attrs))
  def handle_startendtag(self,t,attrs):
   self.handle_starttag(t,attrs)
   if t not in ['meta','link','img','br','hr','input']:self.handle_endtag(t)
  def handle_endtag(self,t):
   self.out.append('</'+t+'>')
   if self.stack and self.stack[-1][0]==t:self.stack.pop()
  def handle_data(self,s):
   if self.stack and self.stack[-1][0]in ['script','style']:self.out.append(s);return
   value=tr(s)
   if self.stack and self.stack[-1][0]=='text':
    a=self.stack[-1][1];c=a.get('class','')
    # Compact labels fit fixed diagram geometry; prose uses full translations.
    if c=='label' and value=='Digital public goods':value='Public goods'
    if c=='label' and len(value)>17 and ' 'in value:
     words=value.split();mid=max(1,len(words)//2);lines=[' '.join(words[:mid]),' '.join(words[mid:])]
     self.out.append(''.join(f'<tspan x="{a.get("x","0")}" dy="{(-7 if i==0 else 17)}">{html.escape(line)}</tspan>'for i,line in enumerate(lines)));return
   self.out.append(html.escape(value,quote=False))
 parser=Translator();parser.feed(page)
 if missing:raise ValueError('Missing English UI text: '+repr(sorted(missing)))
 result=''.join(parser.out)
 result=result.replace('href="AI-for-All-manifesto.md"','href="AI-for-All-manifesto-EN.md"')
 result=result.replace('href="en.html?lang=en"','href="index.html?lang=zh"').replace('data-language="en"','data-language="zh"').replace('<span>English</span>','<span>中文</span>')
 result=result.replace('href="https://www.x-lab.info/ai-for-all/"','href="https://www.x-lab.info/ai-for-all/en.html"',1).replace('property="og:url" content="https://www.x-lab.info/ai-for-all/"','property="og:url" content="https://www.x-lab.info/ai-for-all/en.html"')
 return result
