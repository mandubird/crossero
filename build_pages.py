# -*- coding: utf-8 -*-
"""교회·주일학교 활용 페이지, 콘텐츠 제작 원칙 페이지 생성. 실행: python3 build_pages.py"""
import json
import os

import build_dictionary as bd
from build_dictionary import esc, head, FOOTER, NAV, TITLES, SITE, ROOT

PLAIN_NAV = NAV.replace(' nav-active', '')
MAIL_TRIAL = ("mailto:mandubird@naver.com?subject=" +
              "%5B%EC%8B%AD%EC%9E%90%EA%B0%80%EB%A1%9C%EC%84%B8%EB%A1%9C%5D%20%EA%B5%90%ED%9A%8C%20%EC%8B%9C%EB%B2%94%20%EC%9D%B4%EC%9A%A9%20%EC%8B%A0%EC%B2%AD&body=" +
              "%EA%B5%90%ED%9A%8C%2F%EB%AA%A8%EC%9E%84%20%EC%9D%B4%EB%A6%84%3A%0A%EB%8B%B4%EB%8B%B9%EC%9E%90%20%EC%9D%B4%EB%A6%84%3A%0A%EB%8C%80%EC%83%81(%EC%A3%BC%EC%9D%BC%ED%95%99%EA%B5%90%2F%EC%B2%AD%EB%85%84%EB%B6%80%2F%EA%B5%AC%EC%97%AD%20%EB%93%B1)%3A%0A%EB%8C%80%EB%9E%B5%EC%A0%81%EC%9D%B8%20%EC%9D%B8%EC%9B%90%3A%0A%EC%93%B0%EA%B3%A0%20%EC%8B%B6%EC%9D%80%20%EB%B0%A9%EC%8B%9D(%EC%A3%BC%EB%B3%B4%2F%EC%88%98%EC%97%85%20%EB%B3%B4%EC%A1%B0%20%EB%93%B1)%3A")


