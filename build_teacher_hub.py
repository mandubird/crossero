# -*- coding: utf-8 -*-
"""교사 허브(검색 + 대상별 목록 + 격려 글) 생성. 실행: python3 build_teacher_hub.py"""
import json
import os
import re
import urllib.parse

import build_dictionary as bd
from build_dictionary import esc, head, FOOTER, NAV, ROOT, ENTRIES, SITE

OUT = os.path.join(ROOT, "teachers")
PLAIN_NAV = NAV.replace(' nav-active', '')


def load_puzzles():
    items = []
    for f in ("data.js", "data_bible_extra.js", "data_christian_figures.js"):
        s = open(os.path.join(ROOT, f), encoding="utf-8").read()
        for m in re.finditer(r'"([a-z]{3}_\d{3})":\s*\{\s*title:\s*"([^"]+)",\s*category:\s*"([^"]*)",\s*meta:\s*"([^"]*)"', s):
            tags = [t.strip() for t in m.group(3).split(",") if t.strip()]
            items.append({"id": m.group(1), "title": m.group(2), "tags": tags, "meta": m.group(4)})
    seen, out = set(), []
    for it in items:
        if it["id"] not in seen:
            seen.add(it["id"])
            out.append(it)
    return out


PUZZLES = load_puzzles()
MANIFEST = json.load(open(os.path.join(ROOT, "published_manifest.json"), encoding="utf-8"))

AUDIENCES = [
    {"tag": "주일학교용", "slug": "sunday-school-puzzles", "name": "주일학교",
     "title": "주일학교 성경 퍼즐 모음 - 공과 복습용 가로세로 낱말퀴즈",
     "desc": "주일학교 공과 마무리, 성경 복습, 방과 후 활동에 쓰기 좋은 성경 가로세로 퍼즐 모음. 인물·사건·책별로 골라 무료로 풀어 보세요.",
     "intro": "주일학교 수업에서 퍼즐은 설교 내용을 복습하고 아이들의 집중을 되살리는 데 가장 손쉬운 도구입니다. 아래 퍼즐은 성경 인물과 사건 중심으로 단어가 익숙한 편이어서 초등 고학년부터 어렵지 않게 풀 수 있습니다.",
     "tips": ["수업 마지막 5~10분에 짝 활동으로 풀게 하면 정답 찾는 과정이 자연스러운 복습이 됩니다.", "화면에 띄워 함께 풀 때는 한 사람이 읽고 한 사람이 입력하도록 역할을 나누면 참여가 고르게 됩니다.", "저학년은 힌트 목록을 교사가 먼저 읽어 주고, 정답 글자 수만 알려 주는 방식으로 난이도를 낮출 수 있습니다.", "다 푼 뒤에는 성경사전의 해당 인물·사건 항목을 읽으며 이야기로 다시 연결해 주세요."]},
    {"tag": "중고등부용", "slug": "youth-puzzles", "name": "중고등부",
     "title": "중고등부 성경 퍼즐 모음 - 청소년 성경공부 가로세로 퀴즈",
     "desc": "중고등부 예배 후 활동, 소그룹 모임, 성경 통독 복습에 쓰기 좋은 성경 가로세로 퍼즐 모음입니다.",
     "intro": "중고등부는 단순 암기보다 팀 활동과 약간의 경쟁 요소가 있을 때 반응이 좋습니다. 아래 퍼즐은 책별 핵심 단어와 인물, 교회 역사까지 다양하게 있어 팀을 나눠 정답 수를 겨루는 방식으로 활용하기 좋습니다.",
     "tips": ["팀을 나눠 같은 퍼즐을 풀고 시간과 정답 수를 겨루면 분위기가 살아납니다.", "정답을 맞힌 단어 중 하나를 골라 그 구절을 함께 찾아 읽게 하면 퍼즐이 말씀 읽기로 이어집니다.", "신앙 배경이 다양한 반이라면 새신자용 퍼즐과 섞어 팀을 구성해 부담을 줄일 수 있습니다."]},
    {"tag": "새신자용", "slug": "newcomer-puzzles", "name": "새신자",
     "title": "새신자·초신자용 성경 퍼즐 모음 - 성경 기초 가로세로 퀴즈",
     "desc": "성경이 낯선 새신자와 초신자를 위한 쉬운 성경 가로세로 퍼즐 모음. 대표 인물·사건과 기본 용어를 퍼즐로 익혀 보세요.",
     "intro": "성경을 처음 접하는 분에게는 익숙한 인물과 사건부터 가볍게 시작하는 것이 부담이 적습니다. 아래 퍼즐은 노아, 모세, 다윗처럼 널리 알려진 이야기와 기본 용어 중심이라 새신자 교육이나 환영 모임에서 쓰기에 좋습니다.",
     "tips": ["답을 모르는 분이 위축되지 않도록 '정답보다 힌트를 읽으며 이야기를 나누는 것'이 목적이라고 먼저 말해 주세요.", "한 번에 퍼즐 하나만 하고, 끝난 뒤 성경사전에서 궁금한 인물 하나만 더 읽어 보게 하면 부담이 적습니다."]},
    {"tag": "리더용", "slug": "leader-puzzles", "name": "교사·리더",
     "title": "교사·구역 리더용 성경 퍼즐 모음 - 모임 시작 활동 가로세로 퀴즈",
     "desc": "구역·셀·소그룹 모임을 시작하거나 성경 지식을 점검할 때 쓰기 좋은 성경 가로세로 퍼즐 모음입니다.",
     "intro": "구역이나 셀 모임에서 본격적인 나눔에 들어가기 전, 가볍게 마음을 여는 활동으로 퍼즐을 쓰는 리더들이 많습니다. 아래 퍼즐은 책별·주제별로 나뉘어 있어 그날 본문과 맞는 것을 골라 쓰기 쉽습니다.",
     "tips": ["모임 전날 퍼즐을 먼저 풀어 보고 막히는 힌트를 메모해 두면 진행이 매끄럽습니다.", "본문과 같은 책의 퍼즐을 고르면 모임 주제와 자연스럽게 이어집니다."]},
]


