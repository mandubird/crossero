/**
 * 십자가로세로 전역 인증 시스템 (auth.js)
 */

// 1. 현재 사용자 권한 상태 확인
function checkAuthStatus() {
    const data = localStorage.getItem('crossero_donor');
    if (!data) return null;

    try {
        const donor = JSON.parse(data);
        const now = new Date().getTime();

        // 기간 만료 체크
        if (now > donor.expiry) {
            localStorage.removeItem('crossero_donor');
            return null;
        }
        return donor;
    } catch (e) {
        return null;
    }
}

// 2. 우측 상단 후원자 배지 UI 업데이트
function updatePremiumUI() {
    const user = checkAuthStatus();
    
    // 기존 배지가 있다면 일단 제거 (중복 방지)
    const existingBadge = document.getElementById('premium-badge');
    if (existingBadge) existingBadge.remove();

    if (user) {
        const badge = document.createElement('div');
        badge.id = "premium-badge";
        // 마스터 관리자인 경우와 일반 후원자 구분 표시 가능
        badge.innerHTML = `🙏 ${user.typeName} (인쇄: ${user.printCount}회)`;
        
        // 스타일 적용
        Object.assign(badge.style, {
            position: 'fixed',
            top: '15px',
            right: '15px',
            background: '#ffd700',
            color: '#000',
            padding: '6px 12px',
            borderRadius: '20px',
            fontSize: '12px',
            fontWeight: 'bold',
            zIndex: '10000',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            border: '1px solid #e6be00'
        });
        
        document.body.appendChild(badge);
    }
}

// 3. 인쇄 수량 차감 로직
function deductPrintCount() {
    const user = checkAuthStatus();
    if (user && user.printCount > 0) {
        user.printCount -= 1;
        localStorage.setItem('crossero_donor', JSON.stringify(user));
        updatePremiumUI(); // UI 즉시 갱신
        return true;
    }
    return false;
}

// 페이지 로드 시 자동으로 배지 업데이트 실행
window.addEventListener('DOMContentLoaded', updatePremiumUI);

// 1. 후원 코드 데이터 정의 (CSV의 내용을 각 배열에 입력하세요)
const VALID_CODES_D1 = ["CRS-D1-X3G6", "CRS-D1-FHVX", "CRS-D1-6KST", "CRS-D1-9SGZ", "CRS-D1-Q6SF", "CRS-D1-GN6R", "CRS-D1-AR6D", "CRS-D1-NBX4", "CRS-D1-UA69","CRS-D1-3MSF", "CRS-D1-RFXZ", "CRS-D1-RUK5", "CRS-D1-T9FN", "CRS-D1-7NB5", "CRS-D1-W3CG", "CRS-D1-MZB7"]; // 1일권
const VALID_CODES_D7 = ["CRS-W7-SGJQ", "CRS-W7-9WRF", "CRS-W7-8DCV", "CRS-W7-CR93", "CRS-W7-928D", "CRS-W7-NE3X", "CRS-W7-4DGY", "CRS-W7-PCEU", "CRS-W7-JEVF", "CRS-W7-95CH", "CRS-W7-B4RY", "CRS-W7-P487", "CRS-W7-7J68", "CRS-W7-Y4KM", "CRS-W7-5SJW", "CRS-W7-6ENQ", "CRS-W7-T8VG", "CRS-W7-JAX4", "CRS-W7-Y53J", "CRS-W7-TS6H"]; // 7일권 (추가됨)
const VALID_CODES_M1 = ["CRS-M1-JZ9B", "CRS-M1-RUPT", "CRS-M1-GYWE", "CRS-M1-M3WZ", "CRS-M1-XRTY", "CRS-M1-49JY", "CRS-M1-2QHB", "CRS-M1-YCUF", "CRS-M1-AFVD", "CRS-M1-XY7B", "CRS-M1-5EK6", "CRS-M1-RESV", "CRS-M1-2FBY", "CRS-M1-UQRN", "CRS-M1-N4ZQ", "CRS-M1-MCZF", "CRS-M1-ESNA", "CRS-M1-FR26", "CRS-M1-SGK7", "CRS-M1-VPMS", "CRS-M1-EZC5"]; // 1개월권

/**
 * 후원 코드 검증 및 데이터 저장 함수
 */
function checkDonationCode(inputCode) {
    const now = new Date();
    let expiryDate = new Date();
    let printCount = 0;
    let typeName = "";

    // [수정] 마스터 코드는 제거하고 리스트 기반으로만 검증합니다.

    // 1. 1일권 (24시간, 5회 인쇄)
    if (VALID_CODES_D1.includes(inputCode)) {
        expiryDate.setHours(now.getHours() + 24);
        printCount = 5;
        typeName = "1일 이용권";
    }
    // 2. 7일권 (7일, 30회 인쇄) - 누락되었던 D7 리스트 검증 추가
    else if (VALID_CODES_D7.includes(inputCode)) {
        expiryDate.setDate(now.getDate() + 7);
        printCount = 30; 
        typeName = "7일 이용권";
    }
    // 3. 1개월권 (30일, 100회 인쇄)
    else if (VALID_CODES_M1.includes(inputCode)) {
        expiryDate.setDate(now.getDate() + 30);
        printCount = 100;
        typeName = "1개월 이용권";
    }
    else {
        alert("유효하지 않은 코드입니다. 코드를 다시 확인해 주세요.");
        return;
    }

    // 2. localStorage 저장 데이터 생성
    const donorInfo = {
        isPremium: true,
        code: inputCode,
        expiry: expiryDate.getTime(),
        printCount: printCount,   // ⭐ remainingPrints → printCount 통일 (play.html과 일치)
        typeName: typeName,
        activatedAt: now.getTime()
    };

    // 로컬 스토리지 저장 (기존 supportData와 이름을 맞추려면 'supportData'로 변경 가능)
    localStorage.setItem('crossero_donor', JSON.stringify(donorInfo));
    
    alert(`인증 성공! [${typeName}]\n인쇄 가능 횟수: ${printCount}회`);
    
    // 메인 페이지 또는 플레이 페이지로 이동
    window.location.href = "index.html"; 
}