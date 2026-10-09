// Deterministic 1920x1080 / 30fps motion film. No browser capture.
const fs=require('fs'),path=require('path'),cp=require('child_process');
const {once}=require('events');
const {createCanvas,loadImage,GlobalFonts}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'@napi-rs/canvas'));
const ROOT=path.resolve(__dirname,'../../..'),OUT=process.env.FILM_OUTPUT||path.join(ROOT,'../video-build');fs.mkdirSync(OUT,{recursive:true});
GlobalFonts.registerFromPath(process.env.FILM_FONT||'/root/.local/share/fonts/SourceHanSansSC-Regular.otf','Han');
const captions=fs.existsSync(path.join(OUT,'captions.json'))?JSON.parse(fs.readFileSync(path.join(OUT,'captions.json'))):[];
const LANG=process.env.RELEASE_LANG||'en',EN=LANG==='en';
const dictionary={...require('./deck-en.json'),...require('./film-text-en.json')};
const translate=s=>EN?(dictionary[s]||s):s;
const story=require('../../manifesto-film/source/story.json'), W=1920,H=1080,FPS=30,c=createCanvas(W,H),g=c.getContext('2d');
const C={bg:'#102c25',fg:'#eff4ec',accent:'#cce89d',muted:'#a9c0af',line:'#426450',card:'#19392e'};let imgs={},time=0;
function text(s,x,y,size=32,col=C.fg,align='left',maxWidth=null){s=translate(s);g.font=`${size}px Han`;if(EN){let limit=maxWidth||((size>=55||x===960)?1710:(align==='center'?Math.min(1400,2*Math.min(x-90,1830-x)):(align==='right'?x-105:1810-x)));while(g.measureText(s).width>limit&&size>14){size-=.5;g.font=`${size}px Han`;}}g.fillStyle=col;g.textAlign=align;g.textBaseline='middle';g.fillText(s,x,y);}

