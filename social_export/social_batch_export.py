#!/usr/bin/env python3
import json
import os
import random
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
WWW_DIR = SCRIPT_DIR.parent
DATA_JS_PATH = WWW_DIR / "data.js"
LOGO_PATH = WWW_DIR / "images" / "crossero-logo.png"

QUEUE_DIR = SCRIPT_DIR / "queue"
DONE_DIR = SCRIPT_DIR / "queue_done"
OUTPUT_DIR = SCRIPT_DIR / "output"
LOG_DIR = SCRIPT_DIR / "logs"

DOMAIN = "crossero.com"
BRAND = "십자가로세로"
SIZE = 15

RATIOS = {
    "square": (1080, 1080),
    "vertical": (1080, 1920),
    "landscape": (1200, 900),
}


@dataclass
class WordEntry:
    clue: str
    answer: str


@dataclass
class PlacedWord:
    num: int
    x: int
    y: int
    dir: str
    clue: str
    answer: str


@dataclass
class PuzzleData:
    puzzle_id: str
    title: str
    words: List[WordEntry]


@dataclass
class BuiltPuzzle:
    title: str
    solution: List[List[Optional[str]]]
    number_map: List[List[Optional[int]]]
    across: List[PlacedWord]
    down: List[PlacedWord]


def ensure_dirs() -> None:
    for d in [QUEUE_DIR, DONE_DIR, OUTPUT_DIR, LOG_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def write_log(message: str) -> None:
    log_file = LOG_DIR / f"run_{datetime.now().strftime('%Y%m%d')}.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")


def sanitize_name(s: str, max_len: int = 60) -> str:
    s = (s or "puzzle").strip().replace(":", " ")
    s = re.sub(r"[^\w\s\-가-힣]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return (s or "puzzle")[:max_len]

def seo_image_base(title: str, puzzle_id: str) -> str:
    base = sanitize_name(f"{title}-{puzzle_id}", max_len=50).lower()
    return base.replace("_", "-")


def pick_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    if bold:
        candidates = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]

    for p in candidates:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def load_quiz_data_from_js(puzzle_id: str) -> PuzzleData:
    node_script = f"""
const fs=require('fs');
const vm=require('vm');
let code=fs.readFileSync({json.dumps(str(DATA_JS_PATH))},'utf8');
code += '\\nthis.__DB = QUIZ_DATABASE;';
const ctx={{}};
vm.createContext(ctx);
vm.runInContext(code, ctx);
const q = ctx.__DB[{json.dumps(puzzle_id)}];
if (!q) {{
  console.log(JSON.stringify({{ok:false}}));
  process.exit(0);
}}
console.log(JSON.stringify({{
  ok:true,
  id:{json.dumps(puzzle_id)},
  title:q.title || {json.dumps(puzzle_id)},
  allWords:(q.allWords || []).map(w=>({{ clue:String(w.clue||''), answer:String(w.answer||'') }}))
}}));
"""

    proc = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    payload = json.loads(proc.stdout.strip() or "{}")
    if not payload.get("ok"):
        raise KeyError(f"Puzzle id not found: {puzzle_id}")

    words = []
    for w in payload.get("allWords", []):
        answer = (w.get("answer") or "").strip()
        clue = (w.get("clue") or "").strip()
        if not answer or not clue:
            continue
        if len(answer) < 2 or len(answer) > SIZE:
            continue
        words.append(WordEntry(clue=clue, answer=answer))

    if not words:
        raise ValueError(f"No usable words in puzzle: {puzzle_id}")

    return PuzzleData(puzzle_id=puzzle_id, title=payload["title"], words=words)


def make_empty_grid() -> List[List[Optional[str]]]:
    return [[None for _ in range(SIZE)] for _ in range(SIZE)]


def target_count(pool_size: int) -> int:
    if pool_size >= 50:
        return 35
    if pool_size >= 30:
        return 20
    if pool_size >= 15:
        return 12
    if pool_size >= 8:
        return 8
    return max(5, pool_size - 2)


