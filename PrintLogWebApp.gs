/**
 * [십자가로세로] 인쇄 로그 → 스프레드시트 저장
 *
 * 사용 방법:
 * 1. 스프레드시트 열기: https://docs.google.com/spreadsheets/d/1-165PJsDYWf8Rri24mK-gqXdxyM6GG8Zs-WPa8by--s/edit
 * 2. 확장 프로그램 → Apps Script
 * 3. 이 파일 내용 전체 복사 후 붙여넣기 (기본 Code.gs 덮어쓰기)
 * 4. 저장 → "배포" → "새 배포" → 유형 "웹 앱"
 *    - 설명: 인쇄 로그
 *    - "다음 사용자로 실행": 나
 *    - "액세스 권한": 모든 사용자 (익명 포함)
 * 5. "배포" 클릭 → "웹 앱 URL" 복사
 * 6. play.html 안의 PRINT_LOG_WEB_APP_URL 에 그 URL 붙여넣기
 */

var SPREADSHEET_ID = "1-165PJsDYWf8Rri24mK-gqXdxyM6GG8Zs-WPa8by--s";

function doPost(e) {
  try {
    var params = e.parameter || {};
    var church = params.church || "";
    var memo = params.memo || "";
    var date = params.date || "";
    var puzzle = params.puzzle || "";

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = ss.getSheets()[0];
    // 특정 시트 사용 시: getSheetByName("시트이름") 또는 아래처럼 gid 사용
    // var gid = 567906217; var sheets = ss.getSheets(); for (var i = 0; i < sheets.length; i++) { if (sheets[i].getSheetId() === gid) { sheet = sheets[i]; break; } }
    sheet.appendRow([church, memo, date, puzzle]);

    return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
  } catch (err) {
    return ContentService.createTextOutput("Error: " + err.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
