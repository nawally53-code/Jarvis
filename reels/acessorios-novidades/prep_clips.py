# Cuts the clips used in the reel out of the source videos, improves them (denoise, Lanczos upscale,
# sharpening, a touch of colour/brightness) and exports them as 30 fps JPEG frame sequences in
# assets/clips/<id>/ so the HTML composition can show the exact frame for each moment.
import os, shutil, subprocess

V = "assets/videos/"
#  id      source file                    start  end   speed  size (w x h)
CLIPS = [
  ("h1", "ultra-watch-funcoes.mov",       12.8, 15.6, 1.0, (480, 854)),
  ("h2", "sound-lite-celular.mov",         0.4,  3.2, 1.0, (480, 854)),
  ("h3", "ultra-watch-unboxing.mp4",      10.5, 13.3, 1.0, (480, 854)),
  ("h4", "sound-lite-vitrine.mov",         3.0,  5.8, 1.0, (480, 854)),
  ("a1", "sound-lite-celular.mov",         0.4,  6.4, 1.0, (820, 1458)),
  ("a2", "sound-lite-vitrine.mov",         3.5,  6.5, 1.0, (820, 1458)),
  ("b1", "ultra-watch-unboxing.mp4",       9.0, 14.0, 1.4, (820, 1458)),
  ("b2", "ultra-watch-funcoes.mov",        6.5, 17.8, 1.4, (820, 1458)),
]
for cid, src, a, b, speed, (w, h) in CLIPS:
    out = f"assets/clips/{cid}"
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    vf = (f"setpts=(PTS-STARTPTS)/{speed},fps=30,hqdn3d=2:1.5:4:3,"
          f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},"
          f"unsharp=5:5:0.9:5:5:0,eq=contrast=1.04:brightness=0.02:saturation=1.1")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", V + src,
                    "-vf", vf, "-q:v", "3", f"{out}/f%04d.jpg"], check=True)
    print(cid, len(os.listdir(out)), "frames")
