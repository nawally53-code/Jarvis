# Reel Dia da Black Friday — 27/11 (Multi Friday · Grupo Caldas Celulares)

Reel vertical 1080×1920, ~26,3 s, 30 fps → `reel-dia-black-friday.mp4`. Estilo de alto impacto: fundo escuro com feixes de luz
vermelha girando e pulsando na batida, faixas "SÓ HOJE · 27/11" correndo no topo e na base, cenas que "batem" na tela no ritmo da trilha (130 BPM). A linha do tempo da tabela está escrita a 120 BPM
e é tocada a 130/120 (`SPEED` no `index.html`), então os tempos reais são ~8% menores.

| Tempo | Cena |
|---|---|
| 0–2 s | Calendário vira de 26 para **27/11** + "CHEGOU O GRANDE DIA!" |
| 2–4 s | Slogan MULTI Friday acende em neon + "Caldas Celulares" |
| 4–6 s | Carimbo "SÓ HOJE! 27 de novembro" |
| 6–9 s | ATÉ 60% OFF de desconto em aparelhos (contador) |
| 9–12 s | Compre um Galaxy A57 e leve outro (*consulte condições) |
| 12–15 s | Brindes exclusivos (caixa de presente abrindo) |
| 15–18 s | ATÉ +50GB de bônus de internet no plano Pós (contador) |
| 18–21,5 s | 3 meses grátis de Amazon Prime + cupom de R$ 30 |
| 21,5–23 s | "E MUITO MAIS!" |
| 23–28,5 s | Logo + slogan + "Corre! Venha até uma de nossas lojas e aproveite só hoje!" |

## Áudio
- Trilha original (sem direitos autorais) no estilo da referência: trap/phonk escuro a 130 BPM, 808 distorcido, caixa no 2 e 4,
  chimbal com viradas e riff de cowbell. O 1º compasso (calendário) é uma subida com virada de caixa acelerando; a batida
  "dropa" quando o slogan Multi Friday acende. → `python3 gen_music_phonk.py`
- Efeitos reduzidos aos mais relevantes: impacto no calendário, neon do slogan, impacto no "SÓ HOJE", "ding" em cada oferta revelada e impacto no final.
- Ordem: `node render.js --events` → `python3 gen_sfx.py` → `python3 gen_music_phonk.py` → `node render.js reel-dia-black-friday.mp4`
  (o áudio final `audio.wav` é normalizado para ~-13 LUFS).
