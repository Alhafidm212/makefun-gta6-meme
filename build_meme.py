#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme picture (make.fun bounty).

Original art, drawn from scratch with Pillow (stdlib + Pillow only, no
downloaded images, no network, no clock, no randomness beyond a fixed
seed): a Vice City sunset, a gravestone for the dead meme format
"'we got ___ before GTA 6'" (2013-2026), and make.fun's white ghost
mascot with sparkle eyes and a magenta star, paying its respects.

The joke: after 13 years of waiting, GTA 6 finally launched on
19 Nov 2026 -- so the internet's longest-running meme format died
the same day the game came out. The make.fun ghost, being a ghost,
is the perfect mourner.

Output: meme.png, 1200x1200, deterministic (same bytes every run).
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1200
OUT = "meme.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SKY_TOP = (27, 16, 53)
SKY_MID = (107, 45, 143)
SKY_LOW = (214, 51, 132)
HORIZON = (255, 123, 61)
SUN = (255, 214, 110)
GROUND = (20, 8, 42)
SILHOUETTE = (24, 10, 48)
STONE = (232, 232, 238)
STONE_EDGE = (120, 120, 140)
GHOST = (255, 255, 255)
MAGENTA = (233, 30, 99)

rng = random.Random(20261119)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(draw):
    """Vice City sunset: indigo -> purple -> magenta -> orange."""
    stops = [(0.0, SKY_TOP), (0.35, SKY_MID), (0.62, SKY_LOW), (0.78, HORIZON)]
    for y in range(800):
        t = y / 800
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                col = lerp(c0, c1, (t - t0) / (t1 - t0))
                break
        else:
            col = HORIZON
        draw.line([(0, y), (W, y)], fill=col)


def sun(draw):
    """Retro striped sun low on the horizon."""
    cx, cy, r = 600, 640, 190
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN)
    # Horizontal slits across the lower half (sky colour).
    y = cy + 10
    gap = 7
    while y < cy + r:
        draw.rectangle([cx - r, y, cx + r, y + gap], fill=lerp(SKY_LOW, HORIZON, 0.5))
        y += gap + 16
        gap += 5


