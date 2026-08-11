# Workspace and Delivery Hygiene / 工作区与交付卫生

Use this reference only when the worktree is mixed or dirty, change ownership is unclear,
safe isolation is needed, or delivery has special Git/release handling. Routine clean
work requires one status inspection, not this full reference. The goal is to make
Codex—not the non-coding user—responsible for change ownership and delivery completeness.

只有工作区混合或脏、改动归属不清、需要安全隔离，或者交付存在特殊 Git/发布处理时才读取。
普通干净任务只需检查一次状态，不必加载整份参考。目标是让 Codex，而不是不懂代码的用户，
负责改动归属和交付完整性。

## Contents / 目录

1. [Capture a baseline before editing / 编辑前记录基线](#1-capture-a-baseline-before-editing--编辑前记录基线)
2. [Classify every pre-existing change / 给已有改动分类](#2-classify-every-pre-existing-change--给已有改动分类)
3. [Isolate writable work / 隔离写入任务](#3-isolate-writable-work--隔离写入任务)
4. [Maintain a deliverable change set / 保持改动集可交付](#4-maintain-a-deliverable-change-set--保持改动集可交付)
5. [Deploy from an exact clean revision / 从准确干净版本部署](#5-deploy-from-an-exact-clean-revision--从准确干净版本部署)
6. [Close out with separate states / 分开报告各类状态](#6-close-out-with-separate-states--分开报告各类状态)

## 1. Capture a baseline before editing / 编辑前记录基线

Inspect the repository before the first write:

- current repository, branch, HEAD, upstream, and ahead/behind state;
- tracked modifications, staged changes, and untracked paths;
- active worktrees or project-specific task directories;
- existing task, commit, PR, release, and deployment instructions.

第一次写入前检查：当前仓库、分支、HEAD、上游及领先/落后状态；已修改、已暂存和未跟踪路径；现有工作树或任务目录；任务、提交、PR、发布和部署规则。

Record the path-level baseline in working memory or the project's existing task ledger. Do not paste full diffs, secrets, or hidden reasoning into a log.

在工作记忆或项目既有任务账本中记录路径级基线，不把完整 diff、秘密或隐藏推理写进日志。

## 2. Classify every pre-existing change / 给已有改动分类

Classify each path into one of these buckets:

| Class | Meaning | Action |
|---|---|---|
| Current task / 本任务 | Created or changed for the approved outcome | May edit, stage, test, and commit |
| Related pre-existing / 相关旧改动 | Existed before this task but is necessary for it | Inspect provenance and include only with evidence |
| Unrelated owned / 有归属的无关改动 | Belongs to another task, branch, or person | Preserve; never stage or modify |
| Generated / 生成物 | Reproducible build, cache, or tool output | Follow repository cleanup/ignore rules |
| Unknown / 归属未知 | Ownership cannot yet be established | Inspect history, diff shape, task docs, branches, and worktrees before escalating |

Codex must do the investigation. Do not ask the user “Whose files are these?” unless repository evidence is exhausted and the answer materially changes a destructive or external action. When escalation is unavoidable, present the likely owner and recommended next action.

归属调查由 Codex 完成。只有仓库证据全部查尽、且答案会实质影响破坏性或外部操作时，才能问用户“这些文件是谁的”；提问时必须附最可能归属和推荐处理方式。

## 3. Isolate writable work / 隔离写入任务

When the current worktree contains unrelated or unknown changes:

1. Preserve it exactly; do not reset, stash, overwrite, or commit those paths.
2. Prefer an existing clean task worktree when one is documented.
3. Otherwise create a dedicated branch/worktree from the correct base when safe and permitted.
4. If isolation is impossible, keep an explicit path allowlist for the current task and stage only those paths.

当前工作区存在无关或未知改动时：保持原样，不 reset、stash、覆盖或提交；优先使用已有干净任务工作树；否则在规则允许时从正确基线创建独立分支/工作树；无法隔离时，为本任务维护明确路径白名单，只暂存这些路径。

Do not treat a dirty canonical directory as proof that deployment is impossible. It proves only that deployment must not consume that directory blindly.

canonical 目录不干净，不等于无法部署；它只说明不能直接使用该目录进行部署。

## 4. Maintain a deliverable change set / 保持改动集可交付

- Commit only when the requested delivery level includes a commit or shared Git delivery;
  do not infer commit authority from a request for local file changes.
- In a mixed worktree, never use broad staging that can absorb unrelated paths.
- Before push or PR creation, compare the committed diff with the approved scope.
- After merge, record the exact merged commit and verify that no current-task paths remain only in a local worktree.
- Do not label the coding task complete when intended task changes remain uncommitted, unpushed, or outside the reviewed PR, unless that delivery level was explicitly agreed.

- 只有用户要求的交付层级包含提交或共享 Git 交付时才创建提交；不要从本地文件修改推断提交授权。
- 混合工作区中不得使用会吸收无关路径的宽泛暂存。
- 推送或创建 PR 前，用获批范围核对已提交 diff。
- 合并后记录准确合并提交，并确认没有本任务文件只留在本地工作区。
- 如果本任务改动仍未提交、未推送或没有进入已审查 PR，除非双方明确只交付到该层级，否则不得宣称开发完成。

Unrelated residue does not make the current task incomplete. Report it separately with classification and ownership; do not transfer the cleanup burden to the business user.

无关残留不代表当前任务未完成。应单独报告其分类和归属，不把清理责任转交给业务用户。

## 5. Deploy from an exact clean revision / 从准确干净版本部署

Before deployment:

1. Identify the reviewed and merged commit intended for release.
2. Confirm target environment, build inputs, migration state, and rollback.
3. When the canonical worktree is dirty, use a clean isolated worktree or fresh checkout at the exact commit if repository policy permits.
4. Run preflight, build, and release verification in that clean context.
5. Keep unrelated local changes untouched.
6. Remove only temporary resources created by the current task after evidence is captured.

部署前：确定准备发布的已审查、已合并提交；核对环境、构建输入、迁移状态和回滚；canonical 工作区不干净时，在项目规则允许的情况下从准确提交创建干净隔离工作树或全新检出；在该环境完成预检、构建和发布验证；不触碰无关本地改动；留存证据后只清理本任务创建的临时资源。

If the runbook truly requires the dirty canonical directory, diagnose which exact files or local-only dependencies make it mandatory. Report the technical blocker, likely owner, and recommended resolution—never a vague “clean the worktree and tell me when done.”

如果运行手册确实强制使用不干净的 canonical 目录，要查明究竟哪些文件或本地依赖导致无法隔离，并报告准确技术阻塞、最可能责任归属和推荐解法，不得只说“请清理工作区后告诉我”。

## 6. Close out with separate states / 分开报告各类状态

Never compress coding, Git delivery, deployment, and workspace hygiene into one “done” label.

不要把编码、Git 交付、部署和工作区卫生压缩成一个“已完成”。

Determine closure against the delivery level implied or explicitly requested by the user:

- **Closed**: the requested outcome is reached and verified; no required action remains.
- **Not closed**: an intermediate state remains, including local-only, committed but
  unpushed, PR open, unmerged, merged but not deployed, or deployed but not verified.
- **Blocked**: a named external condition, missing authority, or material decision prevents
  continued progress.

按用户明确要求或业务结果隐含的交付层级判断闭环：已经到达并验证且无必做事项剩余，
才是“已闭环”；停在本地、未推送、PR 未合并、已合并未部署、已部署未验证等中间状态，
都是“未闭环”；只有明确的外部条件、权限或重大决策无法继续时，才是“已阻塞”。

```markdown
## Delivery state / 交付状态

- Closure / 闭环状态: closed | not closed | blocked
- Closure reason / 判断理由:
- Business outcome / 业务结果:
- Intended delivery level / 目标交付层级:
- Reached boundary / 已到达层级:
- Code / 代码: local only | committed <sha> | pushed <branch> | PR <url> | merged <sha>
- Release / 发布: not requested | awaiting approval | deployed <environment/version> | verified
- Current-task remainder / 本任务遗留: none | <paths and next action>
- Other workspace changes / 其他工作区改动: none | <classification, likely owner, preservation status>
- Evidence / 证据:
- Next required action / 下一步必做动作: none | <one concrete action>
- Next owner / 下一步责任人: none—closed | Codex | User | <named external owner>
- User decision / 是否需要用户决定: not needed | <one exact decision>
- Recommendation / 推荐决定及影响:
```

If safe authorized work remains, own and execute the next action before sending a final
handoff. Ask the user only at a real approval boundary. When asking, provide one copy-ready
authorization sentence that names the action, target, and intended stopping point.

如果仍有安全且已授权的必做事项，由 Codex 先执行再发送最终交付；只有到了真实审批
边界才询问用户。询问时提供一句可直接复制的授权语，写清操作、目标和推进终点。
