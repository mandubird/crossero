# -*- coding: utf-8 -*-
"""성경 지도 정적 이미지 생성(Natural Earth 퍼블릭 도메인 해안선·호수·강 사용).
사용: python3 gen_map_images.py <natural-earth geojson 폴더>
출력: images/maps/{slug}-map.png (지명), images/maps/{route-slug}.png (경로), images/maps/bible-map-overview.png"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from dictionary_geo_data import GEO
from dictionary_routes_data import PLACES as RP
from build_routes import ROUTES

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "images", "maps")
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
W, H, SS = 1200, 630, 2
WATER, LAND, LAKE, RIVER = (205, 226, 243), (246, 241, 228), (190, 216, 238), (120, 170, 215)
INK = (22, 38, 58)


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=(6 if bold else 0))


def load(ne, name):
    return json.load(open(os.path.join(ne, f"{name}.geojson"), encoding="utf-8"))["features"]


def rings(geom):
    t = geom["type"]
    if t == "Polygon":
        yield geom["coordinates"]
    elif t == "MultiPolygon":
        for p in geom["coordinates"]:
            yield p
    elif t in ("LineString",):
        yield [geom["coordinates"]]
    elif t == "MultiLineString":
        for l in geom["coordinates"]:
            yield [l]


def bbox_of(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


class Proj:
    def __init__(self, lon0, lat0, lon1, lat1):
        self.k = math.cos(math.radians((lat0 + lat1) / 2))
        # 이미지 비율(W:H)에 맞춰 영역을 확장
        cx, cy = (lon0 + lon1) / 2, (lat0 + lat1) / 2
        w, h = (lon1 - lon0) * self.k, (lat1 - lat0)
        if w / h < W / H:
            w = h * W / H
        else:
            h = w * H / W
        self.cx, self.cy, self.w, self.h = cx, cy, w, h
        self.s = (W * SS) / w

    def xy(self, lon, lat):
        return ((lon - self.cx) * self.k * self.s + W * SS / 2, (self.cy - lat) * self.s + H * SS / 2)

    def view(self):
        return (self.cx - self.w / self.k / 2, self.cy - self.h / 2, self.cx + self.w / self.k / 2, self.cy + self.h / 2)


def base(proj, data):
    land, lakes, rivers = data
    im = Image.new("RGB", (W * SS, H * SS), WATER)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = proj.view()

    def hit(b):
        return not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1)
    for b, poly in land:
        if hit(b):
            for r in poly:
                d.polygon([proj.xy(*p) for p in r], fill=LAND)
    for b, poly in lakes:
        if hit(b):
            for r in poly:
                d.polygon([proj.xy(*p) for p in r], fill=LAKE)
    for b, line in rivers:
        if hit(b):
            d.line([proj.xy(*p) for p in line], fill=RIVER, width=int(2.2 * SS), joint="curve")
    return im, d


def prep(ne):
    def polys(feats):
        out = []
        for f in feats:
            for p in rings(f["geometry"]):
                pts = [pt for r in p for pt in r]
                out.append((bbox_of(pts), [[(c[0], c[1]) for c in r] for r in p]))
        return out
    rv = []
    for f in load(ne, "ne_10m_rivers_lake_centerlines"):
        if (f["properties"].get("name") or "") in ("Jordan", "Nile", "Euphrates", "Tigris", "Tevere"):
            for p in rings(f["geometry"]):
                line = p[0]
                rv.append((bbox_of(line), [(c[0], c[1]) for c in line]))
    return polys(load(ne, "ne_10m_land")), polys(load(ne, "ne_10m_lakes")), rv


class Placer:
    """라벨이 서로 겹치지 않도록 후보 위치를 시도한다."""
    def __init__(self, d):
        self.d, self.rects = d, [(0, 0, W * SS, 100 * SS), (0, (H - 50) * SS, W * SS, H * SS)]

    def obstacle(self, x, y, r):
        self.rects.append((x - r, y - r, x + r, y + r))

    def put(self, x, y, s, f, fill=INK, must=False, gap=18 * SS):
        bb = self.d.textbbox((0, 0), s, font=f, stroke_width=3 * SS)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        cands = [(x + gap, y - h / 2), (x - gap - w, y - h / 2), (x - w / 2, y - gap - h), (x - w / 2, y + gap),
                 (x + gap, y - gap - h), (x + gap, y + gap * 0.4), (x - gap - w, y - gap - h), (x - gap - w, y + gap * 0.4)]
        for cx, cy in cands:
            r = (cx - 2 * SS, cy - 2 * SS, cx + w + 2 * SS, cy + h + 2 * SS)
            if r[0] < 6 * SS or r[2] > (W - 6) * SS:
                continue
            if all(r[2] <= a[0] or r[0] >= a[2] or r[3] <= a[1] or r[1] >= a[3] for a in self.rects):
                self.rects.append(r)
                text_outline(self.d, (cx - bb[0], cy - bb[1]), s, f, fill=fill)
                return True
        if must:
            cx, cy = cands[0]
            self.rects.append((cx, cy, cx + w, cy + h))
            text_outline(self.d, (cx - bb[0], cy - bb[1]), s, f, fill=fill)
            return True
        return False


def text_outline(d, xy, s, f, fill=INK, stroke=(255, 255, 255)):
    d.text(xy, s, font=f, fill=fill, stroke_width=3 * SS, stroke_fill=stroke)


def chrome(im, title, sub):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W * SS, 92 * SS], fill=(11, 42, 74))
    d.text((34 * SS, 16 * SS), title, font=font(40 * SS, True), fill=(255, 255, 255))
    d.text((34 * SS, 62 * SS), sub, font=font(21 * SS), fill=(190, 214, 240))
    d.rectangle([0, (H - 46) * SS, W * SS, H * SS], fill=(11, 42, 74))
    d.text((34 * SS, (H - 36) * SS), "십자가로세로 성경 지도 · crossero.com", font=font(20 * SS, True), fill=(255, 255, 255))
    d.text(((W - 440) * SS, (H - 34) * SS), "지도 데이터 Natural Earth · 위치 OpenBible.info CC BY 4.0", font=font(14 * SS), fill=(160, 190, 225))


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name), optimize=True)


def pin(d, x, y, r=13):
    d.ellipse([x - r * SS, y - r * SS, x + r * SS, y + r * SS], fill=(214, 40, 40), outline=(255, 255, 255), width=3 * SS)
    d.ellipse([x - 4 * SS, y - 4 * SS, x + 4 * SS, y + 4 * SS], fill=(255, 255, 255))


CLUSTER = ("jerusalem", "bethlehem", "mount-of-olives", "gethsemane", "golgotha", "bethel", "jericho", "hebron")


def place_map(slug, g, data, names, sub):
    span = 0.55 if slug in CLUSTER else 1.7
    proj = Proj(g["lon"] - span, g["lat"] - span * 0.62, g["lon"] + span, g["lat"] + span * 0.62)
    im, d = base(proj, data)
    pl = Placer(d)
    x, y = proj.xy(g["lon"], g["lat"])
    pl.obstacle(x, y, 16 * SS)
    others = []
    for s_, o in GEO.items():
        if s_ == slug:
            continue
        ox, oy = proj.xy(o["lon"], o["lat"])
        if 30 * SS < ox < (W - 30) * SS and 112 * SS < oy < (H - 66) * SS and math.hypot(ox - x, oy - y) > 26 * SS:
            others.append((ox, oy, names[s_]))
            pl.obstacle(ox, oy, 8 * SS)
    pl.put(x, y, names[slug], font(34 * SS, True), fill=(160, 20, 20), must=True, gap=24 * SS)
    for ox, oy, nm in others:
        d.ellipse([ox - 6 * SS, oy - 6 * SS, ox + 6 * SS, oy + 6 * SS], fill=(90, 120, 160), outline=(255, 255, 255), width=2 * SS)
        pl.put(ox, oy, nm, font(20 * SS), gap=12 * SS)
    pin(d, x, y)
    chrome(im, f"{names[slug]} 오늘의 위치", sub)
    save(im, f"{slug}-map.png")


def route_map(r, data):
    pts = [(RP[k]["lon"], RP[k]["lat"]) for k, _, _ in r["steps"]]
    b = bbox_of(pts)
    padx, pady = (b[2] - b[0]) * 0.10 + 0.5, (b[3] - b[1]) * 0.12 + 0.6
    proj = Proj(b[0] - padx, b[1] - pady - 0.6, b[2] + padx, b[3] + pady + 1.4)
    im, d = base(proj, data)
    col = tuple(int(r["color"][i:i + 2], 16) for i in (1, 3, 5))
    xy = [proj.xy(*p) for p in pts]
    # 점선 경로
    for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / (14 * SS)))
        for i in range(0, n, 2):
            a, c = i / n, min(1, (i + 1) / n)
            d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * c, y0 + (y1 - y0) * c)], fill=col, width=int(4 * SS))
    seen = {}
    pl = Placer(d)
    first = []
    for i, ((k, ref, note), (x, y)) in enumerate(zip(r["steps"], xy), 1):
        if k in seen:
            continue
        seen[k] = i
        first.append((i, k, x, y))
        pl.obstacle(x, y, 16 * SS)
    for i, k, x, y in first:
        rr = 15 * SS
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col, outline=(255, 255, 255), width=3 * SS)
        f = font(17 * SS, True)
        tw = d.textlength(str(i), font=f)
        d.text((x - tw / 2, y - 11 * SS), str(i), font=f, fill=(255, 255, 255))
    for i, k, x, y in first:
        pl.put(x, y, RP[k]["name"].split("(")[0], font(19 * SS, True), must=False, gap=20 * SS)
    chrome(im, r["name"] + " 지도", f"{r['ref']} · {r['when']}")
    save(im, f"{r['slug']}.png")


def overview(data, names):
    pts = [(g["lon"], g["lat"]) for s, g in GEO.items() if 25 < g["lon"] < 40]
    b = bbox_of(pts)
    proj = Proj(b[0] - 0.8, b[1] - 0.8, b[2] + 0.8, b[3] + 0.8)
    im, d = base(proj, data)
    for s, g in GEO.items():
        x, y = proj.xy(g["lon"], g["lat"])
        if 0 < x < W * SS and 92 * SS < y < (H - 46) * SS:
            d.ellipse([x - 8 * SS, y - 8 * SS, x + 8 * SS, y + 8 * SS], fill=(0, 115, 230), outline=(255, 255, 255), width=3 * SS)
            text_outline(d, (x + 12 * SS, y - 12 * SS), names[s], font(18 * SS, True))
    chrome(im, "성경 지도 - 성경 속 지명", "지명이 지금은 어디에 있을까요?")
    save(im, "bible-map-overview.png")


def main():
    ne = sys.argv[1]
    data = prep(ne)
    from build_dictionary import BY_SLUG
    names = {s: BY_SLUG[s]["name"] for s in GEO}
    for s, g in GEO.items():
        place_map(s, g, data, names, g["where"][:40])
    for r in ROUTES:
        route_map(r, data)
    overview(data, names)
    print("지도 이미지:", len(GEO) + len(ROUTES) + 1)


if __name__ == "__main__":
    main()
