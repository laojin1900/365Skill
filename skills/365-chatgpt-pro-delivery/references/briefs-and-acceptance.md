# Briefs and acceptance / 任务简报与验收

Use only the section matching the selected lane.

## FAST_DELIVERY

```text
Dispatch marker:
Deliverable and audience:
Goal:
Supplied evidence:
Tone, style, dimensions, or format:
Required content:
Must avoid:
Acceptance criteria:
```

For generated visuals, declare the artifact `ILLUSTRATIVE`. Check requested count,
dimensions/aspect ratio, composition, style consistency, unwanted text or logos, obvious
visual defects, and crop safety.

## RESEARCH_DELIVERY

```text
Dispatch marker:
Decision this research supports:
Facts already known:
External facts still needed:
Region and freshness window:
Preferred and excluded sources:
Required comparison or synthesis:
Citation format:
Acceptance criteria:
```

Require source URLs, publication dates, event dates when different, and a clear distinction
between source-backed fact and inference. Codex independently verifies decision-critical
claims against primary sources when practical.

## ENGINEERING_DELIVERY

```text
Dispatch marker:
Delivery mode: PATCH_CANDIDATE | REVIEW_ONLY
Business outcome:
Repository baseline:
Files and symbols supplied:
Callers and contracts supplied:
Runtime/framework versions:
Relevant tests and failures:
Protected behavior to preserve:
Allowed changes:
Forbidden changes:
Required output:
Acceptance criteria:
```

Use `REVIEW_ONLY` when direct callers, runtime contracts, or source files that determine
correctness were not supplied. Never ask for an exact patch against unseen code.

## Codex acceptance checklist

1. Confirm the dispatch marker and inspected-evidence declaration.
2. Separate `DIRECT`, `INFERRED`, `ILLUSTRATIVE`, and `UNVERIFIED` claims.
3. Reject invented files, APIs, commands, metrics, quotations, sources, or test results.
4. Map every accepted item to the user's outcome and constraints.
5. Inspect downloaded archives before extraction; reject traversal, symlinks, credentials,
   generated dependencies, and unrelated files.
6. Run the smallest real local verification appropriate to accepted content.
7. Record accepted unchanged, accepted with local edit, returned, rejected, and unverified
   items.
8. State the actual delivery boundary. Pro consultation never upgrades local work to merged,
   published, deployed, or production-verified.

## Delta correction

```text
The proposal is not yet accepted.

Observed evidence:
- <safe error, failed assertion, or source fact>

Violated constraint:
- <one exact constraint>

Required correction:
- <smallest complete correction>

Return only the delta for unresolved items. Do not rewrite accepted content.
```
