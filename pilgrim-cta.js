/* '달려가노라'(바울과 함께 걷는 순례 게임) 연결 카드.
   말씀을 뽑았거나 카드를 저장한 직후, 퍼즐 정답을 확인한 직후처럼 마음이 말씀에 열린 순간에 보여 준다.
   사용: crsPilgrimCta({ host: 'elementId', campaign: 'verse_after_draw' }) */
(function () {
  'use strict';
  var BASE = 'https://dallyeoganora.vercel.app/';
  function css() {
    if (document.getElementById('pgCtaCss')) return;
    var s = document.createElement('style'); s.id = 'pgCtaCss';
    s.textContent = '.pgcta{display:flex;align-items:center;gap:14px;max-width:560px;margin:18px auto 6px;padding:14px 16px;border:2px solid #f0b36b;border-radius:16px;background:linear-gradient(135deg,#fff7ea,#ffe9cc);text-align:left;text-decoration:none;color:#5a2a05;box-shadow:0 6px 16px rgba(176,92,10,.16);transition:transform .15s;box-sizing:border-box}' +
      '.pgcta:hover{transform:translateY(-2px)}' +
      '.pgcta img{width:64px;height:70px;object-fit:contain;flex:none}' +
      '.pgcta b{display:block;font-size:16.5px;line-height:1.45;color:#7a2e00}' +
      '.pgcta span{display:block;font-size:13px;line-height:1.55;color:#6f4a2a;margin-top:3px}' +
      '.pgcta i{display:inline-block;margin-top:8px;font-style:normal;font-weight:800;font-size:13.5px;background:#c2410c;color:#fff;padding:6px 14px;border-radius:18px}' +
      '@media(max-width:480px){.pgcta{gap:10px;padding:12px}.pgcta img{width:52px;height:57px}.pgcta b{font-size:15px}.pgcta span{font-size:12.5px}}';
    document.head.appendChild(s);
  }
  window.crsPilgrimCta = function (o) {
    try {
      var host = typeof o.host === 'string' ? document.getElementById(o.host) : o.host;
      if (!host || host.querySelector('.pgcta')) return;
      css();
      var a = document.createElement('a');
      a.className = 'pgcta';
      a.href = BASE + '?utm_source=crossero&utm_medium=cta&utm_campaign=' + encodeURIComponent(o.campaign || 'cta');
      a.target = '_blank'; a.rel = 'noopener';
      a.setAttribute('data-ga', 'pilgrim_cta_click'); a.setAttribute('data-ga-label', o.campaign || 'cta');
      a.innerHTML = '<img src="/images/paul-face.png" alt="" width="64" height="70">' +
        '<div><b>' + (o.title || '이 말씀 품고, 바울과 함께 40일 걸어 보기') + '</b>' +
        '<span>' + (o.sub || '달려가노라 · 하루 한 걸음, 바울의 전도 여행길을 걷는 순례 게임') + '</span><i>순례 시작하기 →</i></div>';
      host.appendChild(a);
      if (window.crsTrack) window.crsTrack('pilgrim_cta_view', { campaign: o.campaign || 'cta' });
    } catch (e) {}
  };
})();
