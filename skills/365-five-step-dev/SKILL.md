---
name: 365-five-step-dev
description: "Business-led five-step governance for scoped, risk-aware, evidence-verified Codex delivery. Invoke explicitly when the user says “五步法” or “365五步法”, uses $365-five-step-dev, or directly requests this governance method. Invoke automatically only for an actual production or infrastructure change, a bulk or destructive live-data operation, an unresolved business permission or compliance decision, or a process-governance redesign. 面向懂业务但不熟悉代码与开发流程的用户，帮助管理需求范围、工作区归属、风险边界、验收证据和交付闭环。Do not invoke implicitly for ordinary features, migration-file authoring, permission implementation, commits, PRs, merges, local previews, deployment preparation, a dirty worktree by itself, general questions, or read-only analysis."
---

# 365 Five-Step Development / 365五步法

Use this skill as a business governance layer around Codex, not as a replacement for Codex's native planning, coding, review, testing, repository instructions, or official skills.

把本技能作为 Codex 外层的业务治理流程，而不是用它替代 Codex 原生的规划、编码、审查、测试、项目规则或官方技能。

## Core contract / 核心约定

- Match the user's language. Explain decisions, risks, and evidence in business language; keep technical names only where useful.
- 跟随用户语言。用业务语言解释决策、风险和证据，只在必要时保留技术名词。
- Infer implementation details from the repository before asking. Ask only about choices that cannot be discovered and would materially change the outcome.
- 先从仓库查清实现信息。只询问无法查到、且会实质改变结果的业务选择。
- Give every question a recommended answer and its consequence. Let the user confirm or overturn a reasoned recommendation.
- 每个问题都附推荐答案、理由及影响，让用户做确认或推翻，而不是从零设计方案。
- Do not prescribe a model, reasoning level, agent topology, or fixed tool sequence. Let Codex choose the technical method.
- 不指定模型、推理档位、代理结构或固定工具顺序，把技术方法交给 Codex。
- Do not add approval rituals to safe, reversible local work. Gate only unresolved business decisions and protected actions.
- 不给安全、可逆的本地工作增加审批仪式；只卡住尚未明确的业务决策和受保护操作。
- Own the process complexity. Never require a non-coding user to identify Git ownership, decide how to isolate a dirty worktree, or discover that task changes were left uncommitted.
- 主动承担流程复杂度。不要让不懂代码的用户判断 Git 文件归属、决定如何隔离脏工作区，或事后才发现任务改动没有提交。
- Own closure, not only implementation. Before ending, decide whether the user's requested outcome has reached and verified its intended delivery level. If safe authorized work remains, continue instead of handing the remaining process back to the user.
- 对闭环负责，而不只是对代码负责。结束前判断用户要求的结果是否已经到达并验证其目标交付层级；如果仍有安全且已授权的工作，就继续推进，不把剩余流程交还给用户。

## Grade by impact / 按影响分级

Classify the task after a brief inspection. State the grade and one business-language reason. Grade the actual affected boundary, not the apparent size of the request.

先做简短检查再分级，用一句业务语言说明等级和原因。按真实影响边界判断，不按需求文字长短判断。

| Grade | Typical boundary | Execution depth |
|---|---|---|
| **A — Small / 微小** | Copy, spacing, isolated styling, obvious contained bug; no data, permission, API-contract, or production impact | Abbreviate to inspect → change → verify |
| **B — Standard / 普通** | New page, form, report, contained API or module feature; impact remains inside one product area | Keep the five headings brief and let Codex's native workflow carry the technical detail; continue through safe local work when assumptions are non-material |
| **C — Protected / 高风险** | Production or infrastructure change, schema or migration, auth/permissions, payment/order/inventory, customer data, bulk mutation, shared cross-project capability, destructive action | Run all five steps, load all relevant references, and stop at the exact protected boundary for approval |

If impact is unclear, inspect further before raising the grade. Do not automatically choose the higher grade merely because information is missing.

影响不清楚时先继续查证，不要因为信息暂缺就机械地升到更高等级。

## Five steps / 五步执行

### 1. Research / 理解现状

Read the nearest `AGENTS.md`, relevant project documentation, existing implementation, tests, and runtime boundaries. Reuse existing capabilities. Identify:

- the business flow today;
- the people or systems affected;
- the smallest change that can achieve the outcome;
- facts, assumptions, and genuinely unresolved decisions.

先读最近的 `AGENTS.md`、相关文档、现有实现、测试和运行边界。找出当前业务流程、影响对象、最小可行改动，以及事实、假设和真正待决定的问题。

For any task that may write files, commit, publish, merge, or deploy, read [workspace-delivery.md](references/workspace-delivery.md) and capture the pre-task repository baseline before editing. Classify existing changes yourself; preserve unrelated work.

