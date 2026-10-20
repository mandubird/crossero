# -*- coding: utf-8 -*-
"""사이트 공용 메뉴·서브메뉴·푸터·'계속 둘러보기'. 모든 HTML에 같은 구조를 적용한다(멱등).
사용: python3 site_chrome.py"""
import glob
import os
import re

NAV_ITEMS = [  # (key, label, href)
    ("home", "홈", "/index.html"),
    ("puzzle", "퍼즐", "/list.html"),
    ("dict", "성경사전", "/dictionary/"),
    ("map", "성경지도", "/dictionary/map/"),
    ("teacher", "교사허브", "/teachers/"),
    ("today", "오늘의 말씀", "/today/"),
]

# 성경사전 분류 (type, 폴더, 칩 라벨, 아이콘, 설명)
CATS = [
    ("지명", "places", "성경 지명", "📍", "예루살렘, 베들레헴, 갈릴리 바다… 오늘의 위치와 사진까지"),
    ("인물", "people", "성경 인물", "👤", "아브라함, 모세, 다윗, 바울… 삶과 핵심 구절"),
    ("사건", "events", "성경 사건", "📜", "천지창조, 출애굽, 십자가와 부활… 흐름으로 이해"),
    ("신앙 용어", "terms", "신앙 용어", "✝️", "구원, 은혜, 칭의, 성령… 쉬운 말로 풀이"),
    ("성경 책", "books", "66권 요약", "📚", "창세기부터 요한계시록까지 책별 핵심 요약"),
]
TYPE2CAT = {c[0]: c for c in CATS}

ACTIVE_RULES = [  # (경로 접두어/이름, key) 위에서부터 첫 일치
    ("index.html", "home"), ("dictionary/map/", "map"), ("christmas/", "today"), ("dictionary/", "dict"),
    ("play.html", "puzzle"), ("play2.html", "puzzle"), ("list.html", "puzzle"), ("posts/", "puzzle"),
    ("bible-crossword", "puzzle"), ("how-to-crossword", "puzzle"),
    ("today/", "today"), ("verse/new-year/guide", "guide"), ("verse/", "today"), ("guide/", "guide"),
    ("teachers/", "teacher"), ("sunday-school", "teacher"), ("church-bulletin", "teacher"),
]

FOOT_COLS = [
    ("성경사전", [("📍 성경 지명", "/dictionary/places/"), ("👤 성경 인물", "/dictionary/people/"), ("📜 성경 사건", "/dictionary/events/"),
                 ("✝️ 신앙 용어", "/dictionary/terms/"), ("📚 66권 요약", "/dictionary/books/"), ("⏳ 연대표", "/dictionary/timeline/"), ("👪 가계도", "/dictionary/genealogy/"), ("📖 구절로 찾기", "/dictionary/verses/"), ("🗺️ 성경 지도", "/dictionary/map/")]),
    ("말씀·묵상", [("📘 성경공부 가이드", "/guide/"), ("오늘의 말씀", "/today/"), ("말씀 뽑기", "/verse/"), ("🎭 성탄 성극 대본", "/christmas/"), ("✂️ 성극 소품 도안", "/christmas/props.html"), ("🎨 성탄 활동지", "/christmas/activities.html"), ("🧩 성탄 퍼즐", "/christmas/puzzles.html"), ("새해 말씀 뽑기", "/verse/new-year/"), ("송구영신 진행 가이드", "/verse/new-year/guide/"),
                 ("성탄 말씀 뽑기", "/verse/christmas/"), ("추수감사 말씀 뽑기", "/verse/thanksgiving/")]),
    ("퍼즐·교사 자료", [("퍼즐 목록", "/list.html"), ("퍼즐 게시판", "/posts/index.html"), ("성경 십자말풀이", "/bible-crossword.html"),
                   ("십자말풀이 하는 법", "/how-to-crossword.html"), ("교사 허브", "/teachers/"), ("주일학교 자료", "/sunday-school-materials.html"),
                   ("교회·주일학교 활용", "/church-bulletin-puzzle.html")]),
    ("십자가로세로", [("서비스 소개", "/about.html"), ("후원하기", "/support.html"), ("⭐ 후원자", "/supporters.html"), ("FAQ", "/faq.html"),
                  ("콘텐츠 제작 원칙", "/editorial-policy.html"), ("검수·의견 보내기", "/feedback/"), ("이용약관", "/terms.html"), ("개인정보처리방침", "/privacy.html"),
                  ("문의", "mailto:mandubird@naver.com")]),
]

