/**
 * 십자가로세로 뱃지 시스템 (로그인 없음, localStorage 기반)
 *
 * "완료" 기준: 정답보기(showAllAnswers)를 열람한 시점.
 * 스스로 다 맞혔는지는 구분하지 않음 - 재방문 유도 장치가 목적.
 * 기존 auth.js / play.html 퍼즐 엔진 로직은 건드리지 않고,
 * play.html의 showAllAnswers() 안에서 recordPuzzleCompletion()만 호출.
 */

const BADGE_STORAGE_KEY = 'crossero_badge_progress';

const BADGE_TIERS = [
  { count: 1, icon: '🏆', label: '첫 퍼즐' },
  { count: 5, icon: '🥉', label: '퍼즐 입문자' },
  { count: 10, icon: '🥈', label: '퍼즐 탐험가' },
  { count: 25, icon: '🥇', label: '성경 마스터' },
  { count: 50, icon: '👑', label: '십자가로세로 정복자' },
];

function getBadgeProgress() {
  try {
    const raw = localStorage.getItem(BADGE_STORAGE_KEY);
    if (!raw) return { completedPuzzles: [] };
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed.completedPuzzles)) return { completedPuzzles: [] };
    return parsed;
  } catch (e) {
    return { completedPuzzles: [] };
  }
}

function saveBadgeProgress(progress) {
  localStorage.setItem(BADGE_STORAGE_KEY, JSON.stringify(progress));
}

// play.html의 showAllAnswers()에서 호출
function recordPuzzleCompletion(quizId) {
  if (!quizId) return;
  const progress = getBadgeProgress();
  if (!progress.completedPuzzles.includes(quizId)) {
    progress.completedPuzzles.push(quizId);
    saveBadgeProgress(progress);
  }
}

function getEarnedBadges(count) {
  return BADGE_TIERS.filter(tier => count >= tier.count);
}

function getNextBadge(count) {
  return BADGE_TIERS.find(tier => count < tier.count) || null;
}

// index.html 등에서 호출: 지정한 컨테이너에 뱃지 위젯 렌더링
function renderBadgeWidget(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const progress = getBadgeProgress();
  const count = progress.completedPuzzles.length;

  if (count === 0) {
    container.style.display = 'none';
    return;
  }

  const earned = getEarnedBadges(count);
  const next = getNextBadge(count);

  const badgeChips = BADGE_TIERS.map(tier => {
    const isEarned = count >= tier.count;
    return `<span style="display:inline-flex; align-items:center; gap:4px; padding:6px 12px; border-radius:20px; font-size:13px; font-weight:600; ${
      isEarned
        ? 'background:#fff9e6; border:1px solid #ffd43b; color:#7a4f00;'
        : 'background:#f1f3f5; border:1px solid #e5e5e5; color:#adb5bd;'
    }">${isEarned ? tier.icon : '🔒'} ${tier.label}</span>`;
  }).join('');

  const nextText = next
    ? `<span style="font-size:12px; color:#888;">다음 뱃지까지 ${next.count - count}개 남았어요</span>`
    : `<span style="font-size:12px; color:#888;">모든 뱃지를 획득했습니다!</span>`;

  container.style.display = 'block';
  container.innerHTML = `
    <div style="max-width:820px; margin:16px auto 0 auto; background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:18px 20px;">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; flex-wrap:wrap; gap:6px;">
        <span style="font-size:15px; font-weight:700; color:#333;">🏆 나의 성경 퍼즐 기록</span>
        <span style="font-size:14px; color:#0073e6; font-weight:700;">${count}개 완료</span>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:10px;">${badgeChips}</div>
      ${nextText}
    </div>
  `;
}

window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('badgeWidget')) {
    renderBadgeWidget('badgeWidget');
  }
});
