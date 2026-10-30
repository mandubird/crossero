# -*- coding: utf-8 -*-
"""준비물 안내 블록(성극 소품·활동지·송구영신 카드 인쇄 페이지용).
기본은 네이버 쇼핑 검색 링크(제휴 아님). 쿠팡 파트너스에서 만든 짧은 링크(https://link.coupang.com/a/...)를
ITEMS의 'partner'에 넣으면 그 링크로 바뀌고, 광고 표시 문구가 자동으로 붙는다.
링크 만드는 순서(권장): 1) paper200 2) paper180 3) colorpencil 4) box 5) laminate 6) cutter 7) scissors 8) glue 9) headband 10) string
(카드 인쇄·활동지 준비는 용지와 색연필이 가장 많이 쓰이는 품목이라 앞에 둠). 링크 추가 후 python3 build_dictionary.py(성탄 페이지)와 python3 build_newyear_guide.py 실행."""
import html
import urllib.parse as up

ITEMS = {
    "paper180": {"label": "두꺼운 인쇄용지 A4 (180g 안팎)", "q": "A4 인쇄용지 180g", "partner": ""},
    "paper200": {"label": "카드용 두꺼운 종이 A4 (200g 안팎)", "q": "A4 두꺼운 종이 200g", "partner": ""},
    "colorpencil": {"label": "색연필·사인펜 세트", "q": "색연필 사인펜 세트 어린이", "partner": ""},
    "scissors": {"label": "어린이 안전 가위", "q": "어린이 안전 가위", "partner": ""},
    "glue": {"label": "풀·양면테이프", "q": "풀 양면테이프 문구", "partner": ""},
    "headband": {"label": "머리띠(소품 만들기용)", "q": "머리띠 만들기 키트", "partner": ""},
    "string": {"label": "이름표용 끈", "q": "이름표 목걸이 끈", "partner": ""},
    "laminate": {"label": "코팅 필름(라미네이팅)", "q": "라미네이팅 코팅필름 A4", "partner": ""},
    "cutter": {"label": "종이 재단기·커터", "q": "종이 재단기 A4", "partner": ""},
    "box": {"label": "말씀 상자(선물 상자·바구니)", "q": "선물 상자 바구니 소품", "partner": ""},
}


def shop_block(keys, title="준비물 구경하기"):
    rows, partner = [], False
    for k in keys:
        it = ITEMS[k]
        if it["partner"]:
            partner = True
            href, rel = it["partner"], "nofollow sponsored noopener"
        else:
            href, rel = "https://search.shopping.naver.com/search/all?query=" + up.quote(it["q"]), "nofollow noopener"
        rows.append(f'<li><a href="{html.escape(href)}" target="_blank" rel="{rel}" data-ga="shop_click" data-ga-label="{k}">{html.escape(it["label"])}</a></li>')
    note = ('<p style="font-size:12.5px;color:#7b6a58;margin:8px 0 0">이 목록의 일부 링크는 쿠팡 파트너스 활동의 일환으로, 구매 시 십자가로세로가 일정액의 수수료를 받을 수 있습니다(구매 가격은 같습니다).</p>'
            if partner else '<p style="font-size:12.5px;color:#7b6a58;margin:8px 0 0">편의를 위한 쇼핑 검색 링크이며 십자가로세로와 판매처는 관계가 없습니다.</p>')
    return (f'<h2>{html.escape(title)}</h2><div class="note2" style="background:#f7faff;border-color:#cfe0f5;color:#334"><ul style="margin:0;padding-left:20px;line-height:2">'
            + "".join(rows) + "</ul>" + note + "</div>")
