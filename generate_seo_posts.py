#!/usr/bin/env python3
"""
SEO 게시글 일괄 생성 (data.js 기반)
- posts/*.html 287개 생성
- posts.xml (사이트맵)
- posts/index.html (목록)
"""
import os
import re
import random
from datetime import datetime
from html import escape

DOMAIN = "https://crossero.com"
LASTMOD = "2026-02-14"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. data.js 파싱
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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

def parse_data_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    puzzles = []
    # "id": { ... }, 패턴 찾기 (키만 따옴표)
    pattern = re.compile(r'"([a-zA-Z0-9_]+)"\s*:\s*\{')
    pos = 0
    while True:
        m = pattern.search(content, pos)
        if not m:
            break
        pid = m.group(1)
        start = m.end() - 1  # '{' 위치
        end = find_matching_brace(content, start, '{', '}')
        if end == -1:
            pos = m.end()
            continue
        block = content[start:end+1]
        # title: "..." 추출
        t = re.search(r'title:\s*"([^"]*)"', block)
        title = t.group(1) if t else pid
        # category: "..." 추출
        c = re.search(r'category:\s*"([^"]*)"', block)
        category = c.group(1) if c else "성경"
        # allWords: [ ... ] 추출 후 clue, answer 파싱 (block 내에서)
        aw = re.search(r'allWords:\s*\[', block)
        hints = []
        if aw:
            arr_start = aw.end() - 1  # '[' 위치
            arr_end = find_matching_brace(block, arr_start, '[', ']')
            if arr_end != -1:
                arr_content = block[arr_start:arr_end+1]
                for hint_m in re.finditer(r'clue:\s*"([^"]*)"', arr_content):
                    hints.append(f"{len(hints)+1}. {hint_m.group(1)}")
        puzzles.append({
            'id': pid,
            'title': title,
            'category': category,
            'hints': hints,
        })
        pos = end + 1
    return puzzles

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 소개글·키워드
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTRO_TEMPLATES = [
    "{book}를 주제로 한 <strong>{keyword}</strong>입니다. {hint_count}개의 단어를 맞춰보세요! 가로세로 낱말 퍼즐 형식으로 {book}의 핵심 내용을 재미있게 복습할 수 있습니다.",
    "오늘은 {book}의 주요 내용을 담은 <strong>{keyword}</strong>를 준비했습니다. 총 {hint_count}개의 힌트가 있으며, 주일학교 교재나 성경공부 자료로 활용하기 좋습니다. 무료로 즐기는 {book} 가로세로 퍼즐을 지금 바로 풀어보세요!",
    "{book}의 말씀을 퀴즈로 배우는 <strong>{keyword}</strong>입니다. 가로 힌트와 세로 힌트를 보고 {hint_count}개의 단어를 맞춰보세요. 인쇄도 가능하고 정답 확인도 바로 되니 소그룹 모임이나 가정 예배 시간에도 활용하실 수 있습니다.",
    "무료로 즐기는 {book} <strong>{keyword}</strong>! {hint_count}개의 힌트로 구성된 가로세로 낱말 퍼즐입니다. PC와 모바일 모두 지원되며, 정답을 바로 확인할 수 있어 혼자서도 쉽게 풀 수 있습니다.",
]
KEYWORDS_BY_PREFIX = [
    "성경퀴즈", "가로세로 퀴즈", "말씀 퀴즈", "성경 퍼즐", "무료 성경퀴즈",
    "주일학교 퀴즈", "성경공부 자료", "낱말 퍼즐", "성경 퀴즈 문제",
]

def make_slug(text):
    slug = re.sub(r'[^\w\s\-가-힣]', '', text)
    slug = slug.strip().replace(' ', '-')[:80]
    return slug or 'puzzle'

