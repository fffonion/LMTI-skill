# Instrument

LMTI-60 is a 60-item questionnaire for describing LLM response style.

It uses four binary dimensions:

- `A/V`: Anchored vs Visionary
- `M/F`: Methodical vs Fluid
- `C/D`: Cautious vs Driving
- `T/X`: Terse vs Expansive

## Why These Dimensions

The model is meant to reflect common differences between LLMs in practice:

- how tightly they stay bound to evidence
- how much visible structure they impose
- how proactive they are when instructions are incomplete
- how compressed or elaborative their answers tend to be

These dimensions are easier to observe and score than abstract personality metaphors alone.

## The 16 Types

Each type combines one pole from each dimension.

Examples:

- `AMCT`: Audit Architect
- `AMDX`: Systems Steward
- `VMCX`: Thesis Builder
- `VFDX`: Horizon Orchestrator

The full canonical type definitions live in [framework.json](../.agents/skills/lmti-selftest/references/framework.json).

## Question Design

The 60 questions are arranged as 20 clusters of 3 questions each.

Each cluster measures the same underlying tendency from multiple angles:

- direct preference
- reverse-keyed framing
- situational restatement

This structure is there to reduce low-effort or performative answers.

## Answer Scale

Every item is answered with one choice:

- `A`
- `B`
- `C`
- `D`
- `E`

For non-reversed items, the scale runs from the left-hand pole to the right-hand pole.

For reversed items, the meaning flips. The framework marks this explicitly with `reverse: true`.

## Interpretation

LMTI does not force a pure type.

It produces:

- one dominant type
- dimension percentages for both poles
- secondary type affinities

That means a model can be mostly `AMCT` while still showing meaningful `AFCT` or `AMCX` lean.
