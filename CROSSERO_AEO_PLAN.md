# Crossero AI 검색 최적화 (AEO) 개발계획서

## 목표
ChatGPT, Perplexity, Gemini 등 AI 검색 엔진에서 crossero.com이 **직접 인용되는 출처**가 되도록 최적화

---

## 1. 현재 상황

### 구현 완료 ✅
- FAQ 페이지 기본 구조
- FAQPage Schema 적용
- Dataset Schema 기본형
- HowTo Schema 기본형

### 문제점 ❌
- AI가 인용할 만한 콘텐츠 부족
- URL 구조가 의미 없음 (`play.html?id=1`)
- 이미지 메타데이터 최적화 안 됨
- 퍼즐별 구조화 데이터 없음

---

## 1-2. 당신이 할 일 (수동 등록·제출)

AEO/SEO 효과를 보려면 **한 번만** 아래 작업을 해 두는 것이 좋습니다. (코드/자동화와 별개)

| 순서 | 할 일 | 링크/비고 |
|------|--------|-----------|
| 1 | ~~**Google Search Console** 사이트 등록~~ | ✅ 완료 (crossero.com 등록됨) |
| 2 | ~~**Google** sitemap 제출~~ | ✅ 완료 ([sitemap.xml](https://crossero.com/sitemap.xml) 구글콘솔에 제출됨) |
| 3 | ~~**Naver Search Advisor** 사이트 등록~~ | ✅ 완료 |
| 4 | ~~**네이버** 사이트맵 제출~~ | ✅ 완료 |
| 5 | **Bing Webmaster Tools** 사이트 등록 (선택) | [bing.com/webmasters](https://www.bing.com/webmasters) → 사이트 추가. Bing Chat/Copilot 인용에 도움 됨 |
| 6 | **Bing** sitemap 제출 (선택) | Webmaster Tools 내 **Sitemaps**에 sitemap.xml, posts.xml 제출 |

**※ 도메인 통일**: 301 설정 없이 적용하기 쉽도록 **non-www(https://crossero.com) 기준**으로 통일함. 구글·네이버에 **https://crossero.com** 으로 등록해 사용하면 됨.

**추가(선택):**
- GSC/네이버에서 **URL 검사**로 메인 URL(홈, list, play?id=gen_001 등) 색인 요청
- 나중에 **Semantic URL**로 바꿀 경우: GSC **URL 변경 도구**로 이전 주소 → 새 주소 이동 신고

---

## 2. 구조화 데이터 확장 전략

### 2-1. Dataset Schema 고도화 ⭐⭐⭐

**목표:** 각 퍼즐을 독립적인 데이터셋으로 인식시키기

#### A. 현재 (기본형)
```javascript
{
  "@type": "Dataset",
  "name": "Crossero Bible Crossword Dataset",
  "description": "성경전서 개역한글판을 기반으로..."
}
```

#### B. 개선 (퍼즐별)
```javascript
// play.html?id=gen_001에 추가
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "창세기 성경 가로세로 퍼즐 데이터셋",
  "description": "창세기 핵심 인물, 사건, 지명을 기반으로 제작된 교육용 가로세로 퍼즐 문제 20개",
  "creator": {
    "@type": "Organization",
    "name": "십자가로세로",
    "url": "https://crossero.com"
  },
  "keywords": ["창세기", "성경 퀴즈", "가로세로 퍼즐", "주일학교 자료"],
  "license": "https://crossero.com/about.html",
  "url": "https://crossero.com/play.html?id=gen_001",
  "temporalCoverage": "2024/2026",
  "spatialCoverage": "대한민국",
  "hasPart": [
    {
      "@type": "Question",
      "name": "최초의 인간은?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "아담"
      }
    },
    {
      "@type": "Question",
      "name": "홍수 심판의 주인공은?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "노아"
      }
    }
  ]
}
```

**구현 파일:**
```javascript
// play.html에 추가할 함수
function generateDatasetSchema(puzzleData) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": `${puzzleData.title} 성경 가로세로 퍼즐 데이터셋`,
    "description": `${puzzleData.title}의 핵심 내용을 기반으로 제작된 교육용 가로세로 퍼즐`,
    "creator": {
      "@type": "Organization",
      "name": "십자가로세로",
      "url": "https://crossero.com"
    },
    "keywords": [puzzleData.title, "성경 퀴즈", "가로세로 퍼즐"],
    "url": `https://crossero.com/play.html?id=${puzzleData.id}`,
    "hasPart": puzzleData.allWords.slice(0, 5).map(word => ({
      "@type": "Question",
      "name": word.clue,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": word.answer
      }
    }))
  };
  
  // <head>에 삽입
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(schema);
  document.head.appendChild(script);
}
```

**배포 계획:**
- [x] Week 1: play.html에 자동 생성 함수 추가 ✅
- [ ] Week 2: 287개 퍼즐 전체 적용
- [ ] Week 3: Google Rich Results 테스트

---

### 2-2. Quiz Schema 도입 ⭐⭐⭐

**목표:** AI가 "퀴즈 출처"로 인식

#### 구현
```javascript
// play.html에 추가
{
  "@context": "https://schema.org",
  "@type": "Quiz",
  "about": {
    "@type": "Thing",
    "name": "창세기"
  },
  "educationalAlignment": {
    "@type": "AlignmentObject",
    "alignmentType": "educationalSubject",
    "targetName": "성경 교육"
  },
  "hasPart": [
    {
      "@type": "Question",
      "eduQuestionType": "Multiple choice",
      "text": "최초의 인간은?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "아담"
      },
      "suggestedAnswer": [
        {"@type": "Answer", "text": "아담"},
        {"@type": "Answer", "text": "노아"},
        {"@type": "Answer", "text": "아브라함"}
      ]
    }
  ]
}
```

---

## 3. 답변형 텍스트 콘텐츠 확장

### 3-1. 플레이 페이지 하단 설명 추가 ⭐⭐⭐

**목표:** AI가 "요약"으로 인용할 수 있는 3~5문장 블록

#### 구현 위치
```html
<!-- play.html 퍼즐 아래에 추가 -->
<section class="puzzle-summary">
  <h2>창세기란?</h2>
  <p class="ai-friendly-summary">
    창세기는 성경의 첫 번째 권으로, 하나님이 세상을 창조하신 이야기로 시작합니다. 
    아담과 하와, 노아의 방주, 아브라함과 이삭, 야곱의 이야기를 포함하며, 
    이스라엘 민족의 기원을 다룹니다. 창세기는 총 50장으로 구성되어 있으며, 
    천지창조부터 요셉의 이집트 생애까지를 기록합니다.
  </p>
