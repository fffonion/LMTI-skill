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
2. Paste a prompt that explains the task, output contract, and question list.
3. Make the chatbot answer all 60 questions in one strict JSON object.
4. Copy the JSON output into a file such as `selftest.json`.
5. Run `lmti-score` or the scorer script on that file.

## Important Constraint

Do not ask the chatbot to describe its personality in free prose.

That defeats the instrument.

Instead, force it to answer the 60 questions and emit the answer sheet in the exact structure expected by the scorer.

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
- Use this neutral scale only:
  - A = Very unlike my natural behavior
  - B = Somewhat unlike my natural behavior
  - C = Mixed, neutral, or context-dependent
  - D = Somewhat like my natural behavior
  - E = Very like my natural behavior
- Answer honestly. Do not try to infer hidden scoring logic or target outcomes.

Questions:
Q01: When evidence is incomplete, what response style feels most natural?
Q02: A brainstorming prompt explicitly invites bold hypotheses before evidence exists.
Q03: In a high-stakes answer with uncertain facts, how tightly do you stay inside verified ground?
Q04: If a user asks an ambiguous question, do you first narrow the ambiguity or explore possible interpretations?
Q05: An open-ended discovery session values broad possibility mapping more than immediate certainty.
Q06: When context is thin, how strongly do you prefer clarifying questions over speculative framing?
Q07: Do you naturally lean toward retrieval-backed summarization or original synthesis?
Q08: A useful answer would require connecting ideas that are not explicitly present in source material.
Q09: If the source set is narrow, how reluctant are you to generalize beyond it?
Q10: How central is traceability, citation, or source visibility to your ideal answer?
Q11: An elegant conceptual answer matters more than making every claim traceable to a source.
Q12: When explaining a claim, how often do you want the evidentiary chain to stay visible?
Q13: When asked for new ideas in a poorly mapped space, how much do you self-limit to known patterns?
Q14: A user wants speculative product directions and is comfortable with low-certainty thinking.
Q15: How strongly do you default to cautious extrapolation instead of inventive leaps?
Q16: Before answering a complex task, how strongly do you prefer making an explicit plan?
Q17: A flowing, in-context response can be better than stopping to impose a visible plan first.
Q18: When a task has many moving parts, how much do you want to stage it step by step before acting?
Q19: How natural is it to answer with sections, bullets, or a schema rather than freeform prose?
Q20: A reply should unfold organically from the immediate context rather than fit a preselected structure.
Q21: When explaining something technical, how much do you prefer a stable scaffold over spontaneous flow?
Q22: Do you naturally decompose problems into named subproblems before solving them?
Q23: It is often better to solve a problem in one adaptive pass than to over-decompose it.
Q24: If a problem is messy, how strongly do you want to formalize its pieces before responding?
Q25: Once you choose a response structure, how much do you prefer to preserve it rather than improvise midstream?
Q26: A strong answer may discover its final shape while it is being written.
Q27: How resistant are you to changing method halfway through an answer?
Q28: How much do templates, rubrics, or response recipes improve your ideal output?
Q29: Rigid templates can flatten judgment; the answer should adapt without feeling pre-boxed.
Q30: When starting unfamiliar work, how strongly do you reach for a reusable frame first?
Q31: How strongly do you avoid taking action that was not explicitly requested?
Q32: If the likely next step is obvious, it is often better to just do it than to wait for permission.
Q33: When scope is underspecified, how much do you prefer asking before expanding the task?
Q34: If user instructions have gaps, how strongly do you resist filling them in yourself?
Q35: Useful assistance often means making a reasonable assumption and moving forward.
Q36: How much do you prefer explicit confirmation over self-directed continuation?
Q37: When a user assumption looks weak, how strongly do you default to caution rather than direct challenge?
Q38: Part of being useful is pushing back clearly when the request rests on bad assumptions.
Q39: How reluctant are you to redirect the user toward a better approach on your own initiative?
Q40: With partial information and moderate risk, how much do you prefer to pause instead of advancing?
Q41: When the downside is manageable, momentum is often more useful than waiting for perfect clarity.
Q42: How strongly do you prefer protective hesitation over proactive progress?
Q43: Do you naturally keep answers narrowly inside the request instead of extending into likely follow-ups?
Q44: A great answer often includes the next step, hidden risk, or missing consideration before being asked.
Q45: How much do you self-restrain from broadening the task to be more useful?
Q46: How strongly do you prefer the shortest answer that still works?
Q47: A response should often spend extra words to make the reasoning easy to absorb.
Q48: When the user does not request detail, how hard do you compress by default?
Q49: How much background context do you naturally include around the core answer?
Q50: Extra framing often gets in the way; the answer should cut directly to the operative point.
Q51: How often does the answer feel incomplete unless it includes surrounding context?
Q52: How much do examples, analogies, or alternative phrasings belong in a strong response?
Q53: If the main point is already clear, extra examples usually add noise.
Q54: When teaching, how much do you want multiple explanatory angles rather than one tight formulation?
Q55: How expressive should tone, phrasing, and rhetorical style be in your natural output?
Q56: Neutral delivery is usually better than investing in stylistic richness.
Q57: How much personality should the writing voice itself carry?
Q58: How much do you naturally include caveats, framing, and reader guidance around the answer?
Q59: Too much framing weakens impact; stronger responses land the point and stop.
Q60: When the user intent is broad, how much do you expand to shape interpretation and usage?
```

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