MORE = [  # key, 아이콘, 제목, 설명, href
    ("puzzle", "🧩", "성경 퍼즐", "말씀을 가로세로로 풀어요", "/list.html"),
    ("dict", "📖", "성경사전", "인물·사건·지명·용어 한눈에", "/dictionary/"),
    ("map", "🗺️", "성경 지도", "지명이 지금은 어디에?", "/dictionary/map/"),
    ("teacher", "🧑‍🏫", "교사 허브", "주일학교 자료 모음", "/teachers/"),
    ("today", "📅", "오늘의 말씀", "매일 새로운 한 구절", "/today/"),
    ("guide", "📘", "성경공부 가이드", "읽는 법·구약 흐름·본문 해설", "/guide/"),
]
SUPPORT = ("support", "💝", "후원하기", "무료로 운영되는 이 사역을 응원해 주세요", "/support.html")

CSS = """
:root{--w-read:820px;--w-col:780px;--w-wide:1100px}
.crumb a{display:inline-block;padding:8px 4px;margin:-8px -4px}
.fnav a{padding-top:7px!important;padding-bottom:7px!important}
.nav{position:sticky;top:0;z-index:100;display:flex!important;justify-content:center;gap:4px!important;flex-wrap:nowrap!important;overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nav .nav-item{flex:0 0 auto;padding:11px 15px!important;font-size:15px!important}
@media (max-width:640px){.nav{justify-content:space-between!important;gap:0!important;padding:2px 4px!important}.nav .nav-item{padding:11px 5px!important;font-size:13px!important}}
.subnav{background:#fff;border-bottom:1px solid #e5e5e5}
.subnav-in{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;padding:10px 12px;max-width:var(--w-read);margin:0 auto}
.sn-chip{flex:0 0 auto;padding:6px 11px;border-radius:16px;border:1px solid #d6e2f1;background:#f5f9ff;color:#33506e!important;font-size:13px;text-decoration:none!important;white-space:nowrap}
.sn-chip:hover{background:#e6f0ff}
@media (min-width:641px){.subnav-in{display:grid;grid-template-columns:repeat(5,1fr);gap:6px 8px}.sn-chip{text-align:center}}
@media (max-width:640px){.subnav-in{gap:5px;padding:8px 8px}.sn-chip{padding:5px 9px;font-size:12.5px}}
.sn-chip.on{background:#0073e6;border-color:#0073e6;color:#fff!important;font-weight:700}
.site-more{max-width:var(--w-read);margin:34px auto 8px;padding:0 16px}
.site-more h2{font-size:16px;margin:0 0 10px;color:#334}
.sm-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.sm-card{display:block;background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px 12px;text-decoration:none!important;color:#222!important}
.sm-card:hover{border-color:#0073e6;background:#f5f9ff}
.sm-card b{display:block;font-size:14px}
.sm-card span{display:block;font-size:12px;color:#667;margin-top:2px;line-height:1.4}
.fnav{display:grid;grid-template-columns:repeat(4,1fr);gap:18px 14px;max-width:var(--w-read);margin:0 auto 16px;padding:0 16px;text-align:left}
.fnav h3{font-size:13px;color:#334;margin:0 0 8px}
.fnav a{display:block;font-size:13px;color:#666;text-decoration:none;padding:4px 0}
.fnav a:hover{color:#0073e6}
.vsb{max-width:var(--w-col);margin:6px auto 22px;text-align:left}
.vsb-h{font-weight:800;font-size:17px;color:#0b3d73;margin-bottom:10px;display:flex;align-items:center;justify-content:center;gap:6px 8px;flex-wrap:wrap;text-align:center}.vsb-h span{font-weight:500;font-size:13px;color:#667}
.vsb-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.vsb-c{position:relative;display:flex;flex-direction:column;align-items:center;gap:3px;padding:18px 8px 14px;background:var(--g,#0b5cad);color:#fff;border-radius:16px;text-decoration:none;text-align:center;box-shadow:0 6px 16px rgba(0,0,0,.16);transition:transform .15s}
.vsb-c:hover{transform:translateY(-3px)}
.vsb-c i{font-style:normal;font-size:30px;line-height:1.1}.vsb-c b{font-size:16px}.vsb-c span{font-size:12px;opacity:.92;line-height:1.4}
.vsb-c em{position:absolute;top:-9px;right:10px;font-style:normal;background:#ffd43b;color:#5b4a00;font-size:11px;font-weight:800;padding:2px 9px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,.2)}
@media(max-width:560px){.vsb-row{gap:7px}.vsb-c{padding:14px 4px 11px}.vsb-c b{font-size:13.5px}.vsb-c span{font-size:11.5px}.vsb-c i{font-size:26px}.vsb-h{font-size:15px}}
.wrap{max-width:var(--w-read)!important}
@media (max-width:640px){.playinfo{max-width:calc(100% - 20px)!important;box-sizing:border-box!important}}
.home-hub{max-width:var(--w-col);margin:0 auto 22px}
.home-hub h2{font-size:18px;margin:6px 0 10px;text-align:center}
.hh-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.hh-card{display:block;background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:14px 8px;text-align:center;text-decoration:none!important;color:#222!important}
.hh-card:hover{border-color:#0073e6;background:#f5f9ff}
.hh-card i{display:block;font-style:normal;font-size:26px;margin-bottom:4px}
.hh-card b{display:block;font-size:14px}
.hh-card span{display:block;font-size:11.5px;color:#667;margin-top:2px}
.support-band{background:linear-gradient(135deg,#0073e6,#0052cc);color:#fff;margin:40px 0 0;padding:44px 20px;text-align:center}.support-band h2{color:#fff;font-size:22px;margin:0 0 10px}.support-band p{margin:0 0 20px;font-size:15px;line-height:1.8;opacity:.95}.sb-btn{display:inline-block;background:#fff;color:#0059d6!important;font-weight:700;font-size:16px;padding:13px 30px;border-radius:30px;text-decoration:none!important;box-shadow:0 4px 14px rgba(0,0,0,.18)}.sb-btn:hover{transform:translateY(-1px)}
.explore{max-width:820px;margin:28px auto 0;padding:18px 16px;background:#fff;border:1px solid #e5e7eb;border-radius:16px}
.explore h2{font-size:18px;margin:0 0 6px}.ex-g{margin:14px 0 0}.ex-g h3{font-size:15px;margin:0 0 6px;display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.ex-more{font-size:13px;font-weight:500;color:#0073e6;display:inline-block;padding:9px 4px;margin:-9px -4px}.ex-l{display:flex;flex-wrap:wrap;gap:8px 8px}
.ex-l a{background:#f5f9ff;border:1px solid #d6e2f1;border-radius:18px;padding:8px 13px;font-size:13.5px;line-height:1.3;color:#33506e;text-decoration:none}
.ex-l a:hover{background:#e6f0ff}
.puzzle-zone{background:#eaf3ff;border:2px solid #bcd6f7;border-radius:22px;padding:16px 14px 18px;margin:26px auto;max-width:860px}
.pz-label{display:inline-block;background:#0073e6;color:#fff;font-weight:700;font-size:13px;padding:5px 12px;border-radius:14px;margin-bottom:8px}
.pg-side{display:none}
.pg-pill{display:none}
@media (min-width:1280px){
.pg-side{display:block;position:fixed;left:max(14px,calc(50% - 410px - 176px));top:150px;width:150px;z-index:80;background:linear-gradient(160deg,#fff7ed,#ffedd5);border:1px solid #fdba74;border-radius:16px;padding:12px 10px 12px;text-align:center;box-shadow:0 6px 18px rgba(154,52,18,.15)}
.pg-side a{display:block;text-decoration:none;color:#7c2d12}
.pg-side img{width:84px;height:auto;image-rendering:pixelated;display:block;margin:0 auto 6px}
.pg-side b{display:block;font-size:14px;line-height:1.4}
.pg-side span{display:block;font-size:11.5px;color:#9a3412;margin:4px 0 8px;line-height:1.4}
.pg-side i{display:block;font-style:normal;font-weight:700;font-size:12.5px;background:#c2410c;color:#fff;border-radius:14px;padding:6px 0}
.pg-x{position:absolute;right:4px;top:2px;border:0;background:none;font-size:18px;line-height:1;color:#9a3412;cursor:pointer;padding:2px 6px}
}
@media (max-width:1279px){
.pg-pill{display:flex;align-items:center;gap:8px;position:fixed;left:12px;bottom:14px;z-index:80;background:#fff7ed;border:1px solid #fdba74;border-radius:26px;padding:5px 14px 5px 6px;text-decoration:none;color:#7c2d12;font-size:13px;font-weight:700;box-shadow:0 4px 14px rgba(0,0,0,.18);transform:translateY(90px);opacity:0;transition:transform .45s ease,opacity .45s ease}
.pg-pill.on{transform:none;opacity:1}
.pg-pill img{width:34px;height:auto;image-rendering:pixelated;display:block}
.pg-side{display:none!important}
}
.peek{position:fixed;right:0;top:112px;z-index:90;display:flex;align-items:flex-end;text-decoration:none!important;transform:translateX(0);animation:peek-in 7s ease-in-out infinite}
.peek img{width:62px;height:auto;display:block;margin-right:-8px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.25))}
.peek-b{background:#fff;color:#c2410c;border:2px solid #fdba74;border-radius:14px 14px 0 14px;padding:6px 10px;font-size:13px;font-weight:800;margin-bottom:34px;box-shadow:0 3px 10px rgba(0,0,0,.15);white-space:nowrap;animation:peek-blink 1.6s ease-in-out infinite}
.peek-x{position:absolute;left:-6px;top:-8px;width:20px;height:20px;border-radius:50%;border:0;background:#556;color:#fff;font-size:12px;line-height:20px;padding:0;cursor:pointer;opacity:.0}
.peek:hover .peek-x,.peek:focus-within .peek-x{opacity:.85}
@keyframes peek-in{0%,12%{transform:translateX(105%)}22%,78%{transform:translateX(0)}90%,100%{transform:translateX(105%)}}
@keyframes peek-blink{0%,100%{opacity:1}50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){.peek{animation:none}.peek-b{animation:none}}
@media (max-width:640px){.peek{top:auto;bottom:16px}.peek img{width:46px}.peek-b{font-size:12px;padding:5px 8px;margin-bottom:26px}}
@media (max-width:640px){.sm-grid,.hh-grid{grid-template-columns:repeat(2,1fr)}.fnav{grid-template-columns:repeat(2,1fr)}}
"""


