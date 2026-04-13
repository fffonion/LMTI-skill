# Repo Layout

This repository is intentionally split into two layers.

## Human-Facing Layer

These files explain what the project is and how to install it:

- `README.md`
- `INSTALL.md`
- `docs/`

These are for users and maintainers.

## Skill Layer

The actual installable skills live under:

- `.agents/skills/lmti-selftest`
- `.agents/skills/lmti-score`

Each skill stays minimal:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `scripts/` when determinism matters

This keeps the installed skills lean while letting the repository carry fuller human documentation at the top level.

## Why Not Put READMEs Inside Skill Folders

The skill folders are runtime artifacts.

They should contain only the files needed by the agent:

- concise instructions
- bundled reference data
- deterministic scripts

That keeps context small and avoids dragging human documentation into the active skill footprint.
