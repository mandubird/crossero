# -*- coding: utf-8 -*-
"""송구영신 카운트다운 페이지(/verse/new-year/countdown/) 생성. 실행: python3 build_countdown.py
예배 화면(대형 화면)에 띄우는 새해 카운트다운 + 자정에 새해 말씀 뽑기로 연결. 서버·가입 없음."""
import json
import os
import re

import build_dictionary as bd
from build_dictionary import head, FOOTER, NAV, SITE, ROOT
from season_picks import SEASONS
from verse_lib import KO_BOOKS, load_text

PATH = "/verse/new-year/countdown/"
TITLE = "송구영신 카운트다운 - 12월 31일 예배 화면용 새해 카운트다운과 말씀 뽑기 | 십자가로세로"
DESC = "송구영신예배에서 대형 화면에 띄우는 새해 카운트다운입니다. 자정이 되면 새해 말씀 뽑기로 이어지고, 기다리는 동안 새해 말씀이 한 구절씩 나옵니다. 가입 없이 무료로 쓸 수 있습니다."
NEWYEAR = "2027-01-01T00:00:00+09:00"

FAQ = [
    ("송구영신 카운트다운은 어떻게 쓰나요?", "예배 화면에 이 페이지를 열고 '큰 화면 모드'를 누르면 글자가 크게 표시됩니다. 한국 시간 기준으로 2027년 1월 1일 0시까지 남은 시간이 줄어들고, 0시가 되면 새해 인사와 함께 새해 말씀 뽑기 주소가 나옵니다."),
    ("미리 연습해 볼 수 있나요?", "주소 끝에 ?test=30 을 붙이면 30초 카운트다운으로 연습할 수 있습니다. 예: crossero.com/verse/new-year/countdown/?test=30"),
    ("교회 이름을 화면에 넣을 수 있나요?", "주소 끝에 ?c=교회이름 을 붙이면 화면 위쪽에 교회 이름이 표시됩니다. 예: ?c=은혜교회"),
    ("시계가 정확한가요?", "기기의 시계를 한국 시간으로 계산합니다. 기기 시간이 틀려 있으면 카운트다운도 틀리므로, 행사 전에 시간을 확인하거나 연습 모드로 점검하세요."),
    ("인터넷이 끊기면 어떻게 되나요?", "페이지를 한 번 열어 두면 카운트다운은 기기 안에서 계속 진행됩니다. 다만 0시 이후 새해 말씀 뽑기 페이지를 열려면 인터넷이 필요합니다."),
    ("말씀 뽑기는 어떻게 이어지나요?", "0시가 되면 '새해 말씀 뽑기' 버튼이 나타납니다. 성도들은 각자 휴대폰으로 새해 말씀 뽑기 페이지에서 한 장씩 뽑을 수 있고, 교회에서 카드를 인쇄해 상자에서 뽑는 방법도 송구영신 가이드에 정리되어 있습니다."),
]


def verses():
    text = load_text()
    out, seen = [], set()
    for name, c, v in SEASONS["new-year"]["picks"]:
        t = text[(KO_BOOKS.index(name) + 1, c, v)]
        ref = f"{name} {c}:{v}"
        if len(t) <= 70 and ref not in seen:
            seen.add(ref)
            out.append({"ref": ref, "text": t})
    return out


