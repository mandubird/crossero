# SEO 블로그 글 검증 결과 & 할일

## 0. 매일 발행 & 로컬–서버 동기화 (요약)

| 질문 | 답변 |
|------|------|
| **매일 9시 글 발행** | ✅ GitHub Actions가 **매일 00:00 UTC(= 한국 09:00)**에 워크플로 실행. `posts_schedule.json`의 그날 예약만 발행. |
| **이미지도 잘 불러오나요?** | ✅ 같은 워크플로에서 **Playwright**로 퍼즐 PNG 생성 → `images/puzzles/` 저장 → FTP 업로드. 글이 올라갈 때 이미지도 함께 반영. |
| **바울의 회심 22일** | ✅ `published_manifest.json`에서 act_086 날짜 **2026-02-22**, 글 HTML도 2/22·퍼즐 이미지 경로로 이미 반영. **추가로 바꿀 것 없음.** |
| **로컬 ↔ 서버 동기화** | ✅ **push to main** 시에도 같은 워크플로가 돌아서 FTP 배포됨. → 로컬에서 수정 후 `git push origin main` 하면 서버에 반영. |

**할 일**: GitHub 저장소에 **Secrets**(`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`) 설정되어 있어야 매일 9시·푸시 시 FTP 배포가 성공합니다. 한 번 푸시해서 Actions 로그에서 FTP 단계 성공 여부만 확인하면 됩니다.

**로컬–서버 동기화 절차**: (1) 이 폴더를 Git 저장소로 쓰려면 `git init` 후 `git remote add origin <GitHub 저장소 URL>` 로 연결. (2) 작업 후 `git add .` → `git commit -m "메시지"` → `git push -u origin main` 하면 푸시와 동시에 워크플로가 돌아 서버(FTP)에 반영됩니다.

---

## 1. 요청하신 블로그 글 구조 (목표)

```
┌────────────────────────────────────┐
│  제목: 창세기 성경퀴즈 100문제     │
├────────────────────────────────────┤
│  📅 2026-02-20 | 구약 | ⭐⭐⭐      │
├────────────────────────────────────┤
│  소개글 (키워드 자연스럽게 배치)    │
├────────────────────────────────────┤
│  [퍼즐 이미지]                      │
│  창세기-성경퀴즈-100문제.png        │
├────────────────────────────────────┤
│  📝 가로 힌트 / 📝 세로 힌트        │
├────────────────────────────────────┤
│  🔗 정답 확인하기 (새창)            │
├────────────────────────────────────┤
│  관련 퀴즈 / 키워드                 │
└────────────────────────────────────┘
```

---

## 2. 검증 결과 (현재 vs 요청)

| 항목 | 요청 | 현재 상태 | 조치 |
|------|------|-----------|------|
| **가. 발행일** | 예약별로 날짜 다름 (2026-02-20, 02-21, …) | 모두 동일(생성일) | ✅ 예약 스케줄 + 당일만 발행하도록 변경 |
| **나. 목록 노출** | 발행된 글만 목록·sitemap에 노출, 미래 예약 글 비노출 | 287개 전부 노출 | ✅ 발행된 글만 posts/index.html·posts.xml에 반영 |
| **다. 한글 URL·키워드·Schema·고유 텍스트** | 한글 슬러그, 키워드 자연스럽게, Schema.org, 글마다 고유 | 한글 슬러그 일부, Schema 있음, 고유 텍스트(소개 템플릿 랜덤) | ✅ 한글 제목/키워드 조합으로 slug·파일명 통일, 고유 문장 유지 |
| **라. 퍼즐 이미지** | 글 안에 퍼즐 이미지 (빈 칸 + 힌트 아래), 한글 파일명·alt | 이미지 없음(og만) | ✅ 퍼즐 그리드 PNG 생성(한글 파일명), `<img alt="...">` 반영 |
| **마. 이미지 SEO** | `../images/puzzles/창세기-성경퀴즈-100문제.png`, alt 한글 | 없음 | ✅ 이미지 경로·한글 파일명·alt 적용 |
| **라-2. GSC·네이버** | Search Console·Search Advisor 등록, sitemap 제출, URL 검사 | 미실행(수동) | 📋 할일 목록에 유지 |
| **마-2. posts.xml 날짜** | 발행일별 lastmod, 한꺼번에 287개 아님 | 287개 동일일·한번에 등록 | ✅ 발행된 글만·날짜별 lastmod 반영 |

