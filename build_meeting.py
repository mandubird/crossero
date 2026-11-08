# -*- coding: utf-8 -*-
"""10분 모임 키트(/meeting/) 생성. 실행: python3 build_meeting.py
기도모임·소그룹 인도자가 폰으로 열고 읽기만 하면 되는 10분 순서. 가입·입력·개인정보 수집 없음.
말씀은 개역한글 본문(BIBLE.csv)에서 가져오고, 질문·기도문은 이 파일에서 관리한다."""
import json
import os
import re

import build_dictionary as bd
from build_dictionary import head, FOOTER, NAV, SITE, ROOT, esc
from verse_lib import KO_BOOKS, load_text

KITS = [
    dict(slug="week-1", title="시험 앞에서 마음이 무거울 때", short="시험·불안", emoji="📝",
         verses=[("빌립보서", 4, 6), ("빌립보서", 4, 7)], puzzle="phi_091", puzzle_name="빌립보서: 기쁨의 서신",
         intro="시험, 성적, 입시. 걱정이 머리에서 떠나지 않는 날이 있습니다. 오늘은 걱정을 없애려 하기보다 하나님께 '맡기는' 연습을 해 봅니다.",
         questions=["요즘 가장 마음이 무거운 일을 한 단어로 말해 볼까요? (말하기 싫으면 건너뛰어도 돼요)", "'아무것도 염려하지 말라'는 말이 쉽게 느껴지나요, 어렵게 느껴지나요? 왜 그럴까요?", "오늘 하나님께 '맡기고' 싶은 것 하나는 무엇인가요?"],
         prayer=["하나님, 오늘도 학교에서 많은 일을 견디고 왔습니다.", "시험과 성적과 앞날에 대한 걱정을 이 시간에 내려놓습니다.", "우리가 구할 것을 감사함으로 아뢰오니, 주님의 평강이 우리 마음과 생각을 지켜 주세요.", "예수님의 이름으로 기도합니다. 아멘."],
         do="이번 주 가장 걱정되는 일 하나를 종이에 적어 두고, 매일 그 위에 '맡겼어요'라고 한 번만 써 보세요."),
    dict(slug="week-2", title="우리 학교에 믿는 친구가 나 혼자일 때", short="외로움·용기", emoji="🌱",
         verses=[("디모데전서", 4, 12)], puzzle="jos_021", puzzle_name="여호수아: 요단강 도하",
         intro="믿는 친구가 별로 없는 교실에서 신앙을 드러내기는 쉽지 않습니다. 오늘은 '혼자 같지만 혼자가 아닌' 마음을 서로 나누는 시간입니다.",
         questions=["학교에서 내가 크리스천인 것을 아는 친구가 있나요? 어떤 기분이 드나요?", "'어리다고 업신여김을 받지 않게 하라'는 말씀에서 마음에 남는 단어는 무엇인가요?", "이번 주에 친구에게 작게 해 볼 수 있는 선한 행동 한 가지는 무엇일까요?"],
         prayer=["하나님, 교실에서 때로는 혼자라고 느낍니다.", "그래도 주님이 늘 함께하시고, 이렇게 함께 모인 친구들이 있음을 감사합니다.", "말과 행동과 사랑으로 작은 본이 되게 해 주시고, 담대한 마음을 주세요.", "예수님의 이름으로 기도합니다. 아멘."],
         do="이번 주에 같은 반 친구 한 명에게 '오늘 고마웠어'라고 말해 보세요. 신앙 이야기를 꺼내지 않아도 괜찮습니다."),
    dict(slug="week-3", title="기도가 잘 안 나올 때", short="기도·영적 침체", emoji="🕊️",
         verses=[("로마서", 8, 26)], puzzle="rom_087", puzzle_name="로마서: 오직 의인은 믿음으로",
         intro="기도하려고 앉았는데 할 말이 없고 마음이 멍할 때가 있습니다. 그것도 괜찮다고 성경은 말합니다. 오늘은 '잘 못하는 기도'를 그대로 드려 봅니다.",
         questions=["기도가 안 될 때는 보통 어떤 이유 때문인가요? (피곤, 딴생각, 하나님이 멀게 느껴짐 등)", "'성령이 말할 수 없는 탄식으로 간구하신다'는 말은 어떤 위로가 되나요?", "한 문장짜리 기도를 만든다면 뭐라고 할까요?"],
         prayer=["하나님, 오늘은 무슨 말을 해야 할지 잘 모르겠습니다.", "우리의 연약함을 아시는 하나님께서 우리 대신 간구해 주시니 감사합니다.", "말이 되지 않는 마음도 받아 주시고, 내일은 한 문장이라도 주님께 말할 수 있게 해 주세요.", "예수님의 이름으로 기도합니다. 아멘."],
         do="이번 주에는 잠자기 전에 '하나님, 오늘도 감사해요' 한 문장만 기도해 보세요. 길게 하지 않아도 됩니다."),
    dict(slug="week-4", title="친구 때문에 마음이 상했을 때", short="관계·상처", emoji="💛",
         verses=[("시편", 34, 18), ("골로새서", 3, 13)], puzzle="col_092", puzzle_name="골로새서: 위의 것을 찾으라",
         intro="친구와 다투거나 서운한 일이 생기면 하루 종일 마음이 무겁습니다. 오늘은 상한 마음을 숨기지 않고 하나님 앞에 내놓는 연습을 합니다.",
         questions=["최근 친구나 가족 때문에 서운했던 순간이 있었나요? (이름이나 자세한 이야기는 하지 않아도 돼요)", "'마음이 상한 자에게 가까이 하신다'는 말씀은 지금 어떻게 들리나요?", "누군가를 용서하기 어려울 때, 무엇이 필요할까요?"],
         prayer=["하나님, 마음이 상한 일들을 주님 앞에 내놓습니다.", "상한 마음에 가까이 계시는 하나님, 우리를 위로해 주세요.", "서운한 친구들을 떠올릴 때 미움이 커지지 않게 하시고, 주님이 우리를 용서하신 것처럼 우리도 용서할 힘을 주세요.", "예수님의 이름으로 기도합니다. 아멘."],
         do="이번 주에 서운했던 친구를 위해 '그 친구에게 좋은 하루가 되게 해 주세요'라고 한 번만 기도해 보세요."),
]

SAFETY = ('<div class="m-help"><b>마음이 너무 힘든 친구가 있다면</b><br>혼자 해결하려 하지 말고 믿을 수 있는 어른(부모님·선생님·교회 선생님)께 꼭 이야기하세요. '
          '지금 힘든 마음이 크다면 <a href="tel:1388">청소년전화 1388</a>, <a href="tel:109">자살예방상담전화 109</a>(24시간)에 전화할 수 있습니다.</div>')

CSS = """
.m-wrap{max-width:760px;margin:0 auto;padding:22px 16px 40px;color:#222;text-align:left}
.m-wrap h1{font-size:26px;line-height:1.4;margin:6px 0 8px;color:#0b3d73;word-break:keep-all}
.m-sub{font-size:16px;line-height:1.8;color:#445;margin:0 0 18px;word-break:keep-all}
.m-bar{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.m-bar span{background:#eef5ff;border:1px solid #cfe0f7;color:#0b3d73;border-radius:20px;padding:5px 12px;font-size:13.5px}
.m-step{border:1px solid #dbe6f3;border-radius:14px;padding:16px 18px;margin:0 0 14px;background:#fff}
.m-step h2{display:flex;align-items:center;gap:10px;font-size:19px;margin:0 0 8px;color:#0b3d73}
.m-step h2 i{font-style:normal;font-size:13px;font-weight:700;background:#0073e6;color:#fff;border-radius:14px;padding:3px 10px}
.m-step p,.m-step li{font-size:16.5px;line-height:1.85;word-break:keep-all;margin:0 0 6px}
.m-say{background:#f7faff;border-left:4px solid #8bb6ec;padding:8px 12px;border-radius:6px;margin:6px 0;font-size:16px;line-height:1.8}
.m-verse{font-family:'Noto Serif KR','Nanum Myeongjo',serif;font-size:21px;line-height:1.9;background:#fffaf0;border:1px solid #f0e2bd;border-radius:12px;padding:16px 18px;margin:6px 0 4px;word-break:keep-all}
.m-verse small{display:block;margin-top:6px;font-size:15px;color:#7a6a3a;font-family:inherit}
.m-q li{margin-bottom:10px}
.m-pray p{margin:0 0 4px}
.m-btn{display:inline-block;border:0;border-radius:12px;padding:13px 22px;font-size:16.5px;font-weight:700;cursor:pointer;text-decoration:none;font-family:inherit;margin:4px 6px 4px 0}
.m-btn.main{background:#0073e6;color:#fff}.m-btn.sub{background:#fff;color:#0b3d73;border:1px solid #bcd3f0}
.m-done{display:none;background:#eefaf0;border:1px solid #b9e3c0;border-radius:12px;padding:14px 16px;margin-top:10px;font-size:16px;line-height:1.8}
.m-help{background:#fff6f6;border:1px solid #f3cccc;border-radius:12px;padding:12px 16px;font-size:14.5px;line-height:1.8;margin:18px 0}
.m-note{font-size:13px;color:#667;line-height:1.7;margin-top:18px}
.m-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}
.m-card{display:block;border:1px solid #dbe6f3;border-radius:14px;padding:14px 16px;text-decoration:none;color:#222;background:#fff}
.m-card b{display:block;font-size:17px;color:#0b3d73;margin:4px 0}.m-card span{font-size:14px;color:#556;line-height:1.6}
.m-now{background:#0b3d73;color:#fff;border-radius:14px;padding:16px 18px;margin:0 0 16px}.m-now a{color:#ffd43b;font-weight:700}
.peek,.pg-pill,.pg-side{display:none!important}
@media(max-width:560px){.m-wrap h1{font-size:22px}.m-grid{grid-template-columns:1fr}.m-verse{font-size:19px}}
@media print{.m-btn,nav,footer,.m-done{display:none!important}.m-step{break-inside:avoid}}
"""

