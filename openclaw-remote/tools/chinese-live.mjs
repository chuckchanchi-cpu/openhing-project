import { readFileSync, writeFileSync } from 'node:fs';
import { loadBank, checkChineseAnswer } from './chinese-check.mjs';

const KEY = readFileSync('C:/Users/chuck/.openclaw/secrets/ycq-api-key', 'utf8').trim();
const URL = 'https://yuanchengqu.com/v1/chat/completions';
const bank = loadBank();

// Give the model the taught vocabulary so it must choose from it.
const terms = bank.all.filter(e => e.meaning).map(e => `${e.term}（${e.meaning}）`);
const termList = terms.join('、');

const prompt = `你是香港小學中文老師。請用以下「已教詞語」出 6 題填充題。

已教詞語：${termList}

要求：
- 每題一句，句中用 ________ 表示空格
- 答案必須來自上面「已教詞語」其中一個，不可自創
- 只輸出 JSON，不要 markdown：{"items":[{"n":1,"q":"...________...","statedAnswer":"詞語","kind":"language"}]}`;

const r = await fetch(URL, {
  method: 'POST',
  headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'YL-MiniMax-M3',
    messages: [
      { role: 'system', content: '只輸出有效 JSON。' },
      { role: 'user', content: prompt }
    ],
    max_tokens: 4000
  }),
  signal: AbortSignal.timeout(180000)
});
const j = await r.json();
if (!r.ok) { console.error('API error: ' + (j.error?.message || r.status)); process.exit(1); }

const raw = j.choices?.[0]?.message?.content ?? '';
let parsed = null;
try { parsed = JSON.parse(raw.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim()); }
catch { const m = raw.match(/\{[\s\S]*\}/); if (m) try { parsed = JSON.parse(m[0]); } catch {} }
if (!parsed?.items) { console.error('parse failed: ' + raw.slice(0, 300)); process.exit(1); }

console.log('generated ' + parsed.items.length + ' items\n');

let pass = 0, fail = 0, review = 0;
const rows = [];
for (const it of parsed.items) {
  const res = checkChineseAnswer(it.statedAnswer, bank, it.q);
  if (res.status === 'PASS') pass++;
  else if (res.status === 'FAIL') fail++;
  else review++;
  rows.push({
    n: it.n,
    q: it.q,
    answer: it.statedAnswer,
    status: res.status,
    corrected: res.corrected || null,
    meaning: res.meaning || null
  });
  console.log(`Q${it.n} [${res.status}] ${it.statedAnswer}` + (res.corrected ? ` -> ${res.corrected}` : '') +
    `  「${String(it.q).slice(0, 40)}...」`);
}

const summary = { total: parsed.items.length, pass, fail, review, rows };
writeFileSync('C:/Users/chuck/.openclaw/workspace/tools/chinese-live-test.json', JSON.stringify(summary, null, 1), 'utf8');
console.log(`\n=== ${pass} verified | ${fail} corrected | ${review} 待核 ===`);
console.log(fail === 0 && review === 0 ? 'ALL ANSWERS DETERMINISTICALLY VERIFIED' : 'some items need attention');
