import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
import {createCanvas,GlobalFonts} from '@napi-rs/canvas';
const S=path.dirname(fileURLToPath(import.meta.url)),ROOT=path.resolve(S,'../../..'),W=process.env.RELEASE_BUILD||path.resolve(ROOT,'../release-build'),D=W+'/deck';
const source=ROOT+'/site/launch/downloads/AI-for-All-Conference-ZH.pptx';
GlobalFonts.registerFromPath('/root/.local/share/fonts/SourceHanSansSC-Regular.otf','Source Han Sans SC');
const ctx=createCanvas(10,10).getContext('2d');
const mapping=JSON.parse(await fs.readFile(S+'/deck-en.json','utf8'));
for(const [k,v] of Object.entries(mapping)){const nk=k.replaceAll('\n','');if(mapping[nk]===undefined)mapping[nk]=v;}
const notes=JSON.parse(await fs.readFile(S+'/speaker-notes-en.json','utf8'));
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const rows=(await p.inspect({kind:'textbox,notes',maxChars:600000})).ndjson.trim().split('\n').map(JSON.parse);
const fits=[];
for(const row of rows){
 if(row.kind==='notes'){
  const n=p.resolve(row.id);n.text=notes[row.slideIndex]+'\n\nSources\nhttps://www.x-lab.info/ai-for-all/en.html\nhttps://www.x-lab.info/ai-for-all/presentation/assets/SOURCES.md\nhttps://github.com/X-lab2017/ai-for-all\nEdition: 2026-10-09';continue;
 }
 if(row.kind!=='textbox'||!row.text)continue;
 let newText=mapping[row.text];
 if(newText===undefined){if(/[\u4e00-\u9fff]/.test(row.text))throw Error('Missing translation: '+row.text);continue;}
 const sh=p.resolve(row.id),a=row.position,st=row.style||{};
 // The source title is a single line with two colored runs, not a paragraph break.
 if(a.top<210&&a.height<130)newText=newText.replaceAll('\n',' ');
 if(row.slideIndex===0&&row.text==='AI 普惠宣言'&&a.top>200&&a.top<300){
   newText='AI for All Manifesto';sh.position={...a,left:70,top:195,width:960,height:110};
   st.fontSize=70;st.bold=true;
 }
 if(row.slideIndex===0&&['让 AI 用得起，','更用得好。'].includes(row.text))st.fontSize=60;
 if(row.slideIndex===6&&row.text==='成长飞轮')newText='Growth';
 if(row.slideIndex===6&&row.text==='投入飞轮')newText='Resources';
 let size=st.fontSize||24;let pos=sh.position;
 const measure=sz=>{ctx.font=`${st.bold?'bold ':''}${sz}px Source Han Sans SC`;return Math.max(...newText.split('\n').map(t=>ctx.measureText(t).width));};
 while((measure(size)>pos.width-8 || newText.split('\n').length*size*1.2>pos.height)&&size>14)size-=.5;
 sh.text.replace(row.text,newText);
 sh.text.style={typeface:'Source Han Sans SC',fontSize:size,color:st.color,bold:st.bold||false,alignment:st.alignment||'left'};
 if(newText==='Read the contribution guide ↗')sh.text.get(newText).link={uri:'https://github.com/X-lab2017/ai-for-all/blob/main/translations/contributing.en.md',isExternal:true};
 if(newText.startsWith('Join us  '))sh.text.get(newText).link={uri:'https://www.x-lab.info/ai-for-all/launch/',isExternal:true};
 fits.push({slide:row.slideIndex+1,text:newText,size,width:pos.width,height:pos.height});
}
await fs.mkdir(D+'/en',{recursive:true});
for(let i=0;i<p.slides.items.length;i++){
 const b=await p.export({slide:p.slides.items[i],format:'png',scale:1});
 await fs.writeFile(`${D}/en/slide-${i+1}.png`,new Uint8Array(await b.arrayBuffer()));
}
await fs.writeFile(D+'/en/text-fit.json',JSON.stringify(fits,null,2));
const {finalizePresentation}=await import(pathToFileURL('/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs').href);
const cand=D+'/en/candidate.pptx',final=W+'/output/AI-for-All-Conference-EN-release.pptx';
await(await PresentationFile.exportPptx(p)).save(cand);
const result=await finalizePresentation({workspaceDir:W,candidatePath:cand,finalPath:final,
 pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,
 integrityValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_package_integrity.py',
 layoutValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_layout_geometry.py',
 layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-bullet-geometry','--validate-heading-fit'],
 explicitTotalSlideCount:10,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'reference',families:['Source Han Sans SC'],referencePath:source,referenceSha256:createHash('sha256').update(await fs.readFile(source)).digest('hex')},verifyArtifactToolImport:true,
 receiptPath:D+'/en/validation-release.json'});
console.log(JSON.stringify(result));
