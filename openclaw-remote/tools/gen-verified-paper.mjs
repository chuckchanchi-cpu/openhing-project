#!/usr/bin/env node
/**
 * gen-verified-paper.mjs — Generate an exam paper and verify every answer before output.
 *
 * Combines three things that were built separately:
 *   1. the reseller model catalog (7 models, all proven)
 *   2. paper-pipeline.mjs (deterministic PASS/FAIL/REVIEW gate)
 *   3. multi-model cross-check for items that cannot be computed
 *
 * Design rule: an item only reaches the answer key as PASS. Everything else is either
 * corrected from a computed value or surfaced as 待核 for the teacher.
 *
 * USAGE:
 *   node gen-verified-paper.mjs --subject maths --topic "percentages" --count 8
 *   node gen-verified-paper.mjs --subject chinese --topic "成語" --count 10 --out paper.json
 *   node gen-verified-paper.mjs --selftest
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { runPipeline } from './paper-pipeline.mjs';

const KEY_PATH = 'C:/Users/chuck/.openclaw/secrets/ycq-api-key';
const URL = 'https://yuanchengqu.com/v1/chat/completions';

const GEN_MODEL = 'yuanchengqu/YL-MiniMax-M3'.split('/')[1];
const CHECK_MODELS = ['YL-MiniMax-M3', 'YL-DeepSeek-Pro', 'YL-GLM-5.3'];

function loadKey() { return readFileSync(KEY_PATH, 'utf8').trim(); }

async function call(model, messages, maxTokens = 6000) {
  const r = await fetch(URL, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + loadKey(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, messages, max_tokens: maxTokens }),
    signal: AbortSignal.timeout(240000)
  });
  const j = await r.json();
  if (!r.ok) throw new Error((j.error?.message || r.status).toString().slice(0, 200));
  return j.choices?.[0]?.message?.content ?? '';
}

function parseJson(raw) {
  const t = String(raw).replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim();
  try { return JSON.parse(t); } catch {
    const m = t.match(/\{[\s\S]*\}/);
    if (m) { try { return JSON.parse(m[0]); } catch {} }
    return null;
  }
}

// ---------- subject profiles ----------
const PROFILES = {
  maths: {
    checklist: 'Every item must be solvable from the numbers given, with exactly one correct numeric answer.',
    itemFields: '"n", "q", "expression" (pure arithmetic: digits and + - * / only), "statedAnswer" (plain number), "kind":"compute"',
    kind: 'compute'
  },
  chinese: {
    checklist: 'Each item must test a real, correctly-spelled Chinese word or idiom with exactly one correct option.',
    itemFields: '"n", "q", "options" ({"A":"..","B":"..","C":"..","D":".."}), "statedAnswer" (the LETTER), "kind":"opinion"',
    kind: 'opinion'
  },
  general: {
    checklist: 'Each item must test a stable, verifiable fact with exactly one correct option.',
    itemFields: '"n", "q", "options" ({"A":"..","B":"..","C":"..","D":".."}), "statedAnswer" (the LETTER), "kind":"opinion"',
    kind: 'opinion'
  }
};

async function generate(subject, topic, count, level) {
  const prof = PROFILES[subject] || PROFILES.general;
  const prompt = `Create exactly ${count} ${subject === 'chinese' ? 'Chinese' : subject} questions for ${level}.

Topic: ${topic}

Requirements:
- ${prof.checklist}
- Output STRICT JSON only: {"items":[...]}
- Each item has fields: ${prof.itemFields}
- No markdown fences, no commentary.`;

  const raw = await call(GEN_MODEL, [
    { role: 'system', content: 'You output only valid JSON. Be factually precise.' },
    { role: 'user', content: prompt }
  ]);
  const parsed = parseJson(raw);
  if (!parsed?.items?.length) throw new Error('generation did not return valid items');
  return parsed.items.map((it, i) => ({ ...it, n: it.n ?? i + 1, kind: it.kind || prof.kind }));
}

// Cross-model vote for items that cannot be computed (MC questions).
async function crossCheck(item) {
  const opts = item.options || {};
  const body = `Question: ${item.q}\nOptions:\nA. ${opts.A}\nB. ${opts.B}\nC. ${opts.C}\nD. ${opts.D}\n\nWhich single option is correct? Reply with only the letter A, B, C, or D.`;
  const votes = {};
  for (const m of CHECK_MODELS) {
    try {
      const out = await call(m, [
        { role: 'system', content: 'Answer with a single letter only.' },
        { role: 'user', content: body }
      ], 3000);
      votes[m] = (String(out).match(/\b([A-D])\b/)?.[1]) || '?';
    } catch { votes[m] = 'ERR'; }
  }
  const tally = {};
  for (const v of Object.values(votes)) tally[v] = (tally[v] || 0) + 1;
  const top = Object.entries(tally).sort((a, b) => b[1] - a[1])[0] || ['?', 0];
  const unanimous = Object.keys(tally).length === 1;
  const agreesWithStated = String(item.statedAnswer).toUpperCase() === top[0];

  return {
    votes,
    majority: top[0],
    majorityCount: top[1],
    unanimous,
    agreesWithStated,
    // Unanimous agreement with the stated answer is the only thing we promote to PASS.
    status: unanimous && agreesWithStated ? 'CONFIRMED' : 'DISPUTED'
  };
}

async function buildPaper(subject, topic, count, level) {
  const items = await generate(subject, topic, count, level);

  // Stage 1: deterministic gate (compute items get proven arithmetic)
  const gate = runPipeline(items, { facts: {}, whitelist: {} });

  // Stage 2: for non-compute items, cross-check with independent models
  const enriched = [];
  for (const it of gate.items) {
    if (it.kind === 'compute') { enriched.push(it); continue; }
    const cc = await crossCheck(it);
    enriched.push({ ...it, crossCheck: cc });
  }

  // Stage 3: decide what may enter the answer key
  const key = [];
  const review = [];
  for (const it of enriched) {
    if (it.kind === 'compute') {
      if (it.check.status === 'PASS') key.push({ n: it.n, answer: it.statedAnswer, verified: 'computed' });
      else if (it.check.status === 'FAIL') key.push({ n: it.n, answer: String(it.check.computed), verified: 'corrected', originalStated: it.statedAnswer });
      else review.push({ n: it.n, reason: it.check.reason, item: it.q });
    } else {
      const cc = it.crossCheck;
      if (cc?.status === 'CONFIRMED') key.push({ n: it.n, answer: it.statedAnswer, verified: 'unanimous ' + cc.majorityCount + '-model' });
      else review.push({
        n: it.n,
        reason: cc ? `disputed: models voted ${JSON.stringify(cc.votes)} vs stated ${it.statedAnswer}` : 'no cross-check',
        item: it.q
      });
    }
  }

  return {
    meta: { subject, topic, level, generatedAt: new Date().toISOString(), generator: GEN_MODEL, checkers: CHECK_MODELS },
    counts: { total: enriched.length, verified: key.length, review: review.length },
    answerKey: key,
    needsReview: review,
    items: enriched
  };
}

function selftest() {
  // Validates the decision logic without any network call.
  const fake = [
    { n: 1, kind: 'compute', expression: '20*3', statedAnswer: '60', q: 'a' },      // PASS -> key
    { n: 2, kind: 'compute', expression: '20*3', statedAnswer: '50', q: 'b' },      // FAIL -> corrected
    { n: 3, kind: 'compute', expression: 'bad expr !!', statedAnswer: '1', q: 'c' } // REVIEW
  ];
  const gate = runPipeline(fake, { facts: {}, whitelist: {} });
  const ok = gate.pass === 1 && gate.fail === 1 && gate.review === 1;
  console.log('decision logic: pass=' + gate.pass + ' fail=' + gate.fail + ' review=' + gate.review);
  console.log(ok ? 'SELFTEST OK' : 'SELFTEST MISMATCH');
  process.exit(ok ? 0 : 1);
}

const args = process.argv.slice(2);
const argOf = n => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };

if (args.includes('--selftest')) selftest();
else {
  const subject = argOf('--subject') || 'maths';
  const topic = argOf('--topic');
  const count = parseInt(argOf('--count') || '8', 10);
  const level = argOf('--level') || 'Primary 5, Hong Kong curriculum';
  if (!topic) { console.error('Usage: node gen-verified-paper.mjs --subject maths --topic "percentages" --count 8 [--out file.json]'); process.exit(2); }

  console.error(`generating ${count} ${subject} items on "${topic}" with ${GEN_MODEL} ...`);
  buildPaper(subject, topic, count, level).then(res => {
    const dest = argOf('--out');
    const json = JSON.stringify(res, null, 1);
    if (dest) { writeFileSync(dest, json); console.error('written ' + dest); }
    else console.log(json);

    console.error(`\n=== RESULT ===`);
    console.error(`total ${res.counts.total} | verified ${res.counts.verified} | 待核 ${res.counts.review}`);
    for (const k of res.answerKey) console.error(`  Q${k.n} = ${k.answer}  (${k.verified})`);
    for (const r of res.needsReview) console.error(`  Q${r.n} 待核: ${r.reason}`);
  }).catch(e => { console.error('FAILED: ' + e.message); process.exit(1); });
}
