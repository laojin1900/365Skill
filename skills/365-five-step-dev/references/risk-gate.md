# Protected-Action Gate / 受保护操作闸门

Use this gate only at a real protected boundary. Do not block read-only inspection, source edits, tests, builds, fixtures, local previews, or other reversible preparation already within the user's request.

只在真实的受保护边界使用本闸门。不要阻塞用户需求范围内的只读检查、源码编辑、测试、构建、样例数据、本地预览或其他可逆准备。

## Protected boundaries / 受保护边界

Treat the following as protected when they change real external state or expose sensitive information:

以下行为一旦会改变真实外部状态或暴露敏感信息，即属于受保护操作：

- production deployment, infrastructure mutation, DNS or runtime configuration;
- 生产部署、基础设施变更、DNS 或运行配置修改；
- applied database migration, schema change, destructive query, or permission-policy change;
- 实际执行数据库迁移、结构修改、破坏性查询或权限策略变更；
- payment, order, inventory, pricing, customer, employee, or regulated-data mutation;
- 支付、订单、库存、价格、客户、员工或受监管数据变更；
- bulk create, update, delete, publish, archive, email, message, or notification;
- 批量新建、修改、删除、发布、归档、邮件、消息或通知；
- destructive filesystem or Git action, force push, history rewrite, or deleting a shared resource;
- 破坏性文件或 Git 操作、强推、改写历史或删除共享资源；
- reading, copying, printing, or transmitting credentials, private keys, tokens, or unnecessary personal data;
- 读取、复制、输出或传输凭证、私钥、令牌或非必要个人数据；
- any action whose target or consequence materially exceeds the user's stated scope.
- 目标或后果实质超出用户已说明范围的任何操作。

## Approval packet / 审批说明

Before an unapproved protected action, present one compact packet:

在尚未获得授权的受保护操作前，只提交一份简洁说明：

```markdown
## Approval needed / 需要确认

- Action / 操作:
- Exact target / 准确目标:
- Business effect / 业务影响:
- Data or people affected / 影响的数据或人员:
- Reversibility / 是否可逆:
- Rollback / 回滚办法:
- Verification after action / 操作后如何验证:
- Recommendation / 建议:
```

Ask for confirmation only after Codex has inspected enough context to make a recommendation. Do not ask the user to approve an unknown target, an unspecified command, or a consequence Codex has not assessed.

先查清上下文并形成建议，再请求确认。不要让用户审批未知目标、未说明的命令或尚未评估的后果。

## Existing authorization / 已有授权

A current user request is sufficient authorization when it clearly names the action, exact
target, intended business outcome, and scope. Bind that boundary before acting, but do not
ask the same question again.

当用户当前请求已明确操作、准确目标、业务结果和范围时，即构成有效授权。执行前绑定该边界，
但不要重复询问。

Request fresh confirmation when:

以下情况需要重新确认：

- the target changes;
- 目标发生变化；
- the affected population or record count grows materially;
- 影响人群或数据量显著扩大；
- a reversible action becomes irreversible;
- 可逆操作变为不可逆；
- the rollback plan becomes unavailable;
- 回滚办法失效；
- the permission or credential boundary changes materially;
- 权限或凭据边界发生实质变化；
- the user's intent changes or the user pauses or cancels the goal;
- 用户意图变化，或用户暂停、取消目标；
- the observed data conflicts with the approved assumptions.
- 实际数据与获批前提冲突。

## Execution discipline / 执行纪律

1. Execute only the approved action and target.
2. Capture a durable, non-secret receipt when the system provides one.
3. Verify the business effect immediately.
4. Stop on mismatched counts, permissions, identities, environment, or target.
5. Report partial completion precisely; do not retry a protected mutation blindly.

1. 只执行已授权的操作和目标。
2. 系统提供回执时，保留不含秘密的持久回执。
3. 操作后立即核验业务效果。
4. 数量、权限、身份、环境或目标不一致时立刻停止。
5. 准确报告部分完成状态，不盲目重试受保护变更。
