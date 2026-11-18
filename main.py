#!/usr/bin/env python3
"""Draw a newspaper front page summing up Wednesday 18 November 2026
world news, and write it to /output/entry.png.

Deterministic: no network, no clock, no randomness. Running it twice
produces byte-identical output.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Canvas
W, H = 1024, 1024
PAPER = (250, 247, 240)      # warm off-white
INK = (26, 26, 26)           # near-black text
NAVY = (26, 42, 74)          # masthead
RED = (163, 29, 29)          # date / lead kicker
GREEN = (31, 111, 63)        # health tag
BROWN = (146, 96, 26)        # space tag
GREY = (90, 90, 90)          # summary text

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS_R = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")

MARGIN = 40
CONTENT_W = W - 2 * MARGIN


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, measured with the font."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, y, text, fnt, fill):
    """Draw text centred horizontally; return its height."""
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")
    return fnt.size


def draw_block(draw, x, y, text, fnt, fill, max_width, line_height):
    """Draw wrapped text starting at (x, y); return y after the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_height
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.line([(MARGIN, 26), (W - MARGIN, 26)], fill=INK, width=2)
    masthead = font(SERIF_B, 92)
    draw_centered(d, 34, "WORLD NEWS", masthead, NAVY)
    date_font = font(SERIF_R, 34)
    draw_centered(d, 138, "Wednesday, 18 November 2026", date_font, RED)
    d.line([(MARGIN, 188), (W - MARGIN, 188)], fill=INK, width=5)

    # ---- Lead story -----------------------------------------------
    lead_x = MARGIN
    y = 210
    tag_font = font(SANS_B, 19)
    d.text((lead_x, y), "ASIA", font=tag_font, fill=RED)
    y += 30
    head_font = font(SERIF_B, 52)
    y = draw_block(d, lead_x, y, "Trump lands in China as Xi and Putin meet",
                   head_font, INK, CONTENT_W, 60)
    y += 6
    sum_font = font(SANS_R, 24)
    y = draw_block(d, lead_x, y,
                   "Xi greets Trump at Shenzhen airport; the three leaders "
                   "prepare a rare trilateral summit as APEC opens.",
                   sum_font, INK, CONTENT_W, 31)

    # ---- Story grid: 2 columns x 3 rows ---------------------------
    cards = [
        ("US POLITICS", NAVY,
         "Peltola wins Alaska, Democrats take Senate",
         "Democrats reach a 56-44 majority, their largest since 2009, "
         "after a ninth midterm flip."),
        ("MIDDLE EAST", RED,
         "Iran fires drones at Bahrain and Kuwait",
         "Tehran answers the US strike on Qeshm Island with drone attacks "
         "on Gulf radar sites."),
        ("HEALTH", GREEN,
         "Congo Ebola outbreak passes 11,000 cases",
         "Cases more than doubled in three months; 5,400 dead, the "
         "second-largest outbreak on record."),
        ("SPACE", BROWN,
         "Voyager 1 reaches one light-day from Earth",
         "At 5:16 a.m. ET it crossed 16 billion miles, a distance no "
         "human-made object has reached."),
        ("DISASTER", INK,
         "Russian military plane crashes in Siberia",
         "All 19 people on board killed in the crash in Kemerovo region, "
         "officials say."),
        ("MIDDLE EAST", RED,
         "Gaza: cold kills in displaced tents",
         "Winter cold threatens camps as aid stays short; families shelter "
         "in flimsy tents."),
    ]

    col_w = (CONTENT_W - 28) // 2
    card_h = 168
    grid_top = 448
    row_gap = 14
    card_tag = font(SANS_B, 18)
    card_head = font(SERIF_B, 30)
    card_sum = font(SANS_R, 20)

    for i, (tag, colour, headline, summary) in enumerate(cards):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 28)
        top = grid_top + row * (card_h + row_gap)
        d.line([(x, top), (x + col_w, top)], fill=INK, width=2)
        cy = top + 10
        d.text((x, cy), tag, font=card_tag, fill=colour)
        cy += 28
        cy = draw_block(d, x, cy, headline, card_head, INK, col_w, 36)
        cy += 4
        draw_block(d, x, cy, summary, card_sum, GREY, col_w, 25)

    # ---- Footer ----------------------------------------------------
    foot_y = grid_top + 3 * card_h + 2 * row_gap + 12
    d.line([(MARGIN, foot_y), (W - MARGIN, foot_y)], fill=INK, width=2)
    foot_font = font(SANS_R, 19)
    draw_centered(d, foot_y + 10,
                  "Wednesday, 18 November 2026  ·  Sources: Reuters, AP, AFP",
                  foot_font, GREY)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG")


if __name__ == "__main__":
    main()
