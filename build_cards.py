# -*- coding: utf-8 -*-
"""말씀 카드 갤러리(/cards/) 생성. 실행: python3 build_cards.py   (먼저 cards_plan.py, tools/gen_cards.js 로 이미지를 만든다)
출력: cards/index.html, cards/<세트>/index.html, sitemap.xml 의 CARDS 구간(이미지 사이트맵 포함)"""
import json
import os
import re
import urllib.parse

import build_dictionary as bd
import build_verse as bv
from build_dictionary import esc, head, FOOTER, NAV, SITE, ROOT
from cards_plan import SETS

PLAN = json.load(open("cards_plan.json", encoding="utf-8"))
PH = {p["id"]: p for p in json.load(open("verse/studio_photos.json", encoding="utf-8"))["photos"]}
PHT = json.load(open("verse/studio_photos.json", encoding="utf-8"))["themes"]
SCN = {"wc": "수채화", "ink": "수묵 산수", "hanji": "한지", "marble": "대리석", "gold": "별빛과 금빛", "bokeh": "빛망울", "linen": "리넨",
       "dawn": "새벽 노을", "mist": "안개 숲", "pastel": "파스텔 구름", "parchment": "고서 양피지", "stained": "스테인드글라스"}

CSS = bv.CSS + """
.cgw{max-width:var(--w-wide,1100px);margin:0 auto;padding:26px 20px 14px;text-align:left;color:#222}
.cgw h1{font-size:28px;line-height:1.4;margin:10px 0 6px}.cgw h2{font-size:21px;margin:32px 0 10px;color:#0b3d73}
.cgw p,.cgw li{font-size:16.5px;line-height:1.95;word-break:keep-all}.cgw p{margin:0 0 12px}
.cgw .txt{max-width:var(--w-col,780px)}
.cgw .lead{font-size:17.5px;color:#334}
.cg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;margin:16px 0}
.cg figure{margin:0;background:#fff;border:1px solid #e3eaf3;border-radius:14px;overflow:hidden;box-shadow:0 3px 10px rgba(0,0,0,.05)}
.cg figure a.im{display:block;background:#e9eef5;aspect-ratio:4/5}
.cg img{width:100%;height:100%;object-fit:cover;display:block}
.cg figcaption{padding:10px 12px 12px;font-size:13.5px;line-height:1.65;color:#445}
.cg figcaption b{display:block;color:#0b3d73;font-size:14.5px}
.cg figcaption small{display:block;color:#889;font-size:11.5px;margin-top:4px;line-height:1.5}
.cg .acts{display:flex;gap:6px;margin-top:8px}.cg .acts a{flex:1;text-align:center;padding:7px 4px;border-radius:9px;font-size:12.5px;text-decoration:none;border:1px solid #bcd3f0;color:#0b5cad;background:#fff}
.cg .acts a.p{background:#0073e6;border-color:#0073e6;color:#fff;font-weight:700}
.cgw .hubg{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin:16px 0}
.cgw .hubg a{display:block;text-decoration:none;color:#0b3d73;border:1px solid #d6e4f7;border-radius:14px;overflow:hidden;background:#fff}
.cgw .hubg img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}.cgw .hubg b{display:block;padding:10px 12px 2px;font-size:16px}.cgw .hubg span{display:block;padding:0 12px 12px;font-size:13px;color:#667}
.cgw .box{background:#f4f8ff;border:1px solid #cfe0f5;border-radius:14px;padding:14px 18px;margin:16px 0}
.cgw .btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}.cgw .btnrow a{display:inline-block;padding:13px 20px;border-radius:12px;background:#0073e6;color:#fff;text-decoration:none;font-weight:700;font-size:15.5px}.cgw .btnrow a.alt{background:#fff;color:#0b5cad;border:1px solid #bcd3f0}
@media(max-width:560px){.cg{grid-template-columns:repeat(2,1fr);gap:10px}.cg figcaption{padding:8px 9px 10px;font-size:12.5px}.cg .acts{flex-direction:column}}
"""

