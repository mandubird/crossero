/* 십자가로세로 구독 폼(푸터 삽입형) — <footer> 맨 위에 스스로 들어간다. <div id="crs-subscribe"> 가 있으면 그 자리에 넣는다.
   폼 주소·입력 이름·id는 스티비 '구독 화면 > 코드로 설치하기'의 공개 임베드 코드 그대로이고(스티비 스크립트가 id에 의존),
   스타일만 직접 입혔다. 스티비 스크립트는 폼이 화면에 가까워질 때 불러온다. */
(function () {
  if (!window.CRS_SUBSCRIBE_ENABLED) return; /* 2026-11-08 숨김: 월별 발송 콘텐츠가 준비되면 페이지에서 window.CRS_SUBSCRIBE_ENABLED=true 로 켠다(또는 이 줄 삭제) */
  function init() {
    if (document.getElementById('stb_subscribe_form')) return;
    var host = document.getElementById('crs-subscribe');
    if (!host) {
      var footer = document.querySelector('footer');
      if (!footer) return;
      host = document.createElement('div');
      host.id = 'crs-subscribe';
      var divider = footer.querySelector('.footer-divider');
      if (divider && divider.parentNode === footer) footer.insertBefore(host, divider.nextSibling);
      else footer.insertBefore(host, footer.firstChild);
    }

    var css =
      '#crs-subscribe{max-width:560px;margin:0 auto 22px;padding:0 14px;box-sizing:border-box;text-align:left}' +
      '#crs-subscribe .crs-subc{background:#f0f6ff;border:1px solid #d3e3f8;border-radius:12px;padding:12px 14px 10px}' +
      '#crs-subscribe .crs-subc-head{font-size:13.5px;color:#0b5cad;font-weight:700;margin:0 0 8px;line-height:1.5}' +
      '#crs-subscribe .crs-subc-head span{font-weight:400;color:#667}' +
      '#crs-subscribe .stb_form{display:grid;grid-template-columns:1fr auto;gap:0 6px;margin:0;padding:0;border:0}' +
      '#crs-subscribe fieldset{border:0;margin:0;padding:0;min-width:0}' +
      '#crs-subscribe .stb_form_set_label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}' +
      '#crs-subscribe .stb_form_set_input{width:100%;height:36px;box-sizing:border-box;padding:0 12px;border:1px solid #bcd3f0;border-radius:8px;font-size:13.5px;background:#fff;font-family:inherit}' +
      '#crs-subscribe .stb_form_set_submit{display:flex}' +
      '#crs-subscribe .stb_form_submit_button{height:36px;padding:0 16px;border:0;border-radius:8px;background:#0073e6;color:#fff;font-weight:700;font-size:13.5px;cursor:pointer;white-space:nowrap;font-family:inherit}' +
      '#crs-subscribe .stb_form_policy{grid-column:1/-1;margin-top:6px;font-size:11.5px;color:#667;line-height:1.5}' +
      '#crs-subscribe .stb_form_policy label{cursor:pointer}' +
      '#crs-subscribe .stb_form_policy input{vertical-align:middle;margin:0 3px 0 0}' +
      '#crs-subscribe .stb_form_modal_open_btn{background:none;border:0;padding:0;color:#0b5cad;text-decoration:underline;font-size:inherit;cursor:pointer;font-family:inherit}' +
      '#crs-subscribe .stb_form_msg_error{color:#d33;font-size:11.5px;margin-top:3px}' +
      '#crs-subscribe .stb_form_result{grid-column:1/-1;font-size:12px;color:#0b5cad;margin-top:4px}' +
      '#crs-subscribe .stb_form_modal{position:fixed;left:0;top:0;right:0;bottom:0;z-index:99999;display:flex;align-items:center;justify-content:center}' +
      '#crs-subscribe .stb_form_modal.blind{display:none}' +
      '#crs-subscribe .stb_form_modal_bg{position:absolute;left:0;top:0;right:0;bottom:0;background:rgba(0,0,0,.5)}' +
      '#crs-subscribe .stb_form_modal_body{position:relative;z-index:1;background:#fff;padding:22px;border-radius:12px;max-width:420px;width:calc(100% - 40px);box-sizing:border-box;color:#333}' +
      '#crs-subscribe .stb_form_modal_title{font-size:16px;margin:0 0 10px}' +
      '#crs-subscribe .stb_form_modal_text{font-size:13.5px;line-height:1.7;white-space:pre-line;margin-bottom:14px}' +
      '#crs-subscribe .stb_form_modal_close_btn{padding:8px 18px;border:0;border-radius:8px;background:#0073e6;color:#fff;cursor:pointer}' +
      '@media (max-width:480px){#crs-subscribe{padding:0 10px;margin-bottom:14px}#crs-subscribe .crs-subc{padding:9px 10px 8px;border-radius:10px}#crs-subscribe .crs-subc-head,#crs-subscribe .crs-hide-m{display:none}#crs-subscribe .stb_form_set_input{height:32px;font-size:13px;padding:0 10px}#crs-subscribe .stb_form_submit_button{height:32px;padding:0 14px;font-size:13px}#crs-subscribe .stb_form_policy{font-size:11px;margin-top:5px}}';

    host.innerHTML =
      '<style>' + css + '</style>' +
      '<div class="crs-subc">' +
      '<div class="crs-subc-head">📬 새 성경 퍼즐 메일 받기 <span>· 한 달에 두 번 · 무료 · 언제든 해지</span></div>' +
      '<div id="stb_subscribe">' +
      '<form action="https://stibee.com/api/v1.0/lists/t6cEpKB66B_9cqbWfjBu-08AeE83fw==/public/subscribers" method="POST" target="_blank" accept-charset="utf-8" class="stb_form" name="stb_subscribe_form" id="stb_subscribe_form" data-lang="" novalidate>' +
      '<fieldset class="stb_form_set">' +
      '<label for="stb_email" class="stb_form_set_label">이메일 주소<span class="stb_asterisk">*</span></label>' +
      '<input type="text" class="stb_form_set_input" id="stb_email" name="email" required="required" placeholder="이메일 주소" inputmode="email" autocomplete="email">' +
      '<div class="stb_form_msg_error" id="stb_email_error"></div>' +
      '</fieldset>' +
      '<fieldset class="stb_form_set_submit"><button type="submit" class="stb_form_submit_button" id="stb_form_submit_button" data-ga="subscribe_click" data-ga-label="footer">구독</button></fieldset>' +
      '<div class="stb_form_policy"><label>' +
      '<input type="checkbox" id="stb_policy" value="stb_policy_true"><span>(필수)</span> ' +
      '<button id="stb_form_modal_open" data-modal="stb_form_policy_modal" class="stb_form_modal_open_btn" type="button">개인정보 수집 및 이용</button>에 동의<span class="crs-hide-m"> · </span>' +
      '<a class="crs-hide-m" href="/privacy.html" style="color:#889;">처리방침</a>' +
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

    if (window.matchMedia && window.matchMedia('(max-width:480px)').matches) {
      document.getElementById('stb_email').placeholder = '📬 새 성경 퍼즐 메일 받기 (이메일 주소)';
    }

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
      }, { rootMargin: '300px' });
      io.observe(host);
    } else {
      loadStibee();
    }
    host.addEventListener('focusin', loadStibee, true);
    host.addEventListener('submit', function () {
      if (window.crsTrack) window.crsTrack('subscribe_submit', { method: 'stibee_footer' });
    }, true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

/* 참여 후 구독 안내 — 글을 55% 이상 읽고 15초가 지났거나 퍼즐을 풀었을 때 아래에서 한 번만 올라온다.
   닫으면 21일, 구독 제출 후에는 다시 뜨지 않는다. 퍼즐 풀이 중·스튜디오 화면에서는 뜨지 않는다. */
(function () {
  if (!window.CRS_SUBSCRIBE_ENABLED) return;
  var KEY = 'crs_sub_prompt';
  var path = location.pathname;
  function store(get, v) { try { return get ? localStorage.getItem(KEY) : localStorage.setItem(KEY, v); } catch (e) { return null; } }
  var until = parseInt(store(true) || '0', 10);
  if (until > Date.now()) return;
  var isPlay = /^\/play(2)?(\.html)?$/.test(path);
  var content = /^\/(dictionary|posts|christmas|guide|teachers|today|cards|verse\/[^/]+)\//.test(path) && !/^\/cards\/make\//.test(path);
  if (!isPlay && !content) return;
  var shown = false, t0 = Date.now();
  function show(msg, label) {
    if (shown || !document.getElementById('crs-subscribe')) return;
    shown = true;
    var b = document.createElement('div');
    b.id = 'crs-subprompt';
    b.setAttribute('role', 'dialog');
    b.innerHTML = '<style>#crs-subprompt{position:fixed;left:50%;bottom:14px;transform:translate(-50%,140%);z-index:96;width:calc(100% - 24px);max-width:460px;box-sizing:border-box;background:#fff;border:1px solid #bcd3f0;border-radius:14px;box-shadow:0 8px 28px rgba(0,40,90,.22);padding:14px 16px;transition:transform .4s ease;font-family:inherit}' +
      '#crs-subprompt.on{transform:translate(-50%,0)}#crs-subprompt p{margin:0 0 10px;font-size:15px;line-height:1.55;color:#223}#crs-subprompt p b{color:#0b5cad}' +
      '#crs-subprompt .r{display:flex;gap:8px}#crs-subprompt button{height:42px;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit}' +
      '#crs-subprompt .go{flex:1;border:0;background:#0073e6;color:#fff}#crs-subprompt .no{padding:0 14px;border:1px solid #cfd8e6;background:#fff;color:#556}' +
      '@media (prefers-reduced-motion:reduce){#crs-subprompt{transition:none}}</style>' +
      '<p>' + msg + '</p><div class="r"><button class="go" type="button">메일로 받기</button><button class="no" type="button">나중에</button></div>';
    document.body.appendChild(b);
    requestAnimationFrame(function () { requestAnimationFrame(function () { b.classList.add('on'); }); });
    if (window.crsTrack) window.crsTrack('subscribe_prompt_show', { label: label, page_path: path });
    function close(days) { store(false, String(Date.now() + days * 864e5)); b.classList.remove('on'); setTimeout(function () { b.remove(); }, 450); }
    b.querySelector('.no').onclick = function () { if (window.crsTrack) window.crsTrack('subscribe_prompt_dismiss', { label: label }); close(21); };
    b.querySelector('.go').onclick = function () {
      if (window.crsTrack) window.crsTrack('subscribe_prompt_click', { label: label, page_path: path });
      close(60);
      var h = document.getElementById('crs-subscribe');
      if (h) { h.scrollIntoView({ behavior: 'smooth', block: 'center' }); setTimeout(function () { var i = document.getElementById('stb_email'); if (i) i.focus({ preventScroll: true }); }, 700); }
    };
  }
  if (isPlay) {
    window.addEventListener('crs-puzzle-complete', function () { setTimeout(function () { show('🎉 퍼즐 완성! 새 퍼즐과 <b>말씀카드</b> 소식을 <b>한 달에 두 번</b> 메일로 보내 드려요.', 'puzzle'); }, 1800); });
  } else {
    var check = function () {
      var d = document.documentElement, sc = (window.scrollY + window.innerHeight) / Math.max(d.scrollHeight, 1);
      if (sc >= 0.55 && Date.now() - t0 >= 15000) { window.removeEventListener('scroll', check); show('도움이 되셨나요? 새 퍼즐·말씀카드·교사 자료를 <b>한 달에 두 번</b> 메일로 보내 드려요. (무료)', 'read'); }
    };
    window.addEventListener('scroll', check, { passive: true });
    setTimeout(check, 15500);
  }
  document.addEventListener('submit', function (e) { if (e.target && e.target.id === 'stb_subscribe_form') store(false, String(Date.now() + 3650 * 864e5)); }, true);
})();
