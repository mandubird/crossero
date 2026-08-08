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
  }
};

if (typeof QUIZ_DATABASE !== 'undefined') {
  Object.assign(QUIZ_DATABASE, CHRISTIAN_FIGURES_DATABASE);
}
