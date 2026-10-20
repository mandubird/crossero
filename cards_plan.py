# -*- coding: utf-8 -*-
"""말씀 카드 갤러리(샘플 카드) 계획. 실행: python3 cards_plan.py  → cards_plan.json
세트별로 구절을 고르고, 세트 분위기에 맞는 디자인(배경·글꼴·장식)을 정해 둔다.
실제 이미지는 tools/gen_cards.js 가 스튜디오 코드(crsStudio.renderCard)로 그린다."""
import json
import random
import re

from build_verse import PICKS, BOOKS, load_text
from season_picks import SEASONS
from verse_lib import verse_slug

PH = json.load(open("verse/studio_photos.json", encoding="utf-8"))["photos"]
LIGHT = {p["id"]: p["light"] for p in PH}
BYTHEME = {}
for p in PH:
    BYTHEME.setdefault(p["theme"], []).append(p["id"])

SERIF = ["Noto Serif KR", "Gowun Batang", "Nanum Myeongjo", "Hahmlet", "Song Myung"]
SANS = ["Pretendard Variable", "SUIT Variable", "Gowun Dodum", "Noto Sans KR"]
HAND = ["Nanum Brush Script", "Nanum Pen Script", "Hi Melody"]

# 세트: 키, 이름, 구절 출처, 장수, 사진 주제, 배경 장면, 장식, 테두리, 효과, 글꼴 풀
SETS = [
    dict(k="new-year", name="새해 말씀 카드", src=("season", "new-year"), n=36,
         photo=["night", "light", "sunrise", "mountain", "lake"], scene=["gold", "dawn", "ink", "bokeh", "pastel"],
         orn=["star", "cross", "olive", "anchor", None, None], frame=["double", "corner", None, None], fx=["sparkle", "rays", None, None], fonts=SERIF + SANS[:2]),
    dict(k="christmas", name="성탄 말씀 카드", src=("season", "christmas"), n=24,
         photo=["night", "light"], scene=["gold", "bokeh", "stained", "dawn", "parchment"],
         orn=["star", "dove", "cross", "flame", None], frame=["double", "corner", None], fx=["sparkle", "snow", None], fonts=SERIF),
    dict(k="thanksgiving", name="추수감사 말씀 카드", src=("season", "thanksgiving"), n=24,
         photo=["field", "autumn", "bread", "flower"], scene=["parchment", "linen", "wc", "hanji"],
         orn=["wheat", "grapes", "olive", None, None], frame=["line", "corner", None], fx=[None, "rays", None], fonts=SERIF + SANS[2:]),
    dict(k="comfort", name="위로의 말씀 카드", src=("topic", "위로"), n=24,
         photo=["lake", "sea", "forest", "light"], scene=["wc", "mist", "pastel", "dawn", "marble"],
         orn=["dove", "olive", None, None], frame=["round", "line", None, None], fx=[None, "rays", None], fonts=SERIF + SANS[:2]),
    dict(k="peace", name="평안의 말씀 카드", src=("topic", "평안"), n=19,
         photo=["lake", "water", "sea", "sky"], scene=["pastel", "wc", "hanji", "mist", "linen"],
         orn=["dove", "olive", "lily", None, None], frame=["line", None, None], fx=[None, None, "petals"], fonts=SERIF + SANS[:2]),
    dict(k="courage", name="용기의 말씀 카드", src=("topic", "용기"), n=24,
         photo=["mountain", "light", "sea", "desert"], scene=["ink", "gold", "dawn", "marble"],
         orn=["anchor", "flame", "cross", None, None], frame=["double", None, None], fx=[None, "rays", None], fonts=SERIF[:3] + SANS[:2]),
    dict(k="gratitude", name="감사의 말씀 카드", src=("topic", "감사"), n=21,
         photo=["flower", "field", "sunrise", "bread"], scene=["wc", "linen", "parchment", "pastel"],
         orn=["grapes", "wheat", "lily", None, None], frame=["corner", "round", None], fx=["petals", None, "sparkle"], fonts=SERIF + SANS[2:] + HAND[:1]),
    dict(k="hope", name="소망의 말씀 카드", src=("topic", "소망"), n=20,
         photo=["sunrise", "light", "sky", "field"], scene=["dawn", "pastel", "gold", "wc"],
         orn=["star", "lily", "dove", None, None], frame=[None, "line", None], fx=["rays", "sparkle", None], fonts=SERIF + SANS[:2]),
    dict(k="love", name="사랑의 말씀 카드", src=("topic", "사랑"), n=24,
         photo=["flower", "sunrise", "lake"], scene=["wc", "marble", "bokeh", "pastel", "linen"],
         orn=["heart", "dove", "lily", None, None], frame=["round", "corner", None], fx=["petals", "sparkle", None], fonts=SERIF + SANS[2:] + HAND[:1]),
    dict(k="faith", name="믿음의 말씀 카드", src=("topic", "믿음"), n=22,
         photo=["mountain", "light", "night", "sea"], scene=["ink", "gold", "stained", "parchment", "mist"],
         orn=["cross", "anchor", "flame", None], frame=["double", "line", None], fx=[None, "rays", "sparkle"], fonts=SERIF + SANS[:2]),
]


def verse_pool(src, text):
    kind, key = src
    if kind == "season":
        items = [tuple(x) for x in SEASONS[key]["picks"]]
    else:
        items = [(n, c, v) for n, c, v in PICKS[key]]
    out, seen = [], set()
    for n, c, v in items:
        ref = f"{n} {c}:{v}"
        t = text[(BOOKS.index(n) + 1, c, v)]
        if ref in seen or len(t) > 110 or t in seen:
            continue
        seen.add(ref)
        seen.add(t)
        out.append((ref, t))
    return out


def main():
    text = load_text()
    plan = []
    for S in SETS:
        rnd = random.Random(sum(map(ord, S["k"])))
        pool = verse_pool(S["src"], text)[: S["n"]]
        photos = [i for th in S["photo"] for i in BYTHEME.get(th, [])]
        rnd.shuffle(photos)
        pi = 0
        for idx, (ref, t) in enumerate(pool):
            use_photo = (idx % 3 != 2) and photos  # 약 2/3 사진, 1/3 질감 배경
            if use_photo:
                pid = photos[pi % len(photos)]
                pi += 1
                bg = {"type": "photo", "id": pid}
                dim = 12 if LIGHT.get(pid) else 26
            else:
                bg = {"type": "scene", "k": rnd.choice(S["scene"]), "seed": 3 + rnd.randrange(40)}
                dim = 18 if bg["k"] in ("mist", "dawn", "stained") else (0 if bg["k"] in ("wc", "ink", "hanji", "marble", "linen", "pastel", "parchment") else 6)
            d = {"bg": bg, "font": rnd.choice(S["fonts"]), "dim": dim, "dcolor": "text", "showRef": True, "shadow": True}
            o, f, x = rnd.choice(S["orn"]), rnd.choice(S["frame"]), rnd.choice(S["fx"])
            if o:
                d["orn"] = o
            else:
                d["orn"] = "none"
            d["frame"] = f or "none"
            d["fx"] = x or "none"
            if o and bg["type"] == "scene" and bg["k"] in ("gold", "bokeh", "stained", "dawn"):
                d["dcolor"] = "#f2c75c"
            plan.append({"set": S["k"], "ref": ref, "text": t, "file": f"{S['k']}-{verse_slug(ref)}.jpg", "design": d})
    json.dump(plan, open("cards_plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(plan), dict(Counter(p["set"] for p in plan)))


if __name__ == "__main__":
    main()
