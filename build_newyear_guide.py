# -*- coding: utf-8 -*-
"""송구영신예배 말씀 뽑기 진행 가이드 생성. 실행: python3 build_newyear_guide.py
출력: verse/new-year/guide/index.html, sitemap.xml 의 NYGUIDE 구간"""
import json
import os
import re

import build_dictionary as bd
import build_verse as bv
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT

PATH = "/verse/new-year/guide/"
TITLE = "송구영신예배 말씀 뽑기 방법 - 준비물·진행 순서·카드 인쇄 가이드 | 십자가로세로"
DESC = "12월 31일 송구영신예배에서 새해 말씀 뽑기를 진행하는 방법을 정리했습니다. 말씀 상자 준비, 인원별 카드 수, 30분 진행 순서, 유의할 점, 무료 카드 인쇄까지 한 번에 확인하세요."

FAQ = [
    ("송구영신예배 말씀 뽑기는 성경적인가요?",
     "성경에 새해 말씀을 뽑으라고 정한 규례는 없습니다. 한 해를 시작하며 말씀 앞에 서는 신앙 습관으로 교회가 활용하는 순서이고, 뽑기라는 방식 자체보다 뽑은 말씀을 묵상하고 나누는 데 의미가 있습니다. 뽑힌 구절을 운세나 예언처럼 해석하지 않도록 사전에 안내하는 것이 좋습니다."),
    ("교인이 100명이면 카드를 몇 장 준비해야 하나요?",
     "참석 인원의 1.2배 정도를 권합니다. 100명이면 120장 안팎이고, A4 한 장에 8장씩 인쇄하면 15쪽입니다. 구절 수가 100가지 미만이면 같은 구절을 2~3장씩 인쇄하고 섞어서 상자에 담으면 됩니다."),
    ("뽑은 말씀이 마음에 들지 않으면 다시 뽑아도 되나요?",
     "교회마다 정하기 나름이지만 다시 뽑지 않는 것을 권합니다. 지금 내 형편과 맞지 않아 보이는 구절도 한 해 동안 묵상하면 다른 의미로 다가오는 경우가 많기 때문입니다. 다만 사전에 '한 번만 뽑습니다'라고 안내해 두면 혼란이 없습니다."),
    ("주일학교나 어린이는 어떻게 하나요?",
     "짧고 쉬운 구절 위주의 카드를 따로 모아 별도의 상자로 진행하세요. 글씨를 크게 인쇄하고, 뽑은 뒤 교사와 함께 소리 내어 읽고 한 문장으로 따라 말해 보게 하면 좋습니다."),
    ("카드는 무료로 만들어도 되나요?",
     "십자가로세로의 말씀 카드 인쇄 기능은 무료입니다. 교회·주일학교·소그룹에서의 비영리 사용은 자유롭게 하실 수 있고, 판매하지 않는 조건으로 이용해 주세요. 후원하시면 카드에서 십자가로세로 워터마크를 뺄 수 있습니다."),
    ("카드는 어떤 용지에 인쇄하면 좋나요?",
     "일반 A4 복사지(80g)도 가능하지만 120~200g 정도의 두꺼운 종이를 쓰면 접히지 않고 뽑기 쉽습니다. 교회 프린터가 두꺼운 종이를 지원하지 않으면 인쇄소에서 PDF로 인쇄하는 방법도 있습니다. 인쇄 창에서 'PDF로 저장'을 고르면 파일로 보관할 수 있습니다."),
    ("말씀 뽑기를 온라인 예배나 가정에서도 할 수 있나요?",
     "가능합니다. 새해 말씀 뽑기 페이지의 링크를 공유하면 각자 화면에서 한 장씩 뽑고, 뽑은 말씀 카드를 이미지로 저장해 단체 대화방에 나눌 수 있습니다."),
]

