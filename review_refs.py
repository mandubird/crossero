# -*- coding: utf-8 -*-
"""사전 항목의 성경 구절 인용 검증: 존재 여부(장·절), 지명/인물 이름이 인용 구절에 나오는지 확인."""
import re
import sys

from build_dictionary import ENTRIES
from build_verse_index import parse
from verse_lib import KO_BOOKS, load_text

TEXT = load_text()
BIDX = {b: i + 1 for i, b in enumerate(KO_BOOKS)}
ABBR = {"창": "창세기", "출": "출애굽기", "레": "레위기", "민": "민수기", "신": "신명기", "수": "여호수아", "삿": "사사기", "룻": "룻기", "삼상": "사무엘상", "삼하": "사무엘하",
        "왕상": "열왕기상", "왕하": "열왕기하", "대상": "역대상", "대하": "역대하", "스": "에스라", "느": "느헤미야", "에": "에스더", "욥": "욥기", "시": "시편", "잠": "잠언",
        "전": "전도서", "아": "아가", "사": "이사야", "렘": "예레미야", "애": "예레미야애가", "겔": "에스겔", "단": "다니엘", "호": "호세아", "욜": "요엘", "암": "아모스",
        "옵": "오바댜", "욘": "요나", "미": "미가", "나": "나훔", "합": "하박국", "습": "스바냐", "학": "학개", "슥": "스가랴", "말": "말라기", "마": "마태복음", "막": "마가복음",
        "눅": "누가복음", "요": "요한복음", "행": "사도행전", "롬": "로마서", "고전": "고린도전서", "고후": "고린도후서", "갈": "갈라디아서", "엡": "에베소서", "빌": "빌립보서",
        "골": "골로새서", "살전": "데살로니가전서", "살후": "데살로니가후서", "딤전": "디모데전서", "딤후": "디모데후서", "딛": "디도서", "몬": "빌레몬서", "히": "히브리서",
        "약": "야고보서", "벧전": "베드로전서", "벧후": "베드로후서", "요일": "요한일서", "요이": "요한이서", "요삼": "요한삼서", "유": "유다서", "계": "요한계시록"}
INLINE = re.compile(r"(?<![가-힣])(" + "|".join(sorted(ABBR, key=len, reverse=True)) + r")\s(\d+)(?::(\d+)(?:[-–](?:(\d+):)?(\d+))?)?")


def exists(book, c, v1, c2, v2):
    b = BIDX[book]
    if v2 == 999:
        return any((b, c, v) in TEXT for v in range(1, 6))
    for cc in range(c, c2 + 1):
        lo = v1 if cc == c else 1
        hi = v2 if cc == c2 else lo
        if cc == c2 and cc == c:
            hi = v2
        if not any((b, cc, v) in TEXT for v in range(lo, max(lo, hi) + 1)):
            return False
    return True


def verse_range_text(book, c, v1, c2, v2):
    b = BIDX[book]
    out = []
    if c == c2:
        end = v1 + 40 if v2 == 999 else v2
        for v in range(v1, end + 1):
            t = TEXT.get((b, c, v))
            if t:
                out.append(t)
    else:
        for cc in range(c, c2 + 1):
            for v in range(1, 80):
                if (cc > c or v >= v1) and (cc < c2 or v <= v2):
                    t = TEXT.get((b, cc, v))
                    if t:
                        out.append(t)
    return " ".join(out)


def main():
    missing, noname, inl_bad = [], [], []
    n_ref = n_inl = 0
    for e in ENTRIES:
        # 1) 구조화된 refs
        for ref, note in e["refs"]:
            p = parse(ref)
            if not p:
                continue
            n_ref += 1
            if not exists(*p):
                missing.append((e["slug"], ref))
        # 2) 이름 포함 확인(지명/인물만, 구절 전체 합쳐서)
        if e["type"] in ("지명", "인물"):
            name_forms = {e["name"], e["name"].split("(")[0].strip()}
            alt = re.findall(r"[가-힣]{2,}", e["name"])
            texts = []
            for ref, _ in e["refs"]:
                p = parse(ref)
                if p:
                    texts.append(verse_range_text(*p))
            blob = " ".join(texts)
            blob_ns = blob.replace(" ", "")
            stem = [x[:-1] for x in alt if len(x) >= 3]  # 시내산→시내, 요단강→요단
            if blob and not any(nf and (nf in blob or nf.replace(" ", "") in blob_ns) for nf in list(name_forms) + alt + stem):
                noname.append((e["slug"], e["name"]))
        # 3) 본문 속 약식 인용
        for h, paras in e["sections"]:
            for para in paras:
                for m in INLINE.finditer(para):
                    n_inl += 1
                    book = ABBR[m.group(1)]
                    c = int(m.group(2))
                    v1 = int(m.group(3)) if m.group(3) else 1
                    c2 = int(m.group(4)) if m.group(4) else c
                    v2 = int(m.group(5)) if m.group(5) else (v1 if m.group(3) else 999)
                    if m.group(1) == "약" and not m.group(3):  # '약 38년' 같은 어림수
                        continue
                    if book in BIDX and not exists(book, c, v1, c2, v2):
                        inl_bad.append((e["slug"], m.group(0)))
    print(f"구조화 구절 {n_ref}건, 본문 약식 인용 {n_inl}건 검사")
    print("존재하지 않는 구절(구조화):", missing)
    print("존재하지 않는 구절(본문):", inl_bad)
    print(f"이름이 인용 구절에 한 번도 나오지 않는 항목({len(noname)}):", noname)


if __name__ == "__main__":
    main()
