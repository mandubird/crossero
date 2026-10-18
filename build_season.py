# -*- coding: utf-8 -*-
"""절기 말씀 뽑기 페이지 생성(새해·성탄·추수감사). 실행: python3 build_season.py
출력: verse/<절기>/index.html, sitemap.xml 의 SEASON 구간"""
import json
import os
import re

import build_dictionary as bd
import build_verse as bv
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT
from season_picks import SEASONS
from verse_lib import KO_BOOKS, load_text, verse_slug

CSS = bv.CSS + """
.sgrid{display:grid;grid-template-columns:1fr;gap:8px;text-align:left;margin:10px 0 0}
.sgrid .it{background:#fff;border:1px solid #e5e5e5;border-radius:10px;padding:10px 14px;font-size:15px;line-height:1.7}
.sgrid .it b{color:#0b5cad;font-size:13.5px;margin-right:6px}
.steps{text-align:left;padding-left:22px}.steps li{margin:8px 0;font-size:16px;line-height:1.8}
.vprintall{display:none}
@media print{
  .vprintall,.vprintall *{visibility:visible}
  body:not(.printall) .vprintall{display:none!important}
  body.printall .vprint{display:none!important}
  body.printall .vprintall{display:grid;grid-template-columns:1fr 1fr;gap:6mm;position:absolute;left:0;top:0;width:100%;padding:8mm;box-sizing:border-box}
  .vprintall .pc{border:1px dashed #888;border-radius:4mm;padding:6mm 5mm;text-align:center;height:62mm;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;page-break-inside:avoid}
  .vprintall .pt{font-size:11pt;line-height:1.7;margin-bottom:3mm;word-break:keep-all}
  .vprintall .pr{font-size:9.5pt;color:#555}
  .vprintall .pf{margin-top:3mm;font-size:7pt;color:#999}
}
"""

