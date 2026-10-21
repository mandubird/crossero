# -*- coding: utf-8 -*-
"""말씀 뽑기 페이지 생성. 실행: python3 build_verse.py
BIBLE.csv(성경전서 개역한글판)에서 주제별로 고른 구절만 뽑아 verse/index.html 에 내장한다."""
import csv
import html
import json
import os
import random
import re

import build_dictionary as bd
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT
from bible_book_info import BOOK_INFO
from verse_commentary import C as COMMENTARY
from verse_lib import verse_url

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


def season_banner():
    """절기 말씀 뽑기 배너(말씀 뽑기·오늘의 말씀 페이지에서 공용)."""
    from season_picks import SEASONS as _S
    badge = {"new-year": "송구영신 · 교회 인쇄", "christmas": "성극 · 주일학교", "thanksgiving": "추수감사절"}
    grad = {"new-year": "linear-gradient(135deg,#0b5cad,#0073e6)", "christmas": "linear-gradient(135deg,#8f1d1d,#c0392b)",
            "thanksgiving": "linear-gradient(135deg,#a8530a,#d98a1c)"}
    cards = "".join(
        f'<a class="vsb-c" style="--g:{grad.get(k, "#0b5cad")}" href="/verse/{k}/" data-ga="verse_to_season" data-ga-label="{k}">'
        + ('<em>송구영신 인기</em>' if k == "new-year" else '')
        + f'<i>{c["emoji"]}</i><b>{esc(c["label"].replace(" 뽑기", ""))}</b><span>{esc(badge.get(k, c["sub"]))}</span></a>'
        for k, c in _S.items())
    return '<div class="vsb"><div class="vsb-h">🎄 절기 말씀 뽑기 <span>교회 행사에 바로 쓰세요</span></div><div class="vsb-row">' + cards + '</div></div>'


def build_sets(data):
    """교회 행사용 묶음 인쇄에 쓰는 구절 묶음(절기 + 주제 + 전체)."""
    from season_picks import SEASONS
    text = load_text()
    sets = []
    for key in ("new-year", "christmas", "thanksgiving"):
        cfg = SEASONS.get(key)
        if not cfg:
            continue
        items, seen = [], set()
        for name, c, v in cfg["picks"]:
            ref = f"{name} {c}:{v}"
            if ref in seen:
                continue
            seen.add(ref)
            items.append({"ref": ref, "text": text[(BOOKS.index(name) + 1, c, v)]})
        sets.append({"k": key, "n": cfg["label"], "v": items})
    for t in PICKS:
        sets.append({"k": "t-" + t, "n": t + " 말씀", "v": [{"ref": d["ref"], "text": d["text"]} for d in data if d["topic"] == t]})
    sets.append({"k": "all", "n": "전체 말씀", "v": [{"ref": d["ref"], "text": d["text"]} for d in data]})
    return sets