TXT = {
    "new-year": dict(
        h1="새해 말씀 카드 - 2027 새해 성경 구절 이미지 모음",
        desc="2027 새해에 카카오톡·인스타그램으로 나누고 교회에서 인쇄할 수 있는 새해 말씀 카드 이미지 36장. 고급 배경과 글꼴로 만든 무료 샘플을 보고 같은 디자인으로 바로 만들어 보세요.",
        intro=["새해가 되면 한 해를 붙들 말씀 한 구절을 정하고, 가족과 교회 공동체에 카드로 나누는 일이 널리 이어져 왔습니다. 이 모음은 이사야 43장 19절, 예레미야애가 3장 23절, 빌립보서 3장 14절처럼 새로운 시작과 인도하심, 소망을 담은 구절을 골라 사진과 수묵, 별빛 같은 배경 위에 담은 샘플 카드입니다.",
               "카드를 누르면 같은 디자인이 말씀 카드 스튜디오에서 열려, 글꼴과 배경, 장식을 바꾸고 원하는 크기로 저장할 수 있습니다. 송구영신예배의 말씀 상자 카드는 한꺼번에 인쇄하는 기능도 있습니다."],
        tips=["카카오톡 새해 인사 이미지, 프로필, 휴대폰 배경화면으로 저장해 쓸 수 있습니다.", "교회 주보, 소그룹 새해 모임, 가정예배 카드로 인쇄해 나눌 수 있습니다.", "송구영신예배에서 말씀 상자 카드로 쓰려면 새해 말씀 뽑기 인쇄 도구를 이용하세요."],
        faq=[("새해 말씀 카드는 무료인가요?", "네, 카드 만들기와 이미지 저장은 무료입니다. 후원하시면 이미지의 작은 워터마크를 뺄 수 있습니다."), ("어떤 크기로 저장되나요?", "이 갤러리의 샘플은 1080×1350(인스타 4:5)입니다. 스튜디오에서는 카톡 정사각, 휴대폰 배경화면, A4 인쇄 등 12가지 크기로 저장할 수 있습니다."), ("교회에서 인쇄해 나눠도 되나요?", "교회·주일학교·가정에서의 비영리 사용은 자유롭게 하실 수 있습니다. 판매용으로는 이용하실 수 없습니다.")]),
    "christmas": dict(
        h1="성탄 말씀 카드 - 크리스마스 성경 구절 이미지 모음",
        desc="성탄절에 나눌 수 있는 크리스마스 성경 구절 카드 24장. 별빛과 금빛, 스테인드글라스, 눈 내리는 배경으로 만든 무료 성탄 말씀 이미지를 카톡·인스타·교회 인쇄용으로 사용하세요.",
        intro=["성탄절은 하나님이 사람이 되어 우리에게 오신 날을 기념하는 절기입니다. 이 모음은 누가복음 2장의 천사의 소식, 이사야 9장의 예언, 요한복음 1장 14절처럼 성탄 이야기에 나오는 구절을 별빛과 금빛, 스테인드글라스 같은 배경 위에 담았습니다.",
               "성탄 카드, 교회 성탄 예배 순서지, 주일학교 성탄 행사, 카카오톡 성탄 인사 이미지로 활용해 보세요. 카드를 눌러 같은 디자인을 직접 고쳐 만들 수도 있습니다."],
        tips=["성탄 카드와 선물 포장에 붙이는 작은 카드로 인쇄해 쓸 수 있습니다.", "교회 성탄 예배 주보 표지나 슬라이드 배경으로 활용할 수 있습니다.", "성탄 성극 대본과 소품 도안, 성탄 퍼즐도 함께 준비해 보세요."],
        faq=[("성탄절 성경 구절은 어디에 있나요?", "주로 누가복음 1~2장과 마태복음 1~2장에 있고, 이사야 7장과 9장, 미가 5장의 예언이 함께 인용됩니다."), ("카드를 인쇄해도 되나요?", "교회와 주일학교, 가정에서의 비영리 인쇄는 자유롭게 하실 수 있습니다."), ("배경을 바꿀 수 있나요?", "카드를 눌러 스튜디오에서 사진·질감·글꼴·장식을 바꿀 수 있습니다.")]),
    "thanksgiving": dict(
        h1="추수감사 말씀 카드 - 감사 성경 구절 이미지 모음",
        desc="추수감사절과 감사 예배에 쓰는 성경 구절 카드 24장. 황금빛 들판과 가을 풍경, 한지와 리넨 질감으로 만든 무료 추수감사 말씀 이미지를 카톡과 교회 인쇄에 활용하세요.",
        intro=["추수감사절은 한 해 동안 베풀어 주신 은혜에 감사하는 절기로, 많은 교회가 11월에 감사 예배를 드립니다. 이 모음은 시편 100편, 데살로니가전서 5장 18절 같은 감사의 말씀을 황금빛 들판과 가을 풍경 위에 담았습니다.",
               "감사 예배 순서지, 감사 카드, 교인들에게 보내는 감사 인사 이미지로 활용해 보세요."],
        tips=["성도들에게 감사 카드로 한 장씩 인쇄해 나눠 줄 수 있습니다.", "감사 예배 슬라이드 배경과 주보 표지에 활용할 수 있습니다.", "감사 제목 쓰기 활동지와 함께 쓰면 좋습니다."],
        faq=[("추수감사절은 언제인가요?", "교회마다 다르지만 많은 한국 교회가 11월에 지킵니다."), ("감사 구절은 어떻게 고르나요?", "시편의 감사 시와 바울 서신의 감사 권면이 많이 쓰입니다."), ("무료로 쓸 수 있나요?", "네, 비영리 사용은 자유롭고 이미지 저장은 무료입니다.")]),
    "comfort": dict(
        h1="위로의 말씀 카드 - 힘이 되는 성경 구절 이미지 모음",
        desc="지치고 힘든 사람에게 보내는 위로의 성경 구절 카드 24장. 고요한 호수와 안개 숲, 수채화 배경으로 만든 무료 위로 말씀 이미지를 카톡으로 보내거나 인쇄해 건네세요.",
        intro=["마음이 무겁고 지칠 때 한 구절의 말씀이 큰 위로가 됩니다. 이 모음은 시편 23편, 이사야 41장 10절, 마태복음 11장 28절 같은 위로와 쉼의 말씀을 고요한 호수와 안개 낀 숲 같은 배경에 담았습니다.",
               "아픈 사람과 슬픔 중에 있는 이웃에게 카카오톡으로 보내거나 작은 카드로 인쇄해 전해 보세요. 말씀과 함께 짧은 안부 한 줄을 곁들이면 더 따뜻합니다."],
        tips=["병문안 카드나 위로 문자의 첨부 이미지로 쓸 수 있습니다.", "구역 모임에서 서로를 위한 말씀 카드로 나눌 수 있습니다.", "스스로를 위해 휴대폰 배경화면으로 저장해 두어도 좋습니다."],
        faq=[("위로의 말씀은 어떤 것이 있나요?", "시편 23편, 46편, 이사야 41장 10절, 마태복음 11장 28절 등이 많이 읽힙니다."), ("카드를 보낼 때 주의할 점이 있나요?", "상대의 상황을 존중해 짧은 안부와 함께 보내는 것을 권합니다."), ("이미지를 수정할 수 있나요?", "카드를 눌러 스튜디오에서 글꼴과 배경을 바꿀 수 있습니다.")]),
    "peace": dict(
        h1="평안의 말씀 카드 - 마음이 쉬는 성경 구절 이미지 모음",
        desc="불안한 마음에 평안을 주는 성경 구절 카드 19장. 잔잔한 물과 파스텔 구름, 한지 배경으로 만든 무료 평안 말씀 이미지를 휴대폰 배경화면과 카톡 공유에 활용하세요.",
        intro=["평안은 환경이 고요해서가 아니라 하나님께 맡기는 마음에서 시작된다고 성경은 말합니다. 이 모음은 빌립보서 4장 6~7절, 요한복음 14장 27절 같은 평안의 말씀을 잔잔한 물과 파스텔 구름 위에 담았습니다.",
               "불안한 하루를 시작하는 아침에 휴대폰 배경화면으로 저장해 두거나, 시험과 수술을 앞둔 가족에게 응원 카드로 보낼 수 있습니다."],
        tips=["휴대폰 잠금 화면 배경으로 저장해 하루 여러 번 보세요.", "시험, 면접, 수술을 앞둔 사람에게 응원 카드로 보낼 수 있습니다.", "잠들기 전 한 구절을 천천히 읽는 묵상 카드로 활용해 보세요."],
        faq=[("평안의 말씀으로 가장 많이 읽히는 구절은?", "빌립보서 4장 6~7절과 요한복음 14장 27절이 대표적입니다."), ("휴대폰 배경화면 크기로 저장되나요?", "스튜디오에서 휴대폰 배경화면 크기를 고르면 됩니다."), ("무료인가요?", "네, 무료입니다.")]),
    "courage": dict(
        h1="용기의 말씀 카드 - 담대함을 주는 성경 구절 이미지 모음",
        desc="두려움 앞에서 담대함을 주는 성경 구절 카드 24장. 웅장한 산과 빛내림, 수묵과 금빛 배경으로 만든 무료 용기 말씀 이미지를 응원 메시지와 인쇄에 활용하세요.",
        intro=["두려운 일 앞에서 성경은 담대하라고 거듭 말합니다. 이 모음은 여호수아 1장 9절, 이사야 41장 10절, 시편 27편 1절처럼 용기를 주는 말씀을 웅장한 산과 빛이 내리는 풍경에 담았습니다.",
               "새로운 도전을 앞둔 청년과 학생, 어려운 결정을 앞둔 가족에게 응원의 카드로 보내 보세요."],
        tips=["수험생과 취업 준비생에게 응원 카드로 보낼 수 있습니다.", "새로운 사역과 이사, 이직을 앞둔 사람에게 카드로 전할 수 있습니다.", "청소년부 모임의 말씀 카드로 인쇄해 활용할 수 있습니다."],
        faq=[("용기를 주는 대표 구절은?", "여호수아 1장 9절, 이사야 41장 10절, 시편 27편 1절이 많이 쓰입니다."), ("응원 카드로 보내도 되나요?", "비영리 개인 사용은 자유롭게 하실 수 있습니다."), ("글꼴을 바꾸고 싶어요.", "스튜디오에서 40여 종 글꼴 중 고를 수 있습니다.")]),
    "gratitude": dict(
        h1="감사의 말씀 카드 - 감사 성경 구절 이미지 모음",
        desc="일상의 감사를 나누는 성경 구절 카드 21장. 봄꽃과 황금빛 들판, 수채화 배경으로 만든 무료 감사 말씀 이미지를 감사 인사와 교회 행사에 활용하세요.",
        intro=["감사는 하나님이 하신 일을 기억하는 데서 시작됩니다. 이 모음은 시편과 바울 서신의 감사 구절을 봄꽃과 황금빛 들판, 수채화 배경에 담았습니다.",
               "스승의 날, 어버이날, 교회 직분자 감사 행사, 일상의 감사 인사에 카드로 활용해 보세요."],
        tips=["감사 인사 문자의 첨부 이미지로 보낼 수 있습니다.", "교회 감사 행사 카드로 인쇄할 수 있습니다.", "감사 일기 첫 장에 말씀 카드를 붙여 시작해 보세요."],
        faq=[("감사의 말씀으로 많이 쓰이는 구절은?", "시편 100편, 데살로니가전서 5장 18절, 골로새서 3장 15~17절이 많이 쓰입니다."), ("무료로 쓸 수 있나요?", "네, 비영리 사용은 자유롭습니다."), ("글씨를 크게 할 수 있나요?", "스튜디오의 글자 크기 슬라이더로 조절할 수 있습니다.")]),
    "hope": dict(
        h1="소망의 말씀 카드 - 희망을 주는 성경 구절 이미지 모음",
        desc="낙심한 마음에 소망을 주는 성경 구절 카드 20장. 일출과 노을, 빛내림 배경으로 만든 무료 소망 말씀 이미지를 새로운 시작을 응원하는 카드와 배경화면에 활용하세요.",
        intro=["어둠 속에서도 새벽은 옵니다. 이 모음은 예레미야 29장 11절, 로마서 15장 13절 같은 소망의 말씀을 일출과 노을, 빛이 내리는 하늘 위에 담았습니다.",
               "새로운 시작을 앞둔 사람, 낙심한 이웃에게 소망의 카드로 전해 보세요."],
        tips=["새해와 새 학기, 새 직장을 시작하는 사람에게 보낼 수 있습니다.", "병상의 환우를 위한 소망 카드로 인쇄할 수 있습니다.", "휴대폰 배경화면으로 저장해 두세요."],
        faq=[("소망의 말씀은 어떤 것이 있나요?", "예레미야 29장 11절, 로마서 15장 13절, 이사야 40장 31절 등이 많이 쓰입니다."), ("카드는 무료인가요?", "네, 무료입니다."), ("다른 배경으로 바꿀 수 있나요?", "스튜디오에서 사진 270장과 질감 배경 중 고를 수 있습니다.")]),
    "love": dict(
        h1="사랑의 말씀 카드 - 사랑 성경 구절 이미지 모음",
        desc="사랑을 전하는 성경 구절 카드 24장. 꽃과 수채화, 대리석과 빛망울 배경으로 만든 무료 사랑 말씀 이미지를 결혼식, 기념일, 가족 카드에 활용하세요.",
        intro=["성경은 사랑을 하나님의 성품이자 가장 큰 계명으로 소개합니다. 이 모음은 고린도전서 13장, 요한일서 4장의 사랑의 말씀을 꽃과 수채화 같은 따뜻한 배경에 담았습니다.",
               "결혼식 청첩장, 기념일 카드, 부모님께 드리는 감사 카드로 활용해 보세요."],
        tips=["결혼식 축하 카드와 청첩장 이미지로 활용할 수 있습니다.", "부모님과 가족에게 보내는 카드로 인쇄할 수 있습니다.", "교회 사랑의 모임 카드로 사용할 수 있습니다."],
        faq=[("사랑장이란 무엇인가요?", "고린도전서 13장을 사랑장이라 부르며 결혼식에서 자주 읽습니다."), ("글꼴을 바꿀 수 있나요?", "네, 스튜디오에서 40여 종 글꼴을 고를 수 있습니다."), ("무료인가요?", "네, 무료입니다.")]),
    "faith": dict(
        h1="믿음의 말씀 카드 - 믿음 성경 구절 이미지 모음",
        desc="믿음을 붙드는 성경 구절 카드 22장. 산과 빛내림, 별빛과 금빛, 수묵 배경으로 만든 무료 믿음 말씀 이미지를 소그룹과 교회 행사에 활용하세요.",
        intro=["믿음은 바라는 것들의 실상이라고 성경은 말합니다. 이 모음은 히브리서 11장, 잠언 3장 5~6절 같은 믿음의 말씀을 산과 빛내림, 별빛 배경에 담았습니다.",
               "교회 새신자 환영 카드, 세례 기념 카드, 소그룹 말씀 카드로 활용해 보세요."],
        tips=["세례와 입교 기념 카드로 인쇄할 수 있습니다.", "새신자 환영 카드로 건넬 수 있습니다.", "구역 모임에서 한 달의 말씀 카드로 나눌 수 있습니다."],
        faq=[("믿음의 말씀은 어떤 것이 있나요?", "히브리서 11장 1절, 잠언 3장 5~6절, 로마서 10장 17절이 많이 쓰입니다."), ("인쇄 크기는?", "스튜디오에서 A4·A5·A6 인쇄 크기를 고를 수 있습니다."), ("무료인가요?", "네, 무료입니다.")]),
}


def deep_link(c):
    d = c["design"]
    q = [("v", c["ref"])]
    bg = d["bg"]
    q.append(("b", f"photo:{bg['id']}" if bg["type"] == "photo" else f"scene:{bg['k']}:{bg['seed']}"))
    q.append(("f", d["font"]))
    if d.get("orn", "none") != "none":
        q.append(("o", d["orn"]))
    if d.get("frame", "none") != "none":
        q.append(("fr", d["frame"]))
    if d.get("fx", "none") != "none":
        q.append(("fx", d["fx"]))
    q.append(("dm", str(d["dim"])))
    if d.get("dcolor", "text") != "text":
        q.append(("dc", d["dcolor"]))
    return "/verse/?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)


def bgdesc(c):
    bg = c["design"]["bg"]
    return PHT.get(PH[bg["id"]]["theme"], "풍경") + " 사진" if bg["type"] == "photo" else SCN.get(bg["k"], "질감") + " 배경"


def credit(c):
    bg = c["design"]["bg"]
    if bg["type"] != "photo":
        return ""
    p = PH[bg["id"]]
    return f"사진: {p['artist']} · {p['lic']} · Wikimedia Commons"


def imgfile(c):
    return f"/images/cards/{c['file']}"


def lic_url(c):
    bg = c["design"]["bg"]
    return (PH[bg["id"]]["licurl"] or "https://commons.wikimedia.org") if bg["type"] == "photo" else ""


