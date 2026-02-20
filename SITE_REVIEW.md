# 십자가로세로(crossero) 사이트 최종 점검 · 버전 응용 가이드

레트로버전, 야구덕질버전, 팬덤버전 등으로 응용할 때 참고용 정리입니다.

---

## 1. www 폴더 구조 요약

| 파일 | 역할 | 버전별 변경 |
|------|------|-------------|
| **index.html** | 메인(홈): 태그/추천 퍼즐, 네비, 푸터 | 브랜딩·태그·카피 전면 교체 |
| **list.html** | 퍼즐 목록: 카테고리·태그 필터, 그리드 | **data.js category**에 맞게 섹션/링크 교체 |
| **play.html** | 퍼즐 플레이: 그리드·힌트·정답·인쇄·후원 연동 | 데이터 구조 동일하면 로고/문구만 |
| **about.html** | 소개 페이지 | 카피·링크 교체 |
| **support.html** | 후원: 계좌·코드 입력·구글폼 링크 | 계좌·폼·코드 접두어 교체 |
| **data.js** | **핵심**: 퍼즐 DB `QUIZ_DATABASE` (id, title, category, allWords 등) | 레트로/야구/팬덤 콘텐츠로 통째로 교체 |
| **auth.js** | 후원 코드 검증, localStorage 키 `crossero_donor`, 인쇄 수 차감 | **localStorage 키·코드 접두어·배열** 교체 |
| **robots.txt** | 크롤링 규칙·사이트맵 경로 | 도메인 없음(상대경로) → 수정 불필요 |
| **sitemap.xml** | 검색엔진용 URL 목록 (메인 5개 + play?id=…) | **data.js 기준으로 재생성** (또는 스크립트 사용) |
| **.htaccess** | HTTPS 리다이렉트 | 공통 사용 가능 |
| **naverd6e87bd7f545d5312c9879cedaf2c09f.html** | 네이버 사이트 소유 확인용 | 새 사이트면 새 인증 파일로 교체 |
| **PrintLogWebApp.gs** | 인쇄 로그 → 구글 스프레드시트 (웹앱) | 새 프로젝트면 스프레드시트 ID·play 쪽 URL 교체 |
| **x_play.html** | 플레이 전용(미니멀) 버전 | 필요 시 브랜딩만 교체 |
| **x_index.html** | 인덱스 전용(미니멀) 버전 | 필요 시 브랜딩만 교체 |

**이미지**  
- `images/crossero-logo.png` (로고)  
- `images/og-image.png` (공유 미리보기)  
→ 레트로/야구/팬덤용 로고·og 이미지로 교체.

---

## 2. 버전별로 꼭 바꿔야 할 것 (체크리스트)

### 2.1 브랜딩·도메인 (전 페이지)

- [ ] 사이트명: `십자가로세로` → 새 서비스명
- [ ] `crossero.com` → 새 도메인 (og:image, sitemap, QR 등)
- [ ] 로고: `images/crossero-logo.png` → `images/로고파일명.png`
- [ ] og 이미지: `images/og-image.png` 및 meta `og:image` URL
- [ ] 푸터: "Crossero Puzzle Engine by PuzDuk.com" 등 문구
- [ ] copyright 연도·사이트명 (예: index.html `© 2026 십자가로세로`)

### 2.2 데이터·콘텐츠

- [ ] **data.js**: `QUIZ_DATABASE` 전체를 새 주제(레트로/야구/팬덤) 퍼즐로 교체  
  - 구조 유지: `id`, `title`, `category`, `meta`, `config`, `allWords` (clue, answer)
- [ ] **index.html**:  
  - 태그 링크/라벨 (예: 성경 인물 → 레트로/야구/팬덤 태그)  
  - "이번 주 추천" 등 카피  
  - `list.html`의 **list.html?tag=** 값이 data.js의 `category`와 맞는지 확인
- [ ] **list.html**:  
  - `play.html?category=XXX`·`list.html?tag=XXX` 를 새 data.js의 category/태그 체계에 맞게 수정  
  - 섹션 제목(예: 구약성경 → 레트로/야구/팬덤 카테고리명)

### 2.3 후원·인증

- [ ] **auth.js**  
  - `localStorage` 키: `crossero_donor` → 예) `retro_donor`, `baseball_donor` (버전별로 고유하게)  
  - `VALID_CODES_D1`, `VALID_CODES_D7`, `VALID_CODES_M1` 배열을 새 코드로 교체 (접두어도 변경 가능, 예: RTR-, BB-, FAN-)
- [ ] **support.html**  
  - 계좌 정보(은행·번호·예금주)  
  - "후원 후 메시지 보내기" 구글폼 링크 (`forms.gle/...`)  
  - 코드 예시/placeholder (CRS-** → 새 접두어)
- [ ] **play.html** (및 x_play.html)  
  - 인쇄 시 prompt 기본값: `"교회명을 입력하세요.", "로세로교회"` → 서비스에 맞는 문구로 (예: "단체명", "닉네임")

### 2.4 인쇄 로그·구글 연동

- [ ] **play.html**  
  - `PRINT_LOG_WEB_APP_URL`: 새 프로젝트면 새 웹앱 URL로 교체 (또는 빈 문자열 `""`로 두면 구글폼 방식만 사용)  
  - 구글폼 사용 시: `FORM_ID`, `ENTRY_CHURCH` 등 entry ID를 새 폼에 맞게 수정
