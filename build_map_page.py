# -*- coding: utf-8 -*-
"""성경 지도 페이지(/dictionary/map/). build_dictionary.main()에서 호출."""
import json

MAP_JS = r"""
var m=L.map('bmap',{scrollWheelZoom:false}).setView([31.9,35.3],8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; OpenStreetMap'}).addTo(m);
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var MK={};
P.forEach(function(p){
  var h='<div class="pop"><b>'+esc(p.name)+'</b><br><span>'+esc(p.sub)+'</span>'+(p.img?'<img src="'+p.img+'" alt="'+esc(p.name)+'" loading="lazy">':'<br>')+'<span style="font-size:12px;color:#666">'+esc(p.where)+'<br>성경 언급 '+p.verses+'절</span><br><a href="/dictionary/'+p.slug+'.html">'+esc(p.name)+' 항목 보기 →</a></div>';
  MK[p.slug]=L.circleMarker([p.lat,p.lon],{radius:8,color:'#0052cc',weight:2,fillColor:'#0073e6',fillOpacity:.85}).addTo(m).bindPopup(h).bindTooltip(p.name);
});
var qi=document.getElementById('mq'),qr=document.getElementById('mres');
function reqHref(q){return 'mailto:mandubird@naver.com?subject='+encodeURIComponent('[십자가로세로] 성경 지도 지명 추가 요청: '+q)+'&body='+encodeURIComponent('요청 지명: '+q+'\n찾아본 페이지: '+location.href+'\n\n(성경 구절이나 알고 계신 위치가 있으면 적어 주세요)');}
qi.addEventListener('input',function(){
  var q=qi.value.trim().toLowerCase(); if(!q){qr.style.display='none';qr.innerHTML='';return;}
  var r=P.filter(function(p){return p.name.toLowerCase().indexOf(q)>-1||p.sub.toLowerCase().indexOf(q)>-1||p.where.toLowerCase().indexOf(q)>-1;}).slice(0,8);
  qr.style.display='block';
  qr.innerHTML=r.length?r.map(function(p){return '<a href="#" data-s="'+p.slug+'"><span><b>'+esc(p.name)+'</b> <span style="color:#667;font-size:13px">'+esc(p.where)+'</span></span><small>지도에서 보기</small></a>';}).join(''):'<div class="dreq"><p>"'+esc(q)+'" 지명이 지도에 아직 없어요.</p><a class="dreqbtn" href="'+reqHref(qi.value.trim())+'" data-ga="map_request">✉️ 이 지명 추가를 요청하기</a></div>';
  if(window.crsTrack&&q.length>1)crsTrack('map_search',{q:q,hit:r.length});
});
qr.addEventListener('click',function(e){var a=e.target.closest('a[data-s]');if(!a)return;e.preventDefault();var mk=MK[a.getAttribute('data-s')];
  if(mk){m.setView(mk.getLatLng(),11);mk.openPopup();document.getElementById('bmap').scrollIntoView({behavior:'smooth',block:'center'});}});
document.querySelectorAll('.mbtn').forEach(function(b){b.addEventListener('click',function(){
  if(b.dataset.v==='holy'){m.setView([31.9,35.3],8);}else{m.fitBounds(P.map(function(p){return [p.lat,p.lon]}),{padding:[30,30]});}
  if(window.crsTrack)crsTrack('bible_map_view',{view:b.dataset.v});
});});
"""

EXTRA_HEAD = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">\n'
              '<style>#bmap{height:520px;border-radius:14px;border:1px solid #e5e5e5;margin:14px 0 8px;z-index:0}'
              '.mbtn{border:1px solid #ccd;background:#fff;border-radius:18px;padding:6px 14px;font-size:13px;cursor:pointer;margin-right:6px}'
              '.mbtn:hover{background:#f0f6ff}.pop b{font-size:15px}.pop img{width:200px;height:120px;object-fit:cover;border-radius:6px;display:block;margin:6px 0}'
              '.dres{display:none;margin:8px 0 0}.dres a{display:flex;justify-content:space-between;gap:10px;padding:11px 14px;background:#fff;border:1px solid #e5e5e5;border-radius:10px;margin-bottom:6px;text-decoration:none;color:#222}.dres small{color:#7b8794;white-space:nowrap}'
              '.dreq{padding:14px;background:#fff8ec;border:1px solid #fcd9a8;border-radius:12px;text-align:center}.dreq p{margin:0 0 8px;color:#7a4a00}.dres a.dreqbtn{display:inline-block;background:#d97706;color:#fff!important;border:0;margin:0;padding:9px 16px;border-radius:20px;font-weight:700;text-decoration:none;font-size:14px}'
              '.pop a{color:#0073e6}.steps{padding-left:22px}.steps li{margin:8px 0}.sref{font-size:12px;color:#0073e6}.snote{font-size:13px;color:#667}.faq{margin:10px 0}.faq p{margin:2px 0 0}@media(max-width:600px){#bmap{height:420px}}</style>\n</head>')


