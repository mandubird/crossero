# -*- coding: utf-8 -*-
"""'말씀카드 만들기' 안내 페이지(/cards/make/) 생성. 실행: python3 build_cardmake.py"""
import json
import os
import re

import build_dictionary as bd
import build_verse as bv
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT
from shop_links import shop_block

PATH = "/cards/make/"
TITLE = "말씀카드 만들기 - 무료 온라인 제작과 손으로 만드는 방법(도안·크기·인쇄) | 십자가로세로"
DESC = "말씀카드 만들기를 처음 하는 분을 위한 안내입니다. 온라인에서 무료로 만들어 카톡·인스타그램에 공유하거나 A4로 인쇄하는 법, 종이로 직접 만드는 DIY 준비물과 크기, 교회 행사용 여러 장 인쇄까지 정리했습니다."

SAMPLES = [("new-year-isaiah-43-19", "새해 말씀카드 예시 - 이사야 43:19", "/cards/new-year/", "새해"),
           ("christmas-luke-2-11", "성탄 말씀카드 예시 - 누가복음 2:11", "/cards/christmas/", "성탄"),
           ("comfort-psalms-23-1", "위로의 말씀카드 예시 - 시편 23:1", "/cards/comfort/", "위로"),
           ("peace-philippians-4-6", "평안의 말씀카드 예시 - 빌립보서 4:6", "/cards/peace/", "평안"),
           ("courage-joshua-1-9", "용기의 말씀카드 예시 - 여호수아 1:9", "/cards/courage/", "용기"),
           ("thanksgiving-psalms-100-4", "감사의 말씀카드 예시 - 시편 100:4", "/cards/thanksgiving/", "추수감사")]

HOWTO = [
    ("말씀 고르기", "마음에 닿는 구절을 직접 고르거나, 말씀 뽑기로 한 구절을 뽑습니다."),
    ("배경과 글꼴 고르기", "사진이나 일러스트 배경, 글꼴, 장식을 고릅니다. 글자가 잘 읽히도록 배경이 너무 복잡하지 않은 것을 고르세요."),
    ("크기 고르기", "카카오톡·인스타그램, 휴대폰 배경화면, 엽서·주보 삽입, 책갈피 중 쓸 곳에 맞는 크기를 고릅니다."),
    ("저장하거나 인쇄하기", "이미지로 저장하거나 공유하고, 인쇄할 때는 A4 한 장에 여러 장씩 모아 인쇄해 잘라 씁니다."),
]

FAQ = [
    ("말씀카드는 무료로 만들 수 있나요?", "네. 십자가로세로의 말씀카드 만들기는 무료입니다. 카카오톡·인스타그램용 이미지 저장, 휴대폰·PC 배경화면, 인쇄까지 모두 무료이고, 후원하시면 이미지의 작은 워터마크를 뺄 수 있습니다."),
    ("말씀카드는 어떤 크기로 만들면 좋나요?", "카카오톡과 인스타그램 피드는 정사각(1080×1080)이나 4:5 세로(1080×1350), 스토리와 휴대폰 배경화면은 9:16(1080×1920), 종이로 뽑을 때는 엽서 크기(A6)나 책갈피가 흔히 쓰입니다. 손으로 만들 때는 명함 크기(약 9×5cm)부터 엽서 크기(10×15cm)까지 많이 씁니다."),
    ("교회에서 말씀카드를 여러 장 인쇄하려면 어떻게 하나요?", "교회·모임용 인쇄에서 구절 묶음과 A4 한 장당 카드 수(4~12장)를 고르면 같은 디자인으로 여러 구절을 한꺼번에 인쇄할 수 있습니다. 120~200g 두꺼운 종이에 인쇄하고 점선을 따라 자르면 됩니다."),
    ("말씀카드에 교회 이름을 넣을 수 있나요?", "더보기 탭의 '교회 이름 넣기'에 이름을 입력하면 누구나 카드 위에서 미리 볼 수 있습니다. 저장·인쇄한 카드에 이름이 들어가는 것은 후원 기능입니다."),
    ("성경 본문과 사진 저작권은 괜찮나요?", "성경 본문은 저작권이 만료된 개역한글판을 사용합니다. 배경 사진은 자유 이용이 허용된 사진(CC BY, CC BY-SA, CC0, 퍼블릭 도메인)만 쓰며 촬영자와 라이선스가 카드 아래에 표시됩니다. 교회·가정에서의 비영리 사용은 자유롭고, 판매는 하지 말아 주세요."),
    ("새해 말씀카드는 따로 있나요?", "새해 말씀 뽑기와 새해 말씀카드 모음이 따로 있습니다. 송구영신예배에서 쓰는 방법은 송구영신 진행 가이드에 정리되어 있습니다."),
    ("개역개정이나 새번역으로 만들 수 있나요?", "후원 기능인 '내가 쓴 말씀 직접 입력'에서 원하는 번역본의 본문을 붙여넣어 카드로 만들 수 있습니다. 번역본의 저작권과 사용 허락은 사용하시는 분이 확인해 주세요."),
]

