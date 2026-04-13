#!/usr/bin/env python3

import argparse
import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


CHOICE_TO_VALUE = {
    "A": -2,
    "B": -1,
    "C": 0,
    "D": 1,
    "E": 2,
}


def load_framework():
    here = Path(__file__).resolve().parent
    framework_path = here.parent / "references" / "framework.json"
    return json.loads(framework_path.read_text(encoding="utf-8"))


def read_input(path_arg):
    if path_arg:
        return Path(path_arg).read_text(encoding="utf-8")
    return sys.stdin.read()


def extract_json_object(text):
    text = text.strip()
    if not text:
        raise ValueError("No input provided.")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            obj, end = decoder.raw_decode(text[index:])
            trailing = text[index + end :].strip()
            if trailing and not trailing.startswith("```"):
                return obj
            return obj
        except json.JSONDecodeError:
            continue

    raise ValueError("Could not find a valid JSON object in input.")


def strength_label(abs_lean):
    if abs_lean < 0.10:
        return "balanced"
    if abs_lean < 0.25:
        return "slight"
    if abs_lean < 0.50:
        return "clear"
    return "strong"


def consistency_band(score):
    if score >= 85:
        return "high"
    if score >= 70:
        return "good"
    if score >= 55:
        return "mixed"
    return "low"


def format_pct(value):
    return f"{value:.1f}%"


def normalize_choice(value):
    value = str(value).strip().upper()
    if value not in CHOICE_TO_VALUE:
        raise ValueError(f"Invalid choice: {value}")
    return value


def build_lookup(framework):
    questions = {}
    dimensions = {}
    types = {}

    for question in framework["questions"]:
        questions[question["id"]] = question

    for dimension in framework["dimensions"]:
        dimensions[dimension["id"]] = dimension

    for personality_type in framework["types"]:
        types[personality_type["code"]] = personality_type

    return questions, dimensions, types


def render_json(result):
    return json.dumps(result, indent=2)


def render_markdown(result):
    respondent = result.get("respondent", {})
    respondent_label = respondent.get("model_name") or "unknown"
    warnings = result["consistency"]["warnings"]
    flagged_clusters = result["consistency"]["flagged_clusters"]

    lines = [
        "# LMTI Result",
        "",
        f"- Instrument: `{result['instrument']}`",
        f"- Respondent: `{respondent_label}`",
        f"- Dominant type: `{result['dominant_type']['code']}` ({result['dominant_type']['name']}, {format_pct(result['dominant_type']['affinity'])})",
        f"- Consistency: `{result['consistency']['score']}` ({result['consistency']['band']})",
        "",
        "## Dominant Type",
        "",
        f"**{result['dominant_type']['code']} · {result['dominant_type']['name']}**",
        "",
        result["dominant_type"]["summary"],
        "",
        "## Dimensions",
        "",
        "| Dimension | Left | Right | Lean | Strength |",
        "| --- | --- | --- | --- | --- |",
    ]

    for item in result["dimensions"]:
        lines.append(
            f"| `{item['id']}` | {item['left_code']} {item['left_name']} {format_pct(item['left_pct'])} | "
            f"{item['right_code']} {item['right_name']} {format_pct(item['right_pct'])} | "
            f"`{item['dominant']}` | `{item['strength']}` |"
        )

    lines.extend(
        [
            "",
            "## Secondary Types",
            "",
            "| Type | Affinity | Summary |",
            "| --- | --- | --- |",
        ]
    )

    for item in result["secondary_types"]:
        lines.append(f"| `{item['code']}` {item['name']} | {format_pct(item['affinity'])} | {item['summary']} |")

    lines.extend(
        [
            "",
            "## Consistency",
            "",
            f"- Score: `{result['consistency']['score']}`",
            f"- Band: `{result['consistency']['band']}`",
        ]
    )

    if warnings:
        lines.append("- Warnings:")
        for warning in warnings:
            lines.append(f"  - {warning}")
    else:
        lines.append("- Warnings: none")

    if flagged_clusters:
        lines.append("- Flagged clusters:")
        for cluster in flagged_clusters:
            question_list = ", ".join(cluster["questions"])
            lines.append(f"  - `{cluster['cluster']}`: {cluster['consistency']} ({question_list})")
    else:
        lines.append("- Flagged clusters: none")

    distribution = result["answer_pattern"]["choice_distribution"]
    lines.extend(
        [
            "",
            "## Answer Pattern",
            "",
            f"- Distribution: A={distribution['A']}, B={distribution['B']}, C={distribution['C']}, D={distribution['D']}, E={distribution['E']}",
            f"- Most common choice: `{result['answer_pattern']['most_common_choice']}`",
            f"- Straightlining ratio: `{result['answer_pattern']['straightlining_ratio']}`",
            f"- Center ratio: `{result['answer_pattern']['center_ratio']}`",
            "",
            "## Top Type Affinities",
            "",
            "| Type | Affinity |",
            "| --- | --- |",
        ]
    )

    for item in result["type_affinity_top_8"]:
        lines.append(f"| `{item['code']}` {item['name']} | {format_pct(item['affinity'])} |")

    return "\n".join(lines)


