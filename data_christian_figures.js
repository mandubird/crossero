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
  },

  "cpl_007": {
    title: "기독교 인물: 구약 성경 인물",
    category: "기독교인물, 성경인물, 구약, 주일학교용, 전체",
    meta: "쉬움 · 구약인물",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "하나님과 언약을 맺은 이스라엘의 믿음의 조상은?", answer: "아브라함" },
      { clue: "아브라함의 아내는?", answer: "사라" },
      { clue: "아브라함이 하나님의 명령으로 들어간 땅은?", answer: "가나안" },
      { clue: "이스라엘 백성을 이집트에서 이끌어 낸 지도자는?", answer: "모세" },
      { clue: "모세가 십계명을 받은 산은?", answer: "시내산" },
      { clue: "이스라엘 백성이 출애굽 중에 건넌 바다는?", answer: "홍해" },
      { clue: "모세의 뒤를 이어 이스라엘을 이끈 지도자는?", answer: "여호수아" },
      { clue: "여호수아가 이끈 군대가 함락시킨 성은?", answer: "여리고" },
      { clue: "골리앗과 싸워 이긴 이스라엘의 왕은?", answer: "다윗" },
      { clue: "다윗이 물리친 블레셋의 거인은?", answer: "골리앗" },
      { clue: "지혜로운 왕으로 유명한 다윗의 아들은?", answer: "솔로몬" },
      { clue: "솔로몬이 예루살렘에 건축한 대표적인 건물은?", answer: "성전" }
    ]
  },

  "cpl_008": {
    title: "기독교 인물: 성경 인물 (선지자와 사도)",
    category: "기독교인물, 성경인물, 구약, 신약, 주일학교용, 전체",
    meta: "쉬움 · 선지자와사도",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "갈멜산에서 바알 선지자들과 대결한 선지자는?", answer: "엘리야" },
      { clue: "엘리야가 바알 선지자들과 대결한 산은?", answer: "갈멜산" },
      { clue: "사자굴에 던져졌지만 살아난 성경 인물은?", answer: "다니엘" },
      { clue: "다니엘이 던져진 곳은?", answer: "사자굴" },
      { clue: "페르시아의 왕비가 되어 유대인을 구한 인물은?", answer: "에스더" },
      { clue: "에스더가 왕비가 된 제국은?", answer: "페르시아" },
      { clue: "예수의 열두 제자 가운데 원래 어부였던 인물은?", answer: "베드로" },
      { clue: "베드로의 형제이자 예수의 제자는?", answer: "안드레" },
      { clue: "다메섹으로 가던 길에서 회심한 사도는?", answer: "바울" },
      { clue: "바울이 회심한 길의 목적지는?", answer: "다메섹" }
    ]
  },

  "cpl_009": {
    title: "기독교 인물: 종교개혁과 선교·구제",
    category: "기독교인물, 종교개혁, 선교사, 중고등부용, 전체",
    meta: "보통 · 종교개혁·선교",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "스위스 취리히에서 종교개혁을 이끈 인물은?", answer: "츠빙글리" },
      { clue: "츠빙글리가 종교개혁을 이끈 스위스의 도시는?", answer: "취리히" },
      { clue: "브리스톨에서 고아들을 돌본 것으로 유명한 인물은?", answer: "뮬러" },
      { clue: "조지 뮬러의 사역과 관련된 대표적인 시설은?", answer: "고아원" },
      { clue: "미얀마 선교로 유명한 미국인 선교사는?", answer: "저드슨" },
      { clue: "아도니람 저드슨이 선교한 나라는?", answer: "미얀마" },
      { clue: "영어 성경 번역으로 유명한 종교개혁 시대 인물은?", answer: "틴들" },
      { clue: "윌리엄 틴들이 번역한 성경의 언어는?", answer: "영어" },
      { clue: "스코틀랜드 종교개혁을 이끈 인물은?", answer: "녹스" },
      { clue: "존 녹스가 종교개혁을 이끈 지역은?", answer: "스코틀랜드" },
      { clue: "루터의 동료이자 종교개혁의 교육자로 알려진 인물은?", answer: "멜란히톤" },
      { clue: "필립 멜란히톤이 힘쓴 활동 분야는?", answer: "교육" }
    ]
  },

  "cpl_010": {
    title: "기독교 인물: 설교자와 사상가",
    category: "기독교인물, 신학자, 교회사, 중고등부용, 전체",
    meta: "보통 · 설교자와사상가",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "19세기 영국의 유명한 설교자는?", answer: "스펄전" },
      { clue: "찰스 스펄전이 속했던 교단 전통은?", answer: "침례교" },
      { clue: "영국의 노예무역 폐지 운동에 힘쓴 정치인은?", answer: "윌버포스" },
      { clue: "윌버포스가 반대했던 대표적인 제도는?", answer: "노예무역" },
      { clue: "제2차 세계대전 중 유대인을 숨겨 도운 네덜란드의 기독교인은?", answer: "텐붐" },
      { clue: "코리 텐 붐이 활동한 유럽 국가는?", answer: "네덜란드" },
      { clue: "《신학대전》을 쓴 중세 신학자는?", answer: "아퀴나스" },
      { clue: "토마스 아퀴나스의 대표 저서는?", answer: "신학대전" },
      { clue: "아시시의 성인으로 알려진 인물은?", answer: "프란치스코" },
      { clue: "프란치스코가 활동한 이탈리아의 도시는?", answer: "아시시" },
      { clue: "20세기 영국의 대표적인 설교자는?", answer: "로이드존스" },
      { clue: "로이드 존스가 오래 사역한 런던의 교회는?", answer: "웨스트민스터채플" },
      { clue: "인도 콜카타에서 가난한 사람들을 돌본 인물은?", answer: "테레사" },
      { clue: "마더 테레사가 주로 활동한 인도의 도시는?", answer: "콜카타" }
    ]
  },

  "cpl_011": {
    title: "기독교 인물: 한국 기독교 역사 3",
    category: "기독교인물, 한국기독교, 교회사, 중고등부용, 전체",
    meta: "보통 · 한국교회사",
    config: { 1: { label: "가볍게", density: 0.15, qCount: 5, time: "5분" }, 2: { label: "보통", density: 0.35, qCount: 12, time: "10분" }, 3: { label: "어렵게", density: 0.60, qCount: 25, time: "25분" } },
    allWords: [
      { clue: "이화학당을 세운 미국 감리교 선교사는?", answer: "스크랜턴" },
      { clue: "메리 스크랜턴이 힘쓴 사역 분야는?", answer: "여성교육" },
      { clue: "일제강점기 부흥사로 활동한 한국의 목회자는?", answer: "김익두" },
      { clue: "김익두가 자주 인도한 사역은?", answer: "부흥회" },
      { clue: "제주도 선교로 알려진 한국의 장로교 목사는?", answer: "이기풍" },
      { clue: "이기풍이 선교 활동을 펼친 섬은?", answer: "제주" },
      { clue: "100주년기념교회 담임목사를 지낸 한국의 목회자는?", answer: "이재철" },
      { clue: "이재철 목사와 관련된 서울의 교회는?", answer: "기념교회" }
    ]
  }
};

if (typeof QUIZ_DATABASE !== 'undefined') {
  Object.assign(QUIZ_DATABASE, CHRISTIAN_FIGURES_DATABASE);
}
