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

  var BANNER_IDS = ['top-banner-pc', 'top-banner-mobile', 'popup-banner-pc', 'popup-banner-mobile'];
  var containers = BANNER_IDS.map(function (id) {
    var el = document.getElementById(id);
    return el ? { id: id, el: el } : null;
  }).filter(Boolean);
  if (containers.length === 0) return;

  var pcId = String(window.COUPANG_BANNER_ID_PC || window.COUPANG_TRACKING_CODE);
  var mobileId = String(window.COUPANG_BANNER_ID_MOBILE || pcId);

  function run() {
    if (typeof window.PartnersCoupang === 'undefined' || !window.PartnersCoupang.G) {
      setTimeout(run, 150);
      return;
    }
    var idNumPc = parseInt(pcId, 10);
    var idNumMobile = parseInt(mobileId, 10);

    // G() 호출 전 body 자식 스냅샷
    var beforePc = [].slice.call(document.body.children);
    try {
      window.PartnersCoupang.G({ id: isNaN(idNumPc) ? pcId : idNumPc, subId: null });
    } catch (e) { console.warn('Coupang G (pc1):', e); }

    var beforePc2 = [].slice.call(document.body.children);
    try {
      window.PartnersCoupang.G({ id: isNaN(idNumPc) ? pcId : idNumPc, subId: null });
    } catch (e) { console.warn('Coupang G (pc2):', e); }

    var beforeMobile = [].slice.call(document.body.children);
    try {
      window.PartnersCoupang.G({ id: isNaN(idNumMobile) ? mobileId : idNumMobile, subId: null });
    } catch (e) { console.warn('Coupang G (m1):', e); }

    var beforeMobile2 = [].slice.call(document.body.children);
    try {
      window.PartnersCoupang.G({ id: isNaN(idNumMobile) ? mobileId : idNumMobile, subId: null });
    } catch (e) { console.warn('Coupang G (m2):', e); }

    setTimeout(function () {
      var afterAll = [].slice.call(document.body.children);
      function newEls(before, after) {
        return after.filter(function (el) { return before.indexOf(el) === -1; });
      }
      var pcEl1    = newEls(beforePc,     beforePc2)[0]     || null;
      var pcEl2    = newEls(beforePc2,    beforeMobile)[0]  || null;
      var mobileEl1 = newEls(beforeMobile, beforeMobile2)[0] || null;
      var mobileEl2 = newEls(beforeMobile2, afterAll)[0]    || null;

      if (containers[0] && pcEl1)    containers[0].el.appendChild(pcEl1);
      if (containers[2] && pcEl2)    containers[2].el.appendChild(pcEl2);
      if (containers[1] && mobileEl1) containers[1].el.appendChild(mobileEl1);
      if (containers[3] && mobileEl2) containers[3].el.appendChild(mobileEl2);
    }, 1500);
  }

  var s = document.createElement('script');
  s.src = 'https://ads-partners.coupang.com/g.js';
  s.async = false;
  s.onload = run;
  document.head.appendChild(s);
})();
