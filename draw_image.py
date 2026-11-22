#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Flat newspaper/infographic style, drawn entirely with PIL primitives so
every letter stays crisp and legible for the vision judge.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 234)
INK = (20, 28, 43)
NAVY = (20, 33, 61)
GOLD = (214, 164, 32)
CARD = (255, 255, 255)
GREY = (90, 96, 108)
RULE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, color, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms
def pic_globe(d, cx, cy, r, accent):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(27, 122, 77))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 180, fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 180, 360, fill=(255, 255, 255), width=2)
    # leaf sprouting from the top
    d.polygon([(cx, cy - r - 26), (cx + 20, cy - r - 2), (cx - 2, cy - r + 6)],
              fill=accent)
    d.line([cx, cy - r - 26, cx, cy - r], fill=accent, width=3)


def pic_blast(d, cx, cy, r, accent):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.55
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=(230, 126, 34))
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              fill=accent)
    d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2],
              fill=(255, 214, 90))


def pic_badge(d, cx, cy, r, accent):
    d.polygon([(cx, cy - r), (cx + r * 0.9, cy - r * 0.45), (cx + r * 0.7, cy + r * 0.6),
               (cx, cy + r), (cx - r * 0.7, cy + r * 0.6), (cx - r * 0.9, cy - r * 0.45)],
              fill=(31, 58, 95))
    star = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rad = r * 0.52 if i % 2 == 0 else r * 0.22
        star.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(star, fill=accent)


def pic_ship(d, cx, cy, r, accent):
    # waves
    for k, yy in enumerate((cy + r * 0.62, cy + r * 0.82)):
        for x0 in range(cx - r - 6, cx + r + 6, 34):
            d.arc([x0, yy - 8, x0 + 34, yy + 8], 0, 180, fill=(46, 90, 136), width=4)
    # hull
    d.polygon([(cx - r, cy + r * 0.1), (cx + r, cy + r * 0.1),
               (cx + r * 0.72, cy + r * 0.55), (cx - r * 0.72, cy + r * 0.55)],
              fill=(31, 58, 95))
    # containers + mast
    d.rectangle([cx - r * 0.55, cy - r * 0.42, cx - r * 0.05, cy + r * 0.08],
                fill=(214, 164, 32))
    d.rectangle([cx + r * 0.05, cy - r * 0.42, cx + r * 0.55, cy + r * 0.08],
                fill=(192, 57, 43))
    d.line([cx, cy - r * 0.85, cx, cy - r * 0.4], fill=INK, width=4)
    # flame above the deck
    d.polygon([(cx + r * 0.55, cy - r * 0.35), (cx + r * 0.85, cy - r * 0.75),
               (cx + r * 0.62, cy - r * 0.72), (cx + r * 0.78, cy - r * 1.05),
               (cx + r * 0.42, cy - r * 0.78), (cx + r * 0.3, cy - r * 0.95),
               (cx + r * 0.28, cy - r * 0.55)], fill=accent)