def active_key(path):
    for pre, key in ACTIVE_RULES:
        if path.startswith(pre):
            return key
    return None


def nav_html(key):
    rows = [f'  <a href="{h}" class="nav-item{" nav-active" if k == key else ""}">{t}</a>' for k, t, h in NAV_ITEMS]
    return '<nav class="nav">\n' + "\n".join(rows) + "\n</nav>"


def subnav_html(path, s):
    on = None
    if path == "dictionary/map/index.html" or path.startswith("dictionary/map/"):
        on = "map"
    elif path == "dictionary/index.html":
        on = "all"
    elif path.startswith("dictionary/verses/"):
        on = "verses"
    elif path.startswith("dictionary/timeline/"):
        on = "timeline"
    elif path.startswith("dictionary/genealogy/"):
        on = "genealogy"
    else:
        m = re.match(r"dictionary/(places|people|events|terms|books)/index\.html$", path)
        if m:
            on = m.group(1)
        else:
            b = re.search(r'<span class="badge">([^<]+)</span>', s)
            if b and b.group(1) in TYPE2CAT:
                on = TYPE2CAT[b.group(1)][1]
    chips = [("all", "전체", "/dictionary/")] + [(c[1], f"{c[3]} {c[2]}", f"/dictionary/{c[1]}/") for c in CATS] + [("timeline", "⏳ 연대표", "/dictionary/timeline/"), ("genealogy", "👪 가계도", "/dictionary/genealogy/"), ("verses", "📖 구절로 찾기", "/dictionary/verses/"), ("map", "🗺️ 성경 지도", "/dictionary/map/")]
    a = "".join(f'<a class="sn-chip{" on" if k == on else ""}" href="{h}">{t}</a>' for k, t, h in chips)
    return f'<!--SUBNAV--><div class="subnav"><div class="subnav-in">{a}</div></div><!--/SUBNAV-->'


