# Business Acceptance / 业务验收

Verification proves the business outcome, not merely that code exists or a command exited successfully.

验收要证明业务结果真实成立，而不仅是代码存在或命令执行成功。

## Evidence matrix / 证据矩阵

Build a compact matrix for important outcomes:

为重要业务结果建立简洁证据表：

```markdown
| Business outcome / 业务结果 | Check performed / 实际检查 | Evidence / 证据 | Status / 状态 |
|---|---|---|---|
| ... | ... | ... | Passed / Failed / Not verified |
```

Use the strongest practical evidence at the affected boundary:

在实际受影响边界选择最有说服力的证据：

- **User interface / 用户界面**: open the real page or preview, perform the user flow, and inspect important states.
- **用户界面**：打开真实页面或预览，实际走一遍用户流程并检查关键状态。
- **Persistence / 数据持久化**: create or update data through the intended path, refresh or re-query, and confirm it remains correct.
- **数据持久化**：通过预期路径写入，再刷新或重新查询，确认数据仍正确。
- **Roles and permissions / 角色权限**: test both an allowed role and a denied role where feasible.
- **角色权限**：条件允许时，同时验证允许角色和禁止角色。
- **API or integration / 接口集成**: verify request, response, failure handling, and idempotency where relevant.
- **接口集成**：核验请求、响应、失败处理，以及相关场景下的幂等性。
- **Business amounts / 业务金额与数量**: reconcile with an independent source or known fixture.
- **业务金额与数量**：与独立来源或已知样例对账。
- **Regression / 旧功能回归**: run the narrowest reliable existing tests, then broaden for shared contracts or public modules.
- **旧功能回归**：先运行最相关的既有测试；涉及公共模块或共享契约时扩大检查。
- **Release / 发布**: verify the exact environment, version or commit, health signal, and rollback readiness.
- **发布**：核对准确环境、版本或提交、健康信号和回滚准备。

## Status rules / 状态规则

- **Passed / 通过**: the check actually ran and observed the expected result.
- **通过**：检查已真实执行并观察到预期结果。
- **Failed / 失败**: the check ran and observed a mismatch; report the mismatch and impact.
- **失败**：检查已执行但结果不符；说明差异和影响。
- **Not verified / 未验证**: the check did not run or could not reach the real boundary; explain why and what risk remains.
- **未验证**：检查未执行或无法到达真实边界；说明原因和剩余风险。

Do not convert “not verified” into “passed” because lint, types, unit tests, or code review succeeded. Those are supporting evidence, not substitutes for missing end-to-end evidence.

不要因为 lint、类型检查、单元测试或代码审查通过，就把“未验证”写成“通过”。它们是支撑证据，不能替代缺失的端到端证据。

## User acceptance / 用户亲自验收

Ask the user to perform a final check only when the check depends on their account, judgment, physical device, private data, or production authority. Give exact steps and the expected result.

只有验收依赖用户账号、主观判断、实体设备、私有数据或生产权限时，才交给用户亲自确认。必须给出准确步骤和预期结果。

```markdown
## Please verify / 请您确认

1. Open / 打开:
2. Do / 操作:
3. Expect / 应看到:
4. If different / 若不一致:
```

## Final handoff / 最终交付

Use this order:

1. **Closure / 闭环状态** — closed, not closed, or blocked, with one reason tied to the requested delivery level.
2. **Delivered / 已交付** — the business outcome and boundary actually reached.
3. **Evidence / 证据** — the most important observed checks.
4. **Impact / 影响** — who or what changes.
5. **Open risk / 剩余风险** — failed or unverified items only.
6. **Next action and owner / 下一步及责任人** — write `none—closed` when closed; otherwise name Codex, User, or the external owner.
7. **User decision / 是否需要用户决定** — `not needed`, or one exact decision with a recommended answer and consequence.

Avoid long implementation diaries. Link to durable project files when the user may need details later.

避免提交冗长的实施流水；需要长期保留的细节应链接到项目文件。
