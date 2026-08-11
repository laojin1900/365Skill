# Governance–Execution Routing / 治理与执行路由

Use this reference only when generic governance is widening, duplicating, or slowing a
target-specific implementation or release route.

## Separate the axes / 分开两条轴

| Axis | Owns | Must not own |
|---|---|---|
| Business governance | outcome, unresolved decision, authorization, exact target, rollback, readback, closure | file list, tool order, implementation route, generic test breadth |
| Specialist execution | affected dependencies, implementation route, focused/full checks, guarded operator | broader business authority or a different target/effect |

Hard safety invariants override both: protect secrets and PII, bind the exact reviewed
source and target, preserve unrelated work, execute protected effects serially, keep
rollback and readback, and never transfer authorization.

## Precedence / 优先顺序

1. Hard safety invariant.
2. Nearest repository instruction and target-specific machine contract.
3. Five-step business governance.
4. Generic Codex technical choice.

A lower item cannot widen or weaken a higher item. Governance may stop an unauthorized
effect, but it cannot turn a valid specialist fast/focused route into a full route merely
because the action is protected.

## Evidence reuse / 证据复用

Prepare specialist evidence when the reviewed source and acceptance candidate become
stable. Reuse it while declared dependencies remain unchanged. Invalidate only for a
material change to the target, source ancestry, affected source or contracts, selected
skill, guarded operator, runbook, or evidence digest. Unrelated mainline changes alone do
not invalidate it.

Missing or invalid evidence is one named blocker. It is not a reason to select the broadest
and slowest workflow. Once a protected mutation may have happened, read the immutable
attempt receipt and preserve rollback before depending on a control-plane refresh or retry.

## Repair repeated friction / 修复重复摩擦

For an approved routing redesign, update together:

- the human router;
- the target-specific skill or runbook;
- the machine-readable contract or guarded entrypoint;
- positive, negative, drift, and route-precedence tests.

Do not claim adoption from a prose edit alone. Keep in-flight protected actions pinned to
their reviewed contract until verified success or rollback.
