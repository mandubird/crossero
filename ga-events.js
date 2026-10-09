/* 십자가로세로 GA4 이벤트 헬퍼 — gtag가 없어도 에러 없이 무시됨 */
(function () {
  function track(name, params) {
    try {
      if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
    } catch (e) {}
  }
  window.crsTrack = track;

  // data-ga="이벤트명" [data-ga-label="..."] 가진 요소 클릭 자동 추적
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('[data-ga]');
    if (!el) return;
    track(el.getAttribute('data-ga'), {
      label: el.getAttribute('data-ga-label') || '',
      page_path: location.pathname
    });
  }, true);

  // 퍼즐 시작/완료 추적 (play.html에서 호출)
  var started = false, completed = false;
  window.crsResetTrack = function () { started = false; completed = false; };

  window.crsTrackProgress = function (grid, solution) {
    var id = new URLSearchParams(location.search).get('id') || 'unknown';
    if (!started) {
      started = true;
      track('puzzle_start', { puzzle_id: id });
    }
    if (completed || !grid || !solution) return;
    var total = 0, correct = 0;
    for (var y = 0; y < solution.length; y++) {
      for (var x = 0; x < solution[y].length; x++) {
        if (solution[y][x] !== null) {
          total++;
          if (grid[y][x] === solution[y][x]) correct++;
        }
      }
    }
    if (total > 0 && correct === total) {
      completed = true;
      track('puzzle_complete', { puzzle_id: id });
    }
  };
})();
