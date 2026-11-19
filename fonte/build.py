#!/usr/bin/env python3
# Monta index.html e assets/deck.css e deck.js a partir de src/. Rodar da raiz: python3 fonte/build.py
import pathlib, time, re
R = pathlib.Path(__file__).resolve().parent.parent
S = R / 'src'
v = time.strftime('%Y%m%d%H%M%S')
(R / 'versao.txt').write_text(v + '\n')
telas = ''.join((S / f).read_text() for f in sorted(p.name for p in S.glob('s[0-9]*.html')))
shell = (S / 'shell.html').read_text()
html = shell.replace('__TELAS__', telas).replace('__VERSAO__', v)
(R / 'index.html').write_text(html)
css = ''.join((S / f).read_text() for f in ['base.css', 'tema.css', 'telas.css', 'celular.css'] if (S / f).exists())
(R / 'assets/deck.css').write_text(css)
(R / 'assets/deck.js').write_text((S / 'deck.js').read_text())
tudo = html + css + (R / 'assets/deck.js').read_text()
bad = [x for x in ('—', '–') if x in tudo]
n = html.count('<section class="tela')
rot = html.count('<aside class="roteiro"')
print('telas', n, '· roteiros', rot, '· versão', v, '· TRAVESSÃO!' if bad else '· sem travessão')
for m in re.finditer(r'(?:a definir|lorem|TBD|XXX|\[__)', html, re.I):
    print('TEXTO PROVISÓRIO:', html[max(0, m.start() - 40):m.end() + 40].replace('\n', ' '))
