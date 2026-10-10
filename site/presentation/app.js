(()=>{'use strict';
const $=(s,p=document)=>p.querySelector(s), $$=(s,p=document)=>[...p.querySelectorAll(s)];
const slides=$$('.slide'), stage=$('.stage'), reduce=matchMedia('(prefers-reduced-motion: reduce)');
let current=0, auto=false, elapsed=0, last=0, paused=reduce.matches, manualMotion=false;
const english=document.documentElement.lang==='en';
let themeMode='scene';try{themeMode=localStorage.getItem('aifa-deck-theme')||'scene';}catch(_){}
if(!['scene','light','dark'].includes(themeMode))themeMode='scene';
let lfx=0;
function applyTheme(){const effective=themeMode==='scene'?DECK[current].theme:themeMode;stage.dataset.theme=effective;document.documentElement.dataset.palette=effective;document.documentElement.dataset.uiTheme=themeMode;$('#theme').textContent=({scene:english?'◐ By chapter':'◐ 随章节',light:english?'☀ Light':'☀ 亮色',dark:english?'☾ Dark':'☾ 暗色'})[themeMode];$('#theme').setAttribute('aria-label',(english?'Theme: ':'主题：')+$('#theme').textContent+(english?'. Select to cycle.':'，点击切换'));}
$('#theme').addEventListener('click',()=>{themeMode=['scene','light','dark'][(['scene','light','dark'].indexOf(themeMode)+1)%3];try{localStorage.setItem('aifa-deck-theme',themeMode);}catch(_){}applyTheme();});
function updateLanguage(){const step=$('[data-step][aria-pressed="true"]',slides[current]);$('#language').href=(english?'index.html?lang=zh':'en.html?lang=en')+'&step='+(step?.dataset.step||0)+'&lfx='+lfx+'#s'+(current+1);}
$('#language').addEventListener('click',()=>{updateLanguage();try{localStorage.setItem('aifa-deck-language',english?'zh':'en');}catch(_){}});
function selectLfx(i,focus=false){lfx=i;$$('[data-lfx]').forEach((b,j)=>{b.setAttribute('aria-selected',String(i===j));b.tabIndex=i===j?0:-1;$('#lfx-panel-'+j).hidden=i!==j;if(focus&&i===j)b.focus();});updateLanguage();}
$$('[data-lfx]').forEach(b=>{b.addEventListener('click',()=>{stop();selectLfx(Number(b.dataset.lfx));});b.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();e.stopPropagation();stop();selectLfx(e.key==='Home'?0:e.key==='End'?1:1-lfx,true);}});});
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const legacyChapters={manifesto:1,origins:2,'open-models':3,forces:5,'public-goods':5,evaluation:7,flywheels:6,practice:11,participate:13,panorama:12};
const parsed=()=>clamp((legacyChapters[location.hash.slice(1)]||Number(location.hash.replace('#s',''))||1)-1,0,slides.length-1);
function playLabel(){ $('#autoplay').textContent=auto?(english?'Ⅱ Pause tour':'Ⅱ 暂停导览'):(english?'▷ Auto tour':'▷ 自动导览');$('#autoplay').setAttribute('aria-pressed',String(auto));}
function stop(){auto=false;playLabel();}
function go(n,fromAuto=false){
 n=clamp(n,0,slides.length-1);if(!fromAuto)stop();current=n;elapsed=0;
 slides.forEach((s,i)=>{s.hidden=i!==n;s.classList.toggle('enter',i===n);});
 applyTheme();$('#page-number').textContent=$('#counter').textContent=`${String(n+1).padStart(2,'0')} / 13`;
 $('#chapter-label').textContent=DECK[n].title;$('#previous').disabled=n===0;$('#next').disabled=n===12;
 $$('[data-go]').forEach(b=>{if(Number(b.dataset.go)===n)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
 $('#announcement').textContent=english?`Slide ${n+1}: ${DECK[n].title}`:`第 ${n+1} 页，${DECK[n].title}`;
 $('.play-progress i').style.width='0';history.replaceState(null,'',`#s${n+1}`);updateLanguage();
 if(matchMedia('(max-width:700px) and (orientation:portrait)').matches)window.scrollTo({top:0,behavior:'instant'});
}
function toggleAuto(){if(auto){stop();return;}if(current===12)go(0);auto=true;playLabel();}
$('#autoplay').addEventListener('click',toggleAuto);
$('#previous').addEventListener('click',()=>go(current-1));$('#next').addEventListener('click',()=>go(current+1));
$$('[data-go]').forEach(b=>b.addEventListener('click',()=>{b.closest('dialog')?.close();go(Number(b.dataset.go));}));
$$('a[href^="#s"]').filter(a=>/^#s\d+$/.test(a.getAttribute('href'))).forEach(a=>a.addEventListener('click',e=>{e.preventDefault();go(Number(a.getAttribute('href').slice(2))-1);}));
window.addEventListener('hashchange',()=>go(parsed()));
function selectStep(section,i){
 const s=DECK[Number(section.dataset.index)], data=s.steps[i];if(!data)return;
 $$('[data-step]',section).forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.step)===i)));
 $('.detail h3',section).textContent=data[0];$('.detail p',section).textContent=data[1];
 $$('[data-stage]',section).forEach(g=>g.classList.toggle('selected',Number(g.dataset.stage)===i));
 updateLanguage();
 if(section.classList.contains('possibilities'))$$('[data-community]',section).forEach(el=>{let yes=el.dataset.community.split(' ').includes(String(i))||el.dataset.community==='4';el.classList.toggle('net-dim',!yes);el.classList.toggle('net-bright',yes);});
}
$$('[data-step]').forEach(b=>b.addEventListener('click',()=>{stop();selectStep(b.closest('.slide'),Number(b.dataset.step));}));
function motionLabel(){document.body.classList.toggle('motion-paused',paused);$('#motion').textContent=paused?(english?'Play motion':'开启动效'):(english?'Pause motion':'暂停动效');$('#motion').setAttribute('aria-pressed',String(paused));}
$('#motion').addEventListener('click',()=>{manualMotion=true;paused=!paused;motionLabel();});
reduce.addEventListener('change',e=>{if(!manualMotion){paused=e.matches;motionLabel();}});motionLabel();
function escape(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function showInfo(){stop();const s=DECK[current];$('#info-title').textContent=`${String(current+1).padStart(2,'0')} / ${s.title}`;$('#info-body').innerHTML='<h3>'+(english?'Speaker notes':'讲述提示')+'</h3><p>'+escape(s.notes)+'</p><h3>'+(english?'Content and data sources':'内容与数据来源')+'</h3>'+SOURCES[s.source].map(x=>`<p><a href="${escape(x.url)}" target="_blank" rel="noopener noreferrer">${escape(x.label)} ↗</a><small>${escape(x.note)}</small></p>`).join('')+'<small>'+(english?'Based on the AI for All Manifesto v1.2. This is a presentation summary. Sources reviewed: 2026-10-10.':'正文基于 AI 普惠宣言 v1.2；本演示为讲述摘要。数据核验：2026-10-10。')+'</small>';$('#info').showModal();}
$('#notes').addEventListener('click',showInfo);$('#contents').addEventListener('click',()=>{stop();$('#toc').showModal();});
$$('[data-close]').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
$$('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}}));
async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else $('#hint').textContent=english?'Full screen is unavailable. Try browser full screen or landscape orientation.':'此浏览器不支持全屏接口，可使用浏览器全屏或横屏观看。';}catch(_){$('#hint').textContent=english?'Full screen could not be opened. Try browser full screen or landscape orientation.':'未进入全屏，可使用浏览器全屏或横屏观看。';}}
$('#fullscreen').addEventListener('click',fullscreen);
document.addEventListener('fullscreenchange',()=>{$('#fullscreen').textContent=document.fullscreenElement?'⊡':'⛶';$('#fullscreen').setAttribute('aria-label',document.fullscreenElement?(english?'Exit full screen':'退出全屏'):(english?'Full screen':'全屏演示'));});
document.addEventListener('keydown',e=>{
 if($('dialog[open]')||e.ctrlKey||e.metaKey||e.altKey||e.target.closest('input,textarea,select'))return;
 if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();go(current+1);}else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(current-1);}
 else if(e.key==='Home'){e.preventDefault();go(0);}else if(e.key==='End'){e.preventDefault();go(12);}
 else if(e.key===' '&&!e.target.closest('button,a')){e.preventDefault();toggleAuto();}
 else if(e.key.toLowerCase()==='f')fullscreen();else if(e.key.toLowerCase()==='n')showInfo();
});
let touch=null;stage.addEventListener('touchstart',e=>{if(e.target.closest('button,a'))return;touch=[e.touches[0].clientX,e.touches[0].clientY];},{passive:true});stage.addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch[0],dy=e.changedTouches[0].clientY-touch[1];touch=null;if(Math.abs(dx)>80&&Math.abs(dx)>Math.abs(dy)*2)go(current+(dx<0?1:-1));},{passive:true});
const areas=$$('.motion-area');
areas.forEach(a=>{a._t=0;a._speed=1;a._hover=false;a._section=a.closest('.slide');
 a.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse')a._hover=true;});a.addEventListener('pointerleave',()=>a._hover=false);
 a._perspectives=$$('[data-perspective]',a);a._satellites=$$('[data-satellite]',a);a._growth=$$('[data-growth]',a);a._buds=$$('[data-bud]',a);
 a._tracks=$$('[data-track]',a).map(el=>{const path=document.getElementById(el.dataset.track);if(!path)return null;return{el,path,len:path.getTotalLength(),phase:Number(el.dataset.phase||0),period:Number(el.dataset.period||32000),appear:Number(el.dataset.appear||0)};}).filter(Boolean);
 a._tracks.forEach(t=>{const p=t.path.getPointAtLength(t.phase*t.len);t.el.setAttribute('cx',p.x);t.el.setAttribute('cy',p.y);});
});
$$('[data-regrow]').forEach(b=>b.addEventListener('click',()=>{stop();$('.motion-area',b.closest('.slide'))._t=0;if(paused){paused=false;manualMotion=true;motionLabel();}}));
function frame(now){const dt=last?Math.min(now-last,100):0;last=now;
 if(!document.hidden){
  if(auto){elapsed+=dt;const limit=DECK[current].seconds*1000;$('.play-progress i').style.width=`${Math.min(100,elapsed/limit*100)}%`;if(current===1){const view=elapsed<limit/2?0:1;if(view!==lfx)selectLfx(view);}const steps=DECK[current].steps.length;if(steps)selectStep(slides[current],Math.min(steps-1,Math.floor(elapsed/limit*steps)));if(elapsed>=limit){if(current<12)go(current+1,true);else stop();}}
  if(!paused)for(const a of areas){if(a._section.hidden)continue;const target=a._hover?3:1;a._speed+=(target-a._speed)*(1-Math.exp(-dt/450));a._t+=dt*a._speed;const seconds=a._t/1000;
   a._perspectives.forEach(el=>{const angle=-Math.PI/2+Number(el.dataset.perspective)*Math.PI*2/3+seconds*Math.PI*2/165;el.setAttribute('transform',`translate(${320+192*Math.cos(angle)} ${320+192*Math.sin(angle)})`);});
   a._satellites.forEach(el=>{const angle=-Math.PI/2+Number(el.dataset.satellite)*Math.PI*2/3-seconds*Math.PI*2/95;el.setAttribute('transform',`translate(${80*Math.cos(angle)} ${80*Math.sin(angle)})`);});
   a._growth.forEach(el=>{const p=clamp((seconds-Number(el.dataset.growth)*1.8)/3,0,1);el.style.strokeDashoffset=String(1-p);});
   a._buds.forEach(el=>{const p=clamp((seconds-5-Number(el.dataset.bud)*.2)/3,0,1);el.style.opacity=String(.18+.82*p);});
   a._tracks.forEach(t=>{if(t.appear)t.el.style.opacity=String(clamp((seconds-t.appear/3)/2,0,1));const p=t.path.getPointAtLength(((a._t/t.period+t.phase)%1)*t.len);t.el.setAttribute('cx',p.x);t.el.setAttribute('cy',p.y);});
  }
 }
 requestAnimationFrame(frame);
}
const requested=new URLSearchParams(location.search);const requestedStep=Number(requested.get('step')||0), requestedLfx=Number(requested.get('lfx')||0);go(parsed());if(Number.isInteger(requestedStep))selectStep(slides[current],requestedStep);selectLfx(requestedLfx===1?1:0);requestAnimationFrame(frame);
})();
