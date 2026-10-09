// Code-native cinematic bookends. All motion is deterministic; no external footage.
module.exports=function({g,W,H,C,text,line,box,image,arrow,ring}){
 const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>1-(1-clamp(x))**3;
 function reveal(t,start,duration,draw){let a=ease((t-start)/duration);if(!a)return;g.save();g.globalAlpha*=a;g.translate(0,(1-a)*18);draw();g.restore();}
 function halo(x,y,r,alpha){g.save();let c=g.createRadialGradient(x,y,0,x,y,r);c.addColorStop(0,`rgba(163,202,109,${alpha})`);c.addColorStop(.6,`rgba(82,140,101,${alpha*.3})`);c.addColorStop(1,'rgba(16,44,37,0)');g.fillStyle=c;g.fillRect(x-r,y-r,r*2,r*2);g.restore();}
 function ellipse(cx,cy,rx,ry,rot,start,end,alpha,width=1){g.save();g.globalAlpha*=alpha;g.strokeStyle=C.accent;g.lineWidth=width;g.beginPath();g.ellipse(cx,cy,rx,ry,rot,start,end);g.stroke();g.restore();}
 function dust(t,alpha){g.save();for(let n=0;n<62;n++){let x=95+(n*271.73)%1730,y=160+(n*139.31)%735;g.globalAlpha=alpha*(.3+.7*(.5+.5*Math.sin(n*2.1+t*.5)));g.fillStyle=C.accent;g.beginPath();g.arc(x,y, n%7===0?1.6:.8,0,7);g.fill();}g.restore();}
 function corner(x,y,dx,dy,a){g.save();g.globalAlpha=a;line(x,y,x+dx*35,y,C.accent,2);line(x,y,x,y+dy*35,C.accent,2);g.restore();}
 function orbit(cx,cy,rx,ry,rot,t,alpha){
   ellipse(cx,cy,rx,ry,rot,0,Math.PI*2,alpha*.22);
   let a=t*.3;ellipse(cx,cy,rx,ry,rot,a,a+1.25,alpha*.6,1.7);
   const p={x:rx*Math.cos(a),y:ry*Math.sin(a)},x=cx+p.x*Math.cos(rot)-p.y*Math.sin(rot),y=cy+p.x*Math.sin(rot)+p.y*Math.cos(rot);
   g.save();g.globalAlpha*=alpha;g.fillStyle=C.accent;g.beginPath();g.arc(x,y,3.5,0,7);g.fill();g.restore();
 }
 function opening(t){
   halo(960,470,820,.19);dust(t,.3);
   let gather=ease(t/1.9),spread=1+(1-gather)*.32;
   // Orbital light gathers behind the title, with generous empty space around the words.
   orbit(960,465,755*spread,280*spread,-.15,t,.43);
   orbit(960,465,725*spread,305*spread,.16,-t+3,.28);
   ellipse(960,470,836,353,0,0,Math.PI*2,.09);
   for(let n=0;n<32;n++){
     let a=n/32*Math.PI*2+t*.025,rx=790+(1-gather)*(140+(n%5)*80),ry=305+(1-gather)*210;
     let x=960+Math.cos(a)*rx,y=470+Math.sin(a)*ry;
     g.save();g.globalAlpha=.14+.4*(1-gather);g.fillStyle=C.accent;g.beginPath();g.arc(x,y,1.4,0,7);g.fill();g.restore();
   }
   // A low-opacity title is present from frame one; the main reveal is under one second.
   g.save();let titleIn=.22+.78*ease(t/.95);g.globalAlpha=titleIn;g.translate(0,(1-titleIn)*22);
   g.shadowColor='rgba(199,231,151,.25)';g.shadowBlur=22;
   g.font='bold 156px Han';g.fillStyle=C.fg;g.textAlign='center';g.textBaseline='middle';g.fillText('AI 普惠宣言',960,444);g.restore();
   reveal(t,.6,.8,()=>text('A I   F O R   A L L',960,298,27,C.accent,'center'));
   let drawLine=ease((t-.6)/1.2);line(960-555*drawLine,558,960+555*drawLine,558,C.line,1);
   line(960-92*drawLine,558,960+92*drawLine,558,C.accent,3);
   // One controlled light sweep after the title lands.
   if(t>.55&&t<2.2){let x=405+(t-.55)/1.65*1110;halo(x,558,92,.28);}
   reveal(t,1.15,1,()=>text('让 AI 用得起，更用得好。',960,642,52,C.accent,'center'));
   reveal(t,2,1.2,()=>text('让每个人，都有创造未来的机会。',960,719,33,C.fg,'center'));
   reveal(t,3,.8,()=>{text('一个目标   ·   两股力量   ·   一个内核   ·   两个飞轮   ·   三重普惠',960,849,24,C.muted,'center');});
   let ca=.4*ease((t-.4)/1.6);corner(190,215,1,1,ca);corner(1730,215,-1,1,ca);corner(190,875,1,-1,ca);corner(1730,875,-1,-1,ca);
 }
 function trace(x1,y1,x2,y2,t,alpha=.6){let p=clamp(t);g.save();g.globalAlpha=alpha;line(x1,y1,x1+(x2-x1)*p,y1+(y2-y1)*p,C.accent,2);g.restore();}
 function closing(t){
   const mt=Math.min(t,7);halo(1225,547,650,.1);dust(mt,.14);
   reveal(t,0,.75,()=>{text('让创造，惠及更多人。',105,196,64,C.fg);text('一个完整框架，一份长期承诺',108,269,26,C.muted);});
   // Five parts appear in narrative order and form one complete composition by 5.4 s.
   reveal(t,.3,.7,()=>{box(170,320,1580,82,true);text('一个目标',202,360,23,C.muted);text('AI 普惠：用得起，更用得好',960,360,36,C.accent,'center');});
   reveal(t,.85,.85,()=>{box(170,429,420,217);text('两股力量',203,466,23,C.muted);text('开源 × 开发者',380,543,39,C.fg,'center');text('开放技术  ·  放大创造',380,600,23,C.muted,'center');});
   reveal(t,1.45,.8,()=>{box(700,429,1050,217);text('两个飞轮',730,466,23,C.muted);
     ring(954,540,78,'成长','',mt);ring(1510,540,78,'投入','',mt);
     text('公共品创造价值',1230,500,21,C.muted,'center');arrow(1080,526,1380,526,C.accent);
     arrow(1380,568,1080,568,C.accent);text('资源支持成长',1230,602,21,C.muted,'center');
   });
   if(t>1.7)trace(605,540,685,540,(t-1.7)/.7);
   reveal(t,2.45,.8,()=>{box(170,688,1580,76,true);text('一个内核',202,726,23,C.muted);text('数据与评价',960,726,35,C.accent,'center');text('识别贡献 · 匹配资源 · 核验效果',1715,726,22,C.muted,'right');});
   // Paired streams: practice enters the core; evidence informs the two wheels.
   if(t>2.9){let p=ease((t-2.9)/.85);[954,1510].forEach(x=>{trace(x-9,650,x-9,682,p,.5);trace(x+9,682,x+9,650,p,.5);});}
   reveal(t,3.3,.65,()=>text('实践证据汇入  ·  评价依据反馈',1225,667,18,C.muted,'center'));
   reveal(t,3.8,.7,()=>{text('三重普惠',218,810,24,C.muted);text('开发者   ·   大众   ·   全球南方',1065,810,34,C.fg,'center');});
   reveal(t,4.75,.65,()=>{line(170,848,1750,848,C.line);text('加入 X-lab AI，现在就一起行动！',960,884,38,C.accent,'center');text('github.com/X-lab2017/ai-for-all',960,929,25,C.muted,'center');});
   // A single perimeter light pass seals the assembled panorama; then a calm final hold.
   if(t>5.2&&t<7){let p=(t-5.2)/1.8, x=170+1580*p;halo(x,848,95,.15);}
   const a=.32*ease((t-4.8)/1.5);corner(145,310,1,1,a);corner(1775,310,-1,1,a);corner(145,846,1,-1,a);corner(1775,846,-1,-1,a);
 }
 return {opening,closing};
};
