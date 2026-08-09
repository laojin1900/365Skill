# Handoff and verification / 交接与验证

## Durable checkpoint template

```markdown
# Task handoff: <task>

## Identity
- Project/repository:
- Module or scope:
- Predecessor task:
- Current branch and commit:
- Checkpoint date:

## Current objective and stage
- Requested outcome:
- Intended delivery level:
- Reached boundary:

## Completed work
| Item | Evidence | Delivery state |
|---|---|---|

## Open work and blockers
| Item | Current state | Blocker | Next owner |
|---|---|---|---|

## Known debt
- <bounded, evidence-backed debt>

## Preserved decisions
| Decision | Reason | Evidence |
|---|---|---|

## Active obligations
- External operations:
- Protected actions:
- Callbacks or waits:
- None, when verified:

## Workspace state
- Worktree:
- Staged/unstaged/untracked paths:
- Ownership classification:

## Recommended continuation
1. First action:
2. Later actions:
3. Fresh authorization required for:

## Unverified items
- <item, why unverified, consequence>
```

## Handoff message template

```text
PREDECESSOR_TASK: <id>
SUCCESSOR_TASK: <id>
PROJECT: <project>
CHECKPOINT: <path or artifact id>
CHECKPOINT_DIGEST: <sha256 or unavailable>
SOURCE_COMMIT: <commit or not applicable>

Read and validate the checkpoint. Do not execute protected actions or inherit historical
approval. Return exactly:

HANDOFF_CONTEXT_ACK
WORK_STATE_ACK
HANDOFF_ACCEPTED

Then present the complete owner-facing kickoff with the current objective, completed work,
open work, blockers, decisions, first recommended action, and authorization boundaries.
```

## Verification checklist

- One successor only.
- Predecessor and successor identifiers are exact.
- Checkpoint path and digest match the sent handoff.
- Successor can read the required project evidence.
- All three acknowledgement markers are present.
- Owner-facing kickoff is visible in the successor's final answer.
- Kickoff covers objective, completion, open work, blockers, decisions, and next action.
- Historical approvals are explicitly not inherited.
- No protected action was executed under rotation authority.
- Predecessor worktree is safe before archival.
- Successor remains active and readable after archival.

If any item fails, preserve both tasks and resume the same rotation.
