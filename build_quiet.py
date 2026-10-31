# -*- coding: utf-8 -*-
"""1분 쉼·침묵 묵상 페이지(/quiet/) 생성. 실행: python3 build_quiet.py
한 화면에 말씀 한 구절 + 호흡 안내 + 1·3분 타이머. 서버·가입 없음."""
import json
import os
import re

import build_dictionary as bd
from build_dictionary import head, FOOTER, NAV, SITE, ROOT
from verse_lib import KO_BOOKS, load_text
from verse_picks import PICKS

PATH = "/quiet/"
TITLE = "1분 쉼 · 조용한 묵상 - 말씀 한 구절과 호흡 | 십자가로세로"
DESC = "잠시 멈추어 말씀 한 구절 앞에 서 보세요. 가입도 설명도 없이 호흡 안내와 1분·3분 타이머로 조용히 쉬는 묵상 페이지입니다. 마음이 지칠 때 열어 보세요."

FAQ = [
    ("1분 쉼 묵상은 무엇인가요?", "말씀 한 구절을 보며 천천히 숨을 들이쉬고 내쉬는 짧은 묵상 시간입니다. 가입이나 입력 없이 버튼 하나로 1분 또는 3분 동안 조용히 쉴 수 있습니다."),
    ("예배를 대신하는 것인가요?", "아닙니다. 예배나 공동체 기도를 대신하지 않고, 하루 중 잠시 멈추어 말씀 앞에 서는 개인 묵상을 돕는 도구입니다."),
    ("소리가 나나요?", "기본은 소리가 없습니다. 원하면 '시작과 끝에 작은 종소리'를 켤 수 있고, 이 설정은 이 화면에서만 적용됩니다."),
    ("말씀은 어떻게 고르나요?", "위로와 평안의 말씀 가운데 하루에 한 구절이 정해져 있고, '다른 말씀'을 누르면 다른 구절로 바꿀 수 있습니다. 성경 본문은 개역한글판입니다."),
    ("화면이 꺼지지 않나요?", "지원하는 휴대폰과 브라우저에서는 쉬는 동안 화면이 꺼지지 않게 합니다. 지원하지 않는 기기에서는 화면 설정에 따라 꺼질 수 있습니다."),
]


def verses():
    text = load_text()
    out, seen = [], set()
    for topic in ("위로", "평안"):
        for name, c, v in PICKS[topic]:
            t = text[(KO_BOOKS.index(name) + 1, c, v)]
            ref = f"{name} {c}:{v}"
            if len(t) <= 80 and ref not in seen and t not in seen:
                seen.add(ref)
                seen.add(t)
                out.append({"ref": ref, "text": t})
    return out


CSS = """
.q-wrap{min-height:calc(100vh - 60px);background:linear-gradient(180deg,#1b2a41 0%,#2a3b5c 45%,#46567a 100%);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:34px 20px 40px;text-align:center;position:relative;overflow:hidden}
.q-wrap h1{font-size:15px;font-weight:600;letter-spacing:.14em;color:#c9d6ee;margin:0 0 22px}
.q-verse{max-width:560px;margin:0 auto 6px;min-height:150px;display:flex;flex-direction:column;justify-content:center}
.q-text{font-size:24px;line-height:1.85;word-break:keep-all;margin:0 0 10px;font-family:'Noto Serif KR','Nanum Myeongjo',serif}
.q-ref{font-size:15px;color:#b9c8e6}
.q-breath{width:150px;height:150px;border-radius:50%;margin:26px auto 12px;background:radial-gradient(circle at 40% 35%,#ffffffcc,#9fb6e3aa 60%,#6f87bd66);box-shadow:0 0 50px #9fb6e366;transform:scale(.62);transition:transform 4s ease-in-out}
.q-breath.in{transform:scale(1);transition:transform 4s ease-in-out}.q-breath.out{transform:scale(.62);transition:transform 6s ease-in-out}
.q-say{height:28px;font-size:17px;color:#dbe6fb;margin:0}
.q-time{font-size:34px;font-weight:300;letter-spacing:.08em;margin:6px 0 0;min-height:44px;font-variant-numeric:tabular-nums}
.q-btns{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:18px 0 6px}
.q-btn{border:1px solid #ffffff66;background:#ffffff1f;color:#fff;border-radius:30px;padding:13px 26px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit}
.q-btn.main{background:#fff;color:#1b2a41;border-color:#fff}
.q-btn.ghost{border-color:#ffffff33;font-weight:500;font-size:14.5px;padding:10px 18px}
.q-opt{font-size:14px;color:#c9d6ee;margin-top:10px}.q-opt input{margin-right:6px;transform:scale(1.2)}
.q-done{display:none}.q-done h2{font-size:22px;margin:0 0 8px;color:#fff}.q-done p{color:#dbe6fb;margin:0 0 4px}
.q-wrap.running #qStop{display:inline-block!important;margin-top:14px}
.q-wrap.running .q-menu,.q-wrap.running .q-opt,.q-wrap.running .q-other{display:none}
.q-wrap.finished .q-menu,.q-wrap.finished .q-breath,.q-wrap.finished .q-say,.q-wrap.finished .q-time,.q-wrap.finished .q-opt{display:none}.q-wrap.finished .q-done{display:block}
.q-note{max-width:560px;margin:26px auto 0;font-size:13px;color:#9fb0d2;line-height:1.7}
.peek,.pg-pill,.pg-side{display:none!important}
.q-info{max-width:780px;margin:0 auto;padding:26px 20px 10px;text-align:left;color:#222}
.q-info h2{font-size:20px;margin:26px 0 8px;color:#0b3d73}.q-info p,.q-info li{font-size:16px;line-height:1.9;word-break:keep-all}
@media(prefers-reduced-motion:reduce){.q-breath,.q-breath.in,.q-breath.out{transition:none}}
@media(max-width:560px){.q-text{font-size:21px}.q-breath{width:130px;height:130px}}
"""

