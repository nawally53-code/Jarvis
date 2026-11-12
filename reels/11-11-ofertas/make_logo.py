import sys
from PIL import Image
import numpy as np
src = Image.open(sys.argv[1]).convert("RGBA"); flat = Image.new("RGBA", src.size, "white"); flat.alpha_composite(src)
im = np.asarray(flat.convert("RGB")).astype(np.float32)/255
# alpha from "distance from white": darkest channel decides coverage
a = 1 - im.min(axis=2)
a = np.clip((a - 0.06) / 0.80, 0, 1)            # kill off-white noise, keep edges soft
safe = np.maximum(a, 1e-4)[..., None]
rgb = np.clip((im - (1 - safe)) / safe, 0, 1)    # un-blend from white
out = np.dstack([rgb, a])
img = Image.fromarray((out*255).astype(np.uint8), "RGBA")
img = img.crop(img.getbbox())
img.save(sys.argv[2])
# brand red sample
reds = (im[...,0]>0.8)&(im[...,1]<0.15)&(im[...,2]<0.15)
print(img.size, (im[reds].mean(axis=0)*255).round())
