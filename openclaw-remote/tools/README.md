# Accuracy tools (openclaw-remote/tools)

Deterministic verification for generated exam content. Node 20+, no dependencies.

## Why these exist

Measured on the reseller models (2026-11-15):

| Test | Result |
|---|---|
| 12 clean single-fact tasks x 7 models | **92-100%** accurate |
| Realistic 出卷 (10 MC Chinese GS + 3-model check) | **10/10**, no structural defects |
| Precise sparsely-documented fact (MTR urban line count) | **all 5 models failed, and split 8/6/8/6/6** |

That last row is why this directory exists. When every model is wrong in a different way
there is no majority to outvote, so model consensus cannot verify anything. Asking the model
to self-critique made it *worse*: it confidently re-enumerated and re-answered the same
wrong number.

**Rule: never let the model verify itself. Attach a deterministic check.**

## `gen-verified-paper.mjs` — generate + verify in one step

```bash
node gen-verified-paper.mjs --subject maths --topic "percentages" --count 8 --out paper.json
node gen-verified-paper.mjs --selftest
```

Asks the generator for an `expression` alongside every answer, then recomputes it. Items
that cannot be computed (MC questions) require **unanimous agreement from 3 independent
models** before entering the answer key; anything contested is surfaced as 待核.

Live result: 6/6 maths items verified by recomputation, 0 review. Corrupting one answer
was caught and the correct value reported.

## `paper-pipeline.mjs` — the gate itself

| kind | use for | proven by |
|---|---|---|
| `compute` | arithmetic, %, fractions, unit maths | re-evaluates an expression independently |
| `lookup` | curriculum facts | matches a supplied source-facts file |
| `language` | 錯別字 / 成語 / 繁簡 | matches an approved-forms whitelist |
| `opinion` | 短答 / 長答 / open prose | never auto-passed — always 待核 |

```bash
node paper-pipeline.mjs --selftest
node paper-pipeline.mjs --spec spec.json --out out.json
```

**Only PASS goes in the answer key.** FAIL is corrected from the computed value. REVIEW gets
⚠️ 待核 for the teacher.

## `audit-papers.mjs` — check papers that already exist

Recomputes every `列式`/`計算` against its `答案`, and every table verification cell, across
`--dir`. No regeneration needed.

```bash
node audit-papers.mjs --dir . --out audit.json
node audit-papers.mjs --selftest
```

Result on this repo: **149 files scanned, 35 pairs verified, 0 errors.** The existing papers
are arithmetically sound.

### What it refuses to judge — and why that matters most

The first three versions of this auditor flagged 9 "errors" in the existing Maths papers.
**Every single one was a false positive:**

| Flagged | Reality |
|---|---|
| `325/1000 = 13` | fraction **reduction** (`= 13/40`), not division |
| `28.4 ÷ 7.8 = 3` | integer part + remainder `5 元` — correct |
| `23 ÷ 6 = 3.8` | rounded to 1 d.p. as the question asked |
| `$2.7 \div 0.3$` | LaTeX parse bug; the formula was right |
| `5 + 1÷80 = 5.0125` | mixed number |
| `332/100 = 3 8/25` | fraction → mixed conversion |
| `58×5 − 70 − 65 = 90 ⚠️ 印刷...` | annotated cell, unrelated numbers paired |
| `A≈37.7、B = 39.75` | multiple statements in one cell |

Reporting those would have sent a teacher to "fix" correct material days before an exam.

**So: a finding is a CLAIM TO VERIFY, never a defect to auto-correct.** The auditor only
judges pure arithmetic segments; anything containing CJK text, prose, or multiple statements
is skipped. Tolerance covers exact, integer-part, 1–2 d.p. rounding, fraction equivalence,
and mixed numbers. The selftest carries 13 cases — 8 of them these former false positives —
so the regressions cannot come back.

## `factcheck.mjs` — source grounding

Grounds a claim against zh/en Wikipedia when no local source file exists.

```bash
node factcheck.mjs --claim "Hong Kong MTR has 9 urban lines" --q "港鐵 市區綫 九條" --titles "港鐵"
```

- **A number anywhere in an article is NOT evidence.** Require the value *and* a quantity
  unit (條 / lines / 年 / years) in the same sentence.
- **Score Chinese and English topic terms separately**, or an English claim matches an
  unrelated Chinese article.
- **UNVERIFIABLE is a real verdict**, never a silent pass.

## Ground truth discipline

The MTR investigation caught a second failure mode: **the person running the benchmark was
wrong too.** The assumed answer was 10; zh.wikipedia defines 狹義 港鐵 as **9條市區綫**
(excluding Airport Express and the 12 Light Rail routes).

Before reporting that a model is wrong, verify the expected answer against a source. A
benchmark with a bad answer key manufactures false findings — and would have blamed 5
models for an error that belonged to the test.
