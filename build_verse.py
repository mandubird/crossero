# -*- coding: utf-8 -*-
"""말씀 뽑기 페이지 생성. 실행: python3 build_verse.py
BIBLE.csv(성경전서 개역한글판)에서 주제별로 고른 구절만 뽑아 verse/index.html 에 내장한다."""
import csv
import json
import os
import re

import build_dictionary as bd
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT
from bible_book_info import BOOK_INFO

BOOKS = list(BOOK_INFO)
from verse_picks import PICKS


def load_text():
    rows = csv.reader(open(os.path.join(ROOT, "BIBLE.csv"), encoding="utf-8"))
    next(rows)
    verses = {}
    for b, c, v, t in rows:
        try:
            bi, ci, vi = int(float(b)), int(float(c)), int(float(v))
        except ValueError:
            continue
        if bi >= 1 and len(t) > 3:
            verses[(bi, ci, vi)] = t.strip()
    return verses


def build_data():
    text = load_text()
    out, seen_ref, seen_txt = [], set(), set()
    for topic, items in PICKS.items():
        for name, c, v in items:
            ref = f"{name} {c}:{v}"
            t = text[(BOOKS.index(name) + 1, c, v)]
            if re.match(r"^\(.*절에.*\)$", t):
                raise SystemExit(f"합쳐진 구절 표시 본문: {ref} -> {t}")
            if ref in seen_ref or t in seen_txt:
                continue
            seen_ref.add(ref)
            seen_txt.add(t)
            out.append({"topic": topic, "ref": ref, "text": t})
    return out


CSS = """
.vwrap{max-width:720px;margin:0 auto;padding:28px 20px 12px;text-align:center}
.vchips{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:18px 0 22px}
.vchip{padding:8px 16px;border:1px solid #bcd3f0;background:#fff;color:#0b5cad;border-radius:22px;font-size:15px;cursor:pointer;font-family:inherit}
.vchip.on{background:#0073e6;color:#fff;border-color:#0073e6}
.vbox{width:200px;height:130px;margin:0 auto 16px;background:linear-gradient(135deg,#0b5cad,#0073e6);border-radius:16px;color:#fff;display:flex;align-items:center;justify-content:center;font-size:44px;box-shadow:0 8px 22px rgba(0,115,230,.28);cursor:pointer;transition:transform .2s}
.vbox:hover{transform:translateY(-3px)}
.vbtn{display:inline-block;padding:14px 34px;background:#0073e6;color:#fff;border:0;border-radius:12px;font-weight:700;font-size:17px;cursor:pointer;font-family:inherit}
.vbtn.sub{background:#fff;color:#0b5cad;border:1px solid #bcd3f0;font-weight:600;font-size:14px;padding:10px 16px;margin:4px}
.vcard{max-width:460px;margin:26px auto 8px;padding:34px 28px 26px;background:linear-gradient(180deg,#fffdf6,#f1f7ff);border:1px solid #d6e4f7;border-radius:18px;box-shadow:0 10px 28px rgba(11,92,173,.12);text-align:center;animation:vpop .55s ease both}
@keyframes vpop{from{opacity:0;transform:translateY(24px) scale(.96)}to{opacity:1;transform:none}}
.vtag{display:inline-block;background:#e8f1ff;color:#0b5cad;font-size:12px;font-weight:700;padding:3px 12px;border-radius:20px;margin-bottom:16px}
.vtext{font-size:20px;line-height:1.9;color:#1f2d3d;word-break:keep-all;margin:0 0 16px}
.vref{font-size:15px;color:#6b7b8d;font-weight:600}
.vmark{margin-top:18px;font-size:12px;color:#99a}
.vactions{margin:14px 0 6px}
.vnote{font-size:12.5px;color:#889;line-height:1.7;max-width:560px;margin:22px auto 4px}
.vprint{display:none}
@media print{
  body *{visibility:hidden}
  .vprint,.vprint *{visibility:visible}
  .vprint{display:grid;grid-template-columns:1fr 1fr;gap:10mm;position:absolute;left:0;top:0;width:100%;padding:10mm;box-sizing:border-box}
  .vprint .pc{border:1px dashed #888;border-radius:6mm;padding:10mm 7mm;text-align:center;height:120mm;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center}
  .vprint .pt{font-size:13pt;line-height:1.9;margin-bottom:6mm;word-break:keep-all}
  .vprint .pr{font-size:10.5pt;color:#555}
  .vprint .pf{margin-top:6mm;font-size:8pt;color:#999}
}
"""

