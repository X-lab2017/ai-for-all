/* Export only approved graphics and current presentation slide 12. */
const path=require('path'),fs=require('fs');
const modules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const sharp=require(modules?path.join(modules,'sharp'):'sharp');
const {chromium}=require(modules?path.join(modules,'playwright'):'playwright');
const root=path.resolve(__dirname,'..'), out=path.join(root,'site/launch/assets');
(async()=>{
 await sharp(path.join(out,'manifesto-qr.svg')).resize(1024,1024).png().toFile(path.join(out,'manifesto-qr.png'));
 // The wide approved cover is contained within the social preview, without cropping.
 const wide=fs.readFileSync(path.join(out,'cover-wide.svg')).toString('base64');
 fs.writeFileSync(path.join(out,'social-preview.svg'),`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#143b30"/><image x="0" y="62" width="1200" height="507" href="data:image/svg+xml;base64,${wide}"/></svg>`);
 await sharp(path.join(out,'social-preview.svg')).png().toFile(path.join(out,'social-preview.png'));
 const b=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 const p=await b.newPage({viewport:{width:1920,height:1180},deviceScaleFactor:1});
 await p.goto('file://'+root+'/site/presentation/index.html?lang=zh#s12');
 await p.waitForSelector('#s12:not([hidden])');
 await p.evaluate(()=>{localStorage.setItem('aifa-deck-theme','dark')});await p.reload();await p.waitForSelector('#s12:not([hidden])');
 await p.addStyleTag({content:'*{animation:none!important;transition:none!important}.stage{width:1920px!important;height:1080px!important;max-width:none!important;max-height:none!important;margin:0!important}.stage .primary-nav,.stage .nav-utilities{visibility:hidden!important}body{padding:0!important}'});
 await p.evaluate(()=>document.fonts.ready);
 await p.locator('.stage').screenshot({path:path.join(out,'panorama.png')});
 await b.close();
})();
