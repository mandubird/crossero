# -*- coding: utf-8 -*-
"""바울 관련 페이지에 넣는 '달려가노라' 순례 게임 배너(외부 사이트)."""
from html import escape

URL = "https://dallyeoganora.vercel.app/"

# 사전 항목 슬러그 → 배너 문구 변형
PAUL_ENTRY_SLUGS = {
    "paul", "pauls-conversion", "stephen", "antioch", "ephesus", "damascus", "rome", "jerusalem",
    "book-acts", "book-romans", "book-1-corinthians", "book-2-corinthians", "book-galatians", "book-ephesians",
    "book-philippians", "book-colossians", "book-1-thessalonians", "book-2-thessalonians",
    "book-1-timothy", "book-2-timothy", "book-titus", "book-philemon",
}
# 바울 서신 구절 페이지(verse/<book>-<c>-<v>.html)
PAUL_VERSE_PREFIXES = ("romans-", "1-corinthians-", "2-corinthians-", "galatians-", "ephesians-", "philippians-",
                       "colossians-", "1-thessalonians-", "2-thessalonians-", "1-timothy-", "2-timothy-", "titus-", "philemon-")

_TEXT = {
    "default": ("바울과 함께 순례자의 길 가보기?", "달려가노라 — 바울·실라와 2차 전도여행 길을 하루 한 걸음씩 걷는 순례 게임"),
    "route2": ("바로 이 2차 전도여행 길, 직접 걸어 볼까요?", "달려가노라 — 빌립보에서 고린도까지, 하루 한 걸음씩 도시마다 순례 여권에 도장을 찍어요"),
    "place": ("이 도시에 바울과 함께 가 보기?", "달려가노라 — 바울·실라와 전도여행 길을 걸으며 도시마다 순례 여권 도장을 모아요"),
    "verse": ("바울이 걸은 길을 함께 걸어 보기?", "달려가노라 — 이 말씀을 쓴 바울과 함께 하루 한 걸음씩 걷는 순례 게임"),
}


def banner(slug, variant="default"):
    title, sub = _TEXT.get(variant, _TEXT["default"])
    href = f"{URL}?utm_source=crossero&amp;utm_medium=banner&amp;utm_campaign={escape(slug)}"
    return (f'<a class="pilgrim" href="{href}" target="_blank" rel="noopener" data-ga="pilgrim_banner_click" data-ga-label="{escape(slug)}" '
            'style="display:flex;align-items:center;gap:14px;margin:26px 0;padding:16px 18px;border-radius:16px;text-decoration:none;'
            'background:linear-gradient(135deg,#7c2d12,#c2410c 55%,#f59e0b);color:#fff;box-shadow:0 6px 18px rgba(194,65,12,.25)">'
            '<span style="font-size:34px;line-height:1">🚶</span>'
            '<span style="flex:1;min-width:0"><b style="display:block;font-size:17px;line-height:1.4">' + escape(title) + '</b>'
            '<span style="display:block;font-size:13px;opacity:.92;line-height:1.5;margin-top:2px">' + escape(sub) + '</span></span>'
            '<span style="background:#fff;color:#9a3412;font-weight:700;font-size:13px;padding:8px 14px;border-radius:20px;white-space:nowrap">순례 시작 →</span></a>')
