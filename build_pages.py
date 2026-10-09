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


if __name__ == "__main__":
    for name, fn in (("church-bulletin-puzzle.html", church), ("editorial-policy.html", policy)):
        open(os.path.join(ROOT, name), "w", encoding="utf-8").write(fn())
    print("생성 완료")
