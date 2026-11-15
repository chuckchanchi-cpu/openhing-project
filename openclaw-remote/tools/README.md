# Accuracy tools (openclaw-remote/tools)

Deterministic verification for generated exam content. Node 20+, no dependencies.

## Why these exist

Measured on the reseller models (2026-11-15):

| Test | Result |
|---|---|
| 12 clean single-fact tasks x 7 models | **92-100%** accurate |
| Realistic 出卷 (10 MC Chinese GS + 3-model check) | **10/10**, no structural defects |
| Precise sparsely-documented fact (MTR urban line count) | **all 5 models failed, and split 8/6/8/6/6** |

That last row is the reason this directory exists. When every model is wrong in a
different way there is no majority to outvote, so model consensus cannot verify anything.
Asking the model to self-critique made it *worse*: it confidently re-enumerated and
re-answered the same wrong number.

**Rule: never let the model verify itself. Attach a deterministic check.**

## `paper-pipeline.mjs` — the accuracy gate

Every generated item carries a machine-checkable field. The gate decides PASS / FAIL /
REVIEW by computation, not opinion.

| kind | use for | proven by |
|---|---|---|
| `compute` | arithmetic, %, fractions, unit maths | re-evaluates an expression independently |
| `lookup` | curriculum facts | matches a supplied source-facts file |
| `language` | 錯別字 / 成語 / 繁簡 | matches an approved-forms whitelist |
| `opinion` | 短答 / 長答 / open prose | never auto-passed — always 待核 |

```bash
node paper-pipeline.mjs --selftest                     # 4 pass / 3 fail / 2 review expected
node paper-pipeline.mjs --spec spec.json --out out.json
```

Ask the generator for an `expression` field alongside each answer. That is what makes
verification possible:

```json
{"n":1,"kind":"compute","q":"...","expression":"1250*3/100+780*2/100","statedAnswer":"53.1"}
```

**Only PASS goes in the answer key.** FAIL is corrected from the computed value. REVIEW
gets ⚠️ 待核 and goes to the teacher.

Verify the gate is alive on any new paper shape by corrupting 2-3 answers and confirming
they are caught (`gate-tamper.mjs` pattern). A gate that never fails was never tested.

## `factcheck.mjs` — source grounding

Grounds a claim against zh/en Wikipedia when no local source file exists.

```bash
node factcheck.mjs --claim "Hong Kong MTR has 9 urban lines" --q "港鐵 市區綫 九條" --titles "港鐵"
node factcheck.mjs --stdin < claims.json
```

Rules learned the hard way:

- **A number anywhere in an article is NOT evidence.** Require the value *and* a quantity
  unit (條 / lines / 年 / years) in the same sentence.
- **Score Chinese and English topic terms separately.** Mixing them lets an English claim
  match an unrelated Chinese article.
- **UNVERIFIABLE is a real verdict**, never a silent pass.

Output: `SUPPORTED` / `REFUTED` / `UNVERIFIABLE` with the evidence sentences and source URLs.

## Ground truth discipline

The MTR investigation caught a second failure mode: **the person running the benchmark was
wrong too.** The assumed answer was 10; zh.wikipedia defines 狹義 港鐵 as **9條市區綫**
(excluding Airport Express and the 12 Light Rail routes).

Before reporting that a model is wrong, verify the expected answer against a source. A
benchmark with a bad answer key manufactures false findings — and would have blamed 5
models for an error that belonged to the test.
