# -*- coding: utf-8 -*-
"""성경사전 인덱스(분류 타일+검색)와 분류별 목록 페이지(/dictionary/places/ 등)."""
import json

from site_chrome import CATS

FEATURED = ["jerusalem", "moses", "david", "paul", "abraham", "crucifixion", "resurrection", "jordan-river", "sea-of-galilee", "birth-of-jesus", "creation", "pentecost"]

SEARCH_CSS = ('<style>.dsearch{position:relative;margin:14px 0 6px}.dsearch input{width:100%;box-sizing:border-box;padding:14px 16px;font-size:16px;border:2px solid #cfe0f7;'
              'border-radius:14px;font-family:inherit}.dsearch input:focus{outline:0;border-color:#0073e6}.dres{margin:8px 0 0;display:none}'
              '.dres a{display:flex;justify-content:space-between;gap:10px;padding:11px 14px;background:#fff;border:1px solid #e5e5e5;border-radius:10px;margin-bottom:6px;text-decoration:none;color:#222}'
              '.dres a:hover{border-color:#0073e6}.dres small{color:#7b8794;white-space:nowrap}'
              '.tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:18px 0 8px}'
              '.dreq{padding:14px;background:#fff8ec;border:1px solid #fcd9a8;border-radius:12px;text-align:center}.dreq p{margin:0 0 8px;color:#7a4a00}.dres a.dreqbtn{display:inline-block;background:#d97706;color:#fff!important;border:0;margin:0;padding:9px 16px;border-radius:20px;font-weight:700;text-decoration:none;font-size:14px}'
              '.tile{display:block;background:#fff;border:1px solid #e5e5e5;border-radius:16px;padding:16px;text-decoration:none!important;color:#222!important;box-shadow:0 2px 8px rgba(0,0,0,.04)}'
              '.tile:hover{border-color:#0073e6;box-shadow:0 4px 14px rgba(0,115,230,.14)}'
              '.tile i{font-style:normal;font-size:28px}.tile b{display:block;font-size:17px;margin:4px 0 2px}'
              '.tile em{font-style:normal;font-size:12px;color:#0073e6;font-weight:700}.tile span{display:block;font-size:13px;color:#667;line-height:1.5;margin-top:4px}'
              '.tile small{display:block;font-size:12px;color:#8a97a6;margin-top:8px}'
              '.chips2{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 22px}.chips2 a{padding:8px 14px;background:#fff;border:1px solid #d6e2f1;border-radius:18px;font-size:14px;text-decoration:none;color:#33506e}'
              '.chips2 a:hover{background:#f0f6ff}'
              '@media(max-width:600px){.tile{padding:12px}.tile i{font-size:24px}.tile b{font-size:15px}.tile span{font-size:12px;margin-top:2px}.tile small{display:none}}</style>')

SEARCH_JS = """<script>(function(){var D=%s;var i=document.getElementById('dq'),r=document.getElementById('dres');
if(!i)return;function reqHref(q){return 'mailto:mandubird@naver.com?subject='+encodeURIComponent('[십자가로세로] 성경사전 항목 추가 요청: '+q)+'&body='+encodeURIComponent('요청 항목: '+q+'\n찾아본 페이지: '+location.href+'\n\n(필요하신 내용이 있으면 자유롭게 적어 주세요)');}
i.addEventListener('input',function(){var q=i.value.trim().toLowerCase();if(!q){r.style.display='none';r.innerHTML='';return;}
var m=D.filter(function(d){return d.n.toLowerCase().indexOf(q)>-1||d.s.toLowerCase().indexOf(q)>-1;}).slice(0,12);
r.style.display='block';r.innerHTML=m.length?m.map(function(d){return '<a href="/dictionary/'+d.u+'.html"><span><b>'+d.n+'</b> <span style="color:#667;font-size:13px">'+d.s+'</span></span><small>'+d.t+'</small></a>';}).join(''):'<div class="dreq"><p>"'+q.replace(/</g,'&lt;')+'" 항목이 아직 없어요.</p><a class="dreqbtn" href="'+reqHref(q)+'" data-ga="dict_request">✉️ 이 항목 추가를 요청하기</a></div>';
if(window.crsTrack&&q.length>1)window.crsTrack('dict_search',{q:q});});})();</script>"""


