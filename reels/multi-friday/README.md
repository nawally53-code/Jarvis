# Reel Multi Friday — Claro que tem (Grupo Caldas Celulares)

Reel vertical 1080×1920, 30 s, 30 fps → `reel-multi-friday.mp4`. Visual escuro com neon vermelho, seguindo a arte da campanha.

| Tempo | Cena |
|---|---|
| 0–2,8 s | Gancho: "Clientes aproveitando as ofertas imperdíveis de Black Friday" |
| 2,7–5,2 s | Slogan "MULTI Friday · Claro que tem" acendendo em neon |
| 5–25,25 s | 9 fotos de clientes (2,25 s cada) com legenda, contador e barra de progresso |
| 25,25–30 s | Encerramento: logo + slogan + "Venha até uma das nossas lojas e aproveite as ofertas!" |

## Como editar / renderizar
- Textos, legendas e tempos: `index.html` (arrays `HOOK`, `SHOTS` e constantes da timeline).
- Prévia de quadros: `node render.js --preview 1,5,13 <pasta>`
- Render final: `node render.js reel-multi-friday.mp4` (precisa de Playwright + ffmpeg).
- Logo para fundo escuro: `python3 make_logo_white.py assets/logo-caldas.png assets/logo-caldas-branca.png`
