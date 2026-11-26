# Reel Novidades em Acessórios — DEVIA Sound Lite 3 + Ultra Watch (Grupo Caldas Celulares)

Reel vertical 1080×1920, ~28 s, 30 fps → `reel-acessorios-novidades.mp4`. Layout claro e clean,
com os vídeos reais da loja em um card grande e etiquetas de funções sincronizadas.

| Tempo | Cena |
|---|---|
| 0–2,6 s | Gancho: "Novidades em acessórios" |
| 2,9–11,9 s | DEVIA Sound Lite 3 (grudando no celular + vitrine) com etiquetas |
| 11,9 s | Troca suave para o segundo produto |
| 11,9–23,5 s | DEVIA Ultra Watch: unboxing + funções (atividade/freq. cardíaca, sono, música, chamadas) |
| 23,5–28,4 s | Encerramento: logo + "Venha até uma de nossas lojas e confira!" |

## Como editar / renderizar
1. `python3 prep_clips.py` — corta os trechos de `assets/videos/`, melhora (redução de ruído, ampliação Lanczos, nitidez, cor)
   e gera as sequências de quadros em `assets/clips/` (não versionado).
2. Textos, etiquetas e tempos: `TAGS`, `PRODUCTS`, `SCENES`, `SWITCH` no `index.html`.
3. Sons + música (sintetizados, sem direitos autorais): `node render.js --events` → `python3 gen_sfx.py` → `python3 gen_music.py`.
4. `node render.js reel-acessorios-novidades.mp4`
