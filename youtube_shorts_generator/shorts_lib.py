"""
십자가로세로 유튜브 쇼츠 B(성경 퀴즈형) 생성 공통 모듈.
generate_shorts_b.py, generate_batch.py 에서 공용으로 사용.

기존 퍼즐 생성 엔진(play.html, play2.html, auto_publish_with_images.py)은
건드리지 않고 data.js / images/puzzles 를 읽기만 하는 별도 모듈.
"""
import math
import os
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(BASE_DIR, "data.js")
PUZZLES_IMG_DIR = os.path.join(BASE_DIR, "images", "puzzles")
LOGO_PATH = os.path.join(BASE_DIR, "images", "crossero-logo.png")
CHARACTER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "character.png")

W, H = 1080, 1920
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

BRAND_TEXT = "@십자가로세로"
BRAND_URL = "crossero.com"

GOLD = "#ffd43b"
BLUE = "#0073e6"


def get_font(size):
    return ImageFont.truetype(FONT_PATH, size)


def load_quiz(quiz_id):
    """data.js에서 quiz_id에 해당하는 객체를 파싱."""
    with open(DATA_JS, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(rf'"{re.escape(quiz_id)}"\s*:\s*\{{', content)
    if not m:
        raise ValueError(f"quiz_id '{quiz_id}' 를 data.js에서 찾을 수 없습니다.")

    start = m.end() - 1
    depth = 0
    end = start
    for i in range(start, len(content)):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    block = content[start:end]

    title_m = re.search(r'title:\s*"([^"]*)"', block)
    title = title_m.group(1) if title_m else quiz_id

    category_m = re.search(r'category:\s*"([^"]*)"', block)
    category = category_m.group(1) if category_m else ""

    word_pairs = re.findall(r'\{\s*clue:\s*"([^"]*)"\s*,\s*answer:\s*"([^"]*)"\s*\}', block)
    if not word_pairs:
        raise ValueError(f"'{quiz_id}'에서 allWords(clue/answer)를 찾지 못했습니다.")

    pairs = word_pairs[:3]  # 영상 한 편에 최대 3문제
    clue, answer = pairs[0]
    return {
        "id": quiz_id, "title": title, "category": category,
        "clue": clue, "answer": answer,  # 하위 호환(유튜브 메타 등에서 사용)
        "pairs": pairs,
    }


def blank_clue(clue, answer):
    """clue 안의 '이것' 자리표시자를 answer 글자수만큼의 동그라미(○)로 치환."""
    circles = "○" * max(len(answer), 1)
    if "이것" in clue:
        return clue.replace("이것", circles)
    return clue  # '이것' 패턴이 없으면 원문 유지


def find_puzzle_image(title):
    slug_guess = title.replace(":", "-").replace(" ", "-") + "-십자가로세로.png"
    candidate = os.path.join(PUZZLES_IMG_DIR, slug_guess)
    if os.path.exists(candidate):
        return candidate
    prefix = title.split(":")[0]
    for fname in os.listdir(PUZZLES_IMG_DIR):
        if fname.startswith(prefix):
            return os.path.join(PUZZLES_IMG_DIR, fname)
    return None


def new_canvas(bg=(15, 23, 42)):
    return Image.new("RGB", (W, H), bg)


def draw_centered_text(draw, text, y, font, fill="white", max_width=W - 120, line_gap=16):
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((W - w) / 2, y), line, font=font, fill=fill)
        y += h + line_gap
    return y


def draw_badge(draw, text, cy, fill=GOLD, text_color="#111", font_size=44):
    """이모지 대신 알약 모양 배지로 라벨을 표시 (폰트에 이모지 글리프 없어 깨지는 문제 방지)."""
    font = get_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 36, 18
    box_w, box_h = tw + pad_x * 2, th + pad_y * 2
    x0 = (W - box_w) / 2
    y0 = cy - box_h / 2
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=box_h / 2, fill=fill)
    draw.text((W / 2, cy), text, font=font, fill=text_color, anchor="mm")


def apply_brand_watermark(img):
    """오른쪽 상단에 항상 채널명이 보이도록 워터마크 삽입.
    쇼츠 UI(좋아요/댓글/공유 버튼, 자막)가 하단~우측 하단을 가리는 경우가 많아
    항상 비어있는 상단 여백에 배치."""
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(34)

    text = BRAND_TEXT
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 22, 14
    box_w, box_h = tw + pad_x * 2, th + pad_y * 2
    margin_top, margin_right = 56, 36
    x0 = W - box_w - margin_right
    y0 = margin_top

    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=box_h / 2, fill=(0, 0, 0, 140))
    draw.text((x0 + pad_x, y0 + pad_y - 4), text, font=font, fill=(255, 255, 255, 235))

    out = Image.alpha_composite(img, overlay)
    return out.convert("RGB")