def page(path, title, desc, body, ld=""):
    out = [head(title, desc, path, ld).replace(NAV, PLAIN_NAV).replace('og:type" content="article"', 'og:type" content="website"')]
    out.append('<main class="wrap">')
    out.append(body)
    out.append('</main>')
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def li(items):
    return "<ul class=\"refs\">" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def church():
    faqs = [
        ("퍼즐을 교회에서 인쇄해 나눠 줘도 되나요?", "비영리 교회·주일학교·소그룹 모임의 교육 목적이라면 인쇄해서 나눠 쓰셔도 됩니다. 판매나 외부 재배포, 다른 사이트 게시는 허용되지 않으며, 주보에 넣으실 때는 출처(십자가로세로, crossero.com)를 함께 적어 주세요."),
        ("인쇄 기능은 어떻게 쓰나요?", "퍼즐 화면의 인쇄 버튼은 후원 이용권을 인증한 뒤 사용할 수 있습니다. 교회 시범 이용을 신청하시면 확인 후 이용권을 안내해 드립니다."),
        ("우리 교회 설교 본문으로 퍼즐을 만들어 주나요?", "현재는 성경 66권 순서의 퍼즐과 주제별 퍼즐이 준비되어 있습니다. 원하시는 본문이 있으면 시범 신청 메일에 적어 주세요. 가능한 범위에서 제작을 검토하되, 모든 요청을 약속드리지는 못합니다."),
        ("정답은 어떻게 확인하나요?", "퍼즐 화면의 정답 보기 기능으로 확인하거나, 인쇄 시 QR 코드로 정답 화면을 열 수 있습니다."),
    ]
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        ensure_ascii=False) + "</script>"
    picks = [("초등부", ["gen_002", "exo_012", "bib_107"]), ("중고등부", ["dan_058", "act_086", "cpl_001"]), ("청년·장년·구역", ["psa_045", "cor_088", "rom_087"])]
    cards = ""
    for label, ids in picks:
        cards += f"<h2>{label} 추천</h2><div class=\"cards\">" + "".join(
            f'<a class="card" href="/play.html?id={i}" data-ga="church_pick_puzzle" data-ga-label="{i}"><b>{esc(TITLES.get(i, i))}</b><span>퍼즐 풀어보기 →</span></a>' for i in ids) + "</div>"
    body = f"""
<div class="crumb"><a href="/">홈</a> › 교회·주일학교 활용</div>
<span class="badge">교회·교사용</span>
<h1>교회 주보·주일학교에서 성경 퍼즐 활용하기</h1>
<div class="sub">설교 본문 복습, 공과 마무리, 소그룹 아이스브레이킹까지</div>
<div class="summary">십자가로세로의 가로세로 퍼즐은 성경 66권 순서와 인물·사건·상식 주제로 나뉘어 있어, 이번 주 공과나 설교 본문에 맞는 퍼즐을 골라 바로 쓸 수 있습니다. 한 퍼즐은 보통 10~25분 안에 풀 수 있도록 단어 수를 조정해 두었습니다.</div>

<h2>이렇게 활용해 보세요</h2>
{li([
    "<b>공과 마무리 5~10분</b> — 수업 말미에 오늘 배운 책이나 인물 퍼즐을 짝과 함께 풀며 복습합니다.",
    "<b>주보 한 켠</b> — 한 주 동안 가정에서 풀어 볼 수 있도록 설교 본문과 같은 책의 퍼즐을 소개합니다.",
    "<b>구역·소그룹</b> — 모임을 열기 전 가볍게 시작하는 활동으로, 팀을 나눠 정답 수 대결을 해도 좋습니다.",
    "<b>결석 학생 보충</b> — 링크만 보내 주면 집에서 같은 내용으로 복습할 수 있습니다.",
])}
{cards}

<h2>준비는 이렇게 간단합니다</h2>
{li([
    "<b>1단계</b> — <a href=\"/list.html\">퍼즐 목록</a>에서 이번 주 본문과 맞는 책이나 주제를 고릅니다. 모르는 용어는 <a href=\"/dictionary/\">성경사전</a>에서 먼저 확인해 보세요.",
    "<b>2단계</b> — 화면으로 함께 풀거나, 인쇄용으로 내려받아 나눠 줍니다(인쇄는 이용권 인증 후 사용).",
    "<b>3단계</b> — 정답은 정답 보기 또는 인쇄물의 QR 코드로 확인합니다.",
])}

<h2>교회 시범 이용 신청</h2>
<p>초기에는 일부 교회와 교사 모임에 시범 이용권을 안내해 드리려고 합니다. 실제로 써 보시고 불편한 점이나 바라는 기능을 알려 주시면 이후 서비스에 반영하겠습니다. 아래 버튼을 누르면 메일 양식이 열립니다.</p>
<a class="cta" href="{MAIL_TRIAL}" data-ga="church_trial_click" data-ga-label="church_page">✉️ 교회 시범 이용 신청하기<small>교회명·대상·인원만 적어 보내 주시면 됩니다</small></a>

<h2>자주 묻는 질문</h2>
<div class="faq">{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)}</div>
"""
    return page("/church-bulletin-puzzle.html", "교회 주보·주일학교 성경 퍼즐 활용 가이드 | 십자가로세로",
                "교회 주보, 주일학교 공과, 구역 모임에서 성경 가로세로 퍼즐을 활용하는 방법과 연령별 추천 퍼즐, 교회 시범 이용 신청 안내.", body, ld)