def set_page(S):
    cards = [c for c in PLAN if c["set"] == S["k"] and os.path.exists(imgfile(c)[1:])]
    T = TXT[S["k"]]
    path = f"/cards/{S['k']}/"
    url = SITE + path
    imgs = []
    for c in cards:
        o = {"@type": "ImageObject", "contentUrl": SITE + imgfile(c), "thumbnailUrl": SITE + imgfile(c).replace(".jpg", "_t.jpg"),
             "name": f"{c['ref']} 말씀 카드", "caption": c["text"], "width": 1080, "height": 1350, "encodingFormat": "image/jpeg",
             "creator": {"@type": "Organization", "name": "십자가로세로"}, "acquireLicensePage": SITE + "/cards/"}
        if credit(c):
            o["creditText"] = credit(c)
            o["license"] = lic_url(c)
        imgs.append(o)
    ld = [{"@context": "https://schema.org", "@type": "ImageGallery", "name": T["h1"], "description": T["desc"], "url": url, "inLanguage": "ko", "image": imgs},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faq"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "말씀 카드 갤러리", "item": SITE + "/cards/"},
              {"@type": "ListItem", "position": 3, "name": S["name"], "item": url}]}]
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    title = f"{T['h1']} | 십자가로세로"
    h = head(title, T["desc"], path, ldh, SITE + imgfile(cards[0])).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    figs = ""
    for c in cards:
        alt = f"{c['ref']} 말씀 카드 - {c['text'][:34]}… ({S['name']}, {bgdesc(c)})"
        cr = credit(c)
        figs += (f'<figure><a class="im" href="{deep_link(c)}" data-ga="cards_open" data-ga-label="{esc(c["file"])}">'
                 f'<img src="{imgfile(c).replace(".jpg", "_t.jpg")}" srcset="{imgfile(c).replace(".jpg", "_t.jpg")} 360w, {imgfile(c)} 1080w" sizes="(max-width:560px) 46vw, 240px" width="360" height="450" loading="lazy" alt="{esc(alt)}"></a>'
                 f'<figcaption><b>{esc(c["ref"])}</b>{esc(c["text"])}'
                 + (f'<small>{esc(cr)}</small>' if cr else '') +
                 f'<div class="acts"><a class="p" href="{deep_link(c)}" data-ga="cards_make">만들기</a><a href="{imgfile(c)}" download data-ga="cards_dl">이미지 저장</a></div></figcaption></figure>')
    others = "".join(f'<a href="/cards/{x["k"]}/">{esc(x["name"])}</a> · ' for x in SETS if x["k"] != S["k"]).rstrip(" ·")
    body = f"""<main class="cgw">
<div class="crumb"><a href="/">홈</a> › <a href="/cards/">말씀 카드 갤러리</a> › {esc(S['name'])}</div>
<span class="badge">무료 말씀 카드 {len(cards)}장</span>
<h1>{esc(T['h1'])}</h1>
<div class="txt">{''.join(f'<p class="{"lead" if i == 0 else ""}">{esc(p)}</p>' for i, p in enumerate(T['intro']))}</div>
<div class="btnrow"><a href="/verse/" data-ga="cards_to_studio">🎨 내 말씀 카드 직접 만들기</a><a class="alt" href="/verse/new-year/guide/" data-ga="cards_to_guide">⛪ 교회 인쇄 가이드</a></div>
<div class="cg">{figs}</div>
<h2>이 카드는 이렇게 쓰세요</h2>
<ul class="txt">{''.join(f'<li>{esc(t)}</li>' for t in T['tips'])}</ul>
<h2>자주 묻는 질문</h2>
<div class="faq txt">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in T['faq'])}</div>
<h2>다른 말씀 카드 모음</h2>
<p class="txt">{others}</p>
<div class="box txt"><b>사진 출처와 이용 안내</b><p style="margin-top:6px;font-size:14px">카드의 배경 사진은 위키미디어 커먼즈의 자유 이용 사진(CC BY, CC BY-SA, CC0, 퍼블릭 도메인)이며, 촬영자와 라이선스를 각 카드 아래와 이미지 안에 표시했습니다. CC BY-SA 사진으로 만든 카드는 같은 조건으로 공유됩니다. 수채화·수묵·한지 같은 질감 배경과 장식은 십자가로세로가 직접 그린 도안입니다. 성경 본문은 개역한글판을 사용했으며, 교회·가정에서의 비영리 사용은 자유롭고 판매는 허용되지 않습니다.</p></div>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"]), cards


def hub_page(sets):
    path = "/cards/"
    n = sum(len(c) for _, c in sets)
    title = "말씀 카드 갤러리 - 새해·성탄·위로 성경 구절 이미지 무료 모음 | 십자가로세로"
    desc = f"새해 말씀 카드, 성탄 말씀 카드, 위로·평안·용기·감사 성경 구절 이미지 {n}장을 한곳에 모았습니다. 고급 배경과 글꼴로 만든 무료 샘플을 보고 같은 디자인으로 직접 만들어 카톡·인스타·교회 인쇄에 쓰세요."
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "말씀 카드 갤러리", "url": SITE + path, "inLanguage": "ko",
           "hasPart": [{"@type": "ImageGallery", "name": S["name"], "url": f"{SITE}/cards/{S['k']}/"} for S, _ in sets]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "말씀 카드 갤러리", "item": SITE + path}]}]
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    first = sets[0][1][0]
    h = head(title, desc, path, ldh, SITE + imgfile(first)).replace(NAV, NAV.replace(" nav-active", ""))
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    tiles = "".join(f'<a href="/cards/{S["k"]}/" data-ga="cards_hub_set"><img src="{imgfile(c[0]).replace(".jpg", "_t.jpg")}" width="360" height="450" loading="lazy" alt="{esc(S["name"])} 대표 이미지 - {esc(c[0]["ref"])}"><b>{esc(S["name"])}</b><span>{len(c)}장 · {esc(TXT[S["k"]]["desc"][:30])}…</span></a>' for S, c in sets)
    body = f"""<main class="cgw">
