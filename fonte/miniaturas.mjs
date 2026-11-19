// Fotografa cada tela (modo pdf, estado final) e checa texto sobreposto e texto saindo da tela.
//   node fonte/miniaturas.mjs <base> <pasta> [telas separadas por vírgula]
import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';
const BASE = process.argv[2] || 'http://localhost:4783/'; const OUT = process.argv[3]; const SO = (process.argv[4]||'').split(',').filter(Boolean).map(Number);
mkdirSync(OUT, { recursive: true });
const nav = await chromium.launch({ channel: 'chrome' });
const pg = await nav.newPage({ viewport: { width: 1600, height: 900 } });
pg.on('pageerror', e => console.log('ERRO', e.message));
await pg.goto(BASE + '?pdf=1#1', { waitUntil: 'networkidle' }); await pg.evaluate(() => document.fonts.ready);
const total = await pg.evaluate(() => document.querySelectorAll('.tela').length);
for (let n = 1; n <= total; n++) {
  if (SO.length && !SO.includes(n)) continue;
  await pg.evaluate(n => { location.hash = '#' + n; }, n); await pg.waitForTimeout(450);
  const prob = await pg.evaluate(() => {
    const t = document.querySelector('.tela.ativa'); const out = [];
    const els = [...t.querySelectorAll('h1,h2,h3,p,li,dd,dt,b,span,.mono,.eyebrow')].filter(e => e.offsetParent && e.childElementCount === 0 && e.textContent.trim());
    const st = document.getElementById('stage').getBoundingClientRect();
    const R = els.map(e => [e, e.getBoundingClientRect()]);
    for (const [e, r] of R) { if (r.right > st.right + 1 || r.bottom > st.bottom + 1 || r.left < st.left - 1) out.push('FORA: ' + e.textContent.trim().slice(0, 40)); }
    for (let i = 0; i < R.length; i++) for (let j = i + 1; j < R.length; j++) {
      const [a, ra] = R[i], [b, rb] = R[j]; if (a.contains(b) || b.contains(a)) continue;
      const ix = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left), iy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
      if (ix > 4 && iy > 4) out.push('SOBRE: "' + a.textContent.trim().slice(0, 30) + '" x "' + b.textContent.trim().slice(0, 30) + '"');
    }
    return out.slice(0, 8);
  });
  if (prob.length) console.log('tela', n, prob.join(' | '));
  await pg.screenshot({ path: `${OUT}/${String(n).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 70 });
}
await nav.close(); console.log('ok', total);
