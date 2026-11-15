import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { loadBank, checkChineseAnswer } from './chinese-check.mjs';

const SRC = 'C:/Users/chuck/AppData/Local/Temp/oc-clone-test/Chinese';
const bank = loadBank();

function walk(d, out = []) {
  for (const n of readdirSync(d)) {
    if (n.startsWith('.')) continue;
    const p = join(d, n);
    if (statSync(p).isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const files = walk(SRC);
let pass = 0, fail = 0, review = 0;
const fails = [], reviews = new Set();

for (const f of files.filter(x => x.endsWith('.md'))) {
  const md = readFileSync(f, 'utf8');
  const lines = md.split(/\r?\n/);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!/_{3,}|＿{2,}/.test(line)) continue;
    const window = lines.slice(i, Math.min(i + 3, lines.length)).join(' ');
    const m = window.match(/\*\*([\u4e00-\u9fff]{2,8})\*\*/);
    if (!m) continue;
    const ans = m[1];
    const r = checkChineseAnswer(ans, bank, line.slice(0, 60));
    if (r.status === 'PASS') pass++;
    else if (r.status === 'FAIL') { fail++; fails.push({ file: f.split('Chinese')[1], ans, corrected: r.corrected }); }
    else { review++; reviews.add(ans); }
  }
}

console.log(JSON.stringify({
  bankTerms: bank.counts.terms,
  clozeAnswersFound: pass + fail + review,
  inBank: pass,
  typos: fail,
  unverified: review,
  typoDetail: fails.slice(0, 10),
  unverifiedSample: [...reviews].slice(0, 15)
}, null, 1));