def frame_intro(clue, topic=None):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    draw_badge(draw, "성경 퀴즈", 240, font_size=76)

    y = 440
    if topic:
        y = draw_centered_text(draw, topic, y, get_font(50), fill=GOLD, max_width=W - 80)
        y += 26
    y = draw_centered_text(draw, "가로 힌트", y, get_font(46), fill="#94a3b8", max_width=W - 80)
    y += 44
    draw_centered_text(draw, clue, y, get_font(78), fill="white", max_width=W - 80)

    # 십자가로세로 캐릭터 (하단 쪽에 배치하되, 쇼츠 UI에 잘리지 않도록 여백 확보)
    if os.path.exists(CHARACTER_PATH):
        char = Image.open(CHARACTER_PATH).convert("RGBA")
        target_h = 380
        ratio = target_h / char.height
        char = char.resize((int(char.width * ratio), target_h))
        cx = (W - char.width) // 2
        cy = 1080
        img.paste(char, (cx, cy), char)

    return apply_brand_watermark(img)


def frame_countdown(n, progress):
    """n: 표시 숫자(3,2,1). progress: 0.0(방금 시작)~1.0(다음 숫자로 넘어가기 직전).
    영화식 원형 타이머 - 링이 시계방향으로 줄어들며 숫자를 감쌈."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    cx, cy, r = W / 2, H / 2 - 100, 220
    thickness = 22

    # 배경 트랙(연한 회색 원)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline="#334155", width=thickness)

    # 남은 시간 아크 (12시 방향에서 시계방향으로 감소)
    remaining_deg = 360 * (1 - progress)
    start_angle = -90
    end_angle = start_angle + remaining_deg
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=start_angle, end=end_angle, fill=GOLD, width=thickness)

    font_num = get_font(260)
    text = str(n)
    bbox = draw.textbbox((0, 0), text, font=font_num)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2, cy - th / 2 - bbox[1] * 0.5 - 10), text, font=font_num, fill="white")

    return apply_brand_watermark(img)


def frame_answer(answer):
    img = new_canvas(bg=(10, 40, 20))
    draw = ImageDraw.Draw(img)

    draw_badge(draw, "정답 공개", 700, fill="#a7f3d0", text_color="#064e3b")

    font_answer = get_font(140)
    bbox = draw.textbbox((0, 0), answer, font=font_answer)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 850), answer, font=font_answer, fill="white")

    return apply_brand_watermark(img)


def frame_transition(text):
    """다음 장면(퍼즐 이미지) 전 짧게 보여주는 전환 텍스트 화면."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    cy = H / 2 - 60
    lines = text.split("\n")
    total_h = len(lines) * 90
    y = cy - total_h / 2
    for line in lines:
        y = draw_centered_text(draw, line, y, get_font(64), fill="white", max_width=W - 140)

    return apply_brand_watermark(img)


