#!/usr/bin/env python3
"""
예약 발행 + 퍼즐 이미지 생성 (매일 1회 실행)
- init: posts_schedule.json 생성 (287개를 날짜별 1~3개 배정)
- 일반 실행: 오늘 날짜에 해당하는 글만 발행 (이미지 생성 → HTML → manifest 갱신 → index·posts.xml)
"""
import os
import re
import json
import random
from datetime import datetime, timedelta
from html import escape
from urllib.parse import quote

# generate_seo_posts와 동일한 파싱·템플릿
from generate_seo_posts import (
    parse_data_js,
    INTRO_TEMPLATES,
    KEYWORDS_BY_PREFIX,
    DOMAIN,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_PATH = os.path.join(SCRIPT_DIR, 'posts_schedule.json')
MANIFEST_PATH = os.path.join(SCRIPT_DIR, 'published_manifest.json')
DATA_JS = os.path.join(SCRIPT_DIR, 'data.js')
POSTS_DIR = os.path.join(SCRIPT_DIR, 'posts')
PUZZLES_IMG_DIR = os.path.join(SCRIPT_DIR, 'images', 'puzzles')

# 예약 시작일, 하루 1개
START_DATE = datetime(2026, 2, 20)
POSTS_PER_DAY = (1, 1)

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def find_matching_brace(text, start_pos, open_c, close_c):
    depth = 0
    for i in range(start_pos, len(text)):
        if text[i] == open_c:
            depth += 1
        elif text[i] == close_c:
            depth -= 1
            if depth == 0:
                return i
    return -1


def make_slug_korean(book, keyword):
    """한글 파일명용 슬러그 (공백→하이픈, 특수문자 제거)"""
    s = f"{book}-{keyword}".strip()
    s = re.sub(r'[^\w\s\-가-힣]', '', s)
    s = s.replace(' ', '-').strip('-')[:60]
    return s or 'puzzle'


def make_slug_from_title(display_title):
    """data.js 퍼즐 title로 URL 슬러그 생성. 예: '사도행전: 첫 순교자 스데반' → '사도행전-첫-순교자-스데반'"""
    s = (display_title or '퍼즐').replace(':', ' ').strip()
    s = re.sub(r'[^\w\s\-가-힣]', '', s)
    s = s.replace(' ', '-').strip('-')[:60]
    return s or 'puzzle'


def make_image_slug(puzzle):
    """이미지 파일명: 제목명과 동일한 이름-십자가로세로 (예: 출애굽기-모세의-소명-십자가로세로)"""
    title = (puzzle.get('title') or '퍼즐').replace(':', ' ').strip()
    s = re.sub(r'[^\w\s\-가-힣]', '', title)
    s = s.replace(' ', '-').strip('-')[:50]
    return (s or 'puzzle') + '-십자가로세로'


def get_keyword_for_puzzle(puzzle):
    book = puzzle['title'].split(':')[0].strip() if ':' in puzzle['title'] else puzzle['title'].split()[0]
    kw = random.choice(KEYWORDS_BY_PREFIX)
    return f"{book} {kw}"


def _find_chrome_executable():
    """Mac/Windows에서 시스템 Chrome 경로 (Playwright Chromium 실패 시 대안)."""
    import platform
    if platform.system() == 'Darwin':
        p = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        if os.path.isfile(p):
            return p
    elif platform.system() == 'Windows':
        for p in [
            os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        ]:
            if os.path.isfile(p):
                return p
    return None


def export_puzzle_image_via_browser(pid, slug, timeout=15000):
    """play2.html?id=pid&export=1 로 열어 퍼즐 PNG 저장 + (가로/세로 힌트, 동일 퍼즐 play URL, 힌트 num+clue JSON) 반환.
    반환: (성공여부, across_힌트리스트, down_힌트리스트, answer_url, play_hints_json 또는 None)"""
    if not HAS_PLAYWRIGHT:
        return False, [], [], ''
    import base64
    from pathlib import Path
    play_path = Path(SCRIPT_DIR) / 'play2.html'
    file_url = play_path.as_uri() + '?id=' + pid + '&export=1'
    os.makedirs(PUZZLES_IMG_DIR, exist_ok=True)
    out_path = os.path.join(PUZZLES_IMG_DIR, slug + '.png')
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception:
                chrome_path = _find_chrome_executable()
                browser = p.chromium.launch(headless=True, executable_path=chrome_path) if chrome_path else None
                if not browser:
                    raise
            page = browser.new_page()
            page.goto(file_url, wait_until='domcontentloaded', timeout=timeout)
            page.wait_for_load_state('networkidle')
            page.wait_for_function('window.__puzzleExportReady === true', timeout=timeout)
            data_url = page.evaluate('window.__puzzleExportDataUrl || ""')
            across = page.evaluate('window.__puzzleExportAcross || []')
            down = page.evaluate('window.__puzzleExportDown || []')
            play_g = page.evaluate('window.__puzzlePlayG || ""')
            play_hints = page.evaluate('window.__puzzleExportHints || ""')
            browser.close()
            # 블로그 하단 링크: 같은 퍼즐 빈 칸 + 실제 힌트 (g=, h1=가로, h2=세로 분리로 URL 잘림 방지)
            answer_url = ''
            if play_g:
                answer_url = f"{DOMAIN}/play2.html?play=1&g={quote(play_g, safe='')}"
                if play_hints:
                    try:
                        hints_obj = json.loads(play_hints)
                        arr_a = hints_obj.get('a') or hints_obj.get('across') or []
                        arr_d = hints_obj.get('d') or hints_obj.get('down') or []
                        b64_a = base64.urlsafe_b64encode(json.dumps(arr_a, ensure_ascii=False).encode('utf-8')).decode('ascii').rstrip('=')
                        b64_d = base64.urlsafe_b64encode(json.dumps(arr_d, ensure_ascii=False).encode('utf-8')).decode('ascii').rstrip('=')
                        answer_url += f"&h1={quote(b64_a, safe='')}&h2={quote(b64_d, safe='')}"
                    except Exception:
                        pass
        if not data_url or not data_url.startswith('data:image/png;base64,'):
            return False, [], [], '', None
        b64 = data_url.split(',', 1)[1]
        with open(out_path, 'wb') as f:
            f.write(base64.b64decode(b64))
        return True, across, down, answer_url, (play_hints if play_hints else None)
    except Exception as e:
        if os.environ.get('DEBUG'):
            print(f"  ⚠️ 브라우저 내보내기 실패 ({pid}): {e}")
        return False, [], [], '', None


def generate_puzzle_grid_image(slug, hint_count, size=420, cells=15):
    """퍼즐 빈 칸 그리드 PNG 생성 (한글 파일명). Pillow 필요."""
    if not HAS_PILLOW:
        return None
    os.makedirs(PUZZLES_IMG_DIR, exist_ok=True)
    cell = size // cells
    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # 그리드 선
    for i in range(cells + 1):
        draw.line([(i * cell, 0), (i * cell, size)], fill=(200, 200, 200), width=1)
        draw.line([(0, i * cell), (size, i * cell)], fill=(200, 200, 200), width=1)
    # 일부 칸에 번호 (검은 칸 대신 번호만; 최대 hint_count까지)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 10)
    except Exception:
        font = ImageFont.load_default()
    n = min(hint_count, cells * 2)
    for i in range(n):
        row, col = i // cells, i % cells
        draw.text((col * cell + 2, row * cell + 2), str(i + 1), fill=(100, 100, 100), font=font)
    path = os.path.join(PUZZLES_IMG_DIR, f"{slug}.png")
    img.save(path, 'PNG')
    return path


def split_hints(hints):
    """힌트를 가로/세로로 반씩 나눔 (data.js에 dir 없음)"""
    n = len(hints)
    if n <= 0:
        return [], []
    mid = (n + 1) // 2
    return hints[:mid], hints[mid:]


def generate_post_html_with_image(puzzle, keyword, slug, publish_date, image_slug, has_puzzle_image=True,
                                  display_title=None,
                                   export_across=None, export_down=None, answer_link_override=None,
                                   export_hints_with_num=None):
    """블로그 글 HTML. export_hints_with_num 있으면 그리드와 동일한 번호(가로 1,4 / 세로 2,3 등)로 표기."""
    book = puzzle['title'].split(':')[0].strip() if ':' in puzzle['title'] else puzzle['title'].split()[0]
    pid = puzzle['id']
    hints = puzzle['hints']
    if export_hints_with_num:
        across_list = export_hints_with_num.get('a') or export_hints_with_num.get('across') or []
        down_list = export_hints_with_num.get('d') or export_hints_with_num.get('down') or []
        hint_count = len(across_list) + len(down_list)
        use_num_for_display = True
    elif export_across is not None and export_down is not None:
        across_list, down_list = list(export_across), list(export_down)
        hint_count = len(across_list) + len(down_list)
        use_num_for_display = False
    else:
        across_list, down_list = split_hints(hints or [])
        hint_count = len(hints) if hints else 0
        use_num_for_display = False
    intro = random.choice(INTRO_TEMPLATES).format(book=book, keyword=keyword, hint_count=hint_count)
    title = (display_title or puzzle.get('title') or f"{book} {keyword}").strip()
    date_iso = publish_date.strftime('%Y-%m-%d')
    date_str = publish_date.strftime('%Y년 %m월 %d일')
    cat_esc = escape((puzzle.get('category') or '성경')[:50])
    answer_link = answer_link_override if answer_link_override else f"{DOMAIN}/play.html?id={pid}"
    same_puzzle = bool(answer_link_override)
    if same_puzzle:
        section_heading = "이 퍼즐 풀어보기"
        section_desc = "아래 버튼을 누르면 위와 같은 퍼즐이 빈 칸 상태로 열립니다. 직접 풀어보세요."
        btn_text = "▶ 이 퍼즐 풀어보기 (새창)"
    else:
        section_heading = "이 주제 퍼즐 풀어보기"
        section_desc = f"아래 버튼을 누르면 <strong>{escape(book)}</strong> 주제의 가로세로 퍼즐이 새 창에서 열립니다. 직접 풀어보세요."
        btn_text = f"▶ {escape(book)} 퍼즐 풀어보기 (새창)"

    if has_puzzle_image:
        img_rel = f"../images/puzzles/{image_slug}.png"
        og_img = f"{DOMAIN}/images/puzzles/{image_slug}.png"
    else:
        img_rel = "../images/og-image.png"
        og_img = f"{DOMAIN}/images/og-image.png"
    img_alt = f"{escape(title)} - 무료 온라인 가로세로 낱말퍼즐"
    if use_num_for_display and across_list and isinstance(across_list[0], dict):
        def _num(d):
            return d.get('n') if d.get('n') is not None else d.get('num')
        def _clue(d):
            return d.get('c') or d.get('clue') or ''
        across_html = "".join(f'<div class="hint-item">{_num(d)}. {escape(_clue(d))}</div>' for d in across_list[:20])
        down_html = "".join(f'<div class="hint-item">{_num(d)}. {escape(_clue(d))}</div>' for d in down_list[:20])
    else:
        across_html = "".join(f'<div class="hint-item">{i}. {escape(h)}</div>' for i, h in enumerate(across_list[:20], 1))
        down_html = "".join(f'<div class="hint-item">{i}. {escape(h)}</div>' for i, h in enumerate(down_list[:20], 1))
    if not across_html:
        across_html = '<div class="hint-item">(가로 힌트는 퍼즐 플레이에서 확인하세요)</div>'
    if not down_html:
        down_html = '<div class="hint-item">(세로 힌트는 퍼즐 플레이에서 확인하세요)</div>'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(book)}를 주제로 한 {escape(keyword)}입니다. {hint_count}개의 힌트로 구성된 무료 가로세로 낱말 퍼즐. 주일학교 교재 추천, 주일학교 주보, 주일학교 교안, 주일학교 공과교재로 활용할 수 있습니다.">