JS = r"""
(function(){
  function track(n,p){if(window.crsTrack)window.crsTrack(n,p||{});}
  var kit=document.body.getAttribute('data-kit');
  var btn=document.getElementById('mGather'),done=document.getElementById('mDone'),sh=document.getElementById('mShare');
  function today(){var d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();}
  if(btn){
    var key='crs_meet_'+kit,last=null;try{last=localStorage.getItem(key);}catch(e){}
    function mark(msg){btn.style.display='none';done.style.display='block';if(msg)done.innerHTML=msg;}
    if(last===today())mark('오늘 이 모임은 이미 기록되었어요. 수고했어요 🙏');
    btn.addEventListener('click',function(){
      try{localStorage.setItem(key,today());}catch(e){}
      track('meeting_gather',{kit:kit});
      fetch('https://dallyeoganora.vercel.app/api/public-config').then(function(r){return r.json();}).then(function(c){
        return fetch(c.url+'/rest/v1/rpc/onsuim_gather',{method:'POST',headers:{'Content-Type':'application/json',apikey:c.anon,Authorization:'Bearer '+c.anon},body:JSON.stringify({p_kit:kit})});
      }).then(function(r){if(!r.ok)throw new Error('rpc');return r.json();}).then(function(j){
        var n=j&&j.week_total;
        mark('오늘 모였어요 🙏'+(n?' 이번 주 <b>'+n+'개 모임</b>이 함께 기도했어요.':'')+'<br><a href="https://onsuim.vercel.app/?utm_source=crossero&utm_medium=meeting&utm_campaign=gather_done" target="_blank" rel="noopener" data-ga="onsuim_meeting_click">온쉼 마을에서 불 켜진 창문 보기 →</a>');
      }).catch(function(){mark('오늘 모였어요 🙏 수고했어요. 이 시간이 한 주를 지켜 줄 거예요.');});
    });
  }
  if(sh)sh.addEventListener('click',function(){var u=location.href.split('#')[0];track('meeting_share',{kit:kit});
    if(navigator.share){navigator.share({title:document.title,url:u}).catch(function(){});return;}
    if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){sh.textContent='✅ 링크 복사됨';});}});
  var now=document.getElementById('mNow');
  if(now){var s=new Date(2026,10,9),d=Math.floor((new Date()-s)/864e5/7);var i=((d%4)+4)%4;var a=now.querySelectorAll('[data-w]');for(var k=0;k<a.length;k++){if(+a[k].getAttribute('data-w')===i){a[k].style.display='inline';}}}
})();
"""


def verse_html(k):
    t = load_text()
    out = []
    for n, c, v in k["verses"]:
        out.append((t[(KO_BOOKS.index(n) + 1, c, v)], f"{n} {c}:{v}"))
    text = " ".join(x[0] for x in out)
    ref = out[0][1] if len(out) == 1 else f"{k['verses'][0][0]} {k['verses'][0][1]}:{k['verses'][0][2]}" + ("".join(f", {k['verses'][i][0]} {k['verses'][i][1]}:{k['verses'][i][2]}" if k['verses'][i][0] != k['verses'][0][0] else f"-{k['verses'][i][2]}" for i in range(1, len(k["verses"]))))
    parts = "".join(f"<div>{esc(x[0])}</div>" for x in out)
    return parts, ref


