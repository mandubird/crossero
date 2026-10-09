# -*- coding: utf-8 -*-
"""게시글 → 성경사전 내부 링크 블록 생성. 신규 발행(auto_publish)과 기존 글 일괄 삽입(add_dictionary_links.py)이 함께 쓴다."""
import re
from html import escape

import build_dictionary as bd

MARK_START, MARK_END = "<!-- dict-links -->", "<!-- /dict-links -->"
BOOK_BY_NAME = {e["name"]: e for e in bd.BOOKS}
OTHERS = [e for e in bd.ENTRIES if e["type"] != "성경 책"]
ALIASES = {
    "red-sea-crossing": ["홍해"], "jericho-fall": ["여리고"], "ten-plagues": ["재앙", "유월절"],
    "sermon-on-the-mount": ["산상수훈", "산상 수훈", "팔복"], "pentecost": ["오순절", "성령의 임재", "성령 강림"],
    "jerusalem": ["예루살렘"], "bethlehem": ["베들레헴"], "mount-sinai": ["시내산"], "jordan-river": ["요단"],
    "john-the-baptist": ["세례 요한"], "abraham": ["아브라함"], "joseph": ["요셉"], "samson": ["삼손"],
}
ICON = {"인물": "👤", "사건": "📜", "지명": "📍", "성경 책": "📖"}


def _matches(entry, text):
    names = [entry["name"]] + ALIASES.get(entry["slug"], [])
    for n in names:
        if entry["slug"] == "ruth":
            if re.search(r"룻(?!기)", text):
                return True
        elif n in text:
            return True
    return False


def links_for(title, book, events_text="", limit=3):
    out = []
    b = BOOK_BY_NAME.get(book)
    if b:
        out.append((b["slug"], f"{ICON['성경 책']} {b['name']} 요약"))
    scored = []
    for e in OTHERS:
        if _matches(e, title):
            scored.append((2, e))
        elif events_text and _matches(e, events_text):
            scored.append((1, e))
    scored.sort(key=lambda x: -x[0])
    for _, e in scored[:limit]:
        out.append((e["slug"], f"{ICON[e['type']]} {e['name']}"))
    return out


def dict_links_html(title, book, events_text=""):
    items = links_for(title, book, events_text)
    cards = "".join(f'<a href="/dictionary/{s}.html" class="related-link">{escape(label)}</a>' for s, label in items)
    cards += '<a href="/dictionary/" class="related-link">🗂️ 성경사전 전체 보기</a>'
    return (f'{MARK_START}\n<section class="edu-section dict-links">\n<h3>📖 함께 읽으면 좋은 성경사전</h3>\n'
            f'<p>퍼즐을 풀기 전에 읽으면 힌트가 쉬워지고, 풀고 나서 읽으면 내용을 한 번 더 복습할 수 있습니다.</p>\n'
            f'<div class="related-grid">{cards}</div>\n</section>\n{MARK_END}\n')
