// AI for All / V5 typography and seamless transition revision. Deterministic vector motion.
const fs=require('fs'),path=require('path'),cp=require('child_process');
const {once}=require('events');
const {createCanvas,loadImage,GlobalFonts}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'@napi-rs/canvas'));
const OUT=__dirname,AS=path.join(OUT,'assets'),W=1920,H=1080,FPS=30;
GlobalFonts.registerFromPath(path.join(AS,'NotoSansSC-Regular.ttf'),'Han');
GlobalFonts.registerFromPath(path.join(AS,'NotoSansSC-SemiBold.ttf'),'HanBold');
const frames=createCanvas(W,H),ctx=frames.getContext('2d'),layer=createCanvas(W,H),g=layer.getContext('2d');
const CUTS=[0,7,17.5,27,34,38,46.5,55,63.68,69.53,77.83,87.3,94.7,104.4].map(x=>Math.round(x*30)/30);
const D=CUTS.slice(1).map((v,i)=>v-CUTS[i]),TOTAL=104.4;
const MUSIC=require('./assets/music-cues.json');
let ENERGY=0,PULSE=0,MOTION=0,TEXT_FADE=1;
const phase=[];let accum=0;for(let e of MUSIC.energy){accum+=(.55+1.1*e)/FPS;phase.push(accum)}
let dark=true,C={},images={},globalTime=0;
const clamp=x=>Math.min(1,Math.max(0,x)),ease=x=>1-(1-clamp(x))**3,sm=x=>{x=clamp(x);return x*x*(3-2*x)};
const scenes=[
 ['共同的愿景','AI 普惠宣言','让 AI 用得起，更用得好。'],
 ['一心普惠','让技术成为机会','开发者 · 社会大众 · 全球南方'],
 ['二力相生','开放支持创造','创造，让开放的成果更有价值。'],
 ['从能力到受益','让开放成为真实帮助','AI 能力 → 数字公共品 → AI 普惠'],
 ['三重飞轮','让愿景持续运转','以数据支撑判断，以人才推动创造，以价值促进投入。'],
 ['数据飞轮','以证据改进判断','让贡献被看见，让评价有依据。'],
 ['人才飞轮','让每一份贡献推动成长','让成长改善供给，让成果增进普惠。'],
 ['价值飞轮','让支持形成持续的力量','投入有方向，贡献有回馈，成效可检验。'],
 ['万千可能','回应千差万别的需要','共享 · 复用 · 推广 · 本地化'],
 ['生生不息','让每一轮实践成为新的起点','实践 → 记录 → 检验 → 改进'],
 ['共同把愿景变成行动','让 AI 用得起，更用得好。','AI 普惠宣言 / X-lab AI']
];
function palette(isDark){dark=true;C=dark?{bg:'#143b30',fg:'#f7f6ef',muted:'#b3c8b3',line:'#55785e',accent:'#c5e79c',soft:'#244a39'}:{bg:'#f7f6ef',fg:'#173b31',muted:'#617369',line:'#a6b39a',accent:'#69875e',soft:'#e7eddd'};}
function text(s,x,y,size=32,fill=C.fg,align='left',bold=false){g.save();g.globalAlpha*=TEXT_FADE;g.fillStyle=fill;g.font=`${size}px ${bold?'HanBold':'Han'}`;g.textAlign=align;g.textBaseline='middle';g.fillText(s,x,y);g.restore();}
function line(x,y,xx,yy,col=C.line,w=2){g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.moveTo(x,y);g.lineTo(xx,yy);g.stroke();}
function circle(x,y,r,fill=null,stroke=C.line,w=2){g.beginPath();g.arc(x,y,r,0,Math.PI*2);if(fill){g.fillStyle=fill;g.fill()}if(stroke){g.strokeStyle=stroke;g.lineWidth=w;g.stroke()}}
function glow(x,y,r,a=.15){g.save();let f=g.createRadialGradient(x,y,0,x,y,r);f.addColorStop(0,`rgba(185,221,136,${a})`);f.addColorStop(1,'rgba(185,221,136,0)');g.fillStyle=f;g.fillRect(x-r,y-r,r*2,r*2);g.restore();}
function img(key,x,y,w,h){let im=images[key],k=Math.min(w/im.width,h/im.height);g.drawImage(im,x+(w-im.width*k)/2,y+(h-im.height*k)/2,im.width*k,im.height*k)}
function reveal(t,at,draw,d=.8){const a=ease((t-at)/d);if(!a)return;g.save();g.globalAlpha*=a;g.translate(0,(1-a)*22);draw();g.restore()}
const CHAPTERS={'一心普惠':'一','二力相生':'二','三重飞轮':'三','万千可能':'万','生生不息':'生'};
function chapterLabel(code,label,x,y,align='left',size=42){
 g.font=`${size}px HanBold`;const width=58+24+g.measureText(label).width;let xx=align==='center'?x-width/2:x;
 text(code,xx,y-2,60,'#e1d79c','left',true);text(label,xx+82,y,size,C.fg,'left',true);
}
function heading(i,t,center=false){const x=center?960:120,a=center?'center':'left';reveal(t,.05,()=>{if(CHAPTERS[scenes[i][0]])chapterLabel(CHAPTERS[scenes[i][0]],scenes[i][0],x,210,a);else text(scenes[i][0],x,210,32,C.accent,a)});reveal(t,.4,()=>text(scenes[i][1],x,305,i===10?78:66,C.fg,a,true));reveal(t,1.25,()=>text(scenes[i][2],x,402,31,C.muted,a));}
function bead(x,y,r,a,sz=6){let xx=x+r*Math.cos(a),yy=y+r*Math.sin(a);glow(xx,yy,32,.08);circle(xx,yy,sz,C.accent,null)}
function orbit(x,y,r,t,n=3){circle(x,y,r,null,C.line,1.7+PULSE*.65);for(let j=0;j<n;j++)bead(x,y,r,MOTION*.14*(t<0?-1:1)+j*2*Math.PI/n,5+PULSE*2)}
function wheel(x,y,r,t,title,steps,appear=0){
 const p=ease(t/1.5);g.save();g.globalAlpha*=p;orbit(x,y,r,t,3);circle(x,y,r*.58,null,C.line,1);text(title,x,y,42,C.accent,'center',true);
 steps.forEach((s,j)=>{const a=-Math.PI/2+j*Math.PI*2/steps.length,xx=x+r*Math.cos(a),yy=y+r*Math.sin(a),active=Math.floor(Math.max(0,t-1)/1.6)%steps.length===j;g.fillStyle=C.bg;g.fillRect(xx-100,yy-28,200,56);text(s,xx,yy,29,active?C.accent:C.muted,'center',active)});g.restore();
}
function vision(x,y,r,t){orbit(x,y,r,t);circle(x,y,91,C.soft,C.line);text('AI 普惠',x,y-12,39,C.fg,'center',true);text('共同目标',x,y+39,22,C.muted,'center');
 ['开发者','社会大众','全球南方'].forEach((s,j)=>{const a=-Math.PI/2+j*Math.PI*2/3+t*.13,xx=x+r*Math.cos(a),yy=y+r*Math.sin(a);circle(xx,yy,65,C.bg,C.accent);text(s,xx,yy,27,C.fg,'center');if(j===0){circle(xx,yy,100,null,C.line,1);['Learner','Builder','Engineer'].forEach((q,k)=>{let a=-Math.PI/2+k*Math.PI*2/3-t*.4;circle(xx+100*Math.cos(a),yy+100*Math.sin(a),4,C.accent,null);text(q,xx+126*Math.cos(a),yy+123*Math.sin(a),17,C.muted,'center')})}})
}
const pts=[{x:0,y:0},...Array.from({length:83},(_,k)=>{let j=k+1,a=j*2.399963,r=Math.sqrt(j/84);return {x:470*r*Math.cos(a),y:282*r*Math.sin(a)}})];
const edges=[];for(let i=1;i<pts.length;i++){let n=Array.from({length:i},(_,j)=>j).sort((a,b)=>Math.hypot(pts[i].x-pts[a].x,pts[i].y-pts[a].y)-Math.hypot(pts[i].x-pts[b].x,pts[i].y-pts[b].y)).slice(0,2);for(let j of n)edges.push([i,j])}
function network(x,y,t,scale=1){g.save();g.translate(x,y);g.scale(scale,scale);for(const [i,j]of edges){let a=ease((t-.3-(i%9)*.1)/1.2);g.globalAlpha=a*.65;line(pts[i].x,pts[i].y,pts[j].x,pts[j].y,C.line,1.5)}g.globalAlpha=1;pts.forEach((p,j)=>{let a=ease((t-(j%8)*.12)/1.1);circle(p.x,p.y,(j%9?3.2:5)*a,C.accent,null)});for(let k=0;k<12;k++){let [a,b]=edges[(k*13)%edges.length],p=(t*.2+k/12)%1;circle(pts[a].x+(pts[b].x-pts[a].x)*p,pts[a].y+(pts[b].y-pts[a].y)*p,4,C.accent,null)}circle(0,0,83,C.bg,C.line);text('数字公共品',0,-11,30,C.fg,'center',true);text('共享 · 复用 · 共创',0,32,19,C.muted,'center');g.restore()}
const branches=[[[0,0],[-10,-75],[4,-140],[0,-215]],[[0,-108],[-67,-140],[-120,-210],[-177,-271]],[[0,-151],[70,-177],[145,-252],[194,-328]],[[0,-215],[-26,-288],[-22,-357],[6,-418]],[[-177,-271],[-228,-270],[-260,-300],[-305,-343]],[[-177,-271],[-191,-332],[-192,-370],[-200,-413]],[[194,-328],[253,-335],[284,-382],[320,-438]],[[194,-328],[181,-380],[208,-432],[211,-470]],[[6,-418],[-25,-446],[-66,-483],[-80,-508]],[[6,-418],[39,-454],[72,-498],[81,-533]],[[-230,-304],[-228,-356],[-240,-399],[-255,-446]],[[125,-254],[151,-322],[116,-377],[124,-420]],[[50,-198],[83,-235],[96,-263],[97,-310]],[[-13,-320],[-65,-350],[-104,-390],[-113,-441]]];
function bez(p,u){let v=1-u;return {x:v*v*v*p[0][0]+3*v*v*u*p[1][0]+3*v*u*u*p[2][0]+u*u*u*p[3][0],y:v*v*v*p[0][1]+3*v*v*u*p[1][1]+3*v*u*u*p[2][1]+u*u*u*p[3][1]}}
function curve(p,progress=1,col=C.accent,w=2){g.beginPath();g.moveTo(...p[0]);for(let i=1;i<=65;i++){let q=bez(p,Math.min(progress,i/65));g.lineTo(q.x,q.y);if(i/65>=progress)break;}g.strokeStyle=col;g.lineWidth=w;g.stroke()}
function tree(x,y,t,scale=1){g.save();g.translate(x,y);g.scale(scale,scale);branches.forEach((b,i)=>{let p=ease((t-(i<4?i*.25:1.1+(i%5)*.25))/2);curve(b,p,C.line,2);if(p>.98){let q=bez(b,1);circle(q.x,q.y,8,C.accent,null);g.save();g.translate(q.x,q.y);g.rotate(-.5);g.fillStyle=C.accent;g.beginPath();g.ellipse(10,-7,14,5,0,0,7);g.fill();g.restore()}if(t>3){let q=bez(b,((t-3)*.14+i*.1)%1);circle(q.x,q.y,3.3,C.accent,null)}});
 const ret=[[[320,-438],[482,-260],[425,0],[0,0]],[[0,0],[-419,0],[-425,-246],[-305,-343]]];ret.forEach((p,i)=>{curve(p,ease((t-3)/2),C.accent,1.6);if(t>4){let q=bez(p,(t*.1+i*.5)%1);circle(q.x,q.y,5,C.accent,null)}});
 [[0,0,'实践'],[-158,-207,'记录'],[159,-261,'检验'],[3,-420,'改进']].forEach(([xx,yy,s],i)=>{reveal(t,i*.55,()=>{circle(xx,yy,36,C.bg,C.accent);text(s,xx,yy,22,C.fg,'center')})});g.restore()}