<div class="crumb"><a href="/">홈</a> › 말씀 카드 갤러리</div>
<span class="badge">무료 · 총 {n}장</span>
<h1>말씀 카드 갤러리</h1>
<div class="txt"><p class="lead">새해와 성탄, 위로와 평안처럼 마음에 필요한 주제별로 성경 구절을 카드 이미지로 모았습니다. 고급스러운 사진과 질감 배경, 단정한 글꼴로 만든 샘플을 둘러보고, 마음에 드는 카드를 누르면 같은 디자인이 스튜디오에서 열려 글꼴과 배경을 바꿔 나만의 카드로 만들 수 있습니다.</p>
<p>카카오톡과 인스타그램 공유, 휴대폰 배경화면, 프로필, 교회 주보와 말씀 상자 인쇄까지 한 곳에서 해결할 수 있습니다. 모든 이미지는 무료이며 교회·가정에서의 비영리 사용은 자유롭습니다.</p></div>
<div class="hubg">{tiles}</div>
<div class="btnrow"><a href="/verse/" data-ga="cardshub_to_studio">🎨 말씀 카드 직접 만들기</a><a class="alt" href="/verse/new-year/" data-ga="cardshub_to_newyear">🎍 새해 말씀 뽑기</a></div>
<h2>자주 묻는 질문</h2>
<div class="faq txt"><details><summary>말씀 카드는 어떻게 만드나요?</summary><p>스튜디오에서 구절을 고르거나 말씀 뽑기로 뽑은 뒤 용도(카톡, 배경화면, 인쇄 등)와 배경, 글꼴, 장식을 고르고 이미지로 저장하면 됩니다. 갤러리의 카드를 누르면 같은 디자인으로 바로 시작할 수 있습니다.</p></details>
<details><summary>이미지 저작권은 어떻게 되나요?</summary><p>배경 사진은 위키미디어 커먼즈의 자유 이용 사진이며 촬영자와 라이선스를 이미지에 표시했습니다. 질감 배경과 장식은 직접 제작했습니다. 교회·가정의 비영리 사용은 자유롭고 판매는 허용되지 않습니다.</p></details>
<details><summary>교회에서 여러 장을 한꺼번에 인쇄할 수 있나요?</summary><p>말씀 카드 스튜디오의 '교회·모임용 카드 한꺼번에 인쇄'에서 새해·성탄·주제별 구절을 A4에 4~12장씩 인쇄할 수 있습니다.</p></details></div>
</main>"""
    return "\n".join([h, body, FOOTER, '<script src="/ga-events.js"></script><script src="/subscribe.js"></script>', "</body>\n</html>\n"])


def update_sitemap(sets):
    p = os.path.join(ROOT, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<!-- CARDS-START -->.*?<!-- CARDS-END -->", "", s, flags=re.S)
    blocks = [f"  <url>\n    <loc>{SITE}/cards/</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>"]
    for S, cards in sets:
        im = "".join(f"\n    <image:image><image:loc>{SITE}{imgfile(c)}</image:loc></image:image>" for c in cards)
        blocks.append(f"  <url>\n    <loc>{SITE}/cards/{S['k']}/</loc>\n    <lastmod>{bd.TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>{im}\n  </url>")
    s = s.replace("</urlset>", "\n  <!-- CARDS-START -->\n" + "\n".join(blocks) + "\n  <!-- CARDS-END -->\n</urlset>")
    open(p, "w", encoding="utf-8").write(s)


def main():
    sets = []
    for S in SETS:
        html, cards = set_page(S)
        d = os.path.join(ROOT, "cards", S["k"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
        sets.append((S, cards))
    open(os.path.join(ROOT, "cards", "index.html"), "w", encoding="utf-8").write(hub_page(sets))
    update_sitemap(sets)
    print("말씀 카드 갤러리:", {S["k"]: len(c) for S, c in sets})


if __name__ == "__main__":
    main()