</section>

<style>
.puzzle-summary {
  margin: 40px 0;
  padding: 24px;
  background: #f8f9fa;
  border-left: 4px solid #0073e6;
  border-radius: 4px;
}
.ai-friendly-summary {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
}
</style>
```

#### 자동 생성 시스템
```python
# summary_generator.py
SUMMARIES = {
    'gen': """
        창세기는 성경의 첫 번째 권으로, 하나님이 세상을 창조하신 이야기로 시작합니다.
        아담과 하와, 노아의 방주, 아브라함과 이삭, 야곱의 이야기를 포함하며,
        이스라엘 민족의 기원을 다룹니다. 창세기는 총 50장으로 구성되어 있습니다.
    """,
    'exo': """
        출애굽기는 이스라엘 민족이 이집트의 노예 생활에서 해방되는 과정을 기록합니다.
        모세의 리더십, 열 가지 재앙, 홍해를 건너는 기적, 시내산에서 십계명을 받는
        사건이 핵심입니다. 출애굽기는 총 40장으로 구성되어 있습니다.
    """,
    # ... 287개 퍼즐 전체
}

def add_summary_to_html(puzzle_id):
    summary = SUMMARIES.get(puzzle_id[:3], "")
    return f"""
    <section class="puzzle-summary">
      <h2>{puzzle_title}란?</h2>
      <p class="ai-friendly-summary">{summary}</p>
    </section>
    """