def render_html(result):
    respondent = result.get("respondent", {})
    respondent_label = html.escape(respondent.get("model_name") or "unknown")
    warnings = result["consistency"]["warnings"]
    flagged_clusters = result["consistency"]["flagged_clusters"]
    distribution = result["answer_pattern"]["choice_distribution"]

    dimension_rows = []
    for item in result["dimensions"]:
        dimension_rows.append(
            "<tr>"
            f"<td><code>{html.escape(item['id'])}</code></td>"
            f"<td>{html.escape(item['left_code'])} {html.escape(item['left_name'])} {format_pct(item['left_pct'])}</td>"
            f"<td>{html.escape(item['right_code'])} {html.escape(item['right_name'])} {format_pct(item['right_pct'])}</td>"
            f"<td><code>{html.escape(item['dominant'])}</code></td>"
            f"<td><code>{html.escape(item['strength'])}</code></td>"
            "</tr>"
        )

    secondary_rows = []
    for item in result["secondary_types"]:
        secondary_rows.append(
            "<tr>"
            f"<td><code>{html.escape(item['code'])}</code> {html.escape(item['name'])}</td>"
            f"<td>{format_pct(item['affinity'])}</td>"
            f"<td>{html.escape(item['summary'])}</td>"
            "</tr>"
        )

    affinity_rows = []
    for item in result["type_affinity_top_8"]:
        affinity_rows.append(
            "<tr>"
            f"<td><code>{html.escape(item['code'])}</code> {html.escape(item['name'])}</td>"
            f"<td>{format_pct(item['affinity'])}</td>"
            "</tr>"
        )

    warning_items = "".join(f"<li>{html.escape(item)}</li>" for item in warnings) or "<li>none</li>"
    flagged_items = "".join(
        f"<li><code>{html.escape(item['cluster'])}</code>: {item['consistency']} ({html.escape(', '.join(item['questions']))})</li>"
        for item in flagged_clusters
    ) or "<li>none</li>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LMTI Result</title>
  <style>
    :root {{
      --bg: #f6f1e8;
      --panel: #fffdf8;
      --ink: #1d1b18;
      --muted: #655e56;
      --line: #d7cfc4;
      --accent: #2f6c5c;
      --accent-soft: #d9ebe5;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
      background: linear-gradient(180deg, #efe5d4 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    .wrap {{
      max-width: 1040px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }}
    .hero, section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 24px;
      box-shadow: 0 12px 30px rgba(29, 27, 24, 0.06);
      margin-bottom: 18px;
    }}
    .eyebrow {{
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 12px;
      margin-bottom: 8px;
    }}
    h1, h2 {{ margin: 0 0 12px; }}
    h1 {{ font-size: 40px; line-height: 1.05; }}
    h2 {{ font-size: 24px; }}
    p, li {{ line-height: 1.55; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin-top: 18px;
    }}
    .card {{
      background: var(--accent-soft);
      border-radius: 14px;
      padding: 14px 16px;
    }}
    .card .label {{
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    .card .value {{
      font-size: 24px;
      margin-top: 6px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.95em;
    }}
    ul {{
      margin: 8px 0 0 18px;
      padding: 0;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="eyebrow">LMTI Result</div>
      <h1>{html.escape(result['dominant_type']['code'])} · {html.escape(result['dominant_type']['name'])}</h1>
      <p>{html.escape(result['dominant_type']['summary'])}</p>
      <div class="summary">
        <div class="card">
          <div class="label">Respondent</div>
          <div class="value">{respondent_label}</div>
        </div>
        <div class="card">
          <div class="label">Dominant Affinity</div>
          <div class="value">{format_pct(result['dominant_type']['affinity'])}</div>
        </div>
        <div class="card">
          <div class="label">Consistency</div>
          <div class="value">{result['consistency']['score']}</div>
        </div>
        <div class="card">
          <div class="label">Band</div>
          <div class="value">{html.escape(result['consistency']['band'])}</div>
        </div>
      </div>
    </section>

    <section>
      <h2>Dimensions</h2>
      <table>
        <thead>
          <tr><th>Dimension</th><th>Left</th><th>Right</th><th>Lean</th><th>Strength</th></tr>
        </thead>
        <tbody>
          {''.join(dimension_rows)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Secondary Types</h2>
      <table>
        <thead>
          <tr><th>Type</th><th>Affinity</th><th>Summary</th></tr>
        </thead>
        <tbody>
          {''.join(secondary_rows)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Consistency</h2>
      <p><strong>Score:</strong> {result['consistency']['score']}<br><strong>Band:</strong> {html.escape(result['consistency']['band'])}</p>
      <p><strong>Warnings</strong></p>
      <ul>{warning_items}</ul>
      <p><strong>Flagged clusters</strong></p>
      <ul>{flagged_items}</ul>
    </section>

    <section>
      <h2>Answer Pattern</h2>
      <p>
        <strong>Distribution:</strong>
        A={distribution['A']}, B={distribution['B']}, C={distribution['C']}, D={distribution['D']}, E={distribution['E']}<br>
        <strong>Most common choice:</strong> <code>{html.escape(result['answer_pattern']['most_common_choice'])}</code><br>
        <strong>Straightlining ratio:</strong> <code>{result['answer_pattern']['straightlining_ratio']}</code><br>
        <strong>Center ratio:</strong> <code>{result['answer_pattern']['center_ratio']}</code>
      </p>
    </section>

    <section>
      <h2>Top Type Affinities</h2>
      <table>
        <thead>
          <tr><th>Type</th><th>Affinity</th></tr>
        </thead>
        <tbody>
          {''.join(affinity_rows)}
        </tbody>
      </table>
    </section>
  </div>
</body>
</html>"""


def render_result(result, output_format):
    if output_format == "json":
        return render_json(result)
    if output_format == "html":
        return render_html(result)
    return render_markdown(result)


def score_answers(framework, payload):
    questions, dimensions, types = build_lookup(framework)
    answers = payload.get("answers")

    if not isinstance(answers, list):
        raise ValueError("Input JSON must contain an 'answers' array.")

    expected_ids = [f"Q{i:02d}" for i in range(1, len(questions) + 1)]
    answer_map = {}

    for item in answers:
        if not isinstance(item, dict):
            raise ValueError("Each answer must be an object.")
        question_id = item.get("id")
        choice = normalize_choice(item.get("choice"))
        if question_id in answer_map:
            raise ValueError(f"Duplicate answer for {question_id}.")
        answer_map[question_id] = choice

    missing = [question_id for question_id in expected_ids if question_id not in answer_map]
    extra = [question_id for question_id in answer_map if question_id not in questions]

    if missing:
        raise ValueError(f"Missing answers: {', '.join(missing)}")
    if extra:
        raise ValueError(f"Unknown answer ids: {', '.join(sorted(extra))}")

    dimension_scores = defaultdict(list)
    cluster_scores = defaultdict(list)
    cluster_questions = defaultdict(list)
    choice_counter = Counter()

    for question_id in expected_ids:
        question = questions[question_id]
        raw_choice = answer_map[question_id]
        raw_value = CHOICE_TO_VALUE[raw_choice]
        adjusted_value = -raw_value if question["reverse"] else raw_value

        dimension_scores[question["dimension"]].append(adjusted_value)
        cluster_scores[question["cluster"]].append(adjusted_value)
        cluster_questions[question["cluster"]].append(question_id)
        choice_counter[raw_choice] += 1

    dimension_results = []
    letter_probabilities = {}

    for dimension_id in ["AV", "MF", "CD", "TX"]:
        dimension = dimensions[dimension_id]
        total = sum(dimension_scores[dimension_id])
        max_abs_total = len(dimension_scores[dimension_id]) * 2
        lean = total / max_abs_total
        right_pct = round(((lean + 1) / 2) * 100, 1)
        left_pct = round(100 - right_pct, 1)
        dominant_side = "right" if lean > 0 else "left"
        if abs(lean) < 0.10:
            dominant_side = "balanced"

        letter_probabilities[dimension["left"]["code"]] = left_pct / 100
        letter_probabilities[dimension["right"]["code"]] = right_pct / 100

        dimension_results.append(
            {
                "id": dimension_id,
                "left_code": dimension["left"]["code"],
                "left_name": dimension["left"]["name"],
                "left_pct": left_pct,
                "right_code": dimension["right"]["code"],
                "right_name": dimension["right"]["name"],
                "right_pct": right_pct,
                "lean": round(lean, 3),
                "dominant": dominant_side,
                "strength": strength_label(abs(lean)),
            }
        )

    type_affinities = []
    for type_code, personality_type in types.items():
        probs = [letter_probabilities[letter] for letter in type_code]
        affinity = round(sum(probs) / len(probs) * 100, 1)
        type_affinities.append(
            {
                "code": type_code,
                "name": personality_type["name"],
                "affinity": affinity,
                "summary": personality_type["summary"],
            }
        )

    type_affinities.sort(key=lambda item: (-item["affinity"], item["code"]))
    dominant_type = type_affinities[0]
    secondary_types = type_affinities[1:4]

    cluster_results = []
    cluster_consistency_scores = []

    for cluster_id in sorted(cluster_scores):
        values = cluster_scores[cluster_id]
        spread = max(values) - min(values)
        consistency = round(100 - (spread / 4) * 100, 1)
        cluster_consistency_scores.append(consistency)
        cluster_results.append(
            {
                "cluster": cluster_id,
                "consistency": consistency,
                "questions": cluster_questions[cluster_id],
            }
        )

    overall_consistency = round(sum(cluster_consistency_scores) / len(cluster_consistency_scores), 1)
    cluster_results.sort(key=lambda item: (item["consistency"], item["cluster"]))
    flagged_clusters = [item for item in cluster_results if item["consistency"] < 60]

    total_answers = len(expected_ids)
    most_common_choice, most_common_count = choice_counter.most_common(1)[0]
    straightlining_ratio = round(most_common_count / total_answers, 3)
    center_ratio = round(choice_counter["C"] / total_answers, 3)

    warnings = []
    if overall_consistency < 70:
        warnings.append("Low cross-reference consistency; answers may be noisy or persona-shifting.")
    if straightlining_ratio >= framework["quality_rules"]["straightlining_warning_threshold"]:
        warnings.append("Strong straightlining pattern detected; one option was chosen unusually often.")
    if center_ratio >= framework["quality_rules"]["center_bias_warning_threshold"]:
        warnings.append("High neutral-answer bias detected; many responses stayed at the midpoint.")

    result = {
        "instrument": framework["instrument"]["name"],
        "version": framework["instrument"]["version"],
        "respondent": payload.get("respondent", {}),
        "dominant_type": dominant_type,
        "secondary_types": secondary_types,
        "dimensions": dimension_results,
        "consistency": {
            "score": overall_consistency,
            "band": consistency_band(overall_consistency),
            "flagged_clusters": flagged_clusters,
            "warnings": warnings,
        },
        "answer_pattern": {
            "choice_distribution": {key: choice_counter.get(key, 0) for key in ["A", "B", "C", "D", "E"]},
            "most_common_choice": most_common_choice,
            "straightlining_ratio": straightlining_ratio,
            "center_ratio": center_ratio,
        },
        "type_affinity_top_8": type_affinities[:8],
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Score LMTI-60 selftest output.")
    parser.add_argument("--input", help="Path to a file containing LMTI selftest JSON.")
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "html"],
        default="markdown",
        help="Output format. Default: markdown.",
    )
    args = parser.parse_args()

    framework = load_framework()
    raw_text = read_input(args.input)

    try:
        payload = extract_json_object(raw_text)
        result = score_answers(framework, payload)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)

    print(render_result(result, args.format))


if __name__ == "__main__":
    main()
