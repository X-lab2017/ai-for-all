// Export the source HTML as portable event PDFs using the installed runtime browser.
const fs=require('fs'),path=require('path');
const {chromium}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'));
const ROOT=path.resolve(__dirname,'../../..'),BASE=process.env.RELEASE_BASE_URL||'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1600,height:1000}});
 for(const lang of ['zh','en']){
   await page.goto(`${BASE}/launch/manifesto-${lang}.html`,{waitUntil:'networkidle'});
   await page.evaluate(()=>document.fonts.ready);
   await page.pdf({path:path.join(ROOT,`site/launch/downloads/AI-for-All-Manifesto-${lang.toUpperCase()}.pdf`),printBackground:true,preferCSSPageSize:true});
 }
 for(const [pageName,file] of [['qr-display','AI-for-All-Launch-QR-Display'],['panoramas','AI-for-All-Panoramas']]){
   await page.goto(`${BASE}/launch/${pageName}.html`,{waitUntil:'networkidle'});
   await page.evaluate(()=>document.fonts.ready);
   await page.addStyleTag({content:'@page { size:1600px 900px; margin:0 }'});
   await page.pdf({path:path.join(ROOT,`site/launch/downloads/${file}.pdf`),printBackground:true,preferCSSPageSize:true});
 }
 await browser.close();console.log('Exported four publication PDFs.');
})().catch(e=>{console.error(e);process.exit(1)});
