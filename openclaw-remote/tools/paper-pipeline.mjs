#!/usr/bin/env node
/**
 * paper-pipeline.mjs — Generate exam content with an accuracy gate.
 *
 * THE PROBLEM (measured 2026-11-15):
 *   The reseller models are 92-100% accurate on clean tasks, but on precise
 *   sparsely-documented facts all 5 failed simultaneously AND disagreed (8/6/8/6/6).
 *   Majority voting cannot fix that. Self-critique made it worse.
 *
 * THE FIX: never ask "is this right?" in the abstract. Attach a CHECK to every
 *   generated item whose type determines how it can be proven:
 *
 *   KIND=compute   -> recompute deterministically (arithmetic, fractions, unit maths)
 *   KIND=lookup    -> must match a supplied source-facts file (curriculum facts)
 *   KIND=language  -> orthography/idiom: check against a whitelist file
 *   KIND=opinion   -> cannot be auto-verified; flagged for human review (待核)
 *
 * Items whose check cannot run are NEVER silently passed — they come back as
 * REVIEW and are marked ⚠️ in output. This is the whole point: an error you know
 * about is cheap; an error you don't know about goes onto a student's paper.
 *
 * USAGE:
 *   node paper-pipeline.mjs --spec spec.json --out result.json
 *   node paper-pipeline.mjs --selftest
 */

import { readFileSync, writeFileSync } from 'node:fs';

// ---------- deterministic checkers ----------

export function evalArithmetic(expr) {
  // Only digits, operators, parens, decimal points, spaces — no eval of arbitrary code.
  const cleaned = String(expr).replace(/[×x]/gi, '*').replace(/÷/g, '/').replace(/,/g, '');
  if (!/^[0-9+\-*/().\s]+$/.test(cleaned)) return { ok: false, reason: 'unsafe or non-numeric expression' };
  try {
    // eslint-disable-next-line no-new-func
    const v = Function('"use strict";return (' + cleaned + ')')();
    if (typeof v !== 'number' || !isFinite(v)) return { ok: false, reason: 'non-finite result' };
    return { ok: true, value: v };
  } catch (e) { return { ok: false, reason: 'parse error: ' + e.message }; }
}

function normNum(s) {
  return String(s).replace(/[^0-9.\-/]/g, '').trim();
}

function fracEqual(a, b) {
  const parse = x => {
    const m = String(x).match(/^(-?\d+)\s*\/\s*(\d+)$/);
    if (m) return Number(m[1]) / Number(m[2]);
    const n = parseFloat(String(x).replace(/[^0-9.\-]/g, ''));
    return isNaN(n) ? null : n;
  };
  const av = parse(a), bv = parse(b);
  if (av === null || bv === null) return false;
  return Math.abs(av - bv) < 1e-9;
}

export function checkCompute(item) {
  // item: { expression, statedAnswer }
  const r = evalArithmetic(item.expression);
  if (!r.ok) return { status: 'REVIEW', reason: 'cannot evaluate: ' + r.reason };
  if (fracEqual(item.statedAnswer, r.value) || Math.abs(parseFloat(normNum(item.statedAnswer)) - r.value) < 1e-9) {
    return { status: 'PASS', computed: r.value };
  }
  return { status: 'FAIL', computed: r.value, stated: item.statedAnswer, reason: 'stated answer != recomputed value' };
}

export function checkLookup(item, facts) {
  // item: { question, statedAnswer, factKey }
  const f = facts?.[item.factKey];
  if (f === undefined) return { status: 'REVIEW', reason: 'no source fact for key "' + item.factKey + '"' };
  const norm = s => String(s).trim().toLowerCase().replace(/\s+/g, '').replace(/[。、，,.]/g, '');
  const accepted = Array.isArray(f) ? f : [f];
  if (accepted.some(a => norm(a) === norm(item.statedAnswer))) return { status: 'PASS', source: accepted };
  return { status: 'FAIL', stated: item.statedAnswer, source: accepted, reason: 'answer not in supplied source facts' };
}