CSS = """
.vwrap{max-width:var(--w-wide,1100px);margin:0 auto;padding:28px 20px 12px;text-align:center}
.vchips{max-width:720px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:18px auto 22px}
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
.vwrap>.crumb{max-width:var(--w-col,780px);margin:0 auto 6px;text-align:left}
.vactions{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:460px;margin:14px auto 6px}
.vactions .vbtn.sub{flex:1 1 calc(50% - 8px);margin:0;text-align:center;box-sizing:border-box;text-decoration:none}
.vactions .vhero{flex:1 1 100%;display:block;box-sizing:border-box;padding:16px 18px;border-radius:16px;background:linear-gradient(135deg,#0b5cad,#0073e6);color:#fff;text-decoration:none;font-weight:800;font-size:18px;line-height:1.4;box-shadow:0 8px 20px rgba(0,115,230,.28);text-align:center}
.vactions .vhero small{display:block;font-weight:500;font-size:12.5px;opacity:.92;margin-top:3px}
.vnote{font-size:12.5px;color:#889;line-height:1.7;max-width:560px;margin:22px auto 4px}
.vprint{display:none}
.vs{text-align:left;margin:30px auto 10px;padding:18px 16px;background:#fff;border:1px solid #e5e7eb;border-radius:18px;box-shadow:0 6px 22px rgba(0,0,0,.05)}
.vs h2{margin:0 0 4px;font-size:21px}.vs .vs-sub{margin:0 0 14px;color:#667;font-size:14px;line-height:1.6}
.vs-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:18px}
@media(min-width:900px){.vs{max-width:1060px}.vs-grid{grid-template-columns:minmax(0,420px) minmax(0,1fr);align-items:start}.vs-prev{position:sticky;top:64px}}
.vs-prev canvas{width:100%;height:auto;max-height:78vh;display:block;margin:0 auto;border-radius:12px;box-shadow:0 8px 26px rgba(0,0,0,.22);background:#ddd;object-fit:contain}
#vsInfo{margin:8px 0 10px;font-size:12.5px;color:#7b8794;text-align:center}
.vs-act{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.vs-act button{padding:11px 16px;border:0;border-radius:12px;font-weight:700;font-size:14.5px;font-family:inherit;cursor:pointer;background:#0073e6;color:#fff}
.vs-act button:disabled{opacity:.45;cursor:default}.vs-act button.alt{background:#fff;color:#0b5cad;border:1px solid #bcd3f0}
.vs-ctl label{display:block;font-weight:700;font-size:14px;margin:0 0 6px;color:#334}
.vs-ctl select,.vs-ctl input[type=text],.vs-ctl input[list]{width:100%;padding:11px 12px;border:1px solid #cdd7e4;border-radius:10px;font-size:15px;font-family:inherit;box-sizing:border-box;background:#fff}
.vs-ctl details{border:1px solid #e5e7eb;border-radius:12px;margin:12px 0;padding:0}
.vs-ctl summary{cursor:pointer;padding:12px 14px;font-weight:700;font-size:15px;color:#223}
.vs-ctl .vs-in{padding:2px 14px 14px}
.vs-th{width:calc(33.3% - 6px);max-width:110px;border:2px solid transparent;border-radius:10px;padding:0;background:none;cursor:pointer;overflow:hidden;font-family:inherit}
.vs-pro{display:inline-block;margin-left:6px;padding:1px 8px;border-radius:10px;background:#ffd43b;color:#5b4a00;font-size:11px;font-weight:700;vertical-align:middle}
.vs-th canvas{width:100%;height:auto;display:block;border-radius:8px}.vs-th span{display:block;font-size:11.5px;color:#445;padding:3px 0}
.vs-th.on{border-color:#0073e6}
#vcard,#vactions{display:none!important}
.vs-shuf{width:100%;max-width:340px;padding:13px 18px!important;font-size:16px!important;background:linear-gradient(135deg,#7c3aed,#2563eb)!important;box-shadow:0 6px 16px rgba(76,60,200,.28)}
.vs-lnk{display:inline-block;padding:11px 16px;border:1px solid #bcd3f0;border-radius:12px;background:#fff;color:#0b5cad;font-weight:700;font-size:14.5px;text-decoration:none}
.vs-strip{margin-top:14px}.vs-strip-h{font-weight:800;font-size:14.5px;color:#223;margin-bottom:8px;text-align:left}.vs-strip-h span{font-weight:400;font-size:12.5px;color:#889;margin-left:6px}
.vs-strip-row{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.vs-sth{display:block;width:100%;height:0;padding:0 0 100%;border:2px solid transparent;border-radius:10px;overflow:hidden;background:#e9eef5;cursor:pointer;position:relative;box-sizing:content-box}
.vs-sth img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;display:block}.vs-sth:hover{border-color:#0073e6}.vs-sth.ld{animation:vsld 1.2s ease-in-out infinite}
@keyframes vsld{0%,100%{opacity:.55}50%{opacity:1}}
.vs-use{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:8px 0 10px}
.vs-u{position:relative;display:flex;align-items:center;gap:10px;padding:14px 40px 14px 12px;border:2px solid #cdd7e4;border-radius:14px;background:#fff;cursor:pointer;text-align:left;font-family:inherit;min-height:64px}
.vs-u i{font-style:normal;font-size:28px;flex:none}.vs-u b{display:block;font-size:16px;color:#16325c;line-height:1.3}.vs-u span{display:block;font-size:12.5px;color:#667;line-height:1.4;margin-top:2px}
.vs-u.on{border-color:#0073e6;background:#eaf3ff;box-shadow:0 0 0 2px rgba(0,115,230,.18)}
.vs-u.on::after{content:"✔";position:absolute;top:50%;right:10px;transform:translateY(-50%);width:24px;height:24px;border-radius:50%;background:#0073e6;color:#fff;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center}
.vs-u em{font-style:normal;display:inline-block;margin-left:6px;padding:0 7px;border-radius:9px;background:#ffd43b;color:#5b4a00;font-size:11px;font-weight:800;vertical-align:middle}
.vs-usemore{margin:0 0 6px;border:0!important}.vs-usemore summary{padding:6px 2px;font-size:14px;color:#0b5cad;font-weight:600}
.vs-usegrid{display:flex;flex-wrap:wrap;gap:8px;padding:4px 0 8px}
.vs-usegrid .vs-chip{font-size:14px;padding:9px 14px}
@media(max-width:520px){.vs-use{grid-template-columns:1fr}.vs-u{padding:12px 42px 12px 12px}}
.vs-cust textarea{width:100%;min-height:96px;padding:10px;border:1px solid #cdd7e4;border-radius:9px;font-size:15px;font-family:inherit;box-sizing:border-box;resize:vertical}
.vs-cust input[type=text]{width:100%;padding:9px 10px;border:1px solid #cdd7e4;border-radius:9px;font-size:15px;font-family:inherit;box-sizing:border-box}
.vs-lock{background:#fffbea;border:1px solid #ffd43b;border-radius:12px;padding:12px 14px;font-size:14px;line-height:1.7;color:#5b4a00}.vs-lock a{color:#0b5cad;font-weight:700}
.vs-batch{margin:26px auto 0;padding:20px 20px 18px;background:#f4f8ff;border:1px solid #cfe0f5;border-radius:16px;text-align:left}
.vs-batch h3{margin:0 0 8px;font-size:18px;color:#0b3d73}.vs-brow{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 8px}.vs-brow>div{flex:1 1 170px}.vs-brow label{display:block;font-size:13px;font-weight:600;margin-bottom:4px;color:#334}
.vs-brow select{width:100%;padding:9px 10px;border:1px solid #cdd7e4;border-radius:9px;font-size:14.5px;font-family:inherit;background:#fff}.vs-chk{display:block;font-size:14px;margin:8px 0}
.vs-bprev{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.vs-bprev img{width:calc(25% - 6px);min-width:120px;border:1px solid #cdd7e4;border-radius:4px;background:#fff}
.vs-phs{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-height:300px;overflow-y:auto;padding:2px}.vs-ph{display:block;position:relative;width:100%;height:0;padding:0 0 100%;border:2px solid transparent;border-radius:8px;overflow:hidden;cursor:pointer;background:#e9eef5;box-sizing:content-box}.vs-ph img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;display:block}.vs-ph.on{border-color:#0073e6}
.vs-row{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.vs-sw{width:36px;height:36px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #cdd7e4;cursor:pointer;padding:0}.vs-sw.on{box-shadow:0 0 0 3px #0073e6}
.vs-fgh{margin:14px 0 6px;padding-top:8px;border-top:1px solid #e5e9f0;font-size:13px;font-weight:800;color:#0b3d73}.vs-fgh:first-child{border-top:0;margin-top:0;padding-top:0}
.vs-font{width:100%;text-align:left;border:1px solid #e1e7ef;background:#fff;border-radius:10px;padding:8px 12px;margin:0 0 6px;cursor:pointer;font-family:inherit}
.vs-font .n{display:block;font-size:11.5px;color:#7b8794}.vs-font .s{display:block;font-size:19px;color:#223;line-height:1.5}.vs-font.on{border-color:#0073e6;background:#f0f6ff}
.vs-chip{padding:7px 13px;border:1px solid #cdd7e4;background:#fff;border-radius:18px;font-size:13.5px;cursor:pointer;font-family:inherit}.vs-chip.on{background:#0073e6;color:#fff;border-color:#0073e6}
.vs-ctl input[type=range]{width:100%}.vs-ck{display:flex;align-items:center;gap:8px;font-size:14px;margin:8px 0;font-weight:400}
.vs-note{font-size:12.5px;color:#7b8794;line-height:1.6;margin:6px 0 0}.vs-up{display:inline-block;margin:6px 0 0;padding:9px 14px;border:1px dashed #9bb7dd;border-radius:10px;font-size:14px;cursor:pointer;color:#0b5cad}
@media print{.vs{display:none!important}}
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
    if(window.crsPilgrimCta) window.crsPilgrimCta({host:'vsPgCta',campaign:'verse_after_draw'});
    var m2=$('vsMore'); var gu=window.__GUIDE[d.ref]; if(m2){ if(gu){m2.href=gu;m2.style.display='inline-block';} else m2.style.display='none'; }
    $('vdraw').textContent='🎴 다시 뽑기';
    var mu=window.__GUIDE[d.ref]; var mo=$('vmore'); if(mu){mo.href=mu; mo.style.display='inline-block';} else {mo.style.display='none';}
    var pc=document.querySelectorAll('.vprint .pc');
    [].forEach.call(pc,function(p){p.querySelector('.pt').textContent=d.text;p.querySelector('.pr').textContent=d.ref;});
    if(window.crsStudio){ window.crsStudio.setVerse(d,{random:!!fromDraw}); if(fromDraw) setTimeout(function(){var st=$('vstudio'); if(st) st.scrollIntoView({behavior:'smooth',block:'start'});},350); }
    if(fromDraw&&window.crsTrack) window.crsTrack('verse_draw',{topic:d.topic,ref:d.ref});
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
  $('vprint').addEventListener('click',function(){
    if(!cur)return; if(window.crsTrack) window.crsTrack('verse_print',{topic:cur.topic,ref:cur.ref}); window.print();
  });
  $('vshare').addEventListener('click',function(){
    if(!cur)return;
    var url=location.origin+(window.__GUIDE[cur.ref]||('/verse/?v='+encodeURIComponent(cur.ref)));
    if(window.crsTrack) window.crsTrack('verse_share',{topic:cur.topic,ref:cur.ref});
    if(navigator.share){ navigator.share({title:'오늘의 말씀 - '+cur.ref,text:cur.text,url:url}).catch(function(){}); return; }
    if(navigator.clipboard){ navigator.clipboard.writeText(url).then(function(){ $('vshare').textContent='✅ 링크 복사됨'; setTimeout(function(){$('vshare').textContent='🔗 링크 공유';},1800); }); }
    else { prompt('링크를 복사하세요',url); }
  });
  var q=new URLSearchParams(location.search).get('v');
  if(q){ var f=D.filter(function(d){return d.ref===q;})[0]; if(f){ last=f; show(f,false); } }
})();
"""


