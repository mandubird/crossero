# -*- coding: utf-8 -*-
"""성경 가계도(/dictionary/genealogy/): 아담~노아, 야곱의 열두 아들, 아브라함~예수님(마 1장)."""
import json
import os

NAME2SLUG = {"아담": "adam-and-eve", "노아": "noah", "아브라함": "abraham", "이삭": "isaac", "야곱": "jacob", "다윗": "david",
             "솔로몬": "solomon", "히스기야": "hezekiah", "요시야": "josiah", "보아스": "ruth", "오벳": "ruth", "예수": "jesus",
             "요셉": None, "유다": "judah", "라합": "rahab", "밧세바": "bathsheba"}
CSS = """<style>
.gen{display:flex;flex-direction:column;align-items:stretch;margin:12px 0 22px}
.gen-g{margin:0 0 4px;padding:10px 14px;border-radius:12px;background:#eaf3ff;border:1px solid #bcd6f7;font-weight:700;color:#0b5cad}
.gen-row{display:flex;align-items:center;gap:10px;position:relative;margin:0 0 0 22px;padding:7px 0 7px 22px;border-left:3px solid #cfe0f7}
.gen-row:before{content:"";position:absolute;left:-9px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:#fff;border:3px solid #0073e6}
.gen-n{font-size:12px;color:#8a97a6;min-width:24px}.gen-p{font-weight:700;color:#222;text-decoration:none}
.gen-p.link{color:#0073e6}.gen-w{font-size:12px;background:#fff0f3;color:#b0224a;border-radius:10px;padding:2px 9px}
.gen-note{font-size:13px;color:#667;margin:2px 0 10px}
.sons{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:10px 0 22px}.mom{background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:10px 14px}
.mom h3{margin:0 0 6px;font-size:15px}.mom span{display:inline-block;background:#f1f6ff;border-radius:14px;padding:3px 11px;margin:3px 4px 3px 0;font-size:14px}
@media(max-width:600px){.sons{grid-template-columns:1fr}}
</style>"""

ANCESTORS = ["아담", "셋", "에노스", "게난", "마할랄렐", "야렛", "에녹", "므두셀라", "라멕", "노아"]
SONS = [("레아", ["르우벤", "시므온", "레위", "유다", "잇사갈", "스불론"]), ("라헬", ["요셉", "베냐민"]), ("빌하(라헬의 몸종)", ["단", "납달리"]), ("실바(레아의 몸종)", ["갓", "아셀"])]
MATT = [
    ("아브라함부터 다윗까지 14대 (마 1:2-6)", [("아브라함", ""), ("이삭", ""), ("야곱", ""), ("유다", "다말에게서 베레스를 낳음"), ("베레스", ""), ("헤스론", ""), ("람", ""), ("아미나답", ""), ("나손", ""),
                                     ("살몬", "라합에게서 보아스를 낳음"), ("보아스", "룻에게서 오벳을 낳음"), ("오벳", ""), ("이새", ""), ("다윗", "왕")]),
    ("다윗부터 바벨론 포로까지 14대 (마 1:6-11)", [("다윗", "위 그룹과 겹침, 우리야의 아내에게서 솔로몬을 낳음"), ("솔로몬", ""), ("르호보암", ""), ("아비야", ""), ("아사", ""), ("여호사밧", ""), ("요람", ""),
                                       ("웃시야", ""), ("요담", ""), ("아하스", ""), ("히스기야", ""), ("므낫세", ""), ("아몬", ""), ("요시야", "")]),
    ("바벨론 포로 후부터 그리스도까지 14대 (마 1:12-16)", [("여고냐", "바벨론으로 끌려갈 때"), ("스알디엘", ""), ("스룹바벨", ""), ("아비훗", ""), ("엘리아김", ""), ("아소르", ""), ("사독", ""),
                                            ("아킴", ""), ("엘리웃", ""), ("엘르아살", ""), ("맛단", ""), ("야곱", ""), ("요셉", "마리아의 남편"), ("예수", "그리스도")]),
]


