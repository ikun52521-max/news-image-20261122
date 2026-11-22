#!/usr/bin/env python3
"""Draw the front page of Sunday 22 November 2026 as one 1024x1024 PNG.

No network, no arguments, fully deterministic: the same bytes every run.
Only Pillow (and the standard library) is used.
"""
import os
import random
import shutil
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "news.png"

PAPER = (247, 242, 231)
INK = (24, 26, 34)
RED = (178, 34, 28)
NAVY = (18, 42, 78)
TEAL = (13, 66, 84)
GOLD = (197, 148, 44)
GREY = (98, 96, 90)
RULE = (120, 110, 92)


def find_font(names):
    for base in ("/usr/share/fonts/truetype/dejavu",
                 "/usr/share/fonts/truetype/liberation"):
        for name in names:
            path = os.path.join(base, name)
            if os.path.exists(path):
                return path
    return None


SERIF_B = find_font(["DejaVuSerif-Bold.ttf"])
SERIF = find_font(["DejaVuSerif.ttf"])
SANS_B = find_font(["DejaVuSans-Bold.ttf"])
SANS = find_font(["DejaVuSans.ttf"])


def font(path, size):
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, leading, fill=INK):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, weight=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def burst(draw, cx, cy, r, core=(255, 190, 60), mid=(232, 90, 30),
          outer=(150, 30, 20)):
    rng = random.Random(cx * 31 + cy * 17)
    for rad, col in ((r, outer), (int(r * 0.66), mid), (int(r * 0.38), core)):
        pts = []
        for k in range(14):
            ang = k * 3.14159 * 2 / 14
            rr = rad * rng.uniform(0.72, 1.0)
            pts.append((cx + rr * 1.35 * __import__("math").cos(ang),
                        cy + rr * 0.9 * __import__("math").sin(ang)))
        draw.polygon(pts, fill=col)


