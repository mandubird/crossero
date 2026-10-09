/* 십자가로세로 구독 박스 — <div id="crs-subscribe"></div> 가 있는 페이지에 스티비 구독 폼을 삽입.
   폼 주소·입력 이름·id는 스티비 '구독 화면 > 코드로 설치하기'의 공개 임베드 코드 그대로이고(스티비 스크립트가 id에 의존),
   스타일만 직접 입혔다. 스티비 스크립트는 박스가 화면에 가까워질 때 불러온다. */
(function () {
  var host = document.getElementById('crs-subscribe');
  if (!host) return;

  var css =
    '#crs-subscribe .crs-sub{max-width:720px;margin:28px auto;padding:20px 20px 16px;background:#f0f6ff;border:1px solid #cfe2ff;border-radius:16px;box-sizing:border-box}' +
    '#crs-subscribe .crs-sub-title{font-size:17px;font-weight:700;color:#0b5cad;text-align:center;margin:0 0 4px}' +
    '#crs-subscribe .crs-sub-desc{font-size:13.5px;color:#556;text-align:center;margin:0 0 12px;line-height:1.6}' +
    '#crs-subscribe .stb_form{display:grid;grid-template-columns:1fr auto;gap:0 8px;margin:0;padding:0;border:0;max-width:520px;margin:0 auto}' +
    '#crs-subscribe fieldset{border:0;margin:0;padding:0;min-width:0}' +
    '#crs-subscribe .stb_form_set_label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}' +
    '#crs-subscribe .stb_form_set_input{width:100%;height:44px;box-sizing:border-box;padding:0 14px;border:1px solid #bcd3f0;border-radius:10px;font-size:15px;background:#fff}' +
    '#crs-subscribe .stb_form_set_submit{display:flex}' +
    '#crs-subscribe .stb_form_submit_button{height:44px;padding:0 22px;border:0;border-radius:10px;background:#0073e6;color:#fff;font-weight:700;font-size:15px;cursor:pointer;white-space:nowrap}' +
    '#crs-subscribe .stb_form_policy{grid-column:1/-1;margin-top:8px;font-size:12.5px;color:#556}' +
    '#crs-subscribe .stb_form_policy label{cursor:pointer}' +
    '#crs-subscribe .stb_form_modal_open_btn{background:none;border:0;padding:0;color:#0b5cad;text-decoration:underline;font-size:inherit;cursor:pointer}' +
    '#crs-subscribe .stb_form_msg_error{color:#d33;font-size:12.5px;margin-top:4px}' +
    '#crs-subscribe .stb_form_result{grid-column:1/-1;font-size:13px;color:#0b5cad;margin-top:6px;text-align:center}' +
    '#crs-subscribe .stb_form_modal{position:fixed;left:0;top:0;right:0;bottom:0;z-index:99999;display:flex;align-items:center;justify-content:center}' +
    '#crs-subscribe .stb_form_modal.blind{display:none}' +
    '#crs-subscribe .stb_form_modal_bg{position:absolute;left:0;top:0;right:0;bottom:0;background:rgba(0,0,0,.5)}' +
    '#crs-subscribe .stb_form_modal_body{position:relative;z-index:1;background:#fff;padding:22px;border-radius:12px;max-width:420px;width:calc(100% - 40px);box-sizing:border-box;color:#333}' +
    '#crs-subscribe .stb_form_modal_title{font-size:16px;margin:0 0 10px}' +
    '#crs-subscribe .stb_form_modal_text{font-size:13.5px;line-height:1.7;white-space:pre-line;margin-bottom:14px}' +
    '#crs-subscribe .stb_form_modal_close_btn{padding:8px 18px;border:0;border-radius:8px;background:#0073e6;color:#fff;cursor:pointer}' +
    '@media (max-width:480px){#crs-subscribe .stb_form{grid-template-columns:1fr}#crs-subscribe .stb_form_set_submit{margin-top:8px}#crs-subscribe .stb_form_submit_button{width:100%}}';

  host.innerHTML =
    '<style>' + css + '</style>' +
    '<div class="crs-sub">' +
    '<div class="crs-sub-title">📬 새 성경 퍼즐을 이메일로 받아보세요</div>' +
    '<p class="crs-sub-desc">한 달에 두 번 · 새 퍼즐과 말씀 요약 · 무료이고 언제든 해지할 수 있어요</p>' +
    '<div id="stb_subscribe">' +
    '<form action="https://stibee.com/api/v1.0/lists/t6cEpKB66B_9cqbWfjBu-08AeE83fw==/public/subscribers" method="POST" target="_blank" accept-charset="utf-8" class="stb_form" name="stb_subscribe_form" id="stb_subscribe_form" data-lang="" novalidate>' +
    '<fieldset class="stb_form_set">' +
    '<label for="stb_email" class="stb_form_set_label">이메일 주소<span class="stb_asterisk">*</span></label>' +
    '<input type="text" class="stb_form_set_input" id="stb_email" name="email" required="required" placeholder="이메일 주소를 입력하세요" inputmode="email" autocomplete="email">' +
    '<div class="stb_form_msg_error" id="stb_email_error"></div>' +
    '</fieldset>' +
    '<fieldset class="stb_form_set_submit"><button type="submit" class="stb_form_submit_button" id="stb_form_submit_button" data-ga="subscribe_click" data-ga-label="subscribe_box">구독하기</button></fieldset>' +
    '<div class="stb_form_policy"><label>' +
    '<input type="checkbox" id="stb_policy" value="stb_policy_true"> <span>(필수)</span> ' +
    '<button id="stb_form_modal_open" data-modal="stb_form_policy_modal" class="stb_form_modal_open_btn" type="button">개인정보 수집 및 이용</button>에 동의합니다. ' +
    '<a href="/privacy.html" style="color:#889;">처리방침</a>' +
    '</label>' +
    '<div class="stb_form_msg_error" id="stb_policy_error"></div>' +
    '<div class="stb_form_modal stb_form_policy_text blind" id="stb_form_policy_modal"><div class="stb_form_modal_body">' +
    '<h1 class="stb_form_modal_title">개인정보 수집 및 이용</h1>' +
    '<div class="stb_form_modal_text">뉴스레터 발송을 위한 최소한의 개인정보를 수집하고 이용합니다.\n수집된 정보는 발송 외 다른 목적으로 이용되지 않으며, 서비스가 종료되거나 구독을 해지할 경우 즉시 파기됩니다.</div>' +
    '<div class="stb_form_modal_btn"><button id="stb_form_modal_close" class="stb_form_modal_close_btn" data-modal="stb_form_policy_modal" type="button">닫기</button></div>' +
    '</div><div class="stb_form_modal_bg" id="stb_form_modal_bg"></div></div>' +
    '</div>' +
    '<div class="stb_form_result" id="stb_form_result"></div>' +
    '</form></div></div>';

  var loaded = false;
  function loadStibee() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement('script');
    s.src = 'https://resource.stibee.com/subscribe/stb_subscribe_form.js';
    s.async = true;
    document.body.appendChild(s);
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); loadStibee(); }
    }, { rootMargin: '400px' });
    io.observe(host);
  } else {
    loadStibee();
  }
  host.addEventListener('focusin', loadStibee, true);

  host.addEventListener('submit', function () {
    if (window.crsTrack) window.crsTrack('subscribe_submit', { method: 'stibee_form' });
  }, true);
})();
