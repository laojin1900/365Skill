---
name: 365-session-rotation-maintainer
description: Rotate, replace, or hand off a long-running Codex task to one successor while preserving durable work state, Git ownership, acknowledgement, and verified closeout. Use only when the user explicitly asks to rotate, replace, or hand off a Codex task or session to a successor. Do not invoke for archive-only task management, ordinary project cleanup, task age alone, generic health checks, or production execution.
---

# 365 Session Rotation Maintainer / 365任务轮换

Treat rotation as one recoverable transfer of work and task identity. Preserve the
predecessor until one successor has received, acknowledged, and presented a verified handoff.

把轮换当作一次可恢复的“工作状态 + 任务身份”转移。在唯一继任任务完成接收、确认和可见
交接前，始终保留原任务。

## Core contract / 核心约定

- Rotation requires an explicit user request. Age, context length, inconvenience, or a new
  model release does not authorize replacement or archival.
- Create at most one successor. Never create another because setup, acknowledgement, or
  readback is slow.
- Preserve unrelated worktree changes. Do not reset, clean, stash, absorb, or silently move
  them to make rotation pass.
- Never copy raw transcripts, hidden reasoning, credentials, tokens, private URLs, raw PII,
  or unnecessary logs into the handoff.
- Rotation authority does not authorize merge, deployment, database, Shopify, messaging,
  production, or other protected actions.
- Match the user's language and keep the owner-facing handoff understandable without logs.

## Modes / 模式

- **AUDIT_ONLY** — inspect readiness and report blockers without creating, renaming, or
  archiving tasks.
- **EXECUTE** — perform one complete rotation after explicit authority.
- **RECOVERY** — resume the same nonterminal rotation; never start a parallel replacement.

## Compatibility and fallback / 兼容性与降级

Select one implementation before inventory. If the current project maintains an exact
rotation entry, follow that entry and its selected contract instead of layering this
portable workflow on top. An advertised but unreadable entry is a named blocker, not
permission to fall back to an older contract. Use the workflow below only when no maintained
project implementation covers the requested operation. Never switch an in-flight rotation
to a newer contract; recover it on its bound contract until verified completion or rollback.

Full `EXECUTE` mode requires task-management capabilities that can create one successor,
send it the handoff, read back its acknowledgement and final answer, and archive the
predecessor. Renaming is optional unless the user requires a canonical title.

完整 `EXECUTE` 模式需要当前 Codex 环境能够创建继任任务、发送交接、回读确认和最终答复，
并归档原任务；只有用户要求统一标题时，重命名能力才是必要条件。

When these capabilities are unavailable, remain in `AUDIT_ONLY`: present a checkpoint draft
and one copy-ready handoff packet without writing files or changing tasks. Persist a
checkpoint only when the requested boundary separately includes that local write. State which capability is
missing, keep the predecessor active, and name the user or equipped environment as the next
owner. Do not claim that rotation completed and do not simulate task identifiers or readback.

工具不可用时保持 `AUDIT_ONLY`：在答复中给出检查点草稿和交接包，不改文件或任务；只有当前
请求也明确包含本地持久化时才写检查点。明确缺少哪项
能力，保持原任务活动，并把用户或具备工具的环境列为下一责任人。不得宣称轮换完成，也不得
伪造任务标识或回读结果。

## 1. Freeze and inventory the predecessor / 冻结并盘点原任务

Stop ordinary implementation long enough to capture current truth from durable evidence:

- task and project identity;
- current objective and delivery stage;
- completed work with commit, PR, file, or artifact evidence;
- open work and exact blockers;
- known debt and preserved decisions;
- active external operations, protected actions, callbacks, or waits;
- branch, HEAD, worktree changes, and ownership of residue;
- ranked next actions and which require fresh authorization.

Do not accept `idle`, “waiting”, or a vague chat summary as a complete inventory.

Reuse the current bounded checkpoint and unchanged verified evidence. Search only for
missing facts; do not rebuild the inventory from full transcripts or audit unrelated modules.

## 2. Create a durable checkpoint / 创建持久检查点

