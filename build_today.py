# -*- coding: utf-8 -*-
"""오늘의 말씀(/today/) 생성. 실행: python3 build_today.py [--date YYYY-MM-DD]
날짜마다 구절이 고정되며(KST 기준), 일일 자동 발행 때 다시 생성해 오늘 구절을 HTML에 직접 넣는다.
페이지의 JS는 방문자 날짜로 다시 계산해(embedded schedule) 캐시된 페이지에서도 맞는 구절을 보여준다."""
import urllib.parse
import json
import os
import random
import re
import sys
from datetime import date, datetime, timedelta, timezone

import build_dictionary as bd
import build_verse as bv
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT
from verse_commentary import C as COMMENTARY
from verse_lib import verse_url, verse_slug

EPOCH = date(2026, 10, 12)
KST = timezone(timedelta(hours=9))
WEEK = "월화수목금토일"


def kst_today():
    return datetime.now(KST).date()


def order(data):
    refs = sorted(d["ref"] for d in data)
    random.Random(1012).shuffle(refs)
    return refs


def ref_for(day, refs):
    return refs[(day - EPOCH).days % len(refs)]


def ko_date(d):
    return f"{d.year}년 {d.month}월 {d.day}일({WEEK[d.weekday()]})"


def summary_of(ref):
    c = COMMENTARY.get(ref)
    if not c:
        return None
    m = c["meaning"]
    cut = m.find("다.", 0)
    first = m[: cut + 2] if cut > 0 else m
    return c["who"], first