function mini(kind,x,y,t){g.save();g.translate(x,y);if(kind===0){circle(0,0,45);circle(0,0,15,C.accent,null);for(let a of [-Math.PI/2,Math.PI/6,Math.PI*5/6])circle(45*Math.cos(a),45*Math.sin(a),10,C.bg,C.accent)}if(kind===1){orbit(-24,0,39,t,1);orbit(24,0,39,-t,1)}if(kind===2){for(const [a,b]of [[0,-29],[-34,28],[34,28]])orbit(a,b,29,t,1)}if(kind===3){for(let j=0;j<7;j++){let a=j/7*Math.PI*2,xx=58*Math.cos(a),yy=48*Math.sin(a);line(0,0,xx,yy);circle(xx,yy,4,C.accent,null)}circle(0,0,8,C.accent,null)}if(kind===4){line(0,52,0,-48);line(0,5,-46,-26);line(0,-7,46,-36);line(0,-31,-22,-53);for(const [a,b]of [[-46,-26],[46,-36],[-22,-53],[0,-48]])circle(a,b,5,C.accent,null)}g.restore()}
function qr(x,y,size){const data=require('./assets/qr.json'),n=data.length,mod=size/(n+8);g.fillStyle='white';g.fillRect(x,y,size,size);g.fillStyle='#143b30';data.forEach((r,j)=>r.forEach((v,i)=>{if(v)g.fillRect(x+(i+4)*mod,y+(j+4)*mod,mod+.1,mod+.1)}))}
function original(i,t){palette(![1,2,6,8].includes(i));g.globalAlpha=1;g.fillStyle=C.bg;g.fillRect(0,0,W,H);
 if(dark)glow(1250,610,700,.06);
 img(dark?'brandDark':'brandLight',113,47,196,72);text('AI FOR ALL',1800,83,20,C.muted,'right');
 if(i===0){for(let r of [245,350,455]){g.save();g.translate(960,535);g.scale(1.85,.7);orbit(0,0,r,t,3);g.restore()}reveal(t,0,()=>text('AI 普惠宣言',960,467,139,C.fg,'center',true),1.5);reveal(t,1.5,()=>text('让 AI 用得起，更用得好。',960,655,53,C.accent,'center'));reveal(t,3,()=>text('一心普惠 · 二力相生 · 三重飞轮 · 万千可能 · 生生不息',960,853,29,C.muted,'center'));return}
 if(i===1){heading(i,t);reveal(t,1.1,()=>{text('降低使用门槛',120,610,45,C.fg,'left',true);text('拓展人的能力与选择',120,688,45,C.fg,'left',true)});g.save();g.translate(1320,608);g.scale(.91,.91);vision(0,0,230,t);g.restore();return}
 if(i===2){heading(i,t);const sep=160+80*(1-ease(t/2));orbit(960-sep,690,214,t,3);orbit(960+sep,690,214,-t,3);text('开源之力',960-sep-70,672,44,C.fg,'center',true);text('降低门槛',960-sep-70,737,27,C.muted,'center');text('开发者之力',960+sep+70,672,44,C.fg,'center',true);text('拓展可能',960+sep+70,737,27,C.muted,'center');reveal(t,2,()=>{text('项目',960,659,26,C.accent,'center');text('社区',960,712,26,C.accent,'center')});return}
 if(i===3){heading(i,t,true);const names=['AI 能力','数字公共品','AI 普惠'];names.forEach((n,j)=>reveal(t,.6+j*.7,()=>{let x=370+j*590;circle(x,690,j===1?141:112,null,C.line,2);text(n,x,683,j===1?47:42,C.fg,'center',true);text(['开放可用','共享 · 复用 · 维护','真实帮助'][j],x,754,24,C.muted,'center');if(j<2){line(x+151,690,x+427,690);const p=((t*.28)%1);circle(x+151+276*p,690,6,C.accent,null)}}));return}
 if(i===4){heading(i,t,true);['数据','人才','价值'].forEach((n,j)=>reveal(t,.5+j*.55,()=>{const x=465+j*495;orbit(x,705,150,t+j,3);circle(x,705,108,null,C.line,1);text(n,x,691,60,C.accent,'center',true);text(['证据与判断','能力与创造','资源与持续'][j],x,769,27,C.muted,'center');if(j<2)text('⇄',x+245,705,43,C.accent,'center')}));return}
 if([5,6,7].includes(i)){heading(i,t);const sets=[['数据采集','基准建设','平台支撑','评价应用'],['贡献评价','成长可见','人才汇聚','供给改善','普惠增进'],['资源投入','贡献识别','价值回馈','成效验证']];wheel(1350,660,235,t,scenes[i][0],sets[i-5]);const lines=[['从数据中形成证据','在反馈中完善方法'],['学习、创造、维护','每一种贡献都值得尊重'],['连接资源与真实需要','让投入支持下一轮实践']][i-5];reveal(t,1,()=>text(lines[0],120,610,43,C.fg,'left',true));reveal(t,2.5,()=>text(lines[1],120,695,43,C.fg,'left',true));reveal(t,4.5,()=>{line(120,784,656,784,C.accent,2);text('实践反馈，进入下一轮',120,841,26,C.muted)});return}
 if(i===8){heading(i,t);network(1230,677,t,.97);['学习','工作','社区','本地实践'].forEach((n,j)=>reveal(t,.8+j*.65,()=>{circle(139,554+j*91,5,C.accent,null);text(n,178,554+j*91,42,C.fg,'left',true)}));return}
 if(i===9){heading(i,t);tree(1360,923,t,.8);reveal(t,1.7,()=>text('公开记录，积累证据',120,600,42,C.fg,'left',true));reveal(t,3.7,()=>text('多方参与，检验成效',120,690,42,C.fg,'left',true));reveal(t,5.7,()=>text('经验回到根部，推动下一轮生长',120,833,30,C.accent));return}
 if(i===10){reveal(t,.1,()=>text('让 AI 用得起，更用得好。',960,258,76,C.fg,'center',true));['一心普惠','二力相生','三重飞轮','万千可能','生生不息'].forEach((n,j)=>reveal(t,.3+j*.12,()=>{let x=330+j*315;mini(j,x,458,t);text(n,x,557,32,C.accent,'center')}));reveal(t,1.3,()=>{text('共同把愿景，变成行动。',830,733,52,C.fg,'center',true);text('www.x-lab.info/ai-for-all/',830,811,30,C.muted,'center');qr(1415,664,202);text('阅读宣言 · 加入共建',1516,899,22,C.muted,'center')});reveal(t,2,()=>{text('Music: Heroic Age — Kevin MacLeod (incompetech.com)',120,998,18,C.muted);text('CC BY 4.0 · creativecommons.org/licenses/by/4.0/ · excerpt / mix',120,1030,17,C.muted)});}
}

