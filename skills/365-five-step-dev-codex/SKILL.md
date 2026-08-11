---
name: 365-five-step-dev-codex
description: "The Codex edition of business-led five-step governance for scoped, risk-aware, evidence-verified delivery. Invoke explicitly when the user says 五步法, 365五步法, or 365五步法 Codex版, uses $365-five-step-dev-codex, or directly requests this Codex governance method. Invoke automatically only for an actual production or infrastructure change, a bulk or destructive live-data operation, an unresolved business permission or compliance decision, or a process-governance redesign. Do not invoke for requests that explicitly name the Claude edition. Do not invoke implicitly for ordinary features, database or migration-file authoring, permission implementation, commits, PRs, merges, local previews, deployment preparation, a dirty worktree by itself, general questions, or read-only analysis."
---

# 365 Five-Step Development (Codex Edition) / 365五步法（Codex版）

Use this skill as a thin business-governance layer around Codex. Do not duplicate Codex's
native planning, implementation, debugging, review, testing, Git delivery, repository
instructions, or target-specific skills.

把本技能作为 Codex 外层的轻量业务治理，而不是第二套开发流程。不要重复 Codex 原生的规划、
编码、调试、审查、测试、Git 交付、仓库规则或专业技能。

## Core contract / 核心约定

- Match the user's language and explain decisions, risks, and evidence in business terms.
- Infer repository and implementation details before asking. Ask only about a genuinely
  unresolved business choice that materially changes behavior, cost, ownership, compliance,
  permission, or an irreversible result. Include a recommended answer and consequence.
- Leave technical route selection to Codex and the most specific current project skill.
- Own worktree isolation and delivery completeness. Do not make a non-coding user classify
  files, choose a Git strategy, or discover later that task changes were left uncommitted.
- Own closure. Continue safe, in-scope, already authorized work until the requested delivery
  level is reached or one exact blocker remains.

- 跟随用户语言，用业务语言解释决策、风险和证据。
- 先从仓库查清技术事实；只有业务行为、成本、责任、合规、权限或不可逆结果仍有重大分歧时，
  才向用户提一个带推荐答案和影响的问题。
- 技术路线交给 Codex 和当前项目最具体的专业技能。
- 主动负责工作区隔离、文件归属和交付完整性，不把 Git 判断交给非技术用户。
- 对闭环负责；仍有安全、在范围内且已授权的工作时继续推进。

## Establish one goal capsule / 建立一个目标胶囊

Derive this capsule from the request and repository evidence; do not create a document or
ask the user to fill a form when the fields are already clear:

```text
Business outcome:
Requested delivery level: local | commit | push/PR | merge | deploy/live effect
Exact protected target and effect, if any:
Acceptance evidence:
Stopping condition:
```

A current request that clearly names the action, exact target, and business outcome is
goal-scoped authorization for that effect. It remains valid through preflight, bounded
technical corrections, safe rollback, propagation monitoring, and serial continuation
toward the unchanged outcome. Reconfirm only when the target, scope, material effect,
permission or credential boundary, rollback, or user intent changes materially.

从当前请求和仓库证据推导目标胶囊；字段明确时不要求用户填表。用户已明确动作、准确目标和
业务结果，即形成该效果的目标级授权；同目标的预检、技术修复、安全回滚、传播监控和串行继续
不重复询问。只有目标、范围、实际后果、权限/凭据边界、回滚或用户意图实质变化时才重新确认。

## Scale by actual impact / 按真实影响缩放

Use the grade internally. State it only when it helps the user understand risk or a gate.

| Grade | Actual boundary | Depth |
|---|---|---|
| **A — Small / 微小** | Safe, contained, reversible work; no live effect | Inspect → change → focused verify |
| **B — Standard / 普通** | A bounded product or business behavior with no unresolved protected effect | Keep all five questions internal; add no ceremony |
| **C — Protected / 高风险** | Actual production/infrastructure effect, bulk or destructive live-data action, unresolved permission/compliance decision, or governance redesign | Scale only to the unresolved risk; use the compact protected path when execution is already exact |

Domain words do not determine the grade. Database code, a migration file, permission
implementation, payment-flow code, a commit, or a dirty worktree is not C-grade by itself.

不能按领域名词机械升档。数据库代码、迁移文件、权限实现、支付流程代码、提交或脏工作区本身
不等于 C 级；要看是否真的触及在线效果或尚未解决的业务风险。

## Five steps / 五步执行

### 1. Research / 理解现状

Read the nearest `AGENTS.md`, task-relevant source, tests, manifests, and the smallest
necessary runbook. Establish current behavior, affected people or systems, the smallest
coherent change, known facts, assumptions, and unresolved business decisions.

