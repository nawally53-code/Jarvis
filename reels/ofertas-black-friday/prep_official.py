# Builds the slide product images from the official transparent renders in assets/oficial/,
# and gives the Motorola crops (no official file available) a cleaner, brighter look.
from PIL import Image, ImageEnhance, ImageFilter
O = "assets/oficial/"

def trim(im):
    return im.crop(im.getbbox())

def fit_h(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

# Galaxy A57: back + front render as published
trim(Image.open(O + "galaxy-a57-samsung.png").convert("RGBA")).save("assets/a57.png")

# Galaxy S26 Ultra: back (with S Pen) + front, overlapped like the campaign art
back = fit_h(trim(Image.open(O + "galaxy-s26-ultra-back-samsung.png").convert("RGBA")), 1200)
front = fit_h(trim(Image.open(O + "galaxy-s26-ultra-front-samsung.png").convert("RGBA")), 1160)
W = back.width + int(front.width * 0.78)
canvas = Image.new("RGBA", (W, 1200), (0, 0, 0, 0))
canvas.alpha_composite(back, (0, 0))
canvas.alpha_composite(front, (W - front.width, 20))
canvas.save("assets/s26ultra.png")

# iPhone 16 (black), back + front
trim(Image.open(O + "iphone-16-apple.png").convert("RGBA")).save("assets/iphone16.png")

# Motorola crops: brighter, sharper (originals come from the reference slides)
for n in ["edge70", "g37", "signature"]:
    im = Image.open(f"assets/{n}.png").convert("RGB")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    im.save(f"assets/{n}-hd.png")
for f in ["a57", "s26ultra", "iphone16"]:
    print(f, Image.open(f"assets/{f}.png").size)
