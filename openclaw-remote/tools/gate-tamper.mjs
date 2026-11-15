import { readFileSync, writeFileSync } from 'node:fs';
import { runPipeline } from './tools/paper-pipeline.mjs';

const demo = JSON.parse(readFileSync('C:/Users/chuck/.openclaw/workspace/tools/gate-demo.json', 'utf8'));

// Take the real generated items and silently corrupt 3 stated answers,
// simulating exactly the failure mode the models showed in benchmarking.
const tampered = demo.items.map(it => ({ ...it }));
const idx = [0, 2, 5];
idx.forEach((i, k) => {
  const orig = tampered[i].statedAnswer;
  tampered[i].statedAnswer = String(parseFloat(orig) + (k + 1) * 7); // wrong but plausible
  console.log(`tampered Q${tampered[i].n}: ${orig} -> ${tampered[i].statedAnswer}`);
});

const result = runPipeline(tampered, { facts: {}, whitelist: {} });
console.log('\n=== GATE ON TAMPERED PAPER ===');
console.log(`PASS ${result.pass} | FAIL ${result.fail} | REVIEW ${result.review} of ${result.total}\n`);
for (const it of result.items) {
  const tag = it.check.status === 'PASS' ? 'OK  ' : 'FAIL';
  console.log(`Q${it.n} [${tag}] stated=${it.statedAnswer}` +
    (it.check.status === 'FAIL' ? ` correct=${it.check.computed}` : ''));
}

const caughtAll = result.fail === idx.length;
console.log('\n' + (caughtAll
  ? `✓ GATE WORKS: caught all ${idx.length}/${idx.length} injected errors — none reached the student`
  : `✗ GATE MISSED ${idx.length - result.fail} errors`));
process.exit(caughtAll ? 0 : 1);