function line(x,y,x2,y2,col=C.line,w=2){g.strokeStyle=col;g.lineWidth=w;g.beginPath();g.moveTo(x,y);g.lineTo(x2,y2);g.stroke();}
function box(x,y,w,h,active=false){g.fillStyle=active?'#294b35':C.card;g.strokeStyle=active?C.accent:C.line;g.lineWidth=active?3:1;g.beginPath();g.roundRect(x,y,w,h,12);g.fill();g.stroke();}
function image(key,x,y,w,h){let im=imgs[key],k=Math.min(w/im.width,h/im.height);g.drawImage(im,x+(w-im.width*k)/2,y+(h-im.height*k)/2,im.width*k,im.height*k);}
function arrow(x,y,x2,y2,col=C.accent){line(x,y,x2,y2,col);let a=Math.atan2(y2-y,x2-x);line(x2,y2,x2-14*Math.cos(a-.5),y2-14*Math.sin(a-.5),col);line(x2,y2,x2-14*Math.cos(a+.5),y2-14*Math.sin(a+.5),col);}
function ring(x,y,r,label,sub,t,col=C.accent){g.strokeStyle=C.line;g.lineWidth=2;g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.stroke();g.strokeStyle=col;g.lineWidth=3;g.beginPath();g.arc(x,y,r,t*.32,t*.32+4.4);g.stroke();let a=t*.32;g.fillStyle=col;g.beginPath();g.arc(x+Math.cos(a)*r,y+Math.sin(a)*r,6,0,7);g.fill();text(label,x,y-8,Math.max(27,r*.23),col,'center',r*1.85);text(sub,x,y+35,21,C.muted,'center',r*2.4);}
const ceremony=require('./ceremony_release')({g,W,H,C,text,line,box,image,arrow,ring,EN});
const titles=['让 AI 用得起，更用得好。','开放协作，成为共同基础。','开放的能力，更多人的创造。','开源降低门槛，创造改变未来。','让开放的成果，成为真正的帮助。','让贡献被看见，让支持有依据。','两轮相促，持续发生。','把愿景落到实践，用行动检验承诺。','改变，就从我们开始！','现在，就一起行动！'];
const subtitles=['一个目标 · 两股力量 · 一个内核 · 两个飞轮 · 三重普惠','1991 — 2026 / 35 YEARS OF LINUX','开放模型 → 开发者再创造 → 真实场景','开源降低门槛，开发者放大创造','数字公共品连接创造与实际受益','平台、证据、方法与研究相互配合','成长创造价值，投入支持持续实践','数据、方法与生态，共同连接愿景','开发者、开源社区与合作伙伴，共同建设','一个完整框架，一份长期承诺'];
function header(i){image('brand',105,45,185,55);text('AI FOR ALL  /  X-LAB AI',340,74,21,C.muted);text(`${String(i+1).padStart(2,'0')} / 10`,1810,74,22,C.muted,'right');line(105,120,1810,120);if(i===0||i===9)return;text(titles[i],105,205,i===8?56:64);text(subtitles[i],108,288,27,C.muted);}
function card(x,y,w,h,title,sub,active=false){box(x,y,w,h,active);text(title,x+30,y+70,40,active?C.accent:C.fg,'left',w-60);text(sub,x+30,y+132,24,C.muted,'left',w-60);}
function drawScene(i,t){
 if(i===0){ceremony.opening(t);return;}
 if(i===9){ceremony.closing(t);return;}
 let step=Math.floor(t/1.8);
 if(i===1){text('35',120,505,240,C.accent);text('YEARS OF LINUX',125,680,33,C.muted);image('linux',660,365,1130,460);text('个人项目  →  共同维护  →  广泛采用',660,852,32,C.accent);}
 if(i===2){let names=['阿里巴巴','深度求索','智谱 AI','月之暗面','腾讯'],models=['Qwen','DeepSeek','GLM','Kimi','混元 / Hunyuan'],keys=['qwen','deepseek','glm','kimi','hunyuan'];for(let n=0;n<5;n++){let x=105+n*345;box(x,380,320,335,step===0);g.fillStyle='#f4f5ef';g.fillRect(x+20,405,280,100);image(keys[n],x+40,420,240,70);text(names[n],x+160,562,33,C.fg,'center');text(models[n],x+160,626,27,C.accent,'center');}text('更多人能够学习、构建和改进',960,805,42,C.accent,'center');text('机构与模型系列介绍；各版本许可分别适用，不构成排名或背书。',960,872,20,C.muted,'center');}
 if(i===3){card(105,380,735,310,'开源之力','开放技术、知识与工具',step===0);card(1080,380,735,310,'开发者之力','学习、实践、协作与反馈',step===1);text('×',960,520,85,C.accent,'center');text('技术的普惠性   ×   开发者的创造力',960,795,46,C.accent,'center');}
 if(i===4){let a=['AI 能力','数字公共品','采用与本地化','真实帮助'],b=['技术与创造','工具、数据与知识','适合实际需要','反馈与效果'];for(let n=0;n<4;n++){let x=105+n*440;card(x,420,390,250,a[n],b[n],step===n);if(n<3)arrow(x+397,540,x+435,540);}text('可共享的成果，值得持续维护。',960,790,44,C.accent,'center');}
 if(i===5){ring(430,590,215,'数据与评价','识别贡献 · 匹配资源 · 核验效果',t);['平台连接','数据证据','评价方法','评价研究'].forEach((v,n)=>{let x=850+(n%2)*490,y=385+Math.floor(n/2)*210;card(x,y,450,175,v,['连接参与者与实践','形成可追溯的依据','解释贡献与效果','检验方法本身'][n],step===1);});text('评价帮助人成长，不以单一分数定义人的价值。',960,875,28,C.muted,'center');}
 if(i===6){ring(475,570,190,'成长飞轮','从实践，到创造',t);ring(1450,570,190,'投入飞轮','从支持，到持续',t,'#b8c9e4');let a=[['实践贡献','贡献可见','人才成长','公共品与应用'],['资源投入','匹配支持','价值实现','效果验证']];[475,1450].forEach((x,k)=>a[k].forEach((v,n)=>{let ang=n*Math.PI/2-Math.PI/2,xx=x+Math.cos(ang)*230,yy=570+Math.sin(ang)*195;box(xx-108,yy-34,216,68,Math.floor(t/2)%4===n);text(v,xx,yy,25,C.fg,'center');}));arrow(795,510,1120,510);text('公共品创造价值',960,473,23,C.muted,'center');arrow(1120,615,795,615);text('资源支持成长',960,660,23,C.muted,'center');box(180,815,1560,85,step===2);text('共同内核：数据与评价',960,856,36,C.accent,'center');}
 if(i===7){['OpenDigger','OpenRank','OpenShare'].forEach((v,n)=>card(105+n*580,405,550,300,v,['开源数据与指标','协作网络评价','能力与资源连接'][n],step===n));text('公开记录进展与局限，让实践检验承诺。',960,805,40,C.accent,'center');text('已有实践基础，不等同于本行动已经实现的普惠成效。',960,869,22,C.muted,'center');}
 if(i===8){['开发者','开源社区','合作伙伴'].forEach((v,n)=>card(105+n*580,395,550,310,v,['分享需要，贡献工具与案例','组织学习，带回采用反馈','提供资源，开放应用场景'][n],step===0));text('开放资源    ·    支持创造    ·    公开记录',960,808,40,C.accent,'center');}
}
function subtitle(i,t){g.fillStyle='#091e19';g.fillRect(0,955,W,125);let cap=captions.find(v=>time>=v.start&&time<v.end);if(LANG==='bilingual'){text(cap?cap.text:'',960,980,29,C.fg,'center');text(cap?cap.en:'',960,1019,23,C.muted,'center');}else{text(cap?cap.text:'',960,998,32,C.fg,'center');}text('AI 普惠宣言 · X-lab AI',105,1053,17,C.muted);if(i===9){text('Music: Heroic Age — Kevin MacLeod (incompetech.com) · excerpt / mix',1810,1041,15,C.muted,'right');text('CC BY 4.0 · creativecommons.org/licenses/by/4.0/',1810,1062,15,C.muted,'right');}line(0,1076,W*(time/90),1076,C.accent,4);}

