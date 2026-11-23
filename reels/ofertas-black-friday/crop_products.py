# Crops product renders out of the reference slides (2x Lanczos upscale for sharper display).
import sys, os
from PIL import Image
R = "assets/referencia/"
CROPS = {
  "edge70.png":    ("compre-leve-outro.jpg", (100, 186, 290, 410)),
  "a57.png":       ("compre-leve-outro.jpg", (96, 484, 292, 708)),
  "iphone16.png":  ("iphone16.jpg",          (270, 232, 590, 612)),
  "s26ultra.png":  ("s26-ultra.jpg",         (255, 238, 605, 588)),
  "g37.png":       ("g37-signature.jpg",     (55, 258, 330, 608)),
  "signature.png": ("g37-signature.jpg",     (695, 256, 985, 608)),
  "tv.png":        ("claro-tv.jpg",          (130, 1590, 1190, 2332)),
  "tvbox.png":     ("claro-tv.jpg",          (452, 712, 656, 796)),
}
for out, (src, box) in CROPS.items():
    im = Image.open(R + src).convert("RGB").crop(box)
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im.save("assets/" + out)
    print(out, im.size)
