"""Code-native geometric illustrations; text remains in the approved source."""
import math, re
from collections import deque

def label(x,y,s,cls='label'):
 return f'<text x="{x}" y="{y}" class="{cls}">{s}</text>'

def vision_art():
 s='''<defs><radialGradient id="vision-core" cx="32%" cy="24%" r="78%"><stop stop-color="#f2f6e9"/><stop offset=".7" stop-color="#d8e5c4"/><stop offset="1" stop-color="#b7cb9e"/></radialGradient><radialGradient id="vision-planet" cx="30%" cy="24%" r="80%"><stop stop-color="#f9fbf3"/><stop offset="1" stop-color="#d8e3c9"/></radialGradient></defs><circle class="vision-orbit" cx="320" cy="320" r="192"/>'''
 for i,name in enumerate(['开发者','社会大众','全球南方']):
  a=-math.pi/2+i*math.tau/3;x=320+192*math.cos(a);y=320+192*math.sin(a)
  s+=f'<g class="perspective-ball" data-perspective="{i}" transform="translate({x} {y})">'
  if i==0:
   s+='<circle class="satellite-orbit" r="80"/>'
   for j,name2 in enumerate(['Learner','Builder','Engineer']):
    aa=-math.pi/2+j*math.tau/3
    s+=f'<g class="learner-ball" data-satellite="{j}" transform="translate({80*math.cos(aa)} {80*math.sin(aa)})"><circle r="5"/>'+label(0,23,name2,'satellite-text')+'</g>'
  s+='<circle class="view-ball" r="43"/>'+label(0,7,name,'perspective-text')+'</g>'
 # Draw center last, opaque, with no spokes passing through it.
 s+='<g class="vision-center"><circle r="69" cx="320" cy="320" fill="url(#vision-core)"/>'+label(320,315,'AI 普惠','center')+label(320,345,'共同目标','core-subtitle')+'</g>'
 return s

def network_art(loop):
 # Phyllotactic placement fills one continuous field; groups interweave spatially.
 points=[(300,270,4)]
 for j in range(1,74):
  a=j*2.399963;r=math.sqrt(j/74)
  points.append((300+235*r*math.cos(a),270+216*r*math.sin(a),j%4))
 edges=set()
 for i in range(1,len(points)):
  nearest=sorted((math.dist(points[i][:2],points[j][:2]),j)for j in range(len(points))if i!=j)[:3]
  edges.update(tuple(sorted((i,j)))for _,j in nearest)
  # A link to an earlier node guarantees a single connected component.
  prev=min(range(i),key=lambda j:math.dist(points[i][:2],points[j][:2]));edges.add((prev,i))
 s=''
 for i,j in sorted(edges):
  x,y,c=points[i];xx,yy,cc=points[j]
  s+=f'<line class="net-edge" data-community="{c} {cc}" x1="{x:.2f}" y1="{y:.2f}" x2="{xx:.2f}" y2="{yy:.2f}"/>'
 for i,(x,y,c) in enumerate(points):
  s+=f'<circle class="net-node" data-community="{c}" cx="{x:.2f}" cy="{y:.2f}" r="{4.3 if i%9==0 else 2.5}"/>'
 def route(start,end):
  q=deque([[start]]);seen={start}
  while q:
   p=q.popleft()
   if p[-1]==end:return p
   for a,b in sorted(edges):
    n=b if a==p[-1] else a if b==p[-1] else None
    if n is not None and n not in seen:seen.add(n);q.append(p+[n])
 for k,(start,end) in enumerate([(68,59),(47,72),(60,39),(52,65),(71,43),(57,69)]):
  p=route(start,end);p+=p[-2::-1]
  path='M'+' L'.join(f'{points[i][0]:.2f} {points[i][1]:.2f}'for i in p)
  s+=re.sub(r'data-period="(\d+)"',lambda m:f'data-period="{round(int(m[1])/1.5)}"',loop(path,f'network-track-{k}',2,True))
 s+='<circle class="network-core" cx="300" cy="270" r="65"/>'+label(300,265,'数字公共品','label')+label(300,291,'共享 · 复用 · 共创','network-subtitle')
 for x,y,title in [(154,70,'学习'),(499,228,'工作'),(340,482,'社区'),(96,354,'本地实践')]:
  s+=f'<g class="network-tag"><rect x="{x-47}" y="{y-20}" width="94" height="34" rx="17"/>'+label(x,y+3,title,'network-tag-text')+'</g>'
 return s