```

**배포 계획:**
- [x] Week 1: 주요 66권 요약 작성 (성경 전체) — play.html + aeo_summaries.js 적용 ✅
- [x] Week 2: play.html 템플릿 수정 ✅
- [ ] Week 3: 287개 퍼즐 전체 적용

---

### 3-2. 인물별 요약 블록 생성 ⭐⭐

**목표:** "모세란 누구인가?" 같은 질문에 직접 답변 제공

#### 신규 페이지 생성
```
/bible-characters/moses.html
/bible-characters/david.html
/bible-characters/paul.html
```

#### 템플릿
```html
<!DOCTYPE html>
<html lang="ko">
<head>
<title>모세는 누구인가? | 십자가로세로 성경 인물 사전</title>
<meta name="description" content="모세는 이스라엘 민족을 이집트에서 이끌어낸 위대한 지도자이자 율법을 받은 선지자입니다.">
</head>
<body>

<article>
  <h1>모세는 누구인가?</h1>
  
  <section class="definition">
    <h2>모세의 정의</h2>
    <p class="ai-friendly-answer">
      모세는 기원전 13세기경 이스라엘 민족을 이집트 노예 생활에서 
      해방시킨 위대한 지도자이자 율법을 받은 선지자입니다. 
      출애굽기, 레위기, 민수기, 신명기를 기록했으며, 
      시내산에서 십계명을 받았습니다.
    </p>
  </section>
  
  <section class="key-events">
    <h2>모세의 주요 사건</h2>
    <ul>
      <li>나일강에 버려졌다가 바로의 공주에게 구출됨</li>
      <li>불붙는 떨기나무에서 하나님의 부르심을 받음</li>
      <li>열 가지 재앙으로 이집트를 심판</li>
      <li>홍해를 가르고 이스라엘 민족을 인도</li>
      <li>시내산에서 십계명을 받음</li>
    </ul>
  </section>
  
  <section class="related-puzzles">
    <h2>모세 관련 퍼즐</h2>
    <a href="/play.html?id=exo_001">출애굽기 퍼즐</a>
    <a href="/play.html?id=moses_life">모세의 생애 퍼즐</a>
  </section>
</article>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "모세",
  "description": "이스라엘 민족을 이집트에서 이끌어낸 지도자",
  "birthPlace": "이집트",
  "nationality": "이스라엘",
  "knowsAbout": ["율법", "십계명", "출애굽"]
}
</script>

</body>
</html>
```

**자동 생성:**
```python
# generate_character_pages.py
CHARACTERS = {
    'moses': {
        'name': '모세',
        'definition': '이스라엘 민족을 이집트에서 이끌어낸 지도자',
        'key_events': [
            '불붙는 떨기나무',
            '열 가지 재앙',
            '홍해를 가름',
            '십계명 수령'
        ],
        'related_puzzles': ['exo_001', 'moses_life']
    },
    'david': {
        'name': '다윗',
        'definition': '이스라엘의 위대한 왕이자 시편 저자',
        'key_events': [
            '골리앗을 물리침',
            '사울 왕을 섬김',
            '통일 왕국 건설',
            '시편 저작'
        ],
        'related_puzzles': ['sam_028', 'david_life']
    },
    # ... 주요 인물 30명
}

for char_id, data in CHARACTERS.items():
    generate_character_page(char_id, data)
```

**배포 계획:**
- [ ] Week 1: 주요 인물 30명 페이지 생성
- [ ] Week 2: Person Schema 적용
- [ ] Week 3: sitemap.xml에 추가

---

## 4. Semantic URL 구조 전환

### 4-1. 현재 문제
```
❌ crossero.com/play.html?id=gen_001
→ AI가 URL만 보고 내용 파악 불가
```

### 4-2. 개선안 ⭐⭐⭐

#### A. .htaccess 리다이렉트
```apache
# .htaccess
RewriteEngine On