def purl(i):
    return f"/play.html?id={i}"


def page(path, title, desc, body, ld="", scripts=""):
    out = [head(title, desc, path, ld).replace(NAV, PLAIN_NAV).replace('og:type" content="article"', 'og:type" content="website"')]
    out.append('<main class="wrap">')
    out.append(body)
    out.append('</main>')
    out.append('<div id="crs-subscribe"></div>')
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>' + scripts + '\n</body>\n</html>\n')
    return "\n".join(out)


def card_list(items):
    return '<div class="cards">' + "".join(
        f'<a class="card" href="{purl(p["id"])}" data-ga="teacher_pick_puzzle" data-ga-label="{p["id"]}"><b>{esc(p["title"])}</b><span>{esc(p["meta"])}</span></a>'
        for p in items) + "</div>"


def audience_page(a):
    items = [p for p in PUZZLES if a["tag"] in p["tags"]]
    faq = [(f"{a['name']} 모임에서 성경 퍼즐은 어떻게 쓰나요?", a["tips"][0]),
           ("퍼즐은 무료인가요?", "퍼즐 풀이는 회원가입 없이 무료입니다. 인쇄 기능은 후원 이용권을 인증한 뒤 사용할 수 있고, 교회 시범 이용 신청도 받고 있습니다.")]
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faq]}, ensure_ascii=False) + "</script>"
    body = f"""
<div class="crumb"><a href="/">홈</a> › <a href="/teachers/">교사 허브</a> › {esc(a['name'])}용 퍼즐</div>
<span class="badge">{esc(a['name'])}</span>
<h1>{esc(a['name'])} 성경 퍼즐 모음</h1>
<div class="sub">총 {len(items)}개 · 회원가입 없이 무료로 풀 수 있습니다</div>
<div class="summary">{esc(a['intro'])}</div>
<h2>이렇게 활용해 보세요</h2>
<ul class="refs">{''.join(f'<li>{esc(t)}</li>' for t in a['tips'])}</ul>
<h2>퍼즐 목록 ({len(items)}개)</h2>
{card_list(items)}
<p class="note">교회 단위로 사용하시려면 <a href="/church-bulletin-puzzle.html">교회·주일학교 활용 가이드</a>를 확인해 주세요. 모르는 인물이나 책은 <a href="/dictionary/">성경사전</a>에서 먼저 읽어 볼 수 있습니다.</p>
<div class="faq"><h2>자주 묻는 질문</h2>{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(ans)}</p></details>' for q, ans in faq)}</div>
"""
    return page(f"/teachers/{a['slug']}.html", a["title"] + " | 십자가로세로", a["desc"], body, ld)


