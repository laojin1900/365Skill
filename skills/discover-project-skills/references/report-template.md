# Project Skill Map

Write headings and content in the user's language. For requested bilingual output, write English first and Simplified Chinese second in each summary, table heading, recommendation, and action; keep identifiers, paths, and commands unchanged.

## Scope

- Repository: `<absolute path>`
- Mode: `inventory | discover | extract | audit`
- Evidence reviewed: `<instructions, skills, scripts, docs, workflows, history>`
- Limitations: `<unreadable, excluded, missing, or unverified areas>`

## Executive Summary

State the number of existing skills, strong candidates, weaker candidates, project-only rules, and important risks. Separate facts from inference.

## Existing Skills

| Skill | Purpose and trigger | Resources | Maturity | Evidence or issue |
|---|---|---|---|---|
| `<name>` | `<what and when>` | `<scripts/references/assets>` | `<status>` | `<file:line>` |

Use `None found` when appropriate.

## Candidate Skills

| Candidate | Problem solved | Evidence | Score | Risk | Recommendation |
|---|---|---|---:|---|---|
| `<verb-led-name>` | `<repeatable outcome>` | `<at least one path; prefer two evidence types>` | `<0-10>` | `<low/medium/high>` | `<extract / gather evidence / keep local>` |

For every recommended candidate, add:

- Example requests that should trigger it.
- Expected output and validation method.
- What must be generalized or removed before sharing.

## Other Assets

### Knowledge

List reusable facts or references that do not form complete skills.

### Project Rules and Recipes

List repository-only instructions and project-specific skill compositions. Do not recommend publishing them as standalone skills without a portability reason.

### Tools

List deterministic scripts, CLIs, APIs, or MCP candidates that should remain tools or be bundled by a skill.

## Gaps and Risks

List missing owners, stale facts, secret-handling concerns, unsafe write operations, untested scripts, ambiguous triggers, and client compatibility not yet verified.

## Recommended Next Actions

Give at most five ordered actions. Put the highest-value, lowest-ambiguity extraction first. End with a concrete invocation such as: `把候选 1 提炼成技能，输出到 <library>/skills/`.
