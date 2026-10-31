# -*- coding: utf-8 -*-
"""about.html의 '숫자로 보는 십자가로세로' 블록 갱신. 실행: python3 site_stats.py
저장소의 실제 파일에서 센 숫자만 쓴다(확인할 수 없는 숫자는 넣지 않는다)."""
import datetime
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
S, E = "<!--STATS-START-->", "<!--STATS-END-->"


def count():
    ids = set()
    for f in ("data.js", "data_bible_extra.js", "data_christian_figures.js"):
        ids |= set(re.findall(r'"([a-z]{3}_\d{3})":\s*\{', open(os.path.join(ROOT, f), encoding="utf-8").read()))
    import build_dictionary as bd
    from christmas_data import SCRIPTS
    import build_verse as bv
    from book_key_verses import BOOK_KEY
    have = {d["ref"] for d in bv.build_data()}
    verses = len(have) + sum(1 for b, (c, v) in BOOK_KEY.items() if f"{b} {c}:{v}" not in have)
    guides = len([d for d in glob.glob(os.path.join(ROOT, "guide", "*", "index.html"))])
    return [
        (len(ids), "성경 가로세로 퍼즐", "/list.html"),
        (len(bd.ENTRIES), "성경사전 항목", "/dictionary/"),
        (guides, "성경공부 가이드 글", "/guide/"),
        (verses, "말씀 뽑기 구절", "/verse/"),
        (len(json.load(open(os.path.join(ROOT, "cards_plan.json"), encoding="utf-8"))), "말씀 카드 샘플", "/cards/"),
        (len(json.load(open(os.path.join(ROOT, "verse", "studio_photos.json"), encoding="utf-8"))["photos"]), "무료 라이선스 배경 사진", "/verse/"),
        (len(SCRIPTS), "성탄 성극·스킷 대본", "/christmas/"),
        (len(glob.glob(os.path.join(ROOT, "christmas", "activities", "*.pdf"))) - 1, "성탄 활동지(PDF)", "/christmas/activities.html"),
    ]


def block():
    today = datetime.date.today().isoformat()
    cells = "".join(f'<a href="{u}" style="display:block;background:#fff;border:1px solid #d6e4f7;border-radius:14px;padding:14px 10px;text-align:center;text-decoration:none"><b style="display:block;font-size:26px;color:#0b5cad">{n:,}</b><span style="font-size:13.5px;color:#445">{lab}</span></a>' for n, lab, u in count())
    return (f'{S}\n<div class="section"><h2>숫자로 보는 십자가로세로</h2>'
            f'<p>저장소에 실제로 들어 있는 자료를 세어 적었습니다(기준일 {today}). 해설과 사전 내용은 <a href="/editorial-policy.html">콘텐츠 제작 원칙</a>을 따르고, 수정 내역은 <a href="/feedback/">검수·수정 이력</a>에 공개합니다.</p>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0">{cells}</div></div>\n{E}')


def main():
    p = os.path.join(ROOT, "about.html")
    s = open(p, encoding="utf-8").read()
    b = block()
    if S in s:
        s = re.sub(re.escape(S) + r".*?" + re.escape(E), lambda m: b, s, flags=re.S)
    else:
        k = s.index('  <div class="section">\n    <h2>십자가로세로란?</h2>')
        s = s[:k] + b + "\n" + s[k:]
    open(p, "w", encoding="utf-8").write(s)
    print("통계 블록 갱신")


if __name__ == "__main__":
    main()
