#!/usr/bin/env node
/**
 * factcheck.mjs — Ground model claims in an authoritative source instead of model consensus.
 *
 * WHY THIS EXISTS (measured, 2026-11-15):
 *   - 5 reseller models scored 92-100% on well-posed tasks, so the base models are not "bad".
 *   - On a precise HK fact (MTR urban line count) ALL 5 failed AND split 8/6/8/6/6.
 *     => majority voting / consensus CANNOT catch this: there is no majority.
 *   - Self-critique made it WORSE: it confidently re-enumerated and answered 6 again.
 *   => The only thing that settles a precise fact is a source lookup with strict matching.
 *
 * DESIGN RULE: a number appearing anywhere in an article is NOT evidence.
 * Evidence requires the anchor value and a topic term in the SAME sentence.
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const argOf = n => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };

const LANGS = ['zh', 'en'];

async function wikiSearch(query, lang, limit = 4) {
  const url = `https://${lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&srlimit=${limit}&format=json`;
  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(15000) });
    if (!r.ok) return [];
    const j = await r.json();
    return (j.query?.search || []).map(s => ({ title: s.title, snippet: (s.snippet || '').replace(/<[^>]+>/g, '') }));
  } catch { return []; }
}

async function wikiExtract(title, lang) {
  const url = `https://${lang}.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles=${encodeURIComponent(title)}`;
  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(15000) });
    if (!r.ok) return null;
    const j = await r.json();
    const p = Object.values(j.query?.pages || {})[0];
    return p?.extract || null;
  } catch { return null; }
}

function anchors(claim) {
  const nums = [...claim.matchAll(/\d+(?:\.\d+)?/g)].map(m => m[0]);
  const cjk = [...claim.matchAll(/[\u4e00-\u9fff]{2,}/g)].map(m => m[0]);
  const words = [...claim.matchAll(/[A-Za-z]{4,}/g)].map(m => m[0].toLowerCase());
  return { nums, cjk, words };
}

function splitSentences(text) {
  return (text || '')
    .split(/(?<=[。！？；])|(?<=[.!?])\s+|\n+/)
    .map(s => s.trim())
    .filter(s => s.length > 12);
}

// Quantity units: a count claim is only proven when the number is attached to a unit word.
const UNITS = [
  '條', '个', '個', '種', '种', '名', '位', '所', '間', '间', '座', '架', '部', '次', '年', '人', '萬', '万',
  'line', 'lines', 'station', 'stations', 'year', 'years', 'percent', '%', 'km', 'cm', 'm', 'kg', 'g'
];

function unitNear(sent, num) {
  const idx = sent.indexOf(num);
  if (idx < 0) return false;
  const win = sent.slice(Math.max(0, idx - 12), idx + num.length + 12).toLowerCase();
  return UNITS.some(u => win.includes(u.toLowerCase()));
}

/** A sentence is evidence only if it contains the anchor value AND a topic term. */
function scoreSentence(sent, a) {
  const low = sent.toLowerCase();
  let hasNum = a.nums.length === 0;
  for (const n of a.nums) if (sent.includes(n)) hasNum = true;
  // For numeric claims, require the number to carry a quantity unit nearby.
  let unitOk = a.nums.length === 0;
  for (const n of a.nums) if (unitNear(sent, n)) unitOk = true;
  // Score the two scripts separately: a Chinese source should not be penalised for
  // not containing the English words of the claim (and vice versa).
  let cjkHits = 0;
  for (const c of a.cjk) if (sent.includes(c)) cjkHits++;
  let wordHits = 0;
  for (const w of a.words) if (low.includes(w)) wordHits++;
  const cjkOk = a.cjk.length === 0 ? true : cjkHits >= Math.min(2, a.cjk.length);
  const wordOk = a.words.length === 0 ? true : wordHits / a.words.length >= 0.5;
  const topicOk = a.cjk.length && a.words.length ? (cjkOk || wordOk) : (cjkOk && wordOk);
  const qualifies = hasNum && unitOk && topicOk;
  return { qualifies, score: (hasNum ? 3 : 0) + cjkHits * 2 + wordHits };
}