JS = r"""
(function(){
  var D=window.__POOL, last=null, cur=null;
  var $=function(id){return document.getElementById(id)};
  function show(d,fromDraw){
    cur=d; var c=$('vcard'); c.style.display='block'; c.style.animation='none'; void c.offsetWidth; c.style.animation='';
    $('vtag').textContent=d.topic; $('vtext').textContent=d.text; $('vref').textContent=d.ref;
    var sl=$('vstudiolink'); if(sl) sl.href='/verse/?v='+encodeURIComponent(d.ref);
    $('vactions').style.display='block'; $('vbox').style.display='none'; $('vdraw').textContent='🎴 다시 뽑기';
    [].forEach.call(document.querySelectorAll('.vprint .pc'),function(p){p.querySelector('.pt').textContent=d.text;p.querySelector('.pr').textContent=d.ref;});
    if(fromDraw&&window.crsTrack) window.crsTrack('season_draw',{season:window.__SEASON,ref:d.ref});
  }

  var busy=false;
  function ritual(done){
    if(busy) return; busy=true;
    var ov=document.createElement('div');
    ov.setAttribute('role','dialog'); ov.setAttribute('aria-live','polite');
    ov.style.cssText='position:fixed;inset:0;z-index:9999;background:rgba(10,30,60,.72);display:flex;align-items:center;justify-content:center;padding:24px;opacity:0;transition:opacity .35s';
    ov.innerHTML='<div style="background:#fff;border-radius:20px;padding:34px 28px;max-width:360px;width:100%;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.35)">'
      +'<div style="font-size:44px;margin-bottom:10px">🙏</div>'
      +'<p style="font-size:19px;font-weight:700;color:#0b2a4a;line-height:1.55;margin:0 0 6px">내게 주시는 말씀을<br>기도하며 기다려볼까요?</p>'
      +'<p style="font-size:13px;color:#7b8794;margin:0 0 14px">잠시 마음을 고요히 하고 숨을 고릅니다</p>'
      +'<div id="vdots" style="font-size:26px;letter-spacing:6px;color:#0073e6;height:30px">·</div></div>';
    document.body.appendChild(ov);
    requestAnimationFrame(function(){ov.style.opacity='1';});
    var n=0, dots=ov.querySelector('#vdots');
    var iv=setInterval(function(){n=(n+1)%4; dots.textContent=new Array(n+2).join('·');},450);
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    setTimeout(function(){
      clearInterval(iv); ov.style.opacity='0';
      setTimeout(function(){ if(ov.parentNode) ov.parentNode.removeChild(ov); busy=false; done(); },300);
    }, reduce?1200:3200);
  }
  function draw(){ ritual(drawNow); }
  function drawNow(){
    var d,t=0; do{ d=D[Math.floor(Math.random()*D.length)]; t++; }while(D.length>1&&last&&d.ref===last.ref&&t<10);
    last=d; show(d,true);
  }
  $('vdraw').addEventListener('click',draw); $('vbox').addEventListener('click',draw);
  function wrap(ctx,text,maxW){var words=text.split(' '),lines=[],line='';words.forEach(function(w){var t=line?line+' '+w:w;if(ctx.measureText(t).width>maxW&&line){lines.push(line);line=w;}else line=t;});if(line)lines.push(line);return lines;}
  function makeCanvas(w,h,fs){
    var cv=document.createElement('canvas'); cv.width=w; cv.height=h; var x=cv.getContext('2d');
    var g=x.createLinearGradient(0,0,0,h); g.addColorStop(0,'#fffdf6'); g.addColorStop(1,'#e9f2ff'); x.fillStyle=g; x.fillRect(0,0,w,h);
    x.strokeStyle='#0b5cad'; x.lineWidth=6; x.strokeRect(24,24,w-48,h-48); x.strokeStyle='#9bbbe6'; x.lineWidth=2; x.strokeRect(38,38,w-76,h-76);
    var f='"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif';
    x.textAlign='center'; x.fillStyle='#0b5cad'; x.font='bold '+Math.round(fs*0.7)+'px '+f; x.fillText(window.__LABEL,w/2,Math.round(h*0.14));
    x.fillStyle='#1f2d3d'; x.font=fs+'px '+f;
    var lines=wrap(x,cur.text,w-150), lh=Math.round(fs*1.75), total=lines.length*lh, y=Math.max(Math.round(h*0.24),Math.round((h-total)/2));
    lines.forEach(function(l,i){x.fillText(l,w/2,y+i*lh);});
    x.fillStyle='#4b5d73'; x.font='bold '+Math.round(fs*0.82)+'px '+f; x.fillText(cur.ref,w/2,y+total+Math.round(fs*1.2));
    x.fillStyle='#99a'; x.font=Math.round(fs*0.55)+'px '+f; x.fillText('십자가로세로 · crossero.com',w/2,h-70);
    return cv;
  }
  function save(cv,name){var a=document.createElement('a');a.download=name;a.href=cv.toDataURL('image/png');document.body.appendChild(a);a.click();a.remove();}
  $('vsave').addEventListener('click',function(){ if(!cur)return; save(makeCanvas(600,1400,40),window.__SEASON+'-책갈피-'+cur.ref.replace(/\s|:/g,'_')+'.png'); if(window.crsTrack)window.crsTrack('season_save_bookmark',{season:window.__SEASON,ref:cur.ref}); });
  $('vsavesq').addEventListener('click',function(){ if(!cur)return; save(makeCanvas(1080,1080,46),window.__SEASON+'-카드-'+cur.ref.replace(/\s|:/g,'_')+'.png'); if(window.crsTrack)window.crsTrack('season_save_card',{season:window.__SEASON,ref:cur.ref}); });
  $('vprint').addEventListener('click',function(){ if(!cur)return; if(window.crsTrack)window.crsTrack('season_print',{season:window.__SEASON,ref:cur.ref}); window.print(); });
  $('vshare').addEventListener('click',function(){
    var url=location.origin+location.pathname; if(window.crsTrack)window.crsTrack('season_share',{season:window.__SEASON});
    var t=window.__LABEL+' - 십자가로세로';
    if(navigator.share){ navigator.share({title:t,text:cur?cur.text:t,url:url}).catch(function(){}); return; }
    if(navigator.clipboard){ navigator.clipboard.writeText(url).then(function(){ $('vshare').textContent='✅ 링크 복사됨'; setTimeout(function(){$('vshare').textContent='🔗 링크 공유';},1800); }); } else { prompt('링크를 복사하세요',url); }
  });
  var allBtn=$('vprintall');
  if(allBtn){
    var grid=$('vprintall');
    allBtn.addEventListener('click',function(){
      var box=document.querySelector('.vprintall'); box.innerHTML='';
      D.forEach(function(d){ var c=document.createElement('div'); c.className='pc';
        c.innerHTML='<div class="pt"></div><div class="pr"></div><div class="pf">'+window.__LABEL+' · 십자가로세로</div>';
        c.querySelector('.pt').textContent=d.text; c.querySelector('.pr').textContent=d.ref; box.appendChild(c); });
      document.body.classList.add('printall');
      if(window.crsTrack)window.crsTrack('season_print_all',{season:window.__SEASON,count:D.length});
      window.print();
    });
    window.addEventListener('afterprint',function(){ document.body.classList.remove('printall'); });
  }
})();
"""