function foundation(isDark=true){palette(isDark);g.globalAlpha=1;g.fillStyle=C.bg;g.fillRect(0,0,W,H);if(isDark)glow(960,560,800,.035+ENERGY*.055);img('brandDark',113,47,196,72);text('AI FOR ALL',1800,83,20,C.muted,'right')}
function cinematicTitle(kicker,title,sub,t){reveal(t,.05,()=>{if(CHAPTERS[kicker])chapterLabel(CHAPTERS[kicker],kicker,960,196,'center');else text(kicker,960,196,32,C.accent,'center')});reveal(t,.3,()=>text(title,960,300,82,C.fg,'center',true));if(sub)reveal(t,1.1,()=>text(sub,960,405,31,C.muted,'center'))}

function cover(t){
 foundation();g.fillStyle='#1c2e27';g.fillRect(0,0,W,H);glow(960,560,800,.1);img('brandDark',97,39,220,93);text('AI FOR ALL   /   X-LAB AI',346,87,24,C.fg);line(104,154,1816,154,C.line,1.5);
 for(let k=0;k<4;k++){g.save();g.translate(960,571);g.rotate((k-1.5)*.14);g.scale(1.85,.74+k*.05);g.globalAlpha=.22;orbit(0,0,325+k*48,t,3);g.restore()}
 for(let k=0;k<45;k++){const x=120+((k*367)%1680),y=182+((k*173)%810);circle(x,y,1.7,C.line,null)}
 for(const [x,y,sx,sy]of [[184,239,1,1],[1736,239,-1,1],[184,949,1,-1],[1736,949,-1,-1]]){line(x,y,x+44*sx,y,C.line,2);line(x,y,x,y+44*sy,C.line,2)}
 text('A  I    F  O  R    A  L  L',960,330,33,C.accent,'center');text('AI 普惠宣言',960,477,145,C.fg,'center',true);line(510,603,1410,603,C.line,2);text('让 AI 用得起，更用得好。',960,686,53,C.fg,'center');text('让更多人参与创造，共享技术进步的成果。',960,765,30,C.muted,'center');['一心普惠','二力相生','三重飞轮','万千可能','生生不息'].forEach((n,j)=>chapterLabel(['一','二','三','万','生'][j],n,365+j*300,872,'center',28));
}
function declaration(t){
 foundation();text('我们的主张',118,215,32,C.accent);text('让更多人，共享技术进步',118,306,60,C.fg,'left',true);
 // Preserve the complete supplied statement. Its two sentences appear in sequence and remain visible.
 const first=['人工智能（AI）正在改变人们','学习、创造与解决问题的方式。'];
 const second=['我们主张，让更多人能够获得','和运用 AI 能力，参与创造，','共享技术进步的成果。'];
 reveal(t,.35,()=>first.forEach((v,j)=>text(v,118,462+j*62,37,C.fg)),1);
 reveal(t,2.4,()=>{line(118,586,690,586,C.line,2);second.forEach((v,j)=>text(v,118,660+j*64,37,j===2?C.accent:C.fg,'left',j===2))},1);
 g.save();g.translate(1360,601);const rs=[148,239,329,405];rs.forEach((r,k)=>{circle(0,0,r,k===2?C.soft:null,C.line,k===2?2:1.5)});
 // Redraw inner rings above the lightly filled middle disk.
 circle(0,0,148,null,C.line);circle(0,0,239,null,C.line);
 rs.slice(1).forEach((r,k)=>{for(let j=0;j<3;j++)bead(0,0,r,MOTION*(.06+k*.017)+j*2.1,4+((k+j)%3))});
 ['一','二','三','万','生'].forEach((n,j)=>{let a=-Math.PI/2+j*Math.PI*2/5;let x=329*Math.cos(a),y=329*Math.sin(a);circle(x,y,43,C.bg,C.accent,2);text(n,x,y-2,48,'#e1d79c','center',true);text(['一心普惠','二力相生','三重飞轮','万千可能','生生不息'][j],x,y+77,29,C.fg,'center',true)});
 img('icon',-69,-129,138,164);text('AI FOR ALL',0,65,34,C.fg,'center');text('共同的愿景',0,114,26,C.accent,'center');g.restore();
}
function completeWheel(kind,t){
 const data=[
 {title:'数据飞轮',headline:'以数据支撑判断',steps:['数据采集','基准建设','平台支撑','评价应用'],lines:['以开源实践数据为基础，完善指标与基准。','让评价服务贡献识别、协作分析与效果检验。'],support:['OpenDigger  数据与指标','OSIDX  指数与基准探索','OpenShare  平台实践'],feedback:'评价反馈 → 改进数据采集'},
 {title:'人才飞轮',headline:'以人才推动创造',steps:['贡献评价','成长可见','人才汇聚','供给改善','普惠增进'],lines:['多维评价，让成长可见，让贡献得到认可。','以反馈、回馈与实践机会，支持持续成长。'],support:['学习 · 创造 · 维护','改善数字公共品的质量、可用性与持续供给','让更多人获得切实帮助'],feedback:'新的贡献与成效 → 纳入评价'},
 {title:'价值飞轮',headline:'以价值促进投入',steps:['资源投入','贡献识别','价值回馈','成效验证'],lines:['提供模型调用额度、资金、岗位与实践机会。','明确使用条件、支持范围与合作责任。'],support:['OpenRank  协作网络评价 + 多维实践证据','完善贡献核算、人才识别与资源匹配','结合具体情境，接受实践检验'],feedback:'验证结果 → 支持下一轮投入'}
 ][kind];
 foundation(kind!==1);chapterLabel('三','三重飞轮 · '+data.title,120,211,'left',37);text(data.headline,120,315,72,C.fg,'left',true);
 reveal(t,.35,()=>data.lines.forEach((v,j)=>text(v,120,481+j*65,31,C.fg)),.7);
 reveal(t,1.3,()=>{line(120,604,820,604,C.line,1.5);data.support.forEach((v,j)=>{circle(130,673+j*63,4,C.accent,null);text(v,154,673+j*63,kind===2?28:29,C.muted)})},.7);
 const x=1394,y=644,r=239;
 circle(x,y,r,null,C.line,2);circle(x,y,142,null,C.line,1);text(data.title,x,y,44,C.accent,'center',true);
 const count=data.steps.length,active=Math.floor(Math.max(0,t)/2)%count;
 data.steps.forEach((s,j)=>{let a=-Math.PI/2+j*2*Math.PI/count,xx=x+r*Math.cos(a),yy=y+r*Math.sin(a);g.fillStyle=C.bg;g.fillRect(xx-105,yy-31,210,62);text(s,xx,yy,33,j===active?C.accent:C.fg,'center',j===active);
 let mid=a+Math.PI/count,tx=x+r*Math.cos(mid),ty=y+r*Math.sin(mid);g.save();g.translate(tx,ty);g.rotate(mid+Math.PI/2);g.beginPath();g.moveTo(8,0);g.lineTo(-6,-5);g.lineTo(-6,5);g.closePath();g.fillStyle=C.accent;g.fill();g.restore();});
 bead(x,y,r,-Math.PI/2+t*.34,6);reveal(t,2,()=>text(data.feedback,1394,982,29,C.accent,'center'));
}
function draw(i,t){
 let frame=Math.min(MUSIC.energy.length-1,Math.max(0,Math.round(globalTime*FPS)));ENERGY=MUSIC.energy[frame]||0;PULSE=MUSIC.pulse[frame]||0;MOTION=phase[frame]||0;
 if(i===0){cover(t);return}
 if(i===1){declaration(t);return}
 if(i===2){foundation();chapterLabel('一','一心普惠',120,211);text('让 AI 拓展人的能力与选择',120,315,65,C.fg,'left',true);
 const rows=[['面向开发者','支持学习、构建应用与可靠运行。'],['面向社会大众','让技术进入生活与工作，增进日常福祉。'],['面向全球南方','尊重语言与资源差异，拓展发展机会。']];
 rows.forEach(([title,sub],j)=>reveal(t,.25+j*.65,()=>{text(title,120,494+j*151,39,C.accent,'left',true);text(sub,120,553+j*151,29,C.fg)}));
 g.save();g.translate(1360,670);g.scale(.93,.93);vision(0,0,218,t);g.restore();return}
 if(i===3){original(2,t);return}
 if(i===4){original(3,t);reveal(t,2,()=>text('以数据支撑判断，以人才推动创造，以价值促进投入。',960,944,31,C.accent,'center'));return}
  if(i===8){foundation();cinematicTitle('三重飞轮','共同运转，彼此推动','',t);['数据','人才','价值'].forEach((n,j)=>{const x=465+j*495;let r=151+PULSE*4;orbit(x,659,r,t,4);circle(x,659,108,null,C.line,1);text(n,x,659,63,C.accent,'center',true);if(j<2){line(x+166,659,x+325,659,C.accent,2);circle(x+166+((globalTime*.85)%1)*159,659,6,C.accent,null)}});reveal(t,.8,()=>text('让愿景持续运转',960,913,43,C.fg,'center',true));return}
 if(i===11){foundation();reveal(t,.05,()=>text('五层相连，就是 AI 普惠的全景',960,280,66,C.fg,'center',true),.5);let labels=['一心普惠','二力相生','三重飞轮','万千可能','生生不息'];labels.forEach((n,j)=>reveal(t,j*.75,()=>{let x=330+j*315;g.save();g.translate(x,540);g.scale(1.5,1.5);mini(j,0,0,t);g.restore();chapterLabel(['一','二','三','万','生'][j],n,x,693,'center',42)}));reveal(t,4.2,()=>text('共同愿景，汇成持续行动。',960,859,48,C.fg,'center',true));return}
 if(i>=5&&i<=7){completeWheel(i-5,t);return}
 if(i===9){foundation();chapterLabel('万','万千可能',130,230);text('回应千差万别的需要',130,325,64,C.fg,'left',true);network(1300,661,t*1.5,1.02);['学习与创造','工作与社区','本地需求与实践'].forEach((n,j)=>reveal(t,.25+j*.6,()=>text(n,130,535+j*115,47,C.fg,'left',true)));return}
 if(i===10){foundation();cinematicTitle('生生不息','每一轮实践，都是新的起点','实践 → 记录 → 检验 → 改进',t);tree(960,965,t*1.15,.94);return}
 if(i===12){foundation();reveal(t,.03,()=>text('让 AI 用得起，更用得好。',960,290,90,C.fg,'center',true),.5);reveal(t,.8,()=>text('共同把愿景，变成行动。',960,454,50,C.accent,'center',true));reveal(t,1.5,()=>{qr(846,595,228);text('阅读宣言 · 加入共建',960,879,28,C.muted,'center');text('www.x-lab.info/ai-for-all/',960,953,27,C.muted,'center')});return}
}
async function main(){for(const [key,n]of Object.entries({brandDark:'brand-dark.svg',brandLight:'brand.svg',icon:'brand-icon.svg'}))images[key]=await loadImage(path.join(AS,n));
if(process.argv.includes('--preview')){for(let i=0;i<D.length;i++){globalTime=CUTS[i]+Math.min(i===1?12:5,D[i]-.5);draw(i,Math.min(i===1?12:5,D[i]-.5));fs.writeFileSync(path.join(OUT,'preview',`scene-${String(i+1).padStart(2,'0')}.png`),layer.toBuffer('image/png'));}return}
let proc=cp.spawn('ffmpeg',['-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pix_fmt','rgba','-s',`${W}x${H}`,'-r',`${FPS}`,'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',path.join(OUT,'visual.mp4')],{stdio:['pipe','ignore','inherit']});
for(let i=0;i<D.length;i++){for(let f=0;f<Math.round(D[i]*FPS);f++){let t=f/FPS;globalTime=CUTS[i]+t;ctx.globalAlpha=1;
// Every cut receives a smooth cubic dissolve. Typography fades in sequence to avoid ghosting.
let dissolve=[8,11].includes(i)?.70:.90;
if(i>0&&t<dissolve){
 const u=t/dissolve;
 TEXT_FADE=1-sm(u/.50);draw(i-1,D[i-1]+t);ctx.drawImage(layer,0,0);
 TEXT_FADE=sm((u-.42)/.58);draw(i,t);ctx.globalAlpha=sm(u);ctx.drawImage(layer,0,0);
 TEXT_FADE=1;
}else{TEXT_FADE=1;draw(i,t);ctx.drawImage(layer,0,0)}
ctx.globalAlpha=1;if(globalTime<.35){ctx.fillStyle=`rgba(6,20,16,${1-sm(globalTime/.35)})`;ctx.fillRect(0,0,W,H)}if(globalTime>TOTAL-.7){ctx.fillStyle=`rgba(6,20,16,${sm((globalTime-(TOTAL-.7))/.7)})`;ctx.fillRect(0,0,W,H)}if(!proc.stdin.write(frames.data()))await once(proc.stdin,'drain');}console.log(`Rendered ${CUTS[i+1].toFixed(2)}/${TOTAL} seconds`)}proc.stdin.end();const [code]=await once(proc,'close');if(code)throw Error('ffmpeg '+code)}
main().catch(e=>{console.error(e);process.exit(1)});