def policy():
    body = """
<div class="crumb"><a href="/">홈</a> › 콘텐츠 제작 원칙</div>
<span class="badge">운영 안내</span>
<h1>콘텐츠 제작 원칙</h1>
<div class="sub">십자가로세로가 퍼즐과 사전 콘텐츠를 만드는 방식</div>
<div class="summary">십자가로세로는 성경을 쉽고 즐겁게 복습할 수 있도록 돕는 개인 운영 사역입니다. 아래는 콘텐츠를 만들 때 지키는 원칙입니다.</div>

<h2>운영자</h2>
<p>십자가로세로는 개인이 기획·제작·운영합니다. 문의는 mandubird@naver.com 으로 받고 있으며, 오류 제보와 제안은 언제든 환영합니다.</p>

<h2>성경 본문과 저작권</h2>
<p>퍼즐과 사전의 문장은 직접 작성합니다. 성경 구절은 장·절 위치만 안내하고, 특정 번역본의 본문을 대량으로 옮기지 않습니다. 이는 각 번역본의 저작권을 존중하기 위한 선택입니다. 사실 자체(인물, 연대, 장소)는 공개된 사실에 근거해 작성하며, 다른 사이트의 문장을 그대로 가져오지 않습니다.</p>

<h2>정확성과 해석</h2>
<p>성경 사전 항목은 구절 위치를 기준으로 작성하고, 학자나 교단에 따라 해석이 갈리는 부분(예: 홍해의 정확한 위치, 시내산의 위치)은 '견해가 나뉜다'고 밝힙니다. 특정 교단의 입장을 일방적으로 가르치기보다 본문이 말하는 바를 쉽게 풀어 쓰는 것을 목표로 합니다.</p>

<h2>자동 발행 게시물에 대해</h2>
<p>게시판의 퍼즐 게시물은 퍼즐 데이터와 성경 각 권의 소개 정보를 바탕으로 매일 발행됩니다. 각 게시물에는 책 소개, 주요 사건, 배우는 내용을 함께 실어 퍼즐 풀이가 복습이 되도록 구성합니다. 앞으로는 사전 항목으로의 연결을 늘려 더 깊이 읽을 수 있게 개선할 계획입니다.</p>

<h2>오류 제보와 수정</h2>
<p>사실 오류나 어색한 표현을 발견하시면 mandubird@naver.com 으로 알려 주세요. 확인 후 수정하고, 수정 이력은 페이지의 최종 수정일에 반영합니다.</p>

<h2>광고와 후원</h2>
<p>사이트 운영비를 위해 광고와 후원 이용권을 운영합니다. 광고와 후원은 콘텐츠의 내용에 영향을 주지 않습니다.</p>
"""
    return page("/editorial-policy.html", "콘텐츠 제작 원칙 | 십자가로세로",
                "십자가로세로가 성경 퍼즐과 사전 콘텐츠를 만드는 원칙: 직접 작성, 성경 본문 저작권 존중, 해석이 갈리는 부분의 표기, 오류 제보 방법.", body)


def cards_for(ids, ga):
    return '<div class="cards">' + "".join(
        f'<a class="card" href="/play.html?id={i}" data-ga="{ga}" data-ga-label="{i}"><b>{esc(TITLES.get(i, i))}</b><span>퍼즐 풀어보기 →</span></a>' for i in ids) + "</div>"