def render_map(GEO, BY_SLUG, head, esc, FOOTER, SITE):
    path = "/dictionary/map/"
    title = "성경 지도 - 성경 지명 위치와 바울 성지순례·전도 여행 경로 | 십자가로세로"
    desc = "성경 속 지명 65곳의 오늘의 위치와 사진, 바울 전도 여행·성지순례 경로, 예수님 사역 경로를 성경 지도에서 확인하세요. 성경공부와 성지순례 준비에 활용할 수 있어요."
    pts = []
    for slug, g in GEO.items():
        e = BY_SLUG.get(slug)
        if not e:
            continue
        pts.append({"slug": slug, "name": e["name"], "sub": e["sub"], "lat": g["lat"], "lon": g["lon"],
                    "where": g["where"], "img": g.get("img"), "verses": g["verses"]})
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "성경 지도", "description": desc,
        "inLanguage": "ko", "url": SITE + path, "image": f"{SITE}/images/maps/bible-map-overview.png"}, ensure_ascii=False) + "</script>"
    ld += '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Dataset", "name": "성경 지명 좌표 데이터(십자가로세로 편집본)",
        "description": "성경 속 지명의 위도·경도, 오늘의 위치, 성경 언급 절 수. 위치는 학자들의 식별을 모은 OpenBible.info 데이터를 바탕으로 합니다.",
        "url": SITE + path, "inLanguage": "ko", "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "Organization", "name": "십자가로세로", "url": SITE},
        "isBasedOn": "https://github.com/openbibleinfo/Bible-Geocoding-Data",
        "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITE}/data/bible-places.json"},
                         {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": f"{SITE}/data/bible-places.csv"}]}, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld, f"{SITE}/images/maps/bible-map-overview.png").replace("</head>", EXTRA_HEAD, 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › 성경 지도</div>')
    out.append('<h1>성경 지도</h1><div class="sub">성경 속 지명이 지금은 어디에 있을까요?</div>')
    out.append('<div class="summary">핀을 누르면 그 지명의 오늘의 위치와 사진, 성경사전 항목으로 이동하는 링크를 볼 수 있습니다. '
               '위치는 학자들의 식별을 모은 OpenBible.info 성경 지오코딩 데이터(CC BY 4.0)를 바탕으로 하며, 일부는 학설에 따라 달라질 수 있습니다.</div>')
    out.append('<figure style="margin:14px 0"><img src="/images/maps/bible-map-overview.png" width="1200" height="630" alt="성경 속 지명 지도 - 예루살렘, 베들레헴, 갈릴리 바다, 여리고 등 오늘의 위치" style="width:100%;height:auto;border-radius:14px;display:block"></figure>')
    out.append('<div class="dsearch" style="margin:12px 0 4px"><input id="mq" type="search" placeholder="🔍 지명 찾기 (예: 예루살렘, 갈릴리, 에베소)" autocomplete="off" style="width:100%;box-sizing:border-box;padding:13px 16px;font-size:16px;border:2px solid #cfe0f7;border-radius:14px;font-family:inherit"><div class="dres" id="mres"></div></div>')
    out.append('<div><button class="mbtn" data-v="holy">이스라엘 지역</button><button class="mbtn" data-v="all">전체 보기</button></div>')
    out.append('<div id="bmap" role="application" aria-label="성경 지명 지도"></div>')
    out.append('<div style="font-size:12px;color:#7b8794">지도 © <a href="https://www.openstreetmap.org/copyright" rel="noopener nofollow">OpenStreetMap</a> 기여자 · '
               '데이터 <a href="https://github.com/openbibleinfo/Bible-Geocoding-Data" rel="noopener nofollow">OpenBible.info</a> CC BY 4.0 · '
               '내려받기: <a href="/data/bible-places.json">JSON</a> · <a href="/data/bible-places.csv">CSV</a> (출처 표기 시 자유롭게 사용)</div>')
    from build_routes import ROUTES
    from pilgrim_banner import banner as _pb
    out.append(_pb("map"))
    out.append('<div class="idx-section"><h2>바울의 여행 경로</h2><div class="cards">' + "".join(
        f'<a class="card" href="/dictionary/map/{r["slug"]}.html"><b>{esc(r["short"])}</b><span>{esc(r["ref"])}</span></a>' for r in ROUTES if r["group"] == "paul") + "</div></div>")
    out.append('<div class="idx-section"><h2>예수님의 사역 경로</h2><div class="cards">' + "".join(
        f'<a class="card" href="/dictionary/map/{r["slug"]}.html"><b>{esc(r["short"])}</b><span>{esc(r["ref"])}</span></a>' for r in ROUTES if r["group"] == "jesus") + "</div></div>")
    out.append(f'<div class="idx-section"><h2>지명 목록 ({len(pts)})</h2><div class="cards">' + "".join(
        f'<a class="card" href="/dictionary/{p["slug"]}.html"><b>{esc(p["name"])}</b><span>{esc(p["where"])}</span></a>' for p in pts)
        + "</div></div>")
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>')
    out.append("<script>(function(){var P=" + json.dumps(pts, ensure_ascii=False) + ";" + MAP_JS + "})();</script>")
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def write_datasets(GEO, BY_SLUG, ENTRIES, SITE):
    """성경 지명 좌표 데이터(JSON·CSV)와 바울 여행 경로 JSON을 /data/에 공개한다."""
    import csv
    import os
    root = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(root, "data")
    os.makedirs(out, exist_ok=True)
    rows = []
    for slug, g in GEO.items():
        e = BY_SLUG.get(slug)
        if not e:
            continue
        rows.append({"slug": slug, "name_ko": e["name"], "summary_ko": e["sub"], "latitude": g["lat"], "longitude": g["lon"],
                     "modern_name": g["modern"], "location_ko": g["where"], "bible_verse_mentions": g["verses"],
                     "identification_confidence": g["score"], "page_url": f"{SITE}/dictionary/{slug}.html",
                     "openbible_url": f"https://www.openbible.info/geo/ancient/{g['ob_id']}/{g['ob_slug']}",
                     "photo_credit": g.get("credit") or "", "photo_license": g.get("license") or ""})
    meta = {"name": "성경 지명 좌표 데이터(십자가로세로 편집본)", "license": "CC BY 4.0",
            "attribution": "십자가로세로(crossero.com), 원자료 OpenBible.info 성경 지오코딩 데이터(CC BY 4.0)",
            "note": "위치는 학자들의 식별을 모은 것이며 일부는 학설에 따라 달라질 수 있습니다.", "count": len(rows), "places": rows}
    open(os.path.join(out, "bible-places.json"), "w", encoding="utf-8").write(json.dumps(meta, ensure_ascii=False, indent=1))
    with open(os.path.join(out, "bible-places.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    from build_routes import ROUTES
    from dictionary_routes_data import PLACES as RP
    def pack(group):
        return [{"slug": r["slug"], "name": r["name"], "reference": r["ref"], "approx_date": r["when"], "page_url": f"{SITE}/dictionary/map/{r['slug']}.html",
                 "stops": [{"order": i, "name_ko": RP[k]["name"], "modern_name": RP[k]["modern"], "latitude": RP[k]["lat"], "longitude": RP[k]["lon"],
                            "scripture_reference": ref, "note_ko": note} for i, (k, ref, note) in enumerate(r["steps"], 1)]} for r in ROUTES if r["group"] == group]
    for fname, group, title in (("paul-journeys.json", "paul", "사도 바울의 여행 경로(십자가로세로 편집본)"), ("jesus-ministry.json", "jesus", "예수님의 사역 경로(십자가로세로 편집본)")):
        open(os.path.join(out, fname), "w", encoding="utf-8").write(json.dumps(
            {"name": title, "license": "CC BY 4.0", "attribution": "십자가로세로(crossero.com), 위치 OpenBible.info CC BY 4.0",
             "note": "경로는 방문 순서를 잇는 개략적인 것이며 복음서·사도행전의 순서 정리는 학자마다 다릅니다.", "routes": pack(group)}, ensure_ascii=False, indent=1))


def write_llms(ENTRIES, GEO, SITE):
    import os
    from site_chrome import CATS
    cnt = {c[0]: sum(1 for e in ENTRIES if e["type"] == c[0]) for c in CATS}
    t = f"""# 십자가로세로 (crossero.com)

> 십자가로세로는 성경사전·성경 지도·성경 연대표·성경 퍼즐·말씀 묵상·주일학교 교사 자료를 한곳에 모은 성경 학습·활용 서비스입니다(한국어). 개인 사역으로 운영되며 무료로 이용할 수 있습니다.

## 이 사이트가 답할 수 있는 질문
- 성경 지명(예루살렘, 갈릴리 바다 등)은 지금 어디인가? → 성경 지도, 성경 지명 항목
- 바울의 전도 여행·성지순례 경로는? → 바울 1·2·3차 전도 여행 지도
- 성경 연대기와 시대별 흐름은? → 성경 연대표
- 이 구절과 관련된 인물·사건은? → 구절로 찾기
- 아브라함에서 예수님까지의 족보는? → 성경 가계도
- 주일학교 교사 자료와 성경 퀴즈는? → 교사 허브, 성경 퍼즐

## 인용 안내
- 출처 표기: 십자가로세로(crossero.com). 데이터는 CC BY 4.0이며 원자료는 OpenBible.info입니다.
- 내용은 교회 지도자의 피드백을 받아 수정하며 이력은 [검수·수정 이력]({SITE}/feedback/)에 공개합니다.

## 성경사전
- [성경사전 홈]({SITE}/dictionary/): 지명·인물·사건·신앙 용어·66권 요약 {len(ENTRIES)}개 항목
- [성경 지명]({SITE}/dictionary/places/): {cnt.get('지명', 0)}개, 지명마다 오늘의 위치·사진·지도 이미지 포함
- [성경 인물]({SITE}/dictionary/people/): {cnt.get('인물', 0)}개
- [성경 사건]({SITE}/dictionary/events/): {cnt.get('사건', 0)}개
- [신앙 용어]({SITE}/dictionary/terms/): {cnt.get('신앙 용어', 0)}개
- [성경 66권 요약]({SITE}/dictionary/books/)
- [성경 가계도]({SITE}/dictionary/genealogy/): 아담~노아, 야곱의 열두 아들, 아브라함~예수님
- [성경 연대표]({SITE}/dictionary/timeline/): 창조에서 초대교회까지 10개 시대별 정리
- [구절로 찾기]({SITE}/dictionary/verses/): 성경 구절에서 관련 인물·사건·지명 항목으로 연결

## 성경 지도
- [성경 지도]({SITE}/dictionary/map/): 성경 지명 {len(GEO)}곳의 오늘의 위치 (인터랙티브 지도)
- [바울 1차 전도 여행]({SITE}/dictionary/map/paul-journey-1.html)
- [바울 2차 전도 여행]({SITE}/dictionary/map/paul-journey-2.html)
- [바울 3차 전도 여행]({SITE}/dictionary/map/paul-journey-3.html)
- [바울의 로마 압송 항해]({SITE}/dictionary/map/paul-journey-rome.html)
- [예수님의 탄생과 유년기]({SITE}/dictionary/map/jesus-birth.html)
- [예수님의 갈릴리 사역]({SITE}/dictionary/map/jesus-galilee.html)
- [예수님의 예루살렘 여정]({SITE}/dictionary/map/jesus-to-jerusalem.html)
- [예수님의 십자가 주간과 부활]({SITE}/dictionary/map/jesus-passion.html)

## 데이터 (CC BY 4.0, 출처 표기 필수)
- [성경 지명 좌표 JSON]({SITE}/data/bible-places.json) / [CSV]({SITE}/data/bible-places.csv)
- [바울 여행 경로 JSON]({SITE}/data/paul-journeys.json) / [예수님 사역 경로 JSON]({SITE}/data/jesus-ministry.json)
- 원자료: OpenBible.info 성경 지오코딩 데이터(CC BY 4.0). 위치는 학자들의 식별이며 일부는 학설에 따라 다를 수 있습니다.
- 성경 본문은 개역한글판(저작권 만료)을 사용합니다.

## 말씀·퍼즐·교사 자료
- [성탄절 성극 대본]({SITE}/christmas/): 성탄 성극·크리스마스 성극 대본 10편과 준비 가이드(직접 작성, 비상업적 사용 가능)
- [성탄 성극 소품 도안]({SITE}/christmas/props.html): 별·왕관·양 머리띠·천사 날개·구유 등 A4 PDF 무료 도안
- [오늘의 말씀]({SITE}/today/): 매일 바뀌는 한 구절과 해설
- [말씀 뽑기]({SITE}/verse/): 주제별 구절 카드
- [교사 허브]({SITE}/teachers/): 주일학교·구역 공과 자료 검색
- [퍼즐 목록]({SITE}/list.html): 성경 가로세로 낱말 퍼즐
- [콘텐츠 제작 원칙]({SITE}/editorial-policy.html)
"""
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "llms.txt"), "w", encoding="utf-8").write(t)
