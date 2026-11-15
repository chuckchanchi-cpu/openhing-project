#!/usr/bin/env node
/**
 * chinese-check.mjs — Deterministic verification for Chinese fill-in-the-blank questions.
 *
 * THE GAP THIS CLOSES:
 * Before this, Chinese items could only be checked by "3 models voting". That is the weakest
 * possible check — the MTR incident showed all 5 models can be wrong simultaneously, so
 * agreement proves nothing.
 *
 * Now every 中文 answer is verified against a word bank extracted from the user's OWN
 * curriculum materials (openhing-project/Chinese): 83 terms, 44 with definitions, 70 with
 * real cloze examples. An answer either exists in the taught vocabulary or it doesn't.
 * That is a fact, not an opinion.
 *
 * WHAT IT CHECKS:
 *   1. IN-BANK     the stated answer is a curriculum term            -> PASS
 *   2. TYPO        it is a one-character variant of a bank term      -> FAIL (with the correct form)
 *   3. OUT-OF-BANK not in the taught vocabulary at all               -> 待核 (needs human call)
 *
 * USAGE:
 *   node chinese-check.mjs --answer 執著 --question "他做事非常____"
 *   node chinese-check.mjs --selftest
 */

import { readFileSync } from 'node:fs';

const BANK_PATH = new URL('./chinese-wordbank.json', import.meta.url);

export function loadBank(path = BANK_PATH) {
  const b = JSON.parse(readFileSync(path, 'utf8'));
  return {
    byTerm: new Map(b.entries.map(e => [e.term, e])),
    all: b.entries,
    counts: b.counts
  };
}

/** Character-level edit distance, capped for speed. */
function editDistance(a, b) {
  if (a === b) return 0;
  const m = a.length, n = b.length;
  if (Math.abs(m - n) > 2) return 99;
  let prev = Array.from({ length: n + 1 }, (_, j) => j);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++) {
      cur[j] = Math.min(
        prev[j] + 1,
        cur[j - 1] + 1,
        prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      );
    }
    prev = cur;
  }
  return prev[n];
}

/**
 * @param {string} answer  the model's stated answer
 * @param {object} bank    from loadBank()
 * @param {string} [question] the cloze question, used only for reporting
 */
export function checkChineseAnswer(answer, bank, question = '') {
  const raw = String(answer || '').trim().replace(/[。，、！？\s]/g, '');
  if (!raw) return { status: 'REVIEW', reason: 'empty answer', question };

  // 1. exact curriculum term
  if (bank.byTerm.has(raw)) {
    const e = bank.byTerm.get(raw);
    return {
      status: 'PASS',
      answer: raw,
      meaning: e.meaning || '',
      verifiedBy: 'curriculum word bank',
      sources: e.sources.slice(0, 2),
      question
    };
  }

  // 2. near-miss = almost certainly a typo of a taught term
  let best = null;
  for (const e of bank.all) {
    if (Math.abs(e.term.length - raw.length) > 1) continue;
    const d = editDistance(raw, e.term);
    if (d === 1 && (!best || d < best.d)) best = { term: e.term, d, meaning: e.meaning };
  }
  if (best) {
    return {
      status: 'FAIL',
      answer: raw,
      corrected: best.term,
      meaning: best.meaning,
      reason: `one character off from the taught term 「${best.term}」`,
      question
    };
  }

  // 3. not in the taught vocabulary
  return {
    status: 'REVIEW',
    answer: raw,
    reason: 'not in the curriculum word bank — could be valid but untaught; teacher decides',
    question
  };
}

export function checkItems(items, bank) {
  const results = items.map((it, i) => {
    const ans = it.statedAnswer ?? it.answer ?? '';
    return { n: it.n ?? i + 1, ...it, check: checkChineseAnswer(ans, bank, it.q || it.question || '') };
  });
  return {
    total: results.length,
    pass: results.filter(r => r.check.status === 'PASS').length,
    fail: results.filter(r => r.check.status === 'FAIL').length,
    review: results.filter(r => r.check.status === 'REVIEW').length,
    items: results
  };
}

// ---------- CLI ----------
const isMain = process.argv[1] && process.argv[1].endsWith('chinese-check.mjs');
if (isMain) {
  const args = process.argv.slice(2);
  const argOf = n => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
  const bank = loadBank();

  if (args.includes('--selftest')) {
    const cases = [
      ['執著', 'PASS'],       // real curriculum term
      ['執着', 'FAIL'],       // variant char -> should catch as typo
      ['盲木', 'FAIL'],       // typo of 盲目
      ['量子力學', 'REVIEW'], // not taught -> human call
      ['', 'REVIEW']
    ];
    let ok = true;
    for (const [ans, expect] of cases) {
      const r = checkChineseAnswer(ans, bank);
      const pass = r.status === expect;
      if (!pass) ok = false;
      console.log(`${pass ? 'PASS' : 'FAIL'}  「${ans || '(empty)'}」 -> ${r.status}` +
        (r.corrected ? ` (corrected: ${r.corrected})` : '') + ` [expected ${expect}]`);
    }
    console.log(`\nbank: ${bank.counts.terms} terms, ${bank.counts.withMeaning} with definitions`);
    console.log(ok ? 'SELFTEST OK' : 'SELFTEST MISMATCH');
    process.exit(ok ? 0 : 1);
  }

  const ans = argOf('--answer');
  if (!ans) { console.error('Usage: node chinese-check.mjs --answer 執著 [--question "..."] | --selftest'); process.exit(2); }
  console.log(JSON.stringify(checkChineseAnswer(ans, bank, argOf('--question') || ''), null, 1));
}