---

## 3. 작동 방식 (목표)

- **예약 발행**: `posts_schedule.json`에 날짜별로 1~3개 퍼즐 배정.
- **매일 1회 실행** (예: 오전 9시): `python3 auto_publish_with_images.py`
  - **오늘 날짜**에 해당하는 퍼즐만:
    - 퍼즐 이미지: **play2.html** 전용 엔진으로 PNG 생성 (Playwright) → 실패 시 Pillow 그리드 또는 og 이미지
    - 블로그 HTML 생성 → `posts/한글제목.html` (제목·메타·소개·이미지·가로/세로 힌트·**이 퍼즐 풀어보기** 링크·관련/키워드)
  - **발행된 글만**으로 `posts/index.html`, `posts.xml` 재생성 (날짜·lastmod 반영).
- **결과**: 게시판·sitemap에는 "오늘까지 발행된 글"만 노출, 미래 예약 글은 안 보임.
- **play2.html**: play.html을 복사한 블로그 전용 엔진. `export=1`(이미지 추출), `play=1&g=...(같은 퍼즐 빈 칸)` 지원. **기존 play.html 퍼즐 생성 로직은 수정하지 않음.**

---

## 4. 할일 체크리스트

### 스크립트·구조
- [x] `auto_publish_with_images.py` 구현 (예약 읽기 → 당일 발행 → 이미지 생성 → index·posts.xml 갱신)
- [x] `posts_schedule.json` 생성 (`python3 auto_publish_with_images.py init`): 287개를 날짜별 1~3개씩 배정
- [x] 퍼즐 이미지: **play2.html?export=1** (Playwright) 또는 Pillow 그리드, **제목명-십자가로세로.png**, `images/puzzles/` 저장
- [x] 블로그 HTML: 제목·📅 날짜·구약/신약 등·소개·**퍼즐 이미지**·가로/세로 힌트·**이 퍼즐 풀어보기**(play2.html?play=1&g= 동일 퍼즐) 또는 **이 주제 퍼즐 풀어보기**(play.html?id=)·관련/키워드·Schema
- [x] `posts.xml`: **발행된 글만** 포함, 각 URL에 **발행일 = lastmod** 반영
- [x] `posts/index.html`: **발행된 글만** 링크 목록 (최신순)

### SEO·수동
- [x] Google Search Console 등록, sitemap 제출 (완료)
- [ ] Google URL 검사로 주요 URL 색인 요청 (선택)
- [x] Naver Search Advisor 등록, sitemap 제출 (완료)
- [ ] 각 게시글: 한글 URL(슬러그), 키워드 자연스럽게, Schema.org, 고유 텍스트

### 노출 위치 (결정 후 진행)
- [ ] 블로그 글을 **기존 사이트 어디에 노출할지** 결정 (예: 푸터 "퍼즐 소개 글", 메뉴, about 내 링크 등)
- [ ] 결정 후 해당 위치에 "퍼즐 소개 글" 또는 게시판 링크 추가 (`/posts/` 또는 `posts/index.html`)

---

## 4-2. 다음 할일 (예약 발행·이미지 해결된 뒤 바로 진행)

아래 두 가지는 **글 예약 발행 및 이미지 구성이 끝나면 바로 진행**하면 됩니다.

1. **Google Search Console / Naver Search Advisor**  
   사이트 등록, sitemap 제출, 주요 URL 색인 요청 (수동)
2. **블로그 글 노출 위치**  
   사이트 어디에 노출할지 결정 후, 해당 위치에 링크 추가 (예: 푸터 "퍼즐 소개 글")

---

