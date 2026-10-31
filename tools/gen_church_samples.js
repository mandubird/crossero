// 교회 이름 넣기 예시 카드 생성: 새해 카드 3장에 '○○교회 청년부'를 넣어 images/cards/church-sample-N.jpg 로 저장한다.
// 사용: NODE_PATH=<playwright-core 위치> node tools/gen_church_samples.js <크롬 실행파일>  (먼저 python3 -m http.server 8911)
const fs = require('fs');
const { chromium } = require('playwright-core');
(async () => {
  const plan = JSON.parse(fs.readFileSync('cards_plan.json', 'utf8')).filter(p => p.set === 'new-year');
  const picks = [0, 1, 5].map(i => plan[i]);
  const b = await chromium.launch({ executablePath: process.argv[2], headless: true });
  const pg = await b.newPage({ viewport: { width: 1200, height: 900 } });
  await pg.goto('http://localhost:8911/verse/', { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.crsStudio && window.crsStudio.renderCard);
  await pg.evaluate(() => { window.checkAuthStatus = () => true; window.crsStudio.state.church = '○○교회 청년부'; });
  for (let i = 0; i < picks.length; i++) {
    const c = picks[i];
    const url = await pg.evaluate(async (a) => window.crsStudio.renderCard(Object.assign({ verse: { ref: a.c.ref, text: a.c.text }, w: 1080, h: 1350, type: 'image/jpeg', q: 0.86 }, a.c.design)), { c });
    fs.writeFileSync(`images/cards/church-sample-${i + 1}.jpg`, Buffer.from(url.split(',')[1], 'base64'));
    const th = await pg.evaluate(async (a) => window.crsStudio.renderCard(Object.assign({ verse: { ref: a.c.ref, text: a.c.text }, w: 360, h: 450, type: 'image/jpeg', q: 0.8, thumb: true }, a.c.design)), { c });
    fs.writeFileSync(`images/cards/church-sample-${i + 1}_t.jpg`, Buffer.from(th.split(',')[1], 'base64'));
    console.log('ok', c.ref);
  }
  await b.close();
})();
