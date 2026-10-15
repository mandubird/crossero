# -*- coding: utf-8 -*-
"""사도행전 바울의 여행 경로 지도 페이지(/dictionary/map/paul-*.html)."""
import json

from dictionary_routes_data import PLACES
from dictionary_geo_data import GEO

_G_NAMES = {"nazareth": "나사렛", "bethlehem": "베들레헴", "jerusalem": "예루살렘", "jordan-river": "요단강", "cana": "가나", "capernaum": "가버나움",
            "sea-of-galilee": "갈릴리 바다", "bethsaida": "벳새다", "tyre": "두로", "caesarea-philippi": "가이사랴 빌립보", "samaria": "사마리아",
            "bethany": "베다니", "jericho": "여리고", "mount-of-olives": "감람산", "gethsemane": "겟세마네", "golgotha": "골고다", "tiberias": "디베랴"}
for _k, _n in _G_NAMES.items():
    PLACES.setdefault("g_" + _k, {"name": _n, "lat": GEO[_k]["lat"], "lon": GEO[_k]["lon"], "dict": _k, "modern": GEO[_k]["modern"]})
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


JESUS_ROUTES = [
 {"slug": "jesus-birth", "group": "jesus", "name": "예수님의 탄생과 유년기 경로", "short": "탄생과 유년기", "ref": "마태복음 1–2장, 누가복음 1–2장", "when": "주전 6~4년경(학설에 따라 다름)",
  "color": "#2563eb",
  "intro": "천사의 수태 고지를 받은 나사렛의 마리아가 호적 때문에 베들레헴으로 올라가 예수님을 낳고, 예루살렘 성전에서 봉헌한 뒤 다시 나사렛으로 돌아오기까지의 경로입니다. 복음서마다 기록한 사건이 달라 순서는 개략적으로 정리했습니다.",
  "summary": "나사렛에서 수태 고지를 받고 베들레헴에서 탄생하신 뒤 예루살렘 성전에서 봉헌되고 나사렛에서 자라셨습니다. 애굽으로 피신하신 일(마 2:13-15)은 위치를 특정하기 어려워 지도에서는 생략했습니다.",
  "steps": [("g_nazareth", "눅 1:26-38", "천사가 마리아에게 수태를 알림"), ("g_bethlehem", "눅 2:1-7", "호적을 하러 올라가 예수님을 낳음"), ("g_jerusalem", "눅 2:22-38", "성전에서 봉헌, 시므온과 안나를 만남"),
            ("g_bethlehem", "마 2:1-12", "동방 박사들의 경배(시기는 학설이 갈림)"), ("g_nazareth", "마 2:23, 눅 2:39", "나사렛으로 돌아와 자람"), ("g_jerusalem", "눅 2:41-52", "열두 살 때 성전에서 선생들과 이야기함"),
            ("g_nazareth", "눅 2:51-52", "부모를 순종하며 자람")]},
 {"slug": "jesus-galilee", "group": "jesus", "name": "예수님의 갈릴리 사역 경로", "short": "갈릴리 사역", "ref": "마태복음 3–17장, 마가복음 1–9장 등", "when": "주후 27~29년경",
  "color": "#059669",
  "intro": "요단강에서 세례를 받으신 예수님이 갈릴리 바다 주변에서 하나님 나라를 선포하고 제자를 부르며 병자를 고치신 경로입니다. 복음서 사이에 사건 순서가 다르게 기록되어 있어 대표적인 장소를 중심으로 정리했습니다.",
  "summary": "세례 후 가나와 가버나움, 갈릴리 바다 주변에서 사역하시고, 두로 지방과 가이사랴 빌립보까지 이르러 제자들의 고백을 들으셨습니다.",
  "steps": [("g_jordan-river", "마 3:13-17", "요한에게 세례를 받으심"), ("g_cana", "요 2:1-11", "혼인 잔치에서 첫 표적(위치는 학설이 갈림)"), ("g_capernaum", "마 4:13-17", "가버나움에 거처를 정하고 가르치기 시작하심"),
            ("g_sea-of-galilee", "마 4:18-22", "베드로와 안드레 등 제자들을 부르심"), ("g_nazareth", "눅 4:16-30", "고향에서 배척당하심"), ("g_capernaum", "막 2:1-12", "중풍병자를 고치심"),
            ("g_bethsaida", "눅 9:10-17", "벳새다 근처에서 오천 명을 먹이심"), ("g_tyre", "마 15:21-28", "두로 지방 가나안 여인의 믿음"), ("g_caesarea-philippi", "마 16:13-20", "베드로의 신앙 고백"),
            ("g_capernaum", "마 17:24-27", "가버나움으로 돌아오심")]},
 {"slug": "jesus-to-jerusalem", "group": "jesus", "name": "예수님의 예루살렘 여정 경로", "short": "예루살렘 여정", "ref": "누가복음 9:51–19:28, 요한복음 11장", "when": "주후 29~30년경",
  "color": "#d97706",
  "intro": "누가복음은 예수님이 예루살렘으로 올라가시기로 굳게 결심하신 때(눅 9:51)부터 입성 직전까지를 긴 여정으로 기록합니다. 이 여정에서 사마리아, 베다니, 여리고의 이야기가 이어집니다.",
  "summary": "갈릴리를 떠나 사마리아를 지나 베다니와 여리고를 거쳐 예루살렘으로 향하시는 경로입니다. 누가복음의 여정은 시간순 지도라기보다 주제별 기록으로 읽는 견해도 많습니다.",
  "steps": [("g_capernaum", "눅 9:51", "예루살렘으로 올라가기로 굳게 결심하심"), ("g_samaria", "눅 9:52-56", "사마리아 마을에서 영접받지 못하심"), ("g_bethany", "눅 10:38-42, 요 11:1-44", "마르다와 마리아의 집, 나사로를 살리심"),
            ("g_jericho", "눅 18:35–19:10", "맹인을 고치시고 삭개오를 만나심"), ("g_jerusalem", "눅 19:28", "예루살렘을 향해 올라가심")]},
 {"slug": "jesus-passion", "group": "jesus", "name": "예수님의 십자가 주간과 부활 경로", "short": "십자가 주간", "ref": "마태복음 21–28장 등", "when": "주후 30년경(또는 33년)",
  "color": "#9333ea",
  "intro": "예루살렘 입성부터 십자가, 부활, 승천까지 마지막 한 주와 이후의 경로입니다. 감람산에서 시작해 예루살렘과 겟세마네, 골고다를 지나 갈릴리에서 제자들을 다시 만나시고 감람산에서 승천하셨습니다.",
  "summary": "종려주일의 입성, 최후의 만찬, 겟세마네 기도, 재판과 십자가, 부활, 갈릴리에서의 현현과 승천으로 이어집니다. 십자가의 해는 주후 30년 또는 33년으로 학설이 나뉩니다.",
  "steps": [("g_jericho", "눅 19:1-10", "여리고를 지나 예루살렘으로 가심"), ("g_bethany", "요 12:1-8", "마리아가 향유를 부음"), ("g_mount-of-olives", "마 21:1-7", "나귀를 타고 입성을 준비하심"),
            ("g_jerusalem", "마 21:8-17", "예루살렘 입성과 성전 정화"), ("g_jerusalem", "마 26:17-30", "다락방에서 최후의 만찬"), ("g_gethsemane", "마 26:36-46", "겟세마네에서 기도하심"),
            ("g_jerusalem", "마 26:57–27:26", "재판을 받으심"), ("g_golgotha", "마 27:33-50", "십자가에 못 박히심"), ("g_golgotha", "마 27:57-61", "요셉의 새 무덤에 장사됨"),
            ("g_sea-of-galilee", "요 21:1-14", "갈릴리 바다에서 제자들에게 나타나심"), ("g_mount-of-olives", "행 1:9-12", "감람산에서 승천하심(누가복음은 베다니 앞)")]},
]
ROUTES += JESUS_ROUTES
for _r in ROUTES:
    _r.setdefault("group", "paul")


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
    if r["group"] == "paul":
        from pilgrim_banner import banner as _pb
        out.append(_pb(r["slug"], "route2" if r["slug"] == "paul-journey-2" else "default"))
    out.append("<h2>방문한 곳 순서</h2><ol class=\"steps\">" + "".join(
        f'<li><b>{_esc(p["name"])}</b> <span class="sref">{"행 " if r["group"] == "paul" else ""}{_esc(p["ref"])}</span><br><span class="snote">{_esc(p["note"])} · 오늘의 {_esc(p["modern"])} 일대</span></li>' for p in pts) + "</ol>")
    out.append("<h2>자주 묻는 질문</h2>" + "".join(f'<div class="faq"><b>Q. {_esc(q)}</b><p>{_esc(a)}</p></div>' for q, a in faq))
    out.append("<h2>다른 여행 경로</h2><div class=\"cards\">" + "".join(
        f'<a class="card" href="/dictionary/map/{o["slug"]}.html"><b>{_esc(o["short"])}</b><span>{_esc(o["ref"])}</span></a>' for o in ROUTES if o["slug"] != r["slug"] and o["group"] == r["group"])
        + '<a class="card" href="/dictionary/map/"><b>성경 지도</b><span>지명의 오늘의 위치</span></a></div>')
    if r["group"] == "paul" and "paul" in BY_SLUG:
        out.append('<p style="margin-top:18px">바울의 생애와 편지는 <a href="/dictionary/paul.html">바울 인물 항목</a>에서 볼 수 있습니다.</p>')
    elif "jesus" in BY_SLUG:
        out.append('<p style="margin-top:18px">예수님에 대한 더 자세한 소개는 <a href="/dictionary/jesus.html">예수 그리스도 항목</a>과 <a href="/dictionary/timeline/jesus.html">예수님의 시대 연대표</a>에서 볼 수 있습니다.</p>')
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>')
    out.append("<script>(function(){var P=" + json.dumps(pts, ensure_ascii=False) + ";var C=" + json.dumps(r["color"]) + ";var PFX=" + json.dumps("행 " if r["group"] == "paul" else "") + ";" + """
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
