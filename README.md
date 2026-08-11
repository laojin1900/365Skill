# 365Skill

[English](README.md) | [简体中文](README.zh-CN.md)

An experimental repository for discovering, validating, and sharing reusable Agent Skills across projects and AI clients.

The repository follows the open `SKILL.md` directory format. Each skill is self-contained, reviewable, testable, and can bundle procedural instructions, deterministic scripts, and references that are loaded only when needed.

## Available Skills

| Skill | Status | Purpose |
|---|---|---|
| [`365-chatgpt-pro-delivery`](skills/365-chatgpt-pro-delivery/SKILL.md) | Experimental | Coordinate one bounded ChatGPT Pro contribution with privacy gates, evidence labels, single dispatch, and independent Codex verification |
| [`365-five-step-dev-codex`](skills/365-five-step-dev-codex/SKILL.md) | Experimental | Codex edition of thin, proportional business governance for goal-scoped authorization, risk, evidence, worktree ownership, progress, and closure without duplicating native Codex workflows |
| [`365-five-step-dev-claude`](skills/365-five-step-dev-claude/SKILL.md) | Experimental | Claude Code edition of the same governance layer — graded risk (A/B/C), requirement-collision before work starts, evidence-based closure — refined over ten real-world retrospective cycles |
| [`365-five-step-retro-claude`](skills/365-five-step-retro-claude/SKILL.md) | Experimental | Self-metabolism companion for the Claude Code edition — six-dimension log analysis, git-history cross-checks for silent gaps, upgrades gated on explicit per-proposal approval |
| [`365-session-rotation-maintainer`](skills/365-session-rotation-maintainer/SKILL.md) | Experimental | Rotate one long-running Codex task through a durable checkpoint, one verified successor, preserved worktree ownership, and archive-last recovery |
| [`discover-project-skills`](skills/discover-project-skills/SKILL.md) | Experimental | Inventory existing project skills, discover reusable candidates, and extract approved practices into portable skill packages |
| [`shopify-theme-delivery`](skills/shopify-theme-delivery/SKILL.md) | Experimental | Draft-first Shopify Online Store 2.0 theme delivery with architecture, preservation, remote readback, browser acceptance, and dynamic DOM settling checks |
| [`gws-workspace`](skills/gws-workspace/SKILL.md) | Experimental | Operate Gmail, Calendar, Drive, Sheets, Docs, Slides, Chat, and Tasks through the gws CLI: read-by-default safety gates, helper-command patterns, and a from-zero OAuth setup guide |
| [`gws-weekly-digest`](skills/gws-weekly-digest/SKILL.md) | Experimental | Recurring weekly briefing from mailbox and calendar: last week's mail stats, next seven days of events, markdown digest plus chat summary, strictly read-only |
| [`parallel-sessions-protocol`](skills/parallel-sessions-protocol/SKILL.md) | Experimental | Coordinate any number of parallel sessions on one repository: draft-PR board registration, resource claiming, ledger writes only at merge time, merge discipline, end-of-work teardown registration, three-checkpoint refresh |
| [`project-health-check`](skills/project-health-check/SKILL.md) | Experimental (early) | Read-only cross-project health sweep — CI red streaks, stale PRs, unpushed work, orphan worktrees — rolled into one judgeable report with false-positive guards; findings become follow-up tasks, never in-place fixes |

### Synced from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT)

Verbatim sync of Matt Pocock's production skills — see each skill's `THIRD-PARTY.md` for attribution.

**Engineering**

| [`ask-matt`](skills/ask-matt/SKILL.md) | Stable | Router over the user-invoked skills in this repo — ask which skill or flow fits your situation |
| [`code-review`](skills/code-review/SKILL.md) | Stable | Two-axis review (Standards vs Spec) of changes since a fixed point, in parallel sub-agents |
| [`codebase-design`](skills/codebase-design/SKILL.md) | Stable | Shared vocabulary for designing deep modules: interfaces, seams, testability, AI-navigability |
| [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md) | Stable | Diagnosis loop for hard bugs and performance regressions |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | Stable | Build and sharpen a project's domain model: ubiquitous language and ADRs |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md) | Stable | Relentless interview that also creates docs (ADRs and glossary) as you go |
| [`implement`](skills/implement/SKILL.md) | Stable | Implement a piece of work based on a spec or set of tickets |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Stable | Scan for deepening opportunities, visual HTML report, then grill through the one you pick |
| [`prototype`](skills/prototype/SKILL.md) | Stable | Build a throwaway prototype to answer a design question |
| [`research`](skills/research/SKILL.md) | Stable | Investigate against high-trust primary sources, capture findings as Markdown |
| [`resolving-merge-conflicts`](skills/resolving-merge-conflicts/SKILL.md) | Stable | Resolve an in-progress git merge/rebase conflict |
| [`setup-matt-pocock-skills`](skills/setup-matt-pocock-skills/SKILL.md) | Stable | One-time repo setup for the engineering skills: issue tracker, triage labels, domain docs |
| [`tdd`](skills/tdd/SKILL.md) | Stable | Test-driven development: red-green-refactor, integration tests |
| [`to-spec`](skills/to-spec/SKILL.md) | Stable | Turn the current conversation into a spec and publish it to the issue tracker |
| [`to-tickets`](skills/to-tickets/SKILL.md) | Stable | Break a plan or spec into tracer-bullet tickets with declared blocking edges |
| [`triage`](skills/triage/SKILL.md) | Stable | Move issues/PRs through a triage state machine and write agent-ready briefs |
| [`wayfinder`](skills/wayfinder/SKILL.md) | Stable | Plan huge work as a shared map of decision tickets, resolved one at a time |
| [`wizard`](skills/wizard/SKILL.md) | Stable | Generate an interactive bash wizard for steps only a human can perform |

