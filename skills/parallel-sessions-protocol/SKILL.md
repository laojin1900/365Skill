---
name: parallel-sessions-protocol
description: Coordinate any number of AI or human dev sessions working the same git repository in parallel — start-of-work registration (a draft PR is the shared board, with claim declarations), resource claiming (sequential numbers, file ownership), ledger-writes-only-at-merge-time, merge discipline (local merge preview, exclusive working directories, no `git add -A`), end-of-work registration (push-or-declare WIP, worktree cleanup, triggered write-backs), and a three-checkpoint awareness refresh. Use when multiple sessions / agents / worktrees develop one repo at the same time; when the user says 多会话并行, 并行轨道, 开工登记, 收工登记, 公告板, 会话撞车, 多个会话同时开发, coordinate parallel sessions, multiple Claude sessions on one repo, sessions keep colliding, track claims; when sequential resources (migration or decision numbers) or shared changelog/ledger docs keep colliding between branches; or when a session needs to know what other sessions are doing before acting. NOT for release/QA pipeline coordination through a dedicated controller lane, not for plain merge-conflict fixing, not for in-session subagent orchestration, not for CI test parallelism.
---

# Parallel Sessions Protocol

Keep any number of parallel sessions on one repository from trampling each
other, without capping how many run. Field-proven under real load: one day of
7 simultaneous worktrees and 8 merged PRs produced six distinct collision
incidents; every mechanism below exists because one of them happened.
Posture: guarded-mutation — this skill creates branches and draft PRs;
merging stays governed by each project's own authorization rules.

**Preconditions**: a git repository with a GitHub remote and an authenticated
`gh` CLI (`references/setup-guide.md`). If either is missing, say so and stop
— the board mechanism cannot work without them.

**Core model**: one track = one session + one branch + one exclusive working
directory + one claim declaration. Sharing a working directory across
sessions is the root cause of cross-track pollution — never do it. The number
of tracks is unbounded; the constraint is behavior, not count.

## Mechanism 1 — Register before you code (the board)

Before writing any code:

1. `git fetch origin` and `gh pr list --state open` — see the whole board first.
2. Branch from **latest** `origin/main`; take an exclusive working directory
   (the main checkout counts as one — at most one session may own it at a time;
   every other session uses its own worktree).
3. Immediately open a **draft PR** whose body has three fixed sections
   (template in `references/draft-pr-template.md`):
   - **Claimed scope** — directories/files this track will touch
   - **Claimed numbers** — sequential resources taken (migration/decision
     numbers…); write "none" if none
   - **Current status** — one line, updated at milestones
4. When the track ends (merged or abandoned), the PR closes and the board
   self-cleans. Abandoned tracks delete their branch and worktree.

The board **is** `gh pr list`. Spawned/background sessions follow the same
rule — when writing a dispatch prompt for one, include "register on the
board first".

## Mechanism 2 — Claim before you use

| Resource | Rule |
|---|---|
| Sequential numbers (migrations, decision entries, …) | Before taking a number: check the max on main **and** scan every open PR's "Claimed numbers" section. Take the smallest free one; write it into your draft PR. |
| Files / directories | Do not touch files inside another track's claimed scope. If you must: wait for its merge, or escalate to the human owner to sequence the work. |
| Collision anyway | **The later merger yields** (renumbers / rebases). The earlier merge never changes — renumbering merged history breaks every reference to it. |

## Mechanism 3 — Ledger writes only at merge time

Shared ledger docs (a current-task / decisions / changelog style file that
every track must eventually write) are where parallel tracks collide by
construction. Structural fix:

1. **Never touch shared ledger files while the track is alive.** Process
   notes go in the track's own files (briefs, reports) — zero conflict by
   construction.
2. As the final step before merge: rebase onto latest main, **then** append
   your ledger entries (append-only files: add at the end; newest-first
   files: insert at the top), then request the merge immediately.
3. Merges are serial, so ledger writes become serial too — conflicts go from
   guaranteed to rare.
4. If one still happens (another merge landed between your rebase and your
   merge): the only correct resolution is **keep both sides in full**.
   Dropping either side erases another track's accounting. Never pick one.

## Mechanism 4 — Merge discipline

- Merges are serial. Who may merge what is the **project's** rule (some
  projects let sessions self-merge docs-only PRs; check the project's
  AGENTS.md/CLAUDE.md) — this skill never overrides it.
- **Always preview locally before merging**: `git merge origin/main
  --no-commit --no-ff` on your branch. GitHub's MERGEABLE flag lags behind
  the latest main and reports CLEAN on branches that conflict — verified in
  production.