def render(key, cfg, text):
    pool = []
    seen = set()
    for name, c, v in cfg["picks"]:
        t = text[(KO_BOOKS.index(name) + 1, c, v)]
        if t in seen:
            continue
        seen.add(t)
        pool.append({"topic": cfg["topic"], "ref": f"{name} {c}:{v}", "text": t})
    path = f"/verse/{key}/"
    first = pool[0]["ref"]
    img = f"{SITE}/images/verse/season/{key}-{verse_slug(first)}.jpg"
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in cfg["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": cfg["label"], "url": SITE + path,
              "applicationCategory": "LifestyleApplication", "inLanguage": "ko", "operatingSystem": "Web",
              "description": cfg["desc"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "말씀 뽑기", "item": SITE + "/verse/"},
        {"@type": "ListItem", "position": 3, "name": cfg["label"], "item": SITE + path}]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (app_ld, faq_ld, crumb_ld))
    h = head(cfg["title"], cfg["desc"], path, ld, img).replace(NAV, NAV.replace(" nav-active", "")).replace(
        'og:type" content="article"', 'og:type" content="website"')
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    others = [(k, c) for k, c in SEASONS.items() if k != key]
    prints = "".join('<div class="pc"><div class="pt"></div><div class="pr"></div><div class="pf">' + esc(cfg["label"]) + ' · 십자가로세로</div></div>' for _ in range(4))
    verses = "".join(f'<div class="it"><b>{esc(d["ref"])}</b>{esc(d["text"])}</div>' for d in pool)
    body = f"""<main class="vwrap">
<div class="crumb" style="text-align:left"><a href="/">홈</a> › <a href="/verse/">말씀 뽑기</a> › {esc(cfg['label'])}</div>
<span class="badge">절기 말씀</span>
<h1 style="margin-top:10px">{esc(cfg['h1'])}</h1>
<div class="sub">{esc(cfg['sub'])}</div>
<div class="vbox" id="vbox" title="눌러서 뽑기">{cfg['emoji']}</div>
<button class="vbtn" id="vdraw" data-ga="season_draw_click">🎴 말씀 뽑기</button>
<div class="vcard" id="vcard" style="display:none"><div class="vtag" id="vtag"></div><p class="vtext" id="vtext"></p><div class="vref" id="vref"></div><div class="vmark">{esc(cfg['label'])} · 십자가로세로</div></div>
<div class="vactions" id="vactions" style="display:none">
<a class="vhero" id="vstudiolink" href="/verse/" data-ga="season_to_studio">🎨 사진·글꼴로 꾸며 저장<small>사진 200여 장 · 글꼴 31종 · 카톡·인스타·배경화면·인쇄</small></a>
<button class="vbtn sub" id="vsave">📑 책갈피 이미지 저장</button>
<button class="vbtn sub" id="vsavesq">🖼️ 카드 이미지 저장</button>
<button class="vbtn sub" id="vprint">🖨️ 책갈피 인쇄(4장)</button>
<button class="vbtn sub" id="vshare">🔗 링크 공유</button>
</div>
<div style="text-align:left;margin-top:34px">{''.join(f'<p style="font-size:16px;line-height:1.9;margin:0 0 14px">{esc(p)}</p>' for p in cfg['intro'])}</div>
<h2 style="text-align:left;margin-top:30px">이렇게 해 보세요</h2>
<ol class="steps">{''.join(f'<li>{esc(s)}</li>' for s in cfg['how'])}</ol>
{'<a href="/verse/new-year/guide/" data-ga="season_to_nyguide" style="display:block;text-align:left;margin-top:26px;padding:14px 18px;background:#f4f8ff;border:1px solid #cfe0f5;border-radius:14px;text-decoration:none;color:#0b3d73"><b>⛪ 송구영신예배 말씀 뽑기 진행 가이드</b><br><span style="font-size:14px;color:#556">준비물, 인원별 카드 수, 30분 시간표, 유의할 점을 정리했어요 →</span></a>' if key == 'new-year' else ''}
<h2 style="text-align:left;margin-top:30px">교회·모임용 전체 카드 인쇄</h2>
<p style="text-align:left;font-size:15.5px">이 페이지의 말씀 {len(pool)}장을 A4 용지에 한 번에 인쇄해 잘라서 쓸 수 있습니다. 예배 후 한 장씩 뽑는 말씀 상자, 주일학교 활동, 소그룹 나눔에 활용해 보세요.</p>
<button class="vbtn sub" id="vprintall" data-ga="season_print_all_click">🖨️ 말씀 카드 {len(pool)}장 전체 인쇄</button>
<a class="vbtn sub" href="/verse/#church-print" data-ga="season_to_batch" style="text-decoration:none">🎨 사진·글꼴 골라 예쁘게 인쇄 (A4 4~12장씩)</a>
<h2 style="text-align:left;margin-top:30px">자주 묻는 질문</h2>
<div class="faq" style="text-align:left">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in cfg['faq'])}</div>
<h2 style="text-align:left;margin-top:30px">{esc(cfg['topic'])} 말씀 모음 ({len(pool)}구절)</h2>
<div class="sgrid">{verses}</div>
<h2 style="text-align:left;margin-top:30px">다른 절기 말씀 뽑기</h2>
<div class="cards" style="text-align:left">{''.join(f'<a class="card" href="/verse/{k}/"><b>{c["emoji"]} {esc(c["label"])}</b><span>{esc(c["sub"])}</span></a>' for k, c in others)}
<a class="card" href="/verse/"><b>🎴 주제별 말씀 뽑기</b><span>위로·평안·용기·감사·소망 등 12가지 주제</span></a>
<a class="card" href="/today/"><b>📅 오늘의 말씀</b><span>매일 아침 바뀌는 말씀 한 장</span></a>
{'<a class="card" href="/christmas/"><b>🎭 성탄절 성극 대본</b><span>어린이 성극·낭독극 10편과 준비 가이드</span></a>' if cfg['topic'] == '성탄' else ''}</div>
<p class="vnote">성경 본문은 성경전서 개역한글판(대한성서공회)을 사용했습니다. 개인 묵상과 소모임 나눔을 위한 용도로 제공하며, 판매용으로 이용하실 수 없습니다.</p>
<div class="vprint" aria-hidden="true">{prints}</div>
<div class="vprintall" aria-hidden="true"></div>
</main>"""
    data_js = ("<script>window.__POOL=" + json.dumps(pool, ensure_ascii=False, separators=(",", ":")) +
               f";window.__SEASON={json.dumps(key)};window.__LABEL={json.dumps(cfg['label'], ensure_ascii=False)};</script>")
    return "\n".join([h, body, FOOTER, data_js,
                      '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def update_sitemap(keys):
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- SEASON-START -->.*?<!-- SEASON-END -->", "", s, flags=re.S)
    block = "\n  <!-- SEASON-START -->\n" + "\n".join(
        f"  <url>\n    <loc>{SITE}/verse/{k}/</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        for k in keys) + "\n  <!-- SEASON-END -->\n"
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    text = load_text()
    for key, cfg in SEASONS.items():
        d = os.path.join(ROOT, "verse", key)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render(key, cfg, text))
    update_sitemap(list(SEASONS))
    print(f"절기 말씀 뽑기 페이지 {len(SEASONS)}개 생성")


if __name__ == "__main__":
    main()