export function checkLanguage(item, whitelist) {
  // item: { statedAnswer, allowedKey }
  const list = whitelist?.[item.allowedKey];
  if (!Array.isArray(list)) return { status: 'REVIEW', reason: 'no whitelist for "' + item.allowedKey + '"' };
  const norm = s => String(s).trim();
  if (list.some(x => norm(x) === norm(item.statedAnswer))) return { status: 'PASS' };
  return { status: 'FAIL', stated: item.statedAnswer, reason: 'not in approved form list', allowed: list };
}

export function checkItem(item, ctx) {
  switch (item.kind) {
    case 'compute': return checkCompute(item);
    case 'lookup': return checkLookup(item, ctx.facts);
    case 'language': return checkLanguage(item, ctx.whitelist);
    case 'opinion': return { status: 'REVIEW', reason: 'open-ended; requires human judgement' };
    default: return { status: 'REVIEW', reason: 'unknown kind "' + item.kind + '"' };
  }
}

// ---------- runner ----------

export function runPipeline(items, ctx) {
  const results = items.map((it, i) => ({ n: it.n ?? i + 1, ...it, check: checkItem(it, ctx) }));
  return {
    total: results.length,
    pass: results.filter(r => r.check.status === 'PASS').length,
    fail: results.filter(r => r.check.status === 'FAIL').length,
    review: results.filter(r => r.check.status === 'REVIEW').length,
    items: results
  };
}

function selftest() {
  const ctx = {
    facts: {
      'mtr.urban.lines': '9',
      'hk.airport.open': '1998'
    },
    whitelist: {
      idiom_poji: ['迫不及待']
    }
  };
  const items = [
    { n: 1, kind: 'compute', expression: '847 * 63', statedAnswer: '53361' },       // PASS
    { n: 2, kind: 'compute', expression: '847 * 63', statedAnswer: '53000' },       // FAIL
    { n: 3, kind: 'compute', expression: '3/4 + 5/6', statedAnswer: '19/12' },      // PASS
    { n: 4, kind: 'lookup', factKey: 'mtr.urban.lines', statedAnswer: '9' },        // PASS
    { n: 5, kind: 'lookup', factKey: 'mtr.urban.lines', statedAnswer: '10' },       // FAIL
    { n: 6, kind: 'lookup', factKey: 'unknown.key', statedAnswer: 'x' },            // REVIEW
    { n: 7, kind: 'language', allowedKey: 'idiom_poji', statedAnswer: '迫不及待' },   // PASS
    { n: 8, kind: 'language', allowedKey: 'idiom_poji', statedAnswer: '迫不急待' },   // FAIL
    { n: 9, kind: 'opinion', statedAnswer: '一段文字' }                              // REVIEW
  ];
  const out = runPipeline(items, ctx);
  console.log('pass=' + out.pass + ' fail=' + out.fail + ' review=' + out.review);
  for (const r of out.items) console.log('  Q' + r.n + ' [' + r.check.status + '] ' + (r.check.reason || ''));
  const expected = { pass: 4, fail: 3, review: 2 };
  const ok = out.pass === expected.pass && out.fail === expected.fail && out.review === expected.review;
  console.log(ok ? 'SELFTEST OK' : 'SELFTEST MISMATCH expected ' + JSON.stringify(expected));
  process.exit(ok ? 0 : 1);
}

const isMain = process.argv[1] && process.argv[1].endsWith('paper-pipeline.mjs');
if (isMain) {
  const args = process.argv.slice(2);
  const argOf = n => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
  if (args.includes('--selftest')) selftest();
  else {
    const specPath = argOf('--spec');
    if (!specPath) { console.error('Usage: node paper-pipeline.mjs --spec spec.json --out result.json | --selftest'); process.exit(2); }
    const spec = JSON.parse(readFileSync(specPath, 'utf8'));
    const out = runPipeline(spec.items, spec.ctx || {});
    const dest = argOf('--out');
    if (dest) { writeFileSync(dest, JSON.stringify(out, null, 1)); console.error('written ' + dest); }
    else console.log(JSON.stringify(out, null, 1));
    console.error(`\nPASS ${out.pass} | FAIL ${out.fail} | REVIEW(待核) ${out.review} of ${out.total}`);
  }
}