CSS = bv.CSS + """
.gd{max-width:var(--w-read,820px);margin:0 auto;padding:26px 20px 14px;text-align:left;color:#222}
.gd h1{font-size:28px;line-height:1.4;margin:10px 0 6px}.gd h2{font-size:21px;margin:34px 0 10px;color:#0b3d73}.gd h3{font-size:17px;margin:20px 0 6px}
.gd p,.gd li{font-size:16px;line-height:1.95;word-break:keep-all}.gd p{margin:0 0 12px}
.gd .lead{font-size:17px;color:#445}
.gd .box{background:#f4f8ff;border:1px solid #cfe0f5;border-radius:14px;padding:16px 18px;margin:16px 0}
.gd table{width:100%;border-collapse:collapse;margin:12px 0;font-size:15px}
.gd th,.gd td{border:1px solid #dfe6ef;padding:9px 10px;text-align:left;line-height:1.7;vertical-align:top}.gd th{background:#f1f5fb}
.gd .btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.gd .btnrow a{display:inline-block;padding:13px 20px;border-radius:12px;background:#0073e6;color:#fff;text-decoration:none;font-weight:700;font-size:15.5px}
.gd .btnrow a.alt{background:#fff;color:#0b5cad;border:1px solid #bcd3f0}
.gd .smp{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:14px 0}
.gd .smp a{display:block;border:1px solid #d6e4f7;border-radius:12px;overflow:hidden;text-decoration:none;color:#0b3d73;background:#fff}
.gd .smp img{display:block;width:100%;height:auto}.gd .smp span{display:block;padding:6px 10px 8px;font-size:13.5px;font-weight:700;text-align:center}
"""


def table(head_cells, rows):
    th = "".join(f"<th>{esc(c)}</th>" for c in head_cells)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{th}</tr>{tr}</table>"


