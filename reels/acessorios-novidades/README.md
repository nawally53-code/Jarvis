# Reel Novidades em Acessórios — DEVIA Sound Lite 3 + Ultra Watch (Grupo Caldas Celulares)

Reel vertical 1080×1920, ~30 s, 30 fps → `reel-acessorios-novidades.mp4`. Layout claro "lançamento de produto",
com os vídeos reais da loja em um card grande, capítulos numerados em tela vermelha e etiquetas de funções.

| Tempo | Cena |
|---|---|
| 0–2,9 s | Gancho: "NOVIDADES EM ACESSÓRIOS" + "Olha o que acabou de chegar nas nossas lojas" + mosaico 2×2 com os 4 vídeos rodando |
| 2,9–3,9 s | Capítulo 01 (tela vermelha): DEVIA Sound Lite 3 · Caixa de som magnética |
| 3,9–12,9 s | Vídeos da Sound Lite 3 (grudando no celular + vitrine) com etiquetas |
| 12,9–13,9 s | Capítulo 02: DEVIA Ultra Watch · Smartwatch |
| 13,9–25,5 s | Unboxing + funções do relógio, etiquetas sincronizadas com cada tela (atividade/freq. cardíaca, sono, música, chamadas) |
| 25,5–30,4 s | Encerramento: logo + "Venha até uma de nossas lojas e confira!" |

## Como editar / renderizar
1. `python3 prep_clips.py` — corta os trechos de `assets/videos/`, melhora (redução de ruído, ampliação Lanczos, nitidez, cor)
   e gera as sequências de quadros em `assets/clips/` (não versionado).
2. Textos, etiquetas e tempos: `HEADLINE`, `TAGS`, `PRODUCTS`, `SCENES` no `index.html`.
3. Sons + música (sintetizados, sem direitos autorais): `node render.js --events` → `python3 gen_sfx.py` → `python3 gen_music.py`.
4. `node render.js reel-acessorios-novidades.mp4`
