/* 주간 퍼즐 구독 박스 — <div id="crs-subscribe"></div> 가 있는 페이지에 삽입됨
   CRS_SUBSCRIBE_ENDPOINT 에 이메일 서비스(Stibee/Formspree 등)의 폼 전송 URL을 넣으면
   입력창에서 바로 구독 신청이 되고, 비워 두면 메일 앱으로 신청하는 방식으로 동작함. */
(function () {
  var CRS_SUBSCRIBE_ENDPOINT = '';
  var CRS_SUBSCRIBE_EMAIL_FIELD = 'email';

  var host = document.getElementById('crs-subscribe');
  if (!host) return;

  host.innerHTML =
    '<div style="max-width:720px;margin:32px auto;padding:24px 20px;background:#f0f6ff;border:1px solid #cfe2ff;border-radius:16px;text-align:center;">' +
    '<div style="font-size:18px;font-weight:700;color:#0b5cad;margin-bottom:6px;">📬 매주 토요일, 새 성경 퍼즐을 받아보세요</div>' +
    '<p style="font-size:14px;color:#555;line-height:1.7;margin:0 0 14px;">이번 주 퍼즐과 짧은 말씀 요약을 이메일로 보내드립니다. 광고성 메일은 보내지 않으며 언제든 해지할 수 있습니다.</p>' +
    '<form id="crs-sub-form" style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;">' +
    '<input id="crs-sub-email" type="email" required placeholder="이메일 주소" aria-label="이메일 주소" style="flex:1 1 220px;max-width:320px;padding:12px 14px;border:1px solid #bcd3f0;border-radius:10px;font-size:15px;">' +
    '<button type="submit" data-ga="subscribe_click" data-ga-label="subscribe_box" style="padding:12px 22px;background:#0073e6;color:#fff;border:none;border-radius:10px;font-weight:700;font-size:15px;cursor:pointer;">구독하기</button>' +
    '</form>' +
    '<div id="crs-sub-msg" style="font-size:13px;color:#0b5cad;margin-top:10px;min-height:18px;"></div>' +
    '<div style="font-size:12px;color:#888;margin-top:6px;">수집한 이메일은 퍼즐 발송에만 사용합니다. <a href="/privacy.html" style="color:#888;">개인정보처리방침</a></div>' +
    '</div>';

  var form = document.getElementById('crs-sub-form');
  var msg = document.getElementById('crs-sub-msg');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = document.getElementById('crs-sub-email').value.trim();
    if (!email) return;

    if (!CRS_SUBSCRIBE_ENDPOINT) {
      var subject = encodeURIComponent('[십자가로세로] 주간 퍼즐 구독 신청');
      var body = encodeURIComponent('주간 퍼즐 메일 구독을 신청합니다.\n신청 이메일: ' + email);
      window.location.href = 'mailto:mandubird@naver.com?subject=' + subject + '&body=' + body;
      msg.textContent = '메일 앱이 열리면 그대로 보내 주세요. 확인 후 구독 목록에 추가해 드립니다.';
      if (window.crsTrack) window.crsTrack('subscribe_submit', { method: 'mailto' });
      return;
    }

    var data = new FormData();
    data.append(CRS_SUBSCRIBE_EMAIL_FIELD, email);
    fetch(CRS_SUBSCRIBE_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) {
        if (!r.ok) throw new Error('bad status');
        msg.textContent = '구독해 주셔서 감사합니다. 이번 주 토요일부터 보내드릴게요.';
        form.reset();
        if (window.crsTrack) window.crsTrack('subscribe_submit', { method: 'form' });
      })
      .catch(function () {
        msg.textContent = '잠시 후 다시 시도해 주세요. 계속 안 되면 mandubird@naver.com 으로 알려 주세요.';
      });
  });
})();