JS = r"""
(function(){
  var D=window.__VERSES, topic='전체', last=null, cur=null;
  var $=function(id){return document.getElementById(id)};
  function pool(){return D.filter(function(d){return topic==='전체'||d.topic===topic;});}
  function show(d,fromDraw){
    cur=d;
    var c=$('vcard');
    c.style.display='block'; c.style.animation='none'; void c.offsetWidth; c.style.animation='';
    $('vtag').textContent=d.topic; $('vtext').textContent=d.text; $('vref').textContent=d.ref;
    $('vactions').style.display='block'; $('vbox').style.display='none';
    $('vdraw').textContent='🎴 다시 뽑기';
    var pc=document.querySelectorAll('.vprint .pc');
    [].forEach.call(pc,function(p){p.querySelector('.pt').textContent=d.text;p.querySelector('.pr').textContent=d.ref;});
    if(fromDraw&&window.crsTrack) window.crsTrack('verse_draw',{topic:d.topic,ref:d.ref});
  }
  function draw(){
    var p=pool(); if(!p.length) return;
    var d; var tries=0;
    do{ d=p[Math.floor(Math.random()*p.length)]; tries++; }while(p.length>1&&last&&d.ref===last.ref&&tries<10);
    last=d; show(d,true);
  }
  $('vdraw').addEventListener('click',draw);
  $('vbox').addEventListener('click',draw);
  $('vchips').addEventListener('click',function(e){
    if(!e.target.classList.contains('vchip'))return;
    [].forEach.call(document.querySelectorAll('.vchip'),function(c){c.classList.remove('on');});
    e.target.classList.add('on'); topic=e.target.getAttribute('data-t');
    if(window.crsTrack) window.crsTrack('verse_topic',{topic:topic});
  });
  function wrap(ctx,text,maxW){
    var words=text.split(' '),lines=[],line='';
    words.forEach(function(w){
      var t=line?line+' '+w:w;
      if(ctx.measureText(t).width>maxW&&line){lines.push(line);line=w;}else line=t;
    });
    if(line)lines.push(line);
    return lines;
  }
  function makeCanvas(w,h,fs){
    var cv=document.createElement('canvas'); cv.width=w; cv.height=h; var x=cv.getContext('2d');
    var g=x.createLinearGradient(0,0,0,h); g.addColorStop(0,'#fffdf6'); g.addColorStop(1,'#e9f2ff');
    x.fillStyle=g; x.fillRect(0,0,w,h);
    x.strokeStyle='#0b5cad'; x.lineWidth=6; x.strokeRect(24,24,w-48,h-48);
    x.strokeStyle='#9bbbe6'; x.lineWidth=2; x.strokeRect(38,38,w-76,h-76);
    var f='"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif';
    x.textAlign='center'; x.fillStyle='#0b5cad'; x.font='bold '+Math.round(fs*0.7)+'px '+f;
    x.fillText('✝  '+cur.topic+'  ✝',w/2,Math.round(h*0.14));
    x.fillStyle='#1f2d3d'; x.font=fs+'px '+f;
    var lines=wrap(x,cur.text,w-150), lh=Math.round(fs*1.75);
    var total=lines.length*lh, y=Math.max(Math.round(h*0.24),Math.round((h-total)/2));
    lines.forEach(function(l,i){x.fillText(l,w/2,y+i*lh);});
    x.fillStyle='#4b5d73'; x.font='bold '+Math.round(fs*0.82)+'px '+f;
    x.fillText(cur.ref,w/2,y+total+Math.round(fs*1.2));
    x.fillStyle='#99a'; x.font=Math.round(fs*0.55)+'px '+f;
    x.fillText('십자가로세로 · crossero.com',w/2,h-70);
    return cv;
  }
  function save(cv,name){
    var a=document.createElement('a'); a.download=name; a.href=cv.toDataURL('image/png'); document.body.appendChild(a); a.click(); a.remove();
  }
  $('vsave').addEventListener('click',function(){
    if(!cur)return; save(makeCanvas(600,1400,40),'말씀책갈피-'+cur.ref.replace(/\s|:/g,'_')+'.png');
    if(window.crsTrack) window.crsTrack('verse_save_bookmark',{topic:cur.topic,ref:cur.ref});
  });
  $('vsavesq').addEventListener('click',function(){
    if(!cur)return; save(makeCanvas(1080,1080,46),'말씀카드-'+cur.ref.replace(/\s|:/g,'_')+'.png');
    if(window.crsTrack) window.crsTrack('verse_save_card',{topic:cur.topic,ref:cur.ref});
  });
  $('vprint').addEventListener('click',function(){
    if(!cur)return; if(window.crsTrack) window.crsTrack('verse_print',{topic:cur.topic,ref:cur.ref}); window.print();
  });
  $('vshare').addEventListener('click',function(){
    if(!cur)return;
    var url=location.origin+'/verse/?v='+encodeURIComponent(cur.ref);
    if(window.crsTrack) window.crsTrack('verse_share',{topic:cur.topic,ref:cur.ref});
    if(navigator.share){ navigator.share({title:'오늘의 말씀 - '+cur.ref,text:cur.text,url:url}).catch(function(){}); return; }
    if(navigator.clipboard){ navigator.clipboard.writeText(url).then(function(){ $('vshare').textContent='✅ 링크 복사됨'; setTimeout(function(){$('vshare').textContent='🔗 링크 공유';},1800); }); }
    else { prompt('링크를 복사하세요',url); }
  });
  var q=new URLSearchParams(location.search).get('v');
  if(q){ var f=D.filter(function(d){return d.ref===q;})[0]; if(f){ last=f; show(f,false); } }
})();
"""


