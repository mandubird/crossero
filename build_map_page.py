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
    title = "성경 지도 - 성경 속 지명 오늘의 위치와 사진 | 십자가로세로"
    desc = "예루살렘, 베들레헴, 갈릴리 바다, 여리고 등 성경 속 지명을 지도 위에서 확인하세요. 오늘의 위치와 현재 사진, 성경 구절 수를 함께 볼 수 있어요."
    pts = []
    for slug, g in GEO.items():
        e = BY_SLUG.get(slug)
        if not e:
            continue
        pts.append({"slug": slug, "name": e["name"], "sub": e["sub"], "lat": g["lat"], "lon": g["lon"],
                    "where": g["where"], "img": g.get("img"), "verses": g["verses"]})
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage", "name": "성경 지도", "description": desc,
        "inLanguage": "ko", "url": SITE + path}, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld).replace("</head>", EXTRA_HEAD, 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › 성경 지도</div>')
    out.append('<h1>성경 지도</h1><div class="sub">성경 속 지명이 지금은 어디에 있을까요?</div>')
    out.append('<div class="summary">핀을 누르면 그 지명의 오늘의 위치와 사진, 성경사전 항목으로 이동하는 링크를 볼 수 있습니다. '
               '위치는 학자들의 식별을 모은 OpenBible.info 성경 지오코딩 데이터(CC BY 4.0)를 바탕으로 하며, 일부는 학설에 따라 달라질 수 있습니다.</div>')
    out.append('<div class="dsearch" style="margin:12px 0 4px"><input id="mq" type="search" placeholder="🔍 지명 찾기 (예: 예루살렘, 갈릴리, 에베소)" autocomplete="off" style="width:100%;box-sizing:border-box;padding:13px 16px;font-size:16px;border:2px solid #cfe0f7;border-radius:14px;font-family:inherit"><div class="dres" id="mres"></div></div>')
    out.append('<div><button class="mbtn" data-v="holy">이스라엘 지역</button><button class="mbtn" data-v="all">전체 보기</button></div>')
    out.append('<div id="bmap" role="application" aria-label="성경 지명 지도"></div>')
    out.append('<div style="font-size:12px;color:#7b8794">지도 © <a href="https://www.openstreetmap.org/copyright" rel="noopener nofollow">OpenStreetMap</a> 기여자 · '
               '데이터 <a href="https://github.com/openbibleinfo/Bible-Geocoding-Data" rel="noopener nofollow">OpenBible.info</a> CC BY 4.0</div>')
    from build_routes import ROUTES
    from pilgrim_banner import banner as _pb
    out.append(_pb("map"))
    out.append('<div class="idx-section"><h2>바울의 여행 경로</h2><div class="cards">' + "".join(
        f'<a class="card" href="/dictionary/map/{r["slug"]}.html"><b>{esc(r["short"])}</b><span>{esc(r["ref"])}</span></a>' for r in ROUTES) + "</div></div>")
    out.append(f'<div class="idx-section"><h2>지명 목록 ({len(pts)})</h2><div class="cards">' + "".join(
        f'<a class="card" href="/dictionary/{p["slug"]}.html"><b>{esc(p["name"])}</b><span>{esc(p["where"])}</span></a>' for p in pts)
        + "</div></div>")
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>')
    out.append("<script>(function(){var P=" + json.dumps(pts, ensure_ascii=False) + ";" + MAP_JS + "})();</script>")
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)