## 5. 첫 설정 (기존 287개 글 정리 후 예약 발행으로 전환)

1. **기존 posts 정리** (선택): 예약 발행만 쓰려면 `posts/*.html`(index.html 제외) 삭제, `published_manifest.json` 삭제. **(이미 적용됨: 292개 글·manifest 삭제 완료)**
2. **스케줄 생성**: `python3 auto_publish_with_images.py init` → `posts_schedule.json` 생성.
3. **오늘 분량만 발행**: `python3 auto_publish_with_images.py` → 오늘 날짜에 해당하는 1~3개만 HTML·이미지 생성, `posts/index.html`·`posts.xml`은 발행된 글만 반영.
4. **매일**: cron 등으로 `python3 auto_publish_with_images.py` 실행 (예: 오전 9시).

**퍼즐 이미지·링크** (play2.html 전용 엔진):
- **Playwright**: `play2.html?id=xxx&export=1`로 열어 실제 퍼즐 PNG·힌트·`play2.html?play=1&g=...` URL 수집. 성공 시 블로그에는 **이 퍼즐 풀어보기** 링크(같은 퍼즐 빈 칸).
- **Pillow** (Playwright 실패 시): 간단한 빈 칸 그리드 PNG. 이 경우 링크는 **이 주제 퍼즐 풀어보기**(play.html?id=).
- 둘 다 없으면 글에는 og 이미지 사용.

---

## 6. 작동 예시 (매일 실행)

```bash
# 매일 오전 9시 자동 실행
python3 auto_publish_with_images.py
```

**콘솔 출력 예:**
```
🎨 이미지 생성(Pillow): 출애굽기-모세의-소명-십자가로세로.png
✅ 발행: 출애굽기-성경퀴즈.html (이미지: 출애굽기-모세의-소명-십자가로세로.png)
🎉 완료! 2개 발행 (총 발행 N개)
```

**생성/갱신되는 파일:**
```
posts/
├── 창세기-성경퀴즈-100문제.html   ← 발행된 글만 (한글 슬러그)
└── index.html                    ← 발행된 글만 링크

images/puzzles/
├── 창세기-천지창조-십자가로세로.png   ← 제목명-십자가로세로
└── 출애굽기-모세의-소명-십자가로세로.png

posts_schedule.json               ← init 시 1회 생성
published_manifest.json           ← 발행된 글 목록 (날짜·slug)
posts.xml                         ← 발행된 글만, lastmod=발행일
```

---

## 7. 참고

- **기존 `generate_seo_posts.py`**: 287개 한번에 생성용. 예약 발행으로 전환 후에는 `auto_publish_with_images.py`만 매일 실행하면 됨.
- **cron 예시**: `0 9 * * * cd /path/to/www && python3 auto_publish_with_images.py >> publish.log 2>&1`
- **requirements.txt**: `Playwright`(권장, play2 전용 이미지·동일 퍼즐 링크) 또는 `Pillow`(그리드 이미지). 없으면 og 이미지.
- **매일 1회만 실행 권장**: 같은 날 여러 번 실행하면 같은 퍼즐이 다른 키워드로 중복 발행될 수 있음.
- **play2.html**: 블로그 발행 전용. play.html은 수정하지 않음. `export=1` → PNG·힌트·g= 수집. `play=1&g=` → 같은 퍼즐 빈 칸으로 풀기.

---

## 8. 서버에서 자동 실행 (play2 + 날짜별 자동 발행)

**가능합니다.** 서버에서 cron으로 스크립트만 돌리면, play2.html로 이미지·동일 퍼즐 링크 생성 후 날짜별로 글이 쌓입니다.

