/* 십자가로세로 구독 박스 — <div id="crs-subscribe"></div> 가 있는 페이지에 스티비 구독 폼을 삽입.
   폼 주소는 스티비 '구독 화면 > 코드로 설치하기'의 공개 임베드 코드 그대로이며, 확인 메일·수신거부는 스티비가 처리한다. */
(function () {
  var host = document.getElementById('crs-subscribe');
  if (!host) return;

  host.innerHTML =
    '<div style="max-width:720px;margin:32px auto;padding:24px 20px 8px;background:#f0f6ff;border:1px solid #cfe2ff;border-radius:16px;">' +
    '<div style="text-align:center;">' +
    '<div style="font-size:18px;font-weight:700;color:#0b5cad;margin-bottom:6px;">📬 새 성경 퍼즐을 이메일로 받아보세요</div>' +
    '<p style="font-size:14px;color:#555;line-height:1.7;margin:0;">한 달에 두 번, 새 퍼즐과 짧은 말씀 요약, 함께 읽을 성경사전 항목을 보내드립니다. 구독은 무료이고 메일 아래 링크로 언제든 해지할 수 있습니다.</p>' +
    '</div>' +
    '<link rel="stylesheet" href="https://resource.stibee.com/subscribe/stb_subscribe_form_style.css">' +
    '<div id="stb_subscribe">' +
    '<form action="https://stibee.com/api/v1.0/lists/t6cEpKB66B_9cqbWfjBu-08AeE83fw==/public/subscribers" method="POST" target="_blank" accept-charset="utf-8" class="stb_form" name="stb_subscribe_form" id="stb_subscribe_form" data-lang="" novalidate>' +
    '<fieldset class="stb_form_set">' +
    '<label for="stb_email" class="stb_form_set_label">이메일 주소<span class="stb_asterisk">*</span></label>' +
    '<input type="text" class="stb_form_set_input" id="stb_email" name="email" required="required">' +
    '<div class="stb_form_msg_error" id="stb_email_error"></div>' +
    '</fieldset>' +
    '<div class="stb_form_policy"><label>' +
    '<input type="checkbox" id="stb_policy" value="stb_policy_true"> <span>(필수)</span> ' +
    '<button id="stb_form_modal_open" data-modal="stb_form_policy_modal" class="stb_form_modal_open_btn" type="button">개인정보 수집 및 이용</button>에 동의합니다.' +
    '</label>' +
    '<div class="stb_form_msg_error" id="stb_policy_error"></div>' +
    '<div class="stb_form_modal stb_form_policy_text blind" id="stb_form_policy_modal"><div class="stb_form_modal_body">' +
    '<h1 class="stb_form_modal_title">개인정보 수집 및 이용</h1>' +
    '<div class="stb_form_modal_text">뉴스레터 발송을 위한 최소한의 개인정보를 수집하고 이용합니다.\n수집된 정보는 발송 외 다른 목적으로 이용되지 않으며, 서비스가 종료되거나 구독을 해지할 경우 즉시 파기됩니다.</div>' +
    '<div class="stb_form_modal_btn"><button id="stb_form_modal_close" class="stb_form_modal_close_btn" data-modal="stb_form_policy_modal" type="button">닫기</button></div>' +
    '</div><div class="stb_form_modal_bg" id="stb_form_modal_bg"></div></div>' +
    '</div>' +
    '<div class="stb_form_result" id="stb_form_result"></div>' +
    '<fieldset class="stb_form_set_submit"><button type="submit" class="stb_form_submit_button" id="stb_form_submit_button" style="background-color:#0073e6;color:#FFFFFF;" data-ga="subscribe_click" data-ga-label="subscribe_box">구독하기</button></fieldset>' +
    '</form></div>' +
    '<div style="font-size:12px;color:#888;text-align:center;padding:4px 0 14px;">자세한 내용은 <a href="/privacy.html" style="color:#888;">개인정보처리방침</a>을 확인해 주세요.</div>' +
    '</div>';

  var s = document.createElement('script');
  s.src = 'https://resource.stibee.com/subscribe/stb_subscribe_form.js';
  s.async = true;
  document.body.appendChild(s);

  host.addEventListener('submit', function () {
    if (window.crsTrack) window.crsTrack('subscribe_submit', { method: 'stibee_form' });
  }, true);
})();
