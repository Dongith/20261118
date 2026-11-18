#!/usr/bin/env python3
"""Render a newspaper front page for Wednesday 18 November 2026 and
save it to /output/entry.png.

The program is fully deterministic: no network access, no clock reads,
no randomness, so two runs produce byte-identical PNG output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# Canvas size and palette
WIDTH, HEIGHT = 1024, 1024
PAPER = (250, 247, 240)      # warm off-white
INK = (26, 26, 26)           # near-black text
NAVY = (26, 42, 74)          # masthead and US politics tag
RED = (163, 29, 29)          # date line, lead kicker, Middle East tag
GREEN = (31, 111, 63)        # health tag
BROWN = (146, 96, 26)        # space tag
GREY = (90, 90, 90)          # summary and footer text

FONTS = "/usr/share/fonts/truetype/liberation"
SERIF_BOLD = os.path.join(FONTS, "LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONTS, "LiberationSerif-Regular.ttf")
SANS_BOLD = os.path.join(FONTS, "LiberationSans-Bold.ttf")
SANS = os.path.join(FONTS, "LiberationSans-Regular.ttf")

MARGIN = 40
TEXT_W = WIDTH - 2 * MARGIN


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, font, max_width):
    """Break text into lines that fit inside max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, y, text, font, fill):
    """Draw one line centred on the page; return the font height."""
    draw.text((WIDTH // 2, y), text, font=font, fill=fill, anchor="ma")
    return font.size


def paragraph(draw, x, y, text, font, fill, max_width, leading):
    """Draw wrapped text from (x, y); return the y below the last line."""
    for line in wrap_lines(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    draw.line([(MARGIN, 26), (WIDTH - MARGIN, 26)], fill=INK, width=2)
    masthead_font = load(SERIF_BOLD, 92)
    centred(draw, 34, "WORLD NEWS", masthead_font, NAVY)
    date_font = load(SERIF, 34)
    centred(draw, 138, "Wednesday, 18 November 2026", date_font, RED)
    draw.line([(MARGIN, 188), (WIDTH - MARGIN, 188)], fill=INK, width=5)

    # ---- Lead story ----
    y = 210
    tag_font = load(SANS_BOLD, 19)
    draw.text((MARGIN, y), "ASIA", font=tag_font, fill=RED)
    y += 30
    lead_head_font = load(SERIF_BOLD, 52)
    y = paragraph(draw, MARGIN, y, "Trump lands in China as Xi and Putin meet",
                  lead_head_font, INK, TEXT_W, 60)
    y += 6
    lead_sum_font = load(SANS, 24)
    y = paragraph(draw, MARGIN, y,
                  "Xi greets Trump at Shenzhen airport; the three leaders "
                  "prepare a rare trilateral summit as APEC opens.",
                  lead_sum_font, INK, TEXT_W, 31)

    # ---- Story grid: two columns, three rows ----
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
         "second-largest on record."),
        ("SPACE", BROWN,
         "Voyager 1 reaches one light-day from Earth",
         "At 5:16 a.m. ET it crossed 16 billion miles — farther than any "
         "human-made object."),
        ("DISASTER", INK,
         "Russian military plane crashes in Siberia",
         "All 19 on board were killed in the Kemerovo region crash, "
         "officials say."),
        ("MIDDLE EAST", RED,
         "Gaza: cold kills in displaced tents",
         "Winter cold threatens camps as aid stays short; families shelter "
         "in flimsy tents."),
    ]

    col_w = (TEXT_W - 28) // 2
    card_h = 160
    grid_top = 448
    row_gap = 14
    card_tag_font = load(SANS_BOLD, 18)
    card_head_font = load(SERIF_BOLD, 30)
    card_sum_font = load(SANS, 20)

    for i, (tag, colour, headline, summary) in enumerate(cards):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 28)
        top = grid_top + row * (card_h + row_gap)
        draw.line([(x, top), (x + col_w, top)], fill=INK, width=2)
        cy = top + 10
        draw.text((x, cy), tag, font=card_tag_font, fill=colour)
        cy += 28
        cy = paragraph(draw, x, cy, headline, card_head_font, INK, col_w, 36)
        cy += 4
        paragraph(draw, x, cy, summary, card_sum_font, GREY, col_w, 25)

    # ---- Footer ----
    foot_y = grid_top + 3 * card_h + 2 * row_gap + 12
    draw.line([(MARGIN, foot_y), (WIDTH - MARGIN, foot_y)], fill=INK, width=2)
    foot_font = load(SANS, 19)
    centred(draw, foot_y + 10,
            "Wednesday, 18 November 2026  ·  Sources: Reuters, AP, AFP",
            foot_font, GREY)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG")


if __name__ == "__main__":
    main()
