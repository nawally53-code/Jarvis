# Reel Clientes Black Friday — "A Black Friday lotou nossas lojas!" (Grupo Caldas Celulares)

Reel vertical 1080×1920, ~32 s, 30 fps → `reel-clientes-black-friday.mp4`.

| Tempo | Cena |
|---|---|
| 0–3 s | Gancho estilo manchete: selo "ONTEM NAS NOSSAS LOJAS", "A Black Friday **lotou** nossas lojas!" (marca-texto vermelho), foto da loja cheia, "Olha só quem aproveitou ↓" |
| 3–27,7 s | 7 slides com 2 fotos polaroid cada + 1 slide com foto larga — as fotos caem na tela e "revelam" como foto instantânea |
| 27,7–32,5 s | Encerramento: logo + slogan Multi Friday + "Venha até uma das nossas lojas e aproveite as ofertas!" |

## Como editar / renderizar
- Fotos, ordem e legendas: array `SLIDES` em `index.html` (`cap` = legenda, `pos` = enquadramento da foto).
- Melhoria das fotos: `python3 enhance_photos.py` (originais em `assets/originais/` → `assets/fotos/`): redução de ruído,
  equilíbrio de luz (CLAHE), clareamento das fotos escuras, cor e nitidez, ampliação das fotos pequenas. Requer `opencv-python-headless`.
- Sons (sintetizados, sem áudio de terceiros): `node render.js --events` → `python3 gen_sfx.py` → `node render.js reel-clientes-black-friday.mp4`.
- Prévia de quadros: `node render.js --preview 1,5,13 <pasta>`