def render(day, data):
    by_ref = {d["ref"]: d for d in data}
    refs = order(data)
    today_ref = ref_for(day, refs)
    cur = by_ref[today_ref]
    sched = {}
    for i in range(-60, 61):
        dd = day + timedelta(days=i)
        sched[dd.isoformat()] = ref_for(dd, refs)
    path = "/today/"
    title = f"오늘의 말씀 {ko_date(day)} - {today_ref} | 십자가로세로"
    desc = f"{ko_date(day)}의 말씀은 {today_ref}입니다. \"{cur['text'][:40]}…\" 오늘의 말씀 카드를 책갈피로 저장하고 나눠 보세요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "name": "오늘의 말씀", "url": SITE + path,
        "inLanguage": "ko", "dateModified": day.isoformat(), "description": desc}, ensure_ascii=False) + "</script>"
    h = head(title, desc, path, ld, f"{SITE}/images/verse/{verse_slug(today_ref)}.jpg").replace(NAV, NAV.replace(" nav-active", "")).replace('og:type" content="article"', 'og:type" content="website"')
    h = h.replace("</head>", f"<style>{bv.CSS}\n.tday{{font-size:15px;color:#6b7b8d;margin:4px 0 0}}.vwrap{{max-width:var(--w-read,820px)}}.vcard,.vactions{{max-width:560px}}.past a{{color:inherit}}</style>\n</head>", 1)
    sm = summary_of(today_ref)
    ctx = ""
    if sm:
        ctx = (f'<h2 style="text-align:left;margin-top:30px">말씀의 배경과 뜻</h2><p style="text-align:left">{esc(sm[0])}</p>'
               f'<p style="text-align:left">{esc(sm[1])}</p>')
    guide_link = ""
    if today_ref in COMMENTARY:
        guide_link = f'<a class="vbtn sub" href="{verse_url(today_ref)}" style="text-decoration:none" data-ga="today_to_guide">📖 이 말씀 해설 읽기</a>'
    past = ""
    for i in range(1, 8):
        dd = day - timedelta(days=i)
        r = ref_for(dd, refs)
        past += f'<a class="card" href="/verse/?v={esc(r)}" data-ga="today_past_click"><b>{esc(r)}</b><span>{dd.month}월 {dd.day}일({WEEK[dd.weekday()]}) · {esc(by_ref[r]["text"][:26])}…</span></a>'
    prints = "".join('<div class="pc"><div class="pt"></div><div class="pr"></div><div class="pf">십자가로세로 · crossero.com</div></div>' for _ in range(4))
    body = f"""<main class="vwrap">
<div class="crumb" style="text-align:left"><a href="/">홈</a> › 오늘의 말씀</div>
<span class="badge">매일 새로운 말씀</span>
<h1 style="margin-top:10px">오늘의 말씀</h1>
<div class="sub" id="tdate">{ko_date(day)}</div>
<div class="vcard" id="vcard"><div class="vtag" id="vtag">{esc(cur['topic'])}</div><p class="vtext" id="vtext">{esc(cur['text'])}</p><div class="vref" id="vref">{esc(today_ref)}</div><div class="vmark">십자가로세로 · crossero.com</div></div>
<div class="vactions" id="vactions">
<a class="vhero" id="vstudiolink" href="/verse/?v={urllib.parse.quote(today_ref)}" data-ga="today_to_studio">🎨 사진·글꼴로 꾸며 저장<small>사진 200여 장 · 글꼴 31종 · 카톡·인스타·배경화면·인쇄</small></a>
{guide_link}
<button class="vbtn sub" id="vsave">📑 책갈피 이미지 저장</button>
<button class="vbtn sub" id="vsavesq">🖼️ 카드 이미지 저장</button>
<button class="vbtn sub" id="vprint">🖨️ 책갈피 인쇄(4장)</button>
<button class="vbtn sub" id="vshare">🔗 링크 공유</button>
</div>
<div id="pgCtaToday"></div>
<div id="tctx">{ctx}</div>
<div style="margin-top:26px">{bv.season_banner()}</div>
<a class="cta" href="/verse/" data-ga="today_to_draw" style="margin-top:8px">🎴 다른 말씀도 뽑아 보기<small>위로·평안·용기·감사·소망 등 12가지 주제</small></a>
<h2 style="text-align:left;margin-top:34px">지난 7일의 말씀</h2>
<div class="cards past" style="text-align:left">{past}</div>
<p class="vnote">성경 본문은 성경전서 개역한글판(대한성서공회)을 사용했습니다. 개인 묵상과 소모임 나눔을 위한 용도로 제공하며, 판매용으로 이용하실 수 없습니다. 오늘의 말씀은 매일 아침 바뀝니다.</p>
<div class="vprint" aria-hidden="true">{prints}</div>
</main>"""
    data_js = ("<script>window.__VERSES=" + json.dumps({d["ref"]: d for d in data}, ensure_ascii=False, separators=(",", ":")) +
               ";window.__SCHED=" + json.dumps(sched, separators=(",", ":")) + ";window.__GUIDE=" +
               json.dumps({r: verse_url(r) for r in COMMENTARY}, ensure_ascii=False, separators=(",", ":")) + ";</script>")
    js = r"""
(function(){
  var V=window.__VERSES, S=window.__SCHED, G=window.__GUIDE, cur=null;
  var $=function(id){return document.getElementById(id)};
  var WEEK='월화수목금토일';
  function todayKST(){ try{ return new Date().toLocaleDateString('sv-SE',{timeZone:'Asia/Seoul'}); }catch(e){ return null; } }
  var q=new URLSearchParams(location.search).get('d');
  var d=q||todayKST();
  var ref=S[d];
  if(ref&&V[ref]){
    var parts=d.split('-'); var dt=new Date(Date.UTC(+parts[0],+parts[1]-1,+parts[2]));
    $('tdate').textContent=parts[0]+'년 '+(+parts[1])+'월 '+(+parts[2])+'일('+WEEK[(dt.getUTCDay()+6)%7]+')';
    var v=V[ref]; $('vtag').textContent=v.topic; $('vtext').textContent=v.text; $('vref').textContent=ref;
  }
  cur=V[$('vref').textContent]||null;
  (function(){ var l=$('vstudiolink'); if(l) l.href='/verse/?v='+encodeURIComponent($('vref').textContent); })();
  var pc=document.querySelectorAll('.vprint .pc');
  function fillPrint(){ [].forEach.call(pc,function(p){p.querySelector('.pt').textContent=cur.text;p.querySelector('.pr').textContent=cur.ref;}); }
  if(cur){ cur.ref=$('vref').textContent; fillPrint(); }
  function wrap(ctx,text,maxW){var words=text.split(' '),lines=[],line='';words.forEach(function(w){var t=line?line+' '+w:w;if(ctx.measureText(t).width>maxW&&line){lines.push(line);line=w;}else line=t;});if(line)lines.push(line);return lines;}
  function makeCanvas(w,h,fs){
    var cv=document.createElement('canvas'); cv.width=w; cv.height=h; var x=cv.getContext('2d');
    var g=x.createLinearGradient(0,0,0,h); g.addColorStop(0,'#fffdf6'); g.addColorStop(1,'#e9f2ff'); x.fillStyle=g; x.fillRect(0,0,w,h);
    x.strokeStyle='#0b5cad'; x.lineWidth=6; x.strokeRect(24,24,w-48,h-48); x.strokeStyle='#9bbbe6'; x.lineWidth=2; x.strokeRect(38,38,w-76,h-76);
    var f='"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif';
    x.textAlign='center'; x.fillStyle='#0b5cad'; x.font='bold '+Math.round(fs*0.7)+'px '+f; x.fillText('✝  오늘의 말씀  ✝',w/2,Math.round(h*0.14));
    x.fillStyle='#1f2d3d'; x.font=fs+'px '+f;
    var lines=wrap(x,cur.text,w-150), lh=Math.round(fs*1.75), total=lines.length*lh, y=Math.max(Math.round(h*0.24),Math.round((h-total)/2));
    lines.forEach(function(l,i){x.fillText(l,w/2,y+i*lh);});
    x.fillStyle='#4b5d73'; x.font='bold '+Math.round(fs*0.82)+'px '+f; x.fillText(cur.ref,w/2,y+total+Math.round(fs*1.2));
    x.fillStyle='#99a'; x.font=Math.round(fs*0.55)+'px '+f; x.fillText('십자가로세로 · crossero.com',w/2,h-70);
    return cv;
  }
  function save(cv,name){var a=document.createElement('a');a.download=name;a.href=cv.toDataURL('image/png');document.body.appendChild(a);a.click();a.remove();}
  $('vsave').addEventListener('click',function(){ if(!cur)return; save(makeCanvas(600,1400,40),'오늘의말씀-'+cur.ref.replace(/\s|:/g,'_')+'.png'); if(window.crsTrack)window.crsTrack('today_save_bookmark',{ref:cur.ref}); });
  $('vsavesq').addEventListener('click',function(){ if(!cur)return; save(makeCanvas(1080,1080,46),'오늘의말씀카드-'+cur.ref.replace(/\s|:/g,'_')+'.png'); if(window.crsTrack)window.crsTrack('today_save_card',{ref:cur.ref}); });
  $('vprint').addEventListener('click',function(){ if(!cur)return; if(window.crsTrack)window.crsTrack('today_print',{ref:cur.ref}); window.print(); });
  $('vshare').addEventListener('click',function(){
    if(!cur)return; var url=location.origin+'/today/'; if(window.crsTrack)window.crsTrack('today_share',{ref:cur.ref});
    if(navigator.share){ navigator.share({title:'오늘의 말씀 - '+cur.ref,text:cur.text,url:url}).catch(function(){}); return; }
    if(navigator.clipboard){ navigator.clipboard.writeText(url).then(function(){ $('vshare').textContent='✅ 링크 복사됨'; setTimeout(function(){$('vshare').textContent='🔗 링크 공유';},1800); }); } else { prompt('링크를 복사하세요',url); }
  });
  if(window.crsTrack&&cur) window.crsTrack('today_view',{ref:cur.ref});
})();
"""
    return "\n".join([h, body, FOOTER, data_js,
                      '<script src="/ga-events.js"></script><script src="/subscribe.js"></script><script src="/pilgrim-cta.js"></script><script>if(window.crsPilgrimCta)crsPilgrimCta({host:"pgCtaToday",campaign:"today_verse"});</script>', "<script>" + js + "</script>", "</body>\n</html>\n"])


def update_sitemap(day):
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- TODAY-START -->.*?<!-- TODAY-END -->", "", s, flags=re.S)
    block = (f"\n  <!-- TODAY-START -->\n  <url>\n    <loc>{SITE}/today/</loc>\n    <lastmod>{day.isoformat()}</lastmod>\n"
             "    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n  <!-- TODAY-END -->\n")
    s = s.replace("</urlset>", block + "</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    day = kst_today()
    if "--date" in sys.argv:
        day = date.fromisoformat(sys.argv[sys.argv.index("--date") + 1])
    data = bv.build_data()
    os.makedirs(os.path.join(ROOT, "today"), exist_ok=True)
    open(os.path.join(ROOT, "today", "index.html"), "w", encoding="utf-8").write(render(day, data))
    update_sitemap(day)
    refs = order(data)
    print(f"오늘의 말씀 생성: {day.isoformat()} -> {ref_for(day, refs)}")


if __name__ == "__main__":
    main()