def footer_html():
    cols = "".join(
        f'<div><h3>{h}</h3>' + "".join(f'<a href="{u}">{t}</a>' for t, u in links) + "</div>" for h, links in FOOT_COLS)
    return f'<!--FL--><nav class="fnav" aria-label="사이트 전체 메뉴">{cols}</nav>{ALIGN_JS}<!--/FL-->'


ALIGN_JS = ('<script>(function(){var m=document.querySelector("main")||document.querySelector(".container,.section");if(!m)return;'
            'function a(){var c=getComputedStyle(m),w=m.getBoundingClientRect().width-parseFloat(c.paddingLeft)-parseFloat(c.paddingRight),on=w>280&&innerWidth>640,cap=m.classList.contains("vwrap")?780:99999;'
            'document.querySelectorAll(".site-more,.fnav,.playinfo").forEach(function(e){var pi=e.classList.contains("playinfo");'
            'if(on){e.style.boxSizing="border-box";e.style.maxWidth=Math.min(w,cap)+"px";if(!pi)e.style.padding="0"}'
            'else{e.style.maxWidth="";e.style.boxSizing="";if(!pi)e.style.padding=""}})}'
            'a();addEventListener("resize",a)})();</script>')


def more_html(key, path=""):
    if key == "home":  # 홈은 위 허브와 겹치므로 전폭 후원 띠 한 장만
        return ('<!--MORE--><section class="support-band"><div class="sb-in"><h2>🙏 이 사역을 함께해 주세요</h2>'
                '<p>십자가로세로는 개인 사역으로 무료 운영됩니다.<br>작은 응원이 새 퍼즐과 자료가 됩니다.</p>'
                '<a class="sb-btn" href="/support.html" data-ga="more_click" data-ga-label="support_band">후원하고 함께하기</a></div></section><!--/MORE-->')
    cards = [m for m in MORE if m[0] != key][:3]
    if key != "support" and not path.startswith(("support", "supporters", "sponsor")):
        cards.append(SUPPORT)
    else:
        cards = [m for m in MORE if m[0] != key][:4]
    g = "".join(f'<a class="sm-card" href="{h}" data-ga="more_click" data-ga-label="{k}"><b>{i} {t}</b><span>{d}</span></a>' for k, i, t, d, h in cards)
    return f'<!--MORE--><section class="site-more"><h2>계속 둘러보기</h2><div class="sm-grid">{g}</div></section><!--/MORE-->'


