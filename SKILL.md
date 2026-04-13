---
name: lmti-repo
description: Repository guide for the LMTI multi-skill package. Use when working inside this repo to find the installable skills, human documentation, and scoring implementation quickly.
---

# LMTI Repo

This repository contains two installable skills, not one:

- `.agents/skills/lmti-selftest`
- `.agents/skills/lmti-score`

## Use This Repo

- Use `lmti-selftest` when the task is to answer the LMTI-60 questionnaire and emit strict JSON.
- Use `lmti-score` when the task is to score a prior LMTI answer sheet.

## Where Things Live

- Human docs: `README.md`, `INSTALL.md`, `docs/`
- Canonical instrument: `.agents/skills/lmti-selftest/references/framework.json`
- Canonical scorer: `.agents/skills/lmti-score/scripts/score_lmti.py`

## Editing Rule

Keep human documentation at repo root or in `docs/`.

Keep installable skill folders lean:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `scripts/` only when determinism is required
