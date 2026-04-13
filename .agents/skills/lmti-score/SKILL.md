---
name: lmti-score
description: Score an LMTI-60 selftest result, compute dimension lean, dominant and secondary types, detect inconsistency from cross-reference clusters, and render the output as markdown, JSON, or HTML.
---

# LMTI Score

Use this skill when the user provides LMTI-60 answer output from `lmti-selftest` and wants the personality result.

## Workflow

1. Read `references/framework.json`.
2. Use `scripts/score_lmti.py` to score the result.
3. The input can be:
   - raw JSON from `lmti-selftest`
   - markdown or prose that contains that JSON object
   - a file path whose contents contain that JSON object
4. Prefer running the script with the raw JSON on stdin when the result is pasted in the conversation.
5. Use output format rules:
   - default: `markdown`
   - `json` when the user asks for machine-readable output
   - `html` when the user asks for rendered HTML
6. By default, return the script output directly. Add extra explanation only if the user asks for it.

## Notes

- The scorer reports all four dimension lean scores.
- It always returns one dominant type, but it also returns secondary type affinities because LMTI allows mixed tendencies.
- It computes a consistency score from the 20 three-question cross-reference clusters.
- It also flags straightlining and excessive neutral-answer bias.
- The scorer script supports `--format markdown|json|html`.