def season_html():
    import build_verse as bv
    return bv.season_banner()


def hub_html():
    cards = [("🧩", "퍼즐 풀기", "가로세로 낱말 퍼즐", "/list.html"), ("📍", "성경 지명", "오늘의 위치와 사진", "/dictionary/places/"),
             ("👤", "성경 인물", "삶과 핵심 구절", "/dictionary/people/"), ("📜", "성경 사건", "흐름으로 이해", "/dictionary/events/"),
             ("🗺️", "성경 지도", "지명이 지금은?", "/dictionary/map/"), ("🧑‍🏫", "교사 허브", "주일학교 자료", "/teachers/"),
             ("📅", "오늘의 말씀", "매일 새로운 구절", "/today/"), ("🎴", "말씀 뽑기", "내게 주시는 말씀", "/verse/")]
    g = "".join(f'<a class="hh-card" href="{h}" data-ga="home_hub_click" data-ga-label="{t}"><i>{ic}</i><b>{t}</b><span>{d}</span></a>' for ic, t, d, h in cards)
    return f'<!--HUB--><section class="home-hub">{season_html()}<h2>무엇을 찾으세요?</h2><div class="hh-grid">{g}</div></section><!--/HUB-->'


def explore_html():
    from build_dictionary import BY_SLUG
    from build_routes import ROUTES
    from timeline_data import ERAS
    groups = [
        ("📍 성경 지명", "/dictionary/places/", ["jerusalem", "bethlehem", "nazareth", "jordan-river", "sea-of-galilee", "capernaum", "jericho", "mount-sinai", "babylon", "rome", "ephesus", "damascus", "corinth", "patmos"]),
        ("👤 성경 인물", "/dictionary/people/", ["abraham", "moses", "david", "paul", "jesus", "peter", "elijah", "daniel", "esther", "ruth", "mary", "john-apostle", "isaiah", "joseph"]),
        ("📜 성경 사건", "/dictionary/events/", ["creation", "the-flood", "red-sea-crossing", "ten-commandments", "david-and-goliath", "birth-of-jesus", "crucifixion", "resurrection", "pentecost", "babylonian-exile", "feeding-the-five-thousand", "last-supper"]),
    ]
    rows = []
    for title, more, slugs in groups:
        links = " ".join(f'<a href="/dictionary/{s}.html">{BY_SLUG[s]["name"]}</a>' for s in slugs if s in BY_SLUG)
        rows.append(f'<div class="ex-g"><h3>{title} <a class="ex-more" href="{more}">전체 보기 →</a></h3><div class="ex-l">{links}</div></div>')
    rows.append('<div class="ex-g"><h3>🎭 성탄 성극 <a class="ex-more" href="/christmas/">대본 전체 보기 →</a></h3><div class="ex-l"><a href="/christmas/">성탄절 성극 대본 10편</a> <a href="/christmas/guide.html">성극 준비 가이드</a> <a href="/christmas/reading-luke2.html">누가복음 2장 낭독극</a> <a href="/verse/christmas/">성탄 말씀 뽑기</a></div></div>')
    rl = " ".join(f'<a href="/dictionary/map/{r["slug"]}.html">{r["short"]}</a>' for r in ROUTES)
    rows.append(f'<div class="ex-g"><h3>🗺️ 성경 지도·경로 <a class="ex-more" href="/dictionary/map/">지도 보기 →</a></h3><div class="ex-l">{rl}</div></div>')
    el = " ".join(f'<a href="/dictionary/timeline/{x["slug"]}.html">{x["name"]}</a>' for x in ERAS)
    rows.append(f'<div class="ex-g"><h3>⏳ 시대별 연대표 <a class="ex-more" href="/dictionary/timeline/">전체 보기 →</a></h3><div class="ex-l">{el} <a href="/dictionary/genealogy/">가계도</a> <a href="/dictionary/verses/">구절로 찾기</a></div></div>')
    return ('<!--EXPLORE--><section class="explore"><h2>성경 콘텐츠 둘러보기</h2>' + "".join(rows) + '</section><!--/EXPLORE-->')


