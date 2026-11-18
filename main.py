#!/usr/bin/env python3
"""Wednesday 18 November 2026 — a one-page newspaper front page.

Drawn entirely with Pillow primitives: no templates, no image assets.
Every run produces identical bytes: fixed fonts, fixed geometry, no
randomness and nothing read from the clock or the environment.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
EDGE = 48                      # side margin
SPAN = PAGE_W - 2 * EDGE       # text width for full-width blocks

PAPER = (250, 247, 240)
NAVY = (26, 42, 74)
CRIMSON = (163, 29, 29)
INK = (34, 34, 34)
GREY = (96, 94, 88)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

_cache = {}


def face(path, size):
    """Load (and memoise) a TrueType face at the requested size."""
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def fit(text, font, width):
    """Greedy word wrap: split `text` into lines no wider than `width`."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if font.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def lines_down(pen, x, y, lines, font, colour, step):
    """Paint `lines` top-down starting at (x, y); return the y below them."""
    for line in lines:
        pen.text((x, y), line, font=font, fill=colour)
        y += step
    return y


def centred(pen, y, text, font, colour):
    """Paint one centred line at height y; return the y just below it."""
    x = (PAGE_W - font.getlength(text)) / 2
    pen.text((x, y), text, font=font, fill=colour)
    return y + int(font.size * 1.2)


def rule(pen, y, weight, colour=NAVY):
    """A horizontal rule across the content span; return the y below it."""
    pen.rectangle([EDGE, y, PAGE_W - EDGE, y + weight - 1], fill=colour)
    return y + weight


# --- the day's stories -------------------------------------------------------

LEAD = {
    "tag": "ASIA",
    "tag_colour": CRIMSON,
    "headline": "Trump lands in China as Xi and Putin meet",
    "summary": (
        "Xi greets Trump at Shenzhen airport as a trilateral summit opens "
        "alongside APEC, with trade and security topping the agenda."
    ),
}

GRID = [
    {
        "tag": "US POLITICS",
        "tag_colour": NAVY,
        "headline": "Peltola wins Alaska, Democrats take Senate",
        "summary": (
            "Peltola's win gives Democrats a 56\u201344 Senate majority, "
            "the largest since 2009."
        ),
    },
    {
        "tag": "MIDDLE EAST",
        "tag_colour": (138, 90, 0),
        "headline": "Iran fires drones at Bahrain and Kuwait",
        "summary": (
            "Iran launches drones at Bahrain and Kuwait in answer to the "
            "US strike on Qeshm Island."
        ),
    },
    {
        "tag": "HEALTH",
        "tag_colour": (30, 107, 52),
        "headline": "Congo Ebola outbreak passes 11,000 cases",
        "summary": (
            "The Congo outbreak passes 11,000 cases with 5,400 dead, the "
            "second-largest on record."
        ),
    },
    {
        "tag": "SPACE",
        "tag_colour": (74, 42, 107),
        "headline": "Voyager 1 reaches one light-day from Earth",
        "summary": (
            "Voyager 1 reaches one light-day out at 5:16 a.m. ET, 16 "
            "billion miles from home."
        ),
    },
    {
        "tag": "DISASTER",
        "tag_colour": (122, 31, 31),
        "headline": "Russian military plane crashes in Siberia",
        "summary": (
            "A Russian military plane crashes in Siberia, killing all 19 "
            "on board in Kemerovo."
        ),
    },
    {
        "tag": "MIDDLE EAST",
        "tag_colour": (138, 90, 0),
        "headline": "Gaza: cold kills in displaced tents",
        "summary": (
            "Cold weather is killing people in displaced families' tents "
            "in Gaza as winter sets in."
        ),
    },
]


def story_card(pen, x, y, width, story):
    """Paint one grid card (tag, headline, summary) at (x, y)."""
    tag_face = face(SANS_BOLD, 18)
    head_face = face(SERIF_BOLD, 28)
    body_face = face(SERIF, 20)

    pen.text((x, y), story["tag"], font=tag_face, fill=story["tag_colour"])
    y += 26
    head_lines = fit(story["headline"], head_face, width)
    y = lines_down(pen, x, y, head_lines, head_face, INK, 34)
    y += 6
    body_lines = fit(story["summary"], body_face, width)
    y = lines_down(pen, x, y, body_lines, body_face, INK, 25)
    return y


def front_page():
    """Compose the whole front page and return the Pillow image."""
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(sheet)

    y = 30
    # Masthead.
    y = centred(pen, y, "WORLD NEWS", face(SERIF_BOLD, 92), NAVY)
    y += 4
    # Date line.
    y = centred(
        pen, y, "Wednesday, 18 November 2026", face(SERIF_BOLD, 34), CRIMSON
    )
    y += 14
    y = rule(pen, y, 4)
    y += 16

    # Lead story.
    pen.text((EDGE, y), LEAD["tag"], font=face(SANS_BOLD, 21),
             fill=LEAD["tag_colour"])
    y += 30
    lead_head = fit(LEAD["headline"], face(SERIF_BOLD, 48), SPAN)
    y = lines_down(pen, EDGE, y, lead_head, face(SERIF_BOLD, 48), INK, 56)
    y += 8
    lead_body = fit(LEAD["summary"], face(SERIF, 25), SPAN)
    y = lines_down(pen, EDGE, y, lead_body, face(SERIF, 25), INK, 32)
    y += 14
    y = rule(pen, y, 2, NAVY)
    y += 16

    # 2 x 3 grid of story cards.
    col_w = (SPAN - 32) // 2
    row_h = 175
    for idx, story in enumerate(GRID):
        col, row = idx % 2, idx // 2
        cx = EDGE + col * (col_w + 32)
        cy = y + row * (row_h + 16)
        story_card(pen, cx, cy, col_w, story)

    # Footer.
    foot = "Wednesday, 18 November 2026 \u00b7 Sources: Reuters, AP, AFP"
    centred(pen, PAGE_H - 40, foot, face(SANS, 18), GREY)
    return sheet


def main():
    os.makedirs("/output", exist_ok=True)
    image = front_page()
    path = "/output/entry.png"
    image.save(path, format="PNG")
    with open(path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    size = os.path.getsize(path)
    print(f"wrote {path}: {image.size[0]}x{image.size[1]}, "
          f"{size} bytes, sha256 {digest}")


if __name__ == "__main__":
    main()
