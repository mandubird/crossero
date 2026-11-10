# -*- coding: utf-8 -*-
"""성경 퀴즈 페이지(/quiz/) 생성. 실행: python3 build_quiz.py
허브 + 성경 OX 퀴즈 + 성경 인물 퀴즈. 가입 없이 풀고, 문항마다 근거 구절(장·절)과 해설을 보여 준다.
근거 구절은 BIBLE.csv(개역한글)에서 핵심 낱말이 실제로 들어 있는지 빌드 때마다 검증한다."""
import json
import os
import re

import build_dictionary as bd
from build_dictionary import head, FOOTER, NAV, SITE, ROOT, esc, ENTRIES
from verse_lib import KO_BOOKS, load_text

TEXT = load_text()

# (진술, 정답 O/X, (책, 장, 절), 구절에 들어 있어야 할 낱말, 해설)
OX = [
    ("다윗은 칼로 골리앗을 쓰러뜨렸다.", False, ("사무엘상", 17, 50), "물매", "다윗은 칼 없이 물매와 돌 하나로 골리앗을 이겼습니다."),
    ("노아 때 홍수의 비는 사십 일 동안 내렸다.", True, ("창세기", 7, 12), "사십", "사십 주야 동안 땅에 비가 내렸다고 기록되어 있습니다."),
    ("예수님은 나사렛에서 태어나셨다.", False, ("마태복음", 2, 1), "베들레헴", "예수님은 유대 베들레헴에서 나시고, 자라신 곳이 나사렛입니다."),
    ("요나는 큰 물고기 뱃속에서 사흘 동안 있었다.", True, ("요나", 1, 17), "삼일", "여호와께서 큰 물고기를 예비하사 요나를 삼키게 하셨고, 요나는 사흘 밤낮을 그 뱃속에 있었습니다."),
    ("요셉은 형들에 의해 은 이십에 팔려 갔다.", True, ("창세기", 37, 28), "이십", "형들은 요셉을 은 이십에 이스마엘 상인들에게 팔았습니다."),
    ("모세는 약속의 땅 가나안에 들어갔다.", False, ("신명기", 34, 4), "건너가지", "모세는 느보 산에서 가나안 땅을 바라보기만 하고 건너가지 못했습니다."),
    ("삼손의 힘의 비밀은 머리털과 관련이 있었다.", True, ("사사기", 16, 17), "머리", "삼손은 나실인으로 구별된 자라 머리에 삭도를 대지 않았고, 이것이 힘의 비밀이었습니다."),
    ("베드로는 예수님을 세 번 모른다고 했다.", True, ("마태복음", 26, 75), "세 번", "닭이 울기 전에 세 번 부인할 것이라는 예수님의 말씀이 이루어졌습니다."),
    ("가나의 혼인 잔치에서 예수님은 물을 포도주로 바꾸셨다.", True, ("요한복음", 2, 9), "포도주", "예수님이 행하신 첫 번째 표적입니다."),
    ("다니엘은 사자 굴에서 상하지 않았다.", True, ("다니엘", 6, 22), "사자", "하나님이 천사를 보내어 사자들의 입을 봉하셨습니다."),
    ("아담과 하와의 첫째 아들은 아벨이다.", False, ("창세기", 4, 1), "가인", "첫째 아들은 가인이고, 동생이 아벨입니다."),
    ("야곱의 막내아들은 요셉이다.", False, ("창세기", 35, 18), "베냐민", "야곱의 막내아들은 베냐민입니다."),
    ("여리고 성은 일곱째 날에 성을 일곱 번 돈 뒤 무너졌다.", True, ("여호수아", 6, 15), "일곱 번", "이스라엘은 엿새 동안 하루에 한 번씩, 일곱째 날에는 일곱 번 성을 돌았습니다."),
    ("엘리야는 갈멜산에서 바알의 선지자들과 대결했다.", True, ("열왕기상", 18, 19), "갈멜", "엘리야는 하나님이 참 하나님이심을 갈멜산에서 보여 주었습니다."),
    ("솔로몬은 하나님께 지혜를 구했다.", True, ("열왕기상", 3, 12), "지혜", "솔로몬이 부와 장수가 아니라 듣는 마음(지혜)을 구하자 하나님이 기뻐하셨습니다."),
    ("성령은 오순절에 제자들에게 임하셨다.", True, ("사도행전", 2, 4), "성령", "오순절에 모인 사람들이 성령의 충만함을 받았습니다."),
    ("바울은 예수님의 열두 제자 가운데 한 사람이다.", False, ("사도행전", 9, 4), "사울", "바울(사울)은 예수님이 승천하신 뒤 다메섹 도상에서 예수님을 만난 사도로, 열두 제자에 속하지 않았습니다."),
    ("에스더는 바사(페르시아) 왕의 왕후가 되었다.", True, ("에스더", 2, 17), "왕후", "왕은 에스더를 사랑하여 와스디를 대신해 왕후로 삼았습니다."),
    ("룻은 이스라엘 사람이다.", False, ("룻기", 1, 4), "모압", "룻은 모압 여인이었고, 시어머니 나오미를 따라 베들레헴으로 갔습니다."),
    ("사울은 이스라엘의 초대 왕이다.", True, ("사무엘상", 10, 1), "사울", "사무엘이 기름을 부어 사울을 이스라엘의 첫 왕으로 세웠습니다."),
    ("하나님은 이스라엘 백성이 홍해를 마른 땅으로 건너게 하셨다.", True, ("출애굽기", 14, 21), "마른 땅", "물이 좌우에 벽이 되어 이스라엘 백성은 바다 가운데 마른 땅으로 건넜습니다."),
    ("예수님은 부활하신 뒤 사십 일 동안 제자들에게 나타나셨다.", True, ("사도행전", 1, 3), "사십", "사십 일 동안 여러 번 보이시고 하나님 나라의 일을 말씀하셨습니다."),
    ("요한계시록은 구약성경의 마지막 책이다.", False, None, None, "요한계시록은 신약성경의 마지막 책이자 성경 66권의 마지막 책입니다. 구약의 마지막 책은 말라기입니다."),
    ("아브라함의 아내 사라는 처음에 '사래'라고 불렸다.", True, ("창세기", 17, 15), "사라", "하나님이 사래의 이름을 사라로 바꾸라고 하셨습니다."),
    ("마리아와 요셉은 예수님이 태어나기 전부터 베들레헴에 살고 있었다.", False, ("누가복음", 2, 4), "나사렛", "요셉은 호적을 하러 나사렛에서 베들레헴으로 올라갔습니다."),
    ("애굽에 내린 열 가지 재앙의 마지막은 장자의 죽음이다.", True, ("출애굽기", 12, 29), "장자", "밤중에 애굽 땅의 모든 장자를 치시자 바로가 이스라엘을 보내 주었습니다."),
    ("모세는 불붙은 떨기나무 앞에서 하나님의 부르심을 받았다.", True, ("출애굽기", 3, 2), "떨기나무", "불꽃 가운데서 여호와의 사자가 모세에게 나타났습니다."),
    ("예수님은 떡 다섯 개와 물고기 두 마리로 오천 명을 먹이셨다.", True, ("마태복음", 14, 17), "다섯", "남은 조각이 열두 바구니에 찼습니다."),
    ("성경은 구약 39권과 신약 27권, 모두 66권이다(개신교 기준).", True, None, None, "개신교 성경은 구약 39권, 신약 27권으로 모두 66권입니다."),
    ("하나님은 여섯째 날에 사람을 지으셨다.", True, ("창세기", 1, 31), "여섯째", "하나님이 지으신 모든 것을 보시고 심히 좋았더라고 하신 날이 여섯째 날입니다."),
]

# (단서, 정답, 오답 3개, 근거 구절 표기, 해설)
PEOPLE = [
    ("홍해를 가르고 이스라엘을 이끌어 애굽에서 나온 지도자는?", "모세", ["아론", "여호수아", "다윗"], "출애굽기 14장", "하나님의 부르심을 받아 이스라엘을 애굽에서 이끌어 낸 지도자입니다."),
    ("물매와 돌 하나로 골리앗을 쓰러뜨린 소년은?", "다윗", ["사울", "삼손", "요나단"], "사무엘상 17장", "양 치던 소년 다윗이 하나님의 이름으로 골리앗 앞에 섰습니다."),
    ("사자 굴에 던져졌지만 하나님이 지켜 주신 사람은?", "다니엘", ["에스겔", "요셉", "느헤미야"], "다니엘 6장", "다니엘은 매일 하나님께 기도하다 사자 굴에 던져졌지만 상하지 않았습니다."),
    ("큰 물고기 뱃속에서 사흘을 보낸 선지자는?", "요나", ["엘리야", "호세아", "아모스"], "요나 1장", "니느웨로 가라는 명령을 피하려다 큰 물고기에게 삼켜졌습니다."),
    ("머리털에 힘의 비밀이 있던 사사는?", "삼손", ["기드온", "입다", "에훗"], "사사기 16장", "나실인 삼손의 힘은 하나님이 주신 것이었습니다."),
    ("다메섹으로 가던 길에서 예수님을 만나 회심한 사도는?", "바울", ["베드로", "요한", "바나바"], "사도행전 9장", "교회를 박해하던 사울이 예수님을 만나 복음의 증인이 되었습니다."),
    ("예수님을 세 번 모른다고 했던 제자는?", "베드로", ["도마", "빌립", "안드레"], "마태복음 26장", "닭 울기 전에 세 번 부인했고, 나중에 예수님이 다시 회복시켜 주셨습니다."),
    ("아들 이삭을 바치려고 모리아 산으로 갔던 믿음의 조상은?", "아브라함", ["이삭", "야곱", "롯"], "창세기 22장", "하나님이 시험하셨고, 아브라함은 순종했습니다."),
    ("형들에게 팔려 애굽의 총리가 된 사람은?", "요셉", ["베냐민", "유다", "르우벤"], "창세기 37~41장", "야곱의 열한째 아들 요셉은 애굽에서 총리가 되어 가족을 살렸습니다."),
    ("갈멜산에서 바알의 선지자들과 대결한 선지자는?", "엘리야", ["엘리사", "이사야", "예레미야"], "열왕기상 18장", "하늘에서 불이 내려 여호와가 참 하나님이심이 드러났습니다."),
    ("방주를 지어 가족과 동물들을 구한 사람은?", "노아", ["아담", "에녹", "므두셀라"], "창세기 6~9장", "하나님의 말씀에 순종해 방주를 지었습니다."),
    ("'죽으면 죽으리이다'라고 말하며 민족을 위해 왕 앞에 나선 왕후는?", "에스더", ["룻", "한나", "미리암"], "에스더 4장", "유대 민족을 구하기 위해 목숨을 걸고 왕 앞에 나아갔습니다."),
    ("시어머니 나오미를 따라 베들레헴으로 간 모압 여인은?", "룻", ["에스더", "라합", "다말"], "룻기 1장", "'어머니의 하나님이 나의 하나님이 되시리이다'라고 고백했습니다."),
    ("하나님께 지혜를 구하고 성전을 지은 왕은?", "솔로몬", ["다윗", "히스기야", "요시야"], "열왕기상 3장", "다윗의 아들로 이스라엘의 왕이 되었고 예루살렘 성전을 지었습니다."),
    ("세리였다가 예수님의 제자가 된 사람은?", "마태", ["마가", "누가", "요한"], "마태복음 9장", "세관에 앉아 있다가 예수님의 부르심을 받고 따랐습니다."),
    ("예수님의 어머니는?", "마리아", ["마르다", "엘리사벳", "한나"], "누가복음 1~2장", "천사의 소식을 듣고 순종한 여인입니다."),
    ("교회의 첫 순교자는?", "스데반", ["야고보", "빌립", "디모데"], "사도행전 7장", "돌에 맞아 순교하며 원수를 위해 기도했습니다."),
    ("팥죽 한 그릇에 장자권을 판 사람은?", "에서", ["야곱", "이삭", "이스마엘"], "창세기 25장", "야곱의 쌍둥이 형입니다."),
    ("이스라엘의 첫 번째 왕은?", "사울", ["다윗", "솔로몬", "사무엘"], "사무엘상 10장", "사무엘이 기름을 부어 왕으로 세웠습니다."),
    ("에덴동산에서 하나님이 가장 먼저 지으신 사람은?", "아담", ["가인", "셋", "노아"], "창세기 2장", "하나님이 흙으로 지으시고 생기를 불어넣으셨습니다."),
]

