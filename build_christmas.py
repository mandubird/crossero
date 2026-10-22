# -*- coding: utf-8 -*-
"""성탄 성극 허브(/christmas/), 준비 가이드, 대본 페이지."""
import json
import os

from christmas_data import SCRIPTS
from verse_lib import KO_BOOKS, load_text

CSS = """<style>
.cx-card{display:block;background:#fff;border:1px solid #e5e5e5;border-radius:14px;padding:14px 16px;margin:10px 0;text-decoration:none!important;color:#222!important}
.cx-card:hover{border-color:#c2410c}.cx-card b{font-size:16px}.cx-card em{font-style:normal;font-size:12px;color:#9a3412;margin-left:6px}
.cx-card span{display:block;font-size:13.5px;color:#556;margin-top:4px;line-height:1.6}
.cx-meta{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:12px 0}.cx-meta div{background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:8px 12px;font-size:14px}
.cx-meta b{display:block;font-size:12px;color:#9a3412}
.script{background:#fff;border:1px solid #e5e5e5;border-radius:14px;padding:6px 16px;margin:14px 0}
.ln{display:flex;gap:10px;padding:9px 0;border-bottom:1px dashed #eee;line-height:1.7}.ln:last-child{border-bottom:0}
.ln .sp{flex:0 0 92px;font-weight:700;color:#9a3412;font-size:14px}.ln .tx{flex:1;font-size:15px}
.ln.dir .sp{color:#7b8794}.ln.dir .tx{color:#7b8794;font-style:italic}.fic{color:#c2410c;font-size:12px;margin-left:3px}
.btnrow{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.pbtn{border:0;background:#c2410c;color:#fff;font-weight:700;border-radius:20px;padding:9px 18px;cursor:pointer;font-size:14px;font-family:inherit}
.note2{font-size:13px;color:#7b6a58;background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:10px 14px;margin:12px 0;line-height:1.7}
@media(max-width:600px){.ln{flex-direction:column;gap:2px}.ln .sp{flex:none}}
@media print{.nav,.subnav,footer,.site-more,.peek,.pg-side,.pg-pill,.btnrow,.fbbox,.crumb,.support-band,.fnav{display:none!important}body{background:#fff}.script{border:0}}
</style>"""

AGE_GROUPS = [("유치부·유년부", ["first-christmas", "annunciation", "little-shepherd"]), ("초등부", ["bethlehem-inn", "shepherds-night", "wise-men", "simeon-anna"]),
              ("청소년·청년·장년·가정", ["reading-luke2", "reading-matthew2", "interview"])]
GUIDE_FAQ = [
    ("성탄 연극 대본이나 스킷드라마로도 쓸 수 있나요?", "네. 성극 대본은 성탄 연극 대본으로 그대로 쓸 수 있습니다. 짧은 순서가 필요하면 5분짜리 '첫 성탄 이야기'를 스킷처럼 올리고, 시간이 있으면 목자·박사 이야기 같은 초등부 대본을 쓰세요."),
    ("성탄절 성극은 언제부터 준비하면 되나요?", "보통 공연 4주 전에 대본을 정하고, 3주 전 배역을 확정해 읽기 연습을 시작하며, 1주 전에 의상과 소품을 포함한 리허설을 하면 여유 있게 마칠 수 있습니다."),
    ("대본을 외우기 어려운 어린이는 어떻게 하나요?", "대사가 한두 줄인 역을 맡기거나 해설이 읽어 주는 방식으로 진행하고, 낭독극 대본을 활용하면 외우지 않고도 참여할 수 있습니다."),
    ("성경에 없는 상상 대사를 넣어도 되나요?", "연극적 재미를 위해 가능하지만, 성경 본문과 구별하는 것이 좋습니다. 이 사이트의 대본은 상상 대사를 ✱ 표시로 구분했습니다."),
    ("소품은 무엇을 준비하나요?", "구유(작은 상자), 아기 인형, 목자 지팡이, 별 막대, 천 의상 정도면 충분합니다. 각 대본 페이지에 소품 목록이 있습니다."),
]


def _faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def _faq_html(esc, faq):
    return '<h2>자주 묻는 질문</h2><div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</div>"