FAQ = [["말씀 카드는 무료인가요?", "네, 말씀 뽑기와 카드 만들기, 이미지 저장·공유·인쇄는 모두 무료입니다. 후원하시면 이미지에서 십자가로세로 워터마크를 뺄 수 있어요."], ["어떤 크기로 저장할 수 있나요?", "카카오톡·인스타그램 정사각(1080×1080)과 4:5, 스토리·휴대폰 배경화면(9:16), 아이폰·갤럭시 긴 화면, 프로필(정사각), PC 배경화면(FHD·QHD), 링크 미리보기(가로), 인쇄용 A4·A5·A6, 책갈피까지 12가지 크기를 지원합니다."], ["배경 이미지는 저작권 문제가 없나요?", "배경 사진은 위키미디어 커먼즈의 자유 이용 사진(CC BY, CC BY-SA, CC0, 퍼블릭 도메인)만 골랐고, 촬영자와 라이선스는 사진을 고르면 카드 아래쪽에 자동으로 적힙니다. CC BY-SA 사진으로 만든 카드는 같은 조건(출처 표시, 동일 조건 공유)으로 자유롭게 나눠 쓰실 수 있어요. 일러스트 풍경과 십자가·비둘기·올리브 가지 같은 장식 도안, 테두리, 분위기 효과는 십자가로세로가 직접 그린 그래픽이고, 내 사진을 올려 배경으로 쓸 수도 있습니다(올린 사진은 기기 안에서만 처리)."], ["글꼴도 무료로 쓸 수 있나요?", "노토 산스·노토 세리프·나눔명조·고운바탕·나눔 손글씨 등 구글 폰트의 무료(SIL OFL) 글꼴 42종을 제공합니다."], ["교회 주보나 주일학교에서 인쇄해도 되나요?", "교회·주일학교·가정에서의 비상업적 인쇄와 사용은 자유롭게 하실 수 있습니다. 판매는 하지 말아 주세요. 인쇄 크기로 A4·A5·A6를 고르면 인쇄 창이 열립니다."], ["성경 본문은 어떤 번역인가요?", "저작권이 만료된 성경전서 개역한글판을 사용합니다."]]


