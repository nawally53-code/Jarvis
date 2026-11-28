# Improves the customer photos for the reel: light denoise, local-contrast (CLAHE) exposure balance,
# gentle brightness lift on dark shots, a touch of colour, sharpening, and upscaling small photos.
import glob, os
import cv2
import numpy as np
from PIL import Image, ImageOps

SRC, DST = "assets/originais", "assets/fotos"
os.makedirs(DST, exist_ok=True)
MIN_SIDE = 1500          # shortest side after upscaling

for path in sorted(glob.glob(f"{SRC}/*.jpg")):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    img = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

    # upscale small photos first (Lanczos), so later filters work at the final resolution
    s = MIN_SIDE / min(img.shape[:2])
    if s > 1:
        img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)

    img = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)
    L = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8)).apply(L)
    mean = L.mean() / 255
    if mean < 0.53:                                   # lift darker photos toward a bright, pleasant mid-tone
        gamma = np.log(0.54) / np.log(max(mean, 0.05))
        L = np.clip(255 * (L / 255) ** gamma, 0, 255).astype(np.uint8)
    img = cv2.cvtColor(cv2.merge([L, A, B]), cv2.COLOR_LAB2BGR)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.08, 0, 255)  # a little more colour
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    blur = cv2.GaussianBlur(img, (0, 0), 1.6)         # unsharp mask
    img = cv2.addWeighted(img, 1.55, blur, -0.55, 0)

    out = os.path.join(DST, os.path.basename(path))
    cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print(os.path.basename(path), img.shape[1], "x", img.shape[0], f"L {mean:.2f}->{cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).mean()/255:.2f}")
