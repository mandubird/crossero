# -*- coding: utf-8 -*-
"""검수 참여·의견 보내기·수정 이력 페이지(/feedback/)."""
import json
import os

from feedback_log import FEEDBACK


def render(ctx):
    head, esc, FOOTER, SITE, OUT = (ctx[k] for k in ("head", "esc", "FOOTER", "SITE", "OUT"))
    path = "/feedback/"
    title = "검수 참여와 의견 보내기 · 수정 이력 | 십자가로세로"
    desc = "십자가로세로의 성경사전·지도·연대표 내용에 대한 의견을 받습니다. 대한예수교장로회 소속 목회자를 비롯한 교회 지도자의 피드백을 반영하고, 수정 이력을 공개합니다."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "name": "검수 참여와 의견 보내기", "description": desc, "inLanguage": "ko", "url": SITE + path}, ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › 검수 참여·수정 이력</div>')
    out.append('<h1>✉️ 검수 참여와 수정 이력</h1><div class="sub">성경 콘텐츠를 함께 다듬어 가는 곳</div>')
    out.append('<div class="summary">십자가로세로의 성경사전·성경 지도·연대표·가계도는 한 사람의 운영자가 만든 것이어서 틀리거나 아쉬운 부분이 있을 수 있습니다. '
               '<b>대한예수교장로회 소속 목사님을 비롯한 교회 지도자와 교사의 피드백</b>을 주시면 확인 후 반영하겠습니다.</div>')
    out.append('<a class="cta" href="mailto:mandubird@naver.com?subject=%5B%EC%8B%AD%EC%9E%90%EA%B0%80%EB%A1%9C%EC%84%B8%EB%A1%9C%20%EA%B2%80%EC%88%98%5D%20%EC%9D%98%EA%B2%AC" data-ga="feedback_click" data-ga-label="feedback_page">✉️ 의견 보내기<small>mandubird@naver.com · 항목 이름과 의견을 적어 주세요</small></a>')
    out.append("<h2>이렇게 반영합니다</h2><ul>"
               "<li><b>사실 관계(구절·숫자·이름):</b> 성경 본문과 대조해 바로 수정합니다.</li>"
               "<li><b>교단별 입장이 갈리는 설명:</b> 한쪽 입장으로 단정하지 않고, 이해가 갈린다는 점을 밝히는 방향으로 다듬습니다.</li>"
               "<li><b>학설이 갈리는 연대·위치·저자:</b> 대표 견해를 함께 소개하고 '학설이 갈린다'고 표기합니다.</li>"
               "<li><b>반영 이력:</b> 의견을 반영한 내용은 아래 수정 이력에 공개합니다. 보내 주신 분의 이름은 동의 없이 밝히지 않습니다.</li></ul>")
    out.append("<h2>특히 의견을 구하는 부분</h2><ul>"
               "<li>세례·성찬·칭의·구원·안식일·성령·마리아·예수 그리스도 항목의 표현</li>"
               "<li>출애굽 연대, 십자가의 해, 이사야·요한계시록 저자 등 학설이 갈리는 설명</li>"
               "<li>요한계시록 일곱 교회 등 해석이 필요한 본문의 어조</li></ul>")
    out.append("<h2>수정 이력</h2>")
    rows = "".join(
        f'<tr><td style="white-space:nowrap;padding:8px 10px;border-bottom:1px solid #eee">{esc(f["date"])}</td><td style="padding:8px 10px;border-bottom:1px solid #eee"><b>{esc(f["target"])}</b>'
        f'<br><span style="color:#667">{esc(f["source"])}</span></td><td style="padding:8px 10px;border-bottom:1px solid #eee">{esc(f["summary"])}<br><b>조치:</b> {esc(f["action"])}</td></tr>'
        for f in FEEDBACK)
    out.append('<table style="width:100%;border-collapse:collapse;font-size:14px;background:#fff;border:1px solid #e5e5e5;border-radius:10px"><thead><tr style="background:#f5f9ff"><th style="text-align:left;padding:8px 10px">날짜</th><th style="text-align:left;padding:8px 10px">대상</th><th style="text-align:left;padding:8px 10px">내용</th></tr></thead><tbody>' + rows + "</tbody></table>")
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    d = os.path.join(os.path.dirname(OUT), "feedback")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(out))
