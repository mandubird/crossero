// 쇼츠·스토리용 세로 카드(1080×1920) 한 장 생성. 사용: NODE_PATH=<playwright-core> node tools/gen_story_card.js <크롬> <입력.json> <출력.png>
// 입력 json: {"ref":"골로새서 3:13","text":"...","design":{...cards_plan.json 의 design...}}  (먼저 python3 -m http.server 8911)
const fs = require('fs');
const { chromium } = require('playwright-core');
(async () => {
  const [exe, inp, out] = process.argv.slice(2);
  const c = JSON.parse(fs.readFileSync(inp, 'utf8'));
  const b = await chromium.launch({ executablePath: exe, headless: true });
  const pg = await b.newPage({ viewport: { width: 1200, height: 900 } });
  await pg.goto('http://localhost:8911/verse/', { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.crsStudio && window.crsStudio.renderCard);
  const url = await pg.evaluate(async (a) => window.crsStudio.renderCard(Object.assign({ verse: { ref: a.ref, text: a.text }, w: 1080, h: 1920, type: 'image/png' }, a.design)), c);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64'));
  await b.close();
  console.log('ok', out);
})();