CSS = """
.qz-wrap{max-width:720px;margin:0 auto;padding:20px 16px 36px;color:#222;text-align:left}
.qz-wrap h1{font-size:26px;line-height:1.4;margin:6px 0 8px;color:#0b3d73;word-break:keep-all}
.qz-sub{font-size:16px;line-height:1.8;color:#445;margin:0 0 16px;word-break:keep-all}
.qz-box{border:1px solid #cfe0f7;background:#f7faff;border-radius:16px;padding:18px 18px 16px;margin:14px 0}
.qz-prog{font-size:14px;color:#556;margin:0 0 8px}
.qz-q{font-size:21px;line-height:1.65;font-weight:700;color:#16324f;margin:0 0 14px;word-break:keep-all}
.qz-btns{display:flex;gap:10px;flex-wrap:wrap}
.qz-btn{flex:1;min-width:120px;border:2px solid #bcd3f0;background:#fff;color:#0b3d73;border-radius:14px;padding:15px 12px;font-size:19px;font-weight:700;cursor:pointer;font-family:inherit}
.qz-btn.ox{font-size:34px;padding:12px}
.qz-btn:disabled{cursor:default}
.qz-btn.ok{background:#e8f7ec;border-color:#4cae6a;color:#1d6b38}.qz-btn.no{background:#fdecec;border-color:#e08585;color:#a33}
.qz-start,.qz-next{display:inline-block;border:0;border-radius:14px;padding:14px 26px;font-size:18px;font-weight:700;cursor:pointer;background:#0073e6;color:#fff;font-family:inherit;text-decoration:none;margin:6px 8px 0 0}
.qz-start.sub,.qz-next.sub{background:#fff;color:#0b3d73;border:1px solid #bcd3f0}
.qz-exp{display:none;margin:14px 0 0;padding:12px 14px;border-radius:12px;background:#fff;border:1px solid #dbe6f3;font-size:16px;line-height:1.8}
.qz-exp b.r{color:#1d6b38}.qz-exp b.w{color:#a33}
.qz-score{font-size:30px;font-weight:800;color:#0b3d73;margin:4px 0}
.qz-list details{border:1px solid #e3e8ef;border-radius:10px;padding:10px 14px;margin:0 0 8px;background:#fff}
.qz-list summary{cursor:pointer;font-weight:600;font-size:15.5px;line-height:1.6}
.qz-list p{margin:8px 0 0;font-size:15px;line-height:1.8}
.qz-info h2{font-size:20px;color:#16324f;margin:28px 0 8px}
.qz-info p,.qz-info li{font-size:15.5px;line-height:1.85;word-break:keep-all}
.qz-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}
.qz-card{display:block;border:1px solid #dbe6f3;border-radius:14px;padding:14px 16px;text-decoration:none;color:#222;background:#fff}
.qz-card b{display:block;font-size:18px;color:#0b3d73;margin:2px 0 4px}.qz-card span{font-size:14.5px;color:#556;line-height:1.7}
.peek,.pg-pill,.pg-side{display:none!important}
@media(max-width:560px){.qz-wrap h1{font-size:22px}.qz-q{font-size:19px}.qz-cards{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
  var D=window.__QZ,kind=D.kind,Q=D.q,i=0,score=0,wrong=[],$=function(x){return document.getElementById(x)};
  function track(n,p){if(window.crsTrack)window.crsTrack(n,p||{});}
  function shuffle(a){a=a.slice();for(var k=a.length-1;k>0;k--){var j=Math.floor(Math.random()*(k+1));var t=a[k];a[k]=a[j];a[j]=t;}return a;}
  function show(){
    var q=Q[i];$('qzProg').textContent=(i+1)+' / '+Q.length+'  ·  맞힌 문제 '+score;$('qzQ').textContent=q.q;$('qzExp').style.display='none';$('qzNext').style.display='none';
    var b=$('qzBtns');b.innerHTML='';
    if(kind==='ox'){['O','X'].forEach(function(v){var e=document.createElement('button');e.className='qz-btn ox';e.textContent=v;e.onclick=function(){answer(v==='O'===q.a,v,e);};b.appendChild(e);});}
    else{q.o.forEach(function(t){var e=document.createElement('button');e.className='qz-btn';e.textContent=t;e.onclick=function(){answer(t===q.a,t,e);};b.appendChild(e);});}
  }
  function answer(ok,val,el){
    var q=Q[i],bs=$('qzBtns').children,k;
    for(k=0;k<bs.length;k++){bs[k].disabled=true;
      var good=kind==='ox'?((bs[k].textContent==='O')===q.a):bs[k].textContent===q.a;
      if(good)bs[k].className+=' ok';}
    if(!ok){el.className+=' no';wrong.push(q);}else score++;
    var ans=kind==='ox'?(q.a?'O (맞아요)':'X (틀려요)'):q.a;
    $('qzExp').innerHTML='<b class="'+(ok?'r':'w')+'">'+(ok?'정답입니다!':'아쉬워요.')+'</b> 정답: <b>'+ans+'</b><br>'+q.e+(q.r?'<br><small>근거: '+q.r+'</small>':'')+(q.u?' <a href="'+q.u+'">→ 성경사전에서 더 보기</a>':'');
    $('qzExp').style.display='block';$('qzNext').style.display='inline-block';$('qzNext').textContent=(i===Q.length-1)?'결과 보기':'다음 문제';
    $('qzProg').textContent=(i+1)+' / '+Q.length+'  ·  맞힌 문제 '+score;
  }
  function finish(){
    track('quiz_done',{kind:kind,score:score,total:Q.length});
    var pct=Math.round(score/Q.length*100),msg=pct>=90?'대단해요! 성경을 아주 잘 알고 계시네요.':pct>=60?'잘했어요! 틀린 문제를 다시 보면 더 좋아요.':'괜찮아요. 해설을 읽고 다시 도전해 보세요.';
    $('qzPlay').style.display='none';$('qzEnd').style.display='block';
    $('qzScore').textContent=score+' / '+Q.length+'  ('+pct+'점)';$('qzMsg').textContent=msg;
    var w=$('qzWrong');w.innerHTML=wrong.length?'<h3>다시 볼 문제</h3>'+wrong.map(function(q){return '<p>• '+q.q+' → <b>'+(kind==='ox'?(q.a?'O':'X'):q.a)+'</b></p>';}).join(''):'<p>모두 맞혔어요! 🎉</p>';
  }
  $('qzStart').onclick=function(){Q=shuffle(D.q).slice(0,D.n||D.q.length);i=0;score=0;wrong=[];$('qzIntro').style.display='none';$('qzPlay').style.display='block';$('qzEnd').style.display='none';track('quiz_start',{kind:kind});show();};
  $('qzNext').onclick=function(){if(i===Q.length-1){finish();}else{i++;show();}};
  $('qzAgain').onclick=function(){$('qzStart').onclick();};
  $('qzShare').onclick=function(){var u=location.href.split('#')[0];track('quiz_share',{kind:kind});if(navigator.share){navigator.share({title:document.title,url:u}).catch(function(){});return;}if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){$('qzShare').textContent='✅ 링크 복사됨';});};
})();
"""


