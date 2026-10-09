/* 십자가로세로 구독 박스 — <div id="crs-subscribe"></div> 가 있는 페이지에 삽입됨
   구독 신청은 스티비 호스팅 구독 페이지에서 이메일을 입력해 진행(구독 확인 메일·동의·수신거부는 스티비가 처리). */
(function () {
  var SUBSCRIBE_URL = 'https://page.stibee.com/subscriptions/522433';
  var host = document.getElementById('crs-subscribe');
  if (!host) return;

  host.innerHTML =
    '<div style="max-width:720px;margin:32px auto;padding:24px 20px;background:#f0f6ff;border:1px solid #cfe2ff;border-radius:16px;text-align:center;">' +
    '<div style="font-size:18px;font-weight:700;color:#0b5cad;margin-bottom:6px;">📬 새 성경 퍼즐을 이메일로 받아보세요</div>' +
    '<p style="font-size:14px;color:#555;line-height:1.7;margin:0 0 14px;">한 달에 두 번, 새 퍼즐과 짧은 말씀 요약, 함께 읽을 성경사전 항목을 보내드립니다. 구독은 무료이고 메일 아래 링크로 언제든 해지할 수 있습니다.</p>' +
    '<a href="' + SUBSCRIBE_URL + '" target="_blank" rel="noopener" data-ga="subscribe_click" data-ga-label="subscribe_box" ' +
    'style="display:inline-block;padding:13px 28px;background:#0073e6;color:#fff;border-radius:10px;font-weight:700;font-size:15px;text-decoration:none;">구독하러 가기</a>' +
    '<div style="font-size:12px;color:#888;margin-top:10px;">스티비 구독 페이지에서 이메일 주소만 입력하면 됩니다. 자세한 내용은 <a href="/privacy.html" style="color:#888;">개인정보처리방침</a>을 확인해 주세요.</div>' +
    '</div>';
})();
