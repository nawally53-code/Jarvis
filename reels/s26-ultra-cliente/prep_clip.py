# Builds the edited unboxing clip: removes the part where the customer's face is visible (21.7–23.7 s),
# speeds up the slow unwrapping, then enhances (denoise, Lanczos upscale to 1080x1920, sharpen, colour)
# and exports 30 fps JPEG frames to assets/clip/.
import os, shutil, subprocess
SRC = "assets/videos/unboxing-s26-ultra.mp4"
#          start  end   speed
SEGMENTS = [(0.0,  5.0,  1.4),    # box in hand
            (5.0,  12.0, 2.2),    # removing the seal (sped up)
            (12.0, 21.6, 1.15),   # lid off, phone revealed and lifted
            (23.8, 25.76, 0.8)]   # phone back in the box (hero shot, slightly slowed) — face part skipped
OUT = "assets/clip"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
parts, labels = [], []
for i, (a, b, sp) in enumerate(SEGMENTS):
    parts.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30[s{i}]")
    labels.append(f"[s{i}]")
fc = ";".join(parts) + f";{''.join(labels)}concat=n={len(SEGMENTS)}:v=1:a=0," \
     "hqdn3d=3:2:5:4,scale=1080:1920:flags=lanczos,unsharp=5:5:1.0:5:5:0," \
     "eq=contrast=1.05:brightness=0.025:saturation=1.08[v]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[v]", "-q:v", "3", f"{OUT}/f%04d.jpg"], check=True)
n = len(os.listdir(OUT)); print(n, "frames =", round(n / 30, 2), "s")
# segment boundaries in the edited clip (seconds)
t = 0
for a, b, sp in SEGMENTS:
    t += (b - a) / sp; print(f"  ends at {t:.2f}s")