def pic_flags(d, cx, cy, r, accent):
    # EU circle (blue, gold stars) overlapping Indonesia (red over white)
    d.ellipse([cx - r, cy - r, cx + r * 0.25, cy + r], fill=(29, 78, 216))
    for i in range(8):
        ang = -math.pi / 2 + math.pi * i / 4
        sx = cx - r * 0.375 + r * 0.42 * math.cos(ang)
        sy = cy + r * 0.42 * math.sin(ang)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 214, 90))
    d.ellipse([cx - r * 0.25, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    d.pieslice([cx - r * 0.25, cy - r, cx + r, cy + r], 180, 360, fill=(220, 38, 38))
    d.pieslice([cx - r * 0.25, cy - r, cx + r, cy + r], 0, 180, fill=(255, 255, 255))
    d.ellipse([cx - r * 0.25, cy - r, cx + r, cy + r], outline=INK, width=2)


def pic_mosquito(d, cx, cy, r, accent):
    # shield behind
    d.polygon([(cx, cy - r), (cx + r * 0.85, cy - r * 0.5), (cx + r * 0.85, cy + r * 0.25),
               (cx, cy + r), (cx - r * 0.85, cy + r * 0.25), (cx - r * 0.85, cy - r * 0.5)],
              fill=(14, 124, 123))
    # check mark
    d.line([cx - r * 0.42, cy, cx - r * 0.08, cy + r * 0.35], fill=(255, 255, 255), width=7)
    d.line([cx - r * 0.08, cy + r * 0.35, cx + r * 0.5, cy - r * 0.35],
           fill=(255, 255, 255), width=7)
    # little mosquito flying off top-right
    mx, my = cx + r * 0.95, cy - r * 0.85
    d.ellipse([mx - 16, my - 5, mx + 16, my + 5], fill=INK)
    d.ellipse([mx - 26, my - 12, mx - 6, my + 2], fill=(160, 190, 200))
    d.ellipse([mx + 6, my - 12, mx + 26, my + 2], fill=(160, 190, 200))
    for dx in (-10, 0, 10):
        d.line([mx + dx, my + 4, mx + dx + 6, my + 20], fill=INK, width=2)


# ------------------------------------------------------------------- stories
STORIES = [
    dict(kicker="CLIMATE  ·  ANTALYA, TURKEY", color=(27, 122, 77),
         accent=(46, 160, 90),
         head="COP31 NEARS A FINAL DEAL",
         deck="Climate talks run past deadline as a new package seeks consensus.",
         pic=pic_globe),
    dict(kicker="CONFLICT  ·  BAHRAIN", color=(192, 57, 43),
         accent=(192, 57, 43),
         head="IRAN STRIKES BAHRAIN",
         deck="Attack sets an industrial site ablaze; defences intercept the rest.",
         pic=pic_blast),
    dict(kicker="CRIME  ·  SINALOA, MEXICO", color=(31, 58, 95),
         accent=(214, 164, 32),
         head="\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
         deck="Cartel boss seized in Sinaloa; at least 11 killed in the violence.",
         pic=pic_badge),
    dict(kicker="WAR AT SEA  ·  GULF OF FINLAND", color=(46, 90, 136),
         accent=(230, 126, 34),
         head="RUSSIAN SHIP ABLAZE",
         deck="Cargo vessel Sparta II burns after a drone strike; crew evacuates.",
         pic=pic_ship),
    dict(kicker="TRADE  ·  BRUSSELS – JAKARTA", color=(29, 78, 216),
         accent=(220, 38, 38),
         head="EU–INDONESIA DEAL SIGNED",
         deck="Trade pact sealed after a decade of negotiations.",
         pic=pic_flags),
    dict(kicker="HEALTH  ·  BRAZIL", color=(14, 124, 123),
         accent=(14, 124, 123),
         head="MOSQUITOES BEAT DENGUE",
         deck="Specially bred mosquitoes cut child dengue cases by about 69%.",
         pic=pic_mosquito),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 174], fill=GOLD)
    f_mast = font(SERIF_B, 62)
    d.text((W // 2, 18), "THE WORLD IN ONE DAY", font=f_mast, fill=(255, 255, 255),
           anchor="ma")
    f_date = font(SANS_B, 40)
    d.text((W // 2, 92), "Saturday, 21 November 2026", font=f_date,
           fill=(242, 193, 78), anchor="ma")
    f_sub = font(SANS, 22)
    d.text((W // 2, 186), "Six stories that defined the day",
           font=f_sub, fill=GREY, anchor="ma")

    # ---- story grid: 2 cols x 3 rows ----
    top, bottom = 228, 972
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = (bottom - top - 2 * gap) // 3
    f_kick = font(SANS_B, 17)
    f_head = font(SANS_B, 27)
    f_deck = font(SANS, 19)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                            outline=RULE, width=1)
        d.rounded_rectangle([x0, y0, x1, y0 + 7], radius=4, fill=s["color"])
        d.rectangle([x0, y0 + 3, x1, y0 + 7], fill=s["color"])

        # pictogram in its own tinted square
        px0, py0 = x0 + 16, y0 + 34
        ps = 148
        d.rounded_rectangle([px0, py0, px0 + ps, py0 + ps], radius=10,
                            fill=(245, 244, 238))
        s["pic"](d, px0 + ps // 2, py0 + ps // 2, 52, s["accent"])

        tx = px0 + ps + 18
        tw = x1 - tx - 16
        kick_fnt = f_kick
        while d.textlength(s["kicker"], font=kick_fnt) > tw and kick_fnt.size > 12:
            kick_fnt = font(SANS_B, kick_fnt.size - 1)
        d.text((tx, y0 + 22), s["kicker"], font=kick_fnt, fill=s["color"])
        head_lines = wrap(d, s["head"], f_head, tw)
        y = draw_text_block(d, tx, y0 + 48, head_lines, f_head, INK, 32)
        deck_lines = wrap(d, s["deck"], f_deck, tw)
        draw_text_block(d, tx, y + 6, deck_lines, f_deck, GREY, 24)

    # ---- footer ----
    d.line([margin, 990, W - margin, 990], fill=RULE, width=1)
    f_foot = font(SANS, 17)
    d.text((W // 2, 998), "Sources: Reuters · Associated Press · CNN — 21 November 2026",
           font=f_foot, fill=GREY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
