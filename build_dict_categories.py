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


def render_index(ctx):
    ENTRIES, BY_SLUG, head, esc, FOOTER, SITE, BOOKS, BOOK_GROUPS = (ctx[k] for k in ("ENTRIES", "BY_SLUG", "head", "esc", "FOOTER", "SITE", "BOOKS", "BOOK_GROUPS"))
    path = "/dictionary/"
    title = "성경사전 - 성경 인물·지명·사건·용어와 66권 요약, 성경공부 | 십자가로세로"
    desc = f"성경 지명, 성경 인물, 성경 사건, 신앙 용어와 66권 요약 {len(ENTRIES)}개 항목을 쉽게 정리한 사전. 지명은 오늘의 위치와 사진, 성경 지도로 함께 확인하세요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "성경사전", "description": desc, "inLanguage": "ko", "url": SITE + path,
        "hasPart": [{"@type": "Article", "name": e["name"], "url": f"{SITE}/dictionary/{e['slug']}.html"} for e in ENTRIES]}, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld).replace("</head>", SEARCH_CSS + "\n</head>", 1), '<main class="wrap">']
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
    out.append('<p style="font-size:14px;color:#556;line-height:1.8">각 항목은 성경 본문의 구절 위치를 기준으로 직접 정리했습니다. 읽고 나서 관련 가로세로 퍼즐로 복습할 수 있고, 해석이 갈리는 부분은 그렇다고 밝혀 두었습니다. 작성 원칙은 <a href="/editorial-policy.html">콘텐츠 제작 원칙</a>을 참고해 주세요.</p>')
    out.append("</main>")
    out.append(FOOTER)
    data = [{"n": e["name"], "s": e["sub"], "u": e["slug"], "t": (CATS_BY_TYPE[e["type"]] if e["type"] in CATS_BY_TYPE else e["type"])} for e in ENTRIES]
    out.append(SEARCH_JS % json.dumps(data, ensure_ascii=False))
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


CATS_BY_TYPE = {c[0]: c[2] for c in CATS}


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
