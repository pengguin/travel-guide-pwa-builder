#!/usr/bin/env node
// Isolated, offline rendering of six paired documentation illustrations.
const { chromium } = require('playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const fs = require('node:fs');
const root = path.resolve(__dirname, '..');
const shots = [['01-chat','chat'],['02-home','home'],['03-all-pages','overview'],['04-map','map'],['05-interaction','interaction'],['06-logistics','logistics']];
(async () => {
  const options = {headless:true, timeout:30000};
  if (process.env.CHROME) options.executablePath=process.env.CHROME;
  else if(process.platform==='darwin') options.executablePath='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const browser=await chromium.launch(options), results=[];
  try {
    fs.mkdirSync(path.join(root,'docs/images'),{recursive:true});
    for(const lang of ['en','zh']) for(const [shot,name] of shots){
      const width=name==='overview'?2400:1800, height=name==='overview'?1200:1120;
      const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1.5});
      await page.route(/^https?:/,r=>r.abort());
      const url=pathToFileURL(path.join(root,'docs/artwork/artwork.html'));
      url.search=new URLSearchParams({shot,lang}).toString();
      await page.goto(url.href); await page.evaluate(()=>document.fonts.ready);
      await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
      const check=await page.evaluate(()=>({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,phones:document.querySelectorAll('.device').length,navIcons:document.querySelectorAll('.navitem svg').length,untranslated:window.untranslated||[],contentClearance:[...document.querySelectorAll('.screen')].map(s=>Math.round(s.querySelector('.nav').getBoundingClientRect().top-s.querySelector('.content').lastElementChild.getBoundingClientRect().bottom))}));
      if(check.width!==width||check.height!==height||check.brokenImages||check.untranslated.length||check.contentClearance.some(v=>v<12)||check.navIcons!==check.phones*6) throw new Error(`${name}-${lang}: ${JSON.stringify(check)}`);
      await page.screenshot({path:path.join(root,`docs/images/${name}-${lang}.png`)});
      results.push({name,lang,...check}); console.log(`Rendered ${name}-${lang}; ${check.phones} phones; clearance ${check.contentClearance}`);await page.close();
    }
    fs.writeFileSync(path.join(root,'docs/artwork/render-checks.json'),JSON.stringify(results,null,2)+'\n');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
