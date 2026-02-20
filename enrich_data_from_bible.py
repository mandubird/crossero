#!/usr/bin/env python3
"""
BIBLE.csv(개역한글)에서 책별 단어를 추출해 data.js 퀴즈의 allWords를 보강합니다.
- 풍성한 퍼즐을 위해 각 퀴즈의 title에서 책 이름을 추출하고, 해당 책 말씀에서 2~4글자 단어를 뽑아 추가합니다.
- 사용: python3 enrich_data_from_bible.py [BIBLE.csv 경로]
- 기본 BIBLE.csv 경로: 프로젝트 상위 폴더의 BIBLE.csv
"""
import os
import re
import csv
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_JS = os.path.join(SCRIPT_DIR, 'data.js')
# BIBLE.csv 기본 경로 (data.js와 같은 www 폴더)
DEFAULT_BIBLE_CSV = os.path.join(SCRIPT_DIR, 'BIBLE.csv')

# 책 이름 매핑 (data.js title에 나오는 형태 ↔ CSV 책명)
BOOK_NAME_ALIASES = {
    "창세기": "창세기", "출애굽기": "출애굽기", "레위기": "레위기", "민수기": "민수기", "신명기": "신명기",
    "여호수아": "여호수아", "사사기": "사사기", "룻기": "룻기", "사무엘상": "사무엘상", "사무엘하": "사무엘하",
    "열왕기상": "열왕기상", "열왕기하": "열왕기하", "역대상": "역대상", "역대하": "역대하",
    "에스라": "에스라", "느헤미야": "느헤미야", "에스더": "에스더", "욥기": "욥기", "시편": "시편",
    "잠언": "잠언", "전도서": "전도서", "아가": "아가", "이사야": "이사야", "예레미야": "예레미야",
    "예레미야애가": "예레미야애가", "에스겔": "에스겔", "다니엘": "다니엘", "호세아": "호세아",
    "요엘": "요엘", "아모스": "아모스", "오바댜": "오바댜", "요나": "요나", "미가": "미가",
    "나훔": "나훔", "하박국": "하박국", "스바냐": "스바냐", "학개": "학개", "스가랴": "스가랴",
    "말라기": "말라기", "마태복음": "마태복음", "마가복음": "마가복음", "누가복음": "누가복음",
    "요한복음": "요한복음", "사도행전": "사도행전", "로마서": "로마서", "고린도전서": "고린도전서",
    "고린도후서": "고린도후서", "갈라디아서": "갈라디아서", "에베소서": "에베소서", "빌립보서": "빌립보서",
    "골로새서": "골로새서", "데살로니가전서": "데살로니가전서", "데살로니가후서": "데살로니가후서",
    "디모데전서": "디모데전서", "디모데후서": "디모데후서", "디도서": "디도서", "빌레몬": "빌레몬",
    "히브리서": "히브리서", "야고보서": "야고보서", "베드로전서": "베드로전서", "베드로후서": "베드로후서",
    "요한일서": "요한일서", "요한이서": "요한이서", "요한삼서": "요한삼서", "유다서": "유다서",
    "요한계시록": "요한계시록",
}

# 가벼운 조사/접미사 제외 (2글자 이하 또는 퀴즈에 부적합한 토큰)
SKIP_PATTERN = re.compile(
    r'^(에|을|를|이|가|은|는|의|로|으로|와|과|에서|에게|한|하다|하시|되어|되어서|그리고|그러나|하나님의|그|이|저|것|수|등|및|또한|있다|없다|있다고|있다니|있다는)$'
)


def parse_bible_csv(path):
    """BIBLE.csv 파싱: 책 이름 66개, (book_id, chapter, verse) -> BIBLETEXT."""
    book_names = [""] * 67  # 1-indexed
    verses_by_book = {}  # book_id -> list of (chapter, verse, text)

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 4:
                continue
            try:
                book = int(float(row[0]))
                chapter = int(float(row[1]))
                verse = int(float(row[2]))
                text = row[3].strip().strip('"')
            except (ValueError, IndexError):
                continue
            if book == 0 and chapter == 10 and 1 <= verse <= 66:
                book_names[verse] = text
            elif 1 <= book <= 66 and text and not text.startswith("개역한글"):
                verses_by_book.setdefault(book, []).append((chapter, verse, text))
    return book_names, verses_by_book


def extract_words_from_verses(verses, max_words_per_book=80, answer_len=(2, 5)):
    """구절 리스트에서 2~5글자 한글 단어를 추출. (answer, clue) 리스트 반환."""
    from collections import defaultdict
    word_verses = defaultdict(list)  # word -> [(c,v,text), ...]
    for c, v, text in verses:
        tokens = re.findall(r'[가-힣]{2,5}', text)
        for t in tokens:
            if len(t) < answer_len[0] or len(t) > answer_len[1]:
                continue
            if SKIP_PATTERN.match(t):
                continue
            word_verses[t].append((c, v, text[:50]))
    # 빈도 순으로 정렬해 상위 N개만, clue는 해당 단어가 나오는 첫 구절
    result = []
    for word, vlist in sorted(word_verses.items(), key=lambda x: -len(x[1]))[:max_words_per_book]:
        c, v, snippet = vlist[0]
        clue = f"말씀: {snippet}…" if len(snippet) >= 20 else snippet
        result.append({"answer": word, "clue": clue})
    return result


def get_book_from_title(title):
    """title '창세기: 천지창조' -> '창세기'."""
    if ":" in title:
        return title.split(":")[0].strip()
    for book in BOOK_NAME_ALIASES:
        if book in title:
            return book
    return None


