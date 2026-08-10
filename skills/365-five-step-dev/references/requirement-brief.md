# Business Requirement Brief / 业务需求简报

Use the smallest format that preserves the decisions Codex and the business owner need.

使用足以保留关键决策的最小格式，不为写文档而写文档。

## Quick brief for unresolved scope / 范围未决时的快速简报

Keep this in the conversation unless the project already requires a decision document.

项目没有决策文档要求时，直接在对话中输出即可。

```markdown
## Business plan / 业务方案

- Outcome / 目标结果:
- User and scenario / 用户与场景:
- In scope / 本次包含:
- Out of scope / 本次不包含:
- Affected areas / 影响范围:
- Assumptions / 当前假设:
- Acceptance evidence / 验收证据:
- Rollback / 回滚:
```

Ask no more than three consolidated questions. Ask only questions whose answers change the solution. For each question, include:

1. the recommended answer;
2. why it is recommended;
3. what changes if the user chooses differently.

最多集中询问三个会改变方案的问题。每个问题必须包含推荐答案、推荐理由，以及选择不同答案会发生什么变化。

## Durable brief for material long-running decisions / 重大长任务决策简报

Use this only when a long-running or multi-session task has material decisions that are not
already durable. Write into the repository's established decision-doc location. If none
exists, use `docs/decisions/<task-slug>.md`. Do not create it merely because a task is
protected or C-grade.

只有长任务或跨会话任务存在尚未持久记录的重大决策时才使用。写入项目既有决策文档目录；
没有约定时使用 `docs/decisions/<任务名>.md`。不要仅因任务是受保护或 C 级就创建。

```markdown
# <Outcome> / <业务结果>

## Purpose / 目的
- Business outcome / 业务结果:
- Users and scenario / 用户与场景:
- Why now / 为什么现在做:

## Scope / 范围
- In / 包含:
- Out / 不包含:
- Existing behavior to preserve / 必须保留的现有行为:

## Decisions / 已定决策
| Decision / 决策 | Choice / 选择 | Reason / 理由 | Date / 日期 |
|---|---|---|---|

## Business rules / 业务规则
- Happy path / 正常流程:
- Exceptions / 异常流程:
- Roles and permissions / 角色与权限:
- Data compatibility / 数据兼容:

## Impact and boundary / 影响与边界
- Systems and teams / 系统与团队:
- Protected actions / 受保护操作:
- External dependencies / 外部依赖:
- Rollback / 回滚:

## Acceptance / 验收
| Outcome / 业务结果 | Evidence / 证据 | Status / 状态 |
|---|---|---|

## Open items / 待明确
- Question / 问题:
- Recommended answer / 推荐答案:
- Decision needed by / 最晚决策点:
```

## Decision discipline / 决策纪律

- Separate a business decision from a technical implementation choice. Ask the user only for the former.
- 区分业务决策和技术实现选择，只把前者交给用户。
- Preserve exact business terms, amounts, roles, states, and policy wording. Do not silently paraphrase them into a different rule.
- 原样保留业务术语、金额、角色、状态和政策文案，不得转写成不同规则。
- Record a rejected alternative only when it may be reconsidered later or prevents repeated debate.
- 只有可能重新评估、或需要避免重复争论时，才记录被否决方案。
- Mark unknowns honestly. Do not manufacture decisions to make the brief look complete.
- 对未知项如实标注，不为了让简报“完整”而制造伪决策。

## Oversized work / 超长任务

When one task spans several releases or loosely coupled systems, turn the brief into a map:

当一个任务跨越多次发布或多个松耦合系统时，把简报扩展成任务地图：

1. Define the final business destination.
2. Split delivery into independently verifiable milestones.
3. Give each milestone one owner, boundary, prerequisite, and acceptance test.
4. Keep unresolved decisions separate from implementation tasks.
5. Update the map with evidence at each milestone.

1. 明确最终业务目的地。
2. 拆成可以独立验收的里程碑。
3. 每个里程碑写清责任人、边界、前置条件和验收方式。
4. 把待决策问题和实施任务分开。
5. 每个里程碑完成后用证据更新地图。