JS = r"""
(function(){
  var V=window.__QV,$=function(i){return document.getElementById(i)},wrap=$('qWrap'),cur,timer=null,total=0,left=0,breathT=null,wake=null;
  function pick(){var q=new URLSearchParams(location.search).get('v');var f=V.filter(function(d){return d.ref===q})[0];if(f)return f;var d=new Date(),day=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5);return V[day%V.length];}
  function show(d){cur=d;$('qText').textContent=d.text;$('qRef').textContent=d.ref;$('qLink').href='/verse/?v='+encodeURIComponent(d.ref);}
  function track(n,p){if(window.crsTrack)window.crsTrack(n,p||{});}
  function chime(){try{if(!$('qSound').checked)return;var a=new Audio('/quiet/church_bell.m4a');a.volume=0.5;var pr=a.play();if(pr&&pr.catch)pr.catch(function(){osc();});}catch(e){osc();}}
  function osc(){try{var C=window.AudioContext||window.webkitAudioContext,a=new C(),o=a.createOscillator(),g=a.createGain();o.type='sine';o.frequency.value=528;g.gain.setValueAtTime(0.0001,a.currentTime);g.gain.exponentialRampToValueAtTime(0.18,a.currentTime+0.05);g.gain.exponentialRampToValueAtTime(0.0001,a.currentTime+2.6);o.connect(g);g.connect(a.destination);o.start();o.stop(a.currentTime+2.7);}catch(e){}}
  function breathe(){var b=$('qBreath'),s=$('qSay'),inn=true;function step(){if(inn){b.className='q-breath in';s.textContent='천천히 들이쉬고…';breathT=setTimeout(step,4000);}else{b.className='q-breath out';s.textContent='길게 내쉬며 내려놓아요…';breathT=setTimeout(step,6000);}inn=!inn;}step();}

  var W={on:false,f:0,vol:0.4,out:false,cur:null,oth:null,iv:null};
  function cl(x){return Math.max(0,Math.min(1,x));}
  function windKill(){try{clearInterval(W.iv);if(W.cur)W.cur.pause();if(W.oth)W.oth.pause();}catch(e){}W.on=false;W.cur=W.oth=null;}
  function windStart(){if(!$('qWind').checked)return;windKill();var mk=function(){var x=new Audio('/quiet/forest_wind.m4a');x.preload='auto';x.volume=0;return x;};W.cur=mk();W.oth=mk();W.f=0;W.out=false;W.on=true;
    var p=W.cur.play();if(p&&p.catch)p.catch(function(){});var q=W.oth.play();if(q&&q.then)q.then(function(){W.oth.pause();W.oth.currentTime=0;}).catch(function(){});
    W.iv=setInterval(windTick,100);track('quiet_wind');}
  function windTick(){if(!W.on)return;var c=W.cur,o=W.oth,d=c.duration||0;
    W.f=W.out?Math.max(0,W.f-0.1/1.5):Math.min(1,W.f+0.1/2);
    var left=d?d-c.currentTime:99,cv=1,ov=0;
    if(d&&left<=3){if(o.paused){o.currentTime=0;var pr=o.play();if(pr&&pr.catch)pr.catch(function(){});}ov=1-left/3;cv=left/3;}
    if(d&&left<=0.15){c.pause();c.currentTime=0;W.cur=o;W.oth=c;}
    c.volume=cl(W.vol*W.f*cv);o.volume=cl(W.vol*W.f*ov);
    if(W.out&&W.f<=0)windKill();}
  function windStop(){if(W.on)W.out=true;}
  function fmt(s){var m=Math.floor(s/60),r=s%60;return m+':'+(r<10?'0':'')+r;}
  function start(min){total=min*60;left=total;wrap.className='q-wrap running';$('qTime').textContent=fmt(left);chime();windStart();breathe();track('quiet_start',{min:min});
    try{if(navigator.wakeLock)navigator.wakeLock.request('screen').then(function(l){wake=l;}).catch(function(){});}catch(e){}
    timer=setInterval(function(){left--;$('qTime').textContent=fmt(Math.max(0,left));if(left<=0)finish(true);},1000);}
  function stop(){clearInterval(timer);windStop();clearTimeout(breathT);try{if(wake){wake.release();wake=null;}}catch(e){}$('qBreath').className='q-breath';}
  function finish(ok){stop();wrap.className=ok?'q-wrap finished':'q-wrap';if(ok){chime();track('quiet_done',{min:total/60});}else{$('qSay').textContent='';$('qTime').textContent='';track('quiet_stop');}}
  $('q1').addEventListener('click',function(){start(1)});$('q3').addEventListener('click',function(){start(3)});
  $('qStop').addEventListener('click',function(){finish(false)});$('qAgain').addEventListener('click',function(){wrap.className='q-wrap';});
  $('qOther').addEventListener('click',function(){var d;do{d=V[Math.floor(Math.random()*V.length)];}while(V.length>1&&d.ref===cur.ref);show(d);track('quiet_other');});
  $('qLink').addEventListener('click',function(){track('quiet_to_card',{ref:cur.ref});});
  $('qShare').addEventListener('click',function(){var url=location.origin+'/quiet/?v='+encodeURIComponent(cur.ref);track('quiet_share',{ref:cur.ref});
    if(navigator.share){navigator.share({title:'1분 쉼 · 조용한 묵상',text:cur.text+' - '+cur.ref,url:url}).catch(function(){});return;}
    if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){$('qShare').textContent='✅ 링크 복사됨';setTimeout(function(){$('qShare').textContent='🔗 이 쉼 나누기';},1800);});}});
  show(pick());
})();
"""