def build_puzzle(data: PuzzleData) -> BuiltPuzzle:
    random.seed()
    pool = [WordEntry(w.clue, w.answer) for w in data.words]
    random.shuffle(pool)

    solution = make_empty_grid()
    number_map: List[List[Optional[int]]] = [[None for _ in range(SIZE)] for _ in range(SIZE)]

    across: List[PlacedWord] = []
    down: List[PlacedWord] = []
    placed: List[PlacedWord] = []
    used = set()
    next_num = 1

    t_count = target_count(len(pool))

    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x < SIZE and 0 <= y < SIZE

    def can_place(word: str, x: int, y: int, direction: str) -> Tuple[bool, int]:
        if direction == "across":
            if x < 0 or x + len(word) > SIZE or y < 0 or y >= SIZE:
                return False, 0
        else:
            if y < 0 or y + len(word) > SIZE or x < 0 or x >= SIZE:
                return False, 0

        before = (x - 1, y) if direction == "across" else (x, y - 1)
        after = (x + len(word), y) if direction == "across" else (x, y + len(word))
        if in_bounds(*before) and solution[before[1]][before[0]] is not None:
            return False, 0
        if in_bounds(*after) and solution[after[1]][after[0]] is not None:
            return False, 0

        cross_count = 0

        for i, ch in enumerate(word):
            cx = x + i if direction == "across" else x
            cy = y if direction == "across" else y + i
            existing = solution[cy][cx]

            if existing is not None and existing != ch:
                return False, 0
            if existing == ch:
                cross_count += 1

            if existing is None:
                neighbors = [(cx - 1, cy), (cx + 1, cy)] if direction == "down" else [(cx, cy - 1), (cx, cy + 1)]
                for nx, ny in neighbors:
                    if in_bounds(nx, ny) and solution[ny][nx] is not None:
                        return False, 0

        return True, cross_count

    def place_word(word: WordEntry, x: int, y: int, direction: str) -> bool:
        nonlocal next_num
        ok, _ = can_place(word.answer, x, y, direction)
        if not ok:
            return False

        for i, ch in enumerate(word.answer):
            cx = x + i if direction == "across" else x
            cy = y if direction == "across" else y + i
            solution[cy][cx] = ch

        if number_map[y][x] is None:
            number_map[y][x] = next_num
            next_num += 1

        pw = PlacedWord(
            num=number_map[y][x],
            x=x,
            y=y,
            dir=direction,
            clue=word.clue,
            answer=word.answer,
        )

        if direction == "across":
            across.append(pw)
        else:
            down.append(pw)

        placed.append(pw)
        used.add((word.answer, word.clue))
        return True

    first = pool.pop(0)
    fx = max(0, (SIZE - len(first.answer)) // 2)
    fy = SIZE // 2
    place_word(first, fx, fy, "across")

    retry: List[WordEntry] = []
    attempts = 0
    max_attempts = 12000

    while attempts < max_attempts and len(placed) < t_count and (pool or retry):
        if not pool and retry:
            random.shuffle(retry)
            pool = retry
            retry = []

        if not pool:
            break

        w = pool.pop(0)
        if (w.answer, w.clue) in used:
            attempts += 1
            continue

        candidates: List[Tuple[int, int, int, str]] = []

        for p in reversed(placed):
            new_dir = "down" if p.dir == "across" else "across"
            for wi, wc in enumerate(w.answer):
                for pi, pc in enumerate(p.answer):
                    if wc != pc:
                        continue
                    if new_dir == "across":
                        x = p.x - wi
                        y = p.y + pi
                    else:
                        x = p.x + pi
                        y = p.y - wi
                    ok, cross = can_place(w.answer, x, y, new_dir)
                    if ok:
                        candidates.append((cross, x, y, new_dir))

        placed_now = False
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            top = candidates[: min(3, len(candidates))]
            _, x, y, d = random.choice(top)
            placed_now = place_word(w, x, y, d)

        if not placed_now:
            dirs = ["across", "down"]
            random.shuffle(dirs)
            for d in dirs:
                for _ in range(200):
                    x = random.randint(0, SIZE - 1)
                    y = random.randint(0, SIZE - 1)
                    if place_word(w, x, y, d):
                        placed_now = True
                        break
                if placed_now:
                    break

        if not placed_now:
            retry.append(w)

        attempts += 1

    across.sort(key=lambda q: q.num)
    down.sort(key=lambda q: q.num)

    return BuiltPuzzle(title=data.title, solution=solution, number_map=number_map, across=across, down=down)


def render_board(solution: List[List[Optional[str]]], number_map: List[List[Optional[int]]], show_answer: bool, size_px: int = 900) -> Image.Image:
    cell = size_px // SIZE
    img = Image.new("RGBA", (size_px, size_px), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    num_font = pick_font(max(11, int(cell * 0.2)), bold=True)
    char_font = pick_font(max(18, int(cell * 0.48)), bold=True)

    for y in range(SIZE):
        for x in range(SIZE):
            active = solution[y][x] is not None
            x0 = x * cell
            y0 = y * cell
            x1 = x0 + cell
            y1 = y0 + cell

            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255) if active else (90, 90, 90), outline=(175, 175, 175))

            if active and number_map[y][x] is not None:
                draw.rectangle([x0 + 1, y0 + 1, x0 + int(cell * 0.30), y0 + int(cell * 0.24)], fill=(255, 255, 255))
                draw.text((x0 + 3, y0 + 2), str(number_map[y][x]), font=num_font, fill=(0, 115, 230))

            if show_answer and active and solution[y][x]:
                ch = solution[y][x]
                bbox = draw.textbbox((0, 0), ch, font=char_font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                draw.text((x0 + (cell - tw) // 2, y0 + (cell - th) // 2 - 2), ch, font=char_font, fill=(15, 15, 15))

    return img


def add_branding(base: Image.Image, logo: Optional[Image.Image], y_bottom: int) -> None:
    draw = ImageDraw.Draw(base)
    w, _ = base.size

    if logo is not None:
        target_h = 42
        ratio = target_h / logo.height
        lw = int(logo.width * ratio)
        logo_small = logo.resize((lw, target_h), Image.Resampling.LANCZOS)
        base.alpha_composite(logo_small, (40, y_bottom - target_h))

    domain_font = pick_font(28, bold=True)
    brand_font = pick_font(24, bold=False)
    draw.text((w - 320, y_bottom - 40), DOMAIN, font=domain_font, fill=(22, 70, 146))
    draw.text((w - 320, y_bottom - 12), BRAND, font=brand_font, fill=(30, 30, 30))


def render_board_card(board: Image.Image, title: str, subtitle: str, size: Tuple[int, int], logo: Optional[Image.Image]) -> Image.Image:
    w, h = size
    base = Image.new("RGBA", (w, h), (247, 250, 255, 255))
    draw = ImageDraw.Draw(base)

    header_h = max(180, int(h * 0.16))
    draw.rectangle([0, 0, w, header_h], fill=(232, 243, 255, 255))

    title_font = pick_font(max(32, int(min(w, h) * 0.036)), bold=True)
    sub_font = pick_font(max(24, int(min(w, h) * 0.024)), bold=False)
    draw.text((40, 36), title, font=title_font, fill=(15, 23, 42))
    draw.text((40, 88), subtitle, font=sub_font, fill=(51, 65, 85))

    avail_w = w - 120
    avail_h = h - header_h - 140
    ratio = min(avail_w / board.width, avail_h / board.height)
    bw = int(board.width * ratio)
    bh = int(board.height * ratio)
    board_resized = board.resize((bw, bh), Image.Resampling.LANCZOS)

    bx = (w - bw) // 2
    by = header_h + (avail_h - bh) // 2

    shadow = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([0, 0, bw + 20, bh + 20], radius=16, fill=(0, 0, 0, 45))
    base.alpha_composite(shadow, (bx - 10, by - 8))
    base.alpha_composite(board_resized, (bx, by))

    add_branding(base, logo, h - 30)
    return base


def render_hint_card(across: List[PlacedWord], down: List[PlacedWord], title: str, size: Tuple[int, int], logo: Optional[Image.Image]) -> Image.Image:
    w, h = size
    base = Image.new("RGBA", (w, h), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)

    header_h = max(180, int(h * 0.16))
    draw.rectangle([0, 0, w, header_h], fill=(232, 243, 255, 255))

    title_font = pick_font(max(32, int(min(w, h) * 0.036)), bold=True)
    sub_font = pick_font(max(24, int(min(w, h) * 0.024)), bold=False)
    draw.text((40, 36), title, font=title_font, fill=(15, 23, 42))
    draw.text((40, 88), "Hint Image", font=sub_font, fill=(51, 65, 85))

    pad = 40
    top = header_h + 20
    bottom = h - 90

    draw.rounded_rectangle([pad, top, w - pad, bottom], radius=20, fill=(255, 255, 255), outline=(219, 234, 254), width=2)

    gap = 26
    left_x = pad + 24
    col_w = (w - (pad * 2) - (24 * 2) - gap) // 2
    right_x = left_x + col_w + gap

    sec_font = pick_font(max(22, int(min(w, h) * 0.022)), bold=True)
    hint_font = pick_font(max(18, int(min(w, h) * 0.016)), bold=False)

    draw.text((left_x, top + 14), "Across", font=sec_font, fill=(15, 23, 42))
    draw.text((right_x, top + 14), "Down", font=sec_font, fill=(15, 23, 42))

    y_start = top + 54
    line_h = max(22, int(h * 0.022))
    max_lines = max(10, (bottom - y_start - 12) // line_h)

    for i, q in enumerate(across[:max_lines]):
        txt = f"{q.num}. {q.clue}"
        if len(txt) > 44:
            txt = txt[:41] + "..."
        draw.text((left_x, y_start + i * line_h), txt, font=hint_font, fill=(30, 41, 59))

    for i, q in enumerate(down[:max_lines]):
        txt = f"{q.num}. {q.clue}"
        if len(txt) > 44:
            txt = txt[:41] + "..."
        draw.text((right_x, y_start + i * line_h), txt, font=hint_font, fill=(30, 41, 59))

    add_branding(base, logo, h - 30)
    return base


def save_bundle(built: BuiltPuzzle, out_dir: Path, puzzle_id: str) -> None:
    logo = Image.open(LOGO_PATH).convert("RGBA") if LOGO_PATH.exists() else None

    puzzle_board = render_board(built.solution, built.number_map, show_answer=False)
    answer_board = render_board(built.solution, built.number_map, show_answer=True)
    seo_base = seo_image_base(built.title, puzzle_id)

    for ratio_name, size in RATIOS.items():
        ratio_dir = out_dir / ratio_name
        ratio_dir.mkdir(parents=True, exist_ok=True)

        puzzle_img = render_board_card(puzzle_board, built.title, "Puzzle Image", size, logo)
        hint_img = render_hint_card(built.across, built.down, built.title, size, logo)
        answer_img = render_board_card(answer_board, built.title, "Answer Image", size, logo)

        puzzle_img.save(ratio_dir / "puzzle.png", format="PNG")
        hint_img.save(ratio_dir / "hint.png", format="PNG")
        answer_img.save(ratio_dir / "answer.png", format="PNG")

        # Pinterest/멀티모달 SEO 파일명 버전도 함께 생성
        puzzle_img.save(ratio_dir / f"{seo_base}-bible-crossword-puzzle-{ratio_name}.png", format="PNG")
        hint_img.save(ratio_dir / f"{seo_base}-sunday-school-material-{ratio_name}.png", format="PNG")
        answer_img.save(ratio_dir / f"{seo_base}-church-activity-answer-{ratio_name}.png", format="PNG")

    # Pinterest 설명/ALT 복붙 템플릿
    caption = (
        f"{built.title} Bible crossword puzzle. "
        "Sunday school material and printable church activity. "
        "Use on church bulletin and class handout. Crossero.com"
    )
    alt_lines = [
        f"Puzzle ALT: Crossero Bible Crossword Puzzle for {built.title} - Sunday School Material",
        f"Hint ALT: {built.title} Bible Crossword Hints - Printable Church Activity",
        f"Answer ALT: {built.title} Bible Crossword Answer Sheet - Church Bulletin Puzzle",
    ]
    with (out_dir / "pinterest_caption.txt").open("w", encoding="utf-8") as f:
        f.write(caption + "\n")
    with (out_dir / "image_alt_templates.txt").open("w", encoding="utf-8") as f:
        f.write("\n".join(alt_lines) + "\n")


def collect_queue_files() -> List[Path]:
    return sorted([p for p in QUEUE_DIR.iterdir() if p.is_file() and not p.name.startswith(".")])


def process_one(queue_file: Path) -> bool:
    puzzle_id = queue_file.stem.strip()
    try:
        data = load_quiz_data_from_js(puzzle_id)
    except Exception as e:
        write_log(f"SKIP {puzzle_id}: {e}")
        return False

    try:
        built = build_puzzle(data)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = sanitize_name(data.title)
        out_dir = OUTPUT_DIR / f"{ts}_{puzzle_id}_{safe_title}"
        save_bundle(built, out_dir, puzzle_id)
        write_log(f"OK {puzzle_id} -> {out_dir}")
        return True
    except Exception as e:
        write_log(f"FAIL {puzzle_id}: {e}")
        return False


def main() -> int:
    ensure_dirs()
    queue_files = collect_queue_files()

    if not queue_files:
        print(f"No queue files found: {QUEUE_DIR}")
        print("Create empty files like gen_001.txt then run again.")
        return 0

    print(f"Queue count: {len(queue_files)}")
    success = 0
    failed = 0

    for qf in queue_files:
        ok = process_one(qf)
        if ok:
            success += 1
            shutil.move(str(qf), str(DONE_DIR / qf.name))
        else:
            failed += 1
            fail_name = qf.with_suffix(qf.suffix + ".failed")
            shutil.move(str(qf), str(DONE_DIR / fail_name.name))

    print(f"Done. success={success}, failed={failed}")
    print(f"Output folder: {OUTPUT_DIR}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