def gulf_scene(draw, box):
    """Night over the Gulf: dark sky, burning sea, a tanker, missile arcs."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 34, 52))
    for i in range(26):  # stars, fixed seed positions
        rng = random.Random(9000 + i)
        sx = x0 + rng.randint(6, x1 - x0 - 6)
        sy = y0 + rng.randint(6, 70)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 200))
    # moon
    draw.ellipse([x1 - 66, y0 + 14, x1 - 30, y0 + 50], fill=(238, 230, 200))
    # sea
    draw.rectangle([x0, y0 + 150, x1, y1], fill=(10, 48, 66))
    for yy in range(y0 + 158, y1 - 8, 14):
        draw.line([(x0 + 8, yy), (x1 - 8, yy)], fill=(24, 84, 104), width=2)
    # missile arcs
    for ax, ay, bx in ((x0 + 40, y0 + 140, x0 + 150),
                       (x0 + 210, y0 + 145, x0 + 300)):
        draw.arc([ax, ay - 90, bx, ay + 40], start=200, end=340,
                 fill=(255, 200, 90), width=3)
    # tanker silhouette
    draw.rectangle([x0 + 30, y0 + 205, x0 + 250, y0 + 235], fill=(8, 10, 14))
    draw.rectangle([x0 + 190, y0 + 178, x0 + 228, y0 + 205], fill=(8, 10, 14))
    draw.rectangle([x0 + 96, y0 + 190, x0 + 106, y0 + 205], fill=(8, 10, 14))
    # fires on the tanker
    burst(draw, x0 + 70, y0 + 196, 26)
    burst(draw, x0 + 205, y0 + 190, 20)
    # smoke
    for k, (sx, sy, sr) in enumerate(((x0 + 70, y0 + 160, 16),
                                      (x0 + 82, y0 + 138, 20),
                                      (x0 + 205, y0 + 156, 14))):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(70, 70, 72))
    draw.rectangle(box, outline=(60, 50, 40), width=3)


def baltic_scene(draw, box):
    """Grey Baltic daylight: a listing cargo ship on fire, smoke, patrol boat."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(168, 178, 184))
    for i in range(9):  # cloud puffs
        rng = random.Random(500 + i)
        cx = x0 + rng.randint(10, x1 - x0 - 60)
        cy = y0 + rng.randint(4, 40)
        draw.ellipse([cx, cy, cx + 54, cy + 16], fill=(226, 230, 232))
    # sea
    draw.rectangle([x0, y0 + 118, x1, y1], fill=(74, 104, 126))
    for yy in range(y0 + 126, y1 - 6, 12):
        draw.line([(x0 + 6, yy), (x1 - 6, yy)], fill=(104, 134, 154), width=2)
    # listing ship
    draw.polygon([(x0 + 22, y0 + 128), (x0 + 268, y0 + 118),
                  (x0 + 252, y0 + 150), (x0 + 40, y0 + 158)],
                 fill=(52, 52, 56))
    draw.rectangle([x0 + 150, y0 + 96, x0 + 196, y0 + 122], fill=(52, 52, 56))
    draw.rectangle([x0 + 60, y0 + 108, x0 + 74, y0 + 126], fill=(52, 52, 56))
    burst(draw, x0 + 110, y0 + 108, 24)
    burst(draw, x0 + 180, y0 + 100, 18)
    for sx, sy, sr in ((x0 + 108, y0 + 66, 18), (x0 + 122, y0 + 44, 22),
                       (x0 + 178, y0 + 60, 15)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(58, 58, 60))
    # small patrol boat
    draw.polygon([(x0 + 236, y0 + 158), (x0 + 282, y0 + 158),
                  (x0 + 272, y0 + 170), (x0 + 246, y0 + 170)],
                 fill=(210, 210, 205))
    draw.rectangle(box, outline=(60, 50, 40), width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261122)
    for _ in range(1400):  # paper speckle
        d.point((rng.randint(0, W - 1), rng.randint(0, H - 1)),
                fill=(232, 226, 210))
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=RULE, width=1)

    # ---- masthead ----
    mast = font(SERIF_B, 66)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 34), title, font=mast, fill=NAVY)
    hrule(d, 48, W - 48, 118, weight=3, fill=NAVY)
    date_f = font(SANS_B, 30)
    d.text((48, 130), "SUNDAY, 22 NOVEMBER 2026", font=date_f, fill=RED)
    tag_f = font(SANS, 22)
    tag = "THE WORLD'S NEWS IN ONE PAGE"
    d.text((W - 48 - d.textlength(tag, font=tag_f), 134), tag,
           font=tag_f, fill=GREY)
    hrule(d, 48, W - 48, 172, weight=2)

    # ---- story 1: the Gulf (lead) ----
    kicker = font(SANS_B, 20)
    d.text((48, 190), "LEAD  •  THE GULF", font=kicker, fill=RED)
    h1 = font(SERIF_B, 46)
    y = para(d, (48, 216), "Iran hits U.S. bases in Bahrain", h1, 560, 52)
    deck = font(SERIF, 25)
    y = para(d, (48, y + 8),
             "Two waves of drones and missiles strike four American "
             "bases; Tehran claims two Patriot radars destroyed.",
             deck, 560, 32, fill=(52, 50, 46)) + 6
    body = font(SANS, 20)
    para(d, (48, y),
         "Bahrain said its defences intercepted the fire; a blaze broke "
         "out at an industrial site, with no injuries reported.",
         body, 560, 26)
    gulf_scene(d, (640, 190, 976, 440))
    cap = font(SANS, 17)
    para(d, (640, 448), "Tankers burn near Hormuz as the Gulf war widens.",
         cap, 336, 21, fill=GREY)
    hrule(d, 48, W - 48, 505, weight=2)

    # ---- story 2: the Baltic ----
    baltic_scene(d, (48, 525, 380, 700))
    d.text((48, 706), "The Sparta II burns in the Gulf of Finland.",
           font=cap, fill=GREY)
    d.text((404, 525), "WAR AT SEA  •  THE BALTIC", font=kicker, fill=RED)
    h2 = font(SERIF_B, 32)
    y = para(d, (404, 551), "Drones set Russian ship ablaze off Finland",
             h2, 572, 38)
    y = para(d, (404, y + 6),
             "The sanctioned cargo vessel Sparta II, bound for "
             "Kaliningrad, was hit in the Gulf of Finland; its crew was "
             "evacuated.",
             deck, 572, 32, fill=(52, 50, 46)) + 6
    quote = font(SERIF, 18)
    para(d, (404, y),
         "\u201cWar is spilling over into our immediate vicinity.\u201d "
         "\u2014 Orpo",
         quote, 572, 24, fill=NAVY)
    hrule(d, 48, W - 48, 775, weight=2)

    # ---- story 3: Trump on Iran ----
    d.text((48, 785), "DIPLOMACY  •  WASHINGTON", font=kicker, fill=RED)
    h3 = font(SERIF_B, 33)
    y = para(d, (48, 810),
             "Trump: Iran deal \u201ccould last 20 years\u201d",
             h3, 928, 40)
    para(d, (48, y + 4),
         "The president says he wants a permanent nuclear accord with "
         "Tehran \u2014 and speaks of \u201cultimate regime change\u201d "
         "as Gulf tensions climb.",
         deck, 928, 32, fill=(52, 50, 46))
    hrule(d, 48, W - 48, 912, weight=2)

    # ---- briefs ----
    d.text((48, 924), "ALSO TODAY", font=kicker, fill=RED)
    foot = font(SANS, 13)
    src = ("Sources: euronews \u00b7 Al Jazeera \u00b7 Reuters \u00b7 AP "
           "\u00b7 Yle \u00b7 Finnish Border Guard")
    d.text((W - 48 - d.textlength(src, font=foot), 927), src,
           font=foot, fill=GREY)
    brief = font(SANS, 18)
    para(d, (48, 948),
         "COP31 deadlocked over fossil fuels  \u00b7  Estonia to shut its "
         "border with Russia  \u00b7  U.S. \u201copen to\u201d a UN chief from "
         "the Americas, says Waltz  \u00b7  France and U.S. draft UN plan "
         "for post-UNIFIL Lebanon",
         brief, 928, 24, fill=(52, 50, 46))
    img.save(OUT, format="PNG", optimize=True)
    if os.path.isdir("/output"):
        shutil.copyfile(OUT, "/output/entry.png")
    return OUT


if __name__ == "__main__":
    print(build())
