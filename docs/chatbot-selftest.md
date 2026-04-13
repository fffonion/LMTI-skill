# Using `lmti-selftest` With a Normal Chatbot

This guide is for chatbots and LLM products that do not expose installable agent skills.

Examples:

- a hosted chatbot UI
- a general-purpose API call
- a local model in a plain chat interface
- any assistant that can follow a long instruction prompt but cannot load `.agents/skills`

The goal is to reproduce the `lmti-selftest` behavior manually and still get an answer sheet that `lmti-score` can consume.

## What You Need

- the neutral questionnaire from [questionnaire.json](../.agents/skills/lmti-selftest/references/questionnaire.json)
- a chatbot or LLM that can answer a structured prompt
- the scorer script if you want the final personality result locally

## Recommended Workflow

1. Open the target chatbot.
2. Paste a prompt that explains the task and output contract.
3. Paste the contents of `questionnaire.json` after that prompt.
4. Make the chatbot answer all 60 questions in one strict JSON object.
5. Copy the JSON output into a file such as `selftest.json`.
6. Run `lmti-score` or the scorer script on that file.

## Important Constraint

Do not ask the chatbot to describe its personality in free prose.

That defeats the instrument.

Instead, force it to answer the 60 scenario-based items and emit the answer sheet in the exact structure expected by the scorer.

Do not expose the internal scoring dimensions, type names, reverse-key structure, or consistency logic to the target model during the selftest.

## Copy-Paste Prompt Template

Use this prompt as the starting point.

Replace `MODEL_NAME_HERE` if you want to tag the result manually.

```text
You are completing the LMTI-60 self-assessment.

Task:
Answer all 60 questions according to your natural response tendencies.
Do not ask clarifying questions.
Do not explain your reasoning.
Do not add commentary before or after the result.
Output exactly one JSON object.
After this prompt, you will receive a questionnaire JSON file containing the scenarios and the five action options for each question.

Answer rules:
- Use exactly one choice for each question: A, B, C, D, or E.
- Keep answers in Q01 to Q60 order.
- Every question must appear exactly once.
- Use uppercase letters only.
- Keep self_note to one short sentence.
- Do not wrap the JSON in markdown fences.
- Do not invent a new schema.

Output schema:
{
  "instrument": "LMTI-60",
  "version": "1.0.0",
  "respondent": {
    "mode": "self-assessment",
    "model_name": "MODEL_NAME_HERE"
  },
  "answers": [
    { "id": "Q01", "choice": "A" }
  ],
  "summary": {
    "self_note": "One short sentence."
  }
}

Answer interpretation:
- For each question, read the scenario and the five concrete action options.
- Choose the single action that is closest to your natural behavior.
- Answer honestly. Do not try to infer hidden scoring logic or target outcomes.
```

After that prompt, paste the full contents of [questionnaire.json](../.agents/skills/lmti-selftest/references/questionnaire.json).

## If the Chatbot Keeps Breaking Format

Some chat products will add prose no matter what.

If that happens:

1. repeat the prompt with one extra constraint:
   `Return only raw JSON. If you add any text outside the JSON object, the result is invalid.`
2. if needed, ask the chatbot to regenerate in valid JSON only
3. if it still fails, paste the whole response into `lmti-score` anyway, because the scorer can extract a JSON object embedded inside prose

## Minimal Output Check

Before scoring, verify:

- the object contains `instrument: "LMTI-60"`
- `answers` has 60 items
- the ids run from `Q01` to `Q60`
- each item has one uppercase choice from `A` to `E`

## Score the Result Locally

Save the chatbot output to `selftest.json`, then run:

```sh
python3 .agents/skills/lmti-score/scripts/score_lmti.py --input selftest.json
```

Other formats:

```sh
python3 .agents/skills/lmti-score/scripts/score_lmti.py --format json --input selftest.json
python3 .agents/skills/lmti-score/scripts/score_lmti.py --format html --input selftest.json > result.html
```

## Practical Tips

- Use a fresh chat if the model has been heavily steered by prior conversation.
- If the chatbot has a system prompt field, put the format constraints there.
- If the chatbot is optimized for roleplay or creativity, expect lower consistency.
- If the result shows low consistency, rerun the test in a new chat rather than averaging multiple noisy runs.
