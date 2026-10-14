# -*- coding: utf-8 -*-
"""사도행전 바울의 여행 경로 지도 페이지(/dictionary/map/paul-*.html)."""
import json

from dictionary_routes_data import PLACES
from build_map_page import EXTRA_HEAD

ROUTES = [
 {"slug": "paul-journey-1", "name": "바울 1차 전도 여행", "short": "1차 전도 여행", "ref": "사도행전 13:1–14:28", "when": "주후 46~48년경",
  "color": "#0073e6",
  "intro": "안디옥 교회가 바나바와 사울(바울)을 선교사로 파송하면서 시작된 첫 번째 전도 여행입니다. 구브로(키프로스)를 거쳐 오늘의 튀르키예 남부 내륙 도시들을 돌며 복음을 전했고, 이방인에게도 문이 열려 있음이 분명해진 여행입니다.",
  "summary": "바나바, 마가 요한과 함께 구브로와 갈라디아 남부(비시디아 안디옥, 이고니온, 루스드라, 더베)를 순회하고 안디옥으로 돌아왔습니다.",
  "steps": [("antioch", "13:1-3", "교회의 파송을 받고 출발"), ("seleucia", "13:4", "배를 타고 구브로로"), ("salamis", "13:5", "유대인 회당에서 말씀을 전함"),
            ("paphos", "13:6-12", "총독 서기오 바울이 믿음"), ("perga", "13:13", "마가 요한이 예루살렘으로 돌아감"), ("pisidia", "13:14-50", "안식일 회당 설교, 이방인에게로"),
            ("iconium", "13:51–14:5", "많은 사람이 믿으나 박해를 받음"), ("lystra", "14:6-19", "앉은뱅이를 고침, 돌에 맞음"), ("derbe", "14:20-21", "복음을 전하고 많은 제자를 얻음"),
            ("lystra", "14:21", "돌아오며 제자들을 굳게 함"), ("iconium", "14:21", "장로를 세움"), ("pisidia", "14:21", "교회를 돌아봄"), ("perga", "14:25", "말씀을 전함"),
            ("attalia", "14:25", "항구에서 배를 탐"), ("antioch", "14:26-28", "돌아와 선교 보고")]},
 {"slug": "paul-journey-2", "name": "바울 2차 전도 여행", "short": "2차 전도 여행", "ref": "사도행전 15:36–18:22", "when": "주후 49~52년경",
  "color": "#d97706",
  "intro": "바울이 실라와 함께 1차 여행에서 세운 교회들을 다시 돌아보며 시작한 여행입니다. 드로아에서 마케도냐인의 환상을 본 뒤 유럽으로 건너가 빌립보, 데살로니가, 아덴, 고린도에서 복음을 전했습니다.",
  "summary": "디모데가 합류하고 드로아에서 마게도냐로 건너가 유럽 선교가 시작되었습니다. 고린도에서는 1년 6개월을 머물렀습니다.",
  "steps": [("antioch", "15:36-41", "바나바와 헤어져 실라와 출발"), ("derbe", "16:1", "교회들을 굳게 함"), ("lystra", "16:1-5", "디모데가 합류"),
            ("troas", "16:8-10", "마게도냐인의 환상"), ("neapolis", "16:11", "유럽 땅에 첫발"), ("philippi", "16:12-40", "루디아의 회심, 감옥의 간수"),
            ("amphipolis", "17:1", "지나감"), ("apollonia", "17:1", "지나감"), ("thessalonica", "17:1-9", "회당에서 세 안식일 강론"), ("berea", "17:10-14", "날마다 성경을 상고함"),
            ("athens", "17:16-34", "아레오바고 설교"), ("corinth", "18:1-18", "1년 6개월 체류, 아굴라·브리스길라를 만남"), ("ephesus", "18:19-21", "잠시 들러 강론"),
            ("caesarea", "18:22", "상륙"), ("jerusalem", "18:22", "교회에 문안"), ("antioch", "18:22", "돌아옴")]},
 {"slug": "paul-journey-3", "name": "바울 3차 전도 여행", "short": "3차 전도 여행", "ref": "사도행전 18:23–21:17", "when": "주후 53~57년경",
  "color": "#059669",
  "intro": "바울이 갈라디아와 브루기아의 제자들을 굳게 한 뒤 에베소에 오래 머물며 사역한 여행입니다. 마게도냐와 헬라(그리스)를 다시 거쳐 예루살렘으로 올라가는 길에 에베소 장로들과 작별했습니다.",
  "summary": "에베소에서 약 3년을 사역했고, 고린도에서 로마서를 쓴 것으로 전해집니다. 예루살렘 방문이 이후 체포와 로마 압송으로 이어집니다.",
  "steps": [("antioch", "18:23", "얼마 있다가 떠남"), ("ephesus", "19:1-41", "약 3년 사역, 두란노 서원"), ("philippi", "20:1-6", "마게도냐를 거쳐 감"), ("corinth", "20:2-3", "헬라에서 석 달 체류"),
            ("philippi", "20:6", "무교절 후 배를 탐"), ("troas", "20:6-12", "유두고를 살림"), ("assos", "20:13-14", "걸어서 도착해 합류"), ("mitylene", "20:14", "항해"),
            ("miletus", "20:15-38", "에베소 장로들과 작별"), ("cos", "21:1", "항해"), ("patara", "21:1-2", "배를 갈아탐"), ("tyre", "21:3-6", "7일 머묾"),
            ("ptolemais", "21:7", "형제들에게 문안"), ("caesarea", "21:8-14", "빌립 집사의 집, 아가보의 예언"), ("jerusalem", "21:15-17", "형제들이 기쁘게 영접")]},
 {"slug": "paul-journey-rome", "name": "바울의 로마 압송 항해", "short": "로마 압송 항해", "ref": "사도행전 27:1–28:16", "when": "주후 59~60년경",
  "color": "#9333ea",
  "intro": "가이사랴에서 재판을 받던 바울이 가이사에게 상소하여 죄수의 신분으로 로마로 향한 항해입니다. 지중해에서 만난 유라굴로 광풍과 멜리데(몰타) 섬의 난파, 로마 도착까지가 사도행전의 마지막을 이룹니다.",
  "summary": "백부장 율리오의 호송으로 출발해 폭풍 속에서 14일을 표류하다 멜리데에서 겨울을 보내고, 이듬해 봄 로마에 도착했습니다.",
  "steps": [("caesarea", "27:1-2", "백부장 율리오에게 인계되어 출발"), ("sidon", "27:3", "친구들에게 가서 대접을 받음"), ("myra", "27:5-6", "알렉산드리아 배로 갈아탐"),
            ("cnidus", "27:7", "바람 때문에 지체됨"), ("fairhavens", "27:8-12", "그레데 섬 미항에 도착"), ("cauda", "27:16", "유라굴로 광풍 속에 가우다를 지남"),
            ("malta", "28:1-10", "난파 후 섬에 상륙, 석 달 체류"), ("syracuse", "28:12", "사흘 머묾"), ("puteoli", "28:13-14", "형제들을 만나 이레를 머묾"), ("rome", "28:14-16", "로마에 들어감")]},
]


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def render_route(r, head, FOOTER, SITE, BY_SLUG):
    path = f"/dictionary/map/{r['slug']}.html"
    title = f"{r['name']} 지도 - 경로와 방문 도시 | 십자가로세로"
    desc = f"{r['name']}({r['ref']}) 경로를 지도에서 따라가 보세요. 방문한 도시를 순서대로 보고 오늘의 위치와 해당 구절을 함께 확인할 수 있어요."
    pts = []
    for i, (k, ref, note) in enumerate(r["steps"], 1):
        p = PLACES[k]
        pts.append({"n": i, "key": k, "name": p["name"], "lat": p["lat"], "lon": p["lon"], "ref": ref, "note": note, "modern": p["modern"]})
    faq = [(f"{r['short']}은 언제, 어디를 다녔나요?", f"{r['summary']} (연대는 학자에 따라 다소 차이가 있습니다.)"),
           ("지도의 선은 실제 경로인가요?", "방문한 도시를 순서대로 직선으로 이은 개략적인 경로입니다. 실제 육로와 해로는 이와 다를 수 있습니다.")]
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "Article", "headline": f"{r['name']} 지도", "description": desc, "inLanguage": "ko",
         "author": {"@type": "Organization", "name": "십자가로세로"}, "mainEntityOfPage": SITE + path},
        {"@context": "https://schema.org", "@type": "Trip", "name": r["name"], "description": r["summary"], "inLanguage": "ko",
         "image": f"{SITE}/images/maps/{r['slug']}.png", "url": SITE + path,
         "itinerary": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": p["n"], "name": p["name"],
              "item": {"@type": "Place", "name": p["name"], "geo": {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lon"]}}}
             for p in pts]}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "성경사전", "item": SITE + "/dictionary/"},
            {"@type": "ListItem", "position": 3, "name": "성경 지도", "item": SITE + "/dictionary/map/"},
            {"@type": "ListItem", "position": 4, "name": r["name"], "item": SITE + path}]}))
    out = [head(title, desc, path, ld, f"{SITE}/images/maps/{r['slug']}.png").replace("</head>", EXTRA_HEAD, 1), '<main class="wrap">']
    out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › <a href="/dictionary/map/">성경 지도</a> › {_esc(r["short"])}</div>')
    out.append(f'<h1>{_esc(r["name"])}</h1><div class="sub">{_esc(r["ref"])} · {_esc(r["when"])}</div>')
    out.append(f'<div class="summary">{_esc(r["intro"])}</div>')
    out.append(f'<figure style="margin:14px 0"><img src="/images/maps/{r["slug"]}.png" width="1200" height="630" alt="{_esc(r["name"])} 경로 지도 - {_esc(r["ref"])}" style="width:100%;height:auto;border-radius:14px;display:block"></figure>')
    out.append('<div id="bmap" role="application" aria-label="바울의 여행 경로 지도(확대·이동 가능)"></div>')
    out.append('<div style="font-size:12px;color:#7b8794">선은 방문 순서를 잇는 개략적인 경로입니다. 지도 © <a href="https://www.openstreetmap.org/copyright" rel="noopener nofollow">OpenStreetMap</a> 기여자 · 위치 데이터 <a href="https://github.com/openbibleinfo/Bible-Geocoding-Data" rel="noopener nofollow">OpenBible.info</a> CC BY 4.0</div>')
    from pilgrim_banner import banner as _pb
    out.append(_pb(r["slug"], "route2" if r["slug"] == "paul-journey-2" else "default"))
    out.append("<h2>방문한 곳 순서</h2><ol class=\"steps\">" + "".join(
        f'<li><b>{_esc(p["name"])}</b> <span class="sref">행 {_esc(p["ref"])}</span><br><span class="snote">{_esc(p["note"])} · 오늘의 {_esc(p["modern"])} 일대</span></li>' for p in pts) + "</ol>")
    out.append("<h2>자주 묻는 질문</h2>" + "".join(f'<div class="faq"><b>Q. {_esc(q)}</b><p>{_esc(a)}</p></div>' for q, a in faq))
    out.append("<h2>다른 여행 경로</h2><div class=\"cards\">" + "".join(
        f'<a class="card" href="/dictionary/map/{o["slug"]}.html"><b>{_esc(o["short"])}</b><span>{_esc(o["ref"])}</span></a>' for o in ROUTES if o["slug"] != r["slug"])
        + '<a class="card" href="/dictionary/map/"><b>성경 지도</b><span>지명의 오늘의 위치</span></a></div>')
    if "paul" in BY_SLUG:
        out.append('<p style="margin-top:18px">바울의 생애와 편지는 <a href="/dictionary/paul.html">바울 인물 항목</a>에서 볼 수 있습니다.</p>')
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>')
    out.append("<script>(function(){var P=" + json.dumps(pts, ensure_ascii=False) + ";var C=" + json.dumps(r["color"]) + ";" + """
var m=L.map('bmap',{scrollWheelZoom:false});
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; OpenStreetMap'}).addTo(m);
var ll=P.map(function(p){return [p.lat,p.lon]});
L.polyline(ll,{color:C,weight:3,opacity:.8,dashArray:'6 6'}).addTo(m);
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var seen={};
P.forEach(function(p){
  var k=p.key; if(seen[k]){seen[k].push(p.n);return;} seen[k]=[p.n];
  var ic=L.divIcon({className:'',html:'<div style="background:'+C+';color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.4)">'+p.n+'</div>',iconSize:[26,26],iconAnchor:[13,13]});
  L.marker([p.lat,p.lon],{icon:ic}).addTo(m).bindPopup('<div class="pop"><b>'+esc(p.name)+'</b><br><span style="font-size:12px;color:#666">행 '+esc(p.ref)+'<br>'+esc(p.note)+'</span></div>').bindTooltip(p.n+'. '+p.name);
});
m.fitBounds(ll,{padding:[30,30]});
if(window.crsTrack)crsTrack('bible_route_view',{route:""" + json.dumps(r["slug"]) + """});
})();</script>""")
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)
