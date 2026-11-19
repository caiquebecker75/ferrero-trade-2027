#!/bin/bash
# Renders finais das ilustrações 3D e da animação de montagem (rodar da raiz do projeto).
B=/Applications/Blender.app/Contents/MacOS/Blender
cd "$(dirname "$0")/../.."
for m in chao ponta balcao ilha; do $B -b -P fonte/blender/cena.py -- $m assets/3d/$m.png 160 >/dev/null 2>&1; echo "ok $m"; done
$B -b -P fonte/blender/cena.py -- familia assets/3d/familia.png 128 >/dev/null 2>&1; echo "ok familia"
$B -b -P fonte/blender/cena.py -- montagem "$PWD/assets/video/montagem.mp4" >/tmp/claude-501/fr/montagem.log 2>&1; echo "ok montagem"
ls -la assets/3d assets/video