CSS = """
.cd-wrap{min-height:calc(100vh - 60px);background:radial-gradient(circle at 50% 30%,#2b4170 0%,#162038 70%);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:30px 18px 36px;position:relative}
.cd-church{font-size:20px;color:#c9d6ee;letter-spacing:.1em;margin:0 0 8px;min-height:28px}
.cd-title{font-size:18px;font-weight:600;color:#c9d6ee;margin:0 0 14px;letter-spacing:.1em}
.cd-time{font-size:78px;font-weight:300;letter-spacing:.06em;font-variant-numeric:tabular-nums;line-height:1.1;margin:0}
.cd-sub{font-size:16px;color:#b9c8e6;margin:6px 0 24px}
.cd-verse{max-width:720px;min-height:130px;display:flex;flex-direction:column;justify-content:center;transition:opacity .6s}
.cd-vt{font-size:26px;line-height:1.8;word-break:keep-all;font-family:'Noto Serif KR','Nanum Myeongjo',serif;margin:0 0 8px}.cd-vr{font-size:16px;color:#b9c8e6}
.cd-btns{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:22px 0 0}
.cd-btn{border:1px solid #ffffff66;background:#ffffff1f;color:#fff;border-radius:30px;padding:12px 24px;font-size:16px;font-weight:700;cursor:pointer;text-decoration:none;font-family:inherit}
.cd-btn.main{background:#fff;color:#162038;border-color:#fff}
.cd-new{display:none}.cd-new h2{font-size:44px;margin:0 0 10px;color:#fff}.cd-new p{font-size:20px;color:#dbe6fb;margin:0 0 6px}.cd-url{font-size:30px;font-weight:700;color:#ffe08a;margin:14px 0}
.cd-wrap.big .cd-time{font-size:min(22vw,230px)}.cd-wrap.big .cd-vt{font-size:min(4.2vw,46px)}.cd-wrap.big .cd-title{font-size:min(3vw,30px)}
.cd-wrap.big .cd-btns,.cd-wrap.big .cd-note{display:none}
.cd-wrap.done .cd-time,.cd-wrap.done .cd-sub,.cd-wrap.done .cd-title,.cd-wrap.done .cd-verse{display:none}.cd-wrap.done .cd-new{display:block}
.cd-wrap.big.done .cd-new h2{font-size:min(10vw,110px)}.cd-wrap.big.done .cd-new p{font-size:min(3vw,34px)}.cd-wrap.big.done .cd-url{font-size:min(5vw,56px)}
.cd-note{max-width:560px;margin:26px auto 0;font-size:13px;color:#9fb0d2;line-height:1.7}
.peek,.pg-pill,.pg-side{display:none!important}
.cd-info{max-width:780px;margin:0 auto;padding:26px 20px 10px;text-align:left;color:#222}.cd-info h2{font-size:20px;margin:26px 0 8px;color:#0b3d73}.cd-info p,.cd-info li{font-size:16px;line-height:1.9;word-break:keep-all}
@media(max-width:560px){.cd-time{font-size:50px}.cd-vt{font-size:21px}.cd-new h2{font-size:32px}.cd-url{font-size:22px}}
"""

JS = r"""
(function(){
  var V=window.__CV,$=function(i){return document.getElementById(i)},w=$('cdWrap'),T=new Date('__NY__').getTime(),qs=new URLSearchParams(location.search);
  var test=parseInt(qs.get('test'),10);if(test>0)T=Date.now()+test*1000+500;
  if(qs.get('c'))$('cdChurch').textContent=qs.get('c').slice(0,24);
  function p(n){return n<10?'0'+n:''+n}
  function tick(){var ms=T-Date.now();if(ms<=0){if(!w.classList.contains('done')){w.classList.add('done');if(window.crsTrack)window.crsTrack('cd_zero');}return;}
    var s=Math.ceil(ms/1000),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),sec=s%60;
    $('cdTime').textContent=(d>0?d+'일 ':'')+(d>0||h>0?p(h)+':':'')+p(m)+':'+p(sec);
    $('cdSub').textContent=d>0?'2027년 새해까지 남은 시간':'새해까지 남은 시간';}
  var i=0;function show(){var d=V[i%V.length];i++;var e=$('cdVerse');e.style.opacity=0;setTimeout(function(){$('cdVt').textContent=d.text;$('cdVr').textContent=d.ref;e.style.opacity=1;},500);}
  show();setInterval(show,18000);tick();setInterval(tick,250);
  $('cdBig').addEventListener('click',function(){w.classList.toggle('big');var on=w.classList.contains('big');$('cdBig').textContent=on?'작은 화면으로':'🖥️ 큰 화면 모드';
    if(on&&document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(function(){});if(!on&&document.fullscreenElement)document.exitFullscreen();
    if(window.crsTrack)window.crsTrack('cd_big',{on:on});});
  if(qs.get('big')==='1')w.classList.add('big');
  if(window.crsTrack)window.crsTrack('cd_view',{test:test>0});
})();
""".replace("__NY__", NEWYEAR)