Use the project's existing handoff or task-state location. If none exists, write a bounded
Markdown checkpoint under `docs/session-handoffs/<task-slug>.md`. Commit or publish it only
when the user's requested delivery boundary authorizes that Git effect.

The checkpoint contains decisions and evidence, not conversation history. Read
[references/handoff-and-verification.md](references/handoff-and-verification.md) for the
portable template.

## 3. Audit before successor creation / 创建继任任务前审计

Confirm:

1. predecessor identity and current status are known;
2. worktree state is classified and preserved;
3. no unknown active protected action, external send, deployment, or irreversible operation
   is in flight;
4. the durable checkpoint matches the current work;
5. no nonterminal rotation or already-created successor exists;
6. task-management tools needed to create, message, read, and archive are available, plus
   rename capability when the requested outcome requires a canonical title.

If any condition fails, keep the predecessor active and report one exact blocker, next owner,
and recovery action. Do not archive first and reconstruct later.

## 4. Create exactly one successor / 只创建一个继任任务

Create one successor in the same project or explicitly selected destination. Use a neutral
initial prompt such as:

```text
WAIT_FOR_VERIFIED_HANDOFF
```

Record the returned task identifier and environment/worktree identity. A setup receipt or
provisional client identifier is not yet the verified successor identity.

## 5. Deliver one bounded handoff / 发送一次结构化交接

Send the successor one message containing:

- predecessor and successor identifiers;
- project/repository and relevant branch or commit;
- durable checkpoint path and digest when available;
- complete work inventory summary;
- preserved decisions and constraints;
- exact first recommended action;
- actions that require new user authorization;
- the required acknowledgement format.

Require the successor to validate the checkpoint and return:

```text
HANDOFF_CONTEXT_ACK
WORK_STATE_ACK
HANDOFF_ACCEPTED
```

Do not send duplicate handoffs. Corrections contain only the changed field and its evidence.

## 6. Verify the successor / 验证继任任务

Read back the successor and verify:

- the intended task received the handoff;
- identifiers and checkpoint digest match;
- the successor can access the required repository or artifacts;
- the complete owner-facing kickoff is visible in its final answer, not only commentary;
- open work, blockers, preserved decisions, next action, and authorization boundaries are
  all present;
- no protected operation started from historical approval.

Self-reported acknowledgement alone is insufficient when thread/task readback is available.

## 7. Rename and archive last / 最后再改名和归档

Only after verified acknowledgement and visible kickoff:

1. make the successor the canonical active task using the available project mechanism;
2. rename it to the intended canonical title when requested;
3. archive the predecessor only when its worktree is safe and it owns no active obligation;
4. preserve durable checkpoints and relevant Git history;
5. verify that the successor remains readable and active after archival.

If archival fails after successor verification, keep both tasks and resume the same rotation.
Do not create a replacement successor.

## Recovery / 恢复规则

- Failure before successor creation: predecessor remains canonical.
- Failure after successor creation: preserve both and resume the same successor.
- Stale or mismatched acknowledgement: correct the named mismatch only.
- Dirty or divergent predecessor: preserve visibly; do not archive.
- Active protected operation: wait for its terminal success or verified rollback.
- Unavailable predecessor: reconstruct a checkpoint from durable Git/project evidence and
  mark every uncertain item; never present memory as fact.

Use the available event-wait mechanism for task setup or acknowledgement, preserving its
cursor. Inspect the same successor when setup is ambiguous; do not poll full histories or
repeat unchanged validation. Revalidate changed identity, source, checkpoint, or contract
dependencies, and report only meaningful state changes.

## Closeout / 收尾

Report:

- rotation status: audited, transferred, verified, blocked, or recovered;
- predecessor and successor identifiers;
- durable checkpoint path/digest;
- acknowledgement and final-answer readback evidence;
- Git/worktree state and preserved residue;
- archival result;
- first recommended action and its owner;
- protected actions executed by rotation: always zero.

The rotation is closed only when the successor is verified and the predecessor is either
safely archived or explicitly retained with a named reason.