def render():
    vs = verses()
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "1분 쉼 · 조용한 묵상", "url": SITE + PATH, "applicationCategory": "LifestyleApplication",
              "inLanguage": "ko", "operatingSystem": "Web", "description": DESC, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (app_ld, faq_ld))
    h = head(TITLE, DESC, PATH, ld).replace(NAV, NAV.replace(" nav-active", "")).replace('og:type" content="article"', 'og:type" content="website"')
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    body = f"""<main>
<section class="q-wrap" id="qWrap" aria-label="1분 쉼 묵상">
<h1>1분 쉼 · 조용한 묵상</h1>
<div class="q-verse"><p class="q-text" id="qText"></p><div class="q-ref" id="qRef"></div></div>
<div class="q-breath" id="qBreath" aria-hidden="true"></div>
<p class="q-say" id="qSay" aria-live="polite"></p>
<div class="q-time" id="qTime"></div>
<div class="q-btns q-menu"><button class="q-btn main" id="q1" type="button">🌿 1분 쉬기</button><button class="q-btn" id="q3" type="button">3분 쉬기</button></div>
<div class="q-btns q-other"><button class="q-btn ghost" id="qOther" type="button">다른 말씀</button></div>
<label class="q-opt"><input type="checkbox" id="qSound">시작과 끝에 작은 종소리</label>
<label class="q-opt"><input type="checkbox" id="qWind">쉬는 동안 잔잔한 숲 바람 소리</label>
<button class="q-btn ghost" id="qStop" type="button" style="display:none">그만하기</button>
<div class="q-done" id="qDone"><h2>잠시 쉬었어요 🌿</h2><p>수고했어요. 이 말씀을 오늘 하루 마음에 두어 보세요.</p>
<div class="q-btns"><a class="q-btn main" id="qLink" href="/verse/" style="text-decoration:none" data-ga="quiet_card_link">🎨 이 말씀으로 카드 만들기</a><button class="q-btn" id="qShare" type="button">🔗 이 쉼 나누기</button><button class="q-btn ghost" id="qAgain" type="button">다시 쉬기</button></div></div>
<p class="q-note">예배나 공동체 기도를 대신하지 않고, 하루 중 잠시 멈추어 말씀 앞에 서는 개인 묵상을 돕습니다. 성경 본문은 개역한글판(대한성서공회)입니다.</p>
</section>
<section class="q-info">
<h2>이렇게 쉬어 보세요</h2>
<ol><li>말씀을 한 번 천천히 읽습니다.</li><li>'1분 쉬기'를 누르고, 동그라미가 커질 때 들이쉬고 작아질 때 길게 내쉽니다.</li><li>끝나면 오늘 마음에 남는 단어 하나만 기억해 두세요.</li></ol>
<h2>자주 묻는 질문</h2><div class="faq">{faq_html}</div>
<p><a href="/today/">📅 오늘의 말씀 보기</a> · <a href="/verse/">📖 말씀 뽑기</a> · <a href="/guide/how-to-do-qt-bible-meditation/">QT·성경 묵상하는 법</a></p>
</section>
</main>"""
    data_js = "<script>window.__QV=" + json.dumps(vs, ensure_ascii=False, separators=(",", ":")) + ";</script>"
    return "\n".join([h, body, FOOTER, data_js, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- QUIET-START -->.*?<!-- QUIET-END -->", "", s, flags=re.S)
    block = (f"\n  <!-- QUIET-START -->\n  <url>\n    <loc>{SITE}{PATH}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n"
             "    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n  <!-- QUIET-END -->\n")
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    d = os.path.join(ROOT, "quiet")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render())
    update_sitemap()
    print("쉼 묵상 페이지 생성:", len(verses()), "구절")


if __name__ == "__main__":
    main()
