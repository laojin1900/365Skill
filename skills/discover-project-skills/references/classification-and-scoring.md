# Classification and Scoring

## Classify the Asset

| Asset | Use when | Typical home |
|---|---|---|
| Skill | A repeatable task has a trigger, procedure, output, and validation method | Portable `skills/<name>/` package |
| Knowledge | Facts, schemas, terminology, policies, or reference material inform work but do not define a complete task | A skill's `references/` or governed knowledge base |
| Recipe | Several skills are composed for one project or business scenario | Project playbook or `recipes/` catalog |
| Project rule | A convention applies only inside one repository | `AGENTS.md` or the client's project instruction file |
| Tool or MCP | Deterministic capability or external-system access is the main value | Script, CLI, API, plugin, or MCP server |
| Noise | One-off history, generic advice, generated output, or an obsolete workaround | Do not extract |

Prefer the narrowest truthful classification. A document containing useful knowledge is not automatically a skill.

## Score Candidate Skills

Score each dimension from 0 to 2 and cite evidence.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Repetition | One occurrence | Likely recurring | Repeated across tasks, files, or projects |
| Specialized value | Generic model knowledge | Some local nuance | Non-obvious domain or procedural expertise |
| Portability | Tied to one incident | Generalizable with edits | Useful across projects with stable inputs |
| Actionability | Informational only | Partial procedure | Clear trigger, steps, and output |
| Verifiability | Subjective result | Manual review possible | Observable checks or deterministic tests |

- **8–10**: Strong extraction candidate.
- **5–7**: Keep as a candidate; identify missing evidence or constraints.
- **0–4**: Keep as knowledge, a project rule, or no asset.

Record risk separately; do not hide a valuable high-risk candidate by lowering its usefulness score.

## Assign Risk

| Risk | Meaning |
|---|---|
| Low | Read-only analysis or local transformation with no sensitive input |
| Medium | Writes local files, executes project commands, or handles internal data |
| High | Changes external systems, sends messages, publishes, deletes, pays, or touches production data |

High-risk skills need preview, explicit authorization, bounded scope, post-action verification, and a recovery path.

## Evaluate Existing Skills

- **Draft**: Structure exists, but real usage or tests are missing.
- **Reviewed**: Another person checked the content and safety boundary.
- **Verified**: Realistic trigger and execution tests pass on every claimed client.
- **Deprecated**: A replacement exists or the underlying workflow is stale.

Never mark a skill verified solely because its Markdown parses.

## Evidence Priority

1. Current executable scripts, tests, and CI workflows.
2. Current repository instructions and maintained runbooks.
3. Multiple recent examples in project history.
4. A single document or isolated implementation.
5. Inference from names alone.

For strong recommendations, seek at least two independent evidence types. Note when only weak evidence is available.