# 성경 퍼즐 시맨틱 URL
RewriteRule ^bible-quiz/genesis$ /play.html?id=gen_001 [L]
RewriteRule ^bible-quiz/exodus$ /play.html?id=exo_002 [L]
RewriteRule ^bible-quiz/([a-z]+)$ /play.html?id=$1_001 [L]

# 인물 퍼즐
RewriteRule ^crossword/moses$ /play.html?id=moses_life [L]
RewriteRule ^crossword/david$ /play.html?id=david_life [L]
```

#### B. 자동 매핑 테이블
```python
# url_mapping.py
URL_MAP = {
    'bible-quiz/genesis': 'gen_001',
    'bible-quiz/exodus': 'exo_002',
    'bible-quiz/john': 'joh_080',
    'crossword/moses': 'moses_life',
    'crossword/david': 'david_life',
    # ... 287개 매핑
}

def generate_htaccess():
    with open('.htaccess', 'w') as f:
        f.write("RewriteEngine On\n\n")
        for pretty_url, puzzle_id in URL_MAP.items():
            f.write(f"RewriteRule ^{pretty_url}$ /play.html?id={puzzle_id} [L]\n")
```

#### C. Canonical URL 설정
```html
<!-- play.html에 추가 -->
<link rel="canonical" href="https://crossero.com/bible-quiz/genesis">
```

**배포 계획:**
- [ ] Week 1: URL 매핑 테이블 작성
- [ ] Week 2: .htaccess 생성 및 테스트
- [ ] Week 3: 기존 링크 전부 새 URL로 교체
- [ ] Week 4: sitemap.xml 업데이트

---

## 5. 핀터레스트 멀티모달 AEO 전략

### 5-1. 이미지 Alt 태그 전략 ⭐⭐⭐

**현재:**
```html
❌ <img src="puzzle.png" alt="퍼즐">
```

**개선:**
```html
✅ <img src="genesis-bible-crossword.png" 
     alt="창세기 성경 가로세로 퍼즐 - 주일학교 교육자료 - 십자가로세로">
```

#### 자동 생성 규칙
```python
def generate_image_alt(puzzle_data):
    return f"{puzzle_data.title} 성경 가로세로 퍼즐 - 주일학교 교육자료 - 십자가로세로"

def generate_image_filename(puzzle_data):
    title_en = translate_to_slug(puzzle_data.title)
    return f"{title_en}-bible-crossword-puzzle.png"

# 예시
# 창세기 → genesis-bible-crossword-puzzle.png
# 출애굽기 → exodus-bible-crossword-puzzle.png
```

---

### 5-2. 이미지 파일명 최적화 ⭐⭐⭐

**현재:**
```
❌ puzzle_001.png
❌ img_20240101.png
```

**개선:**
```
✅ genesis-bible-crossword-puzzle.png
✅ moses-crossword-sunday-school.png
✅ john-gospel-crossword-church.png
```

**일괄 변경:**
```python
# rename_images.py
FILENAME_MAP = {
    'gen_001': 'genesis-bible-crossword-puzzle',
    'exo_002': 'exodus-bible-crossword-puzzle',
    'joh_080': 'john-gospel-crossword-church',
    # ... 287개
}

for puzzle_id, new_name in FILENAME_MAP.items():
    old_path = f'images/puzzles/{puzzle_id}.png'
    new_path = f'images/puzzles/{new_name}.png'
    os.rename(old_path, new_path)
```

---

### 5-3. Pinterest 설명 텍스트 구조 ⭐⭐

**필수 포함 키워드:**
```
✅ Bible crossword puzzle
✅ Sunday school material
✅ Printable church activity
✅ Crossero.com
✅ 무료 다운로드 (Free download)
```

#### 템플릿
```python
def generate_pinterest_description(puzzle):
    return f"""
{puzzle.title} Bible Crossword Puzzle 📖

✅ 25x25 grid
✅ Sunday school material
✅ Printable church activity
✅ Free online puzzle

Perfect for church bulletins and Christian education!

Download: crossero.com
#BibleQuiz #SundaySchool #ChristianEducation #{puzzle.title}
    """