async function main(){let a=path.join(ROOT,'site/presentation/assets'),brand=path.join(ROOT,'site/assets');for(let [key,file] of Object.entries({brand:brand+'/XlabAI_Horizontal_ColorDark.svg',symbol:brand+'/XlabAI_Symbol_ColorLight.svg',linux:a+'/linux35.png',qwen:a+'/qwen.png',deepseek:a+'/deepseek.svg',glm:path.join(OUT,'glm.png'),kimi:a+'/kimi.png',hunyuan:a+'/hunyuan.png'}))imgs[key]=await loadImage(file);
 let preview=process.argv.includes('--preview'),proc;if(!preview)proc=cp.spawn('ffmpeg',['-y','-f','rawvideo','-pix_fmt','rgba','-s',`${W}x${H}`,'-r',String(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',path.join(OUT,'AI-for-All-90s-visual.mp4')],{stdio:['pipe','ignore','inherit']});
 let start=0;for(let i=0;i<10;i++){let frames=preview?1:story[i].seconds*FPS;for(let f=0;f<frames;f++){let t=preview?Number(process.env.PREVIEW_TIME||3):f/FPS;time=start+t;g.fillStyle=C.bg;g.fillRect(0,0,W,H);g.save();g.translate(28*Math.max(0,1-t/.6)**3,0);header(i);g.save();let z=(i===0||i===9)?1:1+Math.min(t,5)*.0007;g.translate(960,560);g.scale(z,z);g.translate(-960,-560);drawScene(i,t);g.restore();if(i!==0&&i!==9)line(105,325,105+Math.min(230,t*260),325,C.accent,4);g.restore();subtitle(i,t);if(preview)fs.writeFileSync(path.join(OUT,`scene-${i+1}.png`),c.toBuffer('image/png'));else if(!proc.stdin.write(c.data()))await once(proc.stdin,'drain');}start+=story[i].seconds;console.log(`chapter ${i+1} done`);}if(proc){proc.stdin.end();const [code]=await once(proc,'close');if(code!==0)throw new Error(`ffmpeg exited ${code}`);}}
main().catch(e=>{console.error(e);process.exit(1)});
