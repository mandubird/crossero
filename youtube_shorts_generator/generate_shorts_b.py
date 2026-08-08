#!/usr/bin/env python3
"""
십자가로세로 유튜브 쇼츠 B (성경 퀴즈형) 단건 생성.

사용법:
  python3 generate_shorts_b.py <quiz_id>
  예: python3 generate_shorts_b.py gal_089
"""
import os
import sys

from shorts_lib import render_video, make_youtube_meta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "output")
FRAMES_DIR = os.path.join(HERE, "_frames")


def main(quiz_id):
    out_path = os.path.join(OUT_DIR, f"{quiz_id}_shorts.mp4")
    quiz = render_video(quiz_id, out_path, FRAMES_DIR)

    title, description = make_youtube_meta(quiz)
    meta_path = os.path.join(OUT_DIR, f"{quiz_id}_meta.txt")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"[제목]\n{title}\n\n[설명]\n{description}\n")

    print(f"제목: {quiz['title']}")
    print(f"힌트: {quiz['clue']}")
    print(f"정답: {quiz['answer']}")
    print(f"\n✅ 영상: {out_path}")
    print(f"✅ 유튜브 메타: {meta_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 generate_shorts_b.py <quiz_id>")
        sys.exit(1)
    main(sys.argv[1])
