/* 말씀 카드 장식: 십자가로세로가 직접 그린 도안(저작권 걱정 없음). 장식(orn)·테두리(frame)·분위기 효과(fx) */
(function () {
  'use strict';
  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  var ORN = [
    { k: 'none', n: '없음' }, { k: 'cross', n: '십자가' }, { k: 'dove', n: '비둘기' }, { k: 'olive', n: '올리브 가지' },
    { k: 'wheat', n: '밀 이삭' }, { k: 'lily', n: '백합' }, { k: 'star', n: '베들레헴 별' }, { k: 'fish', n: '물고기' },
    { k: 'grapes', n: '포도' }, { k: 'flame', n: '성령의 불꽃' }, { k: 'anchor', n: '닻' }, { k: 'heart', n: '사랑' }
  ];
  var FRAMES = [
    { k: 'none', n: '없음' }, { k: 'line', n: '가는 선' }, { k: 'double', n: '이중 선' }, { k: 'round', n: '둥근 선' },
    { k: 'corner', n: '모서리 장식' }, { k: 'mat', n: '흰 테두리' }
  ];
  var FX = [
    { k: 'none', n: '없음' }, { k: 'rays', n: '빛 내림' }, { k: 'sparkle', n: '반짝임' }, { k: 'bokeh', n: '빛망울' },
    { k: 'vignette', n: '가장자리 어둡게' }, { k: 'snow', n: '눈송이' }, { k: 'petals', n: '꽃잎' }
  ];

  function ell(x, cx, cy, rx, ry, rot) { x.beginPath(); x.ellipse(cx, cy, rx, ry, rot || 0, 0, 7); x.fill(); }

  var DRAW = {
    cross: function (x) {
      x.beginPath(); x.moveTo(-7, -46); x.lineTo(7, -46); x.lineTo(7, -24); x.lineTo(28, -24); x.lineTo(28, -10); x.lineTo(7, -10); x.lineTo(7, 46); x.lineTo(-7, 46); x.lineTo(-7, -10); x.lineTo(-28, -10); x.lineTo(-28, -24); x.lineTo(-7, -24); x.closePath(); x.fill();
      x.save(); x.globalAlpha *= 0.35; x.lineWidth = 1.6; x.strokeStyle = '#000'; x.beginPath(); x.moveTo(0, -38); x.lineTo(0, 38); x.moveTo(-20, -17); x.lineTo(20, -17); x.stroke(); x.restore();
    },
    dove: function (x) {
      ell(x, 0, 8, 27, 11, -0.28);
      x.beginPath(); x.arc(25, -3, 7.5, 0, 7); x.fill();
      x.beginPath(); x.moveTo(31, -6); x.lineTo(42, -2); x.lineTo(31, 0); x.closePath(); x.fill();
      x.beginPath(); x.moveTo(-20, 11); x.quadraticCurveTo(-40, 12, -50, 28); x.quadraticCurveTo(-34, 28, -24, 19); x.closePath(); x.fill();
      x.beginPath(); x.moveTo(-6, 3); x.bezierCurveTo(-16, -30, 8, -50, 36, -46); x.bezierCurveTo(26, -36, 20, -24, 14, -8); x.closePath(); x.fill();
      x.save(); x.globalAlpha *= 0.55; x.beginPath(); x.moveTo(-10, 8); x.bezierCurveTo(-30, -14, -22, -34, -4, -42); x.bezierCurveTo(-8, -28, -4, -14, 4, 2); x.closePath(); x.fill(); x.restore();
    },
    olive: function (x) {
      var P = function (t) { var u = 1 - t; return [u * u * -46 + 2 * u * t * 0 + t * t * 46, u * u * 14 + 2 * u * t * 26 + t * t * -12]; };
      x.lineWidth = 2.6; x.lineCap = 'round'; x.beginPath(); x.moveTo(-46, 14); x.quadraticCurveTo(0, 26, 46, -12); x.stroke();
      for (var i = 1; i <= 9; i++) {
        var t = i / 10, p = P(t), q = P(t + 0.01), ang = Math.atan2(q[1] - p[1], q[0] - p[0]);
        ell(x, p[0] + Math.cos(ang - 1.1) * 8, p[1] + Math.sin(ang - 1.1) * 8, 9.5, 3.4, ang - 0.75);
        ell(x, p[0] + Math.cos(ang + 1.1) * 8, p[1] + Math.sin(ang + 1.1) * 8, 9.5, 3.4, ang + 0.75);
      }
      var e = P(1); ell(x, e[0] + 7, e[1] - 3, 9.5, 3.4, -0.5);
      x.save(); x.globalAlpha *= 0.7; [0.28, 0.52, 0.74].forEach(function (t, j) { var p = P(t); ell(x, p[0] + (j % 2 ? -3 : 3), p[1] + 11 + (j % 2) * 2, 4, 5.4, 0.3); }); x.restore();
    },
    wheat: function (x) {
      x.lineWidth = 2.6; x.lineCap = 'round'; x.beginPath(); x.moveTo(0, 48); x.quadraticCurveTo(-3, 10, 0, -30); x.stroke();
      for (var i = 0; i < 6; i++) { var y = -40 + i * 11; ell(x, -7.5, y + 4, 4.2, 9.5, 0.55); ell(x, 7.5, y + 4, 4.2, 9.5, -0.55); }
      ell(x, 0, -48, 4, 9, 0);
      x.beginPath(); x.moveTo(-1, 36); x.quadraticCurveTo(-22, 26, -30, 4); x.quadraticCurveTo(-14, 12, -1, 30); x.fill();
      x.beginPath(); x.moveTo(1, 28); x.quadraticCurveTo(20, 20, 27, 2); x.quadraticCurveTo(12, 8, 1, 22); x.fill();
    },
    lily: function (x) {
      x.lineWidth = 2.6; x.lineCap = 'round'; x.beginPath(); x.moveTo(0, 48); x.quadraticCurveTo(2, 38, 0, 26); x.stroke();
      [[-34, 0.9], [34, 0.9], [0, 1]].forEach(function (a) {
        x.save(); x.translate(0, 28); x.rotate(a[0] * Math.PI / 180); x.scale(a[1], a[1]);
        x.beginPath(); x.moveTo(0, 0); x.bezierCurveTo(-19, -26, -11, -54, 0, -70); x.bezierCurveTo(11, -54, 19, -26, 0, 0); x.fill(); x.restore();
      });
      x.save(); x.globalAlpha *= 0.35; x.strokeStyle = '#000'; x.lineWidth = 1.4; x.beginPath(); x.moveTo(0, 22); x.lineTo(0, -34); x.stroke(); x.restore();
      x.beginPath(); x.moveTo(1, 44); x.quadraticCurveTo(18, 40, 26, 24); x.quadraticCurveTo(12, 28, 1, 38); x.fill();
    },
    star: function (x) {
      x.beginPath();
      for (var i = 0; i < 8; i++) { var a = -Math.PI / 2 + i * Math.PI / 4, r = i % 2 === 0 ? (i % 4 === 0 ? 46 : 30) : 8; x.lineTo(Math.cos(a) * r, Math.sin(a) * r * (i % 4 === 0 && i === 0 || i === 4 ? 1 : 1)); }
      x.closePath(); x.fill();
      x.save(); x.globalAlpha *= 0.35; for (var k = 0; k < 4; k++) { var b = Math.PI / 4 + k * Math.PI / 2; x.lineWidth = 1.8; x.strokeStyle = x.fillStyle; x.beginPath(); x.moveTo(Math.cos(b) * 13, Math.sin(b) * 13); x.lineTo(Math.cos(b) * 24, Math.sin(b) * 24); x.stroke(); } x.restore();
    },
    fish: function (x) {
      x.lineWidth = 4.4; x.lineCap = 'round'; x.lineJoin = 'round';
      x.beginPath(); x.moveTo(-46, 0); x.quadraticCurveTo(-4, -40, 30, 12); x.stroke();
      x.beginPath(); x.moveTo(-46, 0); x.quadraticCurveTo(-4, 40, 30, -12); x.stroke();
      x.beginPath(); x.moveTo(24, 0); x.lineTo(46, -15); x.moveTo(24, 0); x.lineTo(46, 15); x.moveTo(46, -15); x.quadraticCurveTo(40, 0, 46, 15); x.stroke();
      x.beginPath(); x.arc(-30, -2, 2.6, 0, 7); x.fill();
    },
    grapes: function (x) {
      var pts = [[-15, -6], [0, -8], [15, -6], [-8, 7], [8, 7], [0, 21], [-22, 6], [22, 6], [-15, 19], [15, 19], [0, 35]];
      pts.forEach(function (p) { x.beginPath(); x.arc(p[0], p[1], 8.4, 0, 7); x.fill(); });
      x.save(); x.globalAlpha *= 0.3; x.fillStyle = '#fff'; pts.forEach(function (p) { x.beginPath(); x.arc(p[0] - 2.6, p[1] - 2.8, 2.4, 0, 7); x.fill(); }); x.restore();
      x.lineWidth = 3; x.lineCap = 'round'; x.beginPath(); x.moveTo(0, -14); x.quadraticCurveTo(2, -30, 8, -40); x.stroke();
      x.beginPath(); x.moveTo(5, -30); x.bezierCurveTo(14, -52, 36, -44, 40, -26); x.bezierCurveTo(26, -32, 16, -26, 5, -30); x.fill();
    },
    flame: function (x) {
      x.beginPath(); x.moveTo(0, -48); x.bezierCurveTo(12, -26, 30, -8, 24, 16); x.bezierCurveTo(20, 36, -20, 36, -24, 16); x.bezierCurveTo(-28, 0, -10, -12, 0, -48); x.closePath(); x.fill();
      x.save(); x.globalCompositeOperation = 'destination-out'; x.globalAlpha = 0.55; x.beginPath(); x.moveTo(0, -8); x.bezierCurveTo(8, 6, 14, 14, 9, 24); x.bezierCurveTo(5, 32, -10, 30, -10, 22); x.bezierCurveTo(-11, 14, -3, 6, 0, -8); x.closePath(); x.fill(); x.restore();
    },
    anchor: function (x) {
      x.lineWidth = 5; x.lineCap = 'round'; x.lineJoin = 'round';
      x.beginPath(); x.arc(0, -36, 7, 0, 7); x.stroke();
      x.beginPath(); x.moveTo(0, -29); x.lineTo(0, 38); x.moveTo(-15, -18); x.lineTo(15, -18); x.stroke();
      x.beginPath(); x.arc(0, 6, 33, 0.14 * Math.PI, 0.86 * Math.PI); x.stroke();
      x.beginPath(); x.moveTo(-31, 12); x.lineTo(-36, 0); x.moveTo(-31, 12); x.lineTo(-20, 8); x.moveTo(31, 12); x.lineTo(36, 0); x.moveTo(31, 12); x.lineTo(20, 8); x.stroke();
    },
    heart: function (x) {
      x.beginPath(); x.moveTo(0, 34); x.bezierCurveTo(-52, -2, -30, -44, 0, -18); x.bezierCurveTo(30, -44, 52, -2, 0, 34); x.closePath(); x.fill();
      x.save(); x.globalCompositeOperation = 'destination-out'; x.beginPath(); x.rect(-2.8, -12, 5.6, 36); x.rect(-11, -3, 22, 5.6); x.fill(); x.restore();
    }
  };

  /* 장식 하나를 (cx,cy) 중심, 크기 size(px)로 그린다 */
  function orn(x, cx, cy, size, k, color) {
    if (!DRAW[k]) return;
    var tmp = document.createElement('canvas'); var n = Math.ceil(size * 1.3); tmp.width = n; tmp.height = n;
    var t = tmp.getContext('2d'); t.translate(n / 2, n / 2); var sc = size / 100; t.scale(sc, sc);
    t.fillStyle = color; t.strokeStyle = color; DRAW[k](t);
    x.save(); x.globalAlpha = 0.95; x.drawImage(tmp, cx - n / 2, cy - n / 2); x.restore();
  }

  function frame(x, w, h, k, color) {
    var m = Math.min(w, h);
    x.save(); x.strokeStyle = color; x.fillStyle = color; x.lineJoin = 'round'; x.lineCap = 'round';
    if (k === 'line') { x.lineWidth = m * 0.004; x.globalAlpha = 0.85; var p = m * 0.045; x.strokeRect(p, p, w - p * 2, h - p * 2); }
    else if (k === 'double') { x.globalAlpha = 0.85; var p1 = m * 0.04, p2 = m * 0.056; x.lineWidth = m * 0.006; x.strokeRect(p1, p1, w - p1 * 2, h - p1 * 2); x.lineWidth = m * 0.0028; x.strokeRect(p2, p2, w - p2 * 2, h - p2 * 2); }
    else if (k === 'round') { x.lineWidth = m * 0.004; x.globalAlpha = 0.85; var p3 = m * 0.045, r = m * 0.07; x.beginPath(); x.moveTo(p3 + r, p3); x.arcTo(w - p3, p3, w - p3, h - p3, r); x.arcTo(w - p3, h - p3, p3, h - p3, r); x.arcTo(p3, h - p3, p3, p3, r); x.arcTo(p3, p3, w - p3, p3, r); x.closePath(); x.stroke(); }
    else if (k === 'corner') {
      x.globalAlpha = 0.9; x.lineWidth = m * 0.005; var q = m * 0.05, L = m * 0.14;
      [[0, 0, 1, 1], [w, 0, -1, 1], [0, h, 1, -1], [w, h, -1, -1]].forEach(function (c) {
        var ox = c[0] + c[2] * q, oy = c[1] + c[3] * q;
        x.beginPath(); x.moveTo(ox + c[2] * L, oy); x.lineTo(ox, oy); x.lineTo(ox, oy + c[3] * L); x.stroke();
        x.beginPath(); x.arc(ox + c[2] * m * 0.022, oy + c[3] * m * 0.022, m * 0.008, 0, 7); x.fill();
        x.lineWidth = m * 0.0025; x.beginPath(); x.moveTo(ox + c[2] * L * 0.55, oy + c[3] * m * 0.014); x.lineTo(ox + c[2] * L * 0.85, oy + c[3] * m * 0.014); x.moveTo(ox + c[2] * m * 0.014, oy + c[3] * L * 0.55); x.lineTo(ox + c[2] * m * 0.014, oy + c[3] * L * 0.85); x.stroke(); x.lineWidth = m * 0.005;
      });
    }
    else if (k === 'mat') {
      var b = m * 0.045; x.fillStyle = '#fbf8f1'; x.beginPath(); x.rect(0, 0, w, b); x.rect(0, h - b * 1.9, w, b * 1.9); x.rect(0, b, b, h - b * 2.9); x.rect(w - b, b, b, h - b * 2.9); x.fill();
    }
    x.restore();
  }

  function fx(x, w, h, k) {
    var m = Math.min(w, h), R = rng(4217);
    x.save();
    if (k === 'rays') {
      var ox = w * 0.82, oy = -h * 0.06;
      for (var i = 0; i < 7; i++) {
        var a = 1.78 + i * 0.13 + R() * 0.05, sp = 0.025 + R() * 0.035, len = Math.max(w, h) * 1.5;
        var g = x.createLinearGradient(ox, oy, ox + Math.cos(a) * len, oy + Math.sin(a) * len); g.addColorStop(0, 'rgba(255,248,225,' + (0.2 + R() * 0.12) + ')'); g.addColorStop(1, 'rgba(255,248,225,0)');
        x.fillStyle = g; x.beginPath(); x.moveTo(ox, oy); x.lineTo(ox + Math.cos(a - sp) * len, oy + Math.sin(a - sp) * len); x.lineTo(ox + Math.cos(a + sp) * len, oy + Math.sin(a + sp) * len); x.closePath(); x.fill();
      }
      var gl = x.createRadialGradient(ox, oy, 0, ox, oy, m * 0.7); gl.addColorStop(0, 'rgba(255,248,225,0.45)'); gl.addColorStop(1, 'rgba(255,248,225,0)'); x.fillStyle = gl; x.fillRect(0, 0, w, h);
    }
    else if (k === 'sparkle') {
      for (var j = 0; j < 46; j++) {
        var sx = R() * w, sy = R() * h, s = m * (0.004 + R() * R() * 0.016); x.globalAlpha = 0.45 + R() * 0.5; x.fillStyle = '#fff';
        x.beginPath(); x.moveTo(sx, sy - s * 2.4); x.quadraticCurveTo(sx, sy, sx + s * 2.4, sy); x.quadraticCurveTo(sx, sy, sx, sy + s * 2.4); x.quadraticCurveTo(sx, sy, sx - s * 2.4, sy); x.quadraticCurveTo(sx, sy, sx, sy - s * 2.4); x.fill();
      }
    }
    else if (k === 'bokeh') {
      for (var b = 0; b < 20; b++) { var bx = R() * w, by = R() * h, br = m * (0.02 + R() * 0.06); x.globalAlpha = 0.07 + R() * 0.13; x.fillStyle = '#fff6dc'; x.beginPath(); x.arc(bx, by, br, 0, 7); x.fill(); x.globalAlpha = 0.2; x.strokeStyle = '#fff'; x.lineWidth = m * 0.0014; x.stroke(); }
    }
    else if (k === 'vignette') {
      var v = x.createRadialGradient(w / 2, h / 2, m * 0.25, w / 2, h / 2, Math.max(w, h) * 0.75); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.5)'); x.fillStyle = v; x.fillRect(0, 0, w, h);
    }
    else if (k === 'snow') {
      x.fillStyle = '#fff'; for (var s2 = 0; s2 < 110; s2++) { x.globalAlpha = 0.35 + R() * 0.55; x.beginPath(); x.arc(R() * w, R() * h, m * (0.002 + R() * R() * 0.007), 0, 7); x.fill(); }
    }
    else if (k === 'petals') {
      for (var p = 0; p < 30; p++) { var pr = m * (0.008 + R() * 0.012); x.globalAlpha = 0.55 + R() * 0.4; x.fillStyle = R() < 0.5 ? '#ffd6e0' : '#fff0f3'; x.beginPath(); x.ellipse(R() * w, R() * h, pr * 1.7, pr, R() * 3.14, 0, 7); x.fill(); }
    }
    x.restore();
  }

  window.crsDeco = { ORN: ORN, FRAMES: FRAMES, FX: FX, orn: orn, frame: frame, fx: fx };
})();
