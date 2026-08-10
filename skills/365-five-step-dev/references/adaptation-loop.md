# Adaptive Process Loop / 自适应流程迭代

Use this reference only when the user explicitly asks to evolve the five-step process or
when repeated evidence shows friction, false blocking, rework, a safety escape, or confirmed
rule value. It is not a sixth delivery step.

## Rule classes / 规则分类

| Class | Examples | Change policy |
|---|---|---|
| Hard safety invariant | secrets/PII, exact target and reviewed source, current scoped authorization, unrelated-work protection, rollback/readback, no blind retry | Never relax through this loop |
| Adaptive process rule | brief length, review depth, test breadth, reminders, escalation timing | May narrow, automate, shadow, demote, or retire |
| User preference | summary detail, preferred status language, optional coordination | May be learned explicitly; never becomes broader authority |

## Evidence signals / 证据信号

Record no signal for ordinary successful work. Use one compact signal only when it matters:

- `PROCESS_FRICTION`: ceremony or time is disproportionate to the controlled risk.
- `PROCESS_FALSE_BLOCK`: safe reversible work stopped without protecting a real boundary.
- `PROCESS_REWORK`: the same preventable misunderstanding or delivery defect recurred.
- `PROCESS_SAFETY_ESCAPE`: a meaningful risk crossed the safeguards.
- `PROCESS_RULE_VALUE_CONFIRMED`: repeated evidence shows a rule prevents real harm at
  acceptable cost.

Attach the observation to existing evidence such as a task closeout, PR, or terminal receipt.
Do not create a global activity log or mandatory retrospective.

```text
Process signal:
Affected rule:
Observed evidence:
Business or safety effect:
Candidate direction: keep | narrow | automate | strengthen | demote | retire
```

## Candidate contract / 候选规则合同

Require every candidate to state:

1. current behavior and affected task class;
2. isolated or repeated evidence;
3. the smallest proposed change;
4. hard invariants that remain unchanged;
5. expected benefit and added cost;
6. success, failure, rollback, and retirement criteria.

Reject “be more careful”, duplication of native Codex capability, or a universal step with
no precise trigger.

## Lifecycle / 生命周期

Use `candidate -> shadow -> active -> advisory/demoted -> retired`.

Shadow evaluation must not block or delay the live task, add a user question, mutate
production, or broaden authority. Promote only with focused evidence, no safety regression,
an exact rollback, and explicit user authorization. Keep the prior version recoverable.

## Anti-bloat check / 防膨胀检查

Before adding a rule, ask:

1. Can native Codex already handle it?
2. Can the trigger be narrower?
3. Can automation or a reminder replace a gate?
4. Can an existing rule be simplified or retired at the same time?
5. Is there a clear demotion or removal condition?

Keep the candidate out of the active skill when these questions lack concrete answers.
