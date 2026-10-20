// 샘플 카드 자동 생성: 스튜디오의 crsStudio.renderCard 로 그려 images/cards/*.jpg 로 저장한다.
// 사용: NODE_PATH=<playwright-core 위치> node tools/gen_cards.js <크롬 실행파일> [시작] [개수] [세트필터]
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright-core');
(async () => {
  const exe = process.argv[2], start = +(process.argv[3] || 0), cnt = +(process.argv[4] || 9999), only = process.argv[5] || '';
  const plan = JSON.parse(fs.readFileSync('cards_plan.json', 'utf8')).filter(p => !only || p.set === only).slice(start, start + cnt);
  fs.mkdirSync('images/cards', { recursive: true });
  const b = await chromium.launch({ executablePath: exe, headless: true });
  const pg = await b.newPage({ viewport: { width: 1200, height: 900 } });
  pg.on('pageerror', e => console.log('PAGEERR', e.message.slice(0, 120)));
  await pg.goto('http://localhost:8911/verse/', { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.crsStudio && window.crsStudio.renderCard);
  let ok = 0;
  for (const c of plan) {
    const out = path.join('images/cards', c.file), th = out.replace('.jpg', '_t.jpg');
    if (fs.existsSync(out) && fs.existsSync(th) && !process.env.FORCE) { ok++; continue; }
    try {
      for (const [w, h, f, q] of [[1080, 1350, out, 0.86], [360, 450, th, 0.8]]) {
        const url = await pg.evaluate(async (a) => window.crsStudio.renderCard(Object.assign({ verse: { ref: a.c.ref, text: a.c.text }, w: a.w, h: a.h, type: 'image/jpeg', q: a.q }, a.c.design)), { c, w, h, q });
        fs.writeFileSync(f, Buffer.from(url.split(',')[1], 'base64'));
      }
      ok++; if (ok % 10 === 0) console.log(ok + '/' + plan.length);
    } catch (e) { console.log('FAIL', c.file, e.message.slice(0, 100)); }
  }
  console.log('done', ok);
  await b.close();
})();