PROPS_FAQ = [
    ("성탄 성극 소품 도안은 무료인가요?", "네, 모든 도안은 무료 A4 PDF로 받아 인쇄할 수 있습니다. 교회·주일학교·가정에서 비상업적으로 쓰시면 됩니다."),
    ("소품 도안은 어떤 종이에 인쇄하나요?", "A4 용지에 배율 100%로 인쇄하세요. 왕관과 머리띠는 180g 이상 두꺼운 종이에 인쇄하면 튼튼합니다."),
    ("어떤 소품이 있나요?", "별, 동방 박사 왕관, 양 머리띠, 천사 날개와 후광, 구유와 아기 예수님, 선물 상자, 배역 이름표, 성극 안내 포스터 도안이 있습니다."),
    ("성탄 성극 대본과 함께 쓸 수 있나요?", "네, 각 성극 대본 페이지의 준비물 목록에서 해당 소품 도안으로 바로 이동할 수 있습니다."),
]
ACTS_FAQ = [
    ("성탄 활동지는 무료인가요?", "네, 색칠 공부·미로·낱말 찾기·빈칸 채우기·순서 카드·OX 퀴즈 활동지를 A4 PDF로 무료로 받아 인쇄할 수 있습니다."),
    ("정답도 함께 있나요?", "미로, 낱말 찾기, 빈칸 채우기, OX 퀴즈는 정답 쪽이 함께 들어 있습니다. 교사용으로 따로 보관하세요."),
    ("어느 연령에 맞나요?", "색칠 공부와 순서 맞추기 카드는 유치부·유년부, 미로와 낱말 찾기는 초등, 빈칸 채우기와 OX 퀴즈는 초등 고학년·청소년에게 맞습니다."),
    ("성탄 예배에서 어떻게 쓰나요?", "성극 연습 전후 대기 시간이나 성탄 공과 복습 활동으로 10~20분 안에 쓸 수 있습니다. 성극 대본과 소품 도안도 함께 활용해 보세요."),
]


def _script_faq(s):
    return [
        (f"{s['title']}은 몇 분짜리 성극인가요?", f"약 {s['minutes']}분이며 대상은 {s['age']}, 인원은 {s['cast_n']}입니다."),
        ("필요한 소품은 무엇인가요?", ", ".join(s["props"]) + " 소품 도안은 성극 소품 도안 페이지에서 인쇄할 수 있습니다."),
        ("어떤 성경 본문을 바탕으로 하나요?", ", ".join(r for r, _ in s["refs"]) + " 본문을 바탕으로 했습니다."),
        ("인쇄해서 써도 되나요?", "교회·주일학교·가정에서의 비상업적 사용은 자유롭게 인쇄해 쓰셔도 됩니다. 판매나 재배포는 하지 말아 주세요."),
    ]


def _cast_chips(esc, cast):
    return " ".join(f'<span style="display:inline-block;background:#f1f6ff;border-radius:14px;padding:3px 11px;margin:3px 3px 3px 0;font-size:14px">{esc(c)}</span>' for c in cast)