def growth_art(loop):
 branches=[('M300 441 C294 391 301 349 300 302',0),('M300 353 C258 333 224 291 199 257',1),('M300 328 C345 305 375 263 401 226',1),('M300 302 C285 257 287 211 304 163',1),('M199 257 C170 258 131 232 102 202',2),('M199 257 C182 219 177 191 179 158',2),('M401 226 C443 220 475 194 491 163',2),('M401 226 C395 179 400 145 420 115',2),('M304 163 C277 140 254 113 252 78',2),('M304 163 C333 135 346 103 347 67',2)]
 branches += [('M155 237 C126 207 109 166 124 130',2),('M186 210 C204 188 224 171 232 144',2),('M448 203 C472 177 487 139 475 108',2),('M402 167 C375 150 370 129 375 111',2),('M274 126 C242 119 220 100 208 79',2),('M333 124 C371 108 392 80 389 52',2)]
 branches += [('M170 215 C146 204 129 191 119 174',2),('M283 225 C259 205 252 183 258 164',2),('M393 185 C423 166 438 146 437 130',2),('M297 194 C326 182 347 168 354 149',2)]
 s='<g class="growth-tree">'
 for i,(path,level)in enumerate(branches):
  s+=f'<path class="growth-base" d="{path}"/><path class="growth-line" data-growth="{level}" pathLength="1" d="{path}"/>'
 for i,(x,y)in enumerate([(102,202),(179,158),(491,163),(420,115),(252,78),(347,67),(124,130),(232,144),(475,108),(375,111),(208,79),(389,52),(119,174),(258,164),(437,130),(354,149)]):
  s+=f'<g class="growth-bud" data-bud="{i}" transform="translate({x} {y})"><circle class="bud-aura" r="13"/><ellipse class="growth-leaf" cx="5" cy="-6" rx="9" ry="4" transform="rotate(-35 5 -6)"/><circle r="3.5"/></g>'
 # Ten restrained markers move along actual branches, then return on the same curve.
 for k,index in enumerate([1,2,5,8,12,15,16,17,18,19]):
  path,level=branches[index]
  x0,y0,x1,y1,x2,y2,x3,y3=map(float,re.findall(r'-?\d+(?:\.\d+)?',path))
  back=f' C{x2} {y2} {x1} {y1} {x0} {y0}'
  markers=loop(path+back,f'growth-branch-{k}',1,True)
  markers=markers.replace('data-phase="0.0000"',f'data-phase="{k/10:.4f}" data-appear="{level*5+7}"').replace('data-period="42000"',f'data-period="{24000+(k%5)*3000}"')
  s+=markers
 s+='</g>'
 s+=loop('M300 437 C115 445 51 336 62 272 C67 241 82 217 102 202', 'growth-feed',1)
 s+=loop('M491 163 C575 283 551 445 320 451 C311 451 304 449 300 441','growth-return',1)
 for x,y,n,sub in [(300,442,'实践','立足需求'),(185,292,'记录','积累证据'),(385,263,'检验','多方参与'),(307,153,'改进','持续演化')]:
  s+=f'<g class="growth-label"><circle cx="{x}" cy="{y}" r="29"/>'+label(x,y+6,n,'label')+label(x,y+49,sub,'growth-subtitle')+'</g>'
 s+=label(300,527,'经验回到根部，推动下一轮生长','caption')
 return s