def search_index():
    rows = []
    for p in PUZZLES:
        rows.append({"t": "퍼즐", "n": p["title"], "u": purl(p["id"]), "g": " ".join(p["tags"]), "d": p["meta"]})
    for e in ENTRIES:
        label = "책 요약" if e["type"] == "성경 책" else "사전"
        rows.append({"t": label, "n": (e["name"] + " 요약") if e["type"] == "성경 책" else e["name"],
                     "u": f"/dictionary/{e['slug']}.html", "g": e["type"] + " " + e["sub"], "d": e["summary"][:70]})
    for m in MANIFEST:
        rows.append({"t": "게시글", "n": m["title"], "u": "/posts/" + urllib.parse.quote(m["slug"]) + ".html", "g": "", "d": m["date"]})
    return rows


def hub():
    counts = {a["tag"]: sum(1 for p in PUZZLES if a["tag"] in p["tags"]) for a in AUDIENCES}
    aud_cards = '<div class="cards">' + "".join(
        f'<a class="card" href="/teachers/{a["slug"]}.html"><b>{esc(a["name"])}용 퍼즐</b><span>{counts[a["tag"]]}개 · {esc(a["desc"][:36])}…</span></a>' for a in AUDIENCES) + "</div>"
    body = f"""
<div class="crumb"><a href="/">홈</a> › 교사 허브</div>
<span class="badge">교사·리더</span>
<h1>교사 허브 - 공과 자료 찾기</h1>
<div class="sub">퍼즐, 성경사전, 게시글을 한 번에 검색하세요</div>
<div class="summary">이번 주 공과에 쓸 자료를 빨리 찾고 싶은 교사와 리더를 위해 만들었습니다. 본문 이름이나 인물, 주제를 입력하면 퍼즐·사전·게시글에서 한꺼번에 찾아 줍니다. 예) 다윗, 요나, 십계명, 로마서</div>

<div id="hub-search" style="margin:18px 0 6px;">
  <input id="q" type="search" placeholder="인물·책·주제 검색 (예: 다윗, 시편, 십계명)" aria-label="자료 검색" style="width:100%;padding:14px 16px;border:2px solid #bcd3f0;border-radius:12px;font-size:16px;">
  <div id="chips" style="margin:10px 0;display:flex;gap:8px;flex-wrap:wrap;">
    <button class="chip on" data-t="">전체</button>
    <button class="chip" data-t="퍼즐">퍼즐</button>
    <button class="chip" data-t="사전">사전</button>
    <button class="chip" data-t="책 요약">책 요약</button>
    <button class="chip" data-t="게시글">게시글</button>
  </div>
  <div id="count" class="note" style="margin:6px 0 10px;"></div>
  <div id="results" class="cards"></div>
</div>

<h2>대상별 퍼즐 모음</h2>
{aud_cards}

<h2>교사를 위한 글</h2>
<div class="cards">
  <a class="card" href="/teachers/encouragement.html"><b>가르치다 지칠 때 - 주일학교 교사를 위한 격려</b><span>번아웃, 인정, 동역자에 대한 이야기</span></a>
  <a class="card" href="/church-bulletin-puzzle.html"><b>교회·주일학교 활용 가이드</b><span>주보·공과·소그룹 활용법, 시범 이용 신청</span></a>
</div>
"""
    style = """<style>
.chip{padding:7px 14px;border:1px solid #bcd3f0;background:#fff;color:#0b5cad;border-radius:20px;font-size:14px;cursor:pointer;}
.chip.on{background:#0073e6;color:#fff;border-color:#0073e6;}
.tag{display:inline-block;font-size:11px;background:#e8f1ff;color:#0b5cad;padding:1px 8px;border-radius:10px;margin-bottom:4px;}
</style>"""
    js = """<script>
(function(){
  var data=[],type='',q=document.getElementById('q'),res=document.getElementById('results'),cnt=document.getElementById('count');
  function norm(s){return (s||'').toLowerCase().replace(/\\s+/g,'');}
  function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function render(){
    var k=norm(q.value),rows=data;
    if(type) rows=rows.filter(function(r){return r.t===type;});
    if(k){
      rows=rows.map(function(r){
        var n=norm(r.n),g=norm(r.g),d=norm(r.d),s=0;
        if(n===k)s=100;else if(n.indexOf(k)===0)s=80;else if(n.indexOf(k)>-1)s=60;else if(g.indexOf(k)>-1)s=30;else if(d.indexOf(k)>-1)s=10;
        return {r:r,s:s};
      }).filter(function(x){return x.s>0;}).sort(function(a,b){return b.s-a.s;}).map(function(x){return x.r;});
    } else { rows=rows.filter(function(r){return r.t!=='게시글';}); }
    cnt.textContent=k?('검색 결과 '+rows.length+'건'):'검색어를 입력하면 결과가 나타납니다. 아래는 추천 자료입니다.';
    var show=rows.slice(0,k?60:12);
    res.innerHTML=show.map(function(r){return '<a class="card" href="'+r.u+'" data-ga="hub_result_click" data-ga-label="'+esc(r.t)+'"><span class="tag">'+esc(r.t)+'</span><b>'+esc(r.n)+'</b><span>'+esc(r.d)+'</span></a>';}).join('')||'<div class="note">검색 결과가 없습니다. 다른 단어로 찾아보세요.</div>';
  }
  fetch('/search-index.json').then(function(r){return r.json();}).then(function(j){data=j;render();});
  var timer;q.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(function(){render();if(window.crsTrack&&q.value)window.crsTrack('hub_search',{term:q.value});},350);});
  document.getElementById('chips').addEventListener('click',function(e){
    if(!e.target.classList.contains('chip'))return;
    [].forEach.call(document.querySelectorAll('.chip'),function(c){c.classList.remove('on');});
    e.target.classList.add('on');type=e.target.getAttribute('data-t');render();
  });
})();
</script>"""
    title = "교사 허브 - 주일학교·구역 공과 자료 검색 | 십자가로세로"
    desc = "주일학교 교사와 구역 리더를 위한 자료 검색. 성경 퍼즐, 성경사전, 게시글을 인물·책·주제로 한 번에 찾아보세요."
    return page("/teachers/", title, desc, body + style, "", js)


