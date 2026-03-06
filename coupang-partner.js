/**
 * 쿠팡 파트너스 배너 - 한 곳에서 설정하면 메뉴 아래 + 팝업 내부(play) 모든 영역에 적용
 * 사용법: 아래 COUPANG_* 값만 쿠팡 파트너스에서 발급한 값으로 바꾸면 됨.
 */
(function () {
  // ========== 여기만 수정 ==========
  window.COUPANG_TRACKING_CODE = 'AF2423892';
  window.COUPANG_BANNER_ID_PC = '970232';
  window.COUPANG_BANNER_ID_MOBILE = '970233';
  // ================================

  if (!window.COUPANG_TRACKING_CODE) return;

  var pcId = String(window.COUPANG_BANNER_ID_PC || window.COUPANG_TRACKING_CODE);
  var mobileId = String(window.COUPANG_BANNER_ID_MOBILE || pcId);
  var idNumPc = parseInt(pcId, 10);
  var idNumMobile = parseInt(mobileId, 10);
  var argPc     = isNaN(idNumPc)     ? pcId     : idNumPc;
  var argMobile = isNaN(idNumMobile) ? mobileId : idNumMobile;

  // 현재 페이지에 존재하는 컨테이너만 순서대로 수집
  // G() 호출 순서와 정확히 일치해야 함
  var SLOTS = [
    { id: 'top-banner-pc',      arg: argPc },
    { id: 'popup-banner-pc',    arg: argPc },
    { id: 'top-banner-mobile',  arg: argMobile },
    { id: 'popup-banner-mobile',arg: argMobile },
  ].filter(function (s) { return !!document.getElementById(s.id); });

  if (SLOTS.length === 0) return;

  function run() {
    if (typeof window.PartnersCoupang === 'undefined' || !window.PartnersCoupang.G) {
      setTimeout(run, 150);
      return;
    }

    // G() 호출 전 body 스냅샷 (1회)
    var before = [].slice.call(document.body.children);

    // new 키워드로 생성자 호출 (필수)
    SLOTS.forEach(function (s) {
      try {
        new window.PartnersCoupang.G({
          id: s.arg,
          subId: null,
          trackingCode: window.COUPANG_TRACKING_CODE
        });
      } catch (e) { console.warn('Coupang G:', e); }
    });

    // G()가 비동기이므로 충분히 대기 후 새 요소 이동
    setTimeout(function () {
      var newEls = [].slice.call(document.body.children).filter(function (el) {
        return before.indexOf(el) === -1;
      });
      SLOTS.forEach(function (s, i) {
        var container = document.getElementById(s.id);
        if (container && newEls[i]) container.appendChild(newEls[i]);
      });
    }, 2500);
  }

  var s = document.createElement('script');
  s.src = 'https://ads-partners.coupang.com/g.js';
  s.async = false;
  s.onload = run;
  document.head.appendChild(s);
})();