<meta name="keywords" content="{escape(keyword)}, {escape(book)}, 십자가로세로, 성경퀴즈, 말씀퀴즈, 가로세로퍼즐, 주일학교 교재 추천, 주일학교 주보, 주일학교 교안, 주일학교 공과교재">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(book)} {escape(keyword)} - 무료 퀴즈">
<meta property="og:image" content="{og_img}">
<meta property="og:type" content="article">
<meta property="og:url" content="{DOMAIN}/posts/{slug}.html">
<meta property="article:published_time" content="{date_iso}">
<link rel="canonical" href="{DOMAIN}/posts/{slug}.html">
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: -apple-system, "Pretendard", sans-serif; background: #f5f5f5; color: #333; line-height: 1.8; }}
.nav {{ display: flex; justify-content: center; gap: 10px; background: #fff; border-bottom: 1px solid #e5e5e5; padding: 12px 0; }}
.nav-item {{ padding: 8px 14px; font-size: 14px; color: #444; text-decoration: none; border-radius: 6px; }}
.nav-item:hover {{ background: #f0f6ff; color: #0073e6; }}
.nav-active {{ background: #0073e6; color: #fff !important; font-weight: 600; }}
@media (max-width: 768px) {{ .nav {{ padding: 8px 6px; gap: 6px; }} .nav-item {{ padding: 6px 10px; font-size: 12px; }} }}
main {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
article {{ background: #fff; border-radius: 12px; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
h1 {{ font-size: 28px; font-weight: 800; color: #222; margin: 0 0 16px 0; }}
.meta {{ color: #888; font-size: 14px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #eee; }}
.intro {{ font-size: 17px; line-height: 1.9; color: #444; margin-bottom: 32px; padding: 20px; background: #f8f9fa; border-left: 4px solid #0073e6; border-radius: 4px; }}
.intro strong {{ color: #0073e6; }}
.puzzle-image {{ width: 100%; max-width: 420px; height: auto; display: block; margin: 24px auto; border: 2px solid #eee; border-radius: 8px; }}
.hints-section {{ margin: 32px 0; }}
.hints-title {{ font-size: 20px; font-weight: 700; color: #222; margin: 0 0 12px 0; padding-left: 12px; border-left: 4px solid #0073e6; }}
.hints-list {{ background: #fafbfc; padding: 24px; border-radius: 8px; border: 1px solid #e1e4e8; }}
.hint-item {{ padding: 10px 0; color: #444; font-size: 15px; border-bottom: 1px dashed #e1e4e8; }}
.hint-item:last-child {{ border-bottom: none; }}
.answer-section {{ margin: 40px 0; padding: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center; color: #fff; }}
.answer-section h3 {{ font-size: 22px; margin: 0 0 12px 0; }}
.answer-btn {{ display: inline-block; padding: 16px 40px; background: #fff; color: #667eea; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 16px; }}
.keywords-section {{ margin-top: 32px; padding: 20px; background: #f8f9fa; border-radius: 8px; border: 1px solid #e1e4e8; }}
.keywords-section h3 {{ font-size: 16px; margin: 0 0 10px 0; color: #555; }}
.keywords-section p {{ margin: 0; font-size: 14px; color: #666; line-height: 1.7; }}
.edu-section {{ margin-top: 20px; padding: 18px; background: #f6fbff; border: 1px solid #dbeafe; border-radius: 8px; }}
.edu-section h3 {{ margin: 0 0 8px 0; font-size: 16px; color: #0f172a; }}
.edu-section p {{ margin: 0; font-size: 14px; color: #334155; line-height: 1.7; }}
.related {{ margin-top: 40px; padding-top: 32px; border-top: 2px solid #eee; }}
.related h3 {{ font-size: 20px; margin: 0 0 16px 0; }}
.related-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
.related-link {{ display: block; padding: 14px; background: #f8f9fa; border: 1px solid #e1e4e8; border-radius: 8px; text-decoration: none; color: #0073e6; font-weight: 600; }}
footer {{ max-width: 800px; margin: 60px auto 40px; padding: 30px 20px; text-align: center; color: #888; font-size: 13px; }}
footer a {{ color: #0073e6; text-decoration: none; }}
.footer-divider {{ height: 1px; background: linear-gradient(to right, transparent, #ccc, transparent); margin-bottom: 30px; }}
.footer-branding {{ font-size: 14px; color: #888; margin-bottom: 10px; text-align: center; }}
.footer-branding strong {{ color: #444; letter-spacing: 0.5px; }}
.footer-copyright {{ font-size: 12px; color: #aaa; text-align: center; }}
@media (max-width: 768px) {{ article {{ padding: 24px 20px; }} h1 {{ font-size: 24px; }} .intro {{ padding: 16px; }} .puzzle-image {{ max-width: 100%; }} footer {{ padding: 0 12px; }} }}
</style>
<link rel="stylesheet" href="../banner.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{escape(title)}","datePublished":"{date_iso}","author":{{"@type":"Organization","name":"십자가로세로"}},"publisher":{{"@type":"Organization","name":"십자가로세로"}},"mainEntityOfPage":"{DOMAIN}/posts/{slug}.html","image":"{og_img}"}}
</script>
</head>
<body>
<nav class="nav">
  <a href="../index.html" class="nav-item">홈</a>
  <a href="../play.html" class="nav-item">퍼즐하기</a>
  <a href="../list.html" class="nav-item">퍼즐목록</a>
  <a href="index.html" class="nav-item nav-active">게시판</a>
  <a href="../sunday-school-materials.html" class="nav-item">주일학교 자료</a>
  <a href="../about.html" class="nav-item">소개</a>
  <a href="../support.html" class="nav-item">후원</a>
  <a href="../faq.html" class="nav-item">FAQ</a>
</nav>
<main>
<div class="banner-mobile-slot"><div id="top-banner-pc" class="top-banner top-banner-pc" aria-label="배너"></div><div id="top-banner-mobile" class="top-banner top-banner-mobile" aria-label="배너"></div></div>
<article>
<h1>{escape(title)}</h1>
<div class="meta">📅 {date_str} · 📁 {cat_esc} · 🧩 {hint_count}개 힌트</div>
<div class="intro">{intro}</div>
<img src="{img_rel}" alt="{escape(img_alt)}" class="puzzle-image" width="420" height="420" loading="lazy">
<div class="hints-section">
<h2 class="hints-title">📝 가로 힌트</h2>
<div class="hints-list">{across_html}</div>
</div>
<div class="hints-section">
<h2 class="hints-title">📝 세로 힌트</h2>
<div class="hints-list">{down_html}</div>
</div>
<div class="answer-section">
<h3>🧩 {section_heading}</h3>
<p>{section_desc}</p>
<a href="{answer_link}" target="_blank" rel="noopener noreferrer" class="answer-btn">{btn_text}</a>
</div>
<div class="edu-section">
<h3>🧑‍🏫 교회 교육 자료 활용</h3>
<p>이 퍼즐은 <strong>주일학교 교재 추천</strong> 자료로 활용할 수 있고, <strong>주일학교 주보</strong>에 넣기 좋은 분량으로 구성되어 있습니다. 수업용 <strong>주일학교 교안</strong>에 활동지로 붙이거나, 예배 후 복습용 <strong>주일학교 공과교재</strong>로 바로 사용할 수 있습니다.</p>
</div>
<div class="keywords-section">
<h3>🏷️ 키워드</h3>
<p>{escape(keyword)}, {escape(book)}, 십자가로세로, 성경퀴즈, 말씀퀴즈, 가로세로퍼즐, 주일학교 교재 추천, 주일학교 주보, 주일학교 교안, 주일학교 공과교재</p>
</div>
<div class="related">
<h3>📚 더 많은 퍼즐</h3>
<div class="related-grid">
<a href="../list.html" class="related-link">📋 전체 목록</a>
<a href="index.html" class="related-link">📋 게시판</a>
<a href="../sunday-school-materials.html" class="related-link">🧑‍🏫 주일학교 자료 모음</a>
<a href="../index.html" class="related-link">🏠 홈</a>
<a href="../about.html" class="related-link">소개</a>
</div>
</div>
</article>
</main>
<footer>
  <div class="footer-divider"></div>
  <div style="display: flex; gap: 12px; justify-content: center; margin-bottom: 20px;">
    <a href="../about.html" style="flex: 1; max-width: 180px; text-align: center; padding: 10px; background: #fff; border: 1px solid #ddd; color: #555; text-decoration: none; border-radius: 8px; font-size: 13px;">📖 만든 이유</a>
    <a href="../support.html" style="flex: 1; max-width: 180px; text-align: center; padding: 10px; background: #fff; border: 1px solid #0073e6; color: #0073e6; text-decoration: none; border-radius: 8px; font-size: 13px; font-weight: bold;">🙏 후원 응원</a>
  </div>
  <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 16px;">
    <a href="../terms.html" style="font-size: 13px; color: #666; text-decoration: none;">이용약관</a>
    <a href="../privacy.html" style="font-size: 13px; color: #666; text-decoration: none;">개인정보처리방침</a>
    <a href="../faq.html" style="font-size: 13px; color: #666; text-decoration: none;">FAQ</a>
    <a href="mailto:mandubird@naver.com" style="font-size: 13px; color: #666; text-decoration: none;">문의</a>
  </div>
  <p class="footer-coupang-disclaimer" style="font-size: 11px; color: #999; margin: 0 0 16px 0; line-height: 1.4;">이 사이트는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
  <div class="footer-branding">Crossero Puzzle <strong>Engine by PuzDuk.com</strong></div>
  <div class="footer-copyright">&copy; 2026 십자가로세로. All rights reserved.</div>
</footer>
<script src="../coupang-partner.js"></script>
</body>
</html>"""


def init_schedule():
    """posts_schedule.json 생성: 287개 퍼즐을 날짜별 1개씩 배정"""
    puzzles = parse_data_js(DATA_JS)
    seen = {}
    for p in puzzles:
        seen[p['id']] = p
    ids = sorted(seen.keys())
    schedule = {}
    d = START_DATE
    idx = 0
    while idx < len(ids):
        n = random.randint(POSTS_PER_DAY[0], POSTS_PER_DAY[1])
        chunk = ids[idx:idx + n]
        schedule[d.strftime('%Y-%m-%d')] = chunk
        idx += len(chunk)
        d += timedelta(days=1)
    with open(SCHEDULE_PATH, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(f"✅ 스케줄 생성: {SCHEDULE_PATH} ({len(schedule)}일, 총 {len(ids)}개)")


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_manifest(entries):
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def rebuild_index_and_xml(manifest_entries):
    """발행된 글만으로 posts/index.html, posts.xml 재생성 (날짜 반영)"""
    os.makedirs(POSTS_DIR, exist_ok=True)
    # 최신순
    entries = sorted(manifest_entries, key=lambda x: (x['date'], x['slug']), reverse=True)

    with open(os.path.join(SCRIPT_DIR, 'posts.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for e in entries:
            f.write(f'  <url>\n')
            f.write(f'    <loc>{DOMAIN}/posts/{e["slug"]}.html</loc>\n')
            f.write(f'    <lastmod>{e["date"]}</lastmod>\n')
            f.write(f'    <changefreq>weekly</changefreq>\n')
            f.write(f'    <priority>0.7</priority>\n')
            f.write(f'  </url>\n')
        f.write('</urlset>\n')

    def _date_str(d):
        parts = d["date"].split("-")
        if len(parts) == 3:
            y, m, d = parts[0], int(parts[1]), int(parts[2])
            return f"{y}년 {m}월 {d}일"
        return d["date"]

    list_rows = "".join(
        f'<li><a href="{escape(e["slug"])}.html" class="board-card">'
        f'<span class="board-title">{escape(e["title"])}</span>'
        f'<span class="board-date">{_date_str(e)}</span></a></li>\n'
        for e in entries
    )
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>주일학교 자료 게시판 | 십자가로세로</title>
<meta name="description" content="주일학교 교재 추천, 주일학교 주보, 주일학교 교안, 주일학교 공과교재로 활용 가능한 성경 퍼즐 게시판입니다.">
<meta name="keywords" content="주일학교 교재 추천, 주일학교 주보, 주일학교 교안, 주일학교 공과교재, 성경퀴즈 게시판">
<meta property="og:title" content="주일학교 자료 게시판 | 십자가로세로">
<meta property="og:description" content="주일학교/교회 교육에 바로 쓸 수 있는 성경 퍼즐 자료 게시판입니다.">
<meta property="og:image" content="{DOMAIN}/images/og-image.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/posts/">
<link rel="canonical" href="{DOMAIN}/posts/">
<style>
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, Pretendard, sans-serif; margin: 0; background: #f5f5f5; color: #333; line-height: 1.6; }}
.nav {{ display: flex; justify-content: center; gap: 10px; background: #fff; border-bottom: 1px solid #e5e5e5; padding: 12px 0; }}
.nav-item {{ padding: 8px 14px; font-size: 14px; color: #444; text-decoration: none; border-radius: 6px; }}
.nav-item:hover {{ background: #f0f6ff; color: #0073e6; }}
.nav-active {{ background: #0073e6; color: #fff !important; font-weight: 600; }}
main {{ max-width: 820px; margin: 0 auto; padding: 40px 20px; }}
.page-title {{ font-size: 24px; margin: 0 0 8px 0; color: #222; font-weight: 700; }}
.intro {{ color: #666; margin-bottom: 28px; font-size: 15px; }}
.intro a {{ color: #0073e6; text-decoration: none; font-weight: 500; }}
.intro a:hover {{ text-decoration: underline; }}
.board-section {{ background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e5e5e5; }}
.board-list {{ list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }}
.board-card {{ display: flex; flex-direction: column; align-items: flex-start; background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px 18px; text-decoration: none; color: inherit; transition: all 0.2s; min-height: 80px; }}
.board-card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,115,230,0.15); border-color: #0073e6; background: #fff; }}
.board-title {{ font-size: 15px; font-weight: 600; color: #0073e6; text-align: left; margin: 0; flex: 1; }}
.board-card:hover .board-title {{ color: #005bb5; }}
.board-date {{ font-size: 12px; color: #888; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #e0e0e0; width: 100%; }}
.board-card:hover .board-date {{ border-top-color: #e8eef5; }}
.footer-divider {{ height: 1px; background: linear-gradient(to right, transparent, #ccc, transparent); margin-bottom: 30px; }}
.footer-branding {{ font-size: 14px; color: #888; margin-bottom: 10px; text-align: center; }}
.footer-branding strong {{ color: #444; }}
.footer-copyright {{ font-size: 12px; color: #aaa; text-align: center; }}
@media (max-width: 768px) {{ .nav {{ padding: 8px 6px; gap: 6px; }} .nav-item {{ padding: 6px 10px; font-size: 12px; }} main {{ padding: 24px 16px; }} .page-title {{ font-size: 20px; }} .board-section {{ padding: 18px 16px; }} .board-list {{ grid-template-columns: 1fr; }} .board-card {{ padding: 14px 16px; }} .board-title {{ font-size: 14px; }} .board-date {{ font-size: 11px; margin-top: 8px; padding-top: 6px; }} }}
</style>
<link rel="stylesheet" href="../banner.css">
</head>
<body>
<nav class="nav">
  <a href="../index.html" class="nav-item">홈</a>
  <a href="../play.html" class="nav-item">퍼즐하기</a>
  <a href="../list.html" class="nav-item">퍼즐목록</a>
  <a href="index.html" class="nav-item nav-active">게시판</a>
  <a href="../sunday-school-materials.html" class="nav-item">주일학교 자료</a>
  <a href="../about.html" class="nav-item">소개</a>
  <a href="../support.html" class="nav-item">후원</a>
  <a href="../faq.html" class="nav-item">FAQ</a>
</nav>
<div class="top-banner-wrap">
  <div id="top-banner-pc" class="top-banner top-banner-pc" aria-label="배너"></div>
  <div id="top-banner-mobile" class="top-banner top-banner-mobile" aria-label="배너"></div>
</div>
<main>
<h1 class="page-title">주일학교 자료 게시판</h1>
<p class="intro">매일 발행되는 성경 퍼즐 자료입니다. <strong>주일학교 교재 추천</strong>, <strong>주일학교 주보</strong>, <strong>주일학교 교안</strong>, <strong>주일학교 공과교재</strong> 용도로 활용할 수 있습니다. <a href="../sunday-school-materials.html">주일학교 자료 모음</a>도 함께 보세요.</p>
<div class="board-section">
<ul class="board-list">
{list_rows}
</ul>
</div>
</main>
<footer>
  <div class="footer-divider"></div>
  <div style="display: flex; gap: 12px; justify-content: center; margin-bottom: 20px;">
    <a href="../about.html" style="flex: 1; max-width: 180px; text-align: center; padding: 10px; background: #fff; border: 1px solid #ddd; color: #555; text-decoration: none; border-radius: 8px; font-size: 13px;">📖 만든 이유</a>
    <a href="../support.html" style="flex: 1; max-width: 180px; text-align: center; padding: 10px; background: #fff; border: 1px solid #0073e6; color: #0073e6; text-decoration: none; border-radius: 8px; font-size: 13px; font-weight: bold;">🙏 후원 응원</a>
  </div>
  <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 16px;">
    <a href="../terms.html" style="font-size: 13px; color: #666; text-decoration: none;">이용약관</a>
    <a href="../privacy.html" style="font-size: 13px; color: #666; text-decoration: none;">개인정보처리방침</a>
    <a href="../faq.html" style="font-size: 13px; color: #666; text-decoration: none;">FAQ</a>
    <a href="mailto:mandubird@naver.com" style="font-size: 13px; color: #666; text-decoration: none;">문의</a>
  </div>
  <p class="footer-coupang-disclaimer" style="font-size: 11px; color: #999; margin: 0 0 16px 0; line-height: 1.4;">이 사이트는 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
  <div class="footer-branding">Crossero Puzzle <strong>Engine by PuzDuk.com</strong></div>
  <div class="footer-copyright">&copy; 2026 십자가로세로. All rights reserved.</div>
</footer>
<script src="../coupang-partner.js"></script>
</body>
</html>"""
    with open(os.path.join(POSTS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("  → posts/index.html, posts.xml 갱신 완료 (발행된 글만 반영)")


def publish_today(force_date=None):
    """force_date: 'YYYY-MM-DD' (테스트용). 없으면 오늘."""
    today = force_date or datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(SCHEDULE_PATH):
        print("❌ posts_schedule.json 없음. 먼저 실행: python3 auto_publish_with_images.py init")
        return
    with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
        schedule = json.load(f)
    today_ids = schedule.get(today, [])
    if not today_ids:
        print(f"오늘({today}) 예약된 퍼즐 없음. 완료.")
        # 기존 발행 목록으로만 index/xml 유지
        rebuild_index_and_xml(load_manifest())
        return

    # 최종 결과물(퍼즐 이미지 + 이 퍼즐 풀어보기)을 내려면 Playwright 필수. og 이미지로 대체하지 않음.
    if not HAS_PLAYWRIGHT:
        print("❌ 발행 중단: Playwright가 없습니다. 최종 결과물(퍼즐 이미지 + 이 퍼즐 풀어보기)을 내려면 필수입니다.")
        print("   설치: pip install playwright && playwright install chromium")
        rebuild_index_and_xml(load_manifest())
        return
    os.makedirs(PUZZLES_IMG_DIR, exist_ok=True)

    puzzles = parse_data_js(DATA_JS)
    by_id = {p['id']: p for p in puzzles}
    manifest = load_manifest()
    published_slugs = {e['slug'] for e in manifest}
    os.makedirs(POSTS_DIR, exist_ok=True)

    try:
        publish_date = datetime.strptime(today, '%Y-%m-%d')
    except ValueError:
        publish_date = datetime.now()
    for pid in today_ids:
        puzzle = by_id.get(pid)
        if not puzzle:
            continue
        keyword = get_keyword_for_puzzle(puzzle)
        book = puzzle['title'].split(':')[0].strip() if ':' in puzzle['title'] else puzzle['title'].split()[0]
        display_title = (puzzle.get('title') or '').strip() or f"{book} 퀴즈"
        slug = make_slug_from_title(display_title)
        if not slug:
            slug = f"puzzle-{pid}"
        if slug in published_slugs:
            slug = f"{slug}-{pid}"
        published_slugs.add(slug)

        hint_count = len(puzzle.get('hints') or [])
        has_img = False
        export_across, export_down, answer_url = None, None, ''
        export_hints_with_num = None
        image_slug = make_image_slug(puzzle)  # 제목-십자가로세로.png
        if HAS_PLAYWRIGHT:
            ok, export_across, export_down, answer_url, play_hints_json = export_puzzle_image_via_browser(pid, image_slug)
            if ok:
                print(f"  🎨 이미지 생성(play2): {image_slug}.png")
                has_img = True
                if play_hints_json:
                    try:
                        export_hints_with_num = json.loads(play_hints_json)
                    except Exception:
                        pass
        if not has_img and HAS_PILLOW:
            generate_puzzle_grid_image(image_slug, hint_count)
            print(f"  🎨 이미지 생성(Pillow): {image_slug}.png")
            has_img = True
        if not has_img:
            print(f"  ⚠️ Playwright/Pillow 미설치 → og 이미지 사용")
        html = generate_post_html_with_image(
            puzzle, keyword, slug, publish_date, image_slug, has_puzzle_image=has_img,
            display_title=display_title,
            export_across=export_across, export_down=export_down, answer_link_override=answer_url or None,
            export_hints_with_num=export_hints_with_num
        )
        path = os.path.join(POSTS_DIR, f"{slug}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        img_note = f" (이미지: {slug}.png)" if has_img else ""
        print(f"  ✅ 발행: {slug}.html{img_note}")

        manifest.append({
            'slug': slug,
            'date': today,
            'id': pid,
            'title': display_title,
        })

    save_manifest(manifest)
    rebuild_index_and_xml(manifest)
    print(f"\n🎉 완료! 오늘 {len(today_ids)}개 발행 (총 발행 {len(manifest)}개)")


def publish_catchup():
    """놓친 과거 날짜를 한꺼번에 발행 (스케줄에 있지만 아직 manifest에 없는 날짜)"""
    if not os.path.exists(SCHEDULE_PATH):
        print("❌ posts_schedule.json 없음. 먼저 실행: python3 auto_publish_with_images.py init")
        return
    with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
        schedule = json.load(f)
    manifest = load_manifest()
    published_dates = {e['date'] for e in manifest}
    today = datetime.now().strftime('%Y-%m-%d')
    to_publish = sorted(
        d for d in schedule.keys()
        if d <= today and d not in published_dates
    )
    if not to_publish:
        print("놓친 날짜 없음. 완료.")
        return
    print(f"📅 놓친 날짜 {len(to_publish)}일 발행 예정: {to_publish[0]} ~ {to_publish[-1]}")
    for d in to_publish:
        print(f"\n--- {d} ---")
        publish_today(force_date=d)
    print(f"\n🎉 캐치업 완료: {len(to_publish)}일 발행됨")


def main():
    import sys
    if len(sys.argv) > 1:
        arg1 = sys.argv[1].strip().lower()
        if arg1 == 'init':
            init_schedule()
            return
        if arg1 == 'catchup':
            publish_catchup()
            return
    # 테스트: python3 auto_publish_with_images.py --date=2026-02-20
    force = None
    for arg in sys.argv[1:]:
        if arg.startswith('--date='):
            force = arg.split('=', 1)[1].strip()
            break
    publish_today(force_date=force)


if __name__ == '__main__':
    main()
