#!/usr/bin/env python3
"""
십자가로세로 유튜브 쇼츠 B 주간 배치 생성.

posts_schedule.json 순서대로 아직 쇼츠를 안 만든 퍼즐을 N개(기본 3개) 골라
영상 + 유튜브 제목/설명(.txt)을 output/batch_YYYY-MM-DD/ 에 만든다.
이미 만든 quiz_id는 shorts_state.json 에 기록해 중복 생성을 막는다.

주말에 한 번 실행 → 이번 주 올릴 3개가 폴더에 준비됨.
YouTube 예약 발행(발행 시간 지정)은 자동화 범위 밖 — 유튜브 스튜디오에서
영상 업로드 시 '예약'으로 직접 날짜/시간만 지정하면 됨 (영상당 몇 초).

사용법:
  python3 generate_batch.py            # 기본 3개
  python3 generate_batch.py 5          # 5개 만들기
"""
import json
import os
import sys
from datetime import date

from shorts_lib import render_video, make_youtube_meta

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(HERE)
SCHEDULE_PATH = os.path.join(BASE_DIR, "posts_schedule.json")
STATE_PATH = os.path.join(HERE, "shorts_state.json")
PRIORITY_PATH = os.path.join(HERE, "priority_topics.json")
OUT_ROOT = os.path.join(HERE, "output")
FRAMES_DIR = os.path.join(HERE, "_frames")


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"used_quiz_ids": []}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_priority():
    if os.path.exists(PRIORITY_PATH):
        with open(PRIORITY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def next_candidates(count, used_ids):
    used = set(used_ids)
    candidates = []

    # 1순위: priority_topics.json (인지도 높은 성경 소재, 초기 2~3주 우선 노출)
    for qid in load_priority():
        if qid not in used and qid not in candidates:
            candidates.append(qid)
        if len(candidates) >= count:
            return candidates

    # 2순위: posts_schedule.json 순서대로 나머지 채움
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        schedule = json.load(f)
    for d in sorted(schedule.keys()):
        for qid in schedule[d]:
            if qid not in used and qid not in candidates:
                candidates.append(qid)
            if len(candidates) >= count:
                return candidates
    return candidates


def main(count):
    state = load_state()
    candidates = next_candidates(count, state["used_quiz_ids"])

    if not candidates:
        print("생성할 새 퍼즐이 없습니다 (posts_schedule.json의 모든 항목을 이미 사용함).")
        return

    batch_dir = os.path.join(OUT_ROOT, f"batch_{date.today().isoformat()}")
    os.makedirs(batch_dir, exist_ok=True)

    print(f"이번 배치: {len(candidates)}개 → {batch_dir}\n")

    for i, quiz_id in enumerate(candidates, 1):
        try:
            out_path = os.path.join(batch_dir, f"{i:02d}_{quiz_id}_shorts.mp4")
            quiz = render_video(quiz_id, out_path, FRAMES_DIR)

            title, description = make_youtube_meta(quiz)
            meta_path = os.path.join(batch_dir, f"{i:02d}_{quiz_id}_meta.txt")
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write(f"[제목]\n{title}\n\n[설명]\n{description}\n")

            state["used_quiz_ids"].append(quiz_id)
            print(f"[{i}/{len(candidates)}] ✅ {quiz['title']}  →  {os.path.basename(out_path)}")
        except Exception as e:
            print(f"[{i}/{len(candidates)}] ❌ {quiz_id} 실패: {e}")

    save_state(state)
    print(f"\n완료. {batch_dir} 폴더의 mp4를 유튜브에 업로드하고, 같은 이름의 _meta.txt에서 제목/설명을 복사해 붙여넣으세요.")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    main(n)
