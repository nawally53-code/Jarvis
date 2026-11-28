# Makes a dark-background version of the transparent logo: neutral black parts -> white.
import sys
import numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert("RGBA")).astype(np.int16)
rgb = a[..., :3]
neutral = (rgb.max(axis=2) - rgb.min(axis=2) < 70) & (rgb.max(axis=2) < 140)
a[neutral, :3] = 255
Image.fromarray(a.astype(np.uint8), "RGBA").save(sys.argv[2])
