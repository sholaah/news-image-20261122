#!/usr/bin/env python3
"""Render Sunday 22 November 2026's world news as one Economist-style cover.

Cream page, red masthead, the date as the huge title, a drawn night scene
over the Strait of Hormuz for the lead story, and a strip of secondary
headlines. Deterministic: same bytes on every run. Pillow only.
"""

import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (243, 236, 218)
INK = (26, 26, 26)
RED = (200, 16, 46)
DARK_RED = (150, 10, 32)
GREY = (90, 86, 76)
SKY_TOP = (11, 21, 38)
SKY_BOT = (30, 58, 82)
SEA = (8, 18, 28)
GOLD = (232, 176, 72)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, text, max_w, start, floor=10):
    """Largest font size at which text fits max_w (measured, not guessed)."""
    size = start
    fnt = font(path, size)
    while size > floor:
        probe = Image.new("RGB", (8, 8))
        if ImageDraw.Draw(probe).textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 2
        fnt = font(path, size)
    return fnt


def tracked(draw, cx, y, text, fnt, fill, tracking=4):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def wrapped(draw, cx, y, text, fnt, fill, width_px, leading):
    """Centre-wrapped paragraph; returns the y after the last line."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width_px:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    for line in lines:
        draw.text((cx - draw.textlength(line, font=fnt) / 2, y),
                  line, font=fnt, fill=fill)
        y += leading
    return y


def night_panel(img, box):
    """Draw the Hormuz night scene: sky, sea, tankers, missile arcs, blast."""
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    panel = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)
    # Vertical sky gradient.
    for yy in range(ph):
        t = yy / max(ph - 1, 1)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        d.line([(0, yy), (pw, yy)], fill=(r, g, b, 255))
    # Stars, seeded so the render never changes.
    rng = random.Random(20261122)
    for _ in range(70):
        sx, sy = rng.randrange(pw), rng.randrange(int(ph * 0.45))
        s = rng.choice([1, 1, 2])
        d.ellipse([sx, sy, sx + s, sy + s], fill=(235, 235, 220, 200))
    # Moon.
    d.ellipse([pw - 130, 26, pw - 82, 74], fill=(238, 230, 205, 255))
    d.ellipse([pw - 122, 30, pw - 90, 66], fill=(30, 58, 82, 255))
    # Sea.
    horizon = int(ph * 0.58)
    d.rectangle([0, horizon, pw, ph], fill=SEA + (255,))
    for yy in range(horizon + 6, ph, 14):
        d.line([(12, yy), (pw - 12, yy)], fill=(46, 84, 112, 255), width=1)
    # Tanker silhouettes.
    def tanker(tx, ty, scale, lit):
        hull = [(tx, ty), (tx + 150 * scale, ty), (tx + 168 * scale, ty + 22 * scale),
                (tx + 150 * scale, ty + 30 * scale), (tx, ty + 30 * scale)]
        d.polygon(hull, fill=(4, 8, 12, 255))
        d.rectangle([tx + 96 * scale, ty - 26 * scale, tx + 128 * scale, ty],
                    fill=(4, 8, 12, 255))
        d.rectangle([tx + 30 * scale, ty - 18 * scale, tx + 46 * scale, ty],
                    fill=(4, 8, 12, 255))
        if lit:
            for wx in range(6):
                d.rectangle([tx + 12 * scale + wx * 20 * scale, ty + 8 * scale,
                             tx + 18 * scale + wx * 20 * scale, ty + 14 * scale],
                            fill=(232, 176, 72, 255))
    tanker(70, horizon + 58, 1.0, True)
    tanker(748, horizon + 52, 0.7, False)
    # Missile arcs with bright heads, launched from the top corners.
    def arc(cx, cy, rad, start, end, colour, width=4):
        d.arc([cx - rad, cy - rad, cx + rad, cy + rad], start, end,
              fill=colour + (255,), width=width)
    arc(120, horizon + 40, 260, 300, 355, (255, 122, 40))
    arc(120, horizon + 40, 260, 318, 352, (255, 196, 90), width=2)
    arc(880, horizon + 60, 300, 185, 240, (255, 122, 40))
    arc(880, horizon + 60, 300, 192, 238, (255, 196, 90), width=2)
    # Explosion bloom over the sea between the tankers.
    ex, ey = 620, horizon + 40
    for rad, col in [(48, (255, 96, 20, 90)), (32, (255, 150, 50, 160)),
                     (18, (255, 210, 110, 220)), (9, (255, 244, 200, 255))]:
        d.ellipse([ex - rad, ey - rad, ex + rad, ey + rad], fill=col)
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        d.line([(ex, ey), (ex + 58 * math.cos(a), ey + 58 * math.sin(a))],
               fill=(255, 190, 90, 180), width=2)
    # Red horizon rule.
    d.rectangle([0, horizon - 2, pw, horizon], fill=(200, 16, 46, 255))
    img.alpha_composite(panel, (x0, y0))


def build():
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)

    # Frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # Red masthead band.
    d.rectangle([28, 28, W - 29, 128], fill=RED)
    tracked(d, W // 2, 52, "THE WORLD TODAY",
            font(SERIF_B, 62), (255, 255, 255), tracking=6)
    d.rectangle([28, 128, W - 29, 132], fill=INK)

    # Dateline.
    tracked(d, W // 2, 148, "SUNDAY  •  22 NOVEMBER 2026",
            font(SANS_B, 21), INK, tracking=3)

    # The date as the huge title, fitted to the page width.
    tracked(d, W // 2, 178, "22 NOVEMBER",
            fit(SERIF_B, "22 NOVEMBER", 900, 118), INK, tracking=2)
    d.line([(180, 316), (W - 180, 316)], fill=RED, width=4)

    # Lead headline.
    y = wrapped(d, W // 2, 336, "IRAN STRIKES A U.S. BASE IN KUWAIT",
                font(SERIF_B, 48), INK, 880, 56)
    wrapped(d, W // 2, y + 4,
            "Tehran claims missile and drone hits on Patriot radars as Bahrain "
            "is targeted too — and the Gulf war widens.",
            font(SERIF_I, 24), GREY, 860, 32)

    # Night scene over the strait.
    night_panel(img, (60, 524, 964, 744))
    d = ImageDraw.Draw(img)
    wrapped(d, W // 2, 752,
            "The Strait of Hormuz: tankers hit, air defences targeted — "
            "a regional war now aimed at America.",
            font(SERIF_I, 20), GREY, 880, 26)

    # Secondary stories: three columns.
    cols = [
        ("POLAND", "Russian missiles land on NATO soil",
         "Warsaw calls it a provocation as 400 drones and 110 missiles "
         "hammer Ukraine."),
        ("PERU", "Andes shaken by a 6.9 quake",
         "A magnitude 6.9 earthquake strikes the mountains; no casualties "
         "immediately reported."),
        ("ISRAEL", "Eisenkot tapped to form a government",
         "The president picks the ex-army chief over Netanyahu as coalition "
         "talks begin."),
    ]
    x = 60
    col_w = 281
    for i, (kicker, head, body) in enumerate(cols):
        cx = x + col_w // 2
        if i:
            d.line([(x - 12, 790), (x - 12, 934)], fill=(180, 172, 150), width=1)
        tracked(d, cx, 790, kicker, font(SANS_B, 20), RED, tracking=3)
        wrapped(d, cx, 818, head, font(SERIF_B, 23), INK, col_w, 28)
        wrapped(d, cx, 878, body, font(SERIF, 16), GREY, col_w, 20)
        x += col_w + 11

    # Bottom ticker, fitted to the page width.
    d.line([(60, 948), (964, 948)], fill=INK, width=1)
    ticker = ("ALSO: DEMOCRATS RECLAIM CONGRESS  •  COP31 INTO OVERTIME  •  "
              "FRANCE PROTESTS AGAIN  •  NORWAY VOIDS OIL LICENCES  •  "
              "DRC EBOLA TOLL PASSES 5,300")
    tracked(d, W // 2, 958, ticker,
            fit(SANS_B, ticker, 900, 14), INK, tracking=0)

    return img.convert("RGB")


if __name__ == "__main__":
    cover = build()
    cover.save("entry.png", format="PNG")
    print("wrote entry.png", cover.size)
