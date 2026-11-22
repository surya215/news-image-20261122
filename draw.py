#!/usr/bin/env python3
"""Render the world news of Sunday 22 November 2026 as one 1024x1024 image.

Deterministic: no randomness, no clock, no network. Pure Pillow drawing.
Run: python3 draw.py  -> writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette: a broadsheet front page -------------------------------------
PAPER = (247, 243, 234)
INK = (24, 24, 28)
NAVY = (16, 42, 78)
NAVY_DARK = (10, 30, 58)
RED = (178, 34, 34)
GOLD = (197, 146, 44)
TEAL = (18, 110, 105)
RULE = (150, 140, 120)
CARD_BG = (255, 255, 255)
CARD_LINE = (205, 196, 178)
MUTED = (90, 86, 76)
SEA = (46, 105, 150)
LAND = (214, 196, 158)
SAND = (232, 214, 176)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def headline_block(draw, x, y, text, fnt, color, max_w, leading):
    return para(draw, x, y, text, fnt, color, max_w, leading)


def label(draw, x, y, text, fnt, fill, halo):
    """Text with a halo so it stays readable over the map."""
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=3,
              stroke_fill=halo)


def draw_gulf_map(draw, x0, y0, w, h):
    """Schematic map of the Gulf: sea, land, Bahrain / Kuwait / Iran dots."""
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=8,
                           fill=(226, 236, 243), outline=CARD_LINE, width=1)
    # sea (Persian Gulf) as a diagonal band
    sea = [(x0 + 30, y0 + h - 40), (x0 + w - 110, y0 + 30),
           (x0 + w - 60, y0 + 55), (x0 + 90, y0 + h - 18)]
    draw.polygon(sea, fill=SEA)
    # Arabian peninsula landmass (bottom-left)
    land_ar = [(x0 + 8, y0 + h - 8), (x0 + 8, y0 + 120),
               (x0 + 70, y0 + 105), (x0 + 95, y0 + h - 30)]
    draw.polygon(land_ar, fill=LAND)
    # Iran landmass (top-right)
    land_ir = [(x0 + w - 8, y0 + 8), (x0 + 150, y0 + 8),
               (x0 + 130, y0 + 55), (x0 + w - 8, y0 + 60)]
    draw.polygon(land_ir, fill=LAND)
    label(draw, x0 + 16, y0 + 158, "ARABIA", font(SANS_B, 11),
          (120, 100, 60), (232, 214, 176))
    label(draw, x0 + w - 62, y0 + 14, "IRAN", font(SANS_B, 11),
          (120, 100, 60), (232, 214, 176))
    label(draw, x0 + 148, y0 + 108, "THE GULF", font(SANS_B, 11),
          (255, 255, 255), SEA)

    def marker(cx, cy, text, lx, ly, fill=INK, halo=(255, 255, 255)):
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                     outline=(255, 255, 255), width=2)
        label(draw, lx, ly, text, font(SANS_B, 13), fill, halo)

    # Bahrain (island in the Gulf, west shore), Kuwait (north-west shore)
    marker(x0 + 92, y0 + 128, "BAHRAIN", x0 + 112, y0 + 132)
    marker(x0 + 62, y0 + 96, "KUWAIT", x0 + 74, y0 + 88)
    marker(x0 + 205, y0 + 62, "TEHRAN", x0 + 217, y0 + 54)
    # strike burst lines around Bahrain
    bx, by = x0 + 92, y0 + 128
    for dx, dy in [(-16, -14), (16, -14), (-18, 6), (18, 8), (0, -20)]:
        draw.line([bx + dx * 0.55, by + dy * 0.55, bx + dx, by + dy],
                  fill=RED, width=2)
    draw.text((x0 + 10, y0 + h - 18), "Schematic map — not to scale",
              font=font(SANS, 10), fill=MUTED)


def icon(draw, kind, x, y, s, color):
    """Small pictogram per story card."""
    if kind == "flame":  # COP31 / climate
        draw.ellipse([x + s * 0.25, y + s * 0.35, x + s * 0.75, y + s * 0.9],
                     fill=color)
        draw.polygon([(x + s * 0.5, y), (x + s * 0.78, y + s * 0.55),
                      (x + s * 0.22, y + s * 0.55)], fill=color)
    elif kind == "ballot":  # Israel government: ballot box + paper slip
        draw.rectangle([x, y + s * 0.4, x + s, y + s * 0.95], fill=color)
        draw.rectangle([x + s * 0.3, y + s * 0.55, x + s * 0.7, y + s * 0.62],
                       fill=(255, 255, 255))
        draw.rectangle([x + s * 0.32, y + s * 0.05, x + s * 0.68, y + s * 0.45],
                       fill=(255, 255, 255), outline=color, width=2)
        draw.line([x + s * 0.42, y + s * 0.25, x + s * 0.58, y + s * 0.25],
                  fill=color, width=2)
    elif kind == "aid":  # Gaza aid
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.line([x + s * 0.5, y + s * 0.2, x + s * 0.5, y + s * 0.8],
                  fill=color, width=4)
        draw.line([x + s * 0.2, y + s * 0.5, x + s * 0.8, y + s * 0.5],
                  fill=color, width=4)
    elif kind == "quake":  # Peru earthquake
        pts = [(x, y + s * 0.6), (x + s * 0.2, y + s * 0.3),
               (x + s * 0.4, y + s * 0.7), (x + s * 0.6, y + s * 0.25),
               (x + s * 0.8, y + s * 0.65), (x + s, y + s * 0.4)]
        draw.line(pts, fill=color, width=4, joint="curve")
    elif kind == "crowd":  # France protests
        for i, cx in enumerate([0.18, 0.5, 0.82]):
            draw.ellipse([x + s * cx - 7, y + s * 0.15, x + s * cx + 7,
                          y + s * 0.15 + 14], fill=color)
            draw.pieslice([x + s * cx - 11, y + s * 0.45, x + s * cx + 11,
                           y + s * 0.95], 180, 360, fill=color)
    elif kind == "ball":  # tennis final: ball with white seams
        draw.ellipse([x, y, x + s, y + s], fill=color)
        draw.arc([x, y, x + s, y + s], 45, 135, fill=(255, 255, 255), width=3)
        draw.arc([x, y, x + s, y + s], 225, 315, fill=(255, 255, 255), width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ======================= MASTHEAD ======================================
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    d.text((32, 14), "THE WORLD IN ONE DAY",
           font=font(SERIF, 52), fill=(255, 255, 255))
    d.text((32, 76), "SUNDAY  •  22 NOVEMBER 2026",
           font=font(SANS_B, 20), fill=(232, 196, 96))
    d.text((W - 32, 20), "ONE DAY.",
           font=font(SERIF, 26), fill=(255, 255, 255), anchor="ra")
    d.text((W - 32, 56), "ONE PAGE.",
           font=font(SERIF, 26), fill=(255, 255, 255), anchor="ra")
    d.text((W - 32, 90), "ALL THE NEWS.",
           font=font(SERIF, 20), fill=(232, 196, 96), anchor="ra")

    # ======================= LEAD STORY ====================================
    lx, ly, lw, lh = 24, 132, 976, 252
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=CARD_BG, outline=CARD_LINE, width=1)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    tx = lx + 28
    d.text((tx, ly + 12), "LEAD STORY  —  THE GULF",
           font=font(SANS_B, 15), fill=RED)
    headline_block(d, tx, ly + 36,
                   "IRAN STRIKES U.S.-LINKED SITES IN BAHRAIN",
                   font(SERIF, 34), INK, 600, 40)
    y = para(d, tx, ly + 118,
             "Missiles and drones hit targets overnight into Sunday, "
             "Iran's Revolutionary Guard says, claiming two U.S. Patriot "
             "radars were destroyed. Bahrain says an industrial facility "
             "was hit and caught fire; its defences intercepted other "
             "attacks and no injuries were reported. U.S. officials say "
             "almost all incoming fire was intercepted.",
             font(SANS, 16), (50, 50, 55), 600, 21)
    d.text((tx, ly + lh - 26), "Sources: Reuters  •  AFP  •  Al Jazeera  •  22 Nov 2026",
           font=font(SANS_B, 12), fill=MUTED)
    draw_gulf_map(d, lx + 660, ly + 14, 300, 224)

    # ======================= SIX STORY CARDS ===============================
    cards = [
        ("CLIMATE  •  ANTALYA, TURKEY", "COP31 TALKS DEADLOCKED",
         "Negotiators run past their deadline with no deal: the draft "
         "drops all mention of fossil fuels and the $120bn adaptation "
         "finance figure. A final plenary is pushed into Sunday.",
         "flame", TEAL),
        ("ISRAEL  •  JERUSALEM", "EISENKOT TAPPED TO FORM GOVERNMENT",
         "President Herzog asks former army chief Gadi Eisenkot to try "
         "to build the next government, bypassing sitting prime minister "
         "Benjamin Netanyahu.",
         "ballot", NAVY),
        ("GAZA  •  AID", "FOUR NATIONS URGE OPEN AID ACCESS",
         "Australia, Canada, Italy and the UK jointly call on Israel to "
         "let aid reach flooded Gaza without restriction, saying the "
         "flooding has added to Palestinians' suffering.",
         "aid", RED),
        ("DISASTER  •  PERU", "PERU COUNTS COST OF FRIDAY'S QUAKE",
         "One dead, 16 hurt and 152 homes uninhabitable after Friday's "
         "6.9-magnitude quake in the Andes, officials say in updated "
         "tolls reported on Sunday.",
         "quake", (146, 94, 22)),
        ("EUROPE  •  FRANCE", "FOURTH WEEKEND OF COST-OF-LIVING PROTESTS",
         "France sees a fourth straight weekend of nationwide protests "
         "over rising living costs, as anger at the government grows.",
         "crowd", (90, 60, 120)),
        ("SPORT  •  TURIN", "ALCARAZ v ZVEREV FOR ATP FINALS TITLE",
         "Carlos Alcaraz fights back past Ben Shelton to set up a title "
         "decider against world No. 1 Alexander Zverev. France also "
         "reach the Nations Championship final.",
         "ball", (34, 120, 60)),
    ]
    gx, gy = 24, 400
    cw, ch, gap = 316, 190, 14
    for i, (tag, head, body, kind, color) in enumerate(cards):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8,
                            fill=CARD_BG, outline=CARD_LINE, width=1)
        d.rectangle([cx, cy, cx + cw, cy + 4], fill=color)
        d.text((cx + 14, cy + 12), tag, font=font(SANS_B, 11), fill=color)
        icon(d, kind, cx + cw - 44, cy + 12, 26, color)
        y = headline_block(d, cx + 14, cy + 34, head, font(SANS_B, 17),
                           INK, cw - 28, 21)
        para(d, cx + 14, y + 6, body, font(SANS, 13), (55, 55, 60),
             cw - 28, 17)

    # ======================= IN BRIEF ======================================
    bx, by, bw, bh = 24, 806, 976, 164
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8,
                        fill=NAVY_DARK, outline=NAVY_DARK)
    d.text((bx + 18, by + 10), "IN BRIEF", font=font(SANS_B, 15),
           fill=(232, 196, 96))
    briefs = [
        ("MYANMAR", "Magnitude 4.1 quake strikes in the early hours of Sunday."),
        ("NORWAY", "Top court rules climate-disputed oil licences invalid."),
        ("HONG KONG", "Voting opens for the powerful Election Committee."),
        ("SOMALIA", "Al-Shabaab claims hundreds dead in ambush on troops."),
        ("GHANA", "New 'Heritage Series' banknotes honour Nkrumah and Annan."),
        ("DR CONGO", "Ebola death toll passes 5,300, officials say."),
    ]
    col_w = (bw - 36) // 2
    for i, (tag, text) in enumerate(briefs):
        x = bx + 18 + (i % 2) * col_w
        y = by + 40 + (i // 2) * 42
        d.text((x, y), tag + " — ", font=font(SANS_B, 13),
               fill=(232, 196, 96))
        tw = d.textlength(tag + " — ", font=font(SANS_B, 13))
        lines = wrap(d, text, font(SANS, 13), col_w - tw - 10)[:2]
        yy = y
        for ln in lines:
            d.text((x + tw, yy), ln, font=font(SANS, 13),
                   fill=(235, 235, 235))
            yy += 17

    # ======================= FOOTER ========================================
    d.text((24, 982), "All stories happened or were first reported on Sunday, 22 November 2026.",
           font=font(SANS, 12), fill=MUTED)
    d.text((W - 24, 982), "Sources: Reuters • AFP • BBC • Al Jazeera • ANI",
           font=font(SANS, 12), fill=MUTED, anchor="ra")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, img.mode,
          os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