Before the first file or Git write, inspect repository status once and preserve unrelated
work. Read [workspace-delivery.md](references/workspace-delivery.md) only for mixed or dirty
worktrees, unclear ownership, isolation, or special delivery handling.

### 2. Plan / 形成方案

Use the goal capsule as the plan when it is sufficient. Read
[requirement-brief.md](references/requirement-brief.md) only when outcome, scope, acceptance,
rollback, or multi-milestone ownership remains materially unresolved. Safe reversible
assumptions may be stated and used without another approval ritual.

### 3. Implement / 实施

Let native Codex and the most specific project skill implement the smallest complete change.
Reuse existing contracts, verify incrementally, avoid unrelated cleanup, and keep current-task
changes isolated and attributable. A material business-scope change updates the goal capsule;
an ordinary technical choice does not create a new approval boundary.

### 4. Review / 换视角检查

Review the actual diff or effect against the business outcome: requirement coverage,
unintended behavior, scope expansion, data/permission/privacy/compatibility risk, failure
paths, rollback, evidence gaps, and delivery completeness. Use an independent review surface
only when actual risk justifies it. Reproduce decision-critical reviewer claims before
accepting them as evidence.

### 5. Verify / 证据验收

Map each important business outcome to observed evidence. Distinguish passed, failed, and
not verified. Prefer the real affected flow over implementation claims. Read
[business-acceptance.md](references/business-acceptance.md) only for material user journeys,
data persistence, permissions, integrations, amounts, or release acceptance.

Verify the requested delivery boundary as well: local code is not a shared GitHub delivery;
a merge is not a deployment; a deployment is not verified until target readback. Inspect
workspace residue only when files or Git changed.

## Ready protected execution / 已就绪的受保护执行

When the goal capsule names the protected action, exact target, and outcome, and the project
provides an exact reviewed source, guarded operator, rollback, and readback:

1. Run one complete preflight binding target, reviewed source, credential boundary, rollback,
   and acceptance evidence.
2. Consume the active goal authorization without an equivalent second approval question.
3. Execute one serial guarded attempt.
4. Read back the target and close success, or run the fixed safe rollback and report the
   terminal result.

Do not add a requirement brief, generic review stage, coordinator route, second approval
prompt, or full-repository suite. The specialist contract owns execution and evidence breadth.
Broaden only for a changed shared contract, shared kernel, or system-wide boundary. Never
blind-retry or execute protected mutations concurrently.

If the target, effect, permission boundary, rollback, or authorization is not exact, read
[risk-gate.md](references/risk-gate.md) and stop only at that unresolved boundary.

## Long-running progress / 长任务进度

At a meaningful wait, handoff, blocker, or user status request, give one compact checkpoint:

```text
Current goal / 当前目标:
Reached boundary / 已到达边界:
Next action and owner / 下一步及责任人:
User decision / 是否需要用户决定: none | <one exact decision with recommendation>
```

Do not emit this certificate every turn. Use it only to prevent the user from wondering what
is happening or what must happen next. Keep material long-running decisions in the project's
existing durable location; do not create a log merely because a task is C-grade.

## Closure / 闭环

Keep ordinary closeout proportional: outcome, strongest verification, actual code/release
state, and one real remaining action if any. Add `Closed`, `Not closed`, or `Blocked` only
when the delivery level is incomplete or ambiguous, or a protected action needs a terminal
success/rollback statement.

Do not stop while safe authorized work remains. If authorization is genuinely missing,
provide one copy-ready sentence naming the exact action, target, and stopping point. Never
leave the user to infer whether they must reply or who owns the next step.

## Conditional references / 按需参考

- Unresolved scope or milestones: [requirement-brief.md](references/requirement-brief.md)
- Mixed worktree or delivery ownership: [workspace-delivery.md](references/workspace-delivery.md)
- Unresolved protected boundary: [risk-gate.md](references/risk-gate.md)
- Material business acceptance: [business-acceptance.md](references/business-acceptance.md)
- Generic governance widens a specialist route: [governance-execution-routing.md](references/governance-execution-routing.md)
- Explicit process improvement or repeated abnormal evidence: [adaptation-loop.md](references/adaptation-loop.md)

Do not load project-specific governance into this global skill. Prefer the nearest repository
skill or `AGENTS.md` for module ownership, coordinators, registries, release models, and
target-specific operators.

## Process evolution / 流程迭代

Normal success creates no retrospective or extra log. When real evidence shows repeated
friction, false blocking, preventable rework, a safety escape, or confirmed rule value, read
[adaptation-loop.md](references/adaptation-loop.md). Prefer narrowing, automating, demoting,
or retiring rules over adding universal gates. Never self-modify the skill; promote a change
only with focused validation, rollback, and explicit user authorization.
