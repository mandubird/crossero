# -*- coding: utf-8 -*-
"""구절 카드 이미지 생성(1200x630 JPEG). 실행: python3 gen_verse_images.py
출력: images/verse/<책영문>-<장>-<절>.jpg  (macOS 한글 폰트 사용 → 로컬에서 실행 후 커밋)"""
import os

from PIL import Image, ImageDraw, ImageFont

import build_verse as bv
from verse_lib import verse_slug

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "images", "verse")
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
W, H = 1200, 630
TOPIC_COLOR = {"위로": (11, 92, 173), "평안": (6, 95, 70), "용기": (153, 27, 27), "감사": (180, 83, 9), "소망": (91, 33, 182),
               "사랑": (190, 24, 93), "믿음": (30, 64, 175), "용서": (15, 118, 110), "인내": (71, 85, 105),
               "기도": (67, 56, 202), "인도": (3, 105, 161), "회복": (21, 128, 61)}


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=(6 if bold else 0))


def wrap(draw, text, fnt, max_w):
    words, lines, line = text.split(" "), [], ""
    for w in words:
        t = f"{line} {w}".strip()
        if draw.textlength(t, font=fnt) > max_w and line:
            lines.append(line)
            line = w
        else:
            line = t
    if line:
        lines.append(line)
    return lines


def card(d):
    color = TOPIC_COLOR.get(d["topic"], (11, 92, 173))
    img = Image.new("RGB", (W, H), "#fffdf6")
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        row = (int(255 * (1 - t) + 233 * t), int(253 * (1 - t) + 242 * t), int(246 * (1 - t) + 255 * t))
        for x in range(W):
            px[x, y] = row
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([28, 28, W - 28, H - 28], radius=26, outline=color, width=6)
    dr.rounded_rectangle([44, 44, W - 44, H - 44], radius=20, outline=(155, 187, 230), width=2)
    # 주제 배지
    dr.rounded_rectangle([84, 82, 84 + 120, 82 + 46], radius=23, fill=color)
    dr.text((84 + 60, 82 + 23), d["topic"], font=font(26, True), fill="white", anchor="mm")
    # 본문: 글자 크기를 줄여 가며 영역(높이 330)에 맞춤
    box_w, box_h, top = W - 220, 330, 160
    fs = 56
    while fs >= 32:
        f = font(fs)
        lines = wrap(dr, d["text"], f, box_w)
        lh = int(fs * 1.55)
        if len(lines) * lh <= box_h:
            break
        fs -= 2
    f = font(fs)
    lines = wrap(dr, d["text"], f, box_w)
    lh = int(fs * 1.55)
    y = top + max(0, (box_h - len(lines) * lh) // 2)
    for ln in lines:
        dr.text((W // 2, y), ln, font=f, fill=(31, 45, 61), anchor="ma")
        y += lh
    dr.text((W // 2, 492), d["ref"], font=font(36, True), fill=color, anchor="ma")
    dr.text((W // 2, 546), "십자가로세로 · crossero.com", font=font(24), fill=(153, 160, 175), anchor="ma")
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    data = bv.build_data()
    total = 0
    for d in data:
        path = os.path.join(OUT, verse_slug(d["ref"]) + ".jpg")
        card(d).save(path, "JPEG", quality=84, optimize=True, progressive=True)
        total += os.path.getsize(path)
    print(f"카드 이미지 {len(data)}장, 합계 {total / 1024 / 1024:.1f}MB")


if __name__ == "__main__":
    main()
