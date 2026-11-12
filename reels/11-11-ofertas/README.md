# Reel 11.11 — Ofertas Imperdíveis (Grupo Caldas Celulares)

Reel vertical 1080×1920, 30 s, 30 fps → `reel-11-11-ofertas.mp4`

| Tempo | Cena |
|---|---|
| 0–2,8 s | Gancho: "Clientes que aproveitaram as ofertas imperdíveis de hoje" |
| 2,6–24,6 s | 8 fotos de clientes (2,75 s cada) com legenda, contador e barra de progresso |
| 24,6–30 s | Encerramento: logo, "Chegou o 11.11 · Dia de Ofertas Imperdíveis!" |

## Como editar / renderizar
- Textos, legendas e tempos: `index.html` (arrays `HOOK`, `SHOTS` e constantes da timeline).
- Prévia de quadros: `node render.js --preview 1,5,13 <pasta>`
- Render final: `node render.js reel-11-11-ofertas.mp4` (precisa de Playwright + ffmpeg).
- Logo transparente: `python3 make_logo.py <logo.png> assets/logo-caldas.png`
