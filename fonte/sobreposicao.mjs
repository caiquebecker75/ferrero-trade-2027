// Confere texto sobre texto NA APRESENTAÇÃO AO VIVO (não no modo PDF): cada tela depois das animações,
// e cada aba das telas com abas. Inclui topo (Sumário, PDF), contador e fonte.
//   node fonte/sobreposicao.mjs <base> <pasta das fotos>
import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';
const BASE = process.argv[2] || 'http://localhost:4783/'; const OUT = process.argv[3]; if (OUT) mkdirSync(OUT, { recursive: true });
const nav = await chromium.launch({ channel: 'chrome' });
const pg = await nav.newPage({ viewport: { width: 1600, height: 900 } });
pg.on('pageerror', (e) => console.log('ERRO', e.message));
await pg.goto(BASE + '#1', { waitUntil: 'networkidle' }); await pg.evaluate(() => document.fonts.ready);
const total = await pg.evaluate(() => document.querySelectorAll('.tela').length);
const confere = () => pg.evaluate(() => {
  const t = document.querySelector('.tela.ativa'); const st = document.getElementById('stage').getBoundingClientRect();
  const fora = [...document.querySelectorAll('#topoBt a,#topoBt button,#cont')];
  const els = [...t.querySelectorAll('h1,h2,h3,p,li,dd,dt,b,span,q,em,cite,i,button,a,small')]
    .filter((e) => e.offsetParent && e.textContent.trim() && !e.closest('[aria-hidden="true"],.gd-itens,.pontos') && getComputedStyle(e).visibility !== 'hidden' && +getComputedStyle(e).opacity > 0.05)
    .filter((e) => ![...e.children].some((c) => c.textContent.trim() === e.textContent.trim()));
  const todos = [...els, ...fora];
  const R = todos.map((e) => [e, e.getBoundingClientRect()]).filter(([, r]) => r.width > 2 && r.height > 2);
  const out = [];
  for (const [e, r] of R) if (r.right > st.right + 2 || r.bottom > st.bottom + 2 || r.left < st.left - 2 || r.top < st.top - 2) out.push('FORA DA TELA: ' + e.textContent.trim().slice(0, 40));
  for (let i = 0; i < R.length; i++) for (let j = i + 1; j < R.length; j++) {
    const [a, ra] = R[i], [b, rb] = R[j]; if (a.contains(b) || b.contains(a)) continue;
    const ix = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left), iy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
    if (ix > 3 && iy > 3) out.push('SOBRE: "' + a.textContent.trim().slice(0, 28) + '" x "' + b.textContent.trim().slice(0, 28) + '"');
  }
  const tit = [...t.querySelectorAll('h1,h2,h3,p.lead,p.explica')].filter((e) => e.offsetParent);
  const imgs = [...t.querySelectorAll('img')].filter((e) => e.offsetParent && !e.closest('.marcas,.cap-marcas,.capa,.kvf,.meio-b') && e.getBoundingClientRect().width > 50);
  for (const h of tit) for (const im of imgs) { if (h.contains(im) || im.closest('section') !== h.closest('section')) continue;
    const a1 = h.getBoundingClientRect(), b1 = im.getBoundingClientRect();
    const ix = Math.min(a1.right, b1.right) - Math.max(a1.left, b1.left), iy = Math.min(a1.bottom, b1.bottom) - Math.max(a1.top, b1.top);
    if (ix > 6 && iy > 6) out.push('IMAGEM SOBRE TEXTO: "' + h.textContent.trim().slice(0, 30) + '" x ' + (im.alt || im.src.split('/').pop())); }
  return [...new Set(out)].slice(0, 10);
});
let ruins = 0;
for (let n = 1; n <= total; n++) {
  await pg.evaluate((n) => { location.hash = '#' + n; }, n);
  await pg.waitForTimeout(2900);
  const k = await pg.evaluate(() => (window.__pdfEstados ? window.__pdfEstados() : 0));
  const estados = Math.max(1, k);
  for (let e = 0; e < estados; e++) {
    if (k) { await pg.evaluate((e) => window.__pdfEstado(e), e); await pg.waitForTimeout(900); }
    const p = await confere();
    if (p.length) { ruins++; console.log(`tela ${n}${k ? ' aba ' + (e + 1) : ''}: ` + p.join(' | ')); }
    if (OUT && e === 0) await pg.screenshot({ path: `${OUT}/${String(n).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 70 });
  }
}
await nav.close(); console.log(ruins ? `${ruins} estados com problema` : 'nenhum texto sobre texto', '· telas', total);
