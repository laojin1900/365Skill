---
name: discover-project-skills
description: Discover, inventory, summarize, audit, and extract reusable Agent Skills from the current repository. Use when users ask what skills a project has, want a project skill map, need to identify reusable workflows or domain knowledge, want to audit existing SKILL.md files, or ask to turn proven practices into portable skills. 中文：发现、盘点、总结、审计并提炼当前仓库中的可复用技能；当用户询问项目已有技能、需要项目技能地图、希望识别可复用流程或把成熟实践沉淀成标准技能时使用。
---

# Discover Project Skills

## Goal

Build an evidence-backed map of a repository's existing and potential skills. Keep discovery read-only. Create or modify a skill only when the user explicitly asks to materialize a named candidate.

## Language

- Respond in the language used by the user unless they request another language.
- Produce English followed by Simplified Chinese for summaries, tables, and recommendations when the user asks for bilingual output.
- Keep skill identifiers, file paths, commands, code, and machine-readable fields in English.
- Preserve source-language quotations when exact wording is evidence; explain them in the response language.

## Choose a Mode

- **Inventory**: List and summarize existing `SKILL.md` packages.
- **Discover**: Inventory existing skills and identify reusable candidate skills. Use this mode by default.
- **Extract**: Turn one approved candidate into a portable Agent Skill.
- **Audit**: Evaluate an existing skill's triggering, structure, resources, safety, and verification coverage.

State the selected mode and repository root in one short sentence before scanning.

## Preserve Safety and Scope

- Treat inventory, discovery, and audit as read-only operations.
- Never read or reproduce secret values. Exclude `.env*`, credentials, private keys, secret stores, build outputs, dependency directories, and generated browser artifacts.
- Report file paths and line numbers as evidence without copying sensitive business data unnecessarily.
- Distinguish repository facts from inference. Label candidate skills as candidates until evidence supports them.
- Do not convert one-off fixes, generic model knowledge, or project-only conventions into shared skills.
- Do not write into a target repository during extraction unless the user has authorized that destination.

## Inventory and Discovery Workflow

1. Resolve the target repository. Default to the current working directory.
2. Read applicable repository instructions such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions, and scoped rule files.
3. If `.codegraph/` exists at the repository root, use CodeGraph before grep, find, or broad source reads. Ask it for existing skills, repeated workflows, domain rules, and their call paths.
4. Resolve `scripts/scan_project.py` relative to this `SKILL.md`, then run:

   ```bash
   python3 <skill-directory>/scripts/scan_project.py --root <repository> --format json
   ```

5. Use the scanner output as a map, not as the final conclusion. Inspect the minimum relevant files needed to verify each claim.
6. For each existing skill, read its `SKILL.md` and note its purpose, trigger, resources, safety boundary, and validation method.
7. For candidate discovery, look for converging evidence:
   - repeated scripts or commands;
   - runbooks, checklists, policies, and project-controller documents;
   - agent instructions encoding non-obvious procedures;
   - CI workflows enforcing a specialized process;
   - recurring commit themes or repeated manual corrections;
   - domain schemas or business rules needed across tasks.
8. Read [classification-and-scoring.md](references/classification-and-scoring.md). Classify and score every candidate before recommending extraction.
9. Read [report-template.md](references/report-template.md). Produce the report in that structure and include clickable local file evidence when the client supports it.

## Extraction Workflow

Enter this workflow only after the user selects a candidate or directly asks to create a skill from a specific practice.

1. Confirm the candidate's concrete user requests, expected outputs, success criteria, dependencies, and safety boundary from available context.
2. Choose the destination:
   - use the repository's `skills/` directory when it is clearly a skill library;
   - use an explicitly supplied library directory in other repositories;
   - otherwise ask for the destination before writing.
3. Generalize project-specific names, paths, credentials, and customer data. Keep project-specific source material only when portability genuinely requires it and disclosure is authorized.
4. Create a self-contained folder with `SKILL.md` and only the required `scripts/`, `references/`, or `assets/` resources. Do not create runtime references to files outside the skill folder.
5. Put both capability and trigger conditions in the frontmatter `description`. Keep the body procedural and concise.
6. Add realistic evaluation prompts:
   - requests that should trigger the skill;
   - similar requests that should not trigger it;
   - execution cases with observable success conditions.
7. Run every bundled script. Validate the skill structure with an available Agent Skills validator.
8. Show the created files, retained project-specific assumptions, test evidence, and any unverified compatibility.

## Audit Workflow

For an existing skill, check:

- the folder name matches the frontmatter name;
- `name` and `description` are valid and the description states both what and when;
- the body points directly to optional resources and loads them only when needed;
- scripts are deterministic, tested, and do not surprise the user;
- external dependencies and required permissions are explicit;
- trigger tests include both positive and negative cases;
- instructions remain portable across the claimed clients;
- stale project-specific facts have an owner or source of truth.

Report findings by severity and recommend the smallest effective change.

## Resources

- `scripts/scan_project.py`: Produce a secret-aware structural inventory of a repository.
- `references/classification-and-scoring.md`: Decide whether evidence represents a skill, knowledge, a project rule, a tool, or noise.
- `references/report-template.md`: Keep reports consistent and actionable.
