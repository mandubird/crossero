/**
 * 쿠팡 파트너스 배너 - 한 곳에서 설정하면 메뉴 아래 + 팝업 내부(play) 모든 영역에 적용
 * 사용법: 아래 COUPANG_* 값만 쿠팡 파트너스에서 발급한 값으로 바꾸면 됨.
 */
(function () {
  // ========== 여기만 수정 ==========
  // 쿠팡 파트너스 > 링크/배너 만들기 > 다이나믹 배너에서 생성한 값
  window.COUPANG_TRACKING_CODE = 'AF2423892';  // 예: 'AF1234567'
  window.COUPANG_BANNER_ID_PC = '970232';   // PC용 배너 ID (비우면 TRACKING_CODE만 사용)
  window.COUPANG_BANNER_ID_MOBILE = '970233'; // 모바일용 배너 ID (비우면 PC와 동일)
  // ================================

  if (!window.COUPANG_TRACKING_CODE) return;

  var BANNER_IDS = [
    'top-banner-pc',
    'top-banner-mobile',
    'popup-banner-pc',
    'popup-banner-mobile'
  ];

  var containers = BANNER_IDS.map(function (id) {
    var el = document.getElementById(id);
    return el ? { id: id, el: el } : null;
  }).filter(Boolean);

  if (containers.length === 0) return;

  var pcId = window.COUPANG_BANNER_ID_PC || window.COUPANG_TRACKING_CODE;
  var mobileId = window.COUPANG_BANNER_ID_MOBILE || pcId;
  var assignOrder = [];
  containers.forEach(function (c) {
    if (c.id.indexOf('mobile') !== -1) assignOrder.push({ container: c.el, bannerId: mobileId });
    else assignOrder.push({ container: c.el, bannerId: pcId });
  });

  var appended = 0;
  function assignIframe(iframe) {
    if (!iframe || iframe.getAttribute('data-coupang-assigned')) return;
    if (appended >= assignOrder.length) return;
    var target = assignOrder[appended].container;
    if (target && !target.querySelector('iframe')) {
      iframe.setAttribute('data-coupang-assigned', '1');
      target.appendChild(iframe);
      appended++;
    }
  }

  var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (m) {
      m.addedNodes.forEach(function (node) {
        if (node.nodeType === 1 && node.tagName === 'IFRAME' && node.src && node.src.indexOf('coupang') !== -1) {
          assignIframe(node);
        }
      });
    });
  });
  observer.observe(document.body, { childList: true, subtree: true });

  function run() {
    if (typeof window.PartnersCoupang === 'undefined' || !window.PartnersCoupang.G) {
      setTimeout(run, 100);
      return;
    }
    assignOrder.forEach(function (item) {
      try {
        window.PartnersCoupang.G({ id: item.bannerId, trackingCode: window.COUPANG_TRACKING_CODE });
      } catch (e) {}
    });
  }

  var s = document.createElement('script');
  s.src = 'https://ads-partners.coupang.com/g.js';
  s.async = true;
  s.onload = run;
  document.head.appendChild(s);
})();