- [ ] **PrintLogWebApp.gs**  
  - 새 사이트용 스프레드시트를 쓰면 `SPREADSHEET_ID` 교체  
  - 배포 후 나온 웹앱 URL을 play.html의 `PRINT_LOG_WEB_APP_URL`에 넣기

### 2.5 검색엔진

- [ ] **sitemap.xml**: 메인 5개 URL의 도메인을 새 도메인으로; 퍼즐 URL은 **data.js 기준으로 다시 생성** (이전에 사용한 스크립트/방식 재사용 가능)
- [ ] **robots.txt**: `Sitemap:` URL만 필요 시 새 도메인으로
- [ ] **naver 인증**: 새 도메인이면 네이버 서치어드바이저에서 새 인증 파일 발급 후 해당 HTML만 교체

### 2.6 기타

- [ ] **.htaccess**: 그대로 두어도 됨 (HTTPS 리다이렉트만)
- [ ] **x_play.html / x_index.html**: 사용할 경우 로고·QR URL(crossero.com) 등만 교체

---

## 3. 재사용 시 유의사항

1. **data.js 구조**  
   - `QUIZ_DATABASE` 키 = 퍼즐 고유 ID (`play.html?id=xxx`)  
   - `category`는 쉼표로 구분된 문자열 → list.html의 `?tag=` / `?category=` 와 일치시켜야 필터·목록이 동작함.

2. **auth.js와 play.html**  
   - `checkAuthStatus()`가 사용하는 localStorage 키를 바꾸면, 기존 crossero 후원자 세션은 새 버전에서 인식되지 않음 (의도된 분리).

3. **인쇄 로그**  
   - 웹앱 URL을 비우면 구글폼 formResponse만 사용; 폼이 “로그인 없이 응답” 허용해야 익명 제출이 스프레드시트에 쌓임.  
   - 웹앱 방식이 더 안정적이면 새 스프레드시트 + PrintLogWebApp.gs 복사 후 ID·URL만 교체.

4. **이미지 폴더**  
   - `images/` 에 로고·og-image 필수. 없으면 깨진 이미지/공유 미리보기 오류 발생.

---

## 4. 현재(crossero) 사이트 상태 요약

- **메인 플로우**: index → list(또는 태그) → play → 인쇄/정답 확인, support에서 코드 입력 후 인쇄 권한 부여.
- **고정 URL**: crossero.com, og:image·sitemap·QR에 반영됨.
- **후원**: 카카오뱅크 계좌 + 구글폼 + auth.js의 CRS- 코드 배열.
- **인쇄 로그**: play.html의 웹앱 URL 설정됨 + PrintLogWebApp.gs는 해당 스프레드시트 ID 사용 중.
- **검색**: robots.txt, sitemap.xml 정리됨; sitemap 퍼즐 목록은 data.js 기준 287개 반영됨.
- **특수 파일**:  
  - `backup/` 은 robots에서 `Disallow: /backup/` 로 제외됨 (검색엔진 제외).  
  - `x_play.html`, `x_index.html` 은 미니멀 버전용으로 보임 (필요 시에만 사용).

레트로/야구/팬덤 버전은 **별 도메인·별 폴더**로 복사한 뒤, 위 체크리스트만 따라가면 동일 엔진으로 운영할 수 있습니다.

---

## 5. sitemap.xml 퍼즐 목록 재생성 (data.js 변경 후)

새 버전에서 data.js를 수정한 뒤, sitemap의 `play.html?id=...` 목록을 맞추려면 프로젝트 루트(www)에서 실행.  
**네이버/구글 공통 형식**(각 URL에 `lastmod`, `changefreq`, `priority`)으로 생성함.

```bash
# 1) 기존 sitemap.xml 백업 권장: cp sitemap.xml sitemap.xml.bak
# 2) 메인 5개 URL(앞 32줄) + data.js 기준 퍼즐 URL로 재생성
DOMAIN="https://YOUR-DOMAIN.com"   # 실제 도메인으로 변경
LASTMOD="2026-02-14"                # 필요 시 날짜 변경

head -32 sitemap.xml > sitemap_head.xml
echo "  <!-- 퍼즐 플레이 페이지 (data.js 기준) -->" >> sitemap_head.xml
grep -oE '"[a-zA-Z0-9_]+":\s*\{' data.js | sed 's/":.*//;s/"//g' | sort -u | while read id; do
  echo "  <url>"
  echo "    <loc>${DOMAIN}/play.html?id=$id</loc>"
  echo "    <lastmod>${LASTMOD}</lastmod>"
  echo "    <changefreq>weekly</changefreq>"
  echo "    <priority>0.8</priority>"
  echo "  </url>"
done >> sitemap_head.xml
echo "</urlset>" >> sitemap_head.xml
mv sitemap_head.xml sitemap.xml
```

- `YOUR-DOMAIN.com` → 실제 도메인 (예: crossero.com, 레트로버전 도메인)
- 메인 5개 URL의 `lastmod`도 맞추려면 기존 sitemap.xml 앞 32줄이 이미 해당 형식이어야 함 (한 번 수동으로 맞춰 두면 이후엔 head -32로 유지됨)