def _cards(items, esc):
    return '<div class="cards">' + "".join(
        f'<a class="card" href="/dictionary/{e["slug"]}.html"><b>{esc(e["name"])}</b><span>{esc(e["sub"])}</span></a>' for e in items) + "</div>"



def _guide_block(ENTRIES, esc):
    """허브 하단 안내(검색 의도별 소제목 + FAQ). 개수는 데이터에서 계산한다."""
    n = {folder: len([e for e in ENTRIES if e["type"] == typ]) for typ, folder, label, icon, d in CATS}
    faq = [
        ("성경사전이란 무엇인가요?", "성경에 나오는 인물, 지명, 사건, 신앙 용어를 쉽게 풀어 정리한 참고 자료입니다. 십자가로세로 성경사전은 인물 %d개, 지명 %d개, 사건 %d개, 신앙 용어 %d개와 66권 요약을 담고 있습니다." % (n["people"], n["places"], n["events"], n["terms"])),
        ("무료 온라인 성경사전은 어떻게 이용하나요?", "가입 없이 누구나 무료로 볼 수 있습니다. 위의 검색창에 이름이나 키워드(예: 예루살렘, 모세, 은혜)를 넣거나, 인물·지명·사건·용어·66권 요약 분류에서 골라 보세요."),
        ("성경 인물이나 지명은 어떻게 찾나요?", "분류별 모음 페이지에서 목록으로 찾거나, '구절로 찾기'에 창세기 12:1처럼 구절을 입력하면 그 구절과 관련된 인물·사건·지명으로 연결됩니다."),
        ("성경 본문도 함께 실려 있나요?", "각 항목은 성경 본문의 장·절 위치를 기준으로 정리했고, 본문 전체를 옮기지 않습니다. 본문은 가지고 계신 성경에서 해당 구절을 함께 읽어 보세요."),
        ("해석이 갈리는 부분은 어떻게 다루나요?", "해석이 갈리는 부분은 그렇다고 밝혀 두었습니다. 작성 원칙은 콘텐츠 제작 원칙 페이지에서 볼 수 있습니다."),
        ("주일학교 교사나 소그룹 인도자도 사용할 수 있나요?", "네. 수업 준비에서 인물과 사건의 배경을 확인하고, 항목과 연결된 가로세로 퍼즐로 복습 활동을 할 수 있습니다. 교사 허브에서 더 많은 자료를 볼 수 있습니다."),
    ]
    h = ['<section class="dguide">']
    h.append('<h2>성경사전, 궁금한 것에 따라 이렇게 찾아보세요</h2>')
    h.append('<h3>성경 인물이 궁금할 때</h3><p>아브라함, 모세, 다윗, 바울 등 <a href="/dictionary/people/">성경 인물 %d명</a>의 삶과 핵심 구절, 함께 읽을 본문을 정리했습니다.</p>' % n["people"])
    h.append('<h3>성경 지명과 지도가 궁금할 때</h3><p><a href="/dictionary/places/">성경 지명 %d곳</a>은 지명의 뜻과 성경 속 사건, 오늘의 위치와 사진까지 볼 수 있고, <a href="/dictionary/map/">성경 지도</a>에서 한눈에 비교할 수 있습니다.</p>' % n["places"])
    h.append('<h3>성경 사건의 흐름이 궁금할 때</h3><p><a href="/dictionary/events/">성경 사건 %d개</a>를 흐름으로 이해하고, <a href="/dictionary/timeline/">성경 연대표</a>에서 창조부터 초대교회까지 시대별로 이어서 볼 수 있습니다.</p>' % n["events"])
    h.append('<h3>성경 66권을 한눈에 보고 싶을 때</h3><p>창세기부터 요한계시록까지 <a href="/dictionary/books/">66권 요약</a>으로 책별 핵심 내용과 구조를 확인하세요.</p>')
    h.append('<h3>어려운 신앙 용어를 쉬운 말로</h3><p>구원, 은혜, 칭의, 성령처럼 자주 듣지만 풀기 어려운 <a href="/dictionary/terms/">신앙 용어 %d개</a>를 쉬운 말로 풀었습니다.</p>' % n["terms"])
    h.append('<h3>구절에서 거꾸로 찾고 싶을 때</h3><p>설교나 묵상 본문의 구절을 알고 있다면 <a href="/dictionary/verses/">구절로 찾기</a>에서 관련 인물·사건·지명을 바로 찾을 수 있습니다.</p>')
    h.append('<h2>무료 온라인 성경사전, 십자가로세로는 이렇게 다릅니다</h2><ul>'
             '<li><b>지명을 오늘의 모습으로</b> — 옛 이름이 지금의 어디인지 위치와 사진, 지도로 확인합니다.</li>'
             '<li><b>구절 위치 기준으로 직접 정리</b> — 해석이 갈리는 부분은 그렇다고 밝힙니다.</li>'
             '<li><b>읽고 나서 퍼즐로 복습</b> — 항목과 연결된 가로세로 퍼즐로 내용을 다시 익힙니다.</li>'
             '<li><b>가입 없이 무료</b> — 교회학교와 소그룹 수업 준비에도 자유롭게 쓸 수 있습니다.</li></ul>')
    h.append('<h2>성경사전 자주 묻는 질문</h2><div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</div></section>")
    css = '<style>.dguide{margin:30px 0 10px;text-align:left}.dguide h2{font-size:20px;color:#16324f;margin:28px 0 8px}.dguide h3{font-size:16.5px;color:#0b3d73;margin:16px 0 4px}.dguide p,.dguide li{font-size:15.5px;line-height:1.85;margin:0 0 6px;word-break:keep-all}.dguide ul{padding-left:20px}</style>'
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return css + "".join(h), '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"

def render_index(ctx):
    ENTRIES, BY_SLUG, head, esc, FOOTER, SITE, BOOKS, BOOK_GROUPS = (ctx[k] for k in ("ENTRIES", "BY_SLUG", "head", "esc", "FOOTER", "SITE", "BOOKS", "BOOK_GROUPS"))
    path = "/dictionary/"
    title = "성경사전 - 성경 인물·지명·사건·용어와 66권 요약, 성경공부 | 십자가로세로"
    desc = f"성경 지명, 성경 인물, 성경 사건, 신앙 용어와 66권 요약 {len(ENTRIES)}개 항목을 쉽게 정리한 사전. 지명은 오늘의 위치와 사진, 성경 지도로 함께 확인하세요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "성경사전", "description": desc, "inLanguage": "ko", "url": SITE + path,
        "hasPart": [{"@type": "Article", "name": e["name"], "url": f"{SITE}/dictionary/{e['slug']}.html"} for e in ENTRIES]}, ensure_ascii=False) + "</script>"
    guide_html, faq_ld = _guide_block(ENTRIES, esc)
    out = [head(title, desc, path, ld + "\n" + faq_ld).replace("</head>", SEARCH_CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › 성경사전</div>')
    out.append('<h1>성경사전</h1><div class="sub">지명 · 인물 · 사건 · 용어, 궁금한 것부터 찾아보세요</div>')
    out.append('<div class="dsearch"><input id="dq" type="search" placeholder="🔍 이름이나 키워드로 찾기 (예: 예루살렘, 모세, 은혜)" autocomplete="off"><div class="dres" id="dres"></div></div>')
    tiles = []
    for typ, folder, label, icon, d in CATS:
        items = [e for e in ENTRIES if e["type"] == typ]
        sample = " · ".join(e["name"] for e in items[:4])
        tiles.append(f'<a class="tile" href="/dictionary/{folder}/" data-ga="dict_tile" data-ga-label="{folder}"><i>{icon}</i><b>{label}</b><em>{len(items)}개</em><span>{esc(d)}</span><small>{esc(sample)} …</small></a>')
    tiles.append('<a class="tile" href="/dictionary/map/" data-ga="dict_tile" data-ga-label="map"><i>🗺️</i><b>성경 지도</b><em>지도 보기</em><span>지명이 지금은 어디에 있을까? 바울의 여행 경로까지</span><small>예루살렘 · 갈릴리 · 에베소 · 로마 …</small></a>')
    tiles.append('<a class="tile" href="/dictionary/genealogy/" data-ga="dict_tile" data-ga-label="genealogy"><i>👪</i><b>가계도</b><em>아담~예수님</em><span>아담에서 노아, 아브라함에서 예수님까지 계보</span><small>야곱의 열두 아들 · 마태복음 1장 …</small></a>')
    tiles.append('<a class="tile" href="/dictionary/timeline/" data-ga="dict_tile" data-ga-label="timeline"><i>⏳</i><b>연대표</b><em>10개 시대</em><span>창조에서 초대교회까지, 시대별 사건·인물·지명과 지도</span><small>족장 · 출애굽 · 왕국 · 예수님 · 초대교회 …</small></a>')
    tiles.append('<a class="tile" href="/dictionary/verses/" data-ga="dict_tile" data-ga-label="verses"><i>📖</i><b>구절로 찾기</b><em>구절 → 항목</em><span>창세기 12:1처럼 구절을 입력하면 관련 인물·사건·지명으로 연결</span><small>책별 구절 목록 포함</small></a>')
    out.append('<div class="tiles">' + "".join(tiles) + "</div>")
    feat = [BY_SLUG[s] for s in FEATURED if s in BY_SLUG]
    out.append('<h2 style="margin-top:26px">많이 찾는 항목</h2><div class="chips2">' + "".join(
        f'<a href="/dictionary/{e["slug"]}.html">{esc(e["name"])}</a>' for e in feat) + "</div>")
    allh = []
    for typ, folder, label, icon, d in CATS:
        its = [e for e in ENTRIES if e["type"] == typ]
        allh.append(f'<h3 style="margin:14px 0 6px">{icon} {label} ({len(its)})</h3><p style="line-height:2;font-size:14px;margin:0">' + " · ".join(
            f'<a href="/dictionary/{e["slug"]}.html">{esc(e["name"])}</a>' for e in its) + "</p>")
    out.append('<details style="margin:18px 0"><summary style="cursor:pointer;font-weight:700;font-size:16px">전체 항목 한눈에 보기 (%d)</summary>' % len(ENTRIES) + "".join(allh) + "</details>")
    out.append(guide_html)
    out.append('<p style="font-size:14px;color:#556;line-height:1.8">각 항목은 성경 본문의 구절 위치를 기준으로 직접 정리했습니다. 읽고 나서 관련 가로세로 퍼즐로 복습할 수 있고, 해석이 갈리는 부분은 그렇다고 밝혀 두었습니다. 작성 원칙은 <a href="/editorial-policy.html">콘텐츠 제작 원칙</a>을 참고해 주세요.</p>')
    out.append("</main>")
    out.append(FOOTER)
    data = [{"n": e["name"], "s": e["sub"], "u": e["slug"], "t": (CATS_BY_TYPE[e["type"]] if e["type"] in CATS_BY_TYPE else e["type"])} for e in ENTRIES]
    out.append(SEARCH_JS % json.dumps(data, ensure_ascii=False))
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


CATS_BY_TYPE = {c[0]: c[2] for c in CATS}
INTRO = {'places': '성경 지명은 사건이 일어난 무대입니다. 각 항목에서 지명의 뜻과 성경 속 사건, 오늘의 위치와 현재 사진·지도를 볼 수 있고, 성경 지도에서 모든 지명의 위치를 한 번에 비교할 수 있습니다. 위치는 학자들의 식별을 따르며 학설이 갈리는 곳은 그렇게 표시했습니다. 궁금한 지명을 골라 읽고 관련 퍼즐로 복습해 보세요.', 'people': '성경 인물 항목은 인물의 삶을 핵심 정보, 본문 해설, 관련 구절, 자주 묻는 질문으로 정리했습니다. 아브라함에서 바울까지 구약과 신약의 주요 인물을 골랐고, 가계도와 연대표에서 그 인물이 어느 시대에 속하는지 함께 볼 수 있습니다. 성경 구절은 모두 장·절 표기로 안내해 직접 읽어 보실 수 있습니다.', 'events': '성경 사건 항목은 천지창조에서 부활과 승천까지 큰 사건을 시간 순서의 맥락 속에서 설명합니다. 각 사건의 배경, 핵심 구절, 등장인물과 지명, 오늘의 적용을 담았고, 성경 지도와 연대표로 이어집니다. 사건에 대한 이해가 교단마다 다른 경우에는 그렇게 밝혀 두었습니다.', 'terms': '신앙 용어 항목은 구원, 은혜, 칭의, 성령처럼 교회에서 자주 쓰지만 뜻이 막연한 말을 쉬운 말로 풀었습니다. 각 항목은 정의, 성경 근거 구절, 자주 하는 질문으로 구성했고, 세례나 성찬처럼 교단마다 이해가 다른 용어는 그 차이를 밝혀 두었습니다. 새신자 교육이나 소그룹 공부에서 쉽게 쓸 수 있습니다.', 'books': '66권 요약은 창세기부터 요한계시록까지 책마다 기록 목적, 핵심 메시지, 구조, 핵심 구절, 읽을 때의 팁을 정리했습니다. 성경 통독 계획을 세우거나 공과 본문을 미리 살펴볼 때 활용하세요. 각 책에서 이어지는 인물·지명 항목과 퍼즐로 복습할 수 있습니다.'}


def render_category(cat, ctx):
    ENTRIES, head, esc, FOOTER, SITE, BOOKS, BOOK_GROUPS = (ctx[k] for k in ("ENTRIES", "head", "esc", "FOOTER", "SITE", "BOOKS", "BOOK_GROUPS"))
    typ, folder, label, icon, d = cat
    path = f"/dictionary/{folder}/"
    items = [e for e in ENTRIES if e["type"] == typ]
    title = f"{label} 모음 - {len(items)}개 항목 한눈에 보기 | 성경사전 | 십자가로세로"
    desc = f"{label} {len(items)}개 항목을 한곳에 모았습니다. {d}"
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": f"{label} 모음", "description": desc, "inLanguage": "ko", "url": SITE + path,
        "hasPart": [{"@type": "Article", "name": e["name"], "url": f"{SITE}/dictionary/{e['slug']}.html"} for e in items]}, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld).replace("</head>", SEARCH_CSS + "\n</head>", 1), '<main class="wrap">']
    out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › {label}</div>')
    out.append(f'<h1>{icon} {label}</h1><div class="sub">{esc(d)}</div>')
    out.append('<div class="summary">' + esc(INTRO[folder]) + '</div>')
    if folder == "places":
        out.append('<a class="cta" href="/dictionary/map/">🗺️ 지도에서 한눈에 보기<small>모든 지명을 지도 위 핀으로, 오늘의 위치와 사진까지</small></a>')
    out.append(f'<div class="dsearch"><input id="dq" type="search" placeholder="🔍 {label} 안에서 찾기" autocomplete="off"><div class="dres" id="dres"></div></div>')
    if folder == "books":
        for testament, groups in BOOK_GROUPS:
            its = [e for e in BOOKS if e["testament"] == testament]
            out.append(f'<div class="idx-section"><h2>{testament} 성경 ({len(its)}권)</h2>')
            for g in groups:
                gi = [e for e in its if e["group"] == g]
                if gi:
                    out.append(f'<h3 class="idx-group">{g}</h3>' + _cards(gi, esc))
            out.append("</div>")
    else:
        out.append(_cards(items, esc))
    others = [c for c in CATS if c[1] != folder]
    out.append('<h2 style="margin-top:30px">다른 분류도 둘러보기</h2><div class="chips2">' + "".join(
        f'<a href="/dictionary/{c[1]}/">{c[3]} {c[2]}</a>' for c in others) + '<a href="/dictionary/map/">🗺️ 성경 지도</a></div>')
    out.append("</main>")
    out.append(FOOTER)
    data = [{"n": e["name"], "s": e["sub"], "u": e["slug"], "t": label} for e in items]
    out.append(SEARCH_JS % json.dumps(data, ensure_ascii=False))
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)
