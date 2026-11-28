# Cuts the clips used in the reel out of the source videos, improves them (denoise, Lanczos upscale,
# sharpening, a touch of colour/brightness) and exports them as 30 fps JPEG frame sequences in
# assets/clips/<id>/ so the HTML composition can show the exact frame for each moment.
import os, shutil, subprocess

V = "assets/videos/"
#  id      source file                    start  end   speed  size (w x h)
CLIPS = [
  ("fachada", "fachada.mov",          0.4, 3.6, 1.0, (1080, 1920)),
  ("entrada", "entrada-banner.mov",   0.6, 3.0, 1.0, (1080, 1920)),
  ("interna", "loja-interna.mov",    15.4, 17.8, 1.0, (1080, 1920)),
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
