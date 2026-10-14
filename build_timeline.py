# -*- coding: utf-8 -*-
"""성경 연대표(/dictionary/timeline/): 시대 개요와 시대별 페이지."""
import json
import os

from timeline_data import ERAS
from build_map_page import EXTRA_HEAD  # noqa: F401  (사용 안 함, 일관성)

CSS = """<style>
.tl{position:relative;margin:18px 0 8px;padding-left:20px;border-left:3px solid #cfe0f7}
.tl-item{position:relative;background:#fff;border:1px solid #e5e5e5;border-radius:14px;padding:14px 16px;margin:0 0 14px;display:block;text-decoration:none!important;color:#222!important}
.tl-item:before{content:"";position:absolute;left:-30px;top:20px;width:14px;height:14px;border-radius:50%;background:#0073e6;border:3px solid #fff;box-shadow:0 0 0 2px #cfe0f7}
.tl-item:hover{border-color:#0073e6}.tl-item b{display:block;font-size:17px}.tl-item em{font-style:normal;color:#0b5cad;font-size:13px;font-weight:700}
.tl-item span{display:block;font-size:14px;color:#556;margin-top:4px;line-height:1.6}
.era-nav{display:flex;justify-content:space-between;gap:10px;margin:22px 0}.era-nav a{flex:1;background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:12px;text-decoration:none;color:#222;font-size:14px}
.era-nav a:hover{border-color:#0073e6}.era-nav small{display:block;color:#7b8794;font-size:12px}
.pts{padding-left:20px}.pts li{margin:6px 0}
</style>"""


