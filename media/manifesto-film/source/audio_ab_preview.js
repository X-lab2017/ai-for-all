// Audio audition wrapper. Reuses the approved panorama without altering the film.
const fs=require('fs'),path=require('path'),cp=require('child_process'),{once}=require('events');
const {createCanvas,loadImage,GlobalFonts}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'@napi-rs/canvas'));
const OUT=process.env.FILM_OUTPUT||path.resolve(__dirname,'../../../../audio-ab-build');
GlobalFonts.registerFromPath(process.env.FILM_FONT||'/root/.local/share/fonts/SourceHanSansSC-Regular.otf','Han');
const c=createCanvas(1920,1080),g=c.getContext('2d');
function text(s,x,y,size,col='#eff4ec',align='left'){g.font=`${size}px Han`;g.fillStyle=col;g.textAlign=align;g.textBaseline='middle';g.fillText(s,x,y);}
async function main(){
 const bg=await loadImage(path.join(OUT,'scene-10.png'));
 for(const [key,name,music] of [['A','庄严磅礴','Reign'],['B','昂扬共创','Americana']]){
  const caps=JSON.parse(fs.readFileSync(path.join(OUT,`captions-${key}.json`)));
  const outfile=path.join(OUT,`AI-for-All-${key}-25s.mp4`);
  const p=cp.spawn('ffmpeg',['-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s','1920x1080','-r','30','-i','-',
    '-i',path.join(OUT,`AI-for-All-${key}-master.wav`),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','21',
    '-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-t','25','-movflags','+faststart',
    '-metadata',`title=AI for All — ${key} ${name} — audio audition`,
    '-metadata',`comment=Music: ${music} — Kevin MacLeod (incompetech.com); CC BY 4.0 https://creativecommons.org/licenses/by/4.0/; excerpt / edit / mix. AI voice: Qwen3-TTS VoiceDesign.`,outfile],{stdio:['pipe','ignore','inherit']});
  for(let f=0;f<750;f++){
   const t=f/30;g.drawImage(bg,0,0);
   g.fillStyle='#102c25';g.fillRect(1190,38,640,72);
   text(`${key}  /  ${name}  ·  声音试听`,1810,74,24,'#cce89d','right');
   g.fillStyle='#091e19';g.fillRect(0,955,1920,125);
   const cap=caps.find(s=>t>=s.start&&t<s.end);
   if(cap)text(cap.text,960,992,35,'#eff4ec','center');
   text('AI 普惠宣言 · X-lab AI',105,1050,18,'#a9c0af');
   text(`Music: ${music} — Kevin MacLeod (incompetech.com) · excerpt / edit / mix`,1810,1032,16,'#a9c0af','right');
   text('CC BY 4.0 · creativecommons.org/licenses/by/4.0/',1810,1057,16,'#a9c0af','right');
   g.fillStyle='#cce89d';g.fillRect(0,1076,1920*t/25,4);
   if(f===22*30)fs.writeFileSync(path.join(OUT,`audition-${key}.png`),c.toBuffer('image/png'));
   if(!p.stdin.write(c.data()))await once(p.stdin,'drain');
  }
  p.stdin.end();const[code]=await once(p,'close');if(code)throw Error(`ffmpeg exit ${code}`);
  console.log(outfile);
 }
}
main().catch(e=>{console.error(e);process.exit(1)});
