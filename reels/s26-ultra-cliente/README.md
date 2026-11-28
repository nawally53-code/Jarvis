# Reel Galaxy S26 Ultra 256GB — unboxing de cliente (Grupo Caldas Celulares)

Reel vertical 1080×1920, ~22 s, sem música (3 sons discretos). O trecho em que o rosto do cliente aparece
(21,7–23,7 s do vídeo original) foi removido; a parte de tirar o lacre foi acelerada.

| Tempo | Cena |
|---|---|
| 0–2,9 s | "UNBOXING NA LOJA" + "Mais um cliente saiu de Galaxy S26 Ultra" |
| 2,9–15,1 s | Unboxing com cartão "Samsung Galaxy S26 Ultra · 256GB"; etiquetas 256GB, Câmera de 200MP, S Pen integrada |
| 15,1–17,5 s | Aparelho na caixa + "Samsung Galaxy S26 Ultra 256GB" grande |
| 17,5–21,9 s | Logo + "Venha até uma de nossas lojas e garanta o seu!" |

Edição do vídeo: `python3 prep_clip.py` (cortes, velocidades e melhoria de imagem) → `assets/clip/`.
Render: `node render.js --events` → `python3 gen_sfx.py` → normalizar `sfx.wav` em `audio.wav` → `node render.js reel-s26-ultra-cliente.mp4`.
