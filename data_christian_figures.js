/**
 * 십자가로세로 - 기독교 인물 퍼즐 데이터 (1차 샘플)
 * 성경 밖 기독교 인물(종교개혁자·선교사·한국 기독교 역사)을 다루는 새 콘텐츠 축.
 *
 * 작성 원칙:
 * - 문장은 특정 책/사이트를 그대로 베끼지 않고 퍼즐용으로 새로 작성
 * - 정답(answer)은 띄어쓰기 없이 저장 (data.js 기존 6,742개 정답 전부 공백 없음 - 엔진이
 *   한 칸=한 글자 구조라 공백 있는 정답은 그리드 생성이 깨질 수 있음). 띄어쓰기가 필요한
 *   이름은 clue 문장 안에서만 자연스럽게 표기.
 * - 한 퍼즐 안에서 정답 중복 없음(크로스워드는 같은 단어를 두 번 배치할 수 없음)
 * - "최초/설립" 등 역사적으로 이견이 있을 수 있는 표현은 게시 전 별도 검증 필요(1차 샘플 단계)
 *
 * data.js 로드 후 자동으로 QUIZ_DATABASE에 병합됨 (Object.assign).
 * 기존 data.js/data_bible_extra.js 파일은 건드리지 않음.
 */

const CHRISTIAN_FIGURES_DATABASE = {
  "cpl_001": {
    title: "기독교 인물: 종교개혁자들",
    category: "기독교인물, 종교개혁, 교회사, 중고등부용, 전체",
    meta: "보통 · 종교개혁",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "95개조 반박문으로 종교개혁을 시작한 독일의 신학자는?", answer: "루터" },
      { clue: "루터가 활동한 나라는?", answer: "독일" },
      { clue: "루터가 95개조 반박문을 붙인 도시는?", answer: "비텐베르크" },
      { clue: "루터의 종교개혁 사상에서 구원의 핵심이 되는 것은?", answer: "믿음" },
      { clue: "제네바에서 종교개혁을 이끈 신학자는?", answer: "칼뱅" },
      { clue: "칼뱅의 대표 저서는?", answer: "기독교강요" },
      { clue: "칼뱅이 활동한 나라는?", answer: "스위스" },
      { clue: "감리교 운동을 이끈 18세기 영국의 신학자는?", answer: "웨슬리" },
      { clue: "웨슬리가 강조한 신앙의 성장 개념은?", answer: "성화" },
      { clue: "웨슬리가 활동한 나라는?", answer: "영국" }
    ]
  },

  "cpl_002": {
    title: "기독교 인물: 선교사들",
    category: "기독교인물, 선교사, 교회사, 중고등부용, 전체",
    meta: "보통 · 선교사",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "근대 개신교 선교운동의 선구자로 불리는 영국 선교사는?", answer: "캐리" },
      { clue: "윌리엄 캐리가 선교사로 활동한 나라는?", answer: "인도" },
      { clue: "캐리가 힘쓴 성경과 문서 사역은?", answer: "번역" },
      { clue: "중국 내륙 선교로 유명한 영국 선교사는?", answer: "테일러" },
      { clue: "허드슨 테일러가 세운 선교 단체는?", answer: "중국내지선교회" },
      { clue: "테일러가 선교한 나라는?", answer: "중국" },
      { clue: "1885년 한국에 들어온 미국 장로교 선교사는?", answer: "언더우드" },
      { clue: "언더우드가 설립에 참여한 서울의 교회는?", answer: "새문안교회" },
      { clue: "배재학당을 세운 미국 감리교 선교사는?", answer: "아펜젤러" },
      { clue: "아펜젤러가 세운 학교는?", answer: "배재학당" },
      { clue: "아펜젤러가 속한 교단 전통은?", answer: "감리교" }
    ]
  },

  "cpl_003": {
    title: "기독교 인물: 한국 기독교 역사",
    category: "기독교인물, 한국기독교, 교회사, 중고등부용, 전체",
    meta: "보통 · 한국교회사",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "신사참배를 거부하다 순교한 한국의 목회자는?", answer: "주기철" },
      { clue: "주기철 목사가 거부한 일제의 종교적 강요는?", answer: "신사참배" },
      { clue: "신앙을 지키다 목숨을 잃는 것을 이르는 말은?", answer: "순교" },
      { clue: "애양원에서 한센인들을 섬긴 한국의 목회자는?", answer: "손양원" },
      { clue: "손양원 목사가 평생 사역한 시설은?", answer: "애양원" },
      { clue: "손양원 목사가 돌본 사람들은?", answer: "한센인" },
      { clue: "3·1운동에 참여한 대표적인 여성 독립운동가는?", answer: "유관순" },
      { clue: "유관순이 만세운동을 이끈 지역은?", answer: "아우내" },
      { clue: "유관순이 다닌 기독교 계열 학교는?", answer: "이화학당" }
    ]
  },

  "cpl_004": {
    title: "기독교 인물: 부흥운동가",
    category: "기독교인물, 부흥운동, 교회사, 중고등부용, 전체",
    meta: "보통 · 부흥운동",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "18세기 대각성운동의 유명한 설교자는?", answer: "휫필드" },
      { clue: "휫필드가 유명했던 사역은?", answer: "설교" },
      { clue: "휫필드가 자주 활용한 야외 설교 방식은?", answer: "야외설교" },
      { clue: "미국 제1차 대각성운동을 대표하는 설교자는?", answer: "에드워즈" },
      { clue: "에드워즈가 활동한 나라는?", answer: "미국" },
      { clue: "에드워즈와 관련된 대표적인 종교 운동은?", answer: "대각성운동" },
      { clue: "19세기 미국의 유명한 복음전도자는?", answer: "무디" },
      { clue: "무디가 설립한 교육기관으로 유명한 곳은?", answer: "무디성경학교" },
      { clue: "20세기 세계적인 복음전도자로 활동한 미국의 목회자는?", answer: "그레이엄" },
      { clue: "빌리 그레이엄이 활용한 대중 매체 가운데 하나는?", answer: "라디오" }
    ]
  },

  "cpl_005": {
    title: "기독교 인물: 신학자와 작가",
    category: "기독교인물, 신학자, 교회사, 중고등부용, 전체",
    meta: "보통 · 신학자",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "《고백록》을 쓴 대표적인 고대 기독교 사상가는?", answer: "아우구스티누스" },
      { clue: "아우구스티누스의 대표 저서는?", answer: "고백록" },
      { clue: "아우구스티누스가 주교로 활동한 북아프리카 도시는?", answer: "히포" },
      { clue: "20세기 영국 복음주의 지도자로 알려진 신학자는?", answer: "스토트" },
      { clue: "존 스토트가 오랜 기간 사역한 영국의 도시는?", answer: "런던" },
      { clue: "《나니아 연대기》를 쓴 기독교 작가는?", answer: "루이스" },
      { clue: "C. S. 루이스의 대표적인 판타지 작품은?", answer: "나니아연대기" },
      { clue: "나치 정권에 저항한 독일의 신학자는?", answer: "본회퍼" },
      { clue: "본회퍼가 신학적 신념으로 저항한 정권은?", answer: "나치" }
    ]
  },

  "cpl_006": {
    title: "기독교 인물: 한국 기독교 역사 2",
    category: "기독교인물, 한국기독교, 교회사, 중고등부용, 전체",
    meta: "보통 · 한국교회사",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "평양대부흥운동의 중심 인물로 알려진 한국 목회자는?", answer: "길선주" },
      { clue: "길선주와 관련된 대표적인 부흥운동은?", answer: "평양대부흥" },
      { clue: "영락교회를 설립한 한국의 목회자는?", answer: "한경직" },
      { clue: "한경직 목사가 세운 대표적인 교회는?", answer: "영락교회" },
      { clue: "오산학교를 세우고 3·1운동에 참여한 민족운동가는?", answer: "이승훈" },
      { clue: "이승훈이 세운 학교는?", answer: "오산학교" },
      { clue: "한국에서 간호와 선교 활동을 펼친 선교사는?", answer: "서서평" },
      { clue: "서서평의 주요 전문 분야는?", answer: "간호" },
      { clue: "《성서조선》을 중심으로 활동한 한국의 기독교 사상가는?", answer: "김교신" },
      { clue: "김교신과 관련된 잡지는?", answer: "성서조선" }
    ]
  }
};

if (typeof QUIZ_DATABASE !== 'undefined') {
  Object.assign(QUIZ_DATABASE, CHRISTIAN_FIGURES_DATABASE);
}
