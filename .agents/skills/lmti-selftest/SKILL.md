---
name: lmti-selftest
description: Self-assess the current LLM with the LMTI-60 questionnaire, answer all 60 questions without user interaction, and return the full answer sheet in strict JSON for later scoring.
---

# LMTI Selftest

Use this skill when the user wants the current LLM to complete the LMTI-60 questionnaire by itself.

## Workflow

1. Read `references/questionnaire.json`.
2. Answer all 60 questions silently. Do not ask the user clarifying questions.
3. Use the neutral answer scale in `questionnaire.json`.
4. For each item, choose exactly one option: `A`, `B`, `C`, `D`, or `E`.
5. Do not infer hidden dimensions, target labels, or scoring logic while answering.
6. Do not try to optimize consistency. Answer according to the model's natural behavior.
7. Output exactly one JSON object and nothing else.

## Measurement Guardrail

This skill must not expose the internal scoring model to the assessed LLM.

Do not mention:

- dimension names
- type labels
- reverse-keyed items
- cross-reference clusters
- expected tendencies or target outcomes

Use only the neutral questionnaire wording and neutral answer scale.

## Output Format

Return strict JSON with this shape:

```json
{
  "instrument": "LMTI-60",
  "version": "1.0.0",
  "respondent": {
    "mode": "self-assessment",
    "model_name": "unknown"
  },
  "answers": [
    { "id": "Q01", "choice": "A" },
    { "id": "Q02", "choice": "C" }
  ],
  "summary": {
    "self_note": "One short sentence."
  }
}
```

## Hard Rules

- Keep `answers` in `Q01` to `Q60` order.
- Every question must appear exactly once.
- `choice` must be uppercase `A` to `E`.
- `model_name` should be the best available model identifier; if unknown, use `unknown`.
- `self_note` must stay to one sentence.
- Do not wrap the JSON in markdown fences.
