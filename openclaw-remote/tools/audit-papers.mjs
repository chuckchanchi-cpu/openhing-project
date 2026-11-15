#!/usr/bin/env node
/**
 * audit-papers.mjs — Audit existing paper files for answer-key errors.
 *
 * WHY: the repo holds 149 markdown material files. If a 列式 does not evaluate to its
 * answer, a student has already been taught the error. This finds them without regenerating.
 *
 * CRITICAL LESSON (2026-11-15): the first version flagged 4 "errors" in existing Maths
 * papers. ALL FOUR WERE FALSE POSITIVES:
 *   1. 28.4 ÷ 7.8 -> 3.64, paper says 3  (correct: integer part, remainder 5 元)
 *   2. 23 ÷ 6 -> 3.83, paper says 3.8    (correct: rounded to 1 d.p. as asked)
 *   3. 2.7 ÷ 0.3 via LaTeX "\div"        (parse bug; the formula was right)
 *   4. wrong answer line paired with a stale expression
 * A naive recompute-and-compare audit manufactures false alarms and would send the user to
 * "fix" correct papers. Tolerance, rounding, and question-type awareness are mandatory.
 * Every finding is a CLAIM TO VERIFY, never a defect to auto-correct.
 *
 * REAL FORMATS IT HANDLES:
 *   - 答案：**12 杯**                         (bold answer after a 列式/計算 line)
 *   - | 題 | 小數 | 答案 | 驗算 | ... 5÷8=0.625 |   (table verification column)
 *   - **答案：足夠。因為...**                   (prose answers -> skipped, not judged)
 *
 * USAGE:
 *   node audit-papers.mjs --dir <repo>/Maths --out audit.json
 *   node audit-papers.mjs --selftest
 */

import { readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

function evalExpr(expr) {
  let s = String(expr)
    .replace(/\\div/g, '/')
    .replace(/\\times/g, '*')
    .replace(/\\cdot/g, '*')
    .replace(/[×✕xX]/g, '*')
    .replace(/[÷]/g, '/')
    .replace(/[＝]/g, '=')
    .replace(/[，,]/g, '')
    .replace(/\$/g, '')
    .replace(/[^\d+\-*/().\s]/g, ' ')
    .replace(/\s+/g, '');
  if (!s) return null;
  if (!/^[0-9+\-*/().]+$/.test(s)) {
    const m = s.match(/\d+(?:\.\d+)?(?:[+\-*/]\d+(?:\.\d+)?)+/);
    if (m) s = m[0];
    else {
      const single = s.match(/^-?\d+(?:\.\d+)?$/);
      return single ? parseFloat(single[0]) : null;
    }
  }
  try {
    // eslint-disable-next-line no-new-func
    const v = Function('"use strict";return (' + s + ')')();
    return typeof v === 'number' && isFinite(v) ? v : null;
  } catch { return null; }
}

/** Accept exact, integer-part, or rounded matches. */
function compatible(stated, computed) {
  if (computed === null || stated === null) return true;
  const diff = Math.abs(stated - computed);
  if (diff <= Math.max(0.02, Math.abs(computed) * 0.002)) return true;
  if (Math.abs(stated - Math.trunc(computed)) <= 0.0001) return true;
  const dec = (String(stated).split('.')[1] || '').length;
  if (Math.abs(stated - Number(computed.toFixed(dec))) <= 0.0001) return true;
  if (Math.abs(stated - Number(computed.toFixed(1))) <= 0.0001) return true;
  if (Math.abs(stated - Number(computed.toFixed(2))) <= 0.0001) return true;
  return false;
}

function firstNumber(str) {
  const m = String(str).match(/-?\d+(?:\.\d+)?/);
  return m ? parseFloat(m[0]) : null;
}

/** Is the stated answer numeric at all? Prose answers ("足夠。因為...") are not judged. */
function numericAnswer(text) {
  const cleaned = String(text).replace(/\*\*/g, '').trim();
  // must start with an optional label then a number
  const m = cleaned.match(/^(?:最多|最少|大約|約|共|餘)?\s*(-?\d+(?:\.\d+)?)/);
  return m ? parseFloat(m[1]) : null;
}

/** Fraction reduction like "325/1000 = 13/40" is EQUIVALENCE, not division. */
function isFractionReduction(a, b) {
  const parseFrac = s => {
    const m = String(s).trim().match(/^(-?\d+)\s*\/\s*(\d+)$/);
    return m ? { n: parseInt(m[1], 10), d: parseInt(m[2], 10) } : null;
  };
  const fa = parseFrac(a), fb = parseFrac(b);
  if (!fa || !fb || fa.d === 0 || fb.d === 0) return false;
  // cross-multiply: a/b == c/d  <=>  a*d == c*b
  return fa.n * fb.d === fb.n * fa.d;
}

/** Mixed number like "3 8/25" -> 3.32 */
function parseMixed(s) {
  const m = String(s).trim().match(/^(-?\d+)\s+(\d+)\s*\/\s*(\d+)$/);
  if (!m) return null;
  const d = parseInt(m[3], 10);
  if (d === 0) return null;
  return parseInt(m[1], 10) + parseInt(m[2], 10) / d;
}

/**
 * A segment is JUDGEABLE only if it is pure arithmetic/mixed-number with no prose.
 * This is the single most important guard: mixed statements like
 * "58×5 − 70 − 65 = 90 ⚠️ 印刷平均數字待核" or "A≈37.7、B = 39.75" pair unrelated
 * numbers and manufacture false alarms. If there is CJK annotation, skip - not judge.
 */
function judgeable(seg) {
  const s = String(seg).trim();
  if (!s) return false;
  if (/[\u4e00-\u9fff]/.test(s)) return false;          // CJK annotation present
  if (/[→→；;、]/.test(s)) return false;                 // multiple statements
  // must be: arithmetic expr | fraction | mixed number | plain number
  if (/^-?\d+(?:\.\d+)?$/.test(s)) return true;
  if (/^-?\d+\s*\/\s*\d+$/.test(s)) return true;
  if (/^-?\d+\s+\d+\s*\/\s*\d+$/.test(s)) return true;
  if (/^-?\d+(?:\.\d+)?(?:\s*[+\-*/÷×]\s*\d+(?:\.\d+)?)+$/.test(s.replace(/[×]/g, '*').replace(/[÷]/g, '/'))) return true;
  return false;
}

/** Arithmetic where an integer prefix precedes a fraction: "5 + 1÷80 = 5.0125". */
function checkEq(a, b) {
  const sa = String(a).trim(), sb = String(b).trim();

  // skip anything polluted with prose or multiple statements
  if (!judgeable(sa) || !judgeable(sb)) return null;

  // fraction reduction equivalence
  if (isFractionReduction(sa, sb)) return 'ok';

  // mixed-number equivalence: "332/100 = 3 8/25"
  const fa = (sa.match(/^(-?\d+)\s*\/\s*(\d+)$/) || []);
  const mb = parseMixed(sb);
  if (fa.length && mb !== null) {
    const d = parseInt(fa[2], 10);
    if (d !== 0) return compatible(mb, parseInt(fa[1], 10) / d) ? 'ok' : 'bad';
  }
  const ma = parseMixed(sa);
  const fb = (sb.match(/^(-?\d+)\s*\/\s*(\d+)$/) || []);
  if (ma !== null && fb.length) {
    const d = parseInt(fb[2], 10);
    if (d !== 0) return compatible(ma, parseInt(fb[1], 10) / d) ? 'ok' : 'bad';
  }

  // "X + n/d" style mixed numbers
  const mixed = sa.match(/^(-?\d+)\s*\+\s*(\d+)\s*[\/÷]\s*(\d+)$/);
  if (mixed) {
    const val = parseInt(mixed[1], 10) + parseInt(mixed[2], 10) / parseInt(mixed[3], 10);
    const rhs = evalExpr(sb);
    if (rhs !== null) return compatible(rhs, val) ? 'ok' : 'bad';
  }

  const va = evalExpr(sa), vb = evalExpr(sb);
  if (va === null || vb === null) return null;
  return compatible(vb, va) ? 'ok' : 'bad';
}

function extractChecks(md) {
  const out = [];
  const lines = md.split(/\r?\n/);
  let pendingExpr = null;
  let pendingSection = '';

  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;

    // new question boundary resets context
    if (/^(?:\d+[.、)]|#{1,6}\s|\|)/.test(line) && !/計算|驗算/.test(line)) {
      if (/^\d+[.、)]/.test(line)) pendingExpr = null;
    }

    // 1) labelled expression FIRST — a labelled line may contain "a ÷ b = c ÷ d",
    //    and the table matcher must never split it into a partial comparison.
    const exprMatch = line.match(/(?:列\s*式|算\s*式|計\s*算)\s*[:：]\s*(.+)$/);
    if (exprMatch) { pendingExpr = exprMatch[1]; continue; }

    // 2) table verification cell (table rows only).
    //    Walk the FULL "= ... = ..." chain so fraction equivalence is not truncated:
    //    "0.325 = 325/1000 = 13/40" must compare as a chain, not as "325/1000 = 13".
    if (/^\|/.test(line)) {
      // grab cells that contain an '=' between numbers/fractions
      const cellMatches = line.match(/[^|]*=[^|]*/g) || [];
      let found = false;
      for (const cell of cellMatches) {
        const segs = cell.split(/[=＝]/).map(s => s.trim()).filter(Boolean);
        if (segs.length < 2) continue;
        found = true;
        for (let i = 1; i < segs.length; i++) {
          const r = checkEq(segs[i - 1], segs[i]);
          const raw = segs[i - 1] + ' = ' + segs[i];
          if (r === 'bad') {
            out.push({ kind: 'formula', raw: raw.trim(), expected: evalExpr(segs[i - 1]), stated: firstNumber(segs[i]), from: segs[i - 1], to: segs[i] });
          } else if (r === 'ok') out.push({ kind: 'ok', raw: raw.trim() });
        }
      }
      if (found) continue;
    }

    // 3) answer line
    const ansMatch = line.match(/答\s*案\s*[:：]?\s*\**\s*(.+)$/);
    if (ansMatch) {
      const stated = numericAnswer(ansMatch[1]);
      if (stated === null) continue; // prose answer, not machine-judged
      if (!pendingExpr) continue;
      const segs = pendingExpr.split(/[=＝]/).map(s => s.trim());
      let computed = null;
      for (let i = segs.length - 1; i >= 0; i--) {
        const v = evalExpr(segs[i]);
        if (v !== null) { computed = v; break; }
      }
      if (computed === null) continue;
      out.push(compatible(stated, computed)
        ? { kind: 'ok', raw: line, expression: pendingExpr, computed, stated }
        : { kind: 'mismatch', raw: line, expression: pendingExpr, expected: computed, stated });
      pendingExpr = null;
    }
  }
  return out;
}

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name.startsWith('.') || name === 'node_modules') continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (/\.md$/i.test(name)) out.push(p);
  }
  return out;
}

