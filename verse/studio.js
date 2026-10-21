/* 십자가로세로 말씀 카드 스튜디오 - 배경(직접 그린 풍경·그라데이션·내 사진)·무료 글꼴·크기 프리셋으로 말씀 카드를 만든다.
   외부 이미지를 쓰지 않으므로 저작권 걱정이 없다. window.crsStudio.setVerse({ref,text,topic}) 로 말씀을 전달한다. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var root = $('vstudio');
  if (!root) return;

  /* ---------- 데이터 ---------- */
  var PRESETS = [
    { k: 'sq', g: '카톡·인스타·SNS', n: '정사각 (카톡·인스타 피드)', w: 1080, h: 1080 },
    { k: 'ig45', g: '카톡·인스타·SNS', n: '인스타 4:5 세로', w: 1080, h: 1350 },
    { k: 'story', g: '휴대폰', n: '스토리·폰 배경화면 (9:16)', w: 1080, h: 1920 },
    { k: 'phone', g: '휴대폰', n: '아이폰·갤럭시 배경화면 (긴 화면)', w: 1170, h: 2532 },
    { k: 'profile', g: '프로필', n: '카톡·SNS 프로필 (정사각)', w: 800, h: 800 },
    { k: 'pc', g: '컴퓨터', n: 'PC 배경화면 (16:9 FHD)', w: 1920, h: 1080 },
    { k: 'pc2', g: '컴퓨터', n: 'PC 배경화면 (QHD 2560×1440)', w: 2560, h: 1440 },
    { k: 'link', g: '카톡·인스타·SNS', n: '링크 미리보기·유튜브 썸네일 (가로)', w: 1280, h: 720 },
    { k: 'a4', g: '인쇄', n: '인쇄 A4 세로', w: 2480, h: 3508, mm: 'A4' },
    { k: 'a5', g: '인쇄', n: '인쇄 A5 세로', w: 1748, h: 2480, mm: 'A5' },
    { k: 'a6', g: '인쇄', n: '엽서·주보 삽입 (A6 세로)', w: 1240, h: 1748, mm: 'A6' },
    { k: 'mark', g: '인쇄', n: '책갈피 (세로 긴 형태)', w: 600, h: 1800 }
  ];

  var FONTS = [
    { k: 'Noto Sans KR', n: '노토 산스 (깔끔한 고딕)', w: '400;700', css: 'Noto+Sans+KR:wght@400;700' },
    { k: 'Noto Serif KR', n: '노토 세리프 (단정한 명조)', w: '400;700', css: 'Noto+Serif+KR:wght@400;700' },
    { k: 'Nanum Myeongjo', n: '나눔명조', w: '400;700', css: 'Nanum+Myeongjo:wght@400;700' },
    { k: 'Gowun Batang', n: '고운바탕 (부드러운 바탕체)', w: '400;700', css: 'Gowun+Batang:wght@400;700' },
    { k: 'Gowun Dodum', n: '고운돋움', w: '400', css: 'Gowun+Dodum' },
    { k: 'Hahmlet', n: '함렛 (현대적 명조)', w: '400;700', css: 'Hahmlet:wght@400;700' },
    { k: 'Nanum Pen Script', n: '나눔 손글씨 펜', w: '400', css: 'Nanum+Pen+Script' },
    { k: 'Gaegu', n: '개구 (귀여운 손글씨)', w: '400;700', css: 'Gaegu:wght@400;700' },
    { k: 'Hi Melody', n: '하이멜로디 (손편지 느낌)', w: '400', css: 'Hi+Melody' },
    { k: 'Gamja Flower', n: '감자꽃', w: '400', css: 'Gamja+Flower' },
    { k: 'Jua', n: '주아 (둥근 제목체)', w: '400', css: 'Jua' },
    { k: 'Do Hyeon', n: '도현 (굵은 제목체)', w: '400', css: 'Do+Hyeon' },
    { k: 'Black Han Sans', n: '검은고딕 (강한 제목체)', w: '400', css: 'Black+Han+Sans' },
    { k: 'Song Myung', n: '송명 (고전 명조)', w: '400', css: 'Song+Myung' },
    { k: 'East Sea Dokdo', n: '동해독도 (붓글씨)', w: '400', css: 'East+Sea+Dokdo' },
    { k: 'Yeon Sung', n: '연성 (손글씨 캘리)', w: '400', css: 'Yeon+Sung' },
    { k: 'Nanum Brush Script', n: '나눔 붓글씨', w: '400', css: 'Nanum+Brush+Script' },
    { k: 'Dokdo', n: '독도 (거친 붓글씨)', w: '400', css: 'Dokdo' },
    { k: 'Poor Story', n: '푸어스토리 (일기장 손글씨)', w: '400', css: 'Poor+Story' },
    { k: 'Single Day', n: '싱글데이 (귀여운 손글씨)', w: '400', css: 'Single+Day' },
    { k: 'Cute Font', n: '큐트 폰트 (동글동글)', w: '400', css: 'Cute+Font' },
    { k: 'Kirang Haerang', n: '기랑해랑 (장난스러운 글씨)', w: '400', css: 'Kirang+Haerang' },
    { k: 'Dongle', n: '동글 (가는 둥근체)', w: '400', css: 'Dongle:wght@400' },
    { k: 'Stylish', n: '스타일리시 (세련된 손글씨)', w: '400', css: 'Stylish' },
    { k: 'Gasoek One', n: '가석원 (굵은 장식체)', w: '400', css: 'Gasoek+One' },
    { k: 'Gugi', n: '구기 (개성 있는 제목체)', w: '400', css: 'Gugi' },
    { k: 'Black And White Picture', n: '흑백사진 (스크립트체)', w: '400', css: 'Black+And+White+Picture' },
    { k: 'Diphylleia', n: '디필레이아 (우아한 명조)', w: '400', css: 'Diphylleia' },
    { k: 'Sunflower', n: '해바라기 (부드러운 고딕)', w: '500', css: 'Sunflower:wght@500' },
    { k: 'Nanum Gothic', n: '나눔고딕', w: '400;700', css: 'Nanum+Gothic:wght@400;700' },
    { k: 'IBM Plex Sans KR', n: 'IBM 플렉스 산스 KR', w: '400;700', css: 'IBM+Plex+Sans+KR:wght@400;700' },
    { k: 'Orbit', n: '오르빗 (둥근 현대체)', w: '400', css: 'Orbit' },
    { k: 'Pretendard Variable', n: '프리텐다드 (세련된 현대 고딕)', w: '400', u: 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css' },
    { k: 'SUIT Variable', n: '수트 (단정한 고딕)', w: '400', u: 'https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/variable/woff2/SUIT-Variable.css' },
    { k: 'Gothic A1', n: '고딕 A1 (깔끔한 고딕)', w: '400;700', css: 'Gothic+A1:wght@400;700' },
    { k: 'Cormorant Garamond', n: '코모란트 (영문 · 우아한 세리프)', w: '400;600', css: 'Cormorant+Garamond:wght@400;600' },
    { k: 'Playfair Display', n: '플레이페어 (영문 · 클래식)', w: '400;700', css: 'Playfair+Display:wght@400;700' },
    { k: 'Lora', n: '로라 (영문 · 읽기 편한 세리프)', w: '400;600', css: 'Lora:wght@400;600' },
    { k: 'Libre Baskerville', n: '바스커빌 (영문 · 단정한 세리프)', w: '400', css: 'Libre+Baskerville' },
    { k: 'Great Vibes', n: '그레이트 바이브스 (영문 · 필기체)', w: '400', css: 'Great+Vibes' },
    { k: 'Dancing Script', n: '댄싱 스크립트 (영문 · 캘리)', w: '400;600', css: 'Dancing+Script:wght@400;600' },
    { k: 'Caveat', n: '카비트 (영문 · 손글씨)', w: '400;600', css: 'Caveat:wght@400;600' }
  ];
  // 글꼴 분류(고르기 쉽게 묶어서 보여 준다)
  var FGROUPS = [['고딕', '깔끔한 고딕체'], ['명조', '단정한 명조·바탕체'], ['손글씨', '손글씨·붓글씨'], ['제목', '굵은 제목체·장식체'], ['영문', '영문 말씀용 (한글은 기본 글꼴로 표시)']];
  var FG = { 'Noto Sans KR': 0, 'Gowun Dodum': 0, 'Pretendard Variable': 0, 'SUIT Variable': 0, 'Gothic A1': 0, 'Nanum Gothic': 0, 'IBM Plex Sans KR': 0, 'Sunflower': 0, 'Orbit': 0,
    'Noto Serif KR': 1, 'Nanum Myeongjo': 1, 'Gowun Batang': 1, 'Hahmlet': 1, 'Song Myung': 1, 'Diphylleia': 1,
    'Nanum Pen Script': 2, 'Gaegu': 2, 'Hi Melody': 2, 'Gamja Flower': 2, 'East Sea Dokdo': 2, 'Yeon Sung': 2, 'Nanum Brush Script': 2, 'Dokdo': 2, 'Poor Story': 2, 'Single Day': 2, 'Cute Font': 2, 'Kirang Haerang': 2, 'Dongle': 2, 'Stylish': 2, 'Black And White Picture': 2,
    'Jua': 3, 'Do Hyeon': 3, 'Black Han Sans': 3, 'Gasoek One': 3, 'Gugi': 3,
    'Cormorant Garamond': 4, 'Playfair Display': 4, 'Lora': 4, 'Libre Baskerville': 4, 'Great Vibes': 4, 'Dancing Script': 4, 'Caveat': 4 };
  function fontUrl(f, text) { return f.u ? f.u : 'https://fonts.googleapis.com/css2?family=' + f.css + '&display=swap' + (text ? '&text=' + encodeURIComponent(text) : ''); }

  var SCENES = [
    { k: 'sunrise', n: '노을 산', light: false }, { k: 'sea', n: '푸른 바다', light: false }, { k: 'forest', n: '숲길 햇살', light: false },
    { k: 'night', n: '별 밤하늘', light: false }, { k: 'field', n: '황금 들판', light: false }, { k: 'snow', n: '겨울 설원', light: false },
    { k: 'lake', n: '호수·선착장', light: false }, { k: 'cross', n: '십자가 언덕', light: false }, { k: 'spring', n: '봄 꽃빛', light: true },
    { k: 'desert', n: '광야의 새벽', light: false }, { k: 'cloud', n: '하늘 구름', light: false }, { k: 'olive', n: '올리브 숲', light: true }
  ];
  if (window.crsBgScenes) window.crsBgScenes.list.forEach(function (q) { SCENES.push(q); });
  var GRADS = [
    ['#f6d365', '#fda085'], ['#a1c4fd', '#c2e9fb'], ['#84fab0', '#8fd3f4'], ['#fbc2eb', '#a6c1ee'], ['#232526', '#414345'], ['#0f2027', '#2c5364'],
    ['#ffecd2', '#fcb69f'], ['#e0c3fc', '#8ec5fc'], ['#fdfbfb', '#ebedee'], ['#667eea', '#764ba2'], ['#134e5e', '#71b280'], ['#f093fb', '#f5576c']
  ];
  var SOLIDS = ['#ffffff', '#f5efe2', '#1b2a41', '#0b5cad', '#2f3e2e', '#7a2e2e', '#222222', '#c8a24a'];
  var TEXTCOLORS = [['자동', 'auto'], ['흰색', '#ffffff'], ['크림', '#fff4d8'], ['검정', '#1d1d1d'], ['남색', '#16325c'], ['금색', '#f2c75c']];

  // 카드를 저장·공유·인쇄한 직후, 말씀에 마음이 열린 순간에 순례 게임 연결을 보여 준다.
  function pgDone() { if (window.crsPilgrimCta) window.crsPilgrimCta({ host: 'vsPgCta', campaign: 'studio_after_save' }); }

  /* ---------- 상태 ---------- */
  var S = { verse: null, preset: 'sq', bg: { type: 'scene', k: 'sunrise', seed: 7 }, font: 'Noto Serif KR', tcolor: 'auto', scale: 1, dim: 15, shadow: true, box: false,
            showRef: true, align: 'center', mark: true, img: null };
  try { var sv = JSON.parse(localStorage.getItem('crsStudio') || 'null'); if (sv) { for (var k0 in sv) if (k0 !== 'img' && k0 !== 'verse') S[k0] = sv[k0]; if (S.bg.type === 'image' || S.bg.type === 'photo') S.bg = { type: 'scene', k: 'sunrise', seed: 7 }; } } catch (e) {}
  function persist() { try { var c = {}; for (var k in S) if (k !== 'img' && k !== 'verse') c[k] = S[k]; localStorage.setItem('crsStudio', JSON.stringify(c)); } catch (e) {} }
  S.frame = S.frame || 'none'; S.orn = S.orn || 'none'; S.fx = S.fx || 'none'; S.dcolor = S.dcolor || 'text';
  function isDonor() { try { return typeof checkAuthStatus === 'function' && !!checkAuthStatus(); } catch (e) { return false; } }
  function track(n, p) { if (window.crsTrack) window.crsTrack(n, p || {}); }

  /* ---------- 난수·도우미 ---------- */
  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function vgrad(x, w, h, stops, y0, y1) { var g = x.createLinearGradient(0, (y0 || 0), 0, (y1 == null ? h : y1)); stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); x.fillStyle = g; x.fillRect(0, y0 || 0, w, (y1 == null ? h : y1) - (y0 || 0)); }
  function glow(x, cx, cy, r, c0, c1) { var g = x.createRadialGradient(cx, cy, 0, cx, cy, r); g.addColorStop(0, c0); g.addColorStop(1, c1 || 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(cx - r, cy - r, r * 2, r * 2); }
  function ridge(x, w, h, base, amp, color, seed, freq, grad2) {
    var R = rng(seed), ph = [R() * 6, R() * 6, R() * 6];
    x.beginPath(); x.moveTo(0, h);
    for (var i = 0; i <= w; i += Math.max(4, w / 220)) {
      var u = i / w;
      var y = base + Math.sin(u * freq + ph[0]) * amp + Math.sin(u * freq * 2.3 + ph[1]) * amp * 0.45 + Math.sin(u * freq * 5.1 + ph[2]) * amp * 0.18;
      x.lineTo(i, y);
    }
    x.lineTo(w, h); x.closePath();
    if (grad2) { var g = x.createLinearGradient(0, base - amp, 0, h); g.addColorStop(0, color); g.addColorStop(1, grad2); x.fillStyle = g; } else x.fillStyle = color;
    x.fill();
  }
  function cloudBlob(x, cx, cy, rw, rh, a) { var g = x.createRadialGradient(cx, cy, 0, cx, cy, rw); g.addColorStop(0, 'rgba(255,255,255,' + a + ')'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.save(); x.translate(cx, cy); x.scale(1, rh / rw); x.translate(-cx, -cy); x.fillStyle = g; x.beginPath(); x.arc(cx, cy, rw, 0, 7); x.fill(); x.restore(); }
  function stars(x, w, h, n, R, maxY) { for (var i = 0; i < n; i++) { var s = R() * R() * 2.4 + 0.5, px = R() * w, py = R() * (maxY || h), o = 0.35 + R() * 0.65; x.fillStyle = 'rgba(255,255,255,' + o + ')'; x.beginPath(); x.arc(px, py, s * (w / 1080), 0, 7); x.fill(); } }
  function pine(x, cx, by, ph, color) { x.fillStyle = color; for (var i = 0; i < 4; i++) { var tw = ph * (0.30 - i * 0.045), ty = by - ph * (0.15 + i * 0.22); x.beginPath(); x.moveTo(cx - tw, ty); x.lineTo(cx, ty - ph * 0.42); x.lineTo(cx + tw, ty); x.closePath(); x.fill(); } x.fillRect(cx - ph * 0.02, by - ph * 0.12, ph * 0.04, ph * 0.12); }
  function bokeh(x, w, h, n, R, colors, rmin, rmax, a) { for (var i = 0; i < n; i++) { var r = rmin + R() * (rmax - rmin), px = R() * w, py = R() * h; var c = colors[(R() * colors.length) | 0]; glow(x, px, py, r, c.replace('A', a * (0.4 + R() * 0.6)), c.replace('A', 0)); } }

  /* ---------- 풍경 배경 ---------- */
  var SCENE = {
    sunrise: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#7fb4e8'], [0.38, '#f6c07a'], [0.62, '#fde4a6'], [1, '#fff3c9']]);
      var sx = w * (0.32 + R() * 0.36), sy = h * 0.66;
      glow(x, sx, sy, w * 0.9, 'rgba(255,230,160,0.95)', 'rgba(255,200,120,0)');
      x.fillStyle = 'rgba(255,248,214,0.95)'; x.beginPath(); x.arc(sx, sy, w * 0.045, 0, 7); x.fill();
      for (var i = 0; i < 4; i++) cloudBlob(x, R() * w, h * (0.12 + R() * 0.3), w * (0.22 + R() * 0.2), h * 0.05, 0.5);
      ridge(x, w, h, h * 0.66, h * 0.05, '#b97d5a', sd + 1, 3, '#7a4a3a');
      ridge(x, w, h, h * 0.76, h * 0.06, '#8a5a42', sd + 2, 4, '#5a3a2c');
      ridge(x, w, h, h * 0.88, h * 0.05, '#4b3a2e', sd + 3, 5, '#2a2018');
    },
    sea: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#4aa7e8'], [0.45, '#bfe6ff'], [0.46, '#9be7ee'], [0.6, '#27b9c9'], [1, '#0b7a96']]);
      for (var i = 0; i < 4; i++) cloudBlob(x, R() * w, h * (0.06 + R() * 0.28), w * (0.25 + R() * 0.25), h * 0.06, 0.8);
      glow(x, w * 0.7, h * 0.46, w * 0.5, 'rgba(255,255,255,0.35)');
      for (var j = 0; j < 190; j++) { var u = R(), yy = h * (0.47 + u * u * 0.53), ww = w * (0.03 + (yy / h - 0.47) * 0.25 * R() + R() * 0.05), xx = R() * w; x.strokeStyle = 'rgba(255,255,255,' + (0.12 + R() * 0.3) + ')'; x.lineWidth = 1 + (yy / h - 0.47) * 7; x.beginPath(); x.moveTo(xx, yy); x.quadraticCurveTo(xx + ww / 2, yy - h * 0.008, xx + ww, yy); x.stroke(); }
      vgrad(x, w, h, [[0, 'rgba(255,255,255,0)'], [1, 'rgba(255,255,255,0.75)']], h * 0.9, h);
    },
    forest: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#cfe9a7'], [0.5, '#74a85a'], [1, '#2c5a2a']]);
      glow(x, w * 0.62, h * 0.22, w * 0.9, 'rgba(255,245,180,0.85)', 'rgba(255,245,180,0)');
      for (var i = 0; i < 9; i++) { var px = (i / 8) * w + (R() - 0.5) * w * 0.1, tw = w * (0.035 + R() * 0.05); x.fillStyle = 'rgba(30,55,25,' + (0.55 + R() * 0.35) + ')'; x.fillRect(px, -10, tw, h * 0.78); }
      for (var j = 0; j < 7; j++) { var rx = w * (0.4 + R() * 0.5); x.fillStyle = 'rgba(255,248,190,0.10)'; x.beginPath(); x.moveTo(rx, 0); x.lineTo(rx + w * 0.07, 0); x.lineTo(rx - w * 0.3, h * 0.85); x.lineTo(rx - w * 0.4, h * 0.85); x.closePath(); x.fill(); }
      x.fillStyle = '#b79b6b'; x.beginPath(); x.moveTo(w * 0.35, h); x.quadraticCurveTo(w * 0.47, h * 0.72, w * 0.5, h * 0.62); x.lineTo(w * 0.54, h * 0.62); x.quadraticCurveTo(w * 0.75, h * 0.74, w * 0.9, h); x.fill();
      vgrad(x, w, h, [[0, 'rgba(20,50,20,0)'], [1, 'rgba(20,50,20,0.55)']], h * 0.8, h);
    },
    night: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#050a24'], [0.55, '#1a2a6c'], [1, '#33407a']]);
      x.save(); x.translate(w * 0.5, h * 0.4); x.rotate(-0.5); glow(x, 0, 0, w * 0.85, 'rgba(190,170,255,0.45)', 'rgba(190,170,255,0)'); x.restore();
      stars(x, w, h, Math.round(w * h / 5500), R, h * 0.85);
      ridge(x, w, h, h * 0.86, h * 0.04, '#1b2542', sd + 4, 4, '#0a0f24');
    },
    field: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#fbd37a'], [0.5, '#fde9b8'], [0.62, '#e8b35c'], [1, '#8a5a1c']]);
      glow(x, w * 0.35, h * 0.55, w * 0.8, 'rgba(255,236,170,0.9)', 'rgba(255,220,140,0)');
      ridge(x, w, h, h * 0.62, h * 0.025, '#caa05a', sd + 1, 3, '#a47a3a');
      for (var i = 0; i < 520; i++) { var gx = R() * w, gy = h * (0.62 + R() * 0.38), gl = h * (0.05 + (gy / h - 0.6) * 0.45 * R()), bend = (R() - 0.5) * gl * 0.5; x.strokeStyle = 'rgba(' + (150 + R() * 70 | 0) + ',' + (100 + R() * 60 | 0) + ',30,' + (0.35 + R() * 0.55) + ')'; x.lineWidth = 2 + (gy / h) * 4; x.beginPath(); x.moveTo(gx, gy); x.quadraticCurveTo(gx + bend * 0.3, gy - gl * 0.6, gx + bend, gy - gl); x.stroke(); }
      bokeh(x, w, h * 0.6, 14, R, ['rgba(255,240,190,A)'], w * 0.015, w * 0.05, 0.5);
    },
    snow: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#7fa9d8'], [0.45, '#f3b9c6'], [0.7, '#ffe6d0'], [1, '#eef4fb']]);
      ridge(x, w, h, h * 0.62, h * 0.06, '#ffffff', sd + 1, 3, '#cfdcee');
      ridge(x, w, h, h * 0.78, h * 0.03, '#f4f8ff', sd + 2, 2, '#dbe6f4');
      for (var i = 0; i < 9; i++) pine(x, w * (0.05 + R() * 0.9), h * (0.8 + R() * 0.17), h * (0.16 + R() * 0.12), 'rgba(24,60,52,' + (0.75 + R() * 0.25) + ')');
      for (var s = 0; s < 80; s++) { x.fillStyle = 'rgba(255,255,255,' + (0.4 + R() * 0.5) + ')'; x.beginPath(); x.arc(R() * w, R() * h, 2 + R() * 4, 0, 7); x.fill(); }
    },
    lake: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#7fb6e8'], [0.4, '#d6ecfa'], [0.45, '#9dc9e8'], [1, '#3b79a6']]);
      for (var i = 0; i < 3; i++) cloudBlob(x, R() * w, h * (0.08 + R() * 0.2), w * 0.3, h * 0.05, 0.7);
      ridge(x, w, h * 0.46, h * 0.40, h * 0.04, '#6f8fb5', sd + 1, 3, '#8fa9c7');
      x.fillStyle = 'rgba(255,255,255,0.12)'; for (var j = 0; j < 30; j++) { x.fillRect(R() * w, h * (0.48 + R() * 0.5), w * (0.05 + R() * 0.15), 3); }
      var px0 = w * 0.38, py = h * 0.97; for (var p = 0; p < 12; p++) { var t = p / 11, yy = py - t * h * 0.34, ww = w * (0.07 - t * 0.035), xx = w * 0.5 + (px0 - w * 0.5) * 0; x.fillStyle = 'rgba(' + (150 - t * 40 | 0) + ',' + (110 - t * 30 | 0) + ',72,0.95)'; x.fillRect(xx - ww / 2, yy - h * 0.014, ww, h * 0.018); }
      x.strokeStyle = 'rgba(90,64,40,0.9)'; x.lineWidth = w * 0.006; x.beginPath(); x.moveTo(w * 0.5 - w * 0.03, h * 0.97); x.lineTo(w * 0.5 - w * 0.0, h * 0.63); x.moveTo(w * 0.5 + w * 0.03, h * 0.97); x.lineTo(w * 0.5 + w * 0.0, h * 0.63); x.stroke();
    },
    cross: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#f0a35a'], [0.35, '#fcd48f'], [0.6, '#fff1c8'], [1, '#fde9b6']]);
      glow(x, w * 0.5, h * 0.58, w * 0.8, 'rgba(255,245,200,0.95)', 'rgba(255,220,140,0)');
      ridge(x, w, h, h * 0.72, h * 0.04, '#c9915a', sd + 1, 3, '#a1704a');
      ridge(x, w, h, h * 0.84, h * 0.035, '#5d4a3a', sd + 2, 2.5, '#2f251d');
      var cx = w * 0.5, cy = h * 0.745, cw = Math.min(w, h) * 0.016, ch = h * 0.17; x.fillStyle = '#4a3322'; x.fillRect(cx - cw / 2, cy - ch * 0.5, cw, ch); x.fillRect(cx - ch * 0.19, cy - ch * 0.5 + ch * 0.18, ch * 0.38, cw);
      x.fillStyle = '#3a2b20'; x.beginPath(); x.ellipse(cx, cy + ch * 0.52, w * 0.13, h * 0.02, 0, 0, 7); x.fill();
    },
    spring: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#fdf3d0'], [0.5, '#e6f3c1'], [1, '#bde19b']]);
      bokeh(x, w, h, 26, R, ['rgba(255,236,150,A)', 'rgba(255,255,255,A)', 'rgba(200,235,150,A)'], w * 0.04, w * 0.13, 0.55);
      for (var i = 0; i < 18; i++) { var px = R() * w, py = h * (0.72 + R() * 0.26), r = w * (0.02 + R() * 0.03); x.fillStyle = 'rgba(255,255,255,0.95)'; for (var k = 0; k < 8; k++) { x.beginPath(); x.ellipse(px + Math.cos(k * 0.785) * r * 1.2, py + Math.sin(k * 0.785) * r * 1.2, r * 0.9, r * 0.45, k * 0.785, 0, 7); x.fill(); } x.fillStyle = '#f6c744'; x.beginPath(); x.arc(px, py, r * 0.6, 0, 7); x.fill(); }
    },
    desert: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#5a6fa8'], [0.3, '#d8a0a8'], [0.55, '#f9d29a'], [1, '#e0a964']]);
      glow(x, w * 0.65, h * 0.5, w * 0.7, 'rgba(255,225,160,0.9)', 'rgba(255,225,160,0)');
      ridge(x, w, h, h * 0.62, h * 0.04, '#d9a25f', sd + 1, 2.5, '#b9803f');
      ridge(x, w, h, h * 0.74, h * 0.05, '#c08a4d', sd + 2, 2, '#946432');
      ridge(x, w, h, h * 0.88, h * 0.05, '#8c5a2f', sd + 3, 2.2, '#5c3a1e');
      stars(x, w, h, 40, R, h * 0.3);
    },
    cloud: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#4a93e0'], [0.6, '#9fd0f5'], [1, '#e8f5ff']]);
      for (var i = 0; i < 14; i++) cloudBlob(x, R() * w, h * (0.1 + R() * 0.8), w * (0.18 + R() * 0.3), h * (0.04 + R() * 0.06), 0.75);
      glow(x, w * 0.2, h * 0.1, w * 0.6, 'rgba(255,255,255,0.55)');
    },
    olive: function (x, w, h, R, sd) {
      vgrad(x, w, h, [[0, '#f6f1dc'], [0.5, '#dfe6bd'], [1, '#aebf7e']]);
      bokeh(x, w, h, 30, R, ['rgba(120,150,70,A)', 'rgba(255,255,230,A)', 'rgba(170,190,110,A)'], w * 0.03, w * 0.1, 0.4);
      for (var b = 0; b < 3; b++) { var bx = w * (0.1 + b * 0.4 + R() * 0.2), by = h * (0.1 + R() * 0.2); x.strokeStyle = 'rgba(86,104,50,0.7)'; x.lineWidth = w * 0.005; x.beginPath(); x.moveTo(bx, by); x.quadraticCurveTo(bx + w * 0.2, by + h * 0.05, bx + w * 0.38, by + h * 0.02); x.stroke(); for (var l = 0; l < 12; l++) { var t = l / 11, lx = bx + w * 0.38 * t, ly = by + h * (0.05 * t * (1 - t) * 3.2 + 0.02 * t); x.fillStyle = 'rgba(' + (96 + R() * 30 | 0) + ',' + (130 + R() * 30 | 0) + ',70,0.85)'; x.beginPath(); x.ellipse(lx, ly + (l % 2 ? 1 : -1) * w * 0.018, w * 0.03, w * 0.009, (l % 2 ? 0.6 : -0.6), 0, 7); x.fill(); } }
    }
  };

  /* ---------- 배경 그리기 ---------- */
  var imgCache = null;
  function drawBg(x, w, h) {
    var b = S.bg;
    if (b.type === 'scene') { var R = rng(b.seed * 9973 + b.k.length * 31); (SCENE[b.k] || (window.crsBgScenes && window.crsBgScenes.draw[b.k]) || SCENE.sunrise)(x, w, h, R, b.seed * 7); }
    else if (b.type === 'grad') { var g = GRADS[b.i] || GRADS[0]; var gg = x.createLinearGradient(0, 0, w * 0.3, h); gg.addColorStop(0, g[0]); gg.addColorStop(1, g[1]); x.fillStyle = gg; x.fillRect(0, 0, w, h); }
    else if (b.type === 'solid') { x.fillStyle = b.c; x.fillRect(0, 0, w, h); }
    else if ((b.type === 'image' && S.img) || (b.type === 'photo' && S.pimg)) { var SI = b.type === 'photo' ? S.pimg : S.img; var iw = SI.width, ih = SI.height, sc = Math.max(w / iw, h / ih), dw = iw * sc, dh = ih * sc; x.drawImage(SI, (w - dw) / 2, (h - dh) / 2, dw, dh); }
    if (S.dim > 0) { x.fillStyle = 'rgba(0,0,0,' + (S.dim / 100 * 0.7) + ')'; x.fillRect(0, 0, w, h); }
  }
  function lightBg() {
    var b = S.bg;
    if (b.type === 'scene') { var s = SCENES.filter(function (q) { return q.k === b.k; })[0]; return s && s.light && S.dim < 30; }
    if (b.type === 'grad') return [1, 2, 3, 6, 8].indexOf(b.i) > -1 && S.dim < 25;
    if (b.type === 'solid') return ['#ffffff', '#f5efe2', '#c8a24a'].indexOf(b.c) > -1 && S.dim < 25;
    return false;
  }

  /* ---------- 글자 ---------- */
  function fontStack() { return '"' + S.font + '","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif'; }
  function wrapLines(x, text, maxW) {
    var words = text.split(' '), lines = [], line = '';
    words.forEach(function (w) { var t = line ? line + ' ' + w : w; if (x.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t; });
    if (line) lines.push(line);
    return lines;
  }
  function balance(x, text, maxW) {
    var base = wrapLines(x, text, maxW), n = base.length;
    if (n < 2) return base;
    var lo = maxW * 0.35, hi = maxW, best = base;
    for (var i = 0; i < 14; i++) { var mid = (lo + hi) / 2, l = wrapLines(x, text, mid); if (l.length <= n) { best = l; hi = mid; } else lo = mid; }
    return best;
  }
  function render(cv, w, h, forExport) {
    cv.width = w; cv.height = h; var x = cv.getContext('2d');
    drawBg(x, w, h);
    var v = S.verse || { text: '여호와는 나의 목자시니 내게 부족함이 없으리로다', ref: '시편 23:1' };
    var tc = S.tcolor;
    if (tc === 'auto') {
      var lum = 0, cnt = 0;
      try {
        var sx0 = Math.round(w * 0.18), sy0 = Math.round(h * 0.28), sw = Math.round(w * 0.64), sh = Math.round(h * 0.44);
        var dat = x.getImageData(sx0, sy0, sw, sh).data, stp = Math.max(1, Math.floor(dat.length / 4 / 1800)) * 4;
        for (var q = 0; q < dat.length; q += stp) { lum += 0.299 * dat[q] + 0.587 * dat[q + 1] + 0.114 * dat[q + 2]; cnt++; }
        lum = cnt ? lum / cnt : 90;
      } catch (e) { lum = lightBg() ? 200 : 90; }
      tc = lum > 168 ? '#1d1d1d' : '#ffffff';
    }
    var dark = tc === '#1d1d1d' || tc === '#16325c';
    var autoLum = (S.tcolor === 'auto') ? (typeof lum === 'number' ? lum : null) : null;
    if (autoLum !== null) {
      // 밝기가 애매한 배경(중간 밝기)에서는 글 뒤에 은은한 번짐을 깔아 글씨가 또렷하게 보이게 한다.
      var veil = null;
      if (autoLum < 150 && autoLum > 80) veil = 'rgba(0,0,0,' + (0.34 * (autoLum - 80) / 70).toFixed(3) + ')';
      else if (autoLum >= 150 && autoLum < 215) veil = 'rgba(255,255,255,' + (0.4 * (215 - autoLum) / 65).toFixed(3) + ')';
      if (veil) { x.save(); x.translate(w / 2, h * 0.5); x.scale(1, (h * 0.42) / (w * 0.7)); var vg = x.createRadialGradient(0, 0, 0, 0, 0, w * 0.7); vg.addColorStop(0, veil); vg.addColorStop(0.6, veil.replace(/[\d.]+\)$/, function (m) { return (parseFloat(m) * 0.55) + ')'; })); vg.addColorStop(1, veil.replace(/[\d.]+\)$/, '0)')); x.fillStyle = vg; x.beginPath(); x.arc(0, 0, w * 0.7, 0, 7); x.fill(); x.restore(); }
    }
    var D = window.crsDeco, dcol = S.dcolor === 'text' ? tc : S.dcolor;
    if (D && S.fx !== 'none') D.fx(x, w, h, S.fx);
    if (D && S.frame !== 'none') D.frame(x, w, h, S.frame, S.frame === 'mat' ? '#fbf8f1' : dcol);
    var portraitish = h >= w;
    var padX = w * (portraitish ? 0.12 : 0.16);
    var maxW = w - padX * 2, maxH = h * (portraitish ? 0.62 : 0.6);
    var MUL = { 'Nanum Pen Script': 1.55, 'Gaegu': 1.3, 'Hi Melody': 1.3, 'Gamja Flower': 1.3, 'East Sea Dokdo': 1.6, 'Yeon Sung': 1.15, 'Black Han Sans': 0.95, 'Song Myung': 1.05, 'Nanum Brush Script': 1.5, 'Dokdo': 1.5, 'Poor Story': 1.3, 'Single Day': 1.3, 'Cute Font': 1.3, 'Kirang Haerang': 1.15, 'Dongle': 1.9, 'Stylish': 1.15, 'Gasoek One': 0.95, 'Black And White Picture': 1.05, 'Orbit': 1.05, 'Great Vibes': 1.4, 'Dancing Script': 1.2, 'Caveat': 1.35, 'Cormorant Garamond': 1.15, 'Libre Baskerville': 0.92 };
    var fs = Math.min(w, h) * (portraitish ? 0.058 : 0.07) * S.scale * (MUL[S.font] || 1), lines, lh, total;
    var fam = fontStack();
    for (var it = 0; it < 30; it++) {
      x.font = (S.font === 'Black Han Sans' || S.font === 'Do Hyeon' || S.font === 'Jua' ? '' : '') + Math.round(fs) + 'px ' + fam;
      var limitW = Math.min(maxW, fs * (portraitish ? 11.5 : 17));
      lines = balance(x, v.text, limitW); lh = fs * 1.62; total = lines.length * lh;
      if (total <= maxH && lines.every(function (l) { return x.measureText(l).width <= maxW + 1; })) break;
      fs *= 0.93;
    }
    var rs = fs * 0.62, refH = (S.showRef && v.ref) ? rs * 2.4 : 0;
    var startY = (h - (total + refH)) / 2 + lh * 0.55 - (h * 0.02);
    var left = S.align === 'left';
    var tx = left ? padX : w / 2;
    x.textAlign = left ? 'left' : 'center'; x.textBaseline = 'middle';
    if (S.box) { var bw = Math.max.apply(null, lines.map(function (l) { return x.measureText(l).width; })) + fs * 2.2, bh = total + refH + fs * 1.6; x.fillStyle = dark ? 'rgba(255,255,255,0.55)' : 'rgba(0,0,0,0.35)'; var bx = left ? padX - fs : (w - bw) / 2; rr(x, bx, startY - lh * 0.55 - fs * 0.8, bw, bh, fs * 0.5); x.fill(); }
    if (S.shadow && !dark) { x.shadowColor = 'rgba(0,0,0,0.45)'; x.shadowBlur = fs * 0.35; x.shadowOffsetY = fs * 0.05; }
    x.fillStyle = tc;
    lines.forEach(function (l, i) { x.fillText(l, tx, startY + i * lh); });
    if (S.showRef && v.ref) {
      x.font = Math.round(rs) + 'px ' + fam; x.globalAlpha = 0.9;
      x.fillText(v.ref, tx, startY + total + rs * 0.9);
      x.globalAlpha = 1;
    }
    x.shadowColor = 'transparent'; x.shadowBlur = 0;
    if (D && S.orn !== 'none') { var mm = Math.min(w, h), osz = mm * (portraitish ? 0.12 : 0.1), top = startY - lh * 0.55 - (S.box ? fs * 0.8 : 0), oy = Math.max(top - osz * 0.7 - mm * 0.02, osz * 0.6 + mm * 0.07); D.orn(x, left ? padX + osz * 0.5 : w / 2, oy, osz, S.orn, dcol); }
    if (S.bg.type === 'photo' && S.pcredit) { x.font = Math.round(Math.min(w, h) * 0.017) + 'px "Noto Sans KR",sans-serif'; x.textAlign = 'center'; x.globalAlpha = 0.65; x.fillStyle = dark ? '#333' : '#fff'; x.fillText(S.pcredit, w / 2, h - Math.min(w, h) * 0.016); x.globalAlpha = 1; }
    if (S.mark && !isDonor()) { x.font = Math.round(Math.min(w, h) * 0.026) + 'px "Noto Sans KR",sans-serif'; x.textAlign = 'center'; x.globalAlpha = 0.7; x.fillStyle = dark ? '#333' : '#fff'; x.fillText('십자가로세로 · crossero.com', w / 2, h - Math.min(w, h) * 0.045); x.globalAlpha = 1; }
    else if (S.mark && isDonor() && false) { /* 후원자: 워터마크 없음 */ }
  }
  function rr(x, a, b, w, h, r) { x.beginPath(); x.moveTo(a + r, b); x.arcTo(a + w, b, a + w, b + h, r); x.arcTo(a + w, b + h, a, b + h, r); x.arcTo(a, b + h, a, b, r); x.arcTo(a, b, a + w, b, r); x.closePath(); }

  /* ---------- 글꼴 로딩 ---------- */
  var loaded = {};
  function loadFont(k, sample0) {
    var f = FONTS.filter(function (q) { return q.k === k; })[0];
    if (!f) return Promise.resolve();
    if (!loaded[k]) {
      loaded[k] = new Promise(function (res) {
        var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = fontUrl(f);
        l.onload = function () { res(); }; l.onerror = function () { res(); }; document.head.appendChild(l);
        setTimeout(res, 4000);
      });
    }
    return loaded[k].then(function () {
      var sample = sample0 || (S.verse ? S.verse.text + S.verse.ref : '여호와는 나의 목자시니 내게 부족함이 없으리로다 시편 23:1 십자가로세로 crossero.com');
      return document.fonts && document.fonts.load ? document.fonts.load('40px "' + k + '"', sample).catch(function () {}) : null;
    });
  }

  /* ---------- 화면 ---------- */
  var cv = $('vsCanvas'), busy = false, pend = false;
  function preset() { return PRESETS.filter(function (p) { return p.k === S.preset; })[0] || PRESETS[0]; }
  function paint() {
    var p = preset(), sc = Math.min(1, 720 / Math.max(p.w, p.h));
    var w = Math.round(p.w * sc), h = Math.round(p.h * sc);
    var S2 = S.scale; render(cv, w, h);
    cv.style.aspectRatio = p.w + ' / ' + p.h;
    $('vsInfo').textContent = p.n + ' · ' + p.w + '×' + p.h + 'px' + (p.mm ? ' · ' + p.mm : '');
  }
  function refresh() {
    persist();
    if (busy) { pend = true; return; }
    busy = true;
    loadFont(S.font).then(function () { paint(); busy = false; if (pend) { pend = false; refresh(); } });
  }
  function exportBlob(type) {
    var p = preset(), c = document.createElement('canvas');
    return loadFont(S.font).then(function () { render(c, p.w, p.h, true); return new Promise(function (res) { c.toBlob(res, type || 'image/png', 0.95); }); });
  }
  function fname(ext) { return '말씀카드-' + (S.verse ? S.verse.ref.replace(/\s|:/g, '_') : 'verse') + '-' + S.preset + '.' + ext; }
  function download(blob, name) { var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000); }

  /* ---------- 컨트롤 만들기 ---------- */
  function build() {
    var sel = $('vsPreset'); var grp = {};
    PRESETS.forEach(function (p) { (grp[p.g] = grp[p.g] || []).push(p); });
    Object.keys(grp).forEach(function (g) { var og = document.createElement('optgroup'); og.label = g; grp[g].forEach(function (p) { var o = document.createElement('option'); o.value = p.k; o.textContent = p.n + ' (' + p.w + '×' + p.h + ')'; og.appendChild(o); }); sel.appendChild(og); });
    sel.value = S.preset;
    sel.addEventListener('change', function () { S.preset = sel.value; track('studio_preset', { preset: S.preset }); refresh(); });
    // 쉬운 용도 고르기(큰 버튼). 위 select 는 내부용으로만 유지한다.
    var USES = [
      { k: 'sq', i: '💬', t: '카카오톡·인스타에 올리기', d: '정사각 사진 · 가장 많이 써요', star: 1 },
      { k: 'phone', i: '📱', t: '휴대폰 배경화면', d: '아이폰·갤럭시 긴 화면' },
      { k: 'profile', i: '👤', t: '프로필 사진', d: '카톡·SNS 동그란 프로필' },
      { k: 'pc', i: '🖥️', t: '컴퓨터 배경화면', d: '넓은 화면(16:9)' },
      { k: 'a4', i: '🖨️', t: '종이로 인쇄하기', d: 'A4 큰 종이 한 장' },
      { k: 'a6', i: '✉️', t: '엽서·주보에 넣기', d: 'A6 작은 크기' },
      { k: 'mark', i: '📑', t: '책갈피', d: '길쭉한 세로 모양' }
    ], MORE = ['ig45', 'story', 'pc2', 'link', 'a5'];
    var ug = $('vsUse'), um = $('vsUseMore'), un = $('vsUseNote');
    function pick(k) { S.preset = k; sel.value = k; track('studio_preset', { preset: k }); umark(); refresh(); }
    function umark() {
      [].forEach.call(root.querySelectorAll('[data-pk]'), function (b) { b.classList.toggle('on', b.dataset.pk === S.preset); });
      var p = preset(), u = USES.filter(function (q) { return q.k === p.k; })[0]; if (un) un.textContent = '지금 선택: ' + (u ? u.t : p.n);
    }
    if (ug) {
      USES.forEach(function (u) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-u'; b.dataset.pk = u.k;
        b.innerHTML = '<i>' + u.i + '</i><div><b>' + u.t + (u.star ? '<em>기본</em>' : '') + '</b><span>' + u.d + '</span></div>';
        b.addEventListener('click', function () { pick(u.k); }); ug.appendChild(b);
      });
      MORE.forEach(function (k) {
        var p = PRESETS.filter(function (q) { return q.k === k; })[0]; if (!p) return;
        var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-chip'; b.dataset.pk = k; b.textContent = p.n;
        b.addEventListener('click', function () { pick(k); }); um.appendChild(b);
      });
      umark();
    }

    // 장식
    (function () {
      var D = window.crsDeco; if (!D) return;
      function group(id, list, key) {
        var el = $(id); if (!el) return;
        list.forEach(function (o) {
          var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-chip'; b.dataset.k = o.k; b.dataset.g = key; b.textContent = o.n;
          b.addEventListener('click', function () { S[key] = o.k; if (key === 'orn' && o.k !== 'none' && S.dcolor === 'text') { } track('studio_deco', { kind: key, k: o.k }); dmark(); refresh(); });
          el.appendChild(b);
        });
      }
      group('vsOrn', D.ORN, 'orn'); group('vsFrame', D.FRAMES, 'frame'); group('vsFx', D.FX, 'fx');
      var dc = $('vsDcolor'); if (dc) [['글자색', 'text'], ['금색', '#f2c75c'], ['흰색', '#ffffff'], ['크림', '#fff4d8']].forEach(function (c) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-chip'; b.dataset.c = c[1]; b.textContent = c[0]; b.addEventListener('click', function () { S.dcolor = c[1]; dmark(); refresh(); }); dc.appendChild(b);
      });
      window.__dmark = dmark;
      function dmark() { [].forEach.call(root.querySelectorAll('[data-g]'), function (b) { b.classList.toggle('on', S[b.dataset.g] === b.dataset.k); }); [].forEach.call(root.querySelectorAll('#vsDcolor [data-c]'), function (b) { b.classList.toggle('on', S.dcolor === b.dataset.c); }); }
      dmark();
    })();

    // 사진 배경
    var PH = null, pg = $('vsPhotos'), pt = $('vsPhotoThemes'), pcur = 'all';
    function usePhoto(p) {
      var im = new Image(); im.onload = function () { S.pimg = im; S.pcredit = '사진: ' + p.artist + ' · ' + p.lic + ' · Wikimedia Commons'; S.bg = { type: 'photo', id: p.id }; mark(); pinfo(p); refresh(); }; im.src = '/images/studio/' + p.id + '.jpg';
    }
    function pinfo(p) { var e = $('vsPhotoCredit'); if (!e) return; e.innerHTML = '사진: <a href="' + p.src + '" target="_blank" rel="noopener nofollow">' + p.title.replace(/</g, '') + '</a> · ' + p.artist.replace(/</g, '') + ' · <a href="' + p.licurl + '" target="_blank" rel="noopener nofollow">' + p.lic + '</a>'; }
    function drawPhotos() {
      pg.innerHTML = '';
      PH.photos.filter(function (p) { return pcur === 'all' || p.theme === pcur; }).forEach(function (p) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-ph'; b.dataset.id = p.id; b.title = p.title + ' / ' + p.artist;
        var i = document.createElement('img'); i.loading = 'lazy'; i.alt = p.title; i.src = '/images/studio/' + p.id + '_t.jpg'; b.appendChild(i);
        b.addEventListener('click', function () { usePhoto(p); track('studio_photo', { id: p.id, theme: p.theme }); });
        pg.appendChild(b);
      });
      mark();
    }
    fetch('/verse/studio_photos.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
      PH = d;
      var all = [['all', '전체']].concat(Object.keys(d.themes).map(function (k) { return [k, d.themes[k]]; }));
      all.forEach(function (t) { var c = document.createElement('button'); c.type = 'button'; c.className = 'vs-chip' + (t[0] === 'all' ? ' on' : ''); c.textContent = t[1]; c.addEventListener('click', function () { pcur = t[0]; [].forEach.call(pt.children, function (q) { q.classList.toggle('on', q === c); }); drawPhotos(); }); pt.appendChild(c); });
      drawPhotos();
      if (!window.__studioInit && !/[?&]b=/.test(location.search)) { window.__studioInit = 1; var pool = ['sunrise2', 'lake4', 'forest6', 'mountain4', 'sky7', 'autumn2', 'field1', 'flower4', 'sunrise4', 'night2', 'desert5', 'lake7']; var id = pool[(Math.random() * pool.length) | 0]; var p = d.photos.filter(function (q) { return q.id === id; })[0]; if (p && S.bg.type === 'scene' && S.bg.k === 'sunrise' && S.bg.seed === 7) usePhoto(p); }
      $('vsRandom').dataset.ph = 1;
    }).catch(function () {});

    // 풍경 썸네일
    var sg = $('vsScenes');
    SCENES.forEach(function (s) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-th'; b.title = s.n; b.dataset.k = s.k;
      var c = document.createElement('canvas'); c.width = 96; c.height = 128; b.appendChild(c);
      var sv = S.bg; S.bg = { type: 'scene', k: s.k, seed: 7 }; var sd = S.dim; S.dim = 0; drawBg(c.getContext('2d'), 96, 128); S.bg = sv; S.dim = sd;
      var sp = document.createElement('span'); sp.textContent = s.n; b.appendChild(sp);
      b.addEventListener('click', function () { S.bg = { type: 'scene', k: s.k, seed: (S.bg.type === 'scene' && S.bg.k === s.k) ? S.bg.seed + 1 : 7 }; mark(); track('studio_bg', { bg: s.k }); refresh(); });
      sg.appendChild(b);
    });
    var gg = $('vsGrads');
    GRADS.forEach(function (g, i) { var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-sw'; b.style.background = 'linear-gradient(135deg,' + g[0] + ',' + g[1] + ')'; b.dataset.g = i; b.addEventListener('click', function () { S.bg = { type: 'grad', i: i }; mark(); refresh(); }); gg.appendChild(b); });
    SOLIDS.forEach(function (c) { var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-sw'; b.style.background = c; b.dataset.c = c; b.addEventListener('click', function () { S.bg = { type: 'solid', c: c }; mark(); refresh(); }); gg.appendChild(b); });
    $('vsUpload').addEventListener('change', function (e) {
      var f = e.target.files && e.target.files[0]; if (!f) return;
      var img = new Image(); img.onload = function () { S.img = img; S.bg = { type: 'image' }; mark(); track('studio_upload'); refresh(); }; img.src = URL.createObjectURL(f);
    });
    function mark() {
      [].forEach.call(root.querySelectorAll('.vs-ph'), function (b) { b.classList.toggle('on', S.bg.type === 'photo' && S.bg.id === b.dataset.id); });
      [].forEach.call(root.querySelectorAll('.vs-th'), function (b) { b.classList.toggle('on', S.bg.type === 'scene' && S.bg.k === b.dataset.k); });
      [].forEach.call(root.querySelectorAll('.vs-sw'), function (b) { b.classList.toggle('on', (S.bg.type === 'grad' && b.dataset.g == S.bg.i) || (S.bg.type === 'solid' && b.dataset.c === S.bg.c)); });
    }
    mark();
    $('vsVar').addEventListener('click', function () { if (S.bg.type === 'scene') { S.bg.seed = (S.bg.seed || 7) + 1; refresh(); } });

    // 글꼴
    var fl = $('vsFonts');
    FGROUPS.forEach(function (g, gi) {
      var hd = document.createElement('div'); hd.className = 'vs-fgh'; hd.textContent = g[1]; fl.appendChild(hd);
      FONTS.filter(function (f) { return (FG[f.k] === undefined ? 0 : FG[f.k]) === gi; }).forEach(function (f) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-font'; b.dataset.k = f.k;
        b.innerHTML = '<span class="n">' + f.n + '</span><span class="s" style="font-family:\'' + f.k + '\',sans-serif">' + (gi === 4 ? 'The Lord is my shepherd' : '여호와는 나의 목자시니') + '</span>';
        b.addEventListener('click', function () { S.font = f.k; fmark(); track('studio_font', { font: f.k }); refresh(); });
        fl.appendChild(b);
      });
    });
    function fmark() { [].forEach.call(root.querySelectorAll('.vs-font'), function (b) { b.classList.toggle('on', b.dataset.k === S.font); }); }
    fmark();
    var fontsOpened = false;
    $('vsFontBox').addEventListener('toggle', function () { if (this.open && !fontsOpened) { fontsOpened = true; FONTS.forEach(function (f) { var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = fontUrl(f, '여호와는나의목자시니' + f.n + 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'); document.head.appendChild(l); }); } });

    // 글자색
    var tl = $('vsTcolor');
    TEXTCOLORS.forEach(function (t) { var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-chip'; b.textContent = t[0]; b.dataset.c = t[1]; b.addEventListener('click', function () { S.tcolor = t[1]; cmark(); refresh(); }); tl.appendChild(b); });
    function cmark() { [].forEach.call(tl.children, function (b) { b.classList.toggle('on', b.dataset.c === S.tcolor); }); }
    cmark();

    function bindRange(id, key, scale) { var el = $(id); el.value = key === 'scale' ? Math.round(S.scale * 100) : S[key]; el.addEventListener('input', function () { S[key] = key === 'scale' ? el.value / 100 : +el.value; refresh(); }); }
    bindRange('vsScale', 'scale'); bindRange('vsDim', 'dim');
    function bindCheck(id, key) { var el = $(id); el.checked = !!S[key]; el.addEventListener('change', function () { S[key] = el.checked; refresh(); }); }
    bindCheck('vsShadow', 'shadow'); bindCheck('vsBox', 'box'); bindCheck('vsRef', 'showRef');
    var ml = $('vsMark'); ml.checked = true;
    if (isDonor()) { $('vsMarkNote').textContent = '후원자님은 워터마크 없이 저장됩니다 🙏'; ml.disabled = true; ml.checked = false; S.mark = false; }
    else { $('vsMarkNote').innerHTML = '작은 워터마크가 들어갑니다. <a href="/support.html" data-ga="studio_to_support">후원하시면 워터마크 없이 저장</a>할 수 있어요.'; ml.disabled = true; S.mark = true; }
    var al = $('vsAlign'); al.value = S.align; al.addEventListener('change', function () { S.align = al.value; refresh(); });

    // 말씀 직접 고르기
    var dl = $('vsRefs'); (window.__VERSES || []).forEach(function (d) { var o = document.createElement('option'); o.value = d.ref; dl.appendChild(o); });
    $('vsPick').addEventListener('change', function () { var d = (window.__VERSES || []).filter(function (q) { return q.ref === $('vsPick').value.trim(); })[0]; if (d) { api.setVerse(d); track('studio_pick', { ref: d.ref }); } });

    syncUI = function () { mark(); fmark(); cmark(); if (window.__dmark) window.__dmark(); try { $('vsDim').value = S.dim; $('vsScale').value = Math.round(S.scale * 100); } catch (e) {} };
    var ctl = root.querySelector('.vs-ctl'); if (ctl) ctl.addEventListener('click', function () { touched = true; });
    if ($('vsShuffle')) $('vsShuffle').addEventListener('click', function () { touched = false; applyRandom().then(function () { syncUI(); refresh(); track('studio_shuffle'); }); });
    if ($('vsLink')) $('vsLink').addEventListener('click', function () {
      var u = deepLink(), b = $('vsLink');
      var done = function () { b.textContent = '✅ 링크 복사됨'; setTimeout(function () { b.textContent = '🔗 링크 복사'; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(done, function () { prompt('링크를 복사하세요', u); }); else prompt('링크를 복사하세요', u);
      track('studio_link_copy');
    });

    // 스타일 랜덤
    $('vsRandom').addEventListener('click', function () {
      var r = Math.random;
      var usedPhoto = false;
      if (PH && r() < 0.7) { var pp = PH.photos[(r() * PH.photos.length) | 0]; usePhoto(pp); usedPhoto = true; }
      else { var sc = SCENES[(r() * SCENES.length) | 0]; S.bg = { type: 'scene', k: sc.k, seed: 1 + ((r() * 30) | 0) }; }
      S.font = FONTS[(r() * FONTS.length) | 0].k; S.tcolor = 'auto'; S.dim = 10 + ((r() * 25) | 0); $('vsDim').value = S.dim;
      var D2 = window.crsDeco; if (D2) { S.orn = r() < 0.55 ? D2.ORN[1 + ((r() * (D2.ORN.length - 1)) | 0)].k : 'none'; S.frame = r() < 0.4 ? D2.FRAMES[1 + ((r() * (D2.FRAMES.length - 1)) | 0)].k : 'none'; S.fx = r() < 0.35 ? D2.FX[1 + ((r() * (D2.FX.length - 1)) | 0)].k : 'none'; S.dcolor = 'text'; if (window.__dmark) window.__dmark(); }
      mark(); fmark(); cmark(); track('studio_random'); refresh();
    });
    $('vsSave').addEventListener('click', function () { exportBlob('image/png').then(function (b) { download(b, fname('png')); pgDone(); track('studio_save', { preset: S.preset, font: S.font, bg: S.bg.type === 'scene' ? S.bg.k : S.bg.type, donor: isDonor() }); }); });
    $('vsSaveJpg').addEventListener('click', function () { exportBlob('image/jpeg').then(function (b) { download(b, fname('jpg')); pgDone(); track('studio_save', { preset: S.preset, type: 'jpg' }); }); });
    $('vsShare').addEventListener('click', function () {
      exportBlob('image/png').then(function (b) {
        var f = new File([b], fname('png'), { type: 'image/png' });
        if (navigator.canShare && navigator.canShare({ files: [f] })) { navigator.share({ files: [f], title: S.verse ? S.verse.ref : '말씀 카드', text: (S.verse ? S.verse.ref + ' ' : '') + '십자가로세로 crossero.com' }).catch(function () {}); pgDone(); track('studio_share', { via: 'native' }); }
        else { download(b, fname('png')); alert('이 기기에서는 바로 공유가 어려워 이미지를 저장했어요. 카카오톡·인스타그램에서 저장된 사진을 올려 주세요.'); pgDone(); track('studio_share', { via: 'download' }); }
      });
    });
    $('vsPrint').addEventListener('click', function () {
      var p = preset();
      exportBlob('image/png').then(function (b) {
        var url = URL.createObjectURL(b), fr = document.createElement('iframe'); fr.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0';
        var size = p.mm ? p.mm + ' portrait' : (p.w > p.h ? 'A4 landscape' : 'A4 portrait');
        fr.srcdoc = '<!doctype html><html><head><style>@page{size:' + size + ';margin:0}html,body{margin:0;height:100%}img{width:100%;height:100%;object-fit:contain;display:block}</style></head><body><img src="' + url + '"></body></html>';
        document.body.appendChild(fr);
        fr.onload = function () { setTimeout(function () { try { fr.contentWindow.focus(); fr.contentWindow.print(); } catch (e) { download(b, fname('png')); } setTimeout(function () { fr.remove(); }, 60000); }, 400); };
        pgDone(); track('studio_print', { preset: S.preset });
      });
    });

    // 내가 쓴 말씀 직접 입력 (후원자 전용: 개역개정·영어 등 어떤 본문이든)
    var cu = $('vsCust');
    if (cu) {
      if (isDonor()) {
        cu.innerHTML = '<p class="vs-note" style="margin-top:0">원하는 번역(개역개정, 새번역, 영어 등)이나 직접 쓴 문장을 붙여넣으세요. 번역본의 저작권과 사용 허락은 사용하시는 분이 확인해 주세요.</p>' +
          '<label for="vsCText">말씀 본문</label><textarea id="vsCText" maxlength="600" placeholder="여기에 말씀을 붙여넣거나 입력하세요"></textarea>' +
          '<label for="vsCRef" style="margin-top:8px">출처 (예: 요한복음 3:16 · 개역개정)</label><input type="text" id="vsCRef" maxlength="60" placeholder="비워 두면 출처 줄이 표시되지 않아요">' +
          '<div class="vs-act" style="margin-top:10px"><button type="button" id="vsCApply">카드에 적용</button></div>';
        $('vsCApply').addEventListener('click', function () {
          var t = $('vsCText').value.replace(/\s*\n\s*/g, ' ').trim(); if (!t) return;
          var r = $('vsCRef').value.trim(); S.showRef = true;
          api.setVerse({ ref: r, text: t, topic: '' }); track('studio_custom_text', { len: t.length });
        });
      } else {
        cu.innerHTML = '<div class="vs-lock">🔒 후원하시면 개역개정·새번역·영어 등 <b>원하는 본문을 직접 붙여넣어</b> 카드로 만들 수 있어요. 후원 이용권을 사용하시는 동안 열립니다.<br><a href="/support.html" data-ga="studio_custom_to_support">후원 안내 보기 →</a></div>';
      }
    }

    // 교회·모임용 묶음 인쇄 (현재 디자인으로 여러 구절을 A4에 모아 인쇄)
    var LAY = [
      { k: 'a8', n: '8장 (2×4 · 100×70mm)', c: 2, r: 4, w: 100, h: 70 },
      { k: 'a6', n: '6장 (2×3 · 100×90mm)', c: 2, r: 3, w: 100, h: 90 },
      { k: 'a4', n: '4장 (2×2 · 100×135mm)', c: 2, r: 2, w: 100, h: 135 },
      { k: 'a10', n: '10장 (2×5 · 100×55mm)', c: 2, r: 5, w: 100, h: 55 },
      { k: 'a12', n: '12장 (3×4 · 66×70mm)', c: 3, r: 4, w: 66, h: 70 }
    ], bsel = $('vsBSet'), blay = $('vsBLay'), bcp = $('vsBCopies'), binfo = $('vsBInfo'), bprev = $('vsBPrev'), bgo = $('vsBGo'), bpr = $('vsBPrint'), bpages = null;
    if (bsel && blay) {
      var SETS = window.__SETS || [];
      SETS.forEach(function (st, i) { var o = document.createElement('option'); o.value = i; o.textContent = st.n + ' (' + st.v.length + '장)'; bsel.appendChild(o); });
      var oc = document.createElement('option'); oc.value = 'c'; oc.textContent = '✍️ 내가 붙여넣은 구절 (후원 기능)'; bsel.appendChild(oc);
      LAY.forEach(function (l, i) { var o = document.createElement('option'); o.value = i; o.textContent = l.n; blay.appendChild(o); });
      function curSet() {
        if (bsel.value !== 'c') return SETS[bsel.value];
        var v = [];
        ($('vsBCustText').value || '').split(/\n/).forEach(function (ln) {
          ln = ln.trim(); if (!ln) return; var p = ln.split('|'), t = p[0].trim(), r = (p.slice(1).join('|') || '').trim();
          if (t) v.push({ text: t, ref: r });
        });
        return { k: 'custom', n: '내 구절', v: v };
      }
      function cmode() {
        var c = bsel.value === 'c', d = isDonor(); $('vsBCustWrap').style.display = c ? 'block' : 'none';
        $('vsBLock').style.display = c && !d ? 'block' : 'none'; $('vsBCustBox').style.display = c && d ? 'block' : 'none';
        bgo.disabled = c && !d;
      }
      var bsum = function () { cmode(); var st = curSet(), l = LAY[blay.value]; if (!st) return;
        if (!st.v.length) { binfo.textContent = bsel.value === 'c' ? (isDonor() ? '구절을 붙여넣으면 장수가 계산돼요.' : '') : ''; bpr.disabled = true; bprev.innerHTML = ''; bpages = null; return; } var n = st.v.length * (+bcp.value), per = l.c * l.r; binfo.textContent = '총 ' + n + '장 · A4 ' + Math.ceil(n / per) + '쪽이에요. 같은 구절이 겹치지 않게 섞어서 상자에 담으세요.'; bpr.disabled = true; bprev.innerHTML = ''; bpages = null; };
      [bsel, blay, bcp].forEach(function (e) { e.addEventListener('change', bsum); }); $('vsBCustText').addEventListener('input', bsum); bsum();
      bgo.addEventListener('click', function () {
        var st = curSet(), l = LAY[blay.value], copies = +bcp.value, cut = $('vsBCut').checked, list = [];
        if (!st || !st.v.length || (bsel.value === 'c' && !isDonor())) return;
        st.v.forEach(function (v) { for (var i = 0; i < copies; i++) list.push(v); });
        bgo.disabled = true; bpr.disabled = true; bprev.innerHTML = ''; var urls = [], sv = S.verse, k = 0, cvs = document.createElement('canvas');
        loadFont(S.font).then(function step() {
          if (k >= list.length) { S.verse = sv; bgo.disabled = false; bgo.textContent = '🖨️ 다시 만들기'; bpages = { urls: urls, l: l, cut: cut }; bpr.disabled = false; binfo.textContent = '미리보기 ' + Math.min(4, urls.length) + '장 · 총 ' + urls.length + '장 준비됐어요. "인쇄하기"를 누르세요.'; track('studio_batch_ready', { set: st.k, n: urls.length, layout: l.k }); return; }
          binfo.textContent = '카드 만드는 중… ' + (k + 1) + ' / ' + list.length;
          S.verse = list[k]; render(cvs, Math.round(l.w * 12), Math.round(l.h * 12), true);
          return new Promise(function (res) { cvs.toBlob(function (b) { var u = URL.createObjectURL(b); urls.push(u); if (k < 4) { var im = new Image(); im.src = u; bprev.appendChild(im); } k++; setTimeout(res, 0); }, 'image/jpeg', 0.9); }).then(step);
        });
      });
      bpr.addEventListener('click', function () {
        if (!bpages) return; var u = bpages.urls, l = bpages.l, per = l.c * l.r, html = '', pg = 0;
        for (var i = 0; i < u.length; i += per) {
          html += '<div class="pg">'; u.slice(i, i + per).forEach(function (x) { html += '<img src="' + x + '">'; }); html += '</div>';
        }
        var css = '@page{size:A4 portrait;margin:0}html,body{margin:0}.pg{width:210mm;height:297mm;display:grid;grid-template-columns:repeat(' + l.c + ',' + l.w + 'mm);grid-template-rows:repeat(' + l.r + ',' + l.h + 'mm);justify-content:center;align-content:center;page-break-after:always;break-after:page}.pg:last-child{page-break-after:auto;break-after:auto}img{width:' + l.w + 'mm;height:' + l.h + 'mm;display:block;box-sizing:border-box;' + (bpages.cut ? 'outline:0.2mm dashed #9aa;outline-offset:-0.1mm;' : '') + '}';
        var fr = document.createElement('iframe'); fr.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0';
        fr.srcdoc = '<!doctype html><html><head><meta charset="utf-8"><style>' + css + '</style></head><body>' + html + '</body></html>';
        document.body.appendChild(fr);
        fr.onload = function () { setTimeout(function () { try { fr.contentWindow.focus(); fr.contentWindow.print(); } catch (e) {} setTimeout(function () { fr.remove(); }, 120000); }, 600); };
        track('studio_batch_print', { n: u.length, layout: l.k });
      });
    }
  }

  /* 디자인 지정(갤러리 카드 → 같은 디자인으로 열기, 샘플 카드 자동 생성에 쓴다) */
  var PHJ = null;
  function phMeta() { return PHJ ? Promise.resolve(PHJ) : fetch('/verse/studio_photos.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) { PHJ = d; return d; }); }
  function applyDesign(o) {
    var ps = [];
    if (o.font) S.font = o.font;
    ['orn', 'frame', 'fx', 'dcolor', 'tcolor', 'align', 'box', 'shadow', 'showRef'].forEach(function (k) { if (o[k] !== undefined) S[k] = o[k]; });
    if (o.dim !== undefined) S.dim = o.dim;
    if (o.scale !== undefined) S.scale = o.scale;
    if (o.bg) {
      if (o.bg.type === 'photo') {
        ps.push(phMeta().then(function (d) {
          var p = d.photos.filter(function (q) { return q.id === o.bg.id; })[0]; if (!p) return;
          return new Promise(function (res) { var im = new Image(); im.onload = function () { S.pimg = im; S.pcredit = '사진: ' + p.artist + ' · ' + p.lic + ' · Wikimedia Commons'; S.bg = { type: 'photo', id: p.id }; res(); }; im.onerror = res; im.src = '/images/studio/' + p.id + '.jpg'; });
        }));
      } else S.bg = o.bg;
    }
    return Promise.all(ps);
  }
  /* 뽑는 순간 완성된 카드를 보여 주기: 갤러리와 같은 추천 디자인(__RECIPES)을 무작위로 적용하고, 같은 말씀의 다른 디자인 미리보기를 보여 준다 */
  var RECIPES = window.__RECIPES || [], touched = false, stripTok = 0, syncUI = function () {};
  function rnd(n) { return (Math.random() * n) | 0; }
  var BASE = { tcolor: 'auto', box: false, align: 'center', scale: 1, showRef: true, shadow: true };
  function withBase(r) { var o = {}, k; for (k in BASE) o[k] = BASE[k]; for (k in r) o[k] = r[k]; return o; }
  function applyRandom() { if (!RECIPES.length) return Promise.resolve(); return applyDesign(withBase(RECIPES[rnd(RECIPES.length)])); }
  function deepLink() {
    var q = [], b = S.bg;
    q.push('v=' + encodeURIComponent(S.verse ? S.verse.ref : ''));
    if (b.type === 'photo') q.push('b=' + encodeURIComponent('photo:' + b.id)); else if (b.type === 'scene') q.push('b=' + encodeURIComponent('scene:' + b.k + ':' + (b.seed || 7)));
    q.push('f=' + encodeURIComponent(S.font)); if (S.orn !== 'none') q.push('o=' + S.orn); if (S.frame !== 'none') q.push('fr=' + S.frame); if (S.fx !== 'none') q.push('fx=' + S.fx); q.push('dm=' + S.dim);
    return location.origin + '/verse/?' + q.join('&');
  }
  function buildStrip() {
    var el = $('vsStrip'); if (!el || !RECIPES.length || !S.verse) return;
    var tok = ++stripTok, p = preset(), tw = 240, th = Math.round(240 * p.h / p.w), picks = [], used = {};
    el.innerHTML = '';
    for (var n = 0; n < 60 && picks.length < 6; n++) { var r = RECIPES[rnd(RECIPES.length)], key = JSON.stringify(r.bg); if (used[key]) continue; used[key] = 1; picks.push(r); }
    var btns = picks.map(function (r) { var b = document.createElement('button'); b.type = 'button'; b.className = 'vs-sth ld'; b.title = '이 디자인으로 바꾸기'; b.style.paddingBottom = (p.h / p.w * 100).toFixed(2) + '%'; el.appendChild(b); return b; });
    picks.reduce(function (pr, r, i) {
      return pr.then(function () {
        if (tok !== stripTok) return;
        return api.renderCard(Object.assign(withBase(r), { verse: S.verse, w: tw, h: th, thumb: true, type: 'image/jpeg', q: 0.8, mark: false })).then(function (url) {
          if (tok !== stripTok) return; var im = new Image(); im.alt = '다른 디자인 미리보기'; im.src = url; btns[i].appendChild(im); btns[i].classList.remove('ld');
          btns[i].onclick = function () { touched = true; applyDesign(withBase(r)).then(function () { syncUI(); refresh(); track('studio_strip_pick'); }); };
        }).catch(function () { btns[i].classList.remove('ld'); });
      });
    }, Promise.resolve());
  }
  var api = {
    setVerse: function (d, o) {
      S.verse = d; root.style.display = 'block';
      var pr = (o && o.random && !touched) ? applyRandom() : Promise.resolve();
      pr.then(function () { syncUI(); refresh(); buildStrip(); });
    },
    applyDesign: applyDesign,
    renderCard: function (o) {
      // 상태(S)를 건드리지 않고 사진·글꼴을 먼저 불러온 뒤, 한 번에(동기) 그려서 화면의 메인 카드와 겹치지 않게 한다.
      var f = o.font || S.font, v = o.verse || S.verse || { text: '', ref: '' };
      var pp = (o.bg && o.bg.type === 'photo') ? phMeta().then(function (d) {
        var p = d.photos.filter(function (q) { return q.id === o.bg.id; })[0]; if (!p) return null;
        return new Promise(function (res) { var im = new Image(); im.onload = function () { res({ im: im, p: p }); }; im.onerror = function () { res(null); }; im.src = '/images/studio/' + p.id + (o.thumb ? '_t' : '') + '.jpg'; });
      }) : Promise.resolve(null);
      return Promise.all([pp, loadFont(f, (v.text || '') + (v.ref || ''))]).then(function (r) {
        var keys = ['verse', 'bg', 'font', 'orn', 'frame', 'fx', 'dcolor', 'dim', 'tcolor', 'align', 'scale', 'showRef', 'box', 'shadow', 'mark', 'pimg', 'pcredit'], keep = {};
        keys.forEach(function (k) { keep[k] = S[k]; });
        S.verse = v; S.mark = o.mark !== false; S.font = f;
        ['orn', 'frame', 'fx', 'dcolor', 'tcolor', 'align', 'box', 'shadow', 'showRef', 'dim', 'scale'].forEach(function (k) { if (o[k] !== undefined) S[k] = o[k]; });
        if (o.bg) { if (o.bg.type === 'photo') { if (r[0]) { S.pimg = r[0].im; S.pcredit = '사진: ' + r[0].p.artist + ' · ' + r[0].p.lic + ' · Wikimedia Commons'; S.bg = { type: 'photo', id: o.bg.id }; } } else S.bg = o.bg; }
        var c = document.createElement('canvas'), url;
        try { render(c, o.w, o.h, true); url = c.toDataURL(o.type || 'image/jpeg', o.q || 0.86); } finally { keys.forEach(function (k) { S[k] = keep[k]; }); }
        return url;
      });
    },
    state: S
  };
  window.crsStudio = api;
  build();
  refresh();
  (function () {
    var m = /[?&]v=([^&#]+)/.exec(location.search); if (!m) return;
    var ref = decodeURIComponent(m[1]).replace(/\+/g, ' ').trim(), hit = null;
    (window.__SETS || []).forEach(function (st) { st.v.forEach(function (v) { if (!hit && v.ref === ref) hit = v; }); });
    (window.__VERSES || []).forEach(function (v) { if (!hit && v.ref === ref) hit = v; });
    if (hit) {
      var q = function (k) { var mm = new RegExp('[?&]' + k + '=([^&#]+)').exec(location.search); return mm ? decodeURIComponent(mm[1].replace(/\+/g, ' ')) : null; }, d = {}, b = q('b');
      if (b) { var bp = b.split(':'); if (bp[0] === 'photo') d.bg = { type: 'photo', id: bp[1] }; else if (bp[0] === 'scene') d.bg = { type: 'scene', k: bp[1], seed: +bp[2] || 7 }; }
      if (q('f')) d.font = q('f'); if (q('o')) d.orn = q('o'); if (q('fr')) d.frame = q('fr'); if (q('fx')) d.fx = q('fx'); if (q('dm')) d.dim = +q('dm'); if (q('dc')) d.dcolor = q('dc');
      applyDesign(d).then(function () { refresh(); });
    }
    if (hit) { api.setVerse({ ref: hit.ref, text: hit.text, topic: hit.topic || '' }); setTimeout(function () { var e = document.getElementById('vstudio'); if (e) e.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 700); }
  })();
  if (location.hash === '#church-print' && window.__VERSES && window.__VERSES.length) {
    api.setVerse(window.__VERSES[(Math.random() * window.__VERSES.length) | 0]);
    setTimeout(function () { var e = document.getElementById('church-print'); if (e) e.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 900);
  }
})();