def render(data):
    path = "/verse/"
    title = "말씀 뽑기 - 오늘의 말씀 카드와 책갈피 | 십자가로세로"
    desc = "버튼을 눌러 위로, 평안, 용기, 감사, 소망의 말씀을 뽑아 보세요. 마음에 드는 구절은 책갈피 이미지로 저장하거나 인쇄하고, 친구와 공유할 수 있어요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication", "name": "말씀 뽑기", "url": SITE + path,
        "applicationCategory": "LifestyleApplication", "inLanguage": "ko", "operatingSystem": "Web",
        "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}, ensure_ascii=False) + "</script>"
    plain_nav = NAV.replace(' nav-active', '')
    h = head(title, desc, path, ld).replace(NAV, plain_nav).replace('og:type" content="article"', 'og:type" content="website"')
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    chips = '<button class="vchip on" data-t="전체">전체</button>' + "".join(
        f'<button class="vchip" data-t="{t}">{t}</button>' for t in PICKS)
    prints = "".join('<div class="pc"><div class="pt"></div><div class="pr"></div><div class="pf">십자가로세로 · crossero.com</div></div>' for _ in range(4))
    body = f"""<main class="vwrap">
<div class="crumb" style="text-align:left"><a href="/">홈</a> › 말씀 뽑기</div>
<span class="badge">무료 · 회원가입 없음</span>
<h1 style="margin-top:10px">말씀 뽑기</h1>
<div class="sub">오늘 마음에 필요한 말씀을 한 장 뽑아 보세요</div>
<div class="vchips" id="vchips">{chips}</div>
<div class="vbox" id="vbox" title="눌러서 뽑기">🎴</div>
<button class="vbtn" id="vdraw" data-ga="verse_draw_click">🎴 말씀 뽑기</button>
<div class="vcard" id="vcard" style="display:none"><div class="vtag" id="vtag"></div><p class="vtext" id="vtext"></p><div class="vref" id="vref"></div><div class="vmark">십자가로세로 · crossero.com</div></div>
<div class="vactions" id="vactions" style="display:none">
<button class="vbtn sub" id="vsave">📑 책갈피 이미지 저장</button>
<button class="vbtn sub" id="vsavesq">🖼️ 카드 이미지 저장</button>
<button class="vbtn sub" id="vprint">🖨️ 책갈피 인쇄(4장)</button>
<button class="vbtn sub" id="vshare">🔗 링크 공유</button>
</div>
<p class="vnote">성경 본문은 성경전서 개역한글판(대한성서공회)을 사용했습니다. 개인 묵상과 소모임 나눔을 위한 용도로 제공하며, 판매용으로 이용하실 수 없습니다. 구절은 주제별로 직접 골랐고, 앞으로 계속 늘려 갑니다. 말씀을 더 깊이 읽고 싶다면 <a href="/dictionary/">성경사전</a>에서 해당 책의 요약을 확인해 보세요.</p>
<div class="vprint" aria-hidden="true">{prints}</div>
</main>"""
    data_js = "<script>window.__VERSES=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";</script>"
    return "\n".join([h, body, FOOTER, data_js,
                      '<script src="/ga-events.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- VERSE-START -->.*?<!-- VERSE-END -->", "", s, flags=re.S)
    block = (f"\n  <!-- VERSE-START -->\n  <url>\n    <loc>{SITE}/verse/</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n"
             "    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n  <!-- VERSE-END -->\n")
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    data = build_data()
    os.makedirs(os.path.join(ROOT, "verse"), exist_ok=True)
    open(os.path.join(ROOT, "verse", "index.html"), "w", encoding="utf-8").write(render(data))
    update_sitemap()
    print(f"말씀 뽑기 생성: 구절 {len(data)}개")


if __name__ == "__main__":
    main()