def pilgrim_html():
    """'달려가노라' 순례 게임 노출: PC 왼쪽 옆면 카드(1280px 이상) + 모바일 하단 왼쪽 알약(스크롤 후)."""
    base = "https://dallyeoganora.vercel.app/?utm_source=crossero&utm_medium=%s&utm_campaign=%s"
    return ('<!--PILGRIM--><aside class="pg-side" id="pgSide" aria-label="바울과 함께 순례자의 길">'
            '<button class="pg-x" id="pgX" aria-label="닫기" type="button">×</button>'
            f'<a href="{base % ("side", "pc_left")}" target="_blank" rel="noopener" data-ga="pilgrim_side_click" data-ga-label="pc_left">'
            '<img src="/images/paul-face.png" alt="" width="84" height="92"><b>바울과 함께<br>순례자의 길</b><span>달려가노라 · 하루 한 걸음 순례 게임</span><i>순례 시작 →</i></a></aside>'
            f'<a class="pg-pill" id="pgPill" href="{base % ("float", "mobile_pill")}" target="_blank" rel="noopener" data-ga="pilgrim_side_click" data-ga-label="mobile_pill">'
            '<img src="/images/paul-face.png" alt="" width="34" height="37"><span>바울과 순례자의 길 →</span></a>'
            '<script>(function(){var s=document.getElementById("pgSide"),p=document.getElementById("pgPill");if(!s||!p)return;'
            'var off=false;try{off=!!sessionStorage.getItem("pgOff")}catch(e){}'
            'function hide(){off=true;try{sessionStorage.setItem("pgOff","1")}catch(e){}s.style.display="none";p.style.display="none"}'
            'document.getElementById("pgX").addEventListener("click",hide);'
            'if(off){hide();return}'
            'var shown=false;function chk(){var h=document.documentElement.scrollHeight-innerHeight;if(!shown&&h>0&&scrollY/h>0.3){shown=true;p.classList.add("on");removeEventListener("scroll",chk)}}'
            'addEventListener("scroll",chk,{passive:true});chk();})();</script><!--/PILGRIM-->')