任何可能写文件、提交、发布、合并或部署的任务，都要先读取 [workspace-delivery.md](references/workspace-delivery.md)，在编辑前记录仓库基线，并由 Codex 自行判断已有改动的归属、保护无关工作。

### 2. Plan / 形成方案

For B or C tasks, use [requirement-brief.md](references/requirement-brief.md) to frame the outcome, scope, non-scope, impact, acceptance evidence, and rollback. Keep the plan short enough for a non-coder to approve.

对 B/C 级任务，按 [requirement-brief.md](references/requirement-brief.md) 整理业务结果、范围、范围外、影响、验收证据和回滚办法。方案必须短到不懂代码的用户也能判断。

- If a missing decision changes the product behavior, cost, ownership, compliance, or irreversible outcome, ask with a recommendation.
- If an assumption is safe and reversible, state it and continue.
- Do not wait for approval before ordinary local edits, tests, documentation, or previews already authorized by the request.
- State the intended delivery level: local-only, committed, pushed/PR, merged, or deployed. Recommend the level implied by the user's requested outcome instead of expecting the user to know Git terminology. The task is not closed until that level is reached and verified, unless a named blocker prevents it.

- 缺失决策会改变产品行为、成本、责任、合规或不可逆结果时，带推荐答案询问。
- 假设安全且可逆时，明确写出后继续。
- 用户已授权的普通本地编辑、测试、文档和预览，不额外等待审批。
- 明确本次交付层级：仅本地、已提交、已推送/PR、已合并或已部署。根据用户想要的业务结果给出推荐，不要求用户先懂 Git 术语；在到达并验证该层级前，不得宣称闭环，除非存在明确阻塞。

### 3. Implement / 实施

Implement the smallest coherent change that satisfies the framed outcome. Follow repository instructions and use relevant native or official skills. Reuse existing modules, verify incrementally, and avoid unrelated cleanup.

实施满足业务结果的最小完整改动。遵守项目规则并使用相关原生或官方技能；优先复用、边做边验证，不顺手清理无关代码。

If implementation reveals a material scope change, report the new fact and reframe the affected part before continuing. Do not treat ordinary technical choices inside the approved outcome as new business approvals.

如果实施中发现会实质改变范围的新事实，先说明并重新界定受影响部分。批准范围内的普通技术选择不重新上升为业务审批。

Keep current-task changes isolated and attributable. In a mixed worktree, stage and commit only the intended paths; never hide, overwrite, reset, stash, or absorb unrelated changes. Prefer a dedicated branch or worktree for new writable work.

保证当前任务改动隔离且可归属。在混合工作区中只暂存和提交本任务路径；不得隐藏、覆盖、重置、stash 或顺带吸收无关改动。新的写入任务优先使用独立分支或工作树。

### 4. Review / 换视角检查

Review against the approved business outcome and the actual diff:

- requirement coverage and unintended behavior;
- scope expansion and unrelated files;
- data, permission, privacy, and compatibility risk;
- failure paths and rollback viability;
- missing or weak verification;
- delivery completeness: current-task files committed as intended, no task files silently left behind, and unrelated residue classified separately.

根据业务目标和真实改动检查：需求覆盖、意外行为、范围膨胀、无关文件、数据与权限风险、兼容性、异常路径、回滚能力、验证缺口和交付完整性。确认本任务文件已按约定提交，没有静默遗漏；无关残留另行分类。

Use an independent review surface when risk and available tooling justify it, but do not force a specific subagent or ask the user to review code.

风险和工具条件合适时使用独立视角审查，但不强制指定某个子代理，也不要求用户逐行看代码。

Treat verification claims inside any agent or reviewer report (mutation checks, cited precedents, re-run conclusions) as unverified until the coordinator independently reproduces the key ones.

任何代理或审查报告中的验证自述（变异检查/先例引用/复核结论）不默认采信，关键项由协调方独立复现后才算数。

### 5. Verify / 证据验收

Read [business-acceptance.md](references/business-acceptance.md) and the closeout section of [workspace-delivery.md](references/workspace-delivery.md). Map every important business outcome to observed evidence. Prefer real user-flow checks over implementation claims.

读取 [business-acceptance.md](references/business-acceptance.md) 和 [workspace-delivery.md](references/workspace-delivery.md) 的收尾规则，把每条重要业务结果映射到实际证据，优先验证真实用户流程，不用“代码写完了”代替验收。

Distinguish clearly among:

- verified and passed;
- verified and failed;
- not verified, with the reason and consequence.

清楚区分：已验证通过、已验证失败、未验证及其原因和后果。没有证据时，不得宣称完成。

Verify the closure boundary as well as the implementation. A local commit is not closed
when the intended outcome is shared GitHub use; a merge is not a deployment; a deployment
is not verified until the target is read back. When the next action is safe, in scope, and
already authorized, execute it before ending.

