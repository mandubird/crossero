# -*- coding: utf-8 -*-
"""책 항목 딕셔너리 생성 헬퍼. 같은 이름 접두어를 가진 퍼즐을 자동으로 연결한다."""
import os
import re

from bible_book_info import BOOK_INFO

ROOT = os.path.dirname(os.path.abspath(__file__))


def _puzzle_titles():
    titles = {}
    for f in ("data.js", "data_bible_extra.js", "data_christian_figures.js"):
        s = open(os.path.join(ROOT, f), encoding="utf-8").read()
        for m in re.finditer(r'"([a-z]{3}_\d{3})":\s*\{\s*title:\s*"([^"]+)"', s):
            titles[m.group(1)] = m.group(2)
    return titles


_TITLES = _puzzle_titles()


def book(name, slug_en, testament, group, chapters, author, theme, refs, overview, flow, msg, faq, related):
    puzzles = sorted(i for i, t in _TITLES.items() if t.startswith(name + ":"))
    count = f"{chapters}편" if name == "시편" else (f"{chapters}장")
    return {
        "slug": f"book-{slug_en}", "type": "성경 책", "name": name, "sub": theme,
        "testament": testament, "group": group,
        "summary": overview,
        "facts": [("구분", f"{testament} · {group}"), ("분량", count), ("저자", author), ("핵심 주제", theme)],
        "sections": [("내용의 흐름", [flow]),
                     ("주요 사건과 주제", [f"{name}에서 특히 눈여겨볼 사건과 주제는 " + ", ".join(BOOK_INFO[name]["events"]) + "입니다. 이 가운데 하나를 골라 먼저 읽고 전체 흐름으로 돌아가면 책의 구조가 훨씬 쉽게 보입니다."]),
                     ("핵심 메시지와 읽는 법", [msg])],
        "refs": refs, "faq": faq, "related": related, "puzzles": puzzles,
    }