def get_keyword(puzzle):
    book = puzzle['title'].split(':')[0].strip() if ':' in puzzle['title'] else puzzle['title'].split()[0]
    kw = random.choice(KEYWORDS_BY_PREFIX)
    return f"{book} {kw}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. HTML 생성
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generate_post_html(puzzle, keyword, date, slug):
    book = puzzle['title'].split(':')[0].strip() if ':' in puzzle['title'] else puzzle['title'].split()[0]
    pid = puzzle['id']
    hints = puzzle['hints']
    hint_count = len(hints)
    intro = random.choice(INTRO_TEMPLATES).format(book=book, keyword=keyword, hint_count=hint_count)
    title = f"{book} {keyword} - 십자가로세로"
    img_src = "images/og-image.png"  # 공통 og 이미지 (퍼즐별 이미지 없으면)
    img_alt = escape(f"{book} {keyword} - 무료 온라인 가로세로 낱말퍼즐")
    answer_link = f"{DOMAIN}/play.html?id={pid}"
    hint_items = "".join(f'<div class="hint-item">{escape(h)}</div>' for h in hints[:30])  # 최대 30개
    if not hint_items:
        hint_items = f'<div class="hint-item">힌트는 퍼즐 플레이 화면에서 확인하세요.</div>'
    date_iso = date.strftime('%Y-%m-%d')
    date_str = date.strftime('%Y년 %m월 %d일')
    cat_esc = escape(puzzle.get('category', '성경')[:50])

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(book)}를 주제로 한 {escape(keyword)}입니다. {hint_count}개의 힌트로 구성된 무료 가로세로 낱말 퍼즐.">
<meta name="keywords" content="{escape(keyword)}, {escape(book)}, 십자가로세로, 성경퀴즈, 말씀퀴즈, 가로세로퍼즐">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(book)} {escape(keyword)} - 무료 퀴즈">
<meta property="og:image" content="{DOMAIN}/images/og-image.png">
<meta property="og:type" content="article">
<meta property="og:url" content="{DOMAIN}/posts/{slug}.html">
<meta property="article:published_time" content="{date_iso}">
<link rel="canonical" href="{DOMAIN}/posts/{slug}.html">
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: -apple-system, "Pretendard", sans-serif; background: #f5f5f5; color: #333; line-height: 1.8; }}
header {{ background: #fff; border-bottom: 2px solid #0073e6; padding: 20px; text-align: center; }}
header a {{ color: #0073e6; text-decoration: none; font-weight: 700; font-size: 24px; }}
main {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
article {{ background: #fff; border-radius: 12px; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
h1 {{ font-size: 28px; font-weight: 800; color: #222; margin: 0 0 16px 0; }}
.meta {{ color: #888; font-size: 14px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #eee; }}
.intro {{ font-size: 17px; line-height: 1.9; color: #444; margin-bottom: 32px; padding: 20px; background: #f8f9fa; border-left: 4px solid #0073e6; border-radius: 4px; }}
.intro strong {{ color: #0073e6; }}
.hints-section {{ margin: 32px 0; }}
.hints-title {{ font-size: 20px; font-weight: 700; color: #222; margin: 0 0 12px 0; padding-left: 12px; border-left: 4px solid #0073e6; }}
.hints-list {{ background: #fafbfc; padding: 24px; border-radius: 8px; border: 1px solid #e1e4e8; }}
.hint-item {{ padding: 10px 0; color: #444; font-size: 15px; border-bottom: 1px dashed #e1e4e8; }}
.hint-item:last-child {{ border-bottom: none; }}
.answer-section {{ margin: 40px 0; padding: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center; color: #fff; }}
.answer-section h3 {{ font-size: 22px; margin: 0 0 12px 0; }}
.answer-btn {{ display: inline-block; padding: 16px 40px; background: #fff; color: #667eea; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 16px; }}
.related {{ margin-top: 40px; padding-top: 32px; border-top: 2px solid #eee; }}
.related h3 {{ font-size: 20px; margin: 0 0 16px 0; }}
.related-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
.related-link {{ display: block; padding: 14px; background: #f8f9fa; border: 1px solid #e1e4e8; border-radius: 8px; text-decoration: none; color: #0073e6; font-weight: 600; }}
footer {{ max-width: 800px; margin: 60px auto 40px; padding: 30px 20px; text-align: center; color: #888; font-size: 13px; }}
footer a {{ color: #0073e6; text-decoration: none; }}
@media (max-width: 768px) {{ article {{ padding: 24px 20px; }} h1 {{ font-size: 24px; }} .intro {{ padding: 16px; }} }}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{escape(title)}","datePublished":"{date_iso}","author":{{"@type":"Organization","name":"십자가로세로"}},"publisher":{{"@type":"Organization","name":"십자가로세로"}},"mainEntityOfPage":"{DOMAIN}/posts/{slug}.html"}}
</script>
</head>
<body>
<header><a href="{DOMAIN}">✙ 십자가로세로</a></header>
<main>
<article>
<h1>{escape(title)}</h1>
<div class="meta">📅 {date_str} · 📁 {cat_esc} · 🧩 {hint_count}개 힌트</div>
<div class="intro">{intro}</div>
<div class="hints-section">
<h2 class="hints-title">📝 힌트</h2>
<div class="hints-list">{hint_items}</div>
</div>
<div class="answer-section">
<h3>🔍 정답 확인</h3>
<p>아래 버튼을 누르면 퍼즐 플레이 화면에서 정답을 볼 수 있습니다.</p>
<a href="{answer_link}" target="_blank" rel="noopener noreferrer" class="answer-btn">▶ 정답 확인하기 (새창)</a>
</div>
<div class="related">
<h3>📚 더 많은 퍼즐</h3>
<div class="related-grid">
<a href="../list.html" class="related-link">📋 전체 목록</a>
<a href="../index.html" class="related-link">🏠 홈</a>
<a href="../about.html" class="related-link">소개</a>
</div>
</div>
</article>
</main>
<footer><p><strong>십자가로세로</strong> - 무료 성경 가로세로 낱말 퍼즐</p><p><a href="{DOMAIN}">홈</a> · <a href="../about.html">소개</a> · <a href="../support.html">후원</a></p><p>&copy; 2026 십자가로세로</p></footer>
</body>
</html>"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 메인
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_js = os.path.join(script_dir, 'data.js')
    posts_dir = os.path.join(script_dir, 'posts')
    os.makedirs(posts_dir, exist_ok=True)

    print("data.js 파싱 중...")
    puzzles = parse_data_js(data_js)
    # 중복 id 제거 (마지막 것만 유지)
    seen = {}
    for p in puzzles:
        seen[p['id']] = p
    puzzles = list(seen.values())
    puzzles.sort(key=lambda x: x['id'])
    print(f"  → {len(puzzles)}개 퍼즐 로드")

    date = datetime.now()
    entries = []
    for i, puzzle in enumerate(puzzles):
        keyword = get_keyword(puzzle)
        slug = make_slug(f"{puzzle['id']}-{puzzle['title'][:30]}-{keyword[:20]}")
        slug = slug or f"post-{puzzle['id']}"
        # 파일명 길이 제한, 중복 방지
        if len(slug) > 60:
            slug = slug[:60]
        base = slug
        idx = 0
        while os.path.exists(os.path.join(posts_dir, f"{slug}.html")):
            idx += 1
            slug = f"{base}-{idx}"
        html = generate_post_html(puzzle, keyword, date, slug)
        path = os.path.join(posts_dir, f"{slug}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        entries.append({'slug': slug, 'title': puzzle['title'], 'keyword': keyword})
        if (i + 1) % 50 == 0:
            print(f"  생성 {i+1}/{len(puzzles)}...")

    # posts.xml (사이트맵)
    xml_path = os.path.join(script_dir, 'posts.xml')
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for e in entries:
            f.write(f'  <url>\n')
            f.write(f'    <loc>{DOMAIN}/posts/{e["slug"]}.html</loc>\n')
            f.write(f'    <lastmod>{LASTMOD}</lastmod>\n')
            f.write(f'    <changefreq>weekly</changefreq>\n')
            f.write(f'    <priority>0.7</priority>\n')
            f.write(f'  </url>\n')
        f.write('</urlset>\n')
    print(f"  → posts.xml 작성 완료")

    # posts/index.html (목록)
    list_items = "".join(
        f'<li><a href="{e["slug"]}.html">{escape(e["title"])} – {escape(e["keyword"])}</a></li>\n'
        for e in entries[:200]  # 상위 200개만 목록
    )
    if len(entries) > 200:
        list_items += f'<li>… 외 {len(entries)-200}개 (전체는 <a href="../list.html">퍼즐 목록</a>에서)</li>'
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>퍼즐 게시글 목록 | 십자가로세로</title>
<link rel="canonical" href="{DOMAIN}/posts/">
<style>
body {{ font-family: -apple-system, sans-serif; margin: 0; background: #f5f5f5; padding: 20px; }}
header {{ text-align: center; margin-bottom: 24px; }}
header a {{ color: #0073e6; text-decoration: none; font-size: 24px; font-weight: bold; }}
main {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 32px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
h1 {{ font-size: 22px; margin: 0 0 20px 0; }}
ul {{ list-style: none; padding: 0; }}
li {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
li a {{ color: #0073e6; text-decoration: none; }}
li a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<header><a href="{DOMAIN}">✙ 십자가로세로</a></header>
<main>
<h1>📋 퍼즐 게시글 목록</h1>
<p>성경 퀴즈·가로세로 퍼즐 관련 SEO 게시글입니다. <a href="../list.html">퍼즐 목록</a>에서 바로 플레이할 수 있습니다.</p>
<ul>
{list_items}
</ul>
</main>
</body>
</html>"""
    with open(os.path.join(posts_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"  → posts/index.html 작성 완료")

    print(f"\n✅ 완료: {len(entries)}개 게시글, posts.xml, posts/index.html")

if __name__ == '__main__':
    main()
