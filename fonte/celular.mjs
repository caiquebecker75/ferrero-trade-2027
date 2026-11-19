// Confere o celular: rolagem lateral, elemento fora da tela, corpo abaixo de 14 px. node fonte/celular.mjs <base> <saida.jpg>
import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
const nav = await chromium.launch({ channel: 'chrome' });
for (const [w,h] of [[390,844],[430,932]]) {
  const ctx = await nav.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const pg = await ctx.newPage(); pg.on('pageerror', e => console.log('ERRO', e.message));
  await pg.goto(process.argv[2], { waitUntil: 'networkidle' }); await pg.waitForTimeout(800);
  const r = await pg.evaluate(() => {
    const W = document.documentElement.clientWidth, out = [];
    if (document.documentElement.scrollWidth > W + 1) out.push('ROLAGEM LATERAL ' + document.documentElement.scrollWidth);
    for (const e of document.querySelectorAll('.tela *')) {
      if (!e.offsetParent || e.closest('.gd-esq')) continue; const b = e.getBoundingClientRect();
      if (b.width && (b.right > W + 2 || b.left < -2)) { out.push('FORA ' + e.tagName + '.' + e.className + ' ' + Math.round(b.right)); }
      if (e.childElementCount === 0 && e.textContent.trim().length > 20 && !e.closest('.fonte,.mono,.eyebrow')) { const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 14) out.push('PEQUENO ' + fs + ' ' + e.textContent.trim().slice(0, 30)); }
    }
    return { cel: document.documentElement.classList.contains('cel'), h: document.body.scrollHeight, out: [...new Set(out)].slice(0, 25) };
  });
  console.log(w, JSON.stringify(r));
  if (w === 390) await pg.screenshot({ path: process.argv[3], fullPage: false });
  await ctx.close();
}
await nav.close();
