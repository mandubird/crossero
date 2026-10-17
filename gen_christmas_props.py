# -*- coding: utf-8 -*-
"""성탄 성극 소품 도안(A4 PDF·미리보기 PNG) 생성: 별, 왕관, 양 머리띠, 천사 날개·후광, 구유와 아기, 선물 상자, 배역 이름표, 안내 포스터."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

from christmas_data import SCRIPTS

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(ROOT, "christmas", "props")
IMG_DIR = os.path.join(ROOT, "images", "christmas")
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
PW, PH = 2480, 3508  # A4 @300dpi (세로)
INK = (40, 30, 25)
LW = 7


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=(6 if bold else 0))


def page(landscape=False):
    sz = (PH, PW) if landscape else (PW, PH)
    im = Image.new("RGB", sz, "white")
    return im, ImageDraw.Draw(im)


def dashed_poly(d, pts, dash=34, gap=24, color=(120, 120, 120), w=5, close=True):
    seq = pts + ([pts[0]] if close else [])
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L // (dash + gap)))
        for i in range(n + 1):
            a = i * (dash + gap) / L
            b = min(1, (i * (dash + gap) + dash) / L)
            if a >= 1:
                break
            d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=color, width=w)


def title(d, text, sub, w):
    d.text((w // 2, 150), text, font=font(120, True), fill=INK, anchor="mm")
    d.text((w // 2, 270), sub, font=font(52), fill=(110, 90, 70), anchor="mm")


def footer(d, w, h):
    d.text((w // 2, h - 90), "십자가로세로 · crossero.com — 교회·주일학교·가정에서 비상업적으로 인쇄해 사용하세요", font=font(40), fill=(150, 130, 110), anchor="mm")


def star_pts(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def p_star():
    im, d = page()
    title(d, "베들레헴의 별", "색칠하고 점선을 따라 오려서 막대(빨대·나무젓가락)에 붙이세요", PW)
    pts = star_pts(PW // 2, 1500, 950, 400)
    d.polygon(pts, outline=INK, width=LW)
    for i in range(0, 10, 2):  # 가운데 선(접힌 느낌)
        d.line([(PW // 2, 1500), pts[i]], fill=(190, 160, 120), width=4)
    d.rounded_rectangle((PW // 2 - 150, 2500, PW // 2 + 150, 3300), 30, outline=INK, width=LW)
    d.text((PW // 2, 2900), "손잡이\n(뒷면에 막대를 붙이세요)", font=font(48), fill=(120, 100, 80), anchor="mm", align="center")
    dashed_poly(d, [(PW // 2 - 200, 520), (PW // 2 + 200, 520), (PW // 2 + 200, 560), (PW // 2 - 200, 560)], color=(255, 255, 255))
    footer(d, PW, PH)
    return im


def p_crown():
    im, d = page(landscape=True)
    W, H = PH, PW
    title(d, "동방 박사의 왕관", "색칠해서 오리고, 오른쪽 끝의 붙임 부분을 겹쳐 머리 둘레에 맞게 붙이세요 (3개)", W)
    for k in range(3):
        y0 = 420 + k * 640
        base = y0 + 460
        pts = [(180, base)]
        n = 6
        span = 2900
        for i in range(n):
            x = 180 + span * i / n
            pts += [(x + span / n * 0.25, y0), (x + span / n * 0.5, base - 140), (x + span / n * 0.75, y0)]
        pts += [(180 + span, base), (180 + span + 220, base), (180 + span + 220, base + 120), (180, base + 120)]
        d.polygon(pts, outline=INK, width=LW)
        for i in range(n):
            cx = 180 + span * i / n + span / n * 0.5
            d.ellipse((cx - 38, base + 5, cx + 38, base + 81), outline=INK, width=LW)
        d.text((180 + span + 110, base + 60), "붙임", font=font(36), fill=(150, 130, 110), anchor="mm")
    footer(d, W, H)
    return im


def p_sheep():
    im, d = page()
    title(d, "양 머리띠 (목자 극의 양)", "머리띠는 점선대로 오리고 귀는 아래에 붙이세요. 흰 솜이나 휴지를 붙이면 더 좋아요", PW)
    d.rounded_rectangle((200, 520, 2280, 800), 60, outline=INK, width=LW)
    d.text((1240, 660), "머리띠 (끝을 맞붙여 머리 둘레에 맞게 조절)", font=font(44), fill=(150, 130, 110), anchor="mm")
    for k, cx in enumerate((760, 1720)):
        cy = 1500
        d.ellipse((cx - 330, cy - 480, cx + 330, cy + 480), outline=INK, width=LW)
        d.ellipse((cx - 180, cy - 330, cx + 180, cy + 330), outline=INK, width=LW)
        for a in range(0, 360, 36):  # 솜털 곡선
            x = cx + 360 * math.cos(math.radians(a)); y = cy + 520 * math.sin(math.radians(a))
            d.ellipse((x - 60, y - 60, x + 60, y + 60), outline=INK, width=5)
        d.text((cx, cy + 650), "귀", font=font(48), fill=(120, 100, 80), anchor="mm")
    footer(d, PW, PH)
    return im


def _wing(d, cx, cy, sgn):
    """둥근 윗선과 물결(깃털) 아랫선을 가진 날개 한 짝."""
    def bez(p0, p1, p2, n=40):
        return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]
    sh = (cx, cy - 430)
    tip = (cx + sgn * 560, cy + 20)
    top = bez(sh, (cx + sgn * 560, cy - 560), tip)
    low = [tip]
    k = 6
    for i in range(k):  # 아랫쪽 깃털 물결
        a0 = (tip[0] + (cx + sgn * 40 - tip[0]) * i / k, tip[1] + (cy + 430 - tip[1]) * i / k)
        a1 = (tip[0] + (cx + sgn * 40 - tip[0]) * (i + 1) / k, tip[1] + (cy + 430 - tip[1]) * (i + 1) / k)
        mid = ((a0[0] + a1[0]) / 2 + sgn * 70, (a0[1] + a1[1]) / 2 + 40)
        low += bez(a0, mid, a1, 10)[1:]
    pts = top + low[1:] + [sh]
    d.polygon(pts, outline=INK, width=LW)
    for r in (0.35, 0.62):  # 깃털 줄
        pts2 = bez((sh[0] + (tip[0] - sh[0]) * 0.08, sh[1] + 90), (cx + sgn * 420 * r + sgn * 40, cy - 340 * r), (tip[0] - sgn * 70 * (1 - r), tip[1] + 160 * r), 30)
        d.line(pts2, fill=(190, 160, 120), width=5)


def p_angel():
    im, d = page()
    title(d, "천사 날개와 후광", "색칠해서 오리세요. 날개는 등에, 후광은 머리띠로 사용해요", PW)
    _wing(d, 1000, 1350, -1)
    _wing(d, 1480, 1350, 1)
    d.text((1240, 2100), "← 날개 두 개 (좌우 대칭) →", font=font(48), fill=(120, 100, 80), anchor="mm")
    d.rounded_rectangle((200, 2650, 2280, 2850), 50, outline=INK, width=LW)
    d.ellipse((1020, 2380, 1460, 2560), outline=INK, width=LW)
    d.text((1240, 2960), "후광 머리띠 (위의 타원을 띠에 붙이거나 철사로 세워요)", font=font(44), fill=(150, 130, 110), anchor="mm")
    footer(d, PW, PH)
    return im


def p_manger():
    im, d = page()
    title(d, "구유와 아기 예수님", "구유는 점선대로 접어 세우고, 아기는 오려서 구유 위에 놓으세요", PW)
    d.polygon([(400, 1000), (2080, 1000), (1840, 1700), (640, 1700)], outline=INK, width=LW)
    for y in range(1050, 1700, 90):  # 짚 무늬
        d.line([(520 + (y - 1000) * 0.3, y), (1960 - (y - 1000) * 0.3, y)], fill=(210, 180, 120), width=6)
    d.line([(700, 1700), (520, 2150)], fill=INK, width=LW + 6)
    d.line([(1780, 1700), (1960, 2150)], fill=INK, width=LW + 6)
    d.line([(640, 1700), (1840, 2150)], fill=INK, width=LW)
    d.line([(1840, 1700), (640, 2150)], fill=INK, width=LW)
    d.ellipse((700, 2550, 1780, 3300), outline=INK, width=LW)
    d.ellipse((1000, 2350, 1480, 2830), outline=INK, width=LW)
    d.arc((1120, 2500, 1360, 2680), 20, 160, fill=INK, width=LW)
    d.ellipse((1130, 2520, 1170, 2560), fill=INK); d.ellipse((1310, 2520, 1350, 2560), fill=INK)
    for y in (2900, 3000, 3100, 3200):
        d.line([(780, y), (1700, y)], fill=(190, 160, 130), width=6)
    d.text((1240, 3420), "아기 예수님(포대기)", font=font(44), fill=(130, 110, 90), anchor="mm")
    footer(d, PW, PH)
    return im


def p_gifts():
    im, d = page()
    title(d, "동방 박사의 선물 상자", "황금 · 유향 · 몰약 — 색칠해서 오려 선물로 드려요", PW)
    labels = [("황금", (220, 170, 40)), ("유향", (160, 120, 200)), ("몰약", (170, 90, 60))]
    for i, (lab, col) in enumerate(labels):
        y0 = 450 + i * 960
        x0 = 520
        d.rectangle((x0, y0 + 220, x0 + 1440, y0 + 800), outline=INK, width=LW)
        d.rectangle((x0 - 40, y0 + 120, x0 + 1480, y0 + 260), outline=INK, width=LW)
        d.rectangle((x0 + 640, y0 + 120, x0 + 800, y0 + 800), outline=INK, width=LW)
        d.ellipse((x0 + 450, y0 - 40, x0 + 820, y0 + 140), outline=INK, width=LW)
        d.ellipse((x0 + 620, y0 - 40, x0 + 990, y0 + 140), outline=INK, width=LW)
        d.text((x0 + 720, y0 + 520), lab, font=font(140, True), fill=INK, anchor="mm")
    footer(d, PW, PH)
    return im


def p_nametags():
    roles = []
    for s in SCRIPTS:
        for c in s["cast"]:
            nm = c.split("(")[0].strip()
            if nm and nm not in roles and nm not in ("해설 A", "해설 B"):
                roles.append(nm)
    roles = ["해설"] + [r for r in roles if r != "해설"] if "해설" not in roles else roles
    pages = []
    per = 10
    for pi in range(0, len(roles), per):
        im, d = page()
        title(d, "성극 배역 이름표", "오려서 목걸이처럼 걸거나 옷에 붙이세요 (구멍 표시에 끈을 연결)", PW)
        for k, nm in enumerate(roles[pi:pi + per]):
            col, row = k % 2, k // 2
            x0 = 180 + col * 1100
            y0 = 400 + row * 600
            d.rounded_rectangle((x0, y0, x0 + 1020, y0 + 520), 40, outline=INK, width=LW)
            d.ellipse((x0 + 490, y0 + 24, x0 + 530, y0 + 64), outline=INK, width=5)
            d.text((x0 + 510, y0 + 300), nm, font=font(120 if len(nm) <= 6 else 90, True), fill=INK, anchor="mm")
            d.text((x0 + 510, y0 + 470), "십자가로세로 성탄 성극", font=font(34), fill=(160, 140, 120), anchor="mm")
        footer(d, PW, PH)
        pages.append(im)
    return pages


def p_poster():
    im, d = page()
    d.text((PW // 2, 420), "성탄 성극", font=font(300, True), fill=INK, anchor="mm")
    d.text((PW // 2, 700), "아기 예수님이 오신 날을 함께 기뻐해요", font=font(72), fill=(110, 90, 70), anchor="mm")
    d.polygon(star_pts(PW // 2, 1350, 450, 190), outline=INK, width=LW)
    for i, lab in enumerate(["제목", "일시", "장소", "배역/참여"]):
        y = 2100 + i * 300
        d.text((330, y), lab, font=font(70, True), fill=INK, anchor="lm")
        d.line([(750, y + 40), (2150, y + 40)], fill=INK, width=5)
    footer(d, PW, PH)
    return im


def save_item(name, imgs, preview_idx=0):
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    imgs = imgs if isinstance(imgs, list) else [imgs]
    imgs[0].save(os.path.join(PDF_DIR, f"{name}.pdf"), "PDF", resolution=300, save_all=True, append_images=imgs[1:])
    pv = imgs[preview_idx].copy()
    pv.thumbnail((720, 720))
    pv.save(os.path.join(IMG_DIR, f"props-{name}.png"), optimize=True)
    return imgs


def main():
    items = [("star", p_star()), ("crown", p_crown()), ("sheep", p_sheep()), ("angel", p_angel()), ("manger", p_manger()), ("gifts", p_gifts()), ("nametags", p_nametags()), ("poster", p_poster())]
    allp = []
    for name, im in items:
        allp += save_item(name, im)
    allp[0].save(os.path.join(PDF_DIR, "all.pdf"), "PDF", resolution=300, save_all=True, append_images=allp[1:])
    print("도안 PDF 생성:", len(items), "종 + 전체 묶음", len(allp), "쪽")


if __name__ == "__main__":
    main()
