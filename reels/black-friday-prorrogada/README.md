# Reel Black Friday Prorrogada — 28/11 (continuação do reel de 27/11 · Grupo Caldas Celulares)

Mesma identidade do reel `dia-black-friday`, ~28 s. Gancho mais lento (0,7x) com a frase "PRORROGAMOS A BLACK FRIDAY!" parada ~1,5 s; depois o vídeo segue no ritmo de 130 BPM (`timeline`/`realOf` no `index.html`; a música tem 2 compassos de subida). Duas versões:
- `reel-black-friday-prorrogada-so-efeitos.mp4` — só os impactos (sem música), para colocar a música direto no Instagram.
  (A versão com trilha pode ser gerada com `python3 gen_music_house.py` + `node render.js <saida>.mp4`.)

| Cena | Conteúdo |
|---|---|
| Gancho | Calendário vira de 27 para **28/11 (sábado)**, carimbo "PRORROGADO" + "PRORROGAMOS A BLACK FRIDAY!" |
| Slogan | MULTI Friday · Claro que tem + "Mais uma chance para você aproveitar!" |
| Carimbo | "ÚLTIMA CHANCE! Só até hoje, 28/11" |
| Ofertas | Até 60% OFF · Compre um Galaxy A57 e leve outro* · Brindes exclusivos · Até +50GB no Pós · 3 meses de Amazon Prime + cupom R$ 30 · E muito mais! |
| Final | Logo + slogan + "Última chance! Venha até uma de nossas lojas e aproveite!" |

Faixas: "PRORROGADO ✦ ATÉ HOJE 28/11 ✦ ÚLTIMA CHANCE ✦ MULTI FRIDAY".

Áudio: `node render.js --events` → `python3 gen_sfx.py` → `python3 gen_music_house.py` → `node render.js reel-black-friday-prorrogada.mp4`.