**Productivity**

| [`grill-me`](skills/grill-me/SKILL.md) | Stable | A relentless interview to sharpen a plan or design |
| [`grilling`](skills/grilling/SKILL.md) | Stable | Grill the user relentlessly about a plan, decision, or idea — stress-test thinking |
| [`handoff`](skills/handoff/SKILL.md) | Stable | Compact the current conversation into a handoff document for another agent |
| [`teach`](skills/teach/SKILL.md) | Stable | Teach the user a new skill or concept within the workspace |
| [`to-questionnaire`](skills/to-questionnaire/SKILL.md) | Stable | Turn an unanswered decision into a questionnaire for someone else |
| [`wait-what`](skills/wait-what/SKILL.md) | Stable | Stop — that last message did not land, re-pitch it |
| [`writing-for-agents`](skills/writing-for-agents/SKILL.md) | Stable | Writing documents for agents: skills, AGENTS.md, CLAUDE.md |

**Misc**

| [`git-guardrails-claude-code`](skills/git-guardrails-claude-code/SKILL.md) | Stable | Claude Code hooks that block dangerous git commands before they execute |
| [`migrate-to-shoehorn`](skills/migrate-to-shoehorn/SKILL.md) | Stable | Migrate tests from `as` assertions to @total-typescript/shoehorn |
| [`scaffold-exercises`](skills/scaffold-exercises/SKILL.md) | Stable | Scaffold exercise directories with sections, problems, solutions, explainers |
| [`setup-pre-commit`](skills/setup-pre-commit/SKILL.md) | Stable | Husky pre-commit hooks with lint-staged, type checking and tests |

**In progress (beta)**

| [`claude-handoff`](skills/claude-handoff/SKILL.md) | Beta | Hand the conversation to a fresh background agent that picks up immediately |
| [`loop-me`](skills/loop-me/SKILL.md) | Beta | Grill yourself into implementable workflow specs over multiple sessions |
| [`setup-ts-deep-modules`](skills/setup-ts-deep-modules/SKILL.md) | Beta | Wire dependency-cruiser into a TypeScript repo for deep modules |
| [`writing-beats`](skills/writing-beats/SKILL.md) | Beta | Shape raw material into a journey of beats, grounding terms first |
| [`writing-fragments`](skills/writing-fragments/SKILL.md) | Beta | Mine raw writing fragments — no structure yet |
| [`writing-shape`](skills/writing-shape/SKILL.md) | Beta | Shape raw material into an article paragraph by paragraph |

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

Install and invoke any of the three core 365 skills in the same way:

```bash
./install.sh 365-five-step-dev-codex codex
./install.sh 365-session-rotation-maintainer codex
./install.sh 365-chatgpt-pro-delivery codex
```

The installer links Codex to this repository checkout. Update the canonical repository
instead of editing the installed copy so the global skill and published source cannot drift.

```text
Use $365-five-step-dev-codex to deliver this business requirement through the 365 five-step method for Codex.
Use $365-session-rotation-maintainer to hand this long-running task to one verified successor.
Use $365-chatgpt-pro-delivery to obtain one Pro review and verify it independently in Codex.
```

For Shopify theme work, link and invoke the delivery skill:

```bash
ln -s "$PWD/skills/shopify-theme-delivery" ~/.codex/skills/shopify-theme-delivery
```

```text
Use $shopify-theme-delivery to plan and validate this draft-theme change before any Shopify write.
```

Client editions use separate skill IDs. This package is the Codex edition; the Claude Code
edition is published as [`365-five-step-dev-claude`](skills/365-five-step-dev-claude/SKILL.md)
(with its companion retro skill, [`365-five-step-retro-claude`](skills/365-five-step-retro-claude/SKILL.md)) —
same governance philosophy, refined independently over ten real-world retrospective cycles on
the Claude Code side, with no invocation collision between the two editions.

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
python3 -m json.tool evals/365-chatgpt-pro-delivery/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-codex/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-codex/workflow-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-codex/regression-cases.json >/dev/null
python3 -m json.tool evals/365-session-rotation-maintainer/trigger-cases.json >/dev/null
python3 -m json.tool evals/discover-project-skills/trigger-cases.json >/dev/null
python3 -m json.tool evals/shopify-theme-delivery/trigger-cases.json >/dev/null
python3 -m json.tool evals/gws-workspace/trigger-cases.json >/dev/null
python3 -m json.tool evals/gws-weekly-digest/trigger-cases.json >/dev/null
python3 -m json.tool evals/parallel-sessions-protocol/trigger-cases.json >/dev/null
python3 -m json.tool evals/project-health-check/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-dev-claude/trigger-cases.json >/dev/null
python3 -m json.tool evals/365-five-step-retro-claude/trigger-cases.json >/dev/null
node --test skills/shopify-theme-delivery/scripts/*.test.mjs
node --test scripts/publication/*.test.mjs
```

Each trigger set contains 10 positive and 10 negative requests in English and Chinese. Structure validation, unit tests, and real-repository scans pass. Independent model-based trigger-rate evaluation remains an upcoming experiment.

## License

This repository is licensed under the [Apache License 2.0](LICENSE).

## References

- [Agent Skills specification](https://github.com/agentskills/agentskills)
- [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- [Superpowers writing-skills](https://github.com/obra/superpowers-skills/tree/main/skills/meta/writing-skills)
