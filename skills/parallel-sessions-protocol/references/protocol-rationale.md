# Design rationale and incident background

## Where this protocol came from

One production repository, one day, seven simultaneous worktrees, eight
merged PRs. Source-code conflicts that day: **zero** — tracks naturally
split by feature domain. Every single collision happened in the
*coordination layer*:

1. **Sequential-number collisions, twice.** Two tracks each claimed the same
   decision-ledger number on the same day. Both records survived (additive
   edits), but the ledger now carries duplicate IDs forever — renumbering
   merged history would break every reference to it. Root cause: the rule
   book governed migration numbers but nobody governed the other sequence.
2. **Shared ledger files edited by four tracks.** A current-task/decisions
   style doc pair collided on merge after merge. GitHub even reported
   MERGEABLE/CLEAN right before a local preview exposed two conflicts —
   the flag lags behind the moving main branch.
3. **`git add -A` swept four uncommitted files from another track** into an
   unrelated commit. Nothing was lost only because the swept content
   happened to be byte-identical with main — luck, not design.
4. **Stale-state questions.** A session asked the owner four decision
   questions from a worksheet another session had already resolved and
   merged hours earlier. Cost: one wasted owner interaction and real
   embarrassment.
5. **Unknown parallel work.** A session planned to start a workstream that
   another session had already begun; the overlap was discovered by accident
   (a worktree listing), not by process.
6. **CI red for 45 consecutive runs across four days, unnoticed.** Every
   session implicitly assumed someone else watched the dashboards.

## Design principles

- **Structural beats disciplinary.** The day's most instructive fact: the
  session that violated the "only the main track edits shared files" rule
  was the same session that had written that rule into the docs hours
  earlier. Discipline fails under load; mechanisms don't. Hence:
  ledger-writes-at-merge-time (serialization removes the conflict class),
  exclusive working directories (removes the sweep class), a self-cleaning
  board (removes the stale-registry class).
- **Zero new systems.** Only git, the GitHub CLI, and files already in the
  repo. Every past attempt at a ceremony-heavy coordination state machine
  in this codebase was eventually retired because the ritual cost outgrew
  the benefit. A rule that costs more than the failure it prevents will be
  skipped exactly when load is highest.
- **Unbounded count, constrained behavior.** Capping "max N parallel
  tracks" was rejected by the owner: the right number depends on the day's
  work. What must be fixed is behavior — and the two bottlenecks no
  protocol removes (the production write path and the owner's own
  review/decision bandwidth) are handled by making the queue *visible* so
  the human throttles intake deliberately.
- **The enforcement vehicle is the auto-loaded project rules file.** A
  protocol only binds sessions if every session reads it without being
  told. Put the operative summary in the file your agent runtime auto-loads
  per project (AGENTS.md / CLAUDE.md equivalents), and keep the full text
  in the project's docs. A skill that is merely *available* governs nobody.

## What deliberately stays out

- **Automated watchdogs / alert bots.** The protocol governs collaboration,
  not monitoring. The start-of-work CI glance raises detection probability
  with session count, but a guarantee needs a scheduled watcher — build
  that as its own small project.
- **Inter-session chat.** Sessions do not read chat channels. The board
  (draft PRs) is the coordination medium; chat webhooks are for humans.
  If your agent platform has direct session-to-session messaging, use it
  for handoffs — but never as a substitute for board registration, because
  messages reach one recipient while the board reaches all.
- **Ledger file splitting.** Per-track journal files with an index were
  considered and rejected while ledger-at-merge-time suffices; splitting
  fragments the record a future reader needs. Revisit only if append
  conflicts become frequent despite serialization.