def vtext(ref):
    name, c, v = ref
    return TEXT[(KO_BOOKS.index(name) + 1, c, v)]


def slug_by_name(name, typ="인물"):
    for e in ENTRIES:
        if e["type"] == typ and e["name"] == name:
            return f"/dictionary/{e['slug']}.html"
    return None


def prep_ox():
    items = []
    for q, a, ref, kw, exp in OX:
        r = None
        if ref:
            assert kw in vtext(ref), f"근거 구절에 '{kw}' 없음: {q} {ref} → {vtext(ref)}"
            r = f"{ref[0]} {ref[1]}:{ref[2]}"
        items.append({"q": q, "a": a, "e": exp, "r": r})
    return items


def prep_people():
    items = []
    for q, a, wrong, ref, exp in PEOPLE:
        items.append({"q": q, "a": a, "o": [a] + wrong, "e": exp, "r": ref, "u": slug_by_name(a)})
    for it in items:
        # 보기 순서는 정답이 늘 첫 번째로 보이지 않도록 질문 문자열 기반으로 고정 섞기
        k = sum(ord(c) for c in it["q"]) % len(it["o"])
        it["o"] = it["o"][k:] + it["o"][:k]
    return items


def page(path, title, desc, h1, sub, kind, qs, n, how, faq, list_html, extra_links):
    ld = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": h1, "url": SITE + path, "applicationCategory": "EducationalApplication", "inLanguage": "ko",
         "operatingSystem": "Web", "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    h = head(title, desc, path, "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace('og:type" content="article"', 'og:type" content="website"').replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    body = f"""<main class="qz-wrap">
<p style="margin:0"><a href="/quiz/">← 성경 퀴즈</a></p>
<h1>{esc(h1)}</h1>
<p class="qz-sub">{esc(sub)}</p>
<div class="qz-box" id="qzIntro"><p style="margin:0 0 6px;font-size:16px;line-height:1.8">{esc(how)}</p><button class="qz-start" id="qzStart" type="button">🎯 퀴즈 시작하기</button></div>
<div class="qz-box" id="qzPlay" style="display:none"><p class="qz-prog" id="qzProg"></p><p class="qz-q" id="qzQ"></p><div class="qz-btns" id="qzBtns"></div><div class="qz-exp" id="qzExp"></div><button class="qz-next" id="qzNext" type="button" style="display:none">다음 문제</button></div>
<div class="qz-box" id="qzEnd" style="display:none"><p style="margin:0;font-size:15px;color:#556">결과</p><p class="qz-score" id="qzScore"></p><p id="qzMsg" style="font-size:16.5px;margin:0 0 6px"></p><div id="qzWrong"></div>
<button class="qz-start" id="qzAgain" type="button">🔁 다시 풀기</button><button class="qz-start sub" id="qzShare" type="button">🔗 친구에게 나누기</button>{extra_links}</div>
<section class="qz-info qz-list"><h2>전체 문제와 정답 보기</h2>{list_html}</section>
<section class="qz-info"><h2>자주 묻는 질문</h2><div class="faq">{faq_html}</div>
<p style="font-size:14px;color:#667;line-height:1.8">문제와 해설은 십자가로세로가 직접 작성했고, 근거 구절은 개역한글판을 기준으로 확인했습니다. 교회학교·소그룹 수업에 자유롭게 쓰실 수 있고, 출처(십자가로세로)를 밝혀 주세요. 퍼즐로 복습하려면 <a href="/list.html">성경 퍼즐 목록</a>, 배경을 더 알고 싶다면 <a href="/dictionary/">성경사전</a>을 이용해 보세요.</p></section>
</main>"""
    data = {"kind": kind, "q": qs, "n": n}
    return "\n".join([h, body, FOOTER, "<script>window.__QZ=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";</script>", '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def ox_page():
    qs = prep_ox()
    lst = "".join(f"<details><summary>{i+1}. {esc(x['q'])}</summary><p><b>정답: {'O' if x['a'] else 'X'}</b> — {esc(x['e'])}" + (f" <small>(근거: {esc(x['r'])})</small>" if x["r"] else "") + "</p></details>" for i, x in enumerate(qs))
    faq = [("성경 OX 퀴즈는 몇 문제인가요?", f"전체 {len(qs)}문제 중 매번 10문제가 무작위로 나옵니다. 다시 풀면 다른 문제가 섞여 나옵니다."),
           ("정답과 해설도 볼 수 있나요?", "문제를 풀 때마다 정답과 짧은 해설, 근거 구절의 장·절을 바로 보여 드립니다. 아래 전체 목록에서도 모든 정답을 볼 수 있습니다."),
           ("어린이도 풀 수 있나요?", "네. 노아, 다윗, 요나처럼 잘 알려진 이야기 중심이라 초등 고학년부터 쉽게 풀 수 있고, 교회학교 수업의 도입 활동으로도 좋습니다."),
           ("회원가입이 필요한가요?", "필요 없습니다. 무료이고 입력 정보도 받지 않습니다.")]
    return page("/quiz/ox/", f"성경 OX 퀴즈 {len(qs)}문제 - 정답과 해설, 무료로 풀기 | 십자가로세로",
                f"성경 OX 퀴즈 {len(qs)}문제를 무료로 풀어 보세요. 노아, 다윗, 요나, 예수님 이야기까지 문제마다 정답과 해설, 근거 구절을 알려 드립니다. 가입 없이 바로 시작.",
                "성경 OX 퀴즈", "맞으면 O, 틀리면 X! 성경 속 이야기를 문제마다 해설과 함께 풀어 보세요.", "ox", qs, 10,
                f"전체 {len(qs)}문제 중 10문제가 무작위로 나옵니다. 문장을 읽고 O 또는 X를 누르세요. 누를 때마다 정답과 해설이 나옵니다.", faq, lst,
                '<a class="qz-start sub" href="/quiz/people/">👤 인물 퀴즈 풀기</a>')


def people_page():
    qs = prep_people()
    lst = "".join(f"<details><summary>{i+1}. {esc(x['q'])}</summary><p><b>정답: {esc(x['a'])}</b> — {esc(x['e'])} <small>(근거: {esc(x['r'])})</small>" + (f' <a href="{x["u"]}">성경사전에서 보기</a>' if x["u"] else "") + "</p></details>" for i, x in enumerate(qs))
    faq = [("성경 인물 퀴즈는 어떻게 푸나요?", "설명을 읽고 네 개의 보기 가운데 알맞은 인물을 고르세요. 문제마다 정답과 해설이 바로 나옵니다."),
           ("몇 문제가 나오나요?", f"전체 {len(qs)}문제 중 매번 10문제가 무작위로 나옵니다."),
           ("인물에 대해 더 알고 싶으면?", "정답 해설 아래의 '성경사전에서 더 보기' 링크로 그 인물의 생애와 핵심 구절을 볼 수 있습니다."),
           ("교회학교에서 활용해도 되나요?", "네. 수업 도입이나 마무리 활동으로 쓰시고, 출처(십자가로세로)를 밝혀 주세요.")]
    return page("/quiz/people/", f"성경 인물 퀴즈 {len(qs)}문제 - 누구일까요? 정답·해설 | 십자가로세로",
                f"성경 인물 퀴즈 {len(qs)}문제! 모세, 다윗, 다니엘, 바울… 설명을 보고 누구인지 맞혀 보세요. 객관식 4지선다, 정답 해설과 성경사전 링크까지 무료.",
                "성경 인물 퀴즈", "설명을 보고 누구인지 맞혀 보세요. 모세, 다윗, 바울… 성경 속 인물을 4지선다로 풀어요.", "people", qs, 10,
                f"전체 {len(qs)}문제 중 10문제가 무작위로 나옵니다. 설명을 읽고 알맞은 인물을 고르세요.", faq, lst,
                '<a class="qz-start sub" href="/quiz/ox/">⭕ OX 퀴즈 풀기</a>')


def hub_page():
    path = "/quiz/"
    title = "성경 퀴즈 게임 - OX 퀴즈·인물 퀴즈 무료로 풀기 | 십자가로세로"
    desc = "성경 퀴즈를 무료로 풀어 보세요. 성경 OX 퀴즈, 성경 인물 퀴즈에 정답과 해설, 근거 구절까지. 가로세로 낱말 퍼즐과 성경사전으로 이어서 공부할 수 있습니다."
    faq = [("성경 퀴즈 게임은 무료인가요?", "네. 가입 없이 무료로 풀 수 있습니다."),
           ("어떤 퀴즈가 있나요?", "성경 OX 퀴즈와 성경 인물 퀴즈가 있고, 이어서 풀 수 있는 가로세로 낱말 퍼즐과 책별 요약, 성경사전이 있습니다."),
           ("교회학교 수업에도 쓸 수 있나요?", "네. 수업 도입이나 마무리 활동으로 활용하실 수 있고, 주일학교 자료는 교사 허브에서 더 볼 수 있습니다.")]
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "성경 퀴즈", "url": SITE + path, "description": desc, "inLanguage": "ko"},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    h = head(title, desc, path, "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace('og:type" content="article"', 'og:type" content="website"').replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    body = f"""<main class="qz-wrap">
<h1>🎯 성경 퀴즈 게임</h1>
<p class="qz-sub">가입 없이 무료로 풀어 보세요. 문제마다 정답과 해설, 근거 구절을 알려 드립니다.</p>
<div class="qz-cards">
<a class="qz-card" href="/quiz/ox/"><span>⭕ OX 퀴즈</span><b>성경 OX 퀴즈</b><span>맞으면 O, 틀리면 X. 노아·다윗·예수님 이야기 {len(OX)}문제 중 10문제.</span></a>
<a class="qz-card" href="/quiz/people/"><span>👤 인물 퀴즈</span><b>성경 인물 퀴즈</b><span>설명을 보고 누구인지 맞혀요. 4지선다 {len(PEOPLE)}문제 중 10문제.</span></a>
<a class="qz-card" href="/list.html"><span>🧩 낱말 퍼즐</span><b>성경 가로세로 퍼즐</b><span>말씀으로 풀어 보는 낱말 퍼즐 모음.</span></a>
<a class="qz-card" href="/dictionary/"><span>📖 성경사전</span><b>더 알아보기</b><span>인물·지명·사건·66권 요약으로 이어서 공부해요.</span></a>
</div>
<section class="qz-info"><h2>성경 퀴즈, 이렇게 활용해 보세요</h2>
<ul><li><b>혼자서</b> — 하루 10문제로 성경 상식을 가볍게 복습합니다.</li><li><b>가족·친구와</b> — 문제를 번갈아 읽고 O/X를 외치며 함께 풉니다.</li><li><b>교회학교·소그룹에서</b> — 수업 도입이나 마무리 활동으로 쓰고, <a href="/teachers/">교사 허브</a>의 자료와 함께 사용하세요.</li></ul>
<h2>자주 묻는 질문</h2><div class="faq">{faq_html}</div></section>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- QUIZ-START -->.*?<!-- QUIZ-END -->", "", s, flags=re.S)
    block = "\n  <!-- QUIZ-START -->\n" + "".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n" for u in ("/quiz/", "/quiz/ox/", "/quiz/people/")) + "  <!-- QUIZ-END -->\n"
    open(p, "w", encoding="utf-8").write(s.replace("</urlset>", block + "</urlset>"))


def main():
    for rel, html in (("quiz/index.html", hub_page()), ("quiz/ox/index.html", ox_page()), ("quiz/people/index.html", people_page())):
        fp = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(html)
    update_sitemap()
    print("퀴즈 페이지 생성: 허브 1 + OX", len(OX), "문항 + 인물", len(PEOPLE), "문항")


if __name__ == "__main__":
    main()
