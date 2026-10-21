# Mockups only: README / social-preview cover art from the game's own graphics.
import random
from PIL import Image, ImageDraw
rgb = lambda r, g, b: (r * 255 // 31, g * 255 // 31, b * 255 // 31)
LOGO = [rgb(31, 29, 31), rgb(30, 30, 17), rgb(18, 18, 24), rgb(7, 7, 16)]   # PAL_LOGO2
CYAN = [rgb(31, 29, 31), rgb(21, 25, 29), rgb(14, 19, 25), rgb(3, 2, 2)]    # PAL_CYANMON
PINK = [rgb(31, 29, 31), rgb(30, 22, 24), rgb(28, 15, 21), rgb(3, 2, 2)]    # PAL_PINKMON
VER = rgb(14, 19, 29)
SHADES = {255: 0, 170: 1, 85: 2, 0: 3}
def colour(path, pal, scale, transparent_white=True):
    g = Image.open(path).convert("L")
    out = Image.new("RGBA", g.size)
    out.putdata([(0, 0, 0, 0) if (v == 255 and transparent_white) else pal[SHADES[v]] + (255,) for v in g.get_flattened_data()])
    return out.resize((g.width * scale, g.height * scale), Image.NEAREST)
def lettering(scale):
    g = Image.open("gfx/title/blue_version.png").convert("L")
    out = Image.new("RGBA", g.size)
    out.putdata([VER + (255,) if v < 128 else (0, 0, 0, 0) for v in g.get_flattened_data()])
    return out.resize((g.width * scale, g.height * scale), Image.NEAREST)
def gradient(w, h, top, bottom):
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return im
def snowflakes(im, n, seed, col=(255, 255, 255)):
    rng = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y, s = rng.randrange(im.width), rng.randrange(im.height), rng.choice((4, 4, 8))
        d.rectangle([x, y, x + s - 1, y + s - 1], fill=col)
        if s == 8:
            for dx, dy in ((-8, 0), (8, 0), (0, -8), (0, 8)):
                d.rectangle([x + dx + 2, y + dy + 2, x + dx + 5, y + dy + 5], fill=col)
    return im
W, H = 1280, 640
# A. box art: logo, lettering, one big Snom, snow
a = snowflakes(gradient(W, H, (196, 222, 246), (246, 250, 255)), 70, 1)
logo = colour("gfx/title/pokemon_logo.png", LOGO, 4)
a.paste(logo, (90, 70), logo)
let = lettering(4); a.paste(let, (90 + (logo.width - let.width) // 2, 70 + logo.height + 24), let)
snom = colour("art/snom_front.png", CYAN, 9); a.paste(snom, (W - snom.width - 70, H - snom.height - 10), snom)
a.save("art/cover/mockup_A_box.png")
# B. the real title screen (colour capture), framed
b = gradient(W, H, (40, 60, 120), (20, 30, 70))
shot = Image.open("art/cover/title_capture.png").convert("RGB")   # 480x432 capture of the SGB title
shot = shot.resize((shot.width * 13 // 10, shot.height * 13 // 10), Image.NEAREST)
d = ImageDraw.Draw(b)
x0, y0 = (W - shot.width) // 2, (H - shot.height) // 2
d.rectangle([x0 - 16, y0 - 16, x0 + shot.width + 15, y0 + shot.height + 15], fill=(88, 140, 220))
b.paste(shot, (x0, y0)); snowflakes(b, 60, 2, (180, 210, 255)); b.paste(shot, (x0, y0))
b.save("art/cover/mockup_B_title.png")
# C. the Snom parade: logo + lettering, the seven title poses in a row, ???? hiding at the end
c = snowflakes(gradient(W, H, (210, 230, 250), (250, 252, 255)), 50, 3)
logo3 = colour("gfx/title/pokemon_logo.png", LOGO, 3)
c.paste(logo3, ((W - logo3.width) // 2, 30), logo3)
let3 = lettering(3); c.paste(let3, ((W - let3.width) // 2, 30 + logo3.height + 14), let3)
poses = ["normal", "hop", "blink", "happy", "look_back", "sleepy", "surprised"]
x = 40
for i, p in enumerate(poses):
    im = colour(f"gfx/pokemon/front/snom_pose_{p}.png", CYAN, 4)
    c.paste(im, (x, H - im.height - 40), im); x += im.width + 10
mystery = colour("gfx/pokemon/front/starsnom.png", PINK, 2)
c.paste(mystery, (W - mystery.width - 20, 24), mystery)
c.save("art/cover/mockup_C_parade.png")
print("ok")
