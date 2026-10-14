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
    ("index.html", "home"), ("dictionary/map/", "map"), ("dictionary/", "dict"),
    ("play.html", "puzzle"), ("play2.html", "puzzle"), ("list.html", "puzzle"), ("posts/", "puzzle"),
    ("bible-crossword", "puzzle"), ("how-to-crossword", "puzzle"),
    ("today/", "today"), ("verse/", "today"),
    ("teachers/", "teacher"), ("sunday-school", "teacher"), ("church-bulletin", "teacher"),
]

FOOT_COLS = [
    ("성경사전", [("📍 성경 지명", "/dictionary/places/"), ("👤 성경 인물", "/dictionary/people/"), ("📜 성경 사건", "/dictionary/events/"),
                 ("✝️ 신앙 용어", "/dictionary/terms/"), ("📚 66권 요약", "/dictionary/books/"), ("⏳ 연대표", "/dictionary/timeline/"), ("📖 구절로 찾기", "/dictionary/verses/"), ("🗺️ 성경 지도", "/dictionary/map/")]),
    ("말씀·묵상", [("오늘의 말씀", "/today/"), ("말씀 뽑기", "/verse/"), ("새해 말씀 뽑기", "/verse/new-year/"),
                 ("성탄 말씀 뽑기", "/verse/christmas/"), ("추수감사 말씀 뽑기", "/verse/thanksgiving/")]),
    ("퍼즐·교사 자료", [("퍼즐 목록", "/list.html"), ("퍼즐 게시판", "/posts/index.html"), ("성경 십자말풀이", "/bible-crossword.html"),
                   ("십자말풀이 하는 법", "/how-to-crossword.html"), ("교사 허브", "/teachers/"), ("주일학교 자료", "/sunday-school-materials.html"),
                   ("교회·주일학교 활용", "/church-bulletin-puzzle.html")]),
    ("십자가로세로", [("서비스 소개", "/about.html"), ("후원하기", "/support.html"), ("⭐ 후원자", "/supporters.html"), ("FAQ", "/faq.html"),
                  ("콘텐츠 제작 원칙", "/editorial-policy.html"), ("이용약관", "/terms.html"), ("개인정보처리방침", "/privacy.html"),
                  ("문의", "mailto:mandubird@naver.com")]),
]

MORE = [  # key, 아이콘, 제목, 설명, href
    ("puzzle", "🧩", "성경 퍼즐", "말씀을 가로세로로 풀어요", "/list.html"),
    ("dict", "📖", "성경사전", "인물·사건·지명·용어 한눈에", "/dictionary/"),
    ("map", "🗺️", "성경 지도", "지명이 지금은 어디에?", "/dictionary/map/"),
    ("teacher", "🧑‍🏫", "교사 허브", "주일학교 자료 모음", "/teachers/"),
    ("today", "📅", "오늘의 말씀", "매일 새로운 한 구절", "/today/"),
]
SUPPORT = ("support", "💝", "후원하기", "무료로 운영되는 이 사역을 응원해 주세요", "/support.html")

