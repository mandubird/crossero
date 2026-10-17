# -*- coding: utf-8 -*-
"""사전 항목·연대표 하단의 의견 보내기 박스."""
from html import escape
from urllib.parse import quote

SENSITIVE = {"baptism", "communion", "justification", "salvation", "sabbath", "holy-spirit", "mary", "jesus", "trinity", "covenant", "sanctification", "grace", "gospel", "church",
             "kingdom-of-god", "sin", "repentance", "isaiah", "john-apostle", "golgotha", "mount-sinai", "tabor", "hermon"}
SENSITIVE_ERAS = {"exodus", "jesus"}


def box(slug, name, sensitive=False):
    subj = quote(f"[십자가로세로 검수] {name}")
    page = f"https://crossero.com/{slug[3:]}.html" if slug.startswith("../") else f"https://crossero.com/dictionary/{slug}.html"
    body = quote(f"검수 대상: {name}\n페이지: {page}\n\n(소속·직분과 의견을 자유롭게 적어 주세요)")
    href = f"mailto:mandubird@naver.com?subject={subj}&body={body}"
    if sensitive:
        msg = ("교단마다 이해가 다를 수 있는 내용입니다. <b>대한예수교장로회 소속 목사님을 비롯한 교회 지도자의 피드백</b>을 주시면 확인 후 반영하겠습니다.")
        bg = "#fff8ec;border:1px solid #fcd9a8"
    else:
        msg = "이 항목의 설명이나 인용 구절에 의견이 있으신가요? 확인 후 반영하겠습니다."
        bg = "#f5f9ff;border:1px solid #d6e2f1"
    return (f'<aside class="fbbox" style="margin:26px 0 8px;padding:14px 16px;border-radius:14px;background:{bg};font-size:14px;line-height:1.7;color:#445">'
            f'{msg}<br><a href="{href}" data-ga="feedback_click" data-ga-label="{escape(slug)}" style="display:inline-block;margin-top:6px;font-weight:700;color:#0073e6">✉️ 의견 보내기</a>'
            f' · <a href="/feedback/" style="color:#0073e6">검수 참여·수정 이력 보기</a></aside>')