def render(data):
    path = "/verse/"
    title = "말씀 카드 만들기 - 성경 구절 카톡·인스타·배경화면·인쇄 이미지 | 십자가로세로"
    desc = "위로·평안·용기·감사·소망의 말씀을 뽑아 풍경 배경과 무료 글꼴로 말씀 카드를 만들어 보세요. 카카오톡·인스타그램 공유, 프로필, 휴대폰·PC 배경화면, 교회 인쇄용 A4·A5 크기로 저장할 수 있어요."
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication", "name": "말씀 뽑기", "url": SITE + path,
        "applicationCategory": "LifestyleApplication", "inLanguage": "ko", "operatingSystem": "Web",
        "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}, ensure_ascii=False) + "</script>" + \
        '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}, ensure_ascii=False) + "</script>"
    plain_nav = NAV.replace(' nav-active', '')
    h = head(title, desc, path, ld).replace(NAV, plain_nav).replace('og:type" content="article"', 'og:type" content="website"')
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    chips = '<button class="vchip on" data-t="전체">전체</button>' + "".join(
        f'<button class="vchip" data-t="{t}">{t}</button>' for t in PICKS)
    prints = "".join('<div class="pc"><div class="pt"></div><div class="pr"></div><div class="pf">십자가로세로 · crossero.com</div></div>' for _ in range(4))
    guide_map = {ref: verse_url(ref) for ref in COMMENTARY}
    topics = {}
    for d in data:
        if d["ref"] in COMMENTARY:
            topics.setdefault(d["topic"], []).append(d)
    _ph = json.load(open("verse/studio_photos.json", encoding="utf-8"))
    NPH = len(_ph["photos"])
    credits = '<details style="margin-top:22px;text-align:left;max-width:760px"><summary style="cursor:pointer;font-weight:700">📷 배경 사진 출처·라이선스 (%d장)</summary><ul style="font-size:12.5px;line-height:1.7;color:#556;columns:1">' % len(_ph["photos"]) + "".join('<li>%s — %s, <a href="%s" rel="nofollow noopener">%s</a> (<a href="%s" rel="nofollow noopener">원본</a>)</li>' % (html.escape(q["title"]), html.escape(q["artist"]), q["licurl"] or "https://commons.wikimedia.org", html.escape(q["lic"]), q["src"]) for q in _ph["photos"]) + '</ul><p style="font-size:12.5px;color:#556">사진은 위키미디어 커먼즈에서 가져왔으며 크기를 줄이고 글자와 어두운 필터를 입혀 사용합니다. CC BY-SA 사진으로 만든 카드는 같은 라이선스 조건으로 공유됩니다.</p></details>'
    guide = '<h2 style="margin-top:34px;text-align:left">해설이 있는 말씀</h2><div class="cards" style="text-align:left">' + "".join(
        f'<a class="card" href="{guide_map[d["ref"]]}"><b>{esc(d["ref"])}</b><span>{esc(d["topic"])} · {esc(d["text"][:30])}…</span></a>'
        for ts in topics.values() for d in ts) + '</div>'
    from season_picks import SEASONS as _SEASONS
    seasons = season_banner()
    body = f"""<main class="vwrap">
<div class="crumb" style="text-align:left"><a href="/">홈</a> › 말씀 뽑기</div>
<h1 style="margin-top:10px">말씀 뽑기 · 말씀 카드 만들기</h1>
<div class="sub">말씀을 한 장 뽑고, 배경과 글꼴을 골라 나만의 카드로 만들어 보세요</div>
<div class="sub" style="margin-top:-6px"><a href="/today/" data-ga="verse_to_today">📅 오늘의 말씀 보기</a> &nbsp;·&nbsp; <a href="/cards/" data-ga="verse_to_cards">🖼️ 샘플 카드 갤러리</a></div>
{seasons}
<div class="vchips" id="vchips">{chips}</div>
<div class="vbox" id="vbox" title="눌러서 뽑기">🎴</div>
<button class="vbtn" id="vdraw" data-ga="verse_draw_click">🎴 말씀 뽑기</button>
<div class="vcard" id="vcard" style="display:none"><div class="vtag" id="vtag"></div><p class="vtext" id="vtext"></p><div class="vref" id="vref"></div><div class="vmark">십자가로세로 · crossero.com</div></div>
<div class="vactions" id="vactions" style="display:none">
<a class="vbtn sub" id="vmore" href="#" style="display:none;text-decoration:none" data-ga="verse_to_guide">📖 이 말씀 해설 읽기</a>
<button class="vbtn sub" id="vprint">🖨️ 책갈피 인쇄(4장)</button>
<button class="vbtn sub" id="vshare">🔗 링크 공유</button>
</div>
<section class="vs" id="vstudio" style="display:none" aria-label="말씀 카드 만들기">
<h2>🎴 뽑은 말씀 카드</h2>
<p class="vs-sub">마음에 드는 디자인을 고르고 저장·공유·인쇄하세요. <a href="#church-print" style="color:#0b5cad;font-weight:700">⛪ 교회 행사용 여러 장 인쇄 ↓</a> · <a href="/cards/" style="color:#0b5cad;font-weight:700">🖼️ 샘플 카드 둘러보기</a></p>
<div class="vs-grid">
 <div class="vs-prev">
  <canvas id="vsCanvas" width="540" height="540"></canvas>
  <div id="vsInfo"></div>
  <div class="vs-act" style="margin-bottom:8px"><button type="button" id="vsShuffle" class="vs-shuf" data-ga="studio_shuffle">🎲 다른 디자인으로</button></div>
  <div class="vs-act">
   <button type="button" id="vsSave" data-ga="studio_save_click">💾 이미지 저장</button>
   <button type="button" id="vsShare" class="alt" data-ga="studio_share_click">📤 공유하기</button>
   <button type="button" id="vsPrint" class="alt" data-ga="studio_print_click">🖨️ 인쇄하기</button>
   <button type="button" id="vsSaveJpg" class="alt">JPG로 저장</button>
  </div>
  <div class="vs-act" style="margin-top:6px"><a id="vsMore" class="vs-lnk" href="#" style="display:none" data-ga="verse_to_guide">📖 이 말씀 해설 읽기</a><button type="button" id="vsLink" class="alt" data-ga="verse_share_link">🔗 링크 복사</button></div>
  <div id="vsPgCta"></div>
  <div class="vs-strip"><div class="vs-strip-h">같은 말씀, 다른 디자인 <span>눌러서 바꿔 보세요</span></div><div class="vs-strip-row" id="vsStrip"></div></div>
  <p class="vs-note" style="text-align:center">공유가 안 되는 기기에서는 이미지가 저장됩니다. 저장한 사진을 카톡·인스타에 올리세요.</p>
 </div>
 <div class="vs-ctl">
  <label style="font-size:16px">① 어디에 쓰실 건가요?</label>
  <div class="vs-use" id="vsUse"></div>
  <details class="vs-usemore"><summary>다른 크기 더 보기</summary><div class="vs-usegrid" id="vsUseMore"></div></details>
  <p class="vs-note" id="vsUseNote" style="text-align:center;margin-bottom:6px"></p>
  <select id="vsPreset" style="display:none" aria-hidden="true" tabindex="-1"></select>
  <details open><summary>② 배경</summary><div class="vs-in">
   <label style="margin-top:2px">📷 사진 <span style="font-weight:400;color:#889">(무료 라이선스 사진 {NPH}장)</span></label>
   <div class="vs-row" id="vsPhotoThemes" style="margin-bottom:4px"></div>
   <div class="vs-phs" id="vsPhotos"></div>
   <p class="vs-note" id="vsPhotoCredit">사진을 고르면 촬영자와 라이선스가 여기와 카드 아래쪽에 표시돼요.</p>
   <label style="margin-top:12px">🎨 일러스트 풍경</label>
   <div class="vs-row" id="vsScenes"></div>
   <button type="button" class="vs-chip" id="vsVar">🔀 같은 풍경, 다른 느낌</button>
   <div class="vs-row" id="vsGrads" style="margin-top:12px"></div>
   <label class="vs-up">📷 내 사진으로 배경 만들기<input type="file" id="vsUpload" accept="image/*" style="display:none"></label>
   <p class="vs-note">내 사진은 이 기기 안에서만 처리되고 서버로 올라가지 않아요.</p>
   <label style="margin-top:12px">배경 어둡게 <span style="font-weight:400;color:#889">(글자가 잘 보이게)</span></label>
   <input type="range" id="vsDim" min="0" max="70" value="15">
  </div></details>
  <details id="vsFontBox"><summary>③ 글꼴 (무료 글꼴 42종)</summary><div class="vs-in"><div id="vsFonts"></div><p class="vs-note">모든 글꼴은 구글 폰트의 무료(SIL OFL) 글꼴이에요.</p></div></details>
  <details open><summary>④ 글자 꾸미기</summary><div class="vs-in">
   <label>글자 크기</label><input type="range" id="vsScale" min="60" max="160" value="100">
   <label style="margin-top:10px">글자 색</label><div class="vs-row" id="vsTcolor"></div>
   <label style="margin-top:10px" for="vsAlign">정렬</label>
   <select id="vsAlign"><option value="center">가운데</option><option value="left">왼쪽</option></select>
   <label class="vs-ck"><input type="checkbox" id="vsShadow"> 글자 그림자</label>
   <label class="vs-ck"><input type="checkbox" id="vsBox"> 글자 뒤에 반투명 상자</label>
   <label class="vs-ck"><input type="checkbox" id="vsRef"> 성경 구절 위치(예: 시편 23:1) 표시</label>
   <label class="vs-ck"><input type="checkbox" id="vsMark" disabled> 십자가로세로 워터마크</label>
   <p class="vs-note" id="vsMarkNote"></p>
  </div></details>
  <details><summary>⑤ 장식 (십자가·비둘기·테두리·효과)</summary><div class="vs-in">
   <label>글 위 장식 <span style="font-weight:400;color:#889">(직접 그린 도안)</span></label><div class="vs-row" id="vsOrn"></div>
   <label style="margin-top:10px">테두리</label><div class="vs-row" id="vsFrame"></div>
   <label style="margin-top:10px">분위기 효과</label><div class="vs-row" id="vsFx"></div>
   <label style="margin-top:10px">장식 색</label><div class="vs-row" id="vsDcolor"></div>
  </div></details>
  <details id="vsCustBox"><summary>⑥ ✍️ 내가 쓴 말씀 직접 입력 <span class="vs-pro">후원 기능</span></summary><div class="vs-in vs-cust" id="vsCust"></div></details>
  <details><summary>⑦ 다른 말씀으로 바꾸기</summary><div class="vs-in">
   <label for="vsPick">구절 선택</label><input list="vsRefs" id="vsPick" placeholder="예: 시편 23:1"><datalist id="vsRefs"></datalist>
   <p class="vs-note">원하는 구절을 목록에서 골라도 되고, 위의 '말씀 뽑기'로 다시 뽑아도 돼요.</p>
  </div></details>
  <div class="vs-act" style="margin-top:8px"><button type="button" class="alt" id="vsRandom">🎲 스타일 랜덤으로 바꾸기</button></div>
 </div>
</div>
<div class="vs-batch" id="church-print">
 <h3>⛪ 교회·모임용 카드 한꺼번에 인쇄</h3>
 <p class="vs-note" style="margin-top:0">위에서 고른 사진·글꼴·장식 디자인 그대로, 여러 구절을 A4 용지에 모아 인쇄해요. 잘라서 말씀 상자에 담아 한 장씩 뽑는 송구영신·신년 예배, 주일학교, 소그룹 모임에 쓸 수 있어요. <a href="/verse/new-year/guide/" style="color:#0b5cad;font-weight:700">송구영신예배 진행 가이드 보기</a></p>
 <div class="vs-brow">
  <div><label for="vsBSet">구절 묶음</label><select id="vsBSet"></select></div>
  <div><label for="vsBLay">용지당 카드</label><select id="vsBLay"></select></div>
  <div><label for="vsBCopies">구절당 장수</label><select id="vsBCopies"><option>1</option><option>2</option><option>3</option><option>5</option></select></div>
 </div>
 <div id="vsBCustWrap" style="display:none">
  <div class="vs-lock" id="vsBLock" style="display:none">🔒 후원하시면 교회가 쓰는 번역본(개역개정·새번역·영어 등)으로 <b>구절 여러 개를 붙여넣어 한꺼번에 인쇄</b>할 수 있어요. <a href="/support.html" data-ga="batch_custom_to_support">후원 안내 보기 →</a></div>
  <div id="vsBCustBox"><label for="vsBCustText" style="font-size:13px;font-weight:600;color:#334">구절 붙여넣기 (한 줄에 카드 한 장)</label>
  <textarea id="vsBCustText" style="width:100%;min-height:130px;padding:10px;border:1px solid #cdd7e4;border-radius:9px;font-size:14.5px;font-family:inherit;box-sizing:border-box" placeholder="본문 | 출처&#10;예) 여호와는 나의 목자시니 내가 부족함이 없으리로다 | 시편 23:1 · 개역개정&#10;출처는 생략해도 돼요."></textarea>
  <p class="vs-note">한 줄에 한 구절씩 쓰고, 본문과 출처는 | 로 나눠요. 번역본의 저작권과 사용 허락은 사용하시는 분이 확인해 주세요.</p></div>
 </div>
 <label class="vs-chk"><input type="checkbox" id="vsBCut" checked> 자르는 선(점선) 넣기</label>
 <p class="vs-note" id="vsBInfo"></p>
 <div class="vs-act"><button type="button" id="vsBGo">🖨️ 인쇄 미리보기 만들기</button><button type="button" class="alt" id="vsBPrint" disabled>인쇄하기 (PDF 저장 가능)</button></div>
 <div class="vs-bprev" id="vsBPrev"></div>
</div>
</section>
{credits}
{guide}
<h2 style="margin-top:34px;text-align:left">자주 묻는 질문</h2><div class="faq" style="text-align:left;max-width:760px"><details><summary>말씀 카드는 무료인가요?</summary><p>네, 말씀 뽑기와 카드 만들기, 이미지 저장·공유·인쇄는 모두 무료입니다. 후원하시면 이미지에서 십자가로세로 워터마크를 뺄 수 있어요.</p></details><details><summary>어떤 크기로 저장할 수 있나요?</summary><p>카카오톡·인스타그램 정사각(1080×1080)과 4:5, 스토리·휴대폰 배경화면(9:16), 아이폰·갤럭시 긴 화면, 프로필(정사각), PC 배경화면(FHD·QHD), 링크 미리보기(가로), 인쇄용 A4·A5·A6, 책갈피까지 12가지 크기를 지원합니다.</p></details><details><summary>배경 이미지는 저작권 문제가 없나요?</summary><p>풍경 배경은 십자가로세로가 직접 그린 그래픽이라 저작권 걱정 없이 쓰실 수 있습니다. 내 사진을 올려 배경으로 쓸 수도 있고, 올린 사진은 기기 안에서만 처리됩니다.</p></details><details><summary>글꼴도 무료로 쓸 수 있나요?</summary><p>노토 산스·노토 세리프·나눔명조·고운바탕·나눔 손글씨 등 구글 폰트의 무료(SIL OFL) 글꼴 42종을 제공합니다.</p></details><details><summary>교회 주보나 주일학교에서 인쇄해도 되나요?</summary><p>교회·주일학교·가정에서의 비상업적 인쇄와 사용은 자유롭게 하실 수 있습니다. 판매는 하지 말아 주세요. 인쇄 크기로 A4·A5·A6를 고르면 인쇄 창이 열립니다.</p></details><details><summary>성경 본문은 어떤 번역인가요?</summary><p>저작권이 만료된 성경전서 개역한글판을 사용합니다.</p></details></div>
<p class="vnote">성경 본문은 성경전서 개역한글판(대한성서공회)을 사용했습니다. 개인 묵상과 소모임 나눔을 위한 용도로 제공하며, 판매용으로 이용하실 수 없습니다. 구절은 주제별로 직접 골랐고, 앞으로 계속 늘려 갑니다. 말씀을 더 깊이 읽고 싶다면 <a href="/dictionary/">성경사전</a>에서 해당 책의 요약을 확인해 보세요.</p>
<div class="vprint" aria-hidden="true">{prints}</div>
</main>"""
    try:
        _pl = json.load(open("cards_plan.json", encoding="utf-8"))
        _seen, _rec = set(), []
        for _c in _pl:
            _d = dict(_c["design"])
            _k = json.dumps(_d, sort_keys=True)
            if _k in _seen:
                continue
            _seen.add(_k)
            _rec.append(_d)
        random.Random(11).shuffle(_rec)
        _rec = _rec[:90]
    except Exception:
        _rec = []
    data_js = ("<script>window.__RECIPES=" + json.dumps(_rec, ensure_ascii=False, separators=(",", ":")) + ";window.__VERSES=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";"
               "window.__SETS=" + json.dumps(build_sets(data), ensure_ascii=False, separators=(",", ":")) + ";window.__GUIDE=" + json.dumps(guide_map, ensure_ascii=False, separators=(",", ":")) + ";</script>")
    return "\n".join([h, body, FOOTER, data_js,
                      '<script src="/ga-events.js"></script><script src="/subscribe.js"></script><script src="/auth.js"></script><script src="/pilgrim-cta.js"></script><script src="/verse/studio_bg.js"></script><script src="/verse/studio_deco.js"></script><script src="/verse/studio.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


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
