import { readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const SRC = 'C:/Users/chuck/AppData/Local/Temp/oc-clone-test/Chinese';
const OUT = 'C:/Users/chuck/.openclaw/workspace/tools/chinese-wordbank.json';

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
const terms = new Map();   // term -> {term, meaning, examples[], sources[]}

function addTerm(term, meaning, example, source) {
  const t = String(term || '').trim();
  if (!/^[\u4e00-\u9fff]{2,8}$/.test(t)) return;
  if (!terms.has(t)) terms.set(t, { term: t, meaning: '', examples: [], sources: [] });
  const e = terms.get(t);
  if (meaning && !e.meaning) e.meaning = String(meaning).trim();
  if (example && !e.examples.includes(example)) e.examples.push(example);
  if (source && !e.sources.includes(source)) e.sources.push(source);
}

// ---------- 1. JS form files: addShortAnswer(form, 'q', 'answer', 'hint') ----------
for (const f of files.filter(x => x.endsWith('.js'))) {
  const src = readFileSync(f, 'utf8');
  const rel = f.split('Chinese')[1].replace(/^[\\/]/, '');

  // match addShortAnswer(form, '<question>', '<answer>', '<hint>')
  const re = /addShortAnswer\s*\(\s*form\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const question = m[1].replace(/\\'/g, "'");
    const answer = m[2].replace(/\\'/g, "'");
    const hint = m[3].replace(/\\'/g, "'");
    // hint looks like "💡 執著 = 堅持不懈"
    const defMatch = hint.match(/=\s*(.+)$/);
    const meaning = defMatch ? defMatch[1].trim() : '';
    addTerm(answer, meaning, question, rel);
  }

  // generic "term": "definition" pairs in JS objects
  const kv = /["']([\u4e00-\u9fff]{2,8})["']\s*:\s*["']([^"']{2,80})["']/g;
  while ((m = kv.exec(src)) !== null) addTerm(m[1], m[2], '', rel);
}

// ---------- 2. Markdown tables: | **term** | pinyin | meaning | usage | ----------
for (const f of files.filter(x => x.endsWith('.md'))) {
  const md = readFileSync(f, 'utf8');
  const rel = f.split('Chinese')[1].replace(/^[\\/]/, '');
  for (const line of md.split(/\r?\n/)) {
    if (!/^\|/.test(line)) continue;
    const cells = line.split('|').map(c => c.trim()).filter(c => c !== '');
    if (cells.length < 2) continue;
    const termMatch = cells[0].match(/^\*\*([\u4e00-\u9fff]{2,8})\*\*$/);
    if (!termMatch) continue;
    const term = termMatch[1];
    const pinyin = cells[1] || '';
    const isPinyin = /^[a-zA-ZüÜāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ\s'’·,0-9]+$/.test(pinyin) && /[a-zA-Z]/.test(pinyin);
    const meaning = cells[2] || '';
    const usage = cells[3] || '';
    addTerm(term, meaning.replace(/\*\*/g, ''), usage.replace(/\*\*/g, ''), rel);
    if (isPinyin) {
      const e = terms.get(term);
      if (e && !e.pinyin) e.pinyin = pinyin.trim();
    }
  }
}

// ---------- 3. Markdown cloze sentences: "…____…" + **answer** ----------
for (const f of files.filter(x => x.endsWith('.md'))) {
  const md = readFileSync(f, 'utf8');
  const rel = f.split('Chinese')[1].replace(/^[\\/]/, '');
  const lines = md.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!/_{3,}|＿{2,}/.test(line)) continue;
    // answer usually appears on a following line as **term**
    const window = lines.slice(i, Math.min(i + 3, lines.length)).join(' ');
    const ans = window.match(/\*\*([\u4e00-\u9fff]{2,8})\*\*/);
    if (ans) addTerm(ans[1], '', line.replace(/^\s*[\d.、)]+\s*/, '').trim(), rel);
  }
}

const entries = [...terms.values()].sort((a, b) => b.examples.length - a.examples.length || a.term.localeCompare(b.term));
const withMeaning = entries.filter(e => e.meaning).length;
const withExample = entries.filter(e => e.examples.length).length;

const bank = {
  generatedAt: new Date().toISOString(),
  source: 'openhing-project/Chinese (JS form files + md tables + cloze sentences)',
  counts: { terms: entries.length, withMeaning, withExample },
  entries
};

writeFileSync(OUT, JSON.stringify(bank, null, 1), 'utf8');
console.log(`terms: ${entries.length} | with definition: ${withMeaning} | with example: ${withExample}`);
console.log('written ' + OUT);
