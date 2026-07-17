# 365Skill

[English](README.md) | [简体中文](README.zh-CN.md)

An experimental repository for discovering, validating, and sharing reusable Agent Skills across projects and AI clients.

The repository follows the open `SKILL.md` directory format. Each skill is self-contained, reviewable, testable, and can bundle procedural instructions, deterministic scripts, and references that are loaded only when needed.

## Available Skills

| Skill | Status | Purpose |
|---|---|---|
| [`discover-project-skills`](skills/discover-project-skills/SKILL.md) | Experimental | Inventory existing project skills, discover reusable candidates, and extract approved practices into portable skill packages |
| [`five-step-dev`](skills/five-step-dev/SKILL.md) | Experimental | Risk-graded five-step dev workflow (Research→Plan→Implement→Review→Verify) for business-minded developers: plan approval + evidence-based verification, with model-switch reminders that reserve top-tier models for high-stakes decisions (zh-CN) |
| [`five-step-retro`](skills/five-step-retro/SKILL.md) | Experimental | Self-iteration loop for five-step-dev: run log + six-dimension retrospective + evidence-backed proposals, human-approved upgrades committed to this repo (zh-CN) |

## Publication Model

The public repository is a deterministic export from a private source repository. Publication is deny-by-default: only skill IDs listed in `catalog/publication-policy.json` are copied to the public mirror. CI rejects unlisted skill directories, evals, catalog entries, and references.

## Quick Start

### Install in Codex

Clone this repository, then link the skill into your personal skills directory:

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/discover-project-skills" ~/.codex/skills/discover-project-skills
```

Invoke it from a new task in any project:

```text
Use $discover-project-skills to scan the current repository and produce a project skill map.
```

Run only the structural scanner:

```bash
python3 skills/discover-project-skills/scripts/scan_project.py \
  --root /path/to/project \
  --format markdown
```

### Other Agent Clients

The skill uses the standard `SKILL.md` format. Copy or link `skills/discover-project-skills/` into a personal or project skill directory supported by your client. Client-specific installation adapters will be added as the experiment expands.

## Modes

- **Inventory**: List and summarize existing `SKILL.md` packages.
- **Discover**: Identify repeatable workflows, domain knowledge, and candidate skills. Read-only by default.
- **Extract**: Create a portable skill package after the user explicitly approves a candidate.
- **Audit**: Review an existing skill's triggering, structure, resources, safety boundary, and validation coverage.

## Languages

The repository documentation is available in English and Simplified Chinese. The skill detects the user's language and responds in the same language. It can also produce an English-Chinese report when bilingual output is requested.

Skill identifiers, paths, commands, and machine-readable fields remain in English for cross-client portability.

## Safety Boundary

The scanner does not read or output values from `.env*`, credential files, private keys, or secret stores. It also excludes dependency directories, build artifacts, generated browser data, and version-control internals.

Discovery and audit are read-only. The skill writes files only after the user explicitly requests extraction and supplies or confirms the target directory.

Scan reports can still contain repository paths, filenames, commands, dependency names, skill descriptions, and recent commit subjects. Review generated reports before sharing them outside your organization or publishing them.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m json.tool evals/discover-project-skills/trigger-cases.json >/dev/null
node --test scripts/publication/*.test.mjs
```

Each trigger set contains 10 positive and 10 negative requests in English and Chinese. Structure validation, unit tests, and real-repository scans pass. Independent model-based trigger-rate evaluation remains an upcoming experiment.

## License

This repository is licensed under the [Apache License 2.0](LICENSE).

## References

- [Agent Skills specification](https://github.com/agentskills/agentskills)
- [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- [Superpowers writing-skills](https://github.com/obra/superpowers-skills/tree/main/skills/meta/writing-skills)