def panorama():
 goal='<svg viewBox="0 0 110 100" aria-hidden="true"><circle cx="55" cy="55" r="31"/><circle class="orb-fill" cx="55" cy="55" r="12"/>'
 for x,y,r in [(55,24,8),(82,71,8),(28,71,8)]:goal+=f'<circle class="orb-fill" cx="{x}" cy="{y}" r="{r}"/>'
 goal+='</svg>'
 pair='<svg viewBox="0 0 110 100" aria-hidden="true"><circle cx="40" cy="49" r="25"/><circle cx="70" cy="49" r="25"/><path d="M55 74V88"/><circle class="solid" cx="55" cy="88" r="3"/></svg>'
 pts=[(55,50)]+[(55+40*math.sqrt(i/18)*math.cos(i*2.39996),50+37*math.sqrt(i/18)*math.sin(i*2.39996))for i in range(1,19)]
 edges=set()
 for i in range(1,len(pts)):
  near=sorted(range(i),key=lambda j:math.dist(pts[i],pts[j]))[:2]
  edges.update((j,i)for j in near)
 network='<svg viewBox="0 0 110 100" aria-hidden="true">'
 for i,j in sorted(edges):network+=f'<path class="faint" d="M{pts[i][0]} {pts[i][1]}L{pts[j][0]} {pts[j][1]}"/>'
 for x,y in pts:network+=f'<circle class="solid" cx="{x}" cy="{y}" r="2"/>'
 network+='<circle class="orb-fill" cx="55" cy="50" r="9"/></svg>'
 tree='<svg viewBox="0 0 110 110" aria-hidden="true"><path d="M55 92C51 65 55 39 56 17M54 62L31 44L20 27M31 44L36 23M55 49L78 31L88 15M78 31L71 14M56 30L43 13M55 75L81 59L93 41M81 59L83 44"/>'
 for x,y in [(20,27),(36,23),(56,17),(88,15),(71,14),(43,13),(93,41),(83,44)]:tree+=f'<ellipse class="solid" cx="{x}" cy="{y}" rx="3.6" ry="2" transform="rotate(-35 {x} {y})"/>'
 tree+='<circle class="solid" cx="55" cy="92" r="3"/></svg>'
 def connector(label):return f'<div class="pan-link"><i></i><span>{label}</span><i></i></div>'
 s=f'<a class="pan-layer" href="#vision">{goal}<small>一 / 一心普惠</small><h3>AI 普惠</h3><p>开发者 · 社会大众 · 全球南方</p><p class="pan-sub">学习者 Learner · 构建者 Builder · 工程师 Engineer</p></a>'+connector('共同目标：让 AI 用得起，更用得好')
 s+=f'<a class="pan-layer" href="#forces">{pair}<small>二 / 二力相生</small><h3>开源之力 × 开发者之力</h3><p>在项目与社区中共同创造</p></a>'+connector('AI 能力 → 数字公共品')
 s+='<div class="pan-wheel-band"><small>三 / 三重飞轮</small><div class="pan-wheels">'
 for i,(title,count,caption)in enumerate([('数据飞轮',4,'以数据支撑判断'),('人才飞轮',5,'以人才推动创造'),('价值飞轮',4,'以价值促进投入')]):
  if i:s+='<span class="pan-exchange" aria-hidden="true">⇄</span>'
  s+=f'<a href="#wheels" data-pan-wheel="{i}"><span class="pan-ring pan-ring-{i}">{count}<i>›</i></span><h3>{title}</h3><p>{caption}</p></a>'
 s+='</div><p class="pan-note">证据、能力与资源相互支持，实践反馈推动下一轮改进。</p></div>'+connector('共享 · 复用 · 推广 · 本地化')
 s+=f'<a class="pan-layer" href="#possibilities">{network}<small>万 / 万千可能</small><h3>学习 · 工作 · 社区 · 本地实践</h3><p>多样实践相互连接，让数字公共品增进普惠</p></a>'
 s+=f'<a class="pan-return" href="#renewal">{tree}<div><small>生 / 生生不息</small><h3>实践 → 记录 → 检验 → 改进</h3><p>从实践生长，在反馈中演化。</p><p>新的证据、贡献与成效，回到三个飞轮。</p></div></a>'
 return s