def render_all(ctx):
    head, esc, FOOTER, SITE, ROOT_OUT, BY_SLUG = (ctx[k] for k in ("head", "esc", "FOOTER", "SITE", "OUT", "BY_SLUG"))
    out_dir = os.path.join(os.path.dirname(ROOT_OUT), "christmas")
    os.makedirs(out_dir, exist_ok=True)
    text = load_text()
    bidx = {b: i + 1 for i, b in enumerate(KO_BOOKS)}
    by_slug = {s["slug"]: s for s in SCRIPTS}

    def tail():
        return FOOTER + '\n<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n'

    # ----- 허브
    path = "/christmas/"
    title = "성탄절 성극 대본 · 성탄 연극 대본 - 성탄 발표회, 어린이 주일학교 | 십자가로세로"
    desc = "성탄절 성극·성탄 연극·성탄 발표회 대본 10편(유치부·초등부·청소년·가정 낭독극)과 준비 가이드, 소품 도안, 성탄 활동지를 무료로 제공합니다. 교회와 주일학교에서 인쇄해 쓸 수 있는 성경 기반 어린이 성극 대본입니다."
    faq = GUIDE_FAQ + [("이 대본은 어디서 가져온 건가요?", "십자가로세로가 직접 작성했거나 저작권이 만료된 개역한글 성경 본문을 그대로 사용한 대본입니다. 다른 사이트의 대본을 옮긴 것이 아닙니다."),
                       ("교회에서 인쇄해서 써도 되나요?", "교회·주일학교·가정에서의 비상업적 사용은 자유롭게 인쇄해 쓰셔도 됩니다. 판매나 재배포는 하지 말아 주세요.")]
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "성탄절 성극 대본 모음", "description": desc, "inLanguage": "ko", "url": SITE + path,
         "hasPart": [{"@type": "CreativeWork", "name": s["title"], "url": f"{SITE}/christmas/{s['slug']}.html"} for s in SCRIPTS]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}))
    out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › 성탄 성극</div>')
    out.append('<h1>🎭 성탄절 성극 대본 모음</h1><div class="sub">크리스마스 성극, 이렇게 준비해 보세요</div>')
    out.append('<div class="summary">성탄절 성극 대본 10편을 연령별로 모았습니다. 모두 성경 본문을 바탕으로 십자가로세로가 직접 작성했거나 개역한글 본문을 그대로 낭독하도록 구성했습니다. 교회 주일학교와 가정 예배에서 인쇄해 사용하세요.</div>')
    out.append('<a class="cta" href="/christmas/guide.html" data-ga="christmas_guide">📋 성극 준비 가이드 보기<small>일정, 배역, 소품, 무대, 연습 팁 한눈에</small></a>')
    out.append('<a class="cta" href="/christmas/puzzles.html" style="background:linear-gradient(135deg,#7c3aed,#5b21b6)" data-ga="christmas_puzzles">🧩 성탄 가로세로 퍼즐<small>탄생·목자·박사·마리아와 요셉·상식 퍼즐 온라인으로 풀기</small></a>')
    out.append('<a class="cta" href="/christmas/activities.html" style="background:linear-gradient(135deg,#059669,#047857)" data-ga="christmas_acts">🎨 성탄 활동지 인쇄하기<small>색칠·미로·낱말 찾기·빈칸 채우기·OX 퀴즈 PDF 무료</small></a>')
    out.append('<a class="cta" href="/christmas/props.html" style="background:linear-gradient(135deg,#c2410c,#9a3412)" data-ga="christmas_props">✂️ 소품 도안 인쇄하기<small>별·왕관·양 머리띠·천사 날개·구유 등 A4 PDF 무료</small></a>')
    for gname, slugs in AGE_GROUPS:
        out.append(f'<h2>{gname}</h2>')
        for sl in slugs:
            s = by_slug[sl]
            out.append(f'<a class="cx-card" href="/christmas/{sl}.html" data-ga="christmas_script" data-ga-label="{sl}"><b>{esc(s["title"])}</b><em>{s["minutes"]}분 · {esc(s["cast_n"])}</em><span>{esc(s["sub"])} — {esc(s["summary"][:70])}…</span></a>')
    out.append('<div class="note2">✱ 표시는 성경에 없는 상상 대사입니다. 성경 본문과 구별해 소개해 주세요. 대본은 교회·주일학교·가정에서 비상업적으로 인쇄해 쓰실 수 있고, 판매나 재배포는 하지 말아 주세요.</div>')
    out.append('<h2>함께 보면 좋은 자료</h2><div class="cards">'
               '<a class="card" href="/verse/christmas/"><b>⭐ 성탄 말씀 뽑기</b><span>성탄 말씀 카드와 인쇄</span></a>'
               '<a class="card" href="/dictionary/map/jesus-birth.html"><b>🗺️ 예수님 탄생과 유년기 경로</b><span>나사렛에서 베들레헴까지</span></a>'
               '<a class="card" href="/dictionary/birth-of-jesus.html"><b>예수님의 탄생</b><span>사건 해설</span></a>'
               '<a class="card" href="/dictionary/bethlehem.html"><b>베들레헴</b><span>오늘의 위치와 사진</span></a></div>')
    out.append('<h2>자주 묻는 질문</h2><div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</div>")
    out.append("</main>")
    out.append(tail())
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write("\n".join(out))

    # ----- 가이드
    path = "/christmas/guide.html"
    title = "성탄절 성극 준비 가이드 - 일정·배역·소품·연습 방법 | 십자가로세로"
    desc = "성탄절 성극을 처음 준비하는 교사를 위한 가이드. 4주 일정, 배역 정하기, 소품 체크리스트, 무대 배치, 연습 팁과 시간표 예시를 정리했습니다."
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "HowTo", "name": "성탄절 성극 준비하는 방법", "description": desc, "inLanguage": "ko",
         "step": [{"@type": "HowToStep", "name": "4주 전: 대본 선택", "text": "참여 인원과 연령, 공연 시간에 맞는 대본을 고릅니다."},
                  {"@type": "HowToStep", "name": "3주 전: 배역 확정과 읽기 연습", "text": "배역을 정하고 대본을 소리 내어 읽습니다."},
                  {"@type": "HowToStep", "name": "2주 전: 동선 연습", "text": "등장과 퇴장, 서는 위치를 연습합니다."},
                  {"@type": "HowToStep", "name": "1주 전: 리허설", "text": "의상과 소품을 갖추고 전체 리허설을 합니다."},
                  {"@type": "HowToStep", "name": "공연 당일", "text": "순서와 시간을 확인하고 응원하며 마무리합니다."}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in GUIDE_FAQ]}))
    out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/christmas/">성탄 성극</a> › 준비 가이드</div>')
    out.append('<h1>📋 성탄절 성극 준비 가이드</h1><div class="sub">처음 준비하는 선생님을 위한 순서</div>')
    out.append('<div class="summary">성극은 대본보다 준비 순서가 성패를 좌우합니다. 아래 순서대로 하면 부담을 줄이고 어린이들이 즐겁게 참여할 수 있습니다.</div>')
    sections = [
        ("1. 4주 일정 예시", ["<b>4주 전</b> 대본 선택과 예배 순서 안에서의 시간 확인", "<b>3주 전</b> 배역 확정, 대본 읽기 연습(소리 내어 2~3회)", "<b>2주 전</b> 등장·퇴장과 서는 위치 연습", "<b>1주 전</b> 의상·소품을 갖춘 전체 리허설", "<b>공연 당일</b> 마이크·조명·소품 점검 후 시작 전 기도"]),
        ("2. 배역 정하기", ["대사가 많은 역(해설)은 읽기에 자신 있는 어린이나 교사에게 맡깁니다.", "대사가 적거나 없는 역(양, 별, 박사 보조)을 두면 모든 아이가 참여할 수 있습니다.", "연령이 낮을수록 한 장면에 한두 줄만 맡기고 모두가 함께하는 마지막 장면을 만듭니다."]),
        ("3. 소품 체크리스트", ["구유와 아기 인형(작은 종이 상자와 수건으로 대체 가능)", "목자 지팡이, 양 머리띠, 별 모양 막대", "마리아·요셉·목자·박사 의상(천과 스카프로 간단히)", "선물 상자 세 개(황금·유향·몰약)", "손전등 또는 반짝이는 조명(천사 등장)"]),
        ("4. 무대 배치", ["왼쪽에 구유(탄생 장면), 오른쪽에 들판(목자 장면)을 두면 동선이 자연스럽습니다.", "해설은 무대 옆 독서대에서 읽게 하면 연기하는 어린이가 부담이 줄어듭니다.", "천사는 가장 마지막에 높은 곳(계단 위)에서 등장하면 효과가 큽니다."]),
        ("5. 연습 팁", ["처음에는 대본을 보며 읽고, 두 번째부터 동작을 붙입니다.", "대사를 외우지 못해도 큰 글씨 대본을 들고 연기할 수 있게 합니다.", "마지막 장면은 모두가 함께 성탄 찬송을 부르며 마무리합니다."]),
        ("6. 시간표 예시(성탄 예배 20분)", ["성극 8~10분 + 찬양 5분 + 말씀 5분", "낭독극은 5~8분으로 가장 짧고 부담이 적습니다.", "준비 시간이 부족하면 '낭독극 + 찬양'으로 구성합니다."]),
    ]
    for h, items in sections:
        out.append(f"<h2>{esc(h)}</h2><ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")
    out.append('<p><a href="/christmas/props.html" data-ga="guide_to_props">✂️ 별·왕관·구유 등 <b>소품 도안(PDF)</b> 인쇄하기 →</a></p>')
    out.append('<h2>추천 대본</h2><div class="cards">' + "".join(
        f'<a class="card" href="/christmas/{s["slug"]}.html"><b>{esc(s["title"])}</b><span>{s["minutes"]}분 · {esc(s["age"])}</span></a>' for s in SCRIPTS[:6]) + '</div><p><a href="/christmas/">대본 전체 보기 →</a></p>')
    out.append('<h2>자주 묻는 질문</h2><div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in GUIDE_FAQ) + "</div>")
    out.append("</main>")
    out.append(tail())
    open(os.path.join(out_dir, "guide.html"), "w", encoding="utf-8").write("\n".join(out))

    # ----- 소품 도안 페이지
    PROPS = [
        ("star", "베들레헴의 별", "별 막대 만들기. 색칠해서 오려 막대에 붙이면 박사들을 이끄는 별이 됩니다.", ["first-christmas", "wise-men", "shepherds-night"]),
        ("crown", "동방 박사의 왕관 (3개)", "색칠해서 오리고 붙임 부분으로 머리 둘레에 맞춰 붙입니다.", ["wise-men", "first-christmas", "reading-matthew2"]),
        ("sheep", "양 머리띠와 귀", "흰 솜이나 휴지를 붙여 양의 귀를 꾸미는 도안입니다.", ["shepherds-night", "little-shepherd", "first-christmas"]),
        ("angel", "천사 날개와 후광", "날개 한 쌍과 후광 머리띠 도안입니다.", ["annunciation", "shepherds-night", "first-christmas"]),
        ("manger", "구유와 아기 예수님", "구유를 접어 세우고 아기 포대기를 오려 올려 놓는 도안입니다.", ["bethlehem-inn", "first-christmas", "simeon-anna"]),
        ("gifts", "동방 박사의 선물 상자", "황금·유향·몰약 상자 세 개를 색칠해 오려 선물로 사용합니다.", ["wise-men", "reading-matthew2"]),
        ("nametags", "배역 이름표", "10개 대본에 나오는 모든 배역의 이름표입니다. 오려서 목걸이처럼 겁니다.", [s["slug"] for s in SCRIPTS]),
        ("poster", "성극 안내 포스터(빈칸 쓰기)", "제목, 일시, 장소, 참여자를 직접 써서 교회 게시판에 붙이는 포스터입니다.", []),
    ]
    path = "/christmas/props.html"
    title = "성탄 성극 소품 도안 - 별·왕관·양 머리띠·천사 날개·구유 인쇄 PDF | 십자가로세로"
    desc = "성탄 성극에 필요한 소품 도안을 A4 PDF로 무료 제공합니다. 별, 동방 박사 왕관, 양 머리띠, 천사 날개와 후광, 구유와 아기 예수님, 선물 상자, 배역 이름표, 안내 포스터."
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "성탄 성극 소품 도안", "description": desc, "inLanguage": "ko", "url": SITE + path,
         "hasPart": [{"@type": "CreativeWork", "name": n, "url": f"{SITE}/christmas/props/{k}.pdf", "encodingFormat": "application/pdf", "isAccessibleForFree": True} for k, n, _, _ in PROPS]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "성탄 성극", "item": SITE + "/christmas/"},
            {"@type": "ListItem", "position": 3, "name": "소품 도안", "item": SITE + path}]},
        _faq_ld(PROPS_FAQ)))
    out = [head(title, desc, path, ld, f"{SITE}/images/christmas/props-star.png").replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/christmas/">성탄 성극</a> › 소품 도안</div>')
    out.append('<h1>✂️ 성탄 성극 소품 도안</h1><div class="sub">인쇄해서 색칠하고 오리면 바로 쓰는 A4 도안</div>')
    out.append('<div class="summary">별, 왕관, 양 머리띠, 천사 날개, 구유, 선물 상자, 배역 이름표, 안내 포스터 도안입니다. 두꺼운 종이(180g 이상)에 인쇄하면 튼튼하고, 어린이들이 직접 색칠하면 성극 준비 시간이 신앙 활동이 됩니다.</div>')
    out.append('<a class="cta" href="/christmas/props/all.pdf" target="_blank" data-ga="christmas_props_all">📥 전체 도안 한 번에 받기 (PDF 10쪽)<small>모든 소품을 한 파일로 인쇄</small></a>')
    for k, n, d_, slugs in PROPS:
        used = "".join(f'<a href="/christmas/{sl}.html" style="margin-right:8px">{esc(by_slug[sl]["title"])}</a>' for sl in slugs[:3])
        out.append(f'<div class="cx-card" style="display:flex;gap:14px;align-items:flex-start;cursor:default"><img src="/images/christmas/props-{k}.png" alt="{esc(n)} 도안 미리보기" loading="lazy" width="120" style="width:120px;height:auto;border:1px solid #eee;border-radius:8px;flex:none;background:#fff">'
                   f'<div><b>{esc(n)}</b><span>{esc(d_)}</span>' + (f'<span style="margin-top:6px;font-size:12.5px">쓰는 대본: {used}</span>' if used else "") +
                   f'<span style="margin-top:8px"><a href="/christmas/props/{k}.pdf" target="_blank" data-ga="christmas_props_download" data-ga-label="{k}" style="font-weight:700;color:#c2410c">📥 PDF 받기</a></span></div></div>')
    out.append('<div class="note2">모든 도안은 십자가로세로가 만들었으며, 교회·주일학교·가정에서 비상업적으로 인쇄해 쓸 수 있습니다. 판매나 재배포는 하지 말아 주세요.</div>')
    out.append('<h2>인쇄 팁</h2><ul><li>A4 용지, 배율 100%(실제 크기)로 인쇄하세요.</li><li>점선은 오리는 선입니다. 어린이는 가위질을 어른이 도와주세요.</li><li>왕관과 머리띠는 머리 둘레에 맞춰 붙임 부분을 조절하세요.</li></ul>')
    out.append(_faq_html(esc, PROPS_FAQ))
    out.append("</main>")
    out.append(tail())
    open(os.path.join(out_dir, "props.html"), "w", encoding="utf-8").write("\n".join(out))

    # ----- 활동지 페이지
    ACTS = [
        ("coloring-stable", "색칠 공부 ① 구유의 아기 예수님", "마리아와 요셉, 구유, 별을 색칠합니다.", "유치부·유년부", False),
        ("coloring-shepherds", "색칠 공부 ② 들에서 만난 천사", "목자와 양, 천사와 별을 색칠합니다.", "유치부·유년부", False),
        ("coloring-kings", "색칠 공부 ③ 별을 따라온 박사들", "세 박사와 선물, 별을 색칠합니다.", "유치부·유년부", False),
        ("maze", "미로 · 아기 예수님께 가는 길", "목자가 구유까지 가는 길을 찾는 미로(정답 쪽 포함).", "유년부·초등", True),
        ("wordsearch", "낱말 찾기 · 성탄 낱말 14개", "예수, 마리아, 베들레헴 등 숨은 낱말 찾기(정답 쪽 포함).", "초등", True),
        ("cloze", "빈칸 채우기 · 누가복음 2:8-14", "개역한글 본문의 핵심 낱말을 채웁니다(정답 쪽 포함).", "초등 고학년·청소년", True),
        ("sequence", "이야기 순서 맞추기 카드", "6장의 카드를 오려 탄생 이야기를 순서대로 놓습니다.", "유년부·초등", False),
        ("ox-quiz", "성탄 OX 퀴즈 10문제", "성경 구절 출처가 달린 정답 쪽이 포함된 퀴즈입니다.", "초등·청소년", True),
    ]
    path = "/christmas/activities.html"
    title = "성탄 활동지 · 크리스마스 주일학교 활동지 - 색칠 공부·미로·낱말 찾기 무료 PDF | 십자가로세로"
    desc = "성탄 주일학교 활동지를 A4 PDF로 무료 제공합니다. 크리스마스 색칠 공부, 미로, 낱말 찾기, 누가복음 빈칸 채우기, 이야기 순서 카드, OX 퀴즈(정답 포함)."
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "성탄 활동지", "description": desc, "inLanguage": "ko", "url": SITE + path,
         "hasPart": [{"@type": "LearningResource", "name": n, "url": f"{SITE}/christmas/activities/{k}.pdf", "encodingFormat": "application/pdf", "isAccessibleForFree": True, "audience": {"@type": "Audience", "audienceType": a}} for k, n, _, a, _ in ACTS]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "성탄 성극", "item": SITE + "/christmas/"},
            {"@type": "ListItem", "position": 3, "name": "활동지", "item": SITE + path}]},
        _faq_ld(ACTS_FAQ)))
    out = [head(title, desc, path, ld, f"{SITE}/images/christmas/act-maze.png").replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/christmas/">성탄 성극</a> › 활동지</div>')
    out.append('<h1>🎨 성탄 활동지 모음</h1><div class="sub">색칠하고, 찾고, 풀어 보는 성탄 활동 8종</div>')
    out.append('<div class="summary">성탄 예배 전후 10~20분 활동으로 쓰기 좋은 활동지입니다. 연령에 맞춰 골라 인쇄하고, 정답이 있는 활동지는 정답 쪽이 함께 들어 있습니다(교사용으로 따로 보관하세요).</div>')
    out.append('<a class="cta" href="/christmas/activities/all.pdf" target="_blank" data-ga="christmas_acts_all">📥 활동지 전체 한 번에 받기 (PDF 12쪽)<small>색칠 3종 · 미로 · 낱말 찾기 · 빈칸 채우기 · 순서 카드 · OX 퀴즈</small></a>')
    for k, n, d_, age, ans in ACTS:
        out.append(f'<div class="cx-card" style="display:flex;gap:14px;align-items:flex-start;cursor:default"><img src="/images/christmas/act-{k}.png" alt="{esc(n)} 활동지 미리보기" loading="lazy" width="120" style="width:120px;height:auto;border:1px solid #eee;border-radius:8px;flex:none;background:#fff">'
                   f'<div><b>{esc(n)}</b><em>{esc(age)}</em><span>{esc(d_)}</span><span style="margin-top:8px"><a href="/christmas/activities/{k}.pdf" target="_blank" data-ga="christmas_acts_download" data-ga-label="{k}" style="font-weight:700;color:#c2410c">📥 PDF 받기' + (" (정답 포함)" if ans else "") + '</a></span></div></div>')
    out.append('<div class="note2">모든 활동지는 십자가로세로가 만들었으며 교회·주일학교·가정에서 비상업적으로 인쇄해 쓸 수 있습니다. 성경 본문은 저작권이 만료된 개역한글판입니다. 판매나 재배포는 하지 말아 주세요.</div>')
    out.append('<h2>활용 팁</h2><ul><li><b>유치부</b>: 색칠 공부와 순서 맞추기 카드(교사가 읽어 주기)</li><li><b>초등 저학년</b>: 미로, 낱말 찾기</li><li><b>초등 고학년·청소년</b>: 빈칸 채우기와 OX 퀴즈를 소그룹 대항전으로</li><li>성극 연습 전후 대기 시간에 활용하면 좋습니다. <a href="/christmas/">성극 대본</a>·<a href="/christmas/props.html">소품 도안</a>과 함께 쓰세요.</li></ul>')
    out.append(_faq_html(esc, ACTS_FAQ))
    out.append("</main>")
    out.append(tail())
    open(os.path.join(out_dir, "activities.html"), "w", encoding="utf-8").write("\n".join(out))

    # ----- 성탄 퍼즐 허브
    from build_dictionary import TITLES
    PZ = [("xms_001", "아기 예수님의 탄생", "쉬움", "마리아·요셉·베들레헴·구유 등 탄생 이야기의 핵심 낱말"),
          ("xms_002", "목자와 천사", "쉬움", "누가복음 2장 8~20절의 목자, 천사, 구주, 평화"),
          ("xms_003", "동방 박사와 별", "쉬움", "마태복음 2장의 박사, 별, 황금·유향·몰약, 헤롯"),
          ("xms_004", "마리아와 요셉", "보통", "수태 고지부터 성전 봉헌, 열두 살 예수님까지"),
          ("xms_005", "성탄 상식 종합", "보통", "임마누엘, 메시아, 구레뇨, 대림절 등 성탄 상식"),
          ("mat_071", "마태복음: 왕의 탄생", "쉬움", "마태복음이 전하는 예수님의 탄생"),
          ("lif_135", "예수님의 생애: 탄생과 유년기", "쉬움", "탄생에서 소년 시절까지"),
          ("mic_064", "미가: 베들레헴의 통치자", "보통", "베들레헴에서 나실 통치자의 예언")]
    PZ = [x for x in PZ if x[0] in TITLES]
    path = "/christmas/puzzles.html"
    title = "성탄 퍼즐 - 크리스마스 성경 가로세로 낱말 퍼즐 모음 | 십자가로세로"
    desc = "크리스마스와 성탄을 주제로 한 성경 가로세로 낱말 퍼즐 모음입니다. 아기 예수님의 탄생, 목자와 천사, 동방 박사, 마리아와 요셉, 성탄 상식을 온라인으로 풀어 보세요."
    faq = [("성탄 퍼즐은 무료인가요?", "온라인에서 풀이하는 것은 무료입니다. 정답 확인과 인쇄 기능은 후원자에게 제공됩니다."),
           ("어떤 연령에 맞나요?", "쉬움 표시 퍼즐은 초등 중학년부터, 보통 표시 퍼즐은 초등 고학년·청소년·성인에게 맞습니다. 난이도(가볍게·보통·어렵게)를 직접 고를 수 있습니다."),
           ("성탄 퍼즐을 한꺼번에 풀 수 있나요?", "'성탄 퍼즐 전체 통합'을 누르면 성탄 관련 모든 낱말이 섞인 큰 퍼즐이 만들어집니다."),
           ("예배나 공과 시간에는 어떻게 쓰나요?", "성극 연습 전후 대기 시간이나 성탄 공과 복습 활동으로 10분 안팎에 풀 수 있습니다. 성극 대본과 활동지와 함께 사용하세요.")]
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "성탄 퍼즐 모음", "description": desc, "inLanguage": "ko", "url": SITE + path,
         "hasPart": [{"@type": "CreativeWork", "name": t, "url": f"{SITE}/play.html?id={k}", "learningResourceType": "가로세로 낱말 퍼즐"} for k, t, _, _ in PZ]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}))
    out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/christmas/">성탄 성극</a> › 성탄 퍼즐</div>')
    out.append('<h1>🧩 성탄 퍼즐 모음</h1><div class="sub">크리스마스 가로세로 낱말 퍼즐로 배우는 성탄 이야기</div>')
    out.append('<div class="summary">아기 예수님의 탄생부터 목자와 천사, 동방 박사까지, 성탄 이야기를 낱말 퍼즐로 풀어 보세요. 힌트는 성경 본문에 근거해 만들었고, 풀면서 성탄 이야기를 다시 읽게 됩니다.</div>')
    out.append('<a class="cta" href="/play.html?category=성탄" data-ga="christmas_puzzle_all">🎄 성탄 퍼즐 전체 통합 풀기<small>성탄 관련 모든 낱말이 섞인 큰 퍼즐 (어렵게)</small></a>')
    out.append("<h2>주제별 성탄 퍼즐</h2>")
    for k, t, lv, d_ in PZ:
        out.append(f'<a class="cx-card" href="/play.html?id={k}" data-ga="christmas_puzzle" data-ga-label="{k}"><b>{esc(t)}</b><em>{lv}</em><span>{esc(d_)} — 퍼즐 풀기 →</span></a>')
    out.append('<h2>함께 쓰면 좋은 자료</h2><div class="cards"><a class="card" href="/christmas/"><b>🎭 성탄 성극 대본</b><span>10편</span></a><a class="card" href="/christmas/activities.html"><b>🎨 성탄 활동지</b><span>색칠·미로·퀴즈</span></a><a class="card" href="/christmas/props.html"><b>✂️ 소품 도안</b><span>별·왕관·구유</span></a><a class="card" href="/verse/christmas/"><b>⭐ 성탄 말씀 뽑기</b><span>말씀 카드</span></a></div>')
    out.append('<h2>자주 묻는 질문</h2><div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</div>")
    out.append("</main>")
    out.append(tail())
    open(os.path.join(out_dir, "puzzles.html"), "w", encoding="utf-8").write("\n".join(out))

    # ----- 대본 페이지
    from feedback_box import box as _fb
    for s in SCRIPTS:
        path = f"/christmas/{s['slug']}.html"
        title = f"성탄절 성극 대본 · {s['title']} ({s['minutes']}분, {s['age']}) | 십자가로세로"
        desc = f"{s['title']} - {s['summary']}"[:150]
        rows = []
        if "reading" in s:
            for sp, book, c, v1, v2 in s["reading"]:
                body = " ".join(text[(bidx[book], c, v)] for v in range(v1, v2 + 1) if (bidx[book], c, v) in text)
                rows.append(f'<div class="ln"><span class="sp">{esc(sp)}</span><span class="tx">{esc(body)} <span style="color:#9aa5b1;font-size:12px">({esc(book)} {c}:{v1}' + (f"-{v2}" if v2 != v1 else "") + ')</span></span></div>')
        else:
            for ln in s["lines"]:
                sp, tx = ln[0], ln[1]
                fic = len(ln) > 2 and ln[2] is True
                cls = "ln dir" if sp == "지문" else "ln"
                rows.append(f'<div class="{cls}"><span class="sp">{esc(sp)}</span><span class="tx">{esc(tx)}' + ('<span class="fic">✱</span>' if fic else "") + "</span></div>")
        ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
            {"@context": "https://schema.org", "@type": "CreativeWork", "name": s["title"], "description": s["summary"], "inLanguage": "ko", "learningResourceType": "성극 대본",
             "audience": {"@type": "Audience", "audienceType": s["age"]}, "timeRequired": f"PT{s['minutes']}M", "isAccessibleForFree": True,
             "author": {"@type": "Organization", "name": "십자가로세로"}, "url": SITE + path},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "성탄 성극", "item": SITE + "/christmas/"},
                {"@type": "ListItem", "position": 3, "name": s["title"], "item": SITE + path}]},
            _faq_ld(_script_faq(s))))
        out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
        out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/christmas/">성탄 성극</a> › {esc(s["title"])}</div>')
        out.append(f'<h1>🎭 {esc(s["title"])}</h1><div class="sub">{esc(s["sub"])}</div>')
        out.append(f'<div class="summary">{esc(s["summary"])}</div>')
        out.append(f'<div class="cx-meta"><div><b>대상</b>{esc(s["age"])}</div><div><b>소요 시간</b>약 {s["minutes"]}분</div><div><b>인원</b>{esc(s["cast_n"])}</div><div><b>성경 본문</b>{esc(", ".join(r for r, _ in s["refs"]))}</div></div>')
        out.append('<div class="btnrow"><button class="pbtn" onclick="window.print()" data-ga="christmas_print">🖨️ 대본 인쇄하기</button></div>')
        out.append("<h2>등장 인물</h2><p>" + _cast_chips(esc, s["cast"]) + "</p>")
        out.append("<h2>준비물</h2><ul>" + "".join(f"<li>{esc(p)}</li>" for p in s["props"]) + '</ul><p><a href="/christmas/props.html" data-ga="script_to_props">✂️ 별·왕관·구유 등 소품 도안(PDF) 인쇄하기 →</a> · <a href="/christmas/props/nametags.pdf" target="_blank">배역 이름표 PDF</a></p>')
        out.append("<h2>대본</h2>")
        if "reading" in s:
            out.append('<div class="note2">성경 본문(개역한글)을 그대로 나누어 읽는 낭독극입니다. 배역별로 맡은 부분만 소리 내어 읽습니다.</div>')
        elif any((len(l) > 2 and l[2] is True) for l in s["lines"]):
            out.append('<div class="note2">✱ 표시는 성경에 없는 상상 대사입니다. 공연 전에 성경 본문과 상상 부분을 구별해 소개해 주세요.</div>')
        out.append('<div class="script">' + "".join(rows) + "</div>")
        out.append("<h2>연습 팁</h2><ul><li>처음에는 대본을 보며 소리 내어 읽고, 두 번째부터 동작을 붙입니다.</li><li>대사가 어려운 어린이는 해설이 대신 읽어 주어도 됩니다.</li><li>마지막은 모두가 함께 성탄 찬송으로 마무리합니다.</li></ul>")
        out.append("<h2>함께 읽을 성경</h2><ul>" + "".join(f"<li><b>{esc(r)}</b> — {esc(n)}</li>" for r, n in s["refs"]) + "</ul>")
        rel = [x for x in s["related"] if x in BY_SLUG]
        out.append("<h2>함께 보면 좋은 사전 항목</h2><div class=\"cards\">" + "".join(
            f'<a class="card" href="/dictionary/{x}.html"><b>{esc(BY_SLUG[x]["name"])}</b><span>{esc(BY_SLUG[x]["sub"])}</span></a>' for x in rel) + "</div>")
        others = [o for o in SCRIPTS if o["slug"] != s["slug"]][:4]
        out.append("<h2>다른 성극 대본</h2><div class=\"cards\">" + "".join(
            f'<a class="card" href="/christmas/{o["slug"]}.html"><b>{esc(o["title"])}</b><span>{o["minutes"]}분 · {esc(o["age"])}</span></a>' for o in others) + '</div><p><a href="/christmas/">대본 전체 보기 →</a> · <a href="/christmas/guide.html">준비 가이드</a></p>')
        out.append('<div class="note2">이 대본은 십자가로세로가 작성했습니다. 교회·주일학교·가정에서 비상업적으로 인쇄해 사용하실 수 있고, 판매나 재배포는 하지 말아 주세요. 성경 본문은 저작권이 만료된 개역한글판입니다.</div>')
        out.append(_fb("../christmas/" + s["slug"], s["title"], False))
        out.append(_faq_html(esc, _script_faq(s)))
        out.append("</main>")
        out.append(tail())
        open(os.path.join(out_dir, f"{s['slug']}.html"), "w", encoding="utf-8").write("\n".join(out))
    return ["index", "guide", "props", "activities", "puzzles"] + [s["slug"] for s in SCRIPTS]