def render():
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    howto_ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "말씀카드 만들기", "totalTime": "PT5M",
                "tool": [{"@type": "HowToTool", "name": "스마트폰 또는 컴퓨터"}],
                "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(HOWTO)]}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "말씀카드 이미지 갤러리", "item": SITE + "/cards/"},
        {"@type": "ListItem", "position": 3, "name": "말씀카드 만들기", "item": SITE + PATH}]}
    article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": "말씀카드 만들기 - 온라인 무료 제작과 손으로 만드는 방법", "description": DESC, "inLanguage": "ko",
                  "mainEntityOfPage": SITE + PATH, "datePublished": "2026-11-07", "dateModified": bd.TODAY,
                  "author": {"@type": "Organization", "name": "십자가로세로", "url": SITE}, "publisher": {"@type": "Organization", "name": "십자가로세로", "url": SITE}}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (article_ld, howto_ld, faq_ld, crumb_ld))
    h = head(TITLE, DESC, PATH, ld).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    smp = "".join(f'<a href="{u}" data-ga="make_sample_click" data-ga-label="{k}"><img src="/images/cards/{f}_t.jpg" width="360" height="450" loading="lazy" alt="{esc(a)}"><span>{esc(k)}</span></a>' for f, a, u, k in SAMPLES)
    sizes = table(["쓰는 곳", "크기(픽셀 또는 용지)", "참고"], [
        ["카카오톡·인스타그램 피드", "1080×1080(정사각), 1080×1350(4:5)", "사진과 함께 올리기 좋은 기본 크기"],
        ["스토리·휴대폰 배경화면", "1080×1920(9:16), 1170×2532(긴 화면)", "글자가 위아래 여백 안에 들어오도록 만듭니다"],
        ["프로필", "800×800(정사각)", "한 줄 말씀이 어울립니다"],
        ["PC 배경화면", "1920×1080, 2560×1440", "가로형"],
        ["링크 미리보기·유튜브 썸네일", "1280×720(가로)", "공유 링크에 보이는 이미지"],
        ["엽서·주보 삽입", "A6 세로", "주보에 끼우거나 선물용"],
        ["책갈피", "600×1800(세로 긴 형태)", "성경책 사이에 끼워 둡니다"],
        ["교회·모임용 여러 장", "A4 한 장에 4~12장", "점선을 따라 잘라 말씀 상자에 담습니다"],
    ])
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    body = f"""<main class="gd">
<div class="crumb"><a href="/">홈</a> › <a href="/cards/">말씀카드 이미지 갤러리</a> › 말씀카드 만들기</div>
<span class="badge">무료 · 설치 없음</span>
<h1>말씀카드 만들기, 이렇게 하세요</h1>
<p class="lead">말씀카드는 성경 구절을 사진이나 그림 위에 적은 카드입니다. 선물하거나 암송에 쓰고, 카카오톡·인스타그램으로 나누고, 송구영신예배나 소그룹에서 한 장씩 뽑아 쓰기도 합니다. 이 글은 온라인에서 무료로 만드는 방법, 종이로 직접 만드는 방법, 교회에서 여러 장 인쇄하는 방법을 한 번에 정리한 안내입니다.</p>
<div class="box"><b>어떤 방법이 맞을까요?</b>
<table><tr><th>방법</th><th>걸리는 시간</th><th>이런 때</th></tr>
<tr><td>온라인 무료 제작</td><td>약 5분</td><td>카톡·인스타 공유, 배경화면, 인쇄용 A4·엽서</td></tr>
<tr><td>손으로 만들기(DIY)</td><td>카드 한 장에 20~30분</td><td>주일학교 활동, 손편지처럼 정성을 담고 싶을 때</td></tr>
<tr><td>교회·모임용 인쇄</td><td>설정 10분 + 인쇄</td><td>송구영신, 성탄, 추수감사 등 행사에서 여러 장 필요할 때</td></tr></table></div>
<div class="btnrow"><a href="/verse/" data-ga="make_to_studio">🎨 말씀카드 지금 만들기</a><a class="alt" href="/cards/" data-ga="make_to_gallery">🖼️ 말씀카드 이미지 보기</a></div>

<h2>1. 온라인에서 무료로 말씀카드 만들기</h2>
<ol>{''.join(f'<li><b>{esc(n)}</b> — {esc(t)}</li>' for n, t in HOWTO)}</ol>
<p>사진 배경 270장, 질감·일러스트 배경, 글꼴 42종, 십자가·비둘기·올리브 가지 같은 장식과 테두리를 고를 수 있습니다. 배경 사진은 자유 이용이 허용된 사진만 쓰고, 촬영자와 라이선스가 카드 아래에 표시됩니다.</p>
<div class="smp">{smp}</div>
<h3>쓰는 곳에 따른 크기</h3>
{sizes}

<h2>2. 종이로 말씀카드 직접 만들기(DIY)</h2>
<p>손으로 만들면 카드마다 정성이 담깁니다. 주일학교 활동이나 선물용으로 많이 합니다.</p>
<ol>
<li><b>구절 고르기</b> — 짧은 구절이 카드에 잘 들어갑니다. 한두 문장이 가장 읽기 좋습니다.</li>
<li><b>종이 자르기</b> — 120~200g 두꺼운 종이를 명함 크기(약 9×5cm), 엽서 크기(10×15cm), 책갈피(약 5×15cm) 중 하나로 자릅니다.</li>
<li><b>말씀 적기</b> — 연필로 가볍게 줄을 긋고 사인펜이나 색연필로 구절과 출처(책 장:절)를 씁니다.</li>
<li><b>꾸미기</b> — 테두리, 꽃, 십자가 같은 단순한 그림을 더합니다. 글자보다 그림이 두드러지지 않게 합니다.</li>
<li><b>보관하기</b> — 코팅지나 투명 테이프를 붙이면 오래 씁니다.</li>
</ol>
<p>직접 그리기 부담스러우면 온라인으로 만든 카드를 인쇄해 가장자리만 손으로 꾸며도 좋습니다.</p>
{shop_block(["paper200", "scissors", "colorpencil", "laminate", "string"], "말씀카드 DIY 준비물")}

<h2>3. 교회·모임에서 여러 장 인쇄하기</h2>
<ul>
<li>구절 묶음(새해·성탄·추수감사·위로·평안 등)과 A4 한 장당 카드 수를 고르면 같은 디자인으로 한꺼번에 인쇄할 수 있습니다.</li>
<li>참석 인원의 1.2배 정도를 준비하고, 120~200g 두꺼운 종이에 인쇄하면 상자에서 뽑기 편합니다.</li>
<li>인원별 장수와 시간표는 <a href="/verse/new-year/guide/">송구영신 말씀 뽑기 진행 가이드</a>의 준비 계산기로 계산해 보세요.</li>
<li>카드 아래에 교회 이름을 넣는 기능은 후원 기능이며, 미리보기는 누구나 해 볼 수 있습니다.</li>
</ul>
<div class="btnrow"><a href="/verse/#church-print" data-ga="make_to_print">🖨️ 교회·모임용 인쇄하기</a><a class="alt" href="/verse/new-year/" data-ga="make_to_newyear">🎍 새해 말씀뽑기</a></div>

<h2>말씀카드에 어떤 구절이 좋을까요?</h2>
<ul>
<li><b>짧은 구절:</b> 카드에 크게 쓸 수 있고 암송하기도 쉽습니다.</li>
<li><b>받는 사람 상황에 맞는 구절:</b> 위로는 시편 23편·이사야 41:10, 새해는 이사야 43:19·예레미야 29:11, 감사는 시편 100편이 많이 쓰입니다.</li>
<li><b>문맥을 함께 읽기:</b> 한 구절만 떼어 쓸 때도 앞뒤 본문을 한 번 읽어 보세요. 뽑은 말씀을 운세처럼 받아들이지 않고 묵상의 시작으로 삼도록 <a href="/guide/bible-verse-drawing-guide/">말씀 뽑기, 해도 될까요?</a> 글을 참고하세요.</li>
</ul>

<h2>자주 묻는 질문</h2>
<div class="faq">{faq_html}</div>
<p><a href="/verse/">말씀카드 만들기·말씀뽑기</a> · <a href="/cards/">말씀카드 이미지 갤러리</a> · <a href="/cards/new-year/">새해 말씀카드</a> · <a href="/christmas/">성탄 성극 대본</a> · <a href="/quiet/">1분 쉼 묵상</a></p>
<p class="vnote" style="font-size:13px;color:#667">성경 본문은 성경전서 개역한글판(대한성서공회)을 사용했습니다. 교회·주일학교·가정에서의 비영리 사용은 자유롭게 하실 수 있고, 판매용으로는 이용하실 수 없습니다.</p>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- CARDMAKE-START -->.*?<!-- CARDMAKE-END -->", "", s, flags=re.S)
    block = (f"\n  <!-- CARDMAKE-START -->\n  <url>\n    <loc>{SITE}{PATH}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n"
             "    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n  <!-- CARDMAKE-END -->\n")
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    d = os.path.join(ROOT, "cards", "make")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render())
    update_sitemap()
    print("말씀카드 만들기 페이지 생성")


if __name__ == "__main__":
    main()