```

---

## 6. AI 인용 유도 콘텐츠 전략

### 6-1. 정의형 문장 반복 ⭐⭐⭐

**규칙:** 모든 페이지 상단에 3문장 정의

```html
<!-- 모든 페이지 <article> 시작 부분 -->
<div class="service-definition">
  <p><strong>십자가로세로</strong>는 성경 기반 가로세로 퍼즐 온라인 서비스입니다.</p>
  <p>교회 주보와 주일학교에서 사용할 수 있는 무료 교육 자료를 제공합니다.</p>
  <p>성경 인물, 사건, 핵심 구절을 바탕으로 제작된 교육형 퍼즐 플랫폼입니다.</p>
</div>
```

---

### 6-2. FAQ 지속 확장 ⭐⭐

**목표:** 현재 8개 → 30개 이상

#### 추가 질문 예시
```
Q9. 어떤 성경 권이 포함되나요?
A9. 구약 39권, 신약 27권 총 66권의 성경 전체를 다룹니다.

Q10. 난이도는 어떻게 되나요?
A10. 초등부용 쉬운 퍼즐부터 성인용 어려운 퍼즐까지 다양합니다.

Q11. 정답은 어떻게 확인하나요?
A11. 후원자에게 제공되는 정답 확인 기능을 통해 즉시 확인 가능합니다.

Q12. 인쇄 품질은 어떤가요?
A12. A4 용지 기준으로 최적화된 고해상도 인쇄를 지원합니다.

... (총 30개까지 확장)
```

**자동 생성:**
```python
# faq_generator.py
FAQ_DATA = [
    {
        'q': '어떤 성경 권이 포함되나요?',
        'a': '구약 39권, 신약 27권 총 66권의 성경 전체를 다룹니다.'
    },
    # ... 30개
]

def generate_faq_html():
    html = "<h1>자주 묻는 질문 (FAQ)</h1>\n"
    schema_items = []
    
    for item in FAQ_DATA:
        html += f"<h2>{item['q']}</h2>\n"
        html += f"<p>{item['a']}</p>\n\n"
        
        schema_items.append({
            "@type": "Question",
            "name": item['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item['a']
            }
        })
    
    # Schema 생성
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": schema_items
    }
    
    return html, schema
```

---

### 6-3. 블로그형 콘텐츠 추가 ⭐⭐

**신규 페이지 생성:**
```
/blog/bible-quiz-for-sunday-school.html
/blog/top-10-bible-crossword-questions.html
/blog/how-to-use-bible-puzzles-in-church.html
/blog/printable-bible-activities.html
```

#### 템플릿
```html
<!DOCTYPE html>
<html lang="ko">
<head>
<title>주일학교를 위한 성경 퀴즈 활용법 | 십자가로세로</title>
<meta name="description" content="주일학교 수업에서 성경 가로세로 퍼즐을 활용하는 5가지 방법을 소개합니다.">
</head>
<body>

<article>
  <h1>주일학교를 위한 성경 퀴즈 활용법</h1>
  
  <section>
    <h2>1. 수업 도입부 집중력 높이기</h2>
    <p>
      수업 시작 5분 동안 간단한 성경 가로세로 퍼즐을 풀면
      아이들의 집중력이 높아지고 본 수업 준비가 됩니다.
      십자가로세로의 짧은 퍼즐을 활용하면 효과적입니다.
    </p>
  </section>
  
  <section>
    <h2>2. 소그룹 활동 자료</h2>
    <p>
      4-5명씩 팀을 나누어 퍼즐을 함께 풀면
      협동심과 성경 지식을 동시에 배울 수 있습니다.
    </p>
  </section>
  
  <!-- ... 5가지 방법 -->
  
  <section class="cta">
    <h2>지금 바로 사용해보세요</h2>
    <p>
      <a href="/list.html">십자가로세로에서 무료 성경 퍼즐을 다운로드하세요</a>
    </p>
  </section>