CSS = """
.nav{position:sticky;top:0;z-index:100;display:flex!important;justify-content:center;gap:4px!important;flex-wrap:nowrap!important;overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nav .nav-item{flex:0 0 auto;padding:11px 15px!important;font-size:15px!important}
@media (max-width:640px){.nav{justify-content:space-between!important;gap:0!important;padding:2px 4px!important}.nav .nav-item{padding:11px 5px!important;font-size:13px!important}}
.subnav{background:#fff;border-bottom:1px solid #e5e5e5}
.subnav-in{display:flex;gap:8px;overflow-x:auto;padding:10px 14px;max-width:820px;margin:0 auto;scrollbar-width:none}
.subnav-in::-webkit-scrollbar{display:none}
.sn-chip{flex:0 0 auto;padding:7px 13px;border-radius:18px;border:1px solid #d6e2f1;background:#f5f9ff;color:#33506e!important;font-size:13.5px;text-decoration:none!important;white-space:nowrap}
.sn-chip:hover{background:#e6f0ff}
.sn-chip.on{background:#0073e6;border-color:#0073e6;color:#fff!important;font-weight:700}
.site-more{max-width:820px;margin:34px auto 8px;padding:0 16px}
.site-more h2{font-size:16px;margin:0 0 10px;color:#334}
.sm-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.sm-card{display:block;background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px 12px;text-decoration:none!important;color:#222!important}
.sm-card:hover{border-color:#0073e6;background:#f5f9ff}
.sm-card b{display:block;font-size:14px}
.sm-card span{display:block;font-size:12px;color:#667;margin-top:2px;line-height:1.4}
.fnav{display:grid;grid-template-columns:repeat(4,1fr);gap:18px 14px;max-width:820px;margin:0 auto 16px;padding:0 16px;text-align:left}
.fnav h3{font-size:13px;color:#334;margin:0 0 8px}
.fnav a{display:block;font-size:13px;color:#666;text-decoration:none;padding:4px 0}
.fnav a:hover{color:#0073e6}
.home-hub{max-width:820px;margin:0 auto 22px}
.home-hub h2{font-size:18px;margin:6px 0 10px;text-align:center}
.hh-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.hh-card{display:block;background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:14px 8px;text-align:center;text-decoration:none!important;color:#222!important}
.hh-card:hover{border-color:#0073e6;background:#f5f9ff}
.hh-card i{display:block;font-style:normal;font-size:26px;margin-bottom:4px}
.hh-card b{display:block;font-size:14px}
.hh-card span{display:block;font-size:11.5px;color:#667;margin-top:2px}
.support-band{background:linear-gradient(135deg,#0073e6,#0052cc);color:#fff;margin:40px 0 0;padding:44px 20px;text-align:center}.support-band h2{color:#fff;font-size:22px;margin:0 0 10px}.support-band p{margin:0 0 20px;font-size:15px;line-height:1.8;opacity:.95}.sb-btn{display:inline-block;background:#fff;color:#0059d6!important;font-weight:700;font-size:16px;padding:13px 30px;border-radius:30px;text-decoration:none!important;box-shadow:0 4px 14px rgba(0,0,0,.18)}.sb-btn:hover{transform:translateY(-1px)}
.puzzle-zone{background:#eaf3ff;border:2px solid #bcd6f7;border-radius:22px;padding:16px 14px 18px;margin:26px auto;max-width:860px}
.pz-label{display:inline-block;background:#0073e6;color:#fff;font-weight:700;font-size:13px;padding:5px 12px;border-radius:14px;margin-bottom:8px}
.peek{position:fixed;right:0;top:112px;z-index:90;display:flex;align-items:flex-end;text-decoration:none!important;transform:translateX(0);animation:peek-in 7s ease-in-out infinite}
.peek img{width:62px;height:auto;display:block;margin-right:-8px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.25))}
.peek-b{background:#fff;color:#c2410c;border:2px solid #fdba74;border-radius:14px 14px 0 14px;padding:6px 10px;font-size:13px;font-weight:800;margin-bottom:34px;box-shadow:0 3px 10px rgba(0,0,0,.15);white-space:nowrap;animation:peek-blink 1.6s ease-in-out infinite}
.peek-x{position:absolute;left:-6px;top:-8px;width:20px;height:20px;border-radius:50%;border:0;background:#556;color:#fff;font-size:12px;line-height:20px;padding:0;cursor:pointer;opacity:.0}
.peek:hover .peek-x,.peek:focus-within .peek-x{opacity:.85}
@keyframes peek-in{0%,12%{transform:translateX(105%)}22%,78%{transform:translateX(0)}90%,100%{transform:translateX(105%)}}
@keyframes peek-blink{0%,100%{opacity:1}50%{opacity:.35}}
@media (prefers-reduced-motion:reduce){.peek{animation:none}.peek-b{animation:none}}
@media (max-width:640px){.peek{top:104px}.peek img{width:50px}.peek-b{font-size:12px;padding:5px 8px;margin-bottom:26px}}
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
    else:
        m = re.match(r"dictionary/(places|people|events|terms|books)/index\.html$", path)
        if m:
            on = m.group(1)
        else:
            b = re.search(r'<span class="badge">([^<]+)</span>', s)
            if b and b.group(1) in TYPE2CAT:
                on = TYPE2CAT[b.group(1)][1]
    chips = [("all", "전체", "/dictionary/")] + [(c[1], f"{c[3]} {c[2]}", f"/dictionary/{c[1]}/") for c in CATS] + [("timeline", "⏳ 연대표", "/dictionary/timeline/"), ("verses", "📖 구절로 찾기", "/dictionary/verses/"), ("map", "🗺️ 성경 지도", "/dictionary/map/")]
    a = "".join(f'<a class="sn-chip{" on" if k == on else ""}" href="{h}">{t}</a>' for k, t, h in chips)
    return f'<!--SUBNAV--><div class="subnav"><div class="subnav-in">{a}</div></div><!--/SUBNAV-->'


def footer_html():
    cols = "".join(
        f'<div><h3>{h}</h3>' + "".join(f'<a href="{u}">{t}</a>' for t, u in links) + "</div>" for h, links in FOOT_COLS)
    return f'<!--FL--><nav class="fnav" aria-label="사이트 전체 메뉴">{cols}</nav><!--/FL-->'


ALIGN_JS = ('<script>(function(){var s=document.querySelector(".site-more");var m=document.querySelector("main");if(!s||!m)return;'
            'function a(){var c=getComputedStyle(m),w=m.getBoundingClientRect().width-parseFloat(c.paddingLeft)-parseFloat(c.paddingRight);'
            'if(w>280&&innerWidth>640){s.style.maxWidth=w+"px";s.style.padding="0"}else{s.style.maxWidth="";s.style.padding=""}}'
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
    return f'<!--MORE--><section class="site-more"><h2>계속 둘러보기</h2><div class="sm-grid">{g}</div></section>{ALIGN_JS}<!--/MORE-->'


def hub_html():
    cards = [("🧩", "퍼즐 풀기", "가로세로 낱말 퍼즐", "/list.html"), ("📍", "성경 지명", "오늘의 위치와 사진", "/dictionary/places/"),
             ("👤", "성경 인물", "삶과 핵심 구절", "/dictionary/people/"), ("📜", "성경 사건", "흐름으로 이해", "/dictionary/events/"),
             ("🗺️", "성경 지도", "지명이 지금은?", "/dictionary/map/"), ("🧑‍🏫", "교사 허브", "주일학교 자료", "/teachers/"),
             ("📅", "오늘의 말씀", "매일 새로운 구절", "/today/"), ("🎴", "말씀 뽑기", "내게 주시는 말씀", "/verse/")]
    g = "".join(f'<a class="hh-card" href="{h}" data-ga="home_hub_click" data-ga-label="{t}"><i>{ic}</i><b>{t}</b><span>{d}</span></a>' for ic, t, d, h in cards)
    return f'<!--HUB--><section class="home-hub"><h2>무엇을 찾으세요?</h2><div class="hh-grid">{g}</div></section><!--/HUB-->'


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


def apply(path, s):
    key = active_key(path)
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
    # 우측 마스코트 후원 안내(게임 화면 제외)
    s = _strip(s, "PEEK")
    if not path.startswith(("play.html", "play2.html", "support.html")) and "</body>" in s:
        s = s.replace("</body>", peek_html() + "\n</body>", 1)
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
