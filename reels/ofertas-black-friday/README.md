# Reel Ofertas Black Friday — Multi Friday (Grupo Caldas Celulares)

Reel vertical 1080×1920, 45 s, 30 fps → `reel-ofertas-black-friday.mp4`. Visual escuro com neon vermelho da Multi Friday,
com um cursor de mouse que clica e revela cada novidade.

| Tempo | Cena |
|---|---|
| 0–2,8 s | Gancho em formato de mensagem de chat: "Vamos conferir as nossas ofertas especiais para essa Black Friday?" + botão "Bora conferir!" clicado pelo cursor |
| 2,85–4,9 s | Slogan "MULTI Friday · Claro que tem" acendendo em neon |
| 4,8–10,4 s | Comprou um smartphone, leva outro igual (Moto Edge 70 Fusion ou Galaxy A57) — 12x R$ 173,25 |
| 10,4–15,2 s | iPhone 16 — 12x R$ 173,25 |
| 15,2–20 s | Galaxy S26 Ultra — 12x R$ 155,75 |
| 20–25,6 s | Moto G37 (12x R$ 49,33) e Motorola Signature (12x R$ 85,75) |
| 25,6–30,1 s | Até +50GB de bônus adicional de internet no plano pós |
| 30,1–35,5 s | Claro tv+ — R$ 99,90/mês por 2 meses |
| 35,5–40 s | Cupom Amazon de R$ 30 |
| 40–45 s | Encerramento: logo + slogan + "Venha até uma das nossas lojas e aproveite as ofertas!" |

Parcelas em 12x calculadas a partir do preço total de cada oferta (total ÷ 12), mantendo os totais das artes originais.

## Como editar / renderizar
- Duração de cada slide: atributo `data-dur` de cada `.slide` (a duração total se ajusta sozinha).
- Slides, preços e textos: `index.html` (cada `.slide`; `data-click` = o que o cursor clica, `data-reveal` = o que aparece no clique).
- Prévia de quadros: `node render.js --preview 1,5,13 <pasta>`
- Render final: `node render.js reel-ofertas-black-friday.mp4` (precisa de Playwright + ffmpeg).
- Fotos dos aparelhos: `python3 crop_products.py` (recorta das artes em `assets/referencia/`).