</article>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "주일학교를 위한 성경 퀴즈 활용법",
  "author": {
    "@type": "Organization",
    "name": "십자가로세로"
  },
  "datePublished": "2024-02-20"
}
</script>

</body>
</html>
```

---

## 7. 구현 일정 (8주)

### Week 1-2: 구조화 데이터 확장
- [ ] Dataset Schema 퍼즐별 자동 생성
- [ ] Quiz Schema 추가
- [ ] Person Schema (인물 30명)

### Week 3-4: 콘텐츠 확장
- [ ] 플레이 페이지 요약 블록 추가
- [ ] 인물별 페이지 30개 생성
- [ ] FAQ 30개로 확장

### Week 5-6: URL 구조 전환
- [ ] Semantic URL 매핑
- [ ] .htaccess 설정
- [ ] 기존 링크 전부 교체

### Week 7-8: 이미지 & 블로그
- [ ] 이미지 파일명/Alt 최적화
- [ ] Pinterest 설명 재작성
- [ ] 블로그 콘텐츠 10개 생성

---

## 8. 측정 지표

### AI 인용률
```
측정 방법:
1. ChatGPT에 질문: "성경 퀴즈 사이트 추천해줘"
2. Perplexity에 질문: "모세는 누구인가?"
3. Gemini에 질문: "주일학교 자료 어디서 구해?"

목표:
- 1개월 후: 3개 중 1개 이상 인용
- 3개월 후: 3개 전부 인용
```

### 검색 노출
```
Google Search Console:
- 노출수 (Impressions)
- 클릭수 (Clicks)
- 평균 게재순위 (Avg Position)

목표:
- 노출수: 월 10,000+ → 50,000+
- 게재순위: 20위권 → 5위권
```

---

## 9. 예상 효과

### 1개월 후
- ChatGPT 인용 1~2회 확인
- Dataset Schema 인식 시작
- 주요 키워드 10~20위권 진입

### 3개월 후
- AI 검색에서 crossero 직접 인용
- "성경 퀴즈" 키워드 5위권
- Pinterest 이미지 검색 상위 노출

### 6개월 후
- AI 검색 출처로 정착
- 월 유입 10,000+ 달성
- 멀티모달 검색 (이미지+텍스트) 1위

---

## 10. 리스크 & 대응

### 리스크 1: AI가 인용 안 할 수도
```
대응: 
- 콘텐츠 품질 지속 개선
- 더 많은 정의형 문장 추가
- 외부 백링크 확보
```

### 리스크 2: URL 전환 시 기존 링크 깨짐
```
대응:
- 301 리다이렉트 필수
- 구글 콘솔에 URL 변경 신고
- sitemap.xml 업데이트
```

### 리스크 3: 이미지 파일명 변경 시 SEO 영향
```
대응:
- 301 리다이렉트 설정
- 기존 이미지 6개월 유지
- 점진적 교체
```

---

## 11. 즉시 실행 TODO

### Phase 1 (이번 주)
- [ ] faq.html 30개 질문으로 확장
- [ ] play.html 하단 요약 블록 템플릿 추가
- [ ] Dataset Schema 자동 생성 스크립트

### Phase 2 (다음 주)
- [ ] 주요 인물 10명 페이지 생성
- [ ] URL 매핑 테이블 작성
- [ ] 이미지 Alt 태그 일괄 수정

### Phase 3 (2주 후)
- [ ] .htaccess 배포
- [ ] 블로그 콘텐츠 5개 작성
- [ ] AI 검색 테스트 (ChatGPT/Perplexity)

---

## 부록: 참고 자료

### Schema.org 문서
- Dataset: https://schema.org/Dataset
- Quiz: https://schema.org/Quiz
- FAQPage: https://schema.org/FAQPage
- Person: https://schema.org/Person

### AI 검색 최적화 가이드
- Google AEO Best Practices
- Bing Chat SEO Guidelines
- ChatGPT Citation Guidelines