def kit_page(i, k):
    parts, ref = verse_html(k)
    path = f"/meeting/{k['slug']}/"
    title = f"10분 모임 키트 {i+1} - {k['title']} | 십자가로세로"
    desc = f"기도모임·소그룹 인도자를 위한 10분 순서. 말씀 {ref}, 나눔 질문, 기도 순서를 폰으로 열어 읽기만 하면 됩니다. 가입 없이 무료."
    ld = {"@context": "https://schema.org", "@type": "HowTo", "name": f"10분 모임 키트: {k['title']}", "description": desc, "totalTime": "PT10M", "inLanguage": "ko",
          "step": [{"@type": "HowToStep", "name": n, "text": t} for n, t in [("시작", "숨을 함께 세 번 고르고 오늘 모임의 주제를 소개합니다."), ("말씀", f"{ref} 말씀을 함께 읽습니다."), ("나눔", "질문 가운데 하나를 골라 한 문장씩 나눕니다."), ("기도", "함께 기도문을 읽고 아멘으로 마칩니다."), ("마무리", "이번 주 실천 한 가지를 정하고 마칩니다.")]]}
    h = head(title, desc, path, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n').replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1).replace("<body>", f'<body data-kit="{k["slug"]}">', 1)
    qs = "".join(f"<li>{esc(q)}</li>" for q in k["questions"])
    pr = "".join(f"<p>{esc(x)}</p>" for x in k["prayer"])
    body = f"""<main class="m-wrap">
<p style="margin:0"><a href="/meeting/">← 10분 모임 키트</a></p>
<h1>{k['emoji']} {esc(k['title'])}</h1>
<p class="m-sub">{esc(k['intro'])}</p>
<div class="m-bar"><span>⏱ 10분</span><span>📱 폰으로 읽기만 하면 돼요</span><span>🔒 가입·입력 없음</span></div>
<section class="m-step"><h2><i>1분</i> 시작</h2>
<div class="m-say">"오늘 하루 수고했어요. 함께 숨을 세 번만 천천히 쉬고 시작할게요."</div>
<p>숨을 고른 뒤, 이름을 한 번씩 부르거나 "오늘 기분은 날씨로 치면?"을 한 마디씩 나눠도 좋아요.</p></section>
<section class="m-step"><h2><i>2분</i> 말씀</h2>
<p>한 사람이 읽고, 다 같이 한 번 더 읽어 보세요.</p>
<div class="m-verse">{parts}<small>{esc(ref)} (개역한글)</small></div>
<p><a href="/verse/?v={esc(k['verses'][0][0])}%20{k['verses'][0][1]}:{k['verses'][0][2]}">🎨 이 말씀으로 카드 만들기</a></p></section>
<section class="m-step"><h2><i>3분</i> 나눔</h2>
<p>질문 가운데 하나만 골라 한 문장씩 나눠요. <b>말하고 싶지 않은 사람은 "패스"해도 괜찮아요.</b></p>
<ul class="m-q">{qs}</ul></section>
<section class="m-step m-pray"><h2><i>2분</i> 기도</h2>
<p>인도자가 한 줄씩 읽고, 다 같이 마지막 "아멘"을 해요. 자기 말로 한 문장씩 더해도 좋아요.</p>
<div class="m-say">{pr}</div></section>
<section class="m-step"><h2><i>1분</i> 마무리</h2>
<p><b>이번 주 한 가지:</b> {esc(k['do'])}</p>
<button class="m-btn main" id="mGather" type="button" data-ga="meeting_gather_click" data-ga-label="{k['slug']}">🙏 오늘 모였어요</button>
<button class="m-btn sub" id="mShare" type="button">🔗 이 키트 나누기</button>
<div class="m-done" id="mDone"></div></section>
<section class="m-step"><h2><i>선택 3분</i> 미니 퍼즐</h2>
<p>어색할 때는 퍼즐로 시작해 보세요. 폰 하나로 같이 보며 풀어요.</p>
<a class="m-btn sub" href="/play.html?id={k['puzzle']}" data-ga="meeting_puzzle" data-ga-label="{k['slug']}">🧩 {esc(k['puzzle_name'])} 풀기</a></section>
{SAFETY}
<p class="m-note">이 키트는 예배나 교회 공동체 활동을 대신하지 않고, 학교·소모임에서 짧게 말씀 앞에 서도록 돕는 자료입니다. 이름·학교·연락처를 입력받지 않습니다. 성경 본문은 개역한글판(대한성서공회)을 사용했습니다. 기도문과 질문은 십자가로세로가 직접 작성했습니다.</p>
<p><a href="/meeting/">다른 주 키트 보기</a> · <a href="/quiet/">🌿 1분 쉼 묵상</a> · <a href="/today/">📅 오늘의 말씀</a></p>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def hub_page():
    path = "/meeting/"
    title = "10분 모임 키트 - 학교·소그룹 기도모임 인도자를 위한 무료 순서 | 십자가로세로"
    desc = "학교 기도모임, 청소년부·청년부 소그룹, 교사 모임에서 폰 하나로 10분이면 진행하는 모임 순서입니다. 말씀 한 구절, 나눔 질문, 기도 순서를 매주 새로 제공합니다. 가입 없이 무료."
    faq = [("10분 모임 키트가 무엇인가요?", "말씀 한 구절과 나눔 질문, 기도 순서가 한 페이지에 담긴 모임용 자료입니다. 인도자가 폰으로 열어 읽기만 하면 10분 안에 모임을 진행할 수 있습니다."),
           ("가입이나 개인정보 입력이 필요한가요?", "필요 없습니다. 이름, 학교, 연락처를 받지 않습니다."),
           ("신앙이 깊지 않아도 인도할 수 있나요?", "네. 인도자가 읽을 문장과 질문이 모두 적혀 있어서 읽기만 해도 모임이 진행됩니다."),
           ("비용이 드나요?", "무료입니다. 출처 표기(십자가로세로)를 하면 모임 자료로 자유롭게 사용하실 수 있습니다.")]
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "10분 모임 키트", "url": SITE + path, "description": desc, "inLanguage": "ko"},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    h = head(title, desc, path, "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1).replace("<body>", '<body data-kit="hub">', 1)
    now_links = "".join(f'<a data-w="{i}" href="/meeting/{k["slug"]}/" style="display:none">{k["emoji"]} {esc(k["title"])} →</a>' for i, k in enumerate(KITS))
    cards = "".join(f'<a class="m-card" href="/meeting/{k["slug"]}/"><span>{k["emoji"]} {i+1}주차 · {esc(k["short"])}</span><b>{esc(k["title"])}</b><span>{esc(k["verses"][0][0])} {k["verses"][0][1]}:{k["verses"][0][2]}</span></a>' for i, k in enumerate(KITS))
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    body = f"""<main class="m-wrap">
<h1>🕯️ 10분 모임 키트</h1>
<p class="m-sub">학교 기도모임, 청소년부·청년부 소그룹, 교사 모임에서 <b>폰 하나로 10분</b>이면 진행할 수 있는 순서입니다. 말씀 한 구절, 나눔 질문, 기도 순서가 한 페이지에 들어 있어요. 신앙이 깊지 않아도 읽기만 하면 인도할 수 있습니다.</p>
<div class="m-bar"><span>⏱ 10분</span><span>🔒 가입·입력 없음</span><span>🆓 무료</span></div>
<div class="m-now" id="mNow"><b>이번 주 키트</b><br>{now_links}</div>
<h2 style="font-size:19px;color:#0b3d73">4주 키트</h2>
<div class="m-grid">{cards}</div>
<h2 style="font-size:19px;color:#0b3d73">이렇게 진행해요</h2>
<ol style="font-size:16.5px;line-height:1.9"><li>모일 친구들에게 키트 링크를 보내요. (키트 페이지의 "나누기" 버튼)</li><li>시작 1분 · 말씀 2분 · 나눔 3분 · 기도 2분 · 마무리 1분 순서로 읽어 가요.</li><li>마치면 "오늘 모였어요"를 눌러요. 누른 모임 수만 합산되고, 학교 이름이나 사람은 기록되지 않아요.</li></ol>
{SAFETY}
<h2 style="font-size:19px;color:#0b3d73">자주 묻는 질문</h2><div class="faq">{faq_html}</div>
<p class="m-note">예배나 교회 공동체 활동을 대신하지 않습니다. 이 키트는 십자가로세로가 직접 작성했으며, 모임 자료로 출처(십자가로세로)를 밝히면 자유롭게 사용하실 수 있습니다. 성경 본문은 개역한글판(대한성서공회)입니다.</p>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "<script>" + JS + "</script>", "</body>\n</html>\n"])


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- MEETING-START -->.*?<!-- MEETING-END -->", "", s, flags=re.S)
    urls = ["/meeting/"] + [f"/meeting/{k['slug']}/" for k in KITS]
    block = "\n  <!-- MEETING-START -->\n" + "".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.6</priority>\n  </url>\n" for u in urls) + "  <!-- MEETING-END -->\n"
    open(p, "w", encoding="utf-8").write(s.replace("</urlset>", block + "</urlset>"))


def main():
    d = os.path.join(ROOT, "meeting")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(hub_page())
    for i, k in enumerate(KITS):
        os.makedirs(os.path.join(d, k["slug"]), exist_ok=True)
        open(os.path.join(d, k["slug"], "index.html"), "w", encoding="utf-8").write(kit_page(i, k))
    update_sitemap()
    print("모임 키트 생성:", len(KITS), "개 + 허브")


if __name__ == "__main__":
    main()
