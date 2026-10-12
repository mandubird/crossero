# -*- coding: utf-8 -*-
"""사이트 공용 메뉴·푸터. 모든 HTML에 같은 구조를 적용한다(멱등). 사용: python3 site_chrome.py"""
import glob
import os
import re

NAV_ITEMS = [  # (key, label, href)
    ("home", "홈", "/index.html"),
    ("puzzle", "퍼즐", "/play.html"),
    ("today", "오늘의 말씀", "/today/"),
    ("dict", "성경사전", "/dictionary/"),
    ("teacher", "교사허브", "/teachers/"),
    ("support", "후원", "/support.html"),
    ("about", "소개", "/about.html"),
]

FOOT_EXPLORE = [("퍼즐목록", "/list.html"), ("게시판", "/posts/index.html"), ("말씀 뽑기", "/verse/"),
                ("성경 십자말풀이", "/bible-crossword.html"), ("십자말풀이 하는 법", "/how-to-crossword.html"),
                ("주일학교 자료", "/sunday-school-materials.html"), ("교회·주일학교 활용", "/church-bulletin-puzzle.html"),
                ("⭐ 후원자", "/supporters.html")]
FOOT_POLICY = [("콘텐츠 제작 원칙", "/editorial-policy.html"), ("이용약관", "/terms.html"),
               ("개인정보처리방침", "/privacy.html"), ("FAQ", "/faq.html"), ("문의", "mailto:mandubird@naver.com")]

ACTIVE_RULES = [  # (경로 접두어/이름, key) 위에서부터 첫 일치
    ("index.html", "home"), ("play.html", "puzzle"), ("play2.html", "puzzle"), ("list.html", "puzzle"), ("posts/", "puzzle"),
    ("today/", "today"), ("verse/", "today"), ("dictionary/", "dict"), ("teachers/", "teacher"),
    ("sunday-school", "teacher"), ("church-bulletin", "teacher"),
    ("support.html", "support"), ("sponsor.html", "support"), ("supporters.html", "support"),
    ("about.html", "about"), ("faq.html", "about"), ("editorial-policy.html", "about"),
]


def active_key(path):
    for pre, key in ACTIVE_RULES:
        if path.startswith(pre):
            return key
    return None


def nav_html(key):
    rows = [f'  <a href="{h}" class="nav-item{" nav-active" if k == key else ""}">{t}</a>' for k, t, h in NAV_ITEMS]
    return '<nav class="nav">\n' + "\n".join(rows) + "\n</nav>"


def _row(links):
    a = "".join(f'\n    <a href="{h}" style="font-size:13px;color:#666;text-decoration:none;">{t}</a>' for t, h in links)
    return f'  <div class="footer-links" style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-bottom:12px;">{a}\n  </div>'


def footer_links_html():
    return _row(FOOT_EXPLORE) + "\n" + _row(FOOT_POLICY)


def _enclosing_div(s, idx):
    start = s.rfind("<div", 0, idx)
    end = s.find("</div>", idx)
    if start < 0 or end < 0:
        return None
    if "<div" in s[start + 4:end]:
        return None
    return start, end + 6


def apply(path, s):
    key = active_key(path)
    s = re.sub(r'<nav class="nav">.*?</nav>', lambda m: nav_html(key), s, count=1, flags=re.S)
    f0 = s.find("<footer")
    if f0 < 0:
        return s
    f1 = s.find("</footer>", f0)
    foot = s[f0:f1]
    # 만든 이유/후원 응원 버튼 줄 제거
    i = foot.find("만든 이유")
    if i >= 0:
        r = _enclosing_div(foot, i)
        if r:
            foot = foot[:r[0]] + foot[r[1]:]
    # 이미 적용된 줄 제거 후, 기존 링크 줄이 있던 자리에 한 번만 삽입
    rows = re.compile(r'[ \t]*<div class="footer-links"[^>]*>.*?</div>\n?', re.S)
    if 'footer-links' in foot:
        m = rows.search(foot)
        pos = m.start()
        foot = rows.sub("", foot)
        foot = foot[:pos] + footer_links_html() + "\n" + foot[pos:]
        return s[:f0] + foot + s[f1:]
    i = foot.find("privacy.html")
    if i < 0:
        i = foot.find("sunday-school-materials.html")
    if i >= 0:
        r = _enclosing_div(foot, i)
        if r:
            foot = foot[:r[0]] + footer_links_html() + foot[r[1]:]
    return s[:f0] + foot + s[f1:]


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    n = 0
    for f in glob.glob(os.path.join(root, "**/*.html"), recursive=True):
        rel = os.path.relpath(f, root)
        if rel.startswith(("node_modules", "images")):
            continue
        s = open(f, encoding="utf-8").read()
        if '<nav class="nav">' not in s:
            continue
        t = apply(rel, s)
        if t != s:
            open(f, "w", encoding="utf-8").write(t)
            n += 1
    print(f"공용 메뉴·푸터 적용: {n}개 파일")


if __name__ == "__main__":
    main()
