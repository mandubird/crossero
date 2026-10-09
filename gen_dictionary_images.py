# -*- coding: utf-8 -*-
"""사전 항목별 대표 이미지 생성(가로 1200x630, 정사각 1000x1000). 실행: python3 gen_dictionary_images.py"""
import hashlib
import os
import random

from PIL import Image, ImageDraw, ImageFont

from dictionary_data_events_places import EVENTS, PLACES
from dictionary_data_books_ot import OT
from dictionary_data_books_nt import NT
from dictionary_data_people import PEOPLE

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "images", "dictionary")
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
LOGO = os.path.join(ROOT, "images", "crossero-logo.png")
COLORS = {"인물": ((11, 92, 173), (0, 115, 230)), "사건": ((120, 53, 15), (217, 119, 6)), "지명": ((6, 95, 70), (16, 185, 129)), "성경 책": ((76, 29, 149), (139, 92, 246))}


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=(6 if bold else 0))


def crossword_motif(draw, x0, y0, cell, cols, rows, seed, color):
    rnd = random.Random(seed)
    for r in range(rows):
        for c in range(cols):
            if rnd.random() < 0.55:
                draw.rounded_rectangle([x0 + c * cell, y0 + r * cell, x0 + (c + 1) * cell - 4, y0 + (r + 1) * cell - 4],
                                       radius=6, fill=color)


def gradient(w, h, c1, c2):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        row = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
        for x in range(w):
            px[x, y] = row
    return img


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=fnt) > max_w:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def card(e, w, h):
    c1, c2 = COLORS[e["type"]]
    img = gradient(w, h, c1, c2)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    seed = int(hashlib.md5(e["slug"].encode()).hexdigest()[:8], 16)
    cell = 46 if w > h else 52
    crossword_motif(d, w - cell * 7 - 20, h - cell * 6 - 20, cell, 7, 6, seed, (255, 255, 255, 38))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)
    pad = 70 if w > h else 80
    bw = 150 if len(e["type"]) <= 2 else 190
    d.rounded_rectangle([pad, pad, pad + bw, pad + 52], radius=26, fill=(255, 255, 255, 235))
    d.text((pad + bw // 2, pad + 26), e["type"], font=font(28, True), fill=c1, anchor="mm")
    name_size = 110 if w > h else 120
    nf = font(name_size, True)
    while d.textlength(e["name"], font=nf) > w - pad * 2 and name_size > 50:
        name_size -= 6
        nf = font(name_size, True)
    d.text((pad, pad + 130), e["name"], font=nf, fill="white")
    sf = font(44)
    y = pad + 130 + name_size + 24
    for line in wrap(d, e["sub"], sf, w - pad * 2):
        d.text((pad, y), line, font=sf, fill=(255, 255, 255, 230))
        y += 58
    d.text((pad, h - pad - 30), "십자가로세로 성경사전", font=font(34, True), fill=(255, 255, 255, 235))
    d.text((pad, h - pad + 12), "crossero.com", font=font(26), fill=(255, 255, 255, 190))
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for e in PEOPLE + EVENTS + PLACES + OT + NT:
        card(e, 1200, 630).save(os.path.join(OUT, f"{e['slug']}-bible-dictionary.png"), optimize=True)
        card(e, 1000, 1000).save(os.path.join(OUT, f"{e['slug']}-bible-dictionary-square.png"), optimize=True)
        n += 1
    print(f"이미지 {n * 2}장 생성")


if __name__ == "__main__":
    main()