def load_quiz_database_js(path):
    """data.js에서 QUIZ_DATABASE 블록을 파싱해 퀴즈별 id, title, allWords 반환. (간단 파싱)"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    quizzes = []
    # "  \"id\": {" 패턴으로 퀴즈 시작 찾기
    for m in re.finditer(r'\s*"([a-z0-9_]+)"\s*:\s*\{', content):
        qid = m.group(1)
        start = m.end()
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
            i += 1
        block = content[start : i - 1]
        title_m = re.search(r'title\s*:\s*"([^"]+)"', block)
        title = title_m.group(1) if title_m else ""
        all_words = []
        for wm in re.finditer(r'\{\s*clue\s*:\s*"([^"]*)"\s*,\s*answer\s*:\s*"([^"]*)"\s*\}', block):
            all_words.append({"clue": wm.group(1), "answer": wm.group(2)})
        quizzes.append({"id": qid, "title": title, "allWords": all_words, "block_start": start, "block_end": i - 1})
    return quizzes, content


def main():
    import sys
    bible_csv = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BIBLE_CSV
    if not os.path.exists(bible_csv):
        print(f"BIBLE.csv를 찾을 수 없습니다: {bible_csv}")
        print("사용: python3 enrich_data_from_bible.py /path/to/BIBLE.csv")
        return
    book_names, verses_by_book = parse_bible_csv(bible_csv)
    book_name_by_id = {i: book_names[i] for i in range(1, 67) if book_names[i]}

    # 책별 추출 단어 (책 이름 -> [ {answer, clue}, ... ])
    words_by_book = {}
    for bid, bname in book_name_by_id.items():
        verses = verses_by_book.get(bid, [])
        if not verses:
            continue
        words_by_book[bname] = extract_words_from_verses(verses, max_words_per_book=60)

    quizzes, full_content = load_quiz_database_js(DATA_JS)
    existing_answers = {}  # qid -> set of answer
    for q in quizzes:
        existing_answers[q["id"]] = {w["answer"] for w in q["allWords"]}

    # 퀴즈별로 추가할 단어 (중복 제외, 최대 15개씩)
    to_add = {}
    for q in quizzes:
        book = get_book_from_title(q["title"])
        if not book or book not in words_by_book:
            continue
        cands = words_by_book[book]
        existing = existing_answers.get(q["id"], set())
        added = []
        for w in cands:
            if w["answer"] in existing or w["answer"] in {a["answer"] for a in added}:
                continue
            added.append(w)
            if len(added) >= 15:
                break
        if added:
            to_add[q["id"]] = added

    # data.js에 삽입: 각 퀴즈 블록의 allWords 배열 안, 마지막 항목 다음에 추가
    # (원본 파일 수정이 복잡하므로, 추가할 allWords만 출력하고 사용자가 수동 병합하거나
    #  별도 병합 스크립트를 돌리게 할 수 있음. 여기서는 새 data.js를 생성하는 방식으로 함.)
    # 실제로 data.js를 직접 수정하면 9000줄이라 위험하므로, "추가용 패치" JS를 생성합니다.
    out_path = os.path.join(SCRIPT_DIR, "data_bible_extra.js")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("/** BIBLE.csv에서 추출한 추가 단어. data.js 로드 후 각 퀴즈 allWords에 concat 하세요. */\n")
        f.write("const BIBLE_EXTRA_WORDS = ")
        f.write(json.dumps(to_add, ensure_ascii=False, indent=2))
        f.write(";\n")
    total_words = sum(len(v) for v in to_add.values())
    print(f"완료: data_bible_extra.js 생성 — {len(to_add)}개 퀴즈, {total_words}개 단어 추가 (play.html에서 자동 병합)")

    # 옵션: --merge 로 data.js를 실제로 수정할지
    if "--merge" in sys.argv:
        # data.js 내 각 퀴즈 블록에서 allWords: [ ... ] 부분을 찾아 교체
        import copy
        new_content = full_content
        for q in quizzes:
            qid = q["id"]
            if qid not in to_add:
                continue
            # 이 퀴즈 블록에서 allWords: [ 까지 찾고, 그 다음 ] 직전에 새 항목 삽입
            block = full_content[q["block_start"]:q["block_end"]]
            pos = block.find("allWords: [")
            if pos == -1:
                continue
            insert_pos = q["block_start"] + pos + len("allWords: [")
            # 기존 마지막 항목 다음 위치 찾기 (마지막 }\n 다음)
            search_start = insert_pos
            depth = 0
            i = search_start
            while i < len(new_content):
                if new_content[i] == "[":
                    depth += 1
                elif new_content[i] == "]":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            end_of_array = i
            # 마지막 ] 직전에 콤마 + 새 항목들 삽입
            new_entries = ",\n      ".join(
                f'{{ clue: "{w["clue"].replace(chr(92), chr(92)+chr(92)).replace('"', '\\"')}", answer: "{w["answer"]}" }}'
                for w in to_add[qid]
            )
            if new_entries:
                insert_text = ",\n      " + new_entries
                new_content = new_content[:end_of_array] + insert_text + new_content[end_of_array:]
            # 다음 퀴즈 block_start/end가 밀리므로, 한 번에 하나씩 하지 말고 오프셋을 두고 한 번에 치환
        # merge 시 오프셋이 바뀌므로, 퀴즈를 역순으로 처리하거나 한 번에 모든 삽입 위치를 계산
        print("--merge는 현재 단순 삽입 시 오프셋 문제로 비활성화. data_bible_extra.js만 사용하세요.")


if __name__ == "__main__":
    main()