- **필요 조건**: 서버에 Python 3, Playwright + Chromium(권장) 또는 Pillow. `play2.html`·`data.js`·스크립트가 있는 `www` 디렉터리를 서버에 둠. cron으로 매일 1회 실행 (예: `0 9 * * * cd /path/to/www && python3 auto_publish_with_images.py`).
- **사이트가 같은 서버에 있는 경우** → 스크립트가 `posts/`, `images/puzzles/` 등을 채우면 그대로 웹에서 노출. 별도 FTP 없이 자동 반영.
- **사이트가 다른 곳(FTP 호스팅 등)인 경우** → 서버에서 스크립트 실행 후, 그 서버에서 FTP/rsync 등으로 `posts/`, `images/puzzles/`, `posts.xml` 만 자동 업로드하는 스크립트를 추가하면 됨 (예: lftp, ncftpput, rsync).

---

## 9. FTP 배포 (GitHub 미연동 시)

crossero.com이 **GitHub에 연동되어 있지 않고 FTP로 올리는 경우**:

- **예약 발행만 로컬(또는 서버)에서 실행**하면 됩니다. 별도 "예약 글 전용" 설정은 없습니다.
- 매일 정해진 시간에 `python3 auto_publish_with_images.py`를 실행한 뒤, **생성·갱신된 파일만 FTP로 업로드**하면 됩니다.
  - 업로드 대상: `posts/*.html`, `posts/index.html`, `images/puzzles/*.png`(이미지 쓸 때), `posts.xml`, **`play2.html`**(「이 퍼즐 풀어보기」 링크가 동작하려면 반드시 업로드)
- cron은 "매일 스크립트 실행"만 담당하고, **실제 사이트 반영은 FTP 업로드**로 하시면 됩니다. (로컬에서 스크립트 돌리고 수동 FTP, 또는 스크립트 실행 환경이 있는 서버에서 돌린 뒤 그 서버에서 FTP로 올리는 방식 모두 가능)

---

## 10. 이미지·링크 규칙 & FAQ

**이미지 파일명**: `제목명-십자가로세로.png` (예: 출애굽기-모세의-소명-십자가로세로.png)

**블로그 하단 링크**:  
- **Playwright 성공 시**: "이 퍼즐 풀어보기" → `play2.html?play=1&g=...` 로 **글에 나온 그 퍼즐과 동일한** 빈 칸이 열림.  
- **Playwright 미사용/실패 시**: "이 주제 퍼즐 풀어보기" → `play.html?id=xxx` 로 같은 주제 퍼즐(새로 섞인 그리드)이 열림. 정답 보기 아님.

**3. 궁금한 점**  
- 가. 이미지가 안 나와요 → Playwright(`playwright install chromium`) 또는 Pillow 설치. 없으면 og 이미지로 표시됨.  
- 나. play2.html이 뭐예요? → play.html을 복사한 **블로그 전용 엔진**. export/play 모드만 추가되어 있어 기존 play.html 퍼즐 로직은 그대로 둠.  
- **다. "이 퍼즐 풀어보기" 클릭 시 Not Found(404)** → **서버에 `play2.html`을 업로드하지 않았기 때문.** crossero.com 루트에 `play2.html`을 올리면 해당 링크가 정상 동작합니다.

**4. 정리**  
- 가. FTP에 파이썬 올려두고 cron 매일 실행하면 그날 분량 발행됨.  
- 나. xml(posts.xml)에도 새로 발행된 글이 반영됨. 스크립트가 발행 시마다 posts.xml을 발행된 글만으로 다시 만들고 lastmod=발행일로 넣음.

---

## 5. 매일 발행 환경 (방향 정리)

### 5.0 왜 Playwright 환경이어야 하는가

- **승인한 최종 결과물** = 퍼즐 그리드 이미지 + 가로/세로 힌트 + **「이 퍼즐 풀어보기」** (글과 동일한 퍼즐).
- 이 결과물은 **Playwright가 동작하는 환경**에서만 나옵니다. (play2.html 띄워서 이미지·URL 추출)
- 일반 FTP 전용 호스팅만 있으면 Python은 돌려도 **브라우저(Chromium) 설치·실행이 불가**한 경우가 많아서, 그대로는 최종 결과물을 만들 수 없음.

**→ 할 방향: Playwright를 쓸 수 있는 서버/호스팅을 정한 뒤, 그곳에서 cron으로 매일 발행.**

