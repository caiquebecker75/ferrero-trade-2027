import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
const nav=await chromium.launch({channel:'chrome'});const pg=await (await nav.newContext({viewport:{width:390,height:844},isMobile:true})).newPage();
await pg.goto(process.argv[2]||'http://localhost:4783/',{waitUntil:'networkidle'});
console.log(JSON.stringify(await pg.evaluate(()=>{const W=document.documentElement.clientWidth;return [document.documentElement.scrollWidth,[...document.querySelectorAll('.tela *')].filter(e=>e.offsetParent&&!e.closest('.gd-esq')&&e.getBoundingClientRect().right>W+2).slice(0,8).map(e=>e.tagName+'.'+e.className+' '+(e.textContent||'').trim().slice(0,25)+' '+Math.round(e.getBoundingClientRect().right))]})));
await nav.close();
