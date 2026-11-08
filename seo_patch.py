# -*- coding: utf-8 -*-
"""SEO/AEO 일괄 보강(여러 번 실행해도 안전): canonical, h1, JSON-LD, twitter 카드.
사용: python3 seo_patch.py"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = ("backup", "node_modules", "youtube_shorts_generator", "blog_drafts", ".git")
BASE = "https://crossero.com/"
stat = {"canonical": 0, "h1": 0, "jsonld": 0, "twitter": 0}


def rd(p):
    return open(p, encoding="utf-8").read()


def wr(p, s):
    open(p, "w", encoding="utf-8").write(s)


def meta(s, prop):
    m = re.search(r'<meta (?:property|name)="%s" content="([^"]*)"' % re.escape(prop), s)
    return m.group(1) if m else ""


def patch(rel, fn):
    p = os.path.join(ROOT, rel)
    s = rd(p)
    n = fn(s)
    if n != s:
        wr(p, n)


# 1) canonical ---------------------------------------------------------
def add_canonical(rel, url):
    def f(s):
        if 'rel="canonical"' in s:
            return s
        stat["canonical"] += 1
        return s.replace("</title>", '</title>\n<link rel="canonical" href="%s">' % url, 1)
    patch(rel, f)


add_canonical("play.html", BASE + "play.html")
add_canonical("play2.html", BASE + "play.html")  # play2는 noindex 복제본 → 본체로 지정
add_canonical("supporters.html", BASE + "supporters.html")
patch("play.html", lambda s: s.replace('<meta property="og:url" content="https://crossero.com">', '<meta property="og:url" content="https://crossero.com/play.html">'))
patch("play2.html", lambda s: s.replace("<title>퍼즐 플레이 | 십자가로세로</title>", "<title>퍼즐 플레이(공유용) | 십자가로세로</title>"))

# 2) h1 ----------------------------------------------------------------
def h1_play(s):
    if "<h1" in s:
        return s
    n = s.replace('<p id="dynamicTitle">', '<h1 id="dynamicTitle">', 1).replace('<p id="dynamicTitle">말씀', '<h1 id="dynamicTitle">말씀')
    n = re.sub(r'(<h1 id="dynamicTitle">[^<]*)</p>', r"\1</h1>", n, count=1)
    n = n.replace("</style>", "header h1#dynamicTitle{font-size:16px;font-weight:400;margin:1em 0;color:inherit}\n</style>", 1)
    stat["h1"] += 1
    return n


patch("play.html", h1_play)
patch("play2.html", h1_play)


def h1_about(s):
    if "<h1" in s:
        return s
    n = s.replace("<h2>십자가로세로는 어떤 사이트인가요?</h2>", "<h1>십자가로세로는 어떤 사이트인가요?</h1>", 1)
    n = n.replace(".section h2 {", ".section h1 {\n  margin-top:0;\n  color:#0073e6;\n  font-size:1.5em;\n}\n\n.section h2 {", 1)
    n = n.replace("  .section h2 { font-size: 18px !important; }", "  .section h2, .section h1 { font-size: 18px !important; }", 1)
    stat["h1"] += 1
    return n


patch("about.html", h1_about)


def h1_list(s):
    if "<h1" in s:
        return s
    n = s.replace("<h2>📚 성경 말씀 퍼즐 모음</h2>", "<h1>📚 성경 말씀 퍼즐 모음</h1>", 1)
    n = n.replace("h2 {\n  margin-bottom:20px;", "h1 {\n  margin-bottom:20px;\n  font-size: 24px;\n  color: #333;\n}\nh2 {\n  margin-bottom:20px;", 1)
    n = n.replace("  h2 { font-size: 19px !important; }", "  h2, h1 { font-size: 19px !important; }", 1)
    stat["h1"] += 1
    return n


patch("list.html", h1_list)

# 3) JSON-LD (구조화 데이터가 없는 소개/정책 페이지) --------------------------
ORG = {"@type": "Organization", "name": "십자가로세로", "url": BASE, "logo": BASE + "images/crossero-logo.png", "email": "mandubird@naver.com"}
LD_TYPE = {"about.html": "AboutPage", "list.html": "CollectionPage"}


def add_ld(rel):
    def f(s):
        if "application/ld+json" in s:
            return s
        title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
        desc = html.unescape(meta(s, "description"))
        url = BASE + rel
        data = {"@context": "https://schema.org", "@type": LD_TYPE.get(rel, "WebPage"), "name": html.unescape(title), "url": url,
                "inLanguage": "ko", "description": desc, "isPartOf": {"@type": "WebSite", "name": "십자가로세로", "url": BASE}, "publisher": ORG}
        if rel == "about.html":
            data["mainEntity"] = ORG
        tag = '<script type="application/ld+json">%s</script>\n' % json.dumps(data, ensure_ascii=False)
        stat["jsonld"] += 1
        return s.replace("</head>", tag + "</head>", 1)
    patch(rel, f)


for r in ("about.html", "list.html", "editorial-policy.html", "supporters.html", "sunday-school-material.html", "terms.html", "privacy.html",
          "puzzle-category-bible.html", "sponsor.html", "support.html"):
    add_ld(r)

# 4) twitter 카드 --------------------------------------------------------
for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(SKIP) or os.path.basename(rel).startswith(("naver", "google")):
        continue
    s = rd(f)
    if "twitter:card" in s or 'property="og:title"' not in s or "</head>" not in s:
        continue
    t, d, im = meta(s, "og:title"), meta(s, "og:description"), meta(s, "og:image")
    tags = '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n' % t
    if d:
        tags += '<meta name="twitter:description" content="%s">\n' % d
    if im:
        tags += '<meta name="twitter:image" content="%s">\n' % im
    wr(f, s.replace("</head>", tags + "</head>", 1))
    stat["twitter"] += 1

# 5) robots.txt AI 크롤러 명시 허용 ------------------------------------------
rp = os.path.join(ROOT, "robots.txt")
r = rd(rp)
if "GPTBot" not in r:
    block = "\n# AI 검색·답변 서비스 크롤러(인용·출처 표기를 환영합니다. 안내: /llms.txt)\n"
    for bot in ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"):
        block += "User-agent: %s\nAllow: /\nDisallow: /backup/\n\n" % bot
    i = r.find("# 사이트맵")
    wr(rp, r[:i] + block.lstrip("\n") + r[i:] if i >= 0 else r + block)
    stat["robots"] = 1
print(stat)