### 5.1 Playwright가 가능한 환경 예시 (찾아볼 것)

| 유형 | 설명 |
|------|------|
| **GitHub Actions** | 저장소를 GitHub에 올리고 **Actions**에서 매일 워크플로우 실행. 러너에 Python + Playwright + Chromium 설치 가능 → 별도 VPS 없이 Playwright 환경 확보. 생성된 `posts/`, `images/puzzles/`, `posts.xml`, `published_manifest.json` 을 아티팩트로 내려받거나, FTP 배포(Secrets에 계정 저장) 스텝으로 기존 호스팅에 올리면 됨. |
| **VPS** | Ubuntu 등 Linux. `pip install playwright`, `playwright install chromium` 후 cron으로 스크립트 실행. 발행 결과물을 같은 서버의 웹 루트에 두거나, FTP로 기존 호스팅에 업로드. |
| **SSH + Python 가능한 호스팅** | 일부 호스팅은 SSH 접속·Python 실행 가능. Chromium 설치 허용 여부는 호스팅마다 다르므로 문의/테스트 필요. |
| **로컬 PC + cron(또는 수동) 후 업로드** | 매일 본인 PC에서 `auto_publish_with_images.py` 실행 → 생성된 `posts/`, `images/puzzles/`, `posts.xml`, `published_manifest.json` 만 FTP로 업로드. 웹은 기존 FTP 호스팅에 두고, 발행만 로컬에서 수행. |

정리: **GitHub에 등록 후 Actions**를 쓰면 별도 서버 없이 Playwright 환경으로 매일 발행 가능(결과물은 FTP 업로드 등 한 단계 추가). 또는 **cron으로 돌릴 “발행 전용 환경”**을 Playwright 가능한 쪽(VPS / SSH 호스팅 / 로컬 중 하나)으로 정하면, 그날 분량이 항상 승인한 테스트 결과물과 동일하게 나옵니다.

### 5.2 그 환경에 올릴 것 (사이트 루트 = www 동일 구조)

| 필수 | 파일/폴더 | 비고 |
|------|-----------|------|
| ✅ | `auto_publish_with_images.py` | 발행 스크립트 |
| ✅ | `generate_seo_posts.py` | 스크립트가 import |
| ✅ | `data.js` | 퍼즐 데이터 |
| ✅ | `posts_schedule.json` | 로컬에서 `python3 auto_publish_with_images.py init` 한 뒤 업로드 |
| ✅ | `run_daily_publish.sh` | cron에서 실행할 셸 스크립트 |
| ✅ | `published_manifest.json` | 없으면 빈 배열 `[]`로 생성되거나 첫 발행 시 생성됨 |
| ✅ | `posts/` 폴더 | 비어 있어도 됨. 스크립트가 index.html·글 HTML 생성 |
| ✅ | `images/` (최소 `og-image.png`) | 대체용. 퍼즐 이미지는 스크립트가 `images/puzzles/` 에 생성 |
| ✅ | **Python 3 + Playwright + Chromium** | 이 환경에서만 최종 결과물(퍼즐 이미지 + 이 퍼즐 풀어보기) 생성 가능. |

- **올리지 않아도 되는 것**: `.venv`는 해당 환경에서 새로 만들어도 됨.

### 5.3 그 환경에서 한 번만

1. **쉘 스크립트 실행 권한**  
   ```bash
   chmod +x /경로/사이트루트/run_daily_publish.sh
   ```
2. **스케줄이 없으면 한 번 init** (로컬에서 이미 했다면 생략)  
   ```bash
   cd /경로/사이트루트
   python3 auto_publish_with_images.py init
   ```
   → `posts_schedule.json` 생성. 이미 업로드했으면 불필요.

### 5.4 cron 등록 (매일 그날 분량 발행)

- **crontab 편집**: `crontab -e`
- **예: 매일 오전 9시** (서버 경로는 실제 사이트 루트로 변경)  
  ```cron
  0 9 * * * /var/www/html/run_daily_publish.sh
  ```
  또는  
  ```cron
  0 9 * * * /home/계정/public_html/run_daily_publish.sh
  ```