HOWTO = [
    ("구절 묶음 정하기", "새해, 위로, 믿음 등 모임 성격에 맞는 구절 묶음을 고릅니다."),
    ("카드 디자인 고르기", "사진 배경, 글꼴, 장식을 고르면 모든 카드에 같은 디자인이 적용됩니다."),
    ("용지당 카드 수와 장수 정하기", "A4 한 장에 4~12장을 고르고 참석 인원에 맞춰 구절당 장수를 정합니다."),
    ("인쇄해서 자르기", "자르는 선을 따라 잘라 말씀 상자에 담습니다."),
]

CSS = bv.CSS + """
.gd{max-width:var(--w-read,820px);margin:0 auto;padding:26px 20px 14px;text-align:left;color:#222}
.gd h1{font-size:28px;line-height:1.4;margin:10px 0 6px}.gd h2{font-size:21px;margin:34px 0 10px;color:#0b3d73}.gd h3{font-size:17px;margin:20px 0 6px}
.gd p,.gd li{font-size:16px;line-height:1.95;word-break:keep-all}.gd p{margin:0 0 12px}
.gd .lead{font-size:17px;color:#445}
.gd .box{background:#f4f8ff;border:1px solid #cfe0f5;border-radius:14px;padding:16px 18px;margin:16px 0}
.gd .box b{color:#0b3d73}
.gd table{width:100%;border-collapse:collapse;margin:12px 0;font-size:15px}
.gd th,.gd td{border:1px solid #dfe6ef;padding:9px 10px;text-align:left;line-height:1.7;vertical-align:top}
.gd th{background:#f1f5fb;white-space:nowrap}
.gd .btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.gd .btnrow a{display:inline-block;padding:13px 20px;border-radius:12px;background:#0073e6;color:#fff;text-decoration:none;font-weight:700;font-size:15.5px}
.gd .btnrow a.alt{background:#fff;color:#0b5cad;border:1px solid #bcd3f0}
.gd .warn{background:#fff8ec;border:1px solid #f0d9a8;border-radius:14px;padding:14px 18px;margin:16px 0}
.gd .tl td:first-child{white-space:nowrap;font-weight:700;color:#0b5cad;width:92px}
"""


def table(head_cells, rows, cls=""):
    th = "".join(f"<th>{esc(c)}</th>" for c in head_cells)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><tr>{th}</tr>{tr}</table>'