def faq_ld(faqs, extra=None):
    items = [{"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    if extra:
        items.append(extra)
    return "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in items)


def bible_crossword():
    faqs = [
        ("성경 십자말풀이는 무료인가요?", "퍼즐 풀이는 회원가입 없이 무료로 할 수 있습니다. 인쇄와 정답 보기 일부 기능은 후원 이용권 인증 후 사용할 수 있습니다."),
        ("성경 가로세로 낱말퀴즈는 어떤 연령에 맞나요?", "초등 고학년부터 어른까지 풀 수 있습니다. 어린이는 인물·사건 퍼즐, 성인은 책별·주제별 퍼즐을 권합니다."),
        ("스마트폰에서도 풀 수 있나요?", "네. 칸을 터치하면 한글 자판이 열리고, 가로·세로 힌트는 화면 아래 목록에서 확인할 수 있습니다."),
        ("퍼즐은 어떻게 구성되어 있나요?", "성경 66권 순서의 퍼즐, 인물·사건·상식 주제 퍼즐, 기독교 인물 퍼즐로 나뉘며 총 200여 개가 있습니다. 모르는 단어는 성경사전에서 먼저 찾아볼 수 있습니다."),
    ]
    body = f"""
<div class="crumb"><a href="/">홈</a> › 성경 십자말풀이</div>
<span class="badge">성경 퍼즐</span>
<h1>성경 십자말풀이 · 가로세로 낱말퀴즈</h1>
<div class="sub">성경 인물·사건·구절로 풀어 보는 한글 낱말 퍼즐</div>
<div class="summary">성경 십자말풀이는 가로·세로 힌트를 보고 성경 속 낱말을 칸에 채워 넣는 낱말 퍼즐입니다. 십자가로세로에는 성경 66권 순서의 퍼즐과 인물·사건·지명 주제 퍼즐이 있어, 설교 본문 복습이나 주일학교 활동에 바로 쓸 수 있습니다. 회원가입 없이 바로 시작할 수 있습니다.</div>

<h2>처음이라면 이 퍼즐부터</h2>
{cards_for(["gen_001", "gen_002", "bib_125", "bib_107"], "landing_pick_puzzle")}

<h2>성경 인물로 풀기</h2>
<p>아브라함, 모세, 다윗처럼 이름은 익숙해도 이야기를 정확히 떠올리기는 어렵습니다. 퍼즐을 풀기 전 <a href="/dictionary/">성경사전</a>에서 인물 이야기를 먼저 읽으면 힌트가 훨씬 쉬워집니다.</p>
{cards_for(["cha_111", "cha_113", "cha_115", "cha_116", "cha_117"], "landing_pick_puzzle")}

<h2>성경 각 권으로 풀기</h2>
<p>창세기부터 요한계시록까지 한 권씩 따라가며 풀 수 있습니다. 한 퍼즐에 그 책의 핵심 인물, 장소, 사건이 담겨 있어 통독 후 복습용으로 좋습니다.</p>
{cards_for(["gen_003", "exo_012", "psa_045", "mat_072", "act_086", "rom_087"], "landing_pick_puzzle")}

<h2>이렇게 풀어 보세요</h2>
{li([
    "<b>1.</b> 칸을 누르면 해당 칸의 힌트가 표시됩니다.",
    "<b>2.</b> 한글을 한 글자씩 입력합니다. 방향키로 이동하고 Backspace로 지울 수 있습니다.",
    "<b>3.</b> 막히면 가로·세로 힌트 목록에서 다른 단어부터 풀어 겹치는 글자를 단서로 삼습니다.",
    "<b>4.</b> 다 풀었다면 같은 책의 다른 퍼즐이나 관련 <a href=\"/dictionary/\">성경사전</a> 항목으로 이어서 복습해 보세요.",
])}
<p class="note">교회·주일학교에서 쓰시려면 <a href="/church-bulletin-puzzle.html">교회 활용 가이드</a>를 참고해 주세요. 낱말퍼즐 푸는 방법이 낯설다면 <a href="/how-to-crossword.html">십자말풀이 하는 법</a>을 먼저 읽어 보세요.</p>

<div class="faq"><h2>자주 묻는 질문</h2>{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)}</div>
<a class="cta" href="/list.html" data-ga="landing_to_list" data-ga-label="bible_crossword">🧩 전체 퍼즐 목록 보기<small>200여 개의 성경 퍼즐</small></a>
"""
    return page("/bible-crossword.html", "성경 십자말풀이·가로세로 낱말퀴즈 무료로 풀기 | 십자가로세로",
                "성경 인물·사건·구절로 풀어 보는 한글 가로세로 낱말퀴즈. 성경 66권별, 인물별 퍼즐 200여 개를 회원가입 없이 무료로 풀어 보세요.", body, faq_ld(faqs))


def howto():
    faqs = [
        ("십자말풀이와 가로세로 낱말퀴즈는 같은 건가요?", "같은 종류의 퍼즐을 가리키는 말입니다. 십자말풀이, 십자낱말, 가로세로 낱말퀴즈, 크로스워드 퍼즐이 모두 비슷하게 쓰입니다."),
        ("십자말풀이는 언제 시작되었나요?", "1913년 12월 21일 미국 뉴욕의 신문 '뉴욕 월드'에 실린 아서 윈의 퍼즐이 최초의 크로스워드로 널리 알려져 있습니다."),
        ("막힐 때는 어떻게 하나요?", "답을 아는 짧은 단어부터 채우고, 교차하는 글자를 단서로 나머지를 추리합니다. 한 번에 다 풀려 하지 말고 확실한 칸부터 채우는 것이 요령입니다."),
        ("한글 십자말풀이는 영어와 어떻게 다른가요?", "영어는 한 칸에 알파벳 한 글자를 넣고, 한글은 한 칸에 음절 한 글자(예: 가, 나)를 넣습니다. 그래서 두세 글자 단어도 칸 수가 적어 교차점을 찾기가 더 까다로울 수 있습니다."),
    ]
    howto_ld = {"@context": "https://schema.org", "@type": "HowTo", "name": "십자말풀이 하는 법",
                "step": [{"@type": "HowToStep", "name": n, "text": t} for n, t in [
                    ("힌트와 칸 수 확인", "번호가 적힌 칸에서 가로 방향과 세로 방향 힌트를 확인하고 정답의 글자 수를 센다."),
                    ("확실한 단어부터 채우기", "답을 확신하는 단어를 먼저 적는다."),
                    ("교차점 활용", "가로와 세로가 겹치는 칸의 글자를 단서로 막힌 단어를 추리한다."),
                    ("남은 칸 정리", "채운 글자가 힌트와 맞는지 검토하고 남은 칸을 채운다.")]]}
    body = f"""
<div class="crumb"><a href="/">홈</a> › 십자말풀이 하는 법</div>
<span class="badge">퍼즐 가이드</span>
<h1>십자말풀이 하는 법과 요령</h1>
<div class="sub">가로세로 낱말퀴즈를 처음 하는 분을 위한 안내</div>
<div class="summary">십자말풀이(가로세로 낱말퀴즈)는 가로 힌트와 세로 힌트를 보고 칸에 글자를 채워 넣는 퍼즐입니다. 한 칸에 한 글자를 넣고, 가로 단어와 세로 단어가 만나는 칸에서는 같은 글자를 쓰는 것이 기본 규칙입니다.</div>

<h2>기본 규칙</h2>
{li([
    "번호가 적힌 칸에서 시작하는 단어가 있고, 번호는 가로 힌트와 세로 힌트 목록에 각각 대응합니다.",
    "정답의 글자 수만큼 칸이 이어져 있습니다. 칸 수는 가장 큰 단서입니다.",
    "가로와 세로가 겹치는 칸에는 두 단어에 모두 맞는 글자가 들어갑니다.",
    "검은 칸은 단어가 끝났다는 뜻이며 글자를 넣지 않습니다.",
])}

<h2>단계별로 푸는 순서</h2>
{li([
    "<b>1단계</b> 힌트를 쭉 읽고 바로 답이 떠오르는 것부터 적습니다.",
    "<b>2단계</b> 적은 글자가 교차하는 다른 단어의 시작이나 중간 글자가 됩니다. 그 글자를 단서로 막힌 단어를 추리합니다.",
    "<b>3단계</b> 글자 수가 적은 단어는 선택지가 좁아 의외로 쉬운 경우가 많습니다.",
    "<b>4단계</b> 끝까지 막힌 칸은 힌트를 다시 읽고 다른 뜻은 없는지 생각해 봅니다.",
])}

<h2>한글 십자말풀이만의 특징</h2>
<p>영어 크로스워드는 한 칸에 알파벳 한 글자를 넣지만, 한글은 한 칸에 '가', '성' 같은 음절 하나를 넣습니다. 같은 글자 수라도 정보량이 많고 받침이 있는 글자도 한 칸에 들어갑니다. 그래서 교차 칸의 글자가 받침까지 맞아야 하므로, 교차 단서가 영어보다 강력하게 작용합니다.</p>

<h2>십자말풀이의 유래</h2>
<p>1913년 12월 21일 미국 뉴욕의 신문 '뉴욕 월드' 일요판에 아서 윈이 실은 단어 퍼즐이 최초의 크로스워드로 널리 알려져 있습니다. 이후 전 세계 신문과 잡지의 단골 코너가 되었고, 지금은 온라인과 앱에서도 즐깁니다.</p>

<h2>바로 해 보기</h2>
<p>성경 낱말로 해 보면 힌트가 익숙해서 입문용으로 좋습니다. 아래 퍼즐은 단어가 쉬운 편입니다.</p>
{cards_for(["gen_002", "bib_107", "bib_125", "nan_131"], "howto_pick_puzzle")}
<p class="note">성경 퍼즐 전체는 <a href="/bible-crossword.html">성경 십자말풀이</a>에서, 모르는 인물은 <a href="/dictionary/">성경사전</a>에서 찾아볼 수 있습니다.</p>

<div class="faq"><h2>자주 묻는 질문</h2>{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)}</div>
"""
    return page("/how-to-crossword.html", "십자말풀이 하는 법·요령 총정리 (가로세로 낱말퀴즈) | 십자가로세로",
                "십자말풀이(가로세로 낱말퀴즈) 기본 규칙, 단계별 푸는 요령, 한글 크로스워드의 특징과 유래를 쉽게 정리했습니다. 초보도 바로 시작할 수 있어요.", body, faq_ld(faqs, howto_ld))


if __name__ == "__main__":
    for name, fn in (("church-bulletin-puzzle.html", church), ("editorial-policy.html", policy),
                     ("bible-crossword.html", bible_crossword), ("how-to-crossword.html", howto)):
        open(os.path.join(ROOT, name), "w", encoding="utf-8").write(fn())
    print("생성 완료")