除验证实现外，还要验证闭环边界。如果目标是让团队在 GitHub 使用，本地提交不算闭环；
合并不等于部署；没有目标读回，部署不算验证完成。下一步安全、在范围内且已经授权时，
必须先执行再结束。

## Protected-action gate / 受保护操作闸门

For C-grade work, read [risk-gate.md](references/risk-gate.md) before the protected action. Read-only inspection and reversible local preparation may continue first.

C 级任务在执行受保护操作前读取 [risk-gate.md](references/risk-gate.md)。此前可以继续只读检查和可逆的本地准备。

A clear user request naming the exact action and target counts as approval; do not ask twice. Reconfirm only when the target, scope, consequence, or rollback materially differs from what the user authorized.

用户已经明确指定操作和目标时即视为授权，不重复询问。只有目标、范围、后果或回滚方式出现实质变化时才重新确认。

For deployment, bind the action to an exact reviewed commit. A dirty canonical worktree is not automatically a blocker: when repository policy permits, prepare and verify from a clean isolated worktree or fresh checkout at that exact commit while leaving unrelated local changes untouched.

部署必须绑定到经过审查的准确提交。canonical 工作区有无关改动时，不自动把它当作阻塞；项目规则允许时，从该提交创建干净的隔离工作树或全新检出进行预检和部署，同时保持无关本地改动不变。

## Long-running work / 长任务连续性

For C-grade or multi-session work, keep a durable decision brief in the repository's existing decision-doc location. If none exists, use `docs/decisions/<task-slug>.md`. Record decisions, reasons, scope, evidence, and open items—not chat history or hidden reasoning.

对于 C 级或跨会话任务，在项目既有决策文档目录保存简报；没有约定时使用 `docs/decisions/<任务名>.md`。只记录决策、理由、范围、证据和待办，不记录聊天流水或隐藏推理。

## Closure and handoff / 闭环与交付格式

Start every final handoff with an explicit closure verdict:

- **Closed / 已闭环**: the requested business outcome and intended delivery level are reached and verified, with no required work remaining.
- **Not closed / 未闭环**: the work is at an intermediate state such as local-only, committed, PR open, merged-but-not-deployed, or deployed-but-not-verified.
- **Blocked / 已阻塞**: a specific external condition, missing authority, or material user decision prevents further progress.

每次最终交付必须先明确写“已闭环、未闭环或已阻塞”。只有业务结果和目标交付层级都已到达并验证、且没有必做事项剩余，才能写“已闭环”。

Do not send a final handoff while safe authorized work remains. Continue autonomously. Stop only at a genuine protected boundary, a material decision, or an external blocker. When stopping, make it impossible for the user to wonder what happens next.

仍有安全且已授权的工作时，不要发送最终交付，继续自主推进。只有真实受保护边界、重大决策或外部阻塞才停止；停止时不得让用户猜测下一步。

For A/B work, keep the final response proportional. Always state the closure verdict, any
remaining action and its owner, and whether the user must decide anything. Include Git,
release, rollback, authorization, or workspace-residue details only when they affected the
task. For C-grade or non-closed work, use this fuller order:

对 A/B 级任务保持简洁。必须说明闭环状态、剩余动作及责任人、是否需要用户决定；只有 Git、
发布、回滚、授权或工作区残留确实影响本次任务时才展开。C 级或尚未闭环的任务使用以下完整顺序：

1. Closure verdict and why / 闭环状态及原因
2. Requested outcome and reached boundary / 用户目标与已到达层级
3. Evidence checked / 已核验证据
4. Code delivery state: commit, branch, PR, merge / 代码交付状态
5. Release state: not requested, pending approval, deployed, verified / 发布状态
6. Workspace residue / 工作区残留
7. Next required action; write `none` only when closed / 下一步必做动作；仅已闭环时可写“无”
8. Next owner: `none—closed`, `Codex`, `User`, or a named external owner / 下一步责任人；已闭环时写“无”
9. User decision: `not needed` or one exact decision with a recommended answer and consequence / 是否需要用户决定

If user authorization is needed, provide one copy-ready approval sentence that names the exact action, target, and stopping point. If no user decision is needed, say so and continue rather than ending with an invitation such as “let me know if you want me to proceed.”

需要用户授权时，提供一句可直接复制的批准语，写清准确操作、目标和推进终点。不需要用户决定时，要明确说明并继续，不得以“如果需要我可以继续”结束。

Do not create a global log, require a retrospective cadence, or modify this skill automatically. Improve the skill only from repeated evidence and with explicit user authorization.

不创建全局运行日志，不强制复盘周期，也不自动修改技能本身。只有出现重复证据且用户明确授权时，才升级本技能。