def playinfo_html():
    return ('<!--PLAYINFO--><section class="playinfo" style="max-width:820px;margin:28px auto 0;padding:18px 18px;background:#fff;border:1px solid #e5e7eb;border-radius:14px;line-height:1.8;font-size:14.5px;color:#374151">'
            '<h2 style="font-size:17px;margin:0 0 8px">성경 가로세로 퍼즐 이용 안내</h2>'
            '<p style="margin:0 0 8px"><b>풀이 방법</b> 빈칸을 누르고 힌트를 읽은 뒤 글자를 입력합니다. 방향키로 칸을 옮기고 Backspace로 고칠 수 있으며, 모바일에서도 같은 방식으로 풉니다.</p>'
            '<p style="margin:0 0 8px"><b>난이도</b> 가볍게(5문항), 보통(12문항), 어렵게(25문항) 중에서 고를 수 있고, 초등 저학년은 가볍게, 청소년·성인은 보통 이상을 권합니다.</p>'
            '<p style="margin:0 0 8px"><b>정답 확인·인쇄</b> 정답 보기와 인쇄 기능은 후원자에게 제공되며, 퍼즐 풀이 자체는 무료입니다. 인쇄한 퍼즐은 주보나 주일학교 활동으로 쓸 수 있습니다.</p>'
            '<p style="margin:0"><b>함께 보면 좋은 곳</b> <a href="/list.html">퍼즐 목록</a> · <a href="/dictionary/">성경사전</a> · <a href="/dictionary/map/">성경 지도</a> · <a href="/teachers/">교사 허브</a> · <a href="/faq.html">자주 묻는 질문</a></p></section><!--/PLAYINFO-->')


def peek_html():
    # 위치: 메뉴(서브메뉴) 바닥 기준 오프셋. 페이지마다 본문 시작 높이가 달라 콘텐츠를 덜 가리도록 조정한다.
    return ('<!--PEEK--><a class="peek" id="crsPeek" href="/support.html" data-ga="peek_support_click" aria-label="후원하기">'
            '<span class="peek-b">후원 ❤️</span><img src="/images/mascot-peek.png" alt="" width="62" height="78"></a>'
            '<script>(function(){var e=document.getElementById("crsPeek");if(!e)return;'
            'try{if(sessionStorage.getItem("peekOff")){e.style.display="none";return}}catch(x){}'
            'function pos(){var sn=document.querySelector(".subnav"),nv=document.querySelector(".nav"),el=sn||nv;if(!el)return;'
            'var b=el.getBoundingClientRect().bottom,p=location.pathname,o=sn?22:(/^\\/(list|puzzle)/.test(p)?6:66);'
            'e.style.top=Math.max(48,b+o)+"px"}'
            'pos();window.addEventListener("resize",pos);window.addEventListener("load",pos)})();</script><!--/PEEK-->')


def _strip(s, tag):
    return re.sub(rf"<!--{tag}-->.*?<!--/{tag}-->\n?", "", s, flags=re.S)


ICONS = ('<!--ICONS--><link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/images/favicon-48.png">'
         '<link rel="icon" type="image/png" sizes="256x256" href="/images/favicon.png"><link rel="apple-touch-icon" href="/images/apple-touch-icon.png"><!--/ICONS-->')