def encouragement():
    secs = [
        ("지친다는 것은 약해서가 아닙니다", [
            "매주 공과를 준비하고, 아이들을 살피고, 부모와 소통하고, 주말 시간을 내어놓는 일은 생각보다 많은 에너지를 씁니다. 정작 본인은 예배에 온전히 집중하지 못한 채 아이들을 돌보다 끝나는 날도 많습니다. 그래서 가르치는 사람이 먼저 지치는 것은 믿음이 부족해서가 아니라 오래 헌신해 온 사람에게 자연스럽게 찾아오는 일입니다.",
            "먼저 이 사실을 스스로에게 허락해 주세요. 피곤하다고 느끼는 것은 잘못이 아닙니다. 갈라디아서 6장 9절은 선을 행하다가 낙심하지 말라고 권하면서, 포기하지 않으면 때가 이르매 거두리라고 말합니다. 지금 보이지 않는 열매가 있다는 약속입니다."]),
        ("보이지 않는 열매를 기억하기", [
            "아이들은 교사가 가르친 내용을 당장 기억하지 못하는 것처럼 보이지만, 환영받은 경험과 어른이 기도해 주던 기억은 오래 남습니다. 많은 사람이 어린 시절 주일학교에서 배운 구절보다 선생님의 표정과 따뜻한 한마디를 먼저 떠올립니다.",
            "이번 주에 한 아이의 이름을 불러 주었다면, 한 번 더 웃어 주었다면 그것으로 충분히 가르친 것입니다. 사역의 성과를 아이들이 배운 양으로만 재지 않아도 됩니다."]),
        ("준비 부담을 줄이는 현실적인 방법", [
            "공과를 처음부터 끝까지 새로 만들려고 하지 마세요. 교재의 핵심 한 가지를 정해 말씀 읽기, 이야기 나누기, 짧은 활동 세 단계로만 구성해도 수업은 충분히 살아납니다. 활동 단계에서는 퍼즐이나 퀴즈처럼 준비가 적게 드는 자료를 활용하면 시간을 크게 아낄 수 있습니다.",
            "혼자 모든 걸 하려 하지 않는 것도 중요합니다. 같은 부서 교사들과 자료를 나누고, 이번 주 한 사람이 활동을 맡는 식으로 돌아가며 준비하면 부담이 눈에 띄게 줄어듭니다."]),
        ("혼자 감당하지 않기", [
            "교사 모임이 단순한 회의가 아니라 서로의 어려움을 이야기하고 기도해 주는 자리가 되면 오래 사역할 힘이 생깁니다. 완벽한 해답을 주지 않아도 됩니다. '이번 주 가장 힘든 일이 무엇이었는지'를 돌아가며 한 문장씩 나누는 것만으로도 위로가 됩니다.",
            "가까이에 그런 자리가 없다면 같은 처지의 교사 한두 명과 짧게 안부를 묻는 것부터 시작해 보세요. 십자가로세로도 이런 교사들의 작은 부담을 덜어 드리는 도구가 되려고 합니다."]),
        ("이번 주에 할 수 있는 작은 일", [
            "한 가지만 하셔도 좋습니다. 이번 주 수업에서 가장 어려웠던 순간을 짧게 적어 보고 그 아이를 위해 기도해 보세요. 아니면 다음 주 활동으로 퍼즐 하나만 정해 두고 나머지 준비 시간을 쉬는 데 쓰셔도 됩니다. 지금 하고 계신 일은 헛되지 않습니다.",
        ]),
    ]
    body = f"""
<div class="crumb"><a href="/">홈</a> › <a href="/teachers/">교사 허브</a> › 격려의 글</div>
<span class="badge">교사를 위한 글</span>
<h1>가르치다 지칠 때 - 주일학교 교사를 위한 격려</h1>
<div class="sub">번아웃, 인정, 동역자에 대하여</div>
<div class="summary">주일학교 교사와 구역 리더가 가장 자주 마주치는 어려움은 자료 준비보다 마음의 피로입니다. 이 글은 지친 마음을 먼저 돌보고, 준비 부담을 줄이는 현실적인 방법을 함께 생각해 보려고 썼습니다.</div>
{''.join(f'<h2>{esc(h)}</h2>' + ''.join(f'<p>{esc(p)}</p>' for p in ps) for h, ps in secs)}
<a class="cta" href="/teachers/sunday-school-puzzles.html" data-ga="encouragement_to_hub">🧩 이번 주 활동용 퍼즐 고르기<small>준비 시간을 줄여 주는 주일학교 퍼즐 모음</small></a>
"""
    return page("/teachers/encouragement.html", "주일학교 교사 번아웃, 지칠 때 읽는 격려의 글 | 십자가로세로",
                "주일학교 교사와 구역 리더가 가르치다 지쳤을 때 읽는 글. 번아웃을 인정하고, 준비 부담을 줄이고, 혼자 감당하지 않는 방법을 정리했습니다.", body)


def sitemap(paths):
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- TEACH-START -->.*?<!-- TEACH-END -->", "", s, flags=re.S)
    block = "\n  <!-- TEACH-START -->\n" + "\n".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
        for u in paths) + "\n  <!-- TEACH-END -->\n"
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    os.makedirs(OUT, exist_ok=True)
    paths = ["/teachers/", "/teachers/encouragement.html"]
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(hub())
    open(os.path.join(OUT, "encouragement.html"), "w", encoding="utf-8").write(encouragement())
    for a in AUDIENCES:
        open(os.path.join(OUT, f"{a['slug']}.html"), "w", encoding="utf-8").write(audience_page(a))
        paths.append(f"/teachers/{a['slug']}.html")
    rows = search_index()
    open(os.path.join(ROOT, "search-index.json"), "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, separators=(",", ":")))
    sitemap(paths)
    print(f"교사 허브 생성: 페이지 {len(paths)}개, 검색 색인 {len(rows)}건")


if __name__ == "__main__":
    main()
