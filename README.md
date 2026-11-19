# Ferrero × 75 LAB · Ferrero Rocher · Trade 2027

Proposta proativa da 75 LAB para a Ferrero (contato: Reinaldo Silva), entrega de 20/11/2026: o PDV inteligente de Ferrero Rocher, com enxoval modular, Códice, realidade aumentada, gestão de campo e piloto mensurável.

- Apresentação: https://projetos.75lab.com.br/ferrero-trade-2027/
- PDF: `ferrero-75lab-trade-2027.pdf` (capa com link e QR, uma página por aba)
- Base: conversa no ChatGPT e o Google Doc "75LAB × Ferrero | Trade 2027, Planejamento estratégico v2.0".

## Linguagem visual (v2)
Identidade Ferrero Rocher sobre o motor 75 LAB: folha dourada com brilho em loop, chocolate, creme, Playfair Display nos títulos, Jost no texto, Space Mono nos rótulos. Elementos de marca desenhados por nós em SVG: o bombom dourado com medalhão oval, a forminha plissada (roseta girando), avelãs flutuando e brilhos. Cortina de transição dourada com o bombom e as duas marcas; entrada com foco, saída com subida.

## Espaços reservados para a equipe de design
Salve o arquivo em `assets/slots/` com o nome abaixo (`.webp`, `.png`, `.jpg` ou `.svg`; vídeo em `.mp4`). Ele aparece sozinho no lugar reservado, sem mexer no HTML. Rode `python3 fonte/build.py` só se mudar o código.

| Nome do arquivo | Onde aparece | Tamanho sugerido |
|---|---|---|
| `logo-ferrero` | topo das telas claras e douradas | altura 76 px, PNG/SVG sem fundo |
| `logo-ferrero-claro` | topo das telas escuras | idem, versão clara |
| `kv-capa` | capa, círculo central | 1240 × 1240 px (recorte circular) |
| `foto-momento` | tela 5, insight (recorte em arco) | 920 × 1120 px |
| `render-display-chao` | tela 9, enxoval | 1200 × 1520 px, PNG sem fundo |
| `render-ponta-gondola` | tela 9 | idem |
| `render-display-balcao` | tela 9 | idem |
| `render-ilha` | tela 9 | idem |
| `animacao-montagem` | tela 10, modularidade | MP4 16:9, 1360 × 764, loop, sem som |

Referências 3D feitas no Blender pela 75 LAB (primeira versão): `assets/referencia/` e `fonte/blender/cena.py`.

## Estrutura (17 telas)
Fio no topo: Objetivo → Por quê → A ideia → Como → Prova.
1 Capa · 2 Quem é a 75 LAB · 3 O objetivo · 4 Por que agora · 5 Insight · 6 Momentos de compra · 7 O problema na loja ·
8 Experiência em Camadas · 9 O enxoval · 10 Modularidade · 11 Clusterização · 12 Códice · 13 Realidade aumentada ·
14 Gestão de campo (abas) · 15 Como medimos · 16 Piloto · 17 Próximo passo.

## Como editar
- Telas em `src/sNN-*.html`; estilos em `src/base.css` (motor), `src/tema.css` (identidade), `src/telas.css` (infográficos) e `src/celular.css`; navegação e espaços reservados em `src/deck.js`. A primeira versão está em `src/casa.css`, `src/quem.css` e `src/ferrero.css` (fora do build).
- Montar: `python3 fonte/build.py` (gera `index.html`, `assets/deck.*`, `versao.txt` e confere travessão e texto provisório).
- Conferências (Playwright de `ariuno-videos`, base `file://…/index.html`): `node fonte/miniaturas.mjs`, `node fonte/sobreposicao.mjs`, `node fonte/celular.mjs`.
- PDF: `PAGINA=index.html node fonte/gerar-pdf.mjs file:///…/ferrero-trade-2027/ ferrero-75lab-trade-2027.pdf`.
- Teclas: setas navegam, M abre o sumário, N mostra o roteiro de fala (o texto detalhado de cada tela está no roteiro).

## Pendências antes de enviar ao cliente
- Preencher os espaços do design (logos, KV, foto, renders e animação) com SKUs e embalagens oficiais.
- Marcar o que da plataforma está disponível para demonstração ao vivo.
- Confirmar cargo e alçada do Reinaldo.