def skyline(draw):
    """Dark building silhouettes with a few lit windows."""
    x = -20
    while x < W + 20:
        bw = rng.randint(70, 150)
        bh = rng.randint(90, 260)
        top = 800 - bh
        draw.rectangle([x, top, x + bw, 800], fill=SILHOUETTE)
        # Antenna on some buildings.
        if rng.random() < 0.4:
            draw.line([x + bw // 2, top, x + bw // 2, top - 34], fill=SILHOUETTE, width=5)
            draw.ellipse([x + bw // 2 - 4, top - 42, x + bw // 2 + 4, top - 34], fill=(255, 80, 80))
        # Lit windows.
        for _ in range(rng.randint(4, 12)):
            wx = x + rng.randint(8, max(9, bw - 14))
            wy = top + rng.randint(12, max(13, bh - 16))
            draw.rectangle([wx, wy, wx + 7, wy + 9], fill=(255, 205, 90))
        x += bw + rng.randint(4, 26)


def palm(draw, bx, by, height, lean, flip=False):
    """One palm-tree silhouette. (bx, by) = base, height in px."""
    s = -1 if flip else 1
    # Trunk: a slightly curved thick line.
    pts = []
    for i in range(21):
        t = i / 20
        px = bx + s * lean * t * t * height * 0.35
        py = by - t * height
        pts.append((px, py))
    draw.line(pts, fill=SILHOUETTE, width=20, joint="curve")
    tx, ty = pts[-1]
    # Fronds: arcs drooping from the crown.
    for ang in range(-160, 161, 40):
        rad = math.radians(ang)
        length = height * 0.55
        ex = tx + s * math.cos(rad) * length
        ey = ty + abs(math.sin(rad)) * length * 0.55 - 14
        midx = tx + s * math.cos(rad) * length * 0.5
        midy = ty - 26
        arc = []
        for i in range(11):
            t = i / 10
            qx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * midx + t * t * ex
            qy = (1 - t) ** 2 * ty + 2 * (1 - t) * t * midy + t * t * ey
            arc.append((qx, qy))
        draw.line(arc, fill=SILHOUETTE, width=9, joint="curve")
    # Coconuts.
    draw.ellipse([tx - 12, ty - 4, tx + 2, ty + 10], fill=SILHOUETTE)
    draw.ellipse([tx + 2, ty - 2, tx + 14, ty + 12], fill=SILHOUETTE)


def sparkle(draw, cx, cy, r, fill):
    """Four-point star (the ghost's sparkle eyes)."""
    pts = [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
           (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
           (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
           (cx - r * 0.28, cy - r * 0.28)]
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill, rot=-90):
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def ghost(draw, cx, top, scale):
    """make.fun's white ghost: sheet body, wavy hem, sparkle eyes,
    small smile, magenta star coin floating by its side."""
    w = int(150 * scale)
    h = int(210 * scale)
    x0, y0 = cx - w // 2, top
    # Body: top semicircle + straight sides + wavy hem.
    body = []
    for i in range(31):  # dome, left to right
        ang = math.pi + i * math.pi / 30
        body.append((cx + (w // 2) * math.cos(ang), y0 + (w // 2) + (w // 2) * math.sin(ang)))
    # Right side down to the hem.
    body.append((cx + w // 2, y0 + h - 18 * scale))
    # Wavy hem: three bumps, right to left.
    for k in range(3):
        bx = cx + w // 2 - k * (w // 3)
        body.append((bx - (w // 6), y0 + h))
        body.append((bx - (w // 3), y0 + h - 18 * scale))
    body.append((cx - w // 2, y0 + h - 18 * scale))
    draw.polygon(body, fill=GHOST, outline=(200, 200, 210))
    # Sparkle eyes.
    ey = y0 + int(78 * scale)
    sparkle(draw, cx - int(32 * scale), ey, int(16 * scale), (20, 20, 30))
    sparkle(draw, cx + int(32 * scale), ey, int(16 * scale), (20, 20, 30))
    # Smile.
    draw.arc([cx - int(22 * scale), ey + int(18 * scale),
              cx + int(22 * scale), ey + int(46 * scale)],
             start=15, end=165, fill=(20, 20, 30), width=4)
    # Magenta star coin floating by the ghost's right side.
    star5(draw, cx + int(118 * scale), y0 + int(42 * scale), int(26 * scale), MAGENTA)


def gravestone(draw, cx, base_y):
    """Grey rounded-top gravestone with the epitaph."""
    w, h = 470, 380
    x0 = cx - w // 2
    y0 = base_y - h
    # Slab: filled rectangle + filled dome, then outline only the outer edge
    # (a pieslice outline would draw a chord straight across the stone).
    draw.rectangle([x0, y0 + w // 2, x0 + w, base_y], fill=STONE)
    draw.pieslice([x0, y0, x0 + w, y0 + w], start=180, end=360, fill=STONE)
    draw.arc([x0, y0, x0 + w, y0 + w], start=180, end=360, fill=STONE_EDGE, width=4)
    draw.line([x0, y0 + w // 2, x0, base_y], fill=STONE_EDGE, width=4)
    draw.line([x0 + w, y0 + w // 2, x0 + w, base_y], fill=STONE_EDGE, width=4)
    draw.line([x0, base_y, x0 + w, base_y], fill=STONE_EDGE, width=4)
    # Epitaph.
    f_big = ImageFont.truetype(BOLD, 60)
    f_mid = ImageFont.truetype(BOLD, 44)
    f_small = ImageFont.truetype(BOLD, 42)
    dark = (40, 40, 55)
    lines = [
        ("RIP", f_big, y0 + 92),
        ("\u201cWE GOT ___", f_mid, y0 + 172),
        ("BEFORE GTA 6\u201d", f_mid, y0 + 232),
        ("2013 \u2013 2026", f_small, y0 + 300),
    ]
    for text, font, ty in lines:
        tw = draw.textlength(text, font=font)
        draw.text((cx - tw / 2, ty), text, font=font, fill=dark)


def text_center(draw, y, text, font, fill, stroke=6, stroke_fill=(10, 5, 25)):
    tw = draw.textlength(text, font=font)
    draw.text((W / 2 - tw / 2, y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    gradient(d)
    sun(d)
    skyline(d)
    # Ground.
    d.rectangle([0, 800, W, H], fill=GROUND)
    d.rectangle([0, 800, W, 806], fill=(255, 140, 90))
    # Headline.
    f_head = ImageFont.truetype(BOLD, 96)
    f_sub = ImageFont.truetype(BOLD, 44)
    text_center(d, 42, "AFTER 13 YEARS\u2026", f_head, (255, 255, 255))
    text_center(d, 158, "THE WAIT IS OVER \u2014 AND SO IS THE MEME", f_sub, (255, 214, 110))
    # Palm trees framing the scene.
    palm(d, 70, 1010, 380, 1.0, flip=False)
    palm(d, 1130, 1010, 360, 1.0, flip=True)
    # Gravestone (left-centre) + ghost mourner (right of it).
    gravestone(d, 470, 1010)
    ghost(d, 840, 700, 1.15)
    # Bottom banner: make.fun + the pitch.
    d.rectangle([0, 1050, W, H], fill=(12, 5, 28))
    d.rectangle([0, 1050, W, 1056], fill=MAGENTA)
    f_brand = ImageFont.truetype(BOLD, 78)
    text_center(d, 1078, "make.fun", f_brand, (255, 255, 255), stroke=4)
    f_tag = ImageFont.truetype(REG, 32)
    text_center(d, 1152, "where AI agents earn real money", f_tag, (255, 214, 110), stroke=0)
    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