def frame_subscribe():
    """구독 유도 화면. 퍼즐 이미지가 정지된 채로 너무 길게 이어진다는 피드백 반영해
    영상 후반부에 장면 전환 + 구독 유도를 동시에 처리."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    y = 640
    y = draw_centered_text(draw, "구독하고", y, get_font(72), fill="white")
    y += 20

    draw_badge(draw, "구독", y + 90, fill=(230, 30, 30), text_color="white", font_size=64)
    y += 190

    y2 = y + 40
    y2 = draw_centered_text(draw, "다음 성경 퀴즈도", y2, get_font(40), fill="#94a3b8")
    draw_centered_text(draw, "놓치지 마세요", y2, get_font(40), fill="#94a3b8")

    return apply_brand_watermark(img)


def frame_puzzle_reveal(puzzle_img_path, title, recap_pairs=None):
    img = new_canvas(bg=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = draw_centered_text(draw, title, 90, get_font(44), fill="#1e293b", max_width=W - 160)

    if recap_pairs:
        y += 10
        for clue, answer in recap_pairs:
            recap = f"Q. {clue}   →   A. {answer}"
            y = draw_centered_text(draw, recap, y, get_font(30), fill=BLUE, max_width=W - 160, line_gap=6)
            y += 6

    puzzle = Image.open(puzzle_img_path).convert("RGBA")
    target_w = W - 160
    ratio = target_w / puzzle.width
    puzzle = puzzle.resize((target_w, int(puzzle.height * ratio)))
    px = (W - puzzle.width) // 2
    py = y + 36
    img.paste(puzzle, (px, py), puzzle)

    # CTA를 퍼즐 이미지 위에 떠 있는 반투명 카드로 표시
    # (퍼즐 폭에 딱 맞춘 띠 모양 대신, 좌우 여백을 둔 카드로 + 하단에 딱 붙지 않게 위로 배치)
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    banner_h = 260
    inset = 70  # 퍼즐 좌우보다 안쪽으로 들여서 "카드"처럼 보이게
    bottom_margin = 130  # 퍼즐 맨 아래에 딱 붙지 않도록 여백 확보(위로 띄움)
    banner_left = px + inset
    banner_right = px + puzzle.width - inset
    banner_bottom = py + puzzle.height - bottom_margin
    banner_top = banner_bottom - banner_h

    odraw.rounded_rectangle([banner_left, banner_top, banner_right, banner_bottom], radius=28, fill=(0, 40, 100, 225))

    odraw.text((W / 2, banner_top + 60), "직접 풀어보세요", font=get_font(62), fill=(255, 255, 255, 255), anchor="mm")
    odraw.text((W / 2, banner_top + 144), BRAND_URL, font=get_font(56), fill=(255, 255, 255, 255), anchor="mm")
    odraw.text((W / 2, banner_top + 214), '검색창에 "십자가로세로"', font=get_font(34), fill=(210, 225, 255, 255), anchor="mm")

    img = Image.alpha_composite(img, overlay).convert("RGB")

    return apply_brand_watermark(img)


def build_frame_sequence(quiz):
    """(PIL.Image, 노출초) 리스트 생성. 문제 최대 3개를 순서대로 반복 후 퍼즐 이미지로 마무리."""
    puzzle_img_path = find_puzzle_image(quiz["title"])
    if not puzzle_img_path:
        raise FileNotFoundError(f"퍼즐 이미지를 찾지 못했습니다: {quiz['title']}")

    pairs = quiz.get("pairs") or [(quiz["clue"], quiz["answer"])]
    total = len(pairs)
    topic = book_hashtag(quiz.get("category", ""))

    sequence = []
    recap_pairs = []
    SUBFRAMES = 10

    for idx, (clue, answer) in enumerate(pairs, start=1):
        blanked = blank_clue(clue, answer)
        recap_pairs.append((blanked, answer))

        sequence.append((frame_intro(blanked, topic=topic), 3.0))

        for n in (3, 2, 1):
            for i in range(SUBFRAMES):
                progress = i / SUBFRAMES
                sequence.append((frame_countdown(n, progress), 1.0 / SUBFRAMES))

        sequence.append((frame_answer(answer), 2.0))

    sequence.append((frame_transition("더 많은 퍼즐이\n보고 싶다면"), 2.0))
    sequence.append((
        frame_puzzle_reveal(puzzle_img_path, quiz["title"], recap_pairs=recap_pairs),
        3.0,
    ))
    sequence.append((frame_subscribe(), 2.5))
    return sequence


def render_video(quiz_id, out_path, frames_dir):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    quiz = load_quiz(quiz_id)
    sequence = build_frame_sequence(quiz)

    concat_lines = []
    for i, (img, dur) in enumerate(sequence):
        fpath = os.path.join(frames_dir, f"{quiz_id}_{i:03d}.png")
        img.save(fpath)
        concat_lines.append(f"file '{fpath}'")
        concat_lines.append(f"duration {dur}")
    concat_lines.append(f"file '{os.path.join(frames_dir, f'{quiz_id}_{len(sequence)-1:03d}.png')}'")

    concat_file = os.path.join(frames_dir, f"{quiz_id}_concat.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-vf", f"scale={W}:{H},format=yuv420p",
        "-r", "30",
        out_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return quiz


def book_hashtag(category):
    """category(예: '신약성경, 서신서, 갈라디아서, 중고등부용, 전체')에서 대표 책 이름 추출.
    구약성경/신약성경 대분류와 모세오경/역사서/시가서/대선지서/소선지서/복음서/서신서 같은
    중분류, 대상·속성 태그를 모두 건너뛰고 실제 책 이름만 남긴다.
    (책 이름과 중분류의 등장 순서가 항목마다 달라 순서만으로는 구분 불가)"""
    parts = [p.strip() for p in category.split(",")]
    skip = {
        "전체", "주일학교용", "중고등부용", "유아부용", "새신자용", "리더용",
        "구약성경", "신약성경",
        "모세오경", "역사서", "시가서", "대선지서", "소선지서", "예언서", "복음서", "서신서",
        "주제별", "인물중심", "지명중심",
    }
    for p in parts:
        if p and p not in skip:
            return p
    return ""


def make_youtube_meta(quiz):
    book = book_hashtag(quiz["category"])
    pairs = quiz.get("pairs") or [(quiz["clue"], quiz["answer"])]
    q_count = len(pairs)

    topic_prefix = f"[{book}] " if book else ""
    title = f"{topic_prefix}『{quiz['title']}』 성경 퀴즈 {q_count}문제 | 정답 공개 #Shorts"

    qa_lines = "\n".join(f"Q{idx}. {clue} → {answer}" for idx, (clue, answer) in enumerate(pairs, start=1))
    description = (
        f"오늘의 성경 퀴즈! 모두 맞혀보세요.\n\n"
        f"{qa_lines}\n\n"
        f"📖 {quiz['title']} 전체 퍼즐은 십자가로세로에서 무료로 풀어보세요.\n"
        f"👉 https://crossero.com\n\n"
        f"#성경퀴즈 #주일학교 #교회학교 #성경가로세로 #십자가로세로"
        + (f" #{book}" if book else "")
    )
    return title, description
