# Reel Clientes nas Lojas — Black Friday (Multi Friday · Grupo Caldas Celulares)

Reel vertical 1080×1920, ~28,6 s, sem música (só 3 efeitos: impacto na abertura, whoosh antes das fotos, impacto no final).
Layout: fotos e vídeos em tela cheia, trocando por uma faixa vermelha diagonal (traço da logo).

| Tempo | Cena |
|---|---|
| 0–3,2 s | Vídeo da loja decorada com layout de capa (moldura branca, selo MULTI FRIDAY) + "Olha quem / aproveitou / a Black Friday / com a gente!" |
| 3,2–24 s | 13 fotos de clientes (1,6 s cada), sem legendas |
| 24–28,6 s | Logo + slogan + "Ainda dá tempo! Ofertas prorrogadas até hoje. Venha até uma de nossas lojas e aproveite!" |

Editar: ordem das fotos em `assets/originais/` (`python3 enhance_photos.py` → `assets/fotos/`), trechos dos vídeos em `prep_clips.py`.
Render: `python3 prep_clips.py` → `node render.js --events` → `python3 gen_sfx.py` → normalizar `sfx.wav` em `audio.wav` → `node render.js reel-clientes-lojas-black-friday.mp4`.