- Never park a worktree on the main branch — it blocks every other session's
  operations that need to check out main.
- **Never `git add -A`** when tracks run in parallel; always add explicit
  paths. A blanket add sweeps other tracks' uncommitted files into your
  commit, and if their content happens to match main you will not even notice.
- After rebasing a pushed branch, push with `--force-with-lease` (plain push
  is rejected; plain `--force` can destroy a concurrent update).

## Mechanism 5 — Refresh at three checkpoints (+ health glance)

Run `git fetch` + `gh pr list` (~30 seconds) at:

1. **Start of work** — prevents claiming work another session already started.
2. **Before asking the owner anything, or reporting a major conclusion** —
   prevents asking questions another session already resolved (this exact
   embarrassment happened: four questions asked from a stale worksheet that
   had been answered and merged hours earlier).
3. **Before merging** — prevents merging on a stale base.

At start of work, also glance at CI: `gh run list --limit 5`. If main is red,
report it before starting anything new — a red cron once ran 45 consecutive
failures over four days because every session assumed someone else was
watching. The glance multiplies detection odds by the number of sessions; it
is still probabilistic, so recommend a dedicated automated watchdog for
guarantees (out of scope here).

## Mechanism 6 — Register at end of work (teardown)

Mechanism 1 point 4 covers a **track** that ends (merged or abandoned). This
mechanism covers the more common case: the **session** stops — done for now,
paused, or interrupted — while the track lives on. Before ending or pausing:

1. **Push or declare.** Push unmerged work to the track's own branch. If you
   cannot push, write a WIP declaration into the draft PR body: current
   state, and where the next session should pick up (one wip commit had to
   be rescued from an interrupted session by another track).
2. **Worktree hygiene.** Remove your worktree when done; if you must leave
   it, log why in the PR body. Orphan worktrees accumulate silently (a
   routine audit found two in one repo) and later block merges.
3. **Refresh the board.** Update the draft PR's "Current status" line.
4. **Write back triggered items.** Any pending-verification / ledger entry
   whose trigger condition has already fired gets closed now, not "later" —
   one audit found five merged PRs whose log entries still said "awaiting
   merge".

Leftovers from interrupted sessions are inventoried and claimed by the next
session entering the repo, via the board — never assume the original session
will come back.

## The human owner's interface

Unlimited tracks does not mean unlimited throughput. Two serial bottlenecks
survive any protocol: the production write path, and the owner's
review/decision bandwidth. The board makes the queue visible — "ready,
awaiting merge" and "waiting for an answer" items are countable — so the
owner throttles intake deliberately instead of being surprised. Per-track
safety gates (requirement confirmation, production-write authorization,
evidence-based acceptance) stay intact regardless of parallelism.

## Failure modes this protocol was built from

| Real incident (one day, one repo) | Killed by |
|---|---|
| Two tracks claimed the same decision number — twice | Mechanism 2 |
| Shared ledger files edited by four tracks → merge conflicts | Mechanism 3 |
| `git add -A` swept another track's four uncommitted files into a commit | Mechanism 4 |
| Owner asked four questions another session had already resolved | Mechanism 5 ② |
| A track started work another session didn't know about | Mechanism 1 |
| CI red for 45 consecutive runs, unnoticed by anyone | Mechanism 5 glance |

## Optional: notification channel

If the project has a chat webhook (Feishu / Slack / …), configure it as an
environment variable (e.g. `NOTIFY_WEBHOOK_URL` in a gitignored env file —
never commit it, never hardcode it in a skill or repo). Use it for merge
announcements and CI alerts to humans. It is **not** an inter-session
channel — sessions coordinate through the board, not through chat.

## Safety gates

- Opening draft PRs and branches: allowed freely (that is the registration).
- Merging: strictly per the project's own authorization rules; when in doubt,
  ask the owner. Never treat this skill as merge authorization.
- Deleting another session's worktree/branch: only after verifying it is
  clean (`git -C <path> status --porcelain` empty) **and** either messaging
  that session or getting the owner's go-ahead.
- Force-push: only `--force-with-lease`, only on your own track's branch.

## References

- `references/draft-pr-template.md` — the three-section board template, with
  filled examples
- `references/protocol-rationale.md` — design principles (structural beats
  disciplinary; zero new systems) and the full incident background
- `references/setup-guide.md` — `gh` CLI setup from zero, worktree basics,
  and the traps (MERGEABLE lag, checked-out-branch merge failures,
  force-with-lease)