const args = process.argv.slice(2);
const argOf = n => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };

if (args.includes('--selftest')) {
  const cases = [
    ['exact', '1. 列式：3.6 ÷ 0.3 = 36 ÷ 3\n答案：**12 杯**', 0],
    ['latex-div (old false positive)', '1. 列式：$2.7 \\div 0.3 = 9$ 碗\n答案：**9 碗**', 0],
    ['rounded-1dp', '6. 列式：23 ÷ 6\n答案：**3.8 元**', 0],
    ['integer-part + remainder', '5. 列式：28.4 ÷ 7.8\n答案：**最多可買 3 枝**', 0],
    ['table verification cell', '| 1 | 5/8 | **0.625** | 5÷8=0.625 |', 0],
    ['table cell wrong', '| 1 | 5/8 | 0.9 | 5÷8=0.9 |', 1],
    ['fraction reduction (was false positive)', '| 3 | 0.325 | **13/40** | 0.325 = 325/1000 = 13/40 |', 0],
    ['mixed number addition', '| 10 | 5 1/80 | **5.0125** | 5 + 1÷80 = 5.0125 |', 0],
    ['fraction simplify 25/105', '| f | 佔幾分之幾 | **5/21** | 25/105 = 5/21 |', 0],
    ['mixed-number conversion', '| 1 | 332/100 | **3 8/25** | 332/100 = 3 8/25 |', 0],
    ['annotated cell (must skip)', '| a | 58×5 − 70 − 65 = 90 ⚠️ 印刷平均數字待核 |', 0],
    ['multi-statement cell (must skip)', '| b | A≈37.7、B = 39.75、C = 32 |', 0],
    ['genuinely wrong answer', '2. 列式：23.8 × 3 + 9.6\n答案：**72 元**', 1],
    ['prose answer skipped', '1. 列式：12 ÷ 3\n答案：**足夠。因為...**', 0]
  ];
  let ok = true;
  for (const [name, md, expect] of cases) {
    const flagged = extractChecks(md).filter(c => c.kind !== 'ok').length;
    const pass = flagged === expect;
    if (!pass) ok = false;
    console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}: flagged ${flagged}, expected ${expect}`);
  }
  console.log(ok ? 'SELFTEST OK' : 'SELFTEST MISMATCH');
  process.exit(ok ? 0 : 1);
}

const dir = argOf('--dir');
if (!dir) { console.error('Usage: node audit-papers.mjs --dir <path> [--out f.json] | --selftest'); process.exit(2); }

const files = walk(dir);
let okPairs = 0;
const findings = [];

for (const f of files) {
  let md = '';
  try { md = readFileSync(f, 'utf8'); } catch { continue; }
  const checks = extractChecks(md);
  okPairs += checks.filter(c => c.kind === 'ok').length;
  const bad = checks.filter(c => c.kind !== 'ok');
  if (bad.length) findings.push({ file: f.replace(dir, '').replace(/^[\\/]/, ''), count: bad.length, items: bad.slice(0, 5) });
}

const report = { scannedFiles: files.length, verifiedPairs: okPairs, flaggedFiles: findings.length, findings };
const outPath = argOf('--out');
if (outPath) {
  writeFileSync(outPath, JSON.stringify(report, null, 1), 'utf8');
  console.error(`[audit] ${files.length} files | ${okPairs} pairs verified OK | ${findings.length} file(s) flagged`);
  for (const f of findings) console.error(`  ? ${f.file} (${f.count}) -- verify by hand, do not auto-fix`);
} else {
  console.log(JSON.stringify(report, null, 1));
}