def render_all(ctx):
    ENTRIES, BY_SLUG, head, esc, FOOTER, SITE, OUT = (ctx[k] for k in ("ENTRIES", "BY_SLUG", "head", "esc", "FOOTER", "SITE", "OUT"))
    tdir = os.path.join(OUT, "timeline")
    os.makedirs(tdir, exist_ok=True)

    def cards(slugs):
        return '<div class="cards">' + "".join(
            f'<a class="card" href="/dictionary/{s}.html"><b>{esc(BY_SLUG[s]["name"])}</b><span>{esc(BY_SLUG[s]["sub"])}</span></a>' for s in slugs) + "</div>"

    # 개요
    path = "/dictionary/timeline/"
    title = "성경 연대표 - 시대별 사건·인물·지명 한눈에 보기 | 성경사전 | 십자가로세로"
    desc = "창조와 족장 시대부터 출애굽, 왕국, 포로기, 예수님의 시대, 초대교회까지 성경의 흐름을 시대별로 정리했습니다. 시대마다 사건·인물·지명과 지도를 함께 볼 수 있어요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "ItemList", "name": "성경 연대표", "description": desc, "inLanguage": "ko", "url": SITE + path,
        "itemListElement": [{"@type": "ListItem", "position": i, "name": e["name"], "url": f"{SITE}/dictionary/timeline/{e['slug']}.html"} for i, e in enumerate(ERAS, 1)]},
        ensure_ascii=False) + "</script>"
    out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › 연대표</div>')
    out.append('<h1>⏳ 성경 연대표</h1><div class="sub">창조에서 초대교회까지, 시대별로 따라가는 성경의 흐름</div>')
    out.append('<div class="summary">시대를 눌러 그 시대의 사건, 인물, 지명과 지도를 볼 수 있습니다. 성경 연대는 학자마다 의견이 달라서 대략적인 시기("경")로 표기했고, 학설이 나뉘는 부분은 그렇다고 밝혔습니다.</div>')
    out.append('<div class="tl">' + "".join(
        f'<a class="tl-item" href="/dictionary/timeline/{e["slug"]}.html" data-ga="timeline_era" data-ga-label="{e["slug"]}">'
        f'<em>{esc(e["period"])}</em><b>{e["icon"]} {esc(e["name"])}</b><span>{esc(e["summary"])}</span></a>' for e in ERAS) + "</div>")
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    open(os.path.join(tdir, "index.html"), "w", encoding="utf-8").write("\n".join(out))

    # 시대별
    for i, e in enumerate(ERAS):
        path = f"/dictionary/timeline/{e['slug']}.html"
        title = f"{e['name']} - 사건·인물·지명 정리 | 성경 연대표 | 십자가로세로"
        desc = f"{e['name']}({e['period']})의 핵심 사건, 인물, 지명을 정리했습니다. {e['summary'][:60]}"
        has_map = os.path.exists(os.path.join(os.path.dirname(OUT), "images", "maps", f"era-{e['slug']}.png"))
        img = f"{SITE}/images/maps/era-{e['slug']}.png" if has_map else None
        faq = [(f"{e['name']}은 언제인가요?", f"{e['period']}으로 추정되며, 성경 연대는 학자마다 의견이 다릅니다."),
               (f"{e['name']}은 성경 어디에 나오나요?", f"{e['refs']}에 기록되어 있습니다.")]
        ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
            {"@context": "https://schema.org", "@type": "Article", "headline": f"{e['name']} - 성경 연대표", "description": desc, "inLanguage": "ko",
             "author": {"@type": "Organization", "name": "십자가로세로"}, "mainEntityOfPage": SITE + path, **({"image": img} if img else {})},
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "성경사전", "item": SITE + "/dictionary/"},
                {"@type": "ListItem", "position": 3, "name": "연대표", "item": SITE + "/dictionary/timeline/"},
                {"@type": "ListItem", "position": 4, "name": e["name"], "item": SITE + path}]}))
        out = [head(title, desc, path, ld, img).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
        out.append(f'<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › <a href="/dictionary/timeline/">연대표</a> › {esc(e["name"])}</div>')
        out.append(f'<h1>{e["icon"]} {esc(e["name"])}</h1><div class="sub">{esc(e["period"])} · {esc(e["refs"])}</div>')
        out.append(f'<div class="summary">{esc(e["summary"])}</div>')
        if has_map:
            out.append(f'<figure style="margin:14px 0"><img src="/images/maps/era-{e["slug"]}.png" width="1200" height="630" alt="{esc(e["name"])} 시대의 주요 지명 지도" style="width:100%;height:auto;border-radius:14px;display:block"><figcaption style="font-size:12px;color:#7b8794;margin-top:4px">이 시대의 주요 지명 (<a href="/dictionary/map/">성경 지도에서 보기</a>)</figcaption></figure>')
        out.append("<h2>핵심 흐름</h2><ul class=\"pts\">" + "".join(f"<li>{esc(p)}</li>" for p in e["points"]) + "</ul>")
        if e["events"]:
            out.append("<h2>주요 사건</h2>" + cards(e["events"]))
        if e["people"]:
            out.append("<h2>주요 인물</h2>" + cards(e["people"]))
        if e["places"]:
            out.append("<h2>주요 지명</h2>" + cards(e["places"]))
        out.append("<h2>이 시대를 읽을 성경</h2>" + cards(e["books"]))
        out.append('<h2>자주 묻는 질문</h2><div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</div>")
        nav = ""
        if i > 0:
            p = ERAS[i - 1]
            nav += f'<a href="/dictionary/timeline/{p["slug"]}.html"><small>← 이전 시대</small>{esc(p["name"])}</a>'
        if i < len(ERAS) - 1:
            n = ERAS[i + 1]
            nav += f'<a href="/dictionary/timeline/{n["slug"]}.html" style="text-align:right"><small>다음 시대 →</small>{esc(n["name"])}</a>'
        out.append(f'<div class="era-nav">{nav}</div>')
        out.append("</main>")
        out.append(FOOTER)
        out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
        open(os.path.join(tdir, f"{e['slug']}.html"), "w", encoding="utf-8").write("\n".join(out))
    return [e["slug"] for e in ERAS]