def render():
    vs = verses()
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "송구영신 카운트다운", "url": SITE + PATH, "applicationCategory": "LifestyleApplication",
              "inLanguage": "ko", "operatingSystem": "Web", "description": DESC, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (app_ld, faq_ld))
    h = head(TITLE, DESC, PATH, ld).replace(NAV, NAV.replace(" nav-active", "")).replace('og:type" content="article"', 'og:type" content="website"')
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    body = f"""<main>
<section class="cd-wrap" id="cdWrap" aria-label="송구영신 카운트다운">
<div class="cd-church" id="cdChurch"></div>
<div class="cd-title">송구영신 카운트다운</div>
<h1 class="cd-time" id="cdTime" aria-live="off">--:--</h1>
<div class="cd-sub" id="cdSub">새해까지 남은 시간</div>
<div class="cd-verse" id="cdVerse"><p class="cd-vt" id="cdVt"></p><div class="cd-vr" id="cdVr"></div></div>
<div class="cd-new" id="cdNew"><h2>🎍 새해 복 많이 받으세요</h2><p>2027년, 한 해를 함께할 말씀을 뽑아 보세요</p><div class="cd-url">crossero.com/verse/new-year/</div>
<div class="cd-btns"><a class="cd-btn main" href="/verse/new-year/" data-ga="cd_to_draw">🎴 새해 말씀 뽑기</a></div></div>
<div class="cd-btns"><button class="cd-btn main" id="cdBig" type="button">🖥️ 큰 화면 모드</button><a class="cd-btn" href="/verse/new-year/guide/" data-ga="cd_to_guide">⛪ 송구영신 진행 가이드</a></div>
<p class="cd-note">한국 시간(KST) 기준 2027년 1월 1일 0시까지입니다. 기기의 시간이 맞는지 확인하고, 행사 전에 주소 끝에 ?test=30 을 붙여 연습해 보세요.</p>
</section>
<section class="cd-info">
<h2>예배에서 이렇게 쓰세요</h2>
<ol><li>예배 화면 컴퓨터에서 이 페이지를 열고 '큰 화면 모드'를 누릅니다.</li><li>카운트다운이 진행되는 동안 새해 말씀이 한 구절씩 바뀌어 나옵니다. 함께 읽거나 조용히 묵상하는 시간으로 쓰세요.</li><li>0시가 되면 새해 인사와 새해 말씀 뽑기 주소가 나옵니다. 성도들은 휴대폰으로 각자 말씀을 뽑거나, 준비한 말씀 카드를 상자에서 뽑습니다.</li></ol>
<h2>자주 묻는 질문</h2><div class="faq">{faq_html}</div>
<p><a href="/verse/new-year/guide/">⛪ 송구영신 말씀 뽑기 진행 가이드</a> · <a href="/verse/new-year/">🎍 새해 말씀 뽑기</a> · <a href="/cards/new-year/">🖼️ 새해 말씀 카드 갤러리</a></p>
</section>
</main>"""
    data_js = "<script>window.__CV=" + json.dumps(vs, ensure_ascii=False, separators=(",", ":")) + ";</script>"
    return "\n".join([h, body, FOOTER, data_js, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- CDOWN-START -->.*?<!-- CDOWN-END -->", "", s, flags=re.S)
    block = (f"\n  <!-- CDOWN-START -->\n  <url>\n    <loc>{SITE}{PATH}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n"
             "    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n  <!-- CDOWN-END -->\n")
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    d = os.path.join(ROOT, "verse", "new-year", "countdown")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render())
    update_sitemap()
    print("송구영신 카운트다운 생성:", len(verses()), "구절")


if __name__ == "__main__":
    main()
