# Reel Galaxy A57 — Comprou um, leva outro igual (Multi Friday · Grupo Caldas Celulares)

Reel vertical 1080×1920, ~21 s, 30 fps → `reel-a57-leve-outro.mp4`.

| Tempo | Cena |
|---|---|
| 0–2,6 s | Gancho: "COMPROU 1… LEVA 2!" (tipografia de impacto com tremor) + "Samsung Galaxy A57 na Multi Friday" |
| 2,6–6,6 s | Galaxy A57 (imagem oficial Samsung) sobe no pódio de luz vermelha |
| 6,6–10,6 s | "Comprou um, leva outro igual!" — segundo aparelho entra com "Compre" + "Leve outro igual" |
| 10,6–16,3 s | 12x R$ 256,58 sem juros (números giram tipo caça-níquel) · Total R$ 3.079 · No Claro Multi 200GB + 50GB |
| 16,3–21,2 s | Encerramento: logo + slogan Multi Friday + "Venha até uma das nossas lojas e aproveite as ofertas!" |

Parcela: R$ 3.079 ÷ 12 = R$ 256,58. Valor da parcela em `PRICE_INT` e `#cents` no `index.html`.

Sons (sintetizados): `node render.js --events` → `python3 gen_sfx.py` → `node render.js reel-a57-leve-outro.mp4`.