- **로그**: `logs/daily_publish.log`에 실행 시각·출력이 쌓임. 실패 시 여기서 확인.

### 5.5 동작 요약

- cron이 매일 지정한 시각에 `run_daily_publish.sh` 실행  
  → `python3 auto_publish_with_images.py` 실행  
  → **오늘 날짜**에 해당하는 예약만 발행(HTML·이미지·manifest·posts/index.html·posts.xml 갱신).  
- 그날 예약이 없으면 새 글은 없고, 기존 발행 목록만으로 index·xml 유지.

---

## 6. GitHub + Actions + 카페24 FTP 자동 발행 (권장)

**흐름**: GitHub에 코드 올림 → Actions에서 매일 Cron 실행 → 발행 스크립트 실행 → 생성된 파일을 FTP로 카페24에 자동 업로드 → 블로그 글 발행. **수동 FTP 올릴 필요 없음.**

### 6.1 GitHub 저장소 만들고 코드 올리기

1. **GitHub 로그인** 후 [github.com](https://github.com) → 우측 상단 **+** → **New repository**.
2. **저장소 이름** 입력 (예: `crossero`), Public 선택, **Create repository**.
3. **로컬에서 Git 초기화 및 푸시** (프로젝트 폴더 = www 폴더 내용이 있는 곳에서 실행):
   ```bash
   cd   # 사이트 루트(www) 폴더로 이동
   git init
   git add .
   git commit -m "Initial: 십자가로세로 사이트 + 발행 스크립트"
   git branch -M main
   git remote add origin https://github.com/본인아이디/저장소이름.git
   git push -u origin main
   ```
   - **올릴 것**: `index.html`, `play.html`, `play2.html`, `list.html`, `about.html`, `support.html`, `data.js`, `auto_publish_with_images.py`, `generate_seo_posts.py`, `run_daily_publish.sh`, `posts_schedule.json`, `published_manifest.json`, `posts/`, `images/`, `posts.xml`, `.github/workflows/daily-publish.yml` 등 **사이트에 필요한 파일 전체**.
   - **올리지 말 것**: `.venv/` (가상환경), 개인 비밀번호·키가 들어간 파일. `.gitignore`에 `.venv/`, `logs/` 추가 권장.
4. **저장소 루트 = 사이트 루트**로 두세요. (www 폴더 **안의 파일들**이 저장소 루트에 오도록. 즉 `git init`을 www 안에서 하거나, 상위에서 하면 `www`를 루트로 두지 말고 www **내용**을 repo 루트에 두세요.)

### 6.2 카페24 FTP 정보 확인

- 카페24 **호스팅 관리** → **FTP 계정/비밀번호**, **FTP 서버 주소**(예: `ftp.계정.cafe24.com` 또는 안내된 주소) 확인.
- **서버 디렉터리**: 웹에서 보이는 사이트 루트가 FTP 기준 어디인지 확인 (예: `/` 또는 `/www/`, `/public_html/` 등). 워크플로우의 `server-dir`와 맞출 때 사용.

### 6.3 GitHub Secrets 설정 (FTP 비밀번호 보관)

1. GitHub 저장소 페이지 → **Settings** → 왼쪽 **Secrets and variables** → **Actions**.
2. **New repository secret** 로 아래 세 개 생성:

| Name | Value |
|------|--------|
| `FTP_SERVER` | 카페24 FTP 서버 주소 (예: `ftp.계정.cafe24.com`) |
| `FTP_USERNAME` | FTP 계정 아이디 |
| `FTP_PASSWORD` | FTP 비밀번호 |
| `FTP_SERVER_DIR` | **(권장)** FTP 접속 후 웹 문서가 올라가는 폴더. 카페24 뉴아우토반은 보통 `www/` 또는 `public_html/`. `550 images: No such file or directory` 나오면 이 값을 웹 루트 경로로 설정(끝에 `/` 포함, 예: `www/`). |

- 저장 후 워크플로우에서 `${{ secrets.FTP_SERVER }}` 등으로 사용됩니다.

### 6.4 워크플로우 파일 (이미 포함된 경우)

- 저장소에 **`.github/workflows/daily-publish.yml`** 이 있으면 다음이 자동으로 설정된 상태입니다.
- **내용 요약**:
  1. **Cron**: 매일 00:00 UTC (= 한국시간 09:00) 실행. 변경하려면 `cron: '0 0 * * *'` 수정.
  2. **스크립트 실행**: Python + Playwright + Chromium 설치 후 `python3 auto_publish_with_images.py` 실행 → 당일 예약 분량 발행, `posts/`, `images/puzzles/`, `posts.xml`, `published_manifest.json` 생성·갱신.
  3. **FTP 배포**: `SamKirkland/FTP-Deploy-Action`으로 위에서 생성·갱신된 파일 포함, 저장소 루트 내용을 카페24 FTP `server-dir`로 업로드. (`.git/`, `.github/`, `.venv/`, `*.py` 등은 제외.)
- **카페24 서버 경로**가 `/www/` 등이면 워크플로우에서 `server-dir`를 `./www/` 등으로 수정.

### 6.5 동작 요약

| 단계 | 내용 |
|------|------|
| **Cron 실행** | 매일 지정 시각(기본 00:00 UTC = 한국 09:00)에 Actions 워크플로우 실행. |
| **스크립트 실행** | Playwright로 퍼즐 이미지·블로그 HTML 생성 → 최종 테스트 결과물과 동일한 품질. |
| **FTP 배포** | 생성된 `posts/`, `images/puzzles/`, `posts.xml`, `published_manifest.json` 등이 카페24로 자동 업로드. |
| **블로그 글 발행** | 사이트에 그날 분량 글이 자동 반영. **수동 FTP 업로드 불필요.** |

- 그날 예약이 없으면 새 글은 생성되지 않고, 기존 발행 목록만 유지된 채 FTP 업로드됩니다.
- **수동 실행**: 저장소 **Actions** 탭 → **Daily publish and FTP deploy** → **Run workflow**.

---

## 7. SEO 가이드 대비 검토 요약 (SEO_GUIDE.md 기준)

### 7.1 이미 적용된 항목

| 항목 | 상태 |
|------|------|
| **robots.txt** | `Sitemap: sitemap.xml`, `Sitemap: posts.xml` 포함 ✅ |
| **index.html** | description, keywords, og:title/description/image/url/type ✅ |
| **list.html** | description, keywords, og (페이지별 제목·설명, 절대 URL og:image) ✅ |
| **about.html** | description, keywords, og (절대 URL, canonical) ✅ |
| **support.html** | description, keywords, og, canonical 추가 완료 ✅ |
| **play.html / play2.html** | description, keywords, og, canonical(JS), Schema.org ✅ |
| **블로그 글** (auto_publish) | title, description, keywords, og, canonical, Article 스키마, 키워드 섹션 ✅ |
| **이미지 alt** | 로고·퍼즐 이미지에 한글 alt 적용 ✅ |

### 7.2 이번에 반영한 수정

- **support.html**: 메타 description, keywords, og:title/description/image/url/type, canonical 추가.
- **index.html**: `<link rel="canonical" href="https://crossero.com/">` 추가.
- **list.html**: og:image를 절대 URL로 통일, og:type/og:url, canonical 추가.
- **about.html**: og:image 절대 URL, og:url, canonical 추가.
- **posts/index.html** (스크립트 템플릿): description, keywords, og 메타 추가. → 다음 발행 시 재생성되면 반영.

### 7.3 가이드에서 코드 외로 할 일 (수동)

- Google Search Console 등록 후 sitemap.xml, posts.xml 제출.
- Naver Search Advisor 등록 후 사이트맵 제출 및 수집 요청.
- URL 검사로 주요 페이지 색인 요청.
- (선택) og:image를 1200×630 비율로 제작·교체 시 SNS 미리보기 품질 향상.