def render(ctx):
    head, esc, FOOTER, SITE, OUT, BY_SLUG = (ctx[k] for k in ("head", "esc", "FOOTER", "SITE", "OUT", "BY_SLUG"))
    path = "/dictionary/genealogy/"
    title = "성경 가계도(성경 족보) - 아담에서 노아, 아브라함에서 예수님까지 | 십자가로세로"
    desc = "아담에서 노아까지 10대, 야곱의 열두 아들, 마태복음 1장의 아브라함에서 예수 그리스도까지 42대를 가계도로 정리했습니다."
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>\n" for x in (
        {"@context": "https://schema.org", "@type": "Article", "headline": "성경 가계도", "description": desc, "inLanguage": "ko",
         "author": {"@type": "Organization", "name": "십자가로세로"}, "mainEntityOfPage": SITE + path},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "성경사전", "item": SITE + "/dictionary/"},
            {"@type": "ListItem", "position": 3, "name": "가계도", "item": SITE + path}]}))
    out = [head(title, desc, path, ld).replace("</head>", CSS + "\n</head>", 1), '<main class="wrap">']
    out.append('<div class="crumb"><a href="/">홈</a> › <a href="/dictionary/">성경사전</a> › 가계도</div>')
    out.append('<h1>👪 성경 가계도</h1><div class="sub">아담에서 노아, 아브라함에서 예수님까지</div>')
    out.append('<div class="summary">성경은 이름의 계보를 통해 하나님의 약속이 이어져 온 흐름을 보여 줍니다. 파란 이름은 사전 항목으로 연결됩니다. 가계의 세대 수와 이름은 성경 본문에 따랐으며, 복음서 사이의 차이는 아래에 따로 적었습니다.</div>')

    def person(n, note="", num=None):
        slug = NAME2SLUG.get(n)
        cls = "gen-p link" if slug and slug in BY_SLUG else "gen-p"
        nm = f'<a class="{cls}" href="/dictionary/{slug}.html">{esc(n)}</a>' if slug and slug in BY_SLUG else f'<span class="{cls}">{esc(n)}</span>'
        w = f'<span class="gen-w">{esc(note)}</span>' if note else ""
        return f'<div class="gen-row"><span class="gen-n">{num or ""}</span>{nm}{w}</div>'

    out.append('<h2>1. 아담에서 노아까지 (창세기 5장)</h2><div class="gen">' + "".join(person(n, "", i) for i, n in enumerate(ANCESTORS, 1)) + "</div>")
    out.append('<div class="gen-note">창세기 5장의 계보는 10대로 정리됩니다. 계보에 나온 나이를 연대로 바로 계산할 수 있는지에 대해서는 학자들의 의견이 다릅니다.</div>')

    out.append('<h2>2. 야곱의 열두 아들 (창세기 29–35장)</h2><div class="sons">' + "".join(
        f'<div class="mom"><h3>{esc(m)}</h3>' + "".join(f"<span>{esc(s)}</span>" for s in sons) + "</div>" for m, sons in SONS) + "</div>")
    out.append('<div class="gen-note">이 열두 아들이 이스라엘 열두 지파의 조상이 되었습니다. 요셉의 두 아들 에브라임과 므낫세가 각각 지파를 이루어 지파 이름에 다소 차이가 있습니다.</div>')

    out.append('<h2>3. 아브라함에서 예수 그리스도까지 (마태복음 1장)</h2>')
    n = 0
    for gname, plist in MATT:
        out.append(f'<div class="gen"><div class="gen-g">{esc(gname)}</div>')
        for nm, note in plist:
            n += 1
            out.append(person(nm, note, None))
        out.append("</div>")
    out.append('<div class="gen-note">마태복음은 계보를 14대씩 세 구간으로 나누어(마 1:17) 일부 왕(아하시야, 요아스, 아마샤, 여호야김)을 생략했습니다. 누가복음 3:23-38의 계보는 이름이 달라 마리아 쪽 혈통이라는 견해와 다른 방식으로 정리했다는 견해가 있습니다.</div>')
    out.append("<h2>함께 보기</h2><div class=\"cards\">" + "".join(
        f'<a class="card" href="/dictionary/{s}.html"><b>{esc(BY_SLUG[s]["name"])}</b><span>{esc(BY_SLUG[s]["sub"])}</span></a>'
        for s in ("abraham", "isaac", "jacob", "david", "jesus") if s in BY_SLUG) + "</div>")
    out.append("</main>")
    out.append(FOOTER)
    out.append('<script src="/ga-events.js"></script><script src="/subscribe.js"></script>\n</body>\n</html>\n')
    d = os.path.join(OUT, "genealogy")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(out))
