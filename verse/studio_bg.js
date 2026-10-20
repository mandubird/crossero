/* 말씀 카드 고급 질감 배경 12종(직접 그린 도안, 저작권 걱정 없음). 노이즈 기반으로 어떤 크기에서도 선명하게 그려진다.
   window.crsBgScenes = { list:[{k,n,light}], draw:{ k: function(x,w,h,R,s) } } */
(function () {
  'use strict';
  function hs(i, j, s) { var n = (i * 374761393 + j * 668265263 + s * 1274126177) | 0; n = (n ^ (n >>> 13)) * 1274126177 | 0; return ((n ^ (n >>> 16)) >>> 0) / 4294967296; }
  function sm(t) { return t * t * (3 - 2 * t); }
  function vn(x, y, s) { var i = Math.floor(x), j = Math.floor(y), fx = sm(x - i), fy = sm(y - j); var a = hs(i, j, s), b = hs(i + 1, j, s), c = hs(i, j + 1, s), d = hs(i + 1, j + 1, s); return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy; }
  function fbm(x, y, s, o) { var v = 0, a = 0.5, f = 1, t = 0; for (var k = 0; k < (o || 4); k++) { v += a * vn(x * f, y * f, s + k * 17); t += a; a *= 0.5; f *= 2; } return v / t; }
  function field(x, w, h, rw, fn) {
    var rh = Math.max(2, Math.round(rw * h / w)), c = document.createElement('canvas'); c.width = rw; c.height = rh;
    var cx = c.getContext('2d'), im = cx.createImageData(rw, rh), d = im.data;
    for (var j = 0; j < rh; j++) for (var i = 0; i < rw; i++) { var p = fn(i / rw, j / rh, i, j), o = (j * rw + i) * 4; d[o] = p[0]; d[o + 1] = p[1]; d[o + 2] = p[2]; d[o + 3] = p.length > 3 ? p[3] : 255; }
    cx.putImageData(im, 0, 0); x.save(); x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high'; x.drawImage(c, 0, 0, w, h); x.restore();
  }
  function lin(x, w, h, stops, x0, y0, x1, y1) { var g = x.createLinearGradient(x0 * w, y0 * h, x1 * w, y1 * h); stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); x.fillStyle = g; x.fillRect(0, 0, w, h); }
  function rad(x, cx, cy, r, c0, c1) { var g = x.createRadialGradient(cx, cy, 0, cx, cy, r); g.addColorStop(0, c0); g.addColorStop(1, c1); x.fillStyle = g; x.fillRect(cx - r, cy - r, r * 2, r * 2); }
  function pick(R, a) { return a[(R() * a.length) | 0]; }
  function grain(x, w, h, s, amt, rw) { field(x, w, h, rw || 260, function (u, v) { var n = (fbm(u * 60, v * 60, s, 2) - 0.5) * amt; var a = Math.abs(n); return n > 0 ? [255, 255, 255, a * 255] : [60, 40, 20, a * 255]; }); }

  var DRAW = {
    /* 수채화 번짐 */
    wc: function (x, w, h, R, s) {
      var P = pick(R, [['#9ec9e8', '#f4b6c2', '#ffe3a8'], ['#a8d8c0', '#cfe6f5', '#f9d8b2'], ['#c7b6e8', '#f6c1d4', '#bfe0ef'], ['#f7c9a0', '#f3a6a0', '#fbe6b0']]);
      x.fillStyle = '#fbf7ef'; x.fillRect(0, 0, w, h);
      for (var i = 0; i < 9; i++) { var cx = R() * w, cy = R() * h, r = (0.28 + R() * 0.4) * Math.max(w, h) * 0.6, col = P[i % 3]; x.save(); x.globalAlpha = 0.34; x.globalCompositeOperation = 'multiply'; var g = x.createRadialGradient(cx, cy, r * 0.1, cx, cy, r); g.addColorStop(0, col); g.addColorStop(0.7, col + 'aa'); g.addColorStop(1, col + '00'); x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, r, r * (0.7 + R() * 0.4), R() * 3, 0, 7); x.fill(); x.restore(); }
      grain(x, w, h, s, 0.07, 220);
    },
    /* 수묵 산수 */
    ink: function (x, w, h, R, s) {
      field(x, w, h, 240, function (u, v) { var n = fbm(u * 8, v * 8, s, 4); var b = 238 + n * 12; return [b, b - 4, b - 14, 255]; });
      var sx = w * (0.62 + R() * 0.2), sy = h * (0.13 + R() * 0.05); x.fillStyle = 'rgba(190,60,45,0.85)'; x.beginPath(); x.arc(sx, sy, w * 0.055, 0, 7); x.fill();
      var layers = [[0.66, 0.13, 0.12, 0.5], [0.77, 0.1, 0.2, 0.68], [0.88, 0.08, 0.32, 0.85]];
      layers.forEach(function (L, li) {
        var base = h * L[0]; x.beginPath(); x.moveTo(0, h);
        for (var i = 0; i <= 60; i++) { var u = i / 60, ridge = Math.pow(fbm(u * 3 + li * 5, li * 3.1, s, 4), 1.3); x.lineTo(u * w, base - ridge * h * L[1] * 2.4); }
        x.lineTo(w, h); x.closePath(); var g = x.createLinearGradient(0, base - h * L[1], 0, h); var a = L[3]; g.addColorStop(0, 'rgba(40,44,48,' + a + ')'); g.addColorStop(1, 'rgba(120,124,128,' + a * 0.3 + ')'); x.fillStyle = g; x.fill();
        var mg = x.createLinearGradient(0, base - h * 0.04, 0, base + h * 0.1); mg.addColorStop(0, 'rgba(244,239,228,0)'); mg.addColorStop(0.5, 'rgba(244,239,228,0.85)'); mg.addColorStop(1, 'rgba(244,239,228,0)'); x.fillStyle = mg; x.fillRect(0, base - h * 0.04, w, h * 0.14);
      });
      grain(x, w, h, s + 3, 0.18, 280);
    },
    /* 한지 질감 */
    hanji: function (x, w, h, R, s) {
      field(x, w, h, 300, function (u, v) { var n = fbm(u * 10, v * 14, s, 4), f = fbm(u * 90, v * 5, s + 9, 2); var b = 244 + n * 10 - (f > 0.62 ? 7 : 0); return [b, b - 6, b - 20, 255]; });
      x.save(); x.lineCap = 'round'; for (var i = 0; i < Math.round(w * h / 9000); i++) { var px = R() * w, py = R() * h, len = 14 + R() * 60, an = R() * 3.14; x.strokeStyle = 'rgba(170,150,110,' + (0.05 + R() * 0.12) + ')'; x.lineWidth = 0.6 + R() * 1.4; x.beginPath(); x.moveTo(px, py); x.quadraticCurveTo(px + Math.cos(an) * len * 0.5 + R() * 8, py + Math.sin(an) * len * 0.5 + R() * 8, px + Math.cos(an) * len, py + Math.sin(an) * len); x.stroke(); } x.restore();
    },
    /* 대리석 */
    marble: function (x, w, h, R, s) {
      var tone = pick(R, [[247, 247, 249], [245, 241, 234], [236, 240, 244]]);
      field(x, w, h, 300, function (u, v) {
        var wx = fbm(u * 2.2, v * 2.2, s, 4), wy = fbm(u * 2.2 + 5, v * 2.2 + 9, s + 5, 4);
        var q = fbm(u * 3 + wx * 2.2, v * 3 + wy * 2.2, s + 2, 5);
        var vein = Math.pow(Math.max(0, 1 - Math.abs(q - 0.5) * 9), 3);
        var vein2 = Math.pow(Math.max(0, 1 - Math.abs(fbm(u * 5 + wy * 3, v * 5 + wx * 3, s + 8, 4) - 0.5) * 14), 4);
        var cloud = fbm(u * 3, v * 3, s + 11, 4);
        var b = 1 - cloud * 0.05 - vein * 0.2 - vein2 * 0.09;
        return [tone[0] * b, tone[1] * b, tone[2] * b, 255];
      });
    },
    /* 별빛과 금빛 */
    gold: function (x, w, h, R, s) {
      lin(x, w, h, [[0, '#070f26'], [0.5, '#13214a'], [1, '#1f2f62']], 0, 0, 0.4, 1);
      rad(x, w * (0.3 + R() * 0.4), h * 0.1, Math.max(w, h) * 0.7, 'rgba(255,214,120,0.38)', 'rgba(255,214,120,0)');
      rad(x, w * (0.2 + R() * 0.6), h * 0.9, Math.max(w, h) * 0.5, 'rgba(120,150,255,0.18)', 'rgba(120,150,255,0)');
      x.save(); x.lineWidth = Math.max(1.5, w * 0.0026); for (var k = 0; k < 5; k++) { x.strokeStyle = 'rgba(244,206,120,' + (0.22 + k * 0.07) + ')'; x.beginPath(); x.ellipse(w * (0.15 + k * 0.17), h * 1.08, w * (0.55 + k * 0.17), h * (0.6 + k * 0.1), -0.22 + k * 0.06, Math.PI * 1.08, Math.PI * 1.92); x.stroke(); } x.restore();
      var n = Math.max(110, Math.round(w * h / 2600)); for (var i = 0; i < n; i++) { var px = R() * w, py = R() * h, r = (0.7 + R() * R() * 2.8) * (w / 600 + 0.7), a = 0.3 + R() * 0.7; if (R() < 0.12) { var g = x.createRadialGradient(px, py, 0, px, py, r * 5); g.addColorStop(0, 'rgba(255,225,150,0.55)'); g.addColorStop(1, 'rgba(255,225,150,0)'); x.fillStyle = g; x.beginPath(); x.arc(px, py, r * 5, 0, 7); x.fill(); } x.fillStyle = 'rgba(' + (240 + (R() * 15 | 0)) + ',' + (196 + (R() * 30 | 0)) + ',' + (112 + (R() * 40 | 0)) + ',' + a + ')'; x.beginPath(); x.arc(px, py, r, 0, 7); x.fill(); }
    },
    /* 빛망울 야경 */
    bokeh: function (x, w, h, R, s) {
      var P = pick(R, [['#1a1030', '#3a1d4f'], ['#07202e', '#0f3b4a'], ['#241012', '#4b1f1a']]);
      lin(x, w, h, [[0, P[0]], [1, P[1]]], 0, 0, 0.3, 1);
      var C = ['255,214,140', '255,170,120', '255,240,200', '170,200,255', '255,150,170'];
      for (var i = 0; i < 26; i++) { var cx = R() * w, cy = R() * h, r = (0.03 + R() * R() * 0.12) * Math.min(w, h) * 1.5, c = pick(R, C); x.save(); x.globalCompositeOperation = 'lighter'; var g = x.createRadialGradient(cx, cy, r * 0.3, cx, cy, r); g.addColorStop(0, 'rgba(' + c + ',' + (0.14 + R() * 0.16) + ')'); g.addColorStop(0.85, 'rgba(' + c + ',' + (0.1 + R() * 0.1) + ')'); g.addColorStop(1, 'rgba(' + c + ',0)'); x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, 7); x.fill(); x.restore(); }
    },
    /* 리넨 질감 */
    linen: function (x, w, h, R, s) {
      field(x, w, h, 340, function (u, v, i, j) { var n = fbm(u * 12, v * 12, s, 3); var hz = (hs(i % 4, j, s) - 0.5) * 9, vt = (hs(i, j % 4, s + 3) - 0.5) * 9; var b = 226 + n * 14 + hz + vt; return [b, b - 8, b - 24, 255]; });
      var g = x.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.3, w / 2, h / 2, Math.max(w, h) * 0.75); g.addColorStop(0, 'rgba(255,250,240,0)'); g.addColorStop(1, 'rgba(120,95,60,0.22)'); x.fillStyle = g; x.fillRect(0, 0, w, h);
    },
    /* 새벽 노을 */
    dawn: function (x, w, h, R, s) {
      var P = pick(R, [['#2c2a5a', '#8a5a8c', '#f19a8a', '#ffd9a0'], ['#1f3a5f', '#6a7fb0', '#f3b6a0', '#ffe2b0'], ['#3a2a4f', '#b05f7c', '#f7a56a', '#ffe08a']]);
      lin(x, w, h, [[0, P[0]], [0.4, P[1]], [0.72, P[2]], [1, P[3]]], 0, 0, 0, 1);
      var sx = w * (0.3 + R() * 0.4), sy = h * 0.74; rad(x, sx, sy, Math.max(w, h) * 0.5, 'rgba(255,236,190,0.75)', 'rgba(255,236,190,0)');
      for (var i = 0; i < 9; i++) { var cy = h * (0.3 + R() * 0.5), cw = w * (0.35 + R() * 0.6), cx = R() * w; var g = x.createLinearGradient(0, cy - h * 0.03, 0, cy + h * 0.03); g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, 'rgba(255,240,230,' + (0.12 + R() * 0.22) + ')'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, cw / 2, h * 0.028, 0, 0, 7); x.fill(); }
      x.fillStyle = 'rgba(20,18,40,0.55)'; x.beginPath(); x.moveTo(0, h); for (var k = 0; k <= 40; k++) { var u = k / 40; x.lineTo(u * w, h * 0.92 - fbm(u * 4, 1.3, s, 4) * h * 0.1); } x.lineTo(w, h); x.fill();
    },
    /* 안개 숲 */
    mist: function (x, w, h, R, s) {
      lin(x, w, h, [[0, '#dfeee4'], [0.45, '#a9c9b4'], [1, '#4d7d66']], 0, 0, 0, 1);
      rad(x, w * (0.55 + R() * 0.3), h * 0.1, Math.max(w, h) * 0.7, 'rgba(255,250,215,0.65)', 'rgba(255,250,215,0)');
      for (var L = 0; L < 4; L++) {
        var base = h * (0.52 + L * 0.14), a = 0.28 + L * 0.2, sz = w * (0.07 + L * 0.03), cnt = Math.round(w / (sz * 0.55));
        x.fillStyle = 'rgba(' + (28 - L * 4) + ',' + (68 - L * 6) + ',' + (52 - L * 5) + ',' + a + ')';
        for (var i = 0; i < cnt; i++) { var cx = (i + R() * 0.8) * (w / cnt), th = sz * (1.6 + R() * 1.3), tw = sz * (0.34 + R() * 0.16), top = base - th; x.beginPath(); x.moveTo(cx, top); x.lineTo(cx + tw, base); x.lineTo(cx - tw, base); x.closePath(); x.fill(); x.fillRect(cx - tw * 0.1, base - 1, tw * 0.2, h - base + 2); }
        x.fillRect(0, base, w, h - base);
        var mg = x.createLinearGradient(0, base - h * 0.16, 0, base + h * 0.04); mg.addColorStop(0, 'rgba(238,246,240,0)'); mg.addColorStop(0.6, 'rgba(238,246,240,' + (0.55 - L * 0.08) + ')'); mg.addColorStop(1, 'rgba(238,246,240,0)'); x.fillStyle = mg; x.fillRect(0, base - h * 0.16, w, h * 0.2);
      }
    },
    /* 파스텔 구름 */
    pastel: function (x, w, h, R, s) {
      var P = pick(R, [['#cfe3ff', '#f7d6ee', '#fff1d6'], ['#d8f0e6', '#cfe0ff', '#fbe3f1'], ['#ffe0d2', '#e9d8ff', '#d4ecff']]);
      lin(x, w, h, [[0, P[0]], [0.55, P[1]], [1, P[2]]], 0, 0, 0.25, 1);
      field(x, w, h, 200, function (u, v) { var c = fbm(u * 3.4, v * 5.2, s, 5); var a = Math.max(0, c - 0.5) * 2.6; return [255, 255, 255, Math.min(0.85, a) * 255]; });
    },
    /* 고서 양피지 */
    parchment: function (x, w, h, R, s) {
      field(x, w, h, 300, function (u, v) { var n = fbm(u * 5, v * 5, s, 5), m = fbm(u * 26, v * 26, s + 4, 3), e = Math.pow(Math.max(Math.abs(u - 0.5), Math.abs(v - 0.5)) * 2, 3); var b = 222 + n * 26 + m * 6 - e * 70; return [b, b - 22 - e * 20, b - 62 - e * 40, 255]; });
      for (var i = 0; i < 4; i++) { var cx = R() * w, cy = R() * h; rad(x, cx, cy, Math.min(w, h) * (0.12 + R() * 0.2), 'rgba(150,100,50,0.10)', 'rgba(150,100,50,0)'); }
    },
    /* 스테인드글라스 */
    stained: function (x, w, h, R, s) {
      var N = 26, pts = [], cols = ['#1f5fa8', '#c0392b', '#e0a526', '#2e8b57', '#6b3fa0', '#d9731a', '#2aa6a6', '#b03a74'];
      for (var i = 0; i < N; i++) pts.push([R(), R(), pick(R, cols)]);
      field(x, w, h, 260, function (u, v) {
        var d1 = 9, d2 = 9, ci = 0; for (var i = 0; i < N; i++) { var dx = (u - pts[i][0]) * (w / Math.max(w, h)), dy = (v - pts[i][1]) * (h / Math.max(w, h)), d = Math.sqrt(dx * dx + dy * dy); if (d < d1) { d2 = d1; d1 = d; ci = i; } else if (d < d2) d2 = d; }
        var edge = d2 - d1; if (edge < 0.012) return [28, 24, 30, 255]; var c = pts[ci][2], r = parseInt(c.slice(1, 3), 16), g = parseInt(c.slice(3, 5), 16), b = parseInt(c.slice(5, 7), 16); var glow = 0.55 + 0.45 * Math.min(1, d1 * 6); var k = 0.65 + (1 - glow) * 0.5 + fbm(u * 8, v * 8, s, 2) * 0.2; return [Math.min(255, r * k), Math.min(255, g * k), Math.min(255, b * k), 255];
      });
      lin(x, w, h, [[0, 'rgba(255,255,255,0.28)'], [1, 'rgba(0,0,30,0.2)']], 0, 0, 0, 1);
    }
  };

  var LIST = [
    { k: 'wc', n: '수채화 번짐', light: true }, { k: 'ink', n: '수묵 산수', light: true }, { k: 'hanji', n: '한지 질감', light: true },
    { k: 'marble', n: '대리석', light: true }, { k: 'gold', n: '별빛과 금빛', light: false }, { k: 'bokeh', n: '빛망울 야경', light: false },
    { k: 'linen', n: '리넨 질감', light: true }, { k: 'dawn', n: '새벽 노을', light: false }, { k: 'mist', n: '안개 숲', light: false },
    { k: 'pastel', n: '파스텔 구름', light: true }, { k: 'parchment', n: '고서 양피지', light: true }, { k: 'stained', n: '스테인드글라스', light: false }
  ];
  window.crsBgScenes = { list: LIST, draw: DRAW };
})();