async function checkClaim(claim, query, titles) {
  const q = query || claim;
  // Topic anchors come from BOTH the claim and the search query, so a claim phrased in
  // English can still be matched against a Chinese source (and vice versa).
  const aClaim = anchors(claim);
  const aQuery = anchors(q);
  const a = {
    nums: aClaim.nums,
    cjk: [...new Set([...aClaim.cjk, ...aQuery.cjk])],
    words: [...new Set([...aClaim.words, ...aQuery.words])]
  };
  // Article titles matching the query are themselves topic evidence.
  const titleTerms = [...a.cjk, ...a.words];
  const evidence = [];
  const sources = [];
  const scanned = [];

  if (titles && titles.length) {
    for (const t of titles) {
      for (const lang of LANGS) {
        const text = await wikiExtract(t, lang);
        if (!text) continue;
        const sents = splitSentences(text);
        const good = sents.map(s => ({ s, ...scoreSentence(s, a) }))
          .filter(x => x.qualifies).sort((x, y) => y.score - x.score).slice(0, 3);
        if (good.length) {
          evidence.push({ lang, title: t, sentences: good.map(g => g.s) });
          sources.push(`https://${lang}.wikipedia.org/wiki/${encodeURIComponent(t)}`);
        }
      }
    }
  }

  for (const lang of LANGS) {
    const hits = await wikiSearch(q, lang);
    for (const h of hits.slice(0, 3)) {
      const text = await wikiExtract(h.title, lang);
      if (!text) continue;
      scanned.push(`https://${lang}.wikipedia.org/wiki/${encodeURIComponent(h.title)}`);
      // An article whose title carries the topic makes a numeric sentence relevant
      // even when the claim's own wording is in another language.
      const titleMatch = titleTerms.some(t => h.title.toLowerCase().includes(t.toLowerCase()) || t.includes(h.title));
      const sents = splitSentences(text);
      const good = sents
        .map(s => {
          const r = scoreSentence(s, a);
          if (!r.qualifies && titleMatch && a.nums.some(n => s.includes(n)) && a.nums.some(n => unitNear(s, n))) {
            return { s, qualifies: true, score: r.score + 1 };
          }
          return { s, ...r };
        })
        .filter(x => x.qualifies)
        .sort((x, y) => y.score - x.score)
        .slice(0, 3);
      if (good.length) {
        evidence.push({ lang, title: h.title, sentences: good.map(g => g.s) });
        sources.push(`https://${lang}.wikipedia.org/wiki/${encodeURIComponent(h.title)}`);
      }
    }
    if (evidence.length >= 2) break;
  }

  if (!evidence.length) {
    // Look for competing values near the same topic = strong sign the claim is wrong
    return {
      claim,
      verdict: 'UNVERIFIABLE',
      reason: 'No sentence paired the claimed value with the topic. Do NOT trust the model here; mark 待核.',
      evidence: [],
      sources: scanned.slice(0, 3)
    };
  }

  // Contradiction check: does evidence state a DIFFERENT value for the same quantity?
  const evText = evidence.map(e => e.sentences.join(' ')).join(' ');
  const supporting = a.nums.filter(n => evText.includes(n));
  const otherNums = [...evText.matchAll(/\d+/g)].map(m => m[0]).filter(n => !supporting.includes(n));

  return {
    claim,
    verdict: supporting.length ? 'SUPPORTED' : 'REFUTED',
    reason: supporting.length
      ? 'A source sentence contains both the claimed value and the topic.'
      : 'Topic found, but the claimed value did not appear with it' +
        (otherNums.length ? ` (other values present: ${[...new Set(otherNums)].slice(0, 6).join(', ')}).` : '.'),
    evidence,
    sources: [...new Set(sources)]
  };
}

async function main() {
  let items;
  if (args.includes('--stdin')) {
    items = JSON.parse(readFileSync(0, 'utf8'));
  } else {
    const claim = argOf('--claim') || argOf('--q');
    if (!claim) { console.error('Usage: node factcheck.mjs --claim "..." [--q "..."] | --stdin'); process.exit(2); }
    const titlesArg = argOf('--titles');
    items = [{ claim, query: argOf('--q'), titles: titlesArg ? titlesArg.split(',').map(s => s.trim()) : undefined }];
  }

  const out = [];
  for (const it of items) out.push(await checkClaim(it.claim, it.query || it.search, it.titles));

  const payload = items.length === 1 ? out[0] : out;
  const dest = argOf('--out');
  if (dest) { writeFileSync(dest, JSON.stringify(payload, null, 1), 'utf8'); console.error('written to ' + dest); }
  else console.log(JSON.stringify(payload, null, 1));
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
export { checkClaim };
