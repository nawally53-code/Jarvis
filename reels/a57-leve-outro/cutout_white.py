# Cuts the white Galaxy A57 out of its white background: flood-fill the background from the
# image border (stops at the phone's grey frame), clean the mask, feather the edge.
import sys
import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
img = cv2.imread(src)
h, w = img.shape[:2]
pad = 10                                              # white border so the fill can go all around
im = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
H, W = im.shape[:2]
mask = np.zeros((H + 2, W + 2), np.uint8)
flags = 4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
cv2.floodFill(im, mask, (0, 0), (0, 0, 0), (9, 9, 9), (9, 9, 9), flags)
bg = mask[1:-1, 1:-1][pad:-pad, pad:-pad] > 0
fg = (~bg).astype(np.uint8) * 255
# keep the largest blob (the phone), fill holes, smooth the edge
n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
fg = np.where(lab == big, 255, 0).astype(np.uint8)
cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
fg = np.zeros_like(fg); cv2.drawContours(fg, cnts, -1, 255, -1)
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
alpha = cv2.GaussianBlur(fg, (0, 0), 1.2)
x, y, bw, bh = cv2.boundingRect(fg)
out = np.dstack([img, alpha])[y:y + bh, x:x + bw]
s = 1500 / bh                                         # upscale to ~1500 px tall
if s > 1:
    out = cv2.resize(out, None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)
    rgb = out[..., :3]
    blur = cv2.GaussianBlur(rgb, (0, 0), 1.4)
    out[..., :3] = cv2.addWeighted(rgb, 1.4, blur, -0.4, 0)
cv2.imwrite(dst, out)
print(src, (w, h), "->", out.shape[1], "x", out.shape[0])
