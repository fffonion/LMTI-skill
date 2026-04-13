# Install

LMTI is distributed as two separate skills:

- `lmti-selftest`
- `lmti-score`

Install both.

## Project-Local Install

Use this if you want the skills available only inside one workspace.

```sh
mkdir -p .agents/skills
cp -R /path/to/LLMTI/.agents/skills/lmti-selftest .agents/skills/
cp -R /path/to/LLMTI/.agents/skills/lmti-score .agents/skills/
```

If you prefer symlinks during development:

```sh
mkdir -p .agents/skills
ln -s /path/to/LLMTI/.agents/skills/lmti-selftest .agents/skills/lmti-selftest
ln -s /path/to/LLMTI/.agents/skills/lmti-score .agents/skills/lmti-score
```

## Global Install

Use this if your Codex setup loads skills from `$CODEX_HOME/skills`.

```sh
mkdir -p "$CODEX_HOME/skills"
cp -R /path/to/LLMTI/.agents/skills/lmti-selftest "$CODEX_HOME/skills/"
cp -R /path/to/LLMTI/.agents/skills/lmti-score "$CODEX_HOME/skills/"
```

If `CODEX_HOME` is unset, use your local Codex home directory directly.

Example:

```sh
mkdir -p ~/.codex/skills
cp -R /path/to/LLMTI/.agents/skills/lmti-selftest ~/.codex/skills/
cp -R /path/to/LLMTI/.agents/skills/lmti-score ~/.codex/skills/
```

## Verify Install

Check that both skill folders exist in the target location:

```sh
find .agents/skills -maxdepth 1 -type d | grep lmti
```

Or for global install:

```sh
find "$CODEX_HOME/skills" -maxdepth 1 -type d | grep lmti
```

## Run

1. Invoke `lmti-selftest`.
2. Save or copy the returned JSON.
3. Invoke `lmti-score` with that JSON.

The scorer can also be run directly from the shell:

```sh
python3 /path/to/LLMTI/.agents/skills/lmti-score/scripts/score_lmti.py --input /path/to/selftest.json
```

Other render modes:

```sh
python3 /path/to/LLMTI/.agents/skills/lmti-score/scripts/score_lmti.py --format json --input /path/to/selftest.json
python3 /path/to/LLMTI/.agents/skills/lmti-score/scripts/score_lmti.py --format html --input /path/to/selftest.json > result.html
```

## Troubleshooting

If the skills do not appear:

- confirm the target folder name is exactly `lmti-selftest` and `lmti-score`
- confirm each folder contains a top-level `SKILL.md`
- restart or reload the tool if it caches skill discovery

If scoring fails:

- confirm the selftest output contains exactly `Q01` through `Q60`
- confirm every `choice` is uppercase `A` to `E`
- confirm the JSON was not wrapped in prose before passing it to the script
