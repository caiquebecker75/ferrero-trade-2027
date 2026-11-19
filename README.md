# Ferrero × 75 LAB · Trade 2027 · O PDV inteligente dos tabletes

Proposta proativa da 75 LAB para a Ferrero (contato: Reinaldo Silva), entrega de 20/11/2026: enxoval modular de PDV para a linha de tabletes Ferrero Rocher, com o lançamento Noz-Pecã & Avelã como produto-herói.

- Apresentação: https://projetos.75lab.com.br/ferrero-trade-2027/
- PDF: `ferrero-75lab-trade-2027.pdf` (capa com link e QR, uma página por aba)
- Base: conversa no ChatGPT e o Google Doc "75LAB × Ferrero | Trade 2027, Planejamento estratégico v2.0" (anexo A, roteiro de 14 telas).

## Estrutura (17 telas)
Fio no topo: Objetivo → Por quê → A ideia → Como → Prova.
1 Capa · 2 Quem é a 75 LAB · 3 O objetivo · 4 Por que agora · 5 Insight do consumidor · 6 Momentos de compra ·
7 O problema na loja · 8 A ideia: Experiência em Camadas · 9 O enxoval (abas com as peças 3D) · 10 Modularidade (animação de montagem) ·
11 Clusterização · 12 Códice · 13 Realidade aumentada · 14 Gestão de campo (abas) · 15 Como medimos (abas) · 16 Piloto · 17 Próximo passo.

## Material próprio
- Ilustrações 3D e animação de montagem: geradas no Blender por `fonte/blender/cena.py` (modelagem procedural nossa, tabletes genéricos sem arte oficial nem gramatura). Renders finais: `fonte/blender/renderizar.sh` (Cycles para as imagens, EEVEE para o MP4).
- Telas reais da plataforma Códice (modo campo, mapa da frota) copiadas de `codice-site/public/sistema`.
- Pesquisa de preço e dashboard da tela 14: simulações de tela em HTML, sem dados.
- Realidade aumentada da tela 13: tablete 3D animado em CSS.

## Como editar
- Telas em `src/sNN-*.html`, estilos em `src/base.css`, `src/quem.css`, `src/casa.css` (regras reaproveitadas do deck Bordon), `src/ferrero.css` e `src/celular.css`; navegação em `src/deck.js`.
- Montar: `python3 fonte/build.py` (gera `index.html`, `assets/deck.*`, `versao.txt` e confere travessão e texto provisório).
- Conferências (Playwright de `ariuno-videos`): `node fonte/miniaturas.mjs <base> <pasta>`, `node fonte/sobreposicao.mjs <base> <pasta>`, `node fonte/celular.mjs <base> <saida.jpg>`. A base pode ser o `file://` do `index.html`.
- PDF: `PAGINA=index.html node fonte/gerar-pdf.mjs file:///…/ferrero-trade-2027/ ferrero-75lab-trade-2027.pdf`.
- Teclas: setas navegam, M abre o sumário, N mostra o roteiro de fala.

## Pendências antes de enviar ao cliente
- Trocar as embalagens genéricas pelas oficiais quando a Ferrero mandar arte, SKUs e gramaturas.
- Marcar, tela a tela, o que da plataforma está disponível para demonstração ao vivo.
- Confirmar cargo e alçada do Reinaldo.
