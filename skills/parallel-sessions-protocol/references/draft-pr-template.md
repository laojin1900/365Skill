# Draft PR board template

Every track opens a draft PR **before writing code**. The body carries three
fixed sections so any session (or the owner) can read the whole board with
one `gh pr list` plus a body view. Keep section titles exact — they are the
machine-greppable contract.

## Template

```markdown
## Claimed scope

- <directory or file this track will touch>
- <another one>

## Claimed numbers

- migration: <NNN or "none">
- decision/ledger entry: <#NNN or "none">

## Current status

<one line — update at each milestone>
```

Chinese projects may use 认领范围 / 占用编号 / 当前状态 as the section
titles; pick one language per repo and keep it consistent, because other
sessions grep for these headings.

## Filled example (feature track)

```markdown
## Claimed scope

- src/lib/logistics/** (new precheck module)
- src/app/api/warehouse/picking/list/ (wire findings into response)

## Claimed numbers

- migration: none
- decision entry: #107

## Current status

T2 server wiring done; T3 UI in review.
```

## Filled example (tiny hotfix track)

```markdown
## Claimed scope

- src/lib/procurement/logistics-parse.ts (+ its test)

## Claimed numbers

- none

## Current status

Fix ready, awaiting merge authorization.
```

## Rules of thumb

- Claim the **narrowest** honest scope. A whole-directory claim blocks other
  tracks from everything under it.
- Update "Current status" when a milestone lands — a stale status is visible
  via the PR's updated-at timestamp, so staleness is at least detectable.
- One PR per track. If a track pivots to a different deliverable, close the
  PR (board self-cleans) and register a new one.
- Draft → Ready is the signal "this track now waits on the owner/merger."