def apply(path, s):
    key = active_key(path)
    # 파비콘(모든 페이지 동일하게: ico + png + 애플 터치 아이콘)
    s = re.sub(r'<link[^>]*rel="(?:shortcut )?icon"[^>]*>\n?', "", s)
    s = re.sub(r'<link[^>]*rel="apple-touch-icon"[^>]*>\n?', "", s)
    s = re.sub(r"<!--ICONS-->.*?<!--/ICONS-->\n?", "", s, flags=re.S)
    s = s.replace("</head>", ICONS + "\n</head>", 1)
    # 스타일
    s = re.sub(r'<style id="crs-chrome">.*?</style>\n?', "", s, flags=re.S)
    s = s.replace("</head>", f'<style id="crs-chrome">{CSS}</style>\n</head>', 1)
    # 메뉴 + 서브메뉴
    s = _strip(s, "SUBNAV")
    s = re.sub(r'<nav class="nav">.*?</nav>', lambda m: nav_html(key), s, count=1, flags=re.S)
    if path.startswith("dictionary/"):
        s = s.replace("</nav>", "</nav>\n" + subnav_html(path, s), 1)
    # 홈 허브
    s = _strip(s, "HUB")
    if path == "index.html":
        s = s.replace("<main>", "<main>\n" + hub_html(), 1)
    # 홈: 성경 콘텐츠 둘러보기(내부 링크)
    s = _strip(s, "EXPLORE")
    if path == "index.html" and "</main>" in s:
        s = s.replace("</main>", explore_html() + "\n</main>", 1)
    # 푸터
    f0 = s.find("<footer")
    if f0 < 0:
        return s
    f1 = s.find("</footer>", f0)
    foot = s[f0:f1]
    i = foot.find("만든 이유")
    if i >= 0:  # 예전 CTA 버튼 줄
        st = foot.rfind("<div", 0, i)
        en = foot.find("</div>", i)
        if st >= 0 and en >= 0 and "<div" not in foot[st + 4:en]:
            foot = foot[:st] + foot[en + 6:]
    legacy = None
    fm = re.search(r"<!--FL-->.*?<!--/FL-->\n?", foot, flags=re.S)
    if fm:
        legacy = fm.start()
        foot = foot[:fm.start()] + foot[fm.end():]
    rows = re.compile(r'[ \t]*<div class="footer-links"[^>]*>.*?</div>\n?', re.S)
    m = rows.search(foot)
    if m:
        if legacy is None:
            legacy = m.start()
        foot = rows.sub("", foot)
    elif legacy is None:  # 아주 오래된 게시글: 주일학교 자료 한 줄만 있는 푸터
        j = foot.find("sunday-school-materials.html")
        if j >= 0:
            st = foot.rfind("<div", 0, j)
            en = foot.find("</div>", j)
            if st >= 0 and en >= 0 and "<div" not in foot[st + 4:en]:
                legacy = st
                foot = foot[:st] + foot[en + 6:]
    block = footer_html() + "\n"
    if legacy is None:
        k = foot.find("<div class=\"footer-divider\"></div>")
        legacy = (k + len('<div class="footer-divider"></div>')) if k >= 0 else len("<footer>")
    foot = foot[:legacy] + block + foot[legacy:]
    s = s[:f0] + foot + s[f1:]
    # 퍼즐 화면 정적 이용 안내(얇은 JS 화면 보강)
    s = _strip(s, "PLAYINFO")
    if path == "play.html":
        f0 = s.find("<footer")
        if f0 > 0:
            s = s[:f0] + playinfo_html() + "\n" + s[f0:]
    # 우측 마스코트 후원 안내(게임 화면 제외)
    s = _strip(s, "PEEK")
    if not path.startswith(("play.html", "play2.html", "support.html")) and "</body>" in s:
        s = s.replace("</body>", peek_html() + "\n</body>", 1)
    # 달려가노라 순례 게임 카드(PC 왼쪽 옆면·모바일 알약, 게임·후원 화면 제외)
    s = _strip(s, "PILGRIM")
    if not path.startswith(("play.html", "play2.html", "support.html", "supporters.html", "sponsor.html")) and "</body>" in s:
        s = s.replace("</body>", pilgrim_html() + "\n</body>", 1)
    # 계속 둘러보기(푸터 바로 위, 게임 화면 제외)
    s = _strip(s, "MORE")
    if not path.startswith(("play.html", "play2.html")):
        f0 = s.find("<footer")
        s = s[:f0] + more_html(key, path) + "\n" + s[f0:]
    return s


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    n = 0
    for f in glob.glob(os.path.join(root, "**/*.html"), recursive=True):
        rel = os.path.relpath(f, root)
        if rel.startswith(("node_modules", "images")):
            continue
        s = open(f, encoding="utf-8").read()
        if '<nav class="nav">' not in s:
            continue
        t = apply(rel, s)
        if t != s:
            open(f, "w", encoding="utf-8").write(t)
            n += 1
    print(f"공용 메뉴·푸터 적용: {n}개 파일")


if __name__ == "__main__":
    main()
