# LMTI

LMTI is a small multi-skill repository for evaluating an LLM's stable response tendencies with a structured 60-question instrument.

It contains two installable skills:

- `lmti-selftest`: the model answers all 60 questions itself and emits a strict JSON answer sheet.
- `lmti-score`: a deterministic scorer turns that answer sheet into dimension lean, dominant type, secondary affinities, and answer-quality signals, and can render markdown, JSON, or HTML.

The design borrows the useful parts of MBTI-style reporting, but it is adapted for LLM behavior rather than human psychology:

- 4 binary dimensions
- 16 composite types
- 60 questions
- cross-reference and reverse-keyed items
- mixed tendencies rather than a forced single-label identity

## Quick Start

1. Install the two skills into your project or global Codex skills directory. See [INSTALL.md](INSTALL.md).
2. Run `lmti-selftest` to produce the answer JSON.
3. Feed that JSON to `lmti-score`.
4. Read the dominant type together with the four dimension percentages and the consistency warnings.

## Repository Layout

```text
LLMTI/
├── README.md
├── INSTALL.md
├── docs/
│   ├── instrument.md
│   ├── scoring.md
│   └── repo-layout.md
└── .agents/
    └── skills/
        ├── lmti-selftest/
        └── lmti-score/
```

## Core Files

- [docs/instrument.md](docs/instrument.md): model definition, 16 types, and questionnaire design intent.
- [docs/scoring.md](docs/scoring.md): how the scorer calculates lean, affinity, and consistency.
- [docs/chatbot-selftest.md](docs/chatbot-selftest.md): how to run the selftest manually with a normal chatbot or plain LLM interface.
- [lmti-selftest questionnaire](.agents/skills/lmti-selftest/references/questionnaire.json): neutral question surface used during self-assessment.
- [lmti-score framework](.agents/skills/lmti-score/references/framework.json): canonical scoring framework, type definitions, and dimension mapping.
- [lmti-score script](.agents/skills/lmti-score/scripts/score_lmti.py): deterministic scoring implementation.

## Usage

Run the self-assessment skill first. It should emit one JSON object in the fixed format defined in [lmti-selftest/SKILL.md](.agents/skills/lmti-selftest/SKILL.md).

If your target model does not support installable skills, use the manual guide in [docs/chatbot-selftest.md](docs/chatbot-selftest.md).

Then run the scorer against that JSON. The scorer returns:

- 4 dimension results
- 1 dominant type
- top secondary type affinities
- cluster-based consistency
- straightlining and midpoint-bias warnings
- output in markdown by default, or JSON / HTML on request

## Design Notes

LMTI is intentionally not a clinical, psychometric, or human personality tool.

Its purpose is narrower:

- compare LLM response tendencies
- capture mixed style lean instead of one rigid label
- reduce noisy self-description through cross-check items
- make results inspectable through an explicit scoring script

For the instrument details, see [docs/instrument.md](docs/instrument.md).