def render():
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    howto_ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "송구영신예배 말씀 뽑기 카드 준비하는 방법",
                "totalTime": "PT30M", "tool": [{"@type": "HowToTool", "name": "프린터와 A4 용지"}, {"@type": "HowToTool", "name": "가위 또는 재단기"}],
                "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(HOWTO)]}
    article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": "송구영신예배 말씀 뽑기 방법과 준비 가이드",
                  "description": DESC, "inLanguage": "ko", "mainEntityOfPage": SITE + PATH,
                  "datePublished": "2026-10-18", "dateModified": bd.TODAY,
                  "author": {"@type": "Organization", "name": "십자가로세로", "url": SITE},
                  "publisher": {"@type": "Organization", "name": "십자가로세로", "url": SITE}}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "말씀 뽑기", "item": SITE + "/verse/"},
        {"@type": "ListItem", "position": 3, "name": "새해 말씀 뽑기", "item": SITE + "/verse/new-year/"},
        {"@type": "ListItem", "position": 4, "name": "송구영신예배 가이드", "item": SITE + PATH}]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n'
                 for x in (article_ld, howto_ld, faq_ld, crumb_ld))
    h = head(TITLE, DESC, PATH, ld).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)

    need = table(["참석 인원", "준비할 카드(약 1.2배)", "A4 8장씩 인쇄 시"],
                 [["30명", "36장", "5쪽"], ["50명", "60장", "8쪽"], ["100명", "120장", "15쪽"],
                  ["200명", "240장", "30쪽"], ["300명", "360장", "45쪽"]])
    flow = table(["시간", "순서", "진행 포인트"], [
        ["0~5분", "안내와 기도", "뽑기의 의미를 짧게 설명합니다. 운세가 아니라 새해를 시작하며 말씀 앞에 서는 시간이라고 먼저 말해 주세요."],
        ["5~10분", "말씀 뽑기", "상자를 돌리거나 한 줄로 나와 한 장씩 뽑습니다. 뽑은 카드는 모두 함께 펼칠 때까지 열어 보지 않게 합니다."],
        ["10~15분", "조용히 읽고 묵상", "카드를 소리 내지 않고 두세 번 읽고, 이 말씀이 올해 내게 무엇을 말하는지 한 문장으로 적어 봅니다."],
        ["15~25분", "짝·조별 나눔", "옆 사람 또는 조원과 2~3분씩 나눕니다. 말씀 풀이를 서로 가르치기보다 듣고 격려하는 데 초점을 둡니다."],
        ["25~30분", "합심기도와 마무리", "뽑은 말씀을 붙들고 기도한 뒤, 카드를 성경 사이나 지갑·책상에 두고 한 해 동안 꺼내 읽도록 권면합니다."],
    ], "tl")
    short = table(["시간", "순서"], [
        ["0~2분", "한 줄 안내와 기도"], ["2~6분", "말씀 뽑기와 읽기"], ["6~10분", "짝과 한 문장 나누고 마무리 기도"]])

    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    body = f"""<main class="gd">
<div class="crumb"><a href="/">홈</a> › <a href="/verse/">말씀 뽑기</a> › <a href="/verse/new-year/">새해 말씀 뽑기</a> › 송구영신예배 가이드</div>
<span class="badge">교회 행사 가이드</span>
<h1>송구영신예배 말씀 뽑기, 이렇게 준비하세요</h1>
<p class="lead">12월 31일 밤 송구영신예배에서 한 해의 말씀을 뽑아 나누는 순서를 준비하는 교회가 많습니다. 이 글은 처음 진행하는 교회도 따라 할 수 있도록 준비물, 인원별 카드 수, 시간표, 유의할 점을 한 번에 정리한 안내입니다.</p>

<div class="box"><b>한눈에 보기</b>
<ul style="margin:8px 0 0;padding-left:20px">
<li>소요 시간: 짧게는 10분, 충분히 하면 30분</li>
<li>준비물: 말씀 카드, 상자(또는 바구니), 필기구, 가위 또는 재단기</li>
<li>카드 수: 참석 인원 × 1.2장 안팎</li>
<li>비용: 십자가로세로의 카드 만들기·인쇄 기능은 무료</li>
</ul></div>

<div class="btnrow">
<a href="/verse/#church-print" data-ga="nyguide_to_batch">🖨️ 말씀 카드 한꺼번에 인쇄하기</a>
<a class="alt" href="/verse/new-year/" data-ga="nyguide_to_newyear">🎍 새해 말씀 뽑기 해 보기</a>
</div>

<h2>송구영신예배와 말씀 뽑기</h2>
<p>송구영신(送舊迎新)은 '묵은 것을 보내고 새것을 맞이한다'는 뜻입니다. 한국 교회는 12월 31일 밤부터 새해 첫 시간까지 함께 모여 지난 한 해를 감사로 돌아보고 새해를 기도로 시작하는 예배를 드립니다. 이 예배에 한 해 동안 마음에 품을 말씀을 한 장씩 받는 순서를 더하는 교회가 많습니다.</p>
<p>말씀 뽑기는 성경이 정한 의식이 아니라 교회가 만든 신앙 습관입니다. 그래서 어떻게 설명하고 진행하느냐가 중요합니다. 뽑힌 구절이 올해의 운세나 예언이 되는 것이 아니라, 한 해 동안 묵상할 말씀 한 구절을 받는 것이라고 분명히 하면 성도들이 부담 없이 참여할 수 있습니다.</p>

<h2>말씀 뽑기를 진행하는 방법 4가지</h2>
<h3>1. 말씀 상자에서 뽑기 (가장 많이 쓰는 방법)</h3>
<p>접은 카드를 상자나 바구니에 담아 두고 한 사람씩 나와 한 장을 뽑습니다. 인원이 많으면 좌석 줄마다 상자를 돌리는 방식이 시간을 줄여 줍니다. 카드를 반으로 접거나 작게 말아 겉에서 글이 보이지 않게 합니다.</p>
<h3>2. 입장할 때 나눠 주기</h3>
<p>예배당 입구에서 봉사자가 카드를 한 장씩 건네는 방법입니다. 시간을 아끼고 안내할 수 있어 인원이 많은 교회에 맞습니다. 이 경우 같은 구절이 겹치지 않도록 섞어서 준비하세요.</p>
<h3>3. 조별로 돌려 뽑고 서로 읽어 주기</h3>
<p>조별 테이블에 상자를 두고, 한 사람이 뽑은 말씀을 다른 조원이 소리 내어 읽어 주는 방식입니다. 읽어 주는 사람의 목소리로 들으면 같은 구절도 새롭게 다가오고, 서로를 위해 축복하는 시간이 됩니다.</p>
<h3>4. 온라인·가정에서 각자 뽑기</h3>
<p>현장에 오지 못하는 성도를 위해 새해 말씀 뽑기 링크를 공유해 각자 뽑게 하고, 뽑은 카드를 이미지로 저장해 단체 대화방에 올려 나누는 방식입니다. 현장 예배와 병행하기 좋습니다.</p>

<h2>준비물 체크리스트</h2>
<ul>
<li>말씀 카드: 모임 인원의 약 1.2배 (아래 표 참고)</li>
<li>말씀 상자 또는 바구니: 인원이 많으면 구역별로 여러 개</li>
<li>필기구와 작은 메모지: 묵상 한 문장 적기용</li>
<li>가위, 칼, 재단기: 카드 자르기용. 점선 위로 자르면 크기가 맞습니다.</li>
<li>안내 문구: 뽑기의 의미를 설명하는 한두 문장 (아래 목회자 유의점 참고)</li>
<li>봉사자 2~3명: 상자 돌리기, 카드 나눠 주기, 어린이 돕기</li>
</ul>

<h3>인원별 카드 수 계산</h3>
{need}
<p>구절이 100가지 미만이면 같은 구절을 2~3장씩 섞어서 준비하면 됩니다. 같은 구절을 받은 사람끼리 나누는 시간을 가지면 오히려 교제의 계기가 되기도 합니다.</p>

<h3>용지와 인쇄 팁</h3>
<ul>
<li>두꺼운 종이(120~200g)를 쓰면 접거나 상자에서 뽑을 때 편합니다.</li>
<li>일반 복사지에 인쇄해도 되고, 인쇄 창에서 'PDF로 저장'을 골라 인쇄소에 맡길 수도 있습니다.</li>
<li>컬러 프린터가 없으면 사진 배경 대신 연한 색 배경으로 만들면 흑백 인쇄 때 글자가 선명합니다.</li>
<li>행사 전날이 아니라 최소 1주일 전에 시험 인쇄를 해 글자 크기와 잉크 상태를 확인하세요.</li>
</ul>

<h2>시간표 예시</h2>
<h3>30분 진행안</h3>
{flow}
<h3>10분 짧은 진행안</h3>
{short}

<h2>목회자·교사가 유의할 점</h2>
<div class="warn"><b>뽑기 결과를 예언처럼 해석하지 않도록 안내하세요.</b>
<p style="margin-top:6px">"이 말씀은 올해 일어날 일을 알려 주는 것이 아니라, 한 해 동안 묵상하며 하나님께 구할 말씀입니다"라고 시작 전에 한 번 말해 주면 오해가 줄어듭니다.</p></div>
<ul>
<li><b>구절을 미리 골라 두세요.</b> 위로·인도·소망·감사처럼 격려가 되는 구절 위주로 준비하면 부담스러운 구절이 걸리는 일을 피할 수 있습니다. 십자가로세로의 새해 말씀 묶음은 이 기준으로 골랐습니다.</li>
<li><b>성경을 아무 곳이나 펼쳐 나온 구절로 정하는 방식은 권하지 않습니다.</b> 문맥과 상관없는 구절이 걸려 오해가 생길 수 있어, 미리 고른 구절 카드를 쓰는 편이 안전합니다.</li>
<li><b>다시 뽑지 않는 규칙을 정하세요.</b> 시작 전에 "한 번만 뽑고, 마음에 안 들어도 올해는 이 말씀을 붙들어 봅니다"라고 안내하면 좋습니다.</li>
<li><b>새신자와 어린이를 배려하세요.</b> 성경 구절이 낯선 분은 옆에서 한 번 읽어 주고, 어려운 낱말은 간단히 풀어 주세요.</li>
<li><b>뽑은 뒤의 묵상이 핵심입니다.</b> 뽑기만 하고 끝나지 않도록 한 문장 묵상과 짝 나눔, 합심기도를 꼭 포함하세요.</li>
</ul>

<h2>대상별로 이렇게 바꿔 보세요</h2>
<ul>
<li><b>주일학교:</b> 짧고 쉬운 구절만 모아 큰 글씨로 인쇄하고, 뽑은 뒤 교사와 소리 내어 읽고 한 문장을 따라 말하게 합니다.</li>
<li><b>청년부:</b> 구절 하나를 뽑고 '올해 이 말씀을 붙들고 싶은 이유'를 두세 문장으로 적어 조별로 나눕니다.</li>
<li><b>가정:</b> 가족이 함께 한 장씩 뽑고, 서로를 위해 뽑힌 말씀으로 축복기도를 해 줍니다.</li>
<li><b>소그룹·구역:</b> 새해 첫 모임에서 뽑고, 한 달에 한 번 그 말씀을 어떻게 붙들고 있는지 돌아봅니다.</li>
</ul>

<h2>십자가로세로로 카드 만들기</h2>
<ol>
{''.join(f'<li><b>{esc(n)}</b> — {esc(t)}</li>' for n, t in HOWTO)}
</ol>
<p>사진 배경 200여 장, 글꼴 42종, 십자가·비둘기·올리브 가지 같은 장식과 테두리를 고를 수 있고, 새해·성탄·추수감사 구절과 12가지 주제 구절 묶음을 제공합니다. 인쇄 창에서 'PDF로 저장'을 고르면 파일로 보관하거나 인쇄소에 전달할 수 있습니다.</p>
<div class="btnrow">
<a href="/verse/#church-print" data-ga="nyguide_to_batch2">🖨️ 지금 카드 만들기</a>
<a class="alt" href="/verse/" data-ga="nyguide_to_verse">📖 말씀 카드 스튜디오</a>
</div>
<p>묵상 안내문을 함께 나눠 주고 싶다면 해설이 있는 말씀 페이지도 활용해 보세요. <a href="/verse/jeremiah-29-11.html">예레미야 29:11</a>, <a href="/verse/joshua-1-9.html">여호수아 1:9</a>, <a href="/verse/isaiah-41-10.html">이사야 41:10</a> 같은 새해에 자주 뽑히는 구절의 해설을 읽어 볼 수 있습니다.</p>

<h2>자주 묻는 질문</h2>
<div class="faq">{faq_html}</div>

<p class="vnote" style="margin-top:24px;font-size:13px;color:#667">성경 본문은 성경전서 개역한글판(대한성서공회)을 사용했습니다. 교회·주일학교·가정에서의 비영리 사용은 자유롭게 하실 수 있고, 판매용으로는 이용하실 수 없습니다. 구절은 한 해를 시작하며 격려가 되는 말씀으로 직접 골랐으며, 교단과 교회의 신학적 입장에 따라 다르게 운영하실 수 있습니다.</p>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- NYGUIDE-START -->.*?<!-- NYGUIDE-END -->", "", s, flags=re.S)
    block = (f"\n  <!-- NYGUIDE-START -->\n  <url>\n    <loc>{SITE}{PATH}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n"
             "    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n  <!-- NYGUIDE-END -->\n")
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    d = os.path.join(ROOT, "verse", "new-year", "guide")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render())
    update_sitemap()
    print("송구영신 가이드 생성")


if __name__ == "__main__":
    main()
