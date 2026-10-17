# -*- coding: utf-8 -*-
"""성탄 활동지(A4 PDF) 생성: 색칠 공부 3종, 미로, 낱말 찾기, 빈칸 채우기, 이야기 순서 카드, OX 퀴즈 + 정답지."""
import math
import os
import random
import re

from PIL import Image, ImageDraw, ImageFont

from verse_lib import KO_BOOKS, load_text

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(ROOT, "christmas", "activities")
IMG_DIR = os.path.join(ROOT, "images", "christmas")
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
PW, PH = 2480, 3508
INK = (40, 30, 25)
LW = 8
TEXT = load_text()
BIDX = {b: i + 1 for i, b in enumerate(KO_BOOKS)}


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=(6 if bold else 0))


def page():
    im = Image.new("RGB", (PW, PH), "white")
    return im, ImageDraw.Draw(im)


def head(d, t, sub):
    d.text((PW // 2, 170), t, font=font(120, True), fill=INK, anchor="mm")
    d.text((PW // 2, 300), sub, font=font(52), fill=(110, 90, 70), anchor="mm")
    d.text((300, 110), "이름 : ____________", font=font(50), fill=(140, 120, 100), anchor="lm")


def foot(d):
    d.text((PW // 2, PH - 90), "십자가로세로 · crossero.com — 교회·주일학교·가정에서 비상업적으로 인쇄해 사용하세요", font=font(40), fill=(150, 130, 110), anchor="mm")


def star(d, cx, cy, ro, ri=None, w=LW):
    ri = ri or ro * 0.42
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, outline=INK, width=w)


def person(d, x, y, s=1.0, hat=None, staff=False):
    """간단한 사람 윤곽(머리·옷·팔)."""
    hr = 90 * s
    d.ellipse((x - hr, y - hr, x + hr, y + hr), outline=INK, width=LW)
    d.ellipse((x - 30 * s, y - 20 * s, x - 14 * s, y - 4 * s), fill=INK)
    d.ellipse((x + 14 * s, y - 20 * s, x + 30 * s, y - 4 * s), fill=INK)
    d.arc((x - 36 * s, y + 5 * s, x + 36 * s, y + 55 * s), 20, 160, fill=INK, width=LW - 2)
    d.polygon([(x - 110 * s, y + 520 * s), (x + 110 * s, y + 520 * s), (x + 70 * s, y + hr), (x - 70 * s, y + hr)], outline=INK, width=LW)
    d.line([(x - 70 * s, y + hr + 40 * s), (x - 170 * s, y + 330 * s)], fill=INK, width=LW)
    d.line([(x + 70 * s, y + hr + 40 * s), (x + 170 * s, y + 330 * s)], fill=INK, width=LW)
    if hat == "crown":
        d.polygon([(x - 80 * s, y - hr), (x - 80 * s, y - hr - 90 * s), (x - 40 * s, y - hr - 40 * s), (x, y - hr - 100 * s), (x + 40 * s, y - hr - 40 * s), (x + 80 * s, y - hr - 90 * s), (x + 80 * s, y - hr)], outline=INK, width=LW)
    elif hat == "scarf":
        d.arc((x - hr - 20 * s, y - hr - 20 * s, x + hr + 20 * s, y + hr + 40 * s), 180, 360, fill=INK, width=LW + 6)
    elif hat == "halo":
        d.ellipse((x - 70 * s, y - hr - 90 * s, x + 70 * s, y - hr - 40 * s), outline=INK, width=LW)
    if staff:
        d.line([(x + 200 * s, y + 280 * s), (x + 200 * s, y + 560 * s)], fill=INK, width=LW + 4)
        d.arc((x + 140 * s, y + 220 * s, x + 260 * s, y + 340 * s), 180, 360, fill=INK, width=LW + 4)


def sheep(d, x, y, s=1.0):
    for dx, dy in ((-90, -30), (0, -60), (90, -30), (-60, 40), (60, 40), (0, 20)):
        d.ellipse((x + (dx - 80) * s, y + (dy - 80) * s, x + (dx + 80) * s, y + (dy + 80) * s), outline=INK, width=LW - 2)
    d.ellipse((x + 130 * s, y - 40 * s, x + 270 * s, y + 90 * s), outline=INK, width=LW - 2)
    d.ellipse((x + 200 * s, y - 5 * s, x + 218 * s, y + 13 * s), fill=INK)
    for dx in (-60, 60):
        d.line([(x + dx * s, y + 110 * s), (x + dx * s, y + 220 * s)], fill=INK, width=LW)


def hills(d, y0):
    d.arc((-600, y0, 1500, y0 + 1500), 180, 360, fill=INK, width=LW)
    d.arc((900, y0 + 120, 3100, y0 + 1700), 180, 360, fill=INK, width=LW)


def c_stable():
    im, d = page()
    head(d, "구유의 아기 예수님", "마리아, 요셉, 별과 구유를 예쁘게 색칠해 보세요")
    star(d, 1240, 600, 260)
    d.polygon([(380, 1500), (1240, 850), (2100, 1500)], outline=INK, width=LW)
    d.rectangle((520, 1500, 1960, 2900), outline=INK, width=LW)
    d.polygon([(900, 2400), (1580, 2400), (1480, 2900), (1000, 2900)], outline=INK, width=LW)
    d.ellipse((1020, 2200, 1460, 2480), outline=INK, width=LW)
    d.ellipse((1130, 2250, 1180, 2300), fill=INK); d.ellipse((1290, 2250, 1340, 2300), fill=INK)
    person(d, 760, 1750, 0.8, "scarf")
    person(d, 1720, 1750, 0.8)
    d.line([(520, 2900), (1960, 2900)], fill=INK, width=LW)
    foot(d)
    return im


def c_shepherds():
    im, d = page()
    head(d, "들에서 만난 천사", "목자와 양들, 천사를 색칠해 보세요")
    for i, (x, y) in enumerate([(300, 700), (1000, 560), (1900, 760), (2200, 520), (600, 480)]):
        star(d, x, y, 80)
    person(d, 1240, 780, 0.7, "halo")
    for dx in (-330, 330):  # 날개
        sg = 1 if dx > 0 else -1
        d.polygon([(1240 + sg * 90, 900), (1240 + sg * 480, 760), (1240 + sg * 560, 1010), (1240 + sg * 90, 1180)], outline=INK, width=LW)
    hills(d, 2050)
    person(d, 650, 1900, 0.75, "scarf", staff=True)
    sheep(d, 1500, 2700, 1.0)
    sheep(d, 1980, 2950, 0.7)
    foot(d)
    return im


def c_kings():
    im, d = page()
    head(d, "별을 따라온 박사들", "세 박사와 선물과 별을 색칠해 보세요")
    star(d, 1240, 650, 380)
    for k, x in enumerate((560, 1240, 1920)):
        person(d, x, 1500, 0.78, "crown")
        d.rectangle((x - 170, 2150, x + 170, 2420), outline=INK, width=LW)
        d.rectangle((x - 190, 2090, x + 190, 2160), outline=INK, width=LW)
        d.line([(x, 2090), (x, 2420)], fill=INK, width=LW)
    d.text((1240, 2700), "황금 · 유향 · 몰약", font=font(80, True), fill=INK, anchor="mm")
    foot(d)
    return im


def maze_pages():
    random.seed(12)
    cols, rows, cs = 15, 20, 136
    ox, oy = (PW - cols * cs) // 2, 520
    walls = {(x, y): {"N": True, "S": True, "E": True, "W": True} for x in range(cols) for y in range(rows)}
    seen = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        nb = [(dx, dy, a, b) for dx, dy, a, b in ((1, 0, "E", "W"), (-1, 0, "W", "E"), (0, 1, "S", "N"), (0, -1, "N", "S")) if 0 <= x + dx < cols and 0 <= y + dy < rows and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        dx, dy, a, b = random.choice(nb)
        walls[(x, y)][a] = False
        walls[(x + dx, y + dy)][b] = False
        seen.add((x + dx, y + dy))
        stack.append((x + dx, y + dy))
    # 정답 경로(BFS)
    from collections import deque
    prev = {(0, 0): None}
    q = deque([(0, 0)])
    while q:
        c = q.popleft()
        if c == (cols - 1, rows - 1):
            break
        x, y = c
        for dx, dy, a in ((1, 0, "E"), (-1, 0, "W"), (0, 1, "S"), (0, -1, "N")):
            n = (x + dx, y + dy)
            if not walls[c][a] and n not in prev:
                prev[n] = c
                q.append(n)
    path = []
    c = (cols - 1, rows - 1)
    while c:
        path.append(c)
        c = prev[c]

    def draw(sol):
        im, d = page()
        head(d, "아기 예수님께 가는 길", "목자가 아기 예수님이 계신 구유까지 길을 찾아 주세요" + (" (정답)" if sol else ""))
        for (x, y), w in walls.items():
            x0, y0 = ox + x * cs, oy + y * cs
            if w["N"] and not (x == 0 and y == 0):
                d.line([(x0, y0), (x0 + cs, y0)], fill=INK, width=8)
            if w["W"]:
                d.line([(x0, y0), (x0, y0 + cs)], fill=INK, width=8)
            if w["S"] and not (x == cols - 1 and y == rows - 1):
                d.line([(x0, y0 + cs), (x0 + cs, y0 + cs)], fill=INK, width=8)
            if w["E"]:
                d.line([(x0 + cs, y0), (x0 + cs, y0 + cs)], fill=INK, width=8)
        d.text((ox, oy - 50), "▶ 출발 (목자)", font=font(54, True), fill=INK, anchor="lm")
        d.text((ox + cols * cs, oy + rows * cs + 70), "도착 ▶ 아기 예수님의 구유", font=font(54, True), fill=INK, anchor="rm")
        if sol:
            pts = [(ox + x * cs + cs // 2, oy + y * cs + cs // 2) for x, y in reversed(path)]
            d.line(pts, fill=(220, 60, 40), width=14, joint="curve")
        foot(d)
        return im
    return draw(False), draw(True)


def wordsearch_pages():
    random.seed(7)
    words = ["예수", "마리아", "요셉", "베들레헴", "구유", "천사", "목자", "별", "박사", "경배", "구주", "평화", "나사렛", "황금"]
    N = 14
    grid = [[None] * N for _ in range(N)]
    placed = {}
    for w in sorted(words, key=len, reverse=True):
        for _ in range(500):
            horiz = random.random() < 0.5
            L = len(w)
            x = random.randint(0, N - (L if horiz else 1))
            y = random.randint(0, N - (1 if horiz else L))
            cells = [(x + (i if horiz else 0), y + (0 if horiz else i)) for i in range(L)]
            if all(grid[cy][cx] in (None, w[i]) for i, (cx, cy) in enumerate(cells)):
                for i, (cx, cy) in enumerate(cells):
                    grid[cy][cx] = w[i]
                placed[w] = cells
                break
    fill = list("하나라마바사아자차카타파가다는은의도지기이오서세시")
    for y in range(N):
        for x in range(N):
            if grid[y][x] is None:
                grid[y][x] = random.choice(fill)

    def draw(sol):
        im, d = page()
        head(d, "성탄 낱말 찾기", "가로·세로로 숨은 낱말 14개를 찾아 동그라미 하세요" + (" (정답)" if sol else ""))
        cs = 140
        ox, oy = (PW - N * cs) // 2, 430
        for y in range(N):
            for x in range(N):
                d.rectangle((ox + x * cs, oy + y * cs, ox + (x + 1) * cs, oy + (y + 1) * cs), outline=(210, 200, 190), width=3)
                d.text((ox + x * cs + cs // 2, oy + y * cs + cs // 2), grid[y][x], font=font(90, True), fill=INK, anchor="mm")
        if sol:
            for w, cells in placed.items():
                (x0, y0), (x1, y1) = cells[0], cells[-1]
                d.rounded_rectangle((ox + min(x0, x1) * cs + 8, oy + min(y0, y1) * cs + 8, ox + (max(x0, x1) + 1) * cs - 8, oy + (max(y0, y1) + 1) * cs - 8), 60, outline=(220, 60, 40), width=8)
        half = (len(words) + 1) // 2
        d.text((PW // 2, oy + N * cs + 120), "  ·  ".join(words[:half]), font=font(62, True), fill=(110, 80, 60), anchor="mm")
        d.text((PW // 2, oy + N * cs + 220), "  ·  ".join(words[half:]), font=font(62, True), fill=(110, 80, 60), anchor="mm")
        foot(d)
        return im
    return draw(False), draw(True)


def cloze_pages():
    vs = " ".join(TEXT[(BIDX["누가복음"], 2, v)] for v in range(8, 15))
    blanks = ["목자들", "양 떼", "천사", "구주", "그리스도", "구유", "평화"]
    for b in blanks:
        assert b in vs, b
    body = vs
    bank = []
    for b in blanks:
        body = body.replace(b, "§" + str(len(bank)) + "§", 1)
        bank.append(b)
    random.seed(3)
    shuffled = bank[:]
    random.shuffle(shuffled)

    def draw(sol):
        im, d = page()
        head(d, "누가복음 2장 8~14절 빈칸 채우기", "아래 낱말을 보고 빈칸에 알맞은 낱말을 써 보세요" + (" (정답)" if sol else ""))
        tf = font(76)
        x0, y = 260, 520
        maxw = PW - 520
        line = ""
        toks = re.split(r"(§\d+§)", body)
        segs = []
        for t in toks:
            m = re.match(r"§(\d+)§", t)
            if m:
                segs.append(("blank", bank[int(m.group(1))]))
            else:
                for w in re.findall(r"\S+\s*", t):
                    segs.append(("w", w))
        x = x0
        for kind, t in segs:
            if kind == "blank":
                wlen = max(260, len(t) * 90)
                if x + wlen > x0 + maxw:
                    x, y = x0, y + 150
                if sol:
                    d.text((x + wlen // 2, y), t, font=font(76, True), fill=(200, 50, 30), anchor="mm")
                d.line([(x, y + 48), (x + wlen, y + 48)], fill=INK, width=6)
                x += wlen + 24
            else:
                wlen = d.textlength(t, font=tf)
                if x + wlen > x0 + maxw:
                    x, y = x0, y + 150
                d.text((x, y), t, font=tf, fill=INK, anchor="lm")
                x += wlen
        bx = PW // 2
        d.rounded_rectangle((260, y + 260, PW - 260, y + 520), 40, outline=INK, width=LW)
        d.text((bx, y + 330), "낱말 상자", font=font(52, True), fill=(120, 100, 80), anchor="mm")
        d.text((bx, y + 440), "   ".join(shuffled), font=font(72, True), fill=INK, anchor="mm")
        foot(d)
        return im
    return draw(False), draw(True)


def sequence_page():
    im, d = page()
    head(d, "성탄 이야기 순서 맞추기", "카드를 오려서 이야기 순서대로 놓고, 동그라미에 번호를 써 보세요")
    cards = [("천사가 마리아에게 예수님의 탄생을 알려요", "누가복음 1:26-38"), ("마리아와 요셉이 베들레헴으로 가요", "누가복음 2:1-5"), ("아기 예수님이 구유에서 태어나요", "누가복음 2:6-7"),
             ("천사가 목자들에게 기쁜 소식을 전해요", "누가복음 2:8-14"), ("목자들이 아기 예수님을 찾아가요", "누가복음 2:15-20"), ("동방 박사들이 별을 따라와 경배해요", "마태복음 2:1-12")]
    random.seed(4)
    order = list(range(6))
    random.shuffle(order)
    for k, i in enumerate(order):
        col, row = k % 2, k // 2
        x0, y0 = 180 + col * 1130, 460 + row * 900
        d.rounded_rectangle((x0, y0, x0 + 1050, y0 + 820), 50, outline=INK, width=LW)
        d.ellipse((x0 + 40, y0 + 40, x0 + 190, y0 + 190), outline=INK, width=LW)
        t, ref = cards[i]
        lines = [t[j:j + 12] for j in range(0, len(t), 12)]
        for n, ln in enumerate(lines):
            d.text((x0 + 525, y0 + 330 + n * 110), ln, font=font(76, True), fill=INK, anchor="mm")
        d.text((x0 + 525, y0 + 730), ref, font=font(46), fill=(140, 120, 100), anchor="mm")
    foot(d)
    return im, order


def ox_pages():
    qs = [("예수님은 베들레헴에서 태어나셨어요.", True, "누가복음 2:4-7"), ("천사가 목자들에게 나타났어요.", True, "누가복음 2:9"), ("아기 예수님은 침대에 누워 계셨어요.", False, "누가복음 2:12 (구유)"),
          ("마리아에게 천사가 나타나 예수님의 탄생을 알려 주었어요.", True, "누가복음 1:26-31"), ("동방 박사들은 별을 보고 찾아왔어요.", True, "마태복음 2:2"),
          ("박사들이 드린 선물은 황금, 유향, 몰약이에요.", True, "마태복음 2:11"), ("목자들은 낮에 양을 치고 있었어요.", False, "누가복음 2:8 (밤)"),
          ("천사는 '무서워 말라'고 말했어요.", True, "누가복음 2:10"), ("박사들은 헤롯에게 돌아가 아기가 있는 곳을 알렸어요.", False, "마태복음 2:12"),
          ("마리아와 요셉은 아기를 성전에 데려가 주께 드렸어요.", True, "누가복음 2:22")]

    def draw(sol):
        im, d = page()
        head(d, "성탄 OX 퀴즈", "맞으면 O, 틀리면 X에 동그라미 하세요" + (" (정답)" if sol else ""))
        for i, (q, a, ref) in enumerate(qs):
            y = 520 + i * 285
            d.text((220, y), f"{i + 1}.", font=font(74, True), fill=INK, anchor="lm")
            d.text((340, y), q, font=font(62), fill=INK, anchor="lm")
            for k, lab in enumerate(("O", "X")):
                cx = 1880 + k * 280
                d.ellipse((cx - 90, y - 90, cx + 90, y + 90), outline=INK, width=LW)
                d.text((cx, y), lab, font=font(100, True), fill=INK, anchor="mm")
                if sol and ((lab == "O") == a):
                    d.ellipse((cx - 100, y - 100, cx + 100, y + 100), outline=(220, 60, 40), width=12)
            if sol:
                d.text((340, y + 80), ref, font=font(40), fill=(200, 80, 60), anchor="lm")
        foot(d)
        return im
    return draw(False), draw(True)


def save(name, imgs):
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    imgs = imgs if isinstance(imgs, list) else [imgs]
    imgs[0].save(os.path.join(PDF_DIR, f"{name}.pdf"), "PDF", resolution=300, save_all=True, append_images=imgs[1:])
    pv = imgs[0].copy()
    pv.thumbnail((720, 720))
    pv.save(os.path.join(IMG_DIR, f"act-{name}.png"), optimize=True)
    return imgs


def main():
    allp = []
    items = {}
    items["coloring-stable"] = [c_stable()]
    items["coloring-shepherds"] = [c_shepherds()]
    items["coloring-kings"] = [c_kings()]
    m, ms = maze_pages(); items["maze"] = [m, ms]
    w, ws = wordsearch_pages(); items["wordsearch"] = [w, ws]
    c, cs_ = cloze_pages(); items["cloze"] = [c, cs_]
    sq, order = sequence_page(); items["sequence"] = [sq]
    o, osol = ox_pages(); items["ox-quiz"] = [o, osol]
    for name, imgs in items.items():
        save(name, imgs)
        allp += imgs
    allp[0].save(os.path.join(PDF_DIR, "all.pdf"), "PDF", resolution=300, save_all=True, append_images=allp[1:])
    print("활동지:", len(items), "종,", len(allp), "쪽(정답지 포함)")


if __name__ == "__main__":
    main()
