# Scoring

The canonical scorer is [score_lmti.py](../.agents/skills/lmti-score/scripts/score_lmti.py).

## Output Formats

The scorer supports three output modes:

- `markdown`
- `json`
- `html`

Markdown is the default.

Examples:

```sh
python3 .agents/skills/lmti-score/scripts/score_lmti.py --input /path/to/selftest.json
python3 .agents/skills/lmti-score/scripts/score_lmti.py --format json --input /path/to/selftest.json
python3 .agents/skills/lmti-score/scripts/score_lmti.py --format html --input /path/to/selftest.json > result.html
```

## Choice Values

The script converts answer choices into numeric values:

- `A = -2`
- `B = -1`
- `C = 0`
- `D = 1`
- `E = 2`

If a question is reverse-keyed, the numeric sign is flipped before scoring.

## Dimension Lean

Each dimension has 15 questions.

The scorer:

1. sums all adjusted values for the dimension
2. divides by the maximum possible absolute score
3. converts the result into left and right percentages

This yields a lean from `-1.0` to `1.0`:

- negative means lean toward the left pole
- positive means lean toward the right pole
- near zero means balanced or context-sensitive

## Type Affinity

Type affinity is calculated from the four dimension percentages.

For a type like `AMCT`, the scorer takes the probability-like percentage for:

- `A`
- `M`
- `C`
- `T`

It averages those four values and reports the result as an affinity score.

The highest affinity becomes the dominant type. The next few are kept as secondary tendencies.

## Consistency

Each three-question cluster is scored for internal spread after reverse adjustment.

Low spread means the answers are aligned.

High spread means the model answered similar prompts in contradictory ways.

The scorer reports:

- overall consistency score
- qualitative band
- flagged low-consistency clusters

## Answer-Pattern Warnings

The scorer also checks for:

- straightlining
- excessive midpoint use

These warnings do not invalidate the result, but they do reduce confidence in interpretation.
