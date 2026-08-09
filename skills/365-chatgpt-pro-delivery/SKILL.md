---
name: 365-chatgpt-pro-delivery
description: Coordinate one bounded collaboration between Codex and an explicitly requested ChatGPT Pro workspace. Use when the user asks Codex to consult ChatGPT Pro, obtain a Pro review, combine Pro research or creative work with Codex verification, or divide a named deliverable between the two, including an explicitly requested review of local work. Do not invoke for ordinary ChatGPT questions, local-only work that does not request Pro, or when the user forbids external transmission.
---

# 365 ChatGPT Pro Delivery / 365 ChatGPT Pro 协作

Obtain one useful independent contribution from ChatGPT Pro while Codex keeps ownership of
scope, privacy, repository evidence, integration, verification, and final claims.

从 ChatGPT Pro 获取一次边界清晰的独立贡献；范围、隐私、代码证据、整合、验证和最终结论
始终由 Codex 负责。

## Core contract / 核心约定

- Match the user's language.
- Use Pro only because the user requested it or because the current request explicitly asks
  for this skill.
- Send the minimum sanitized context needed for the named outcome. Never send secrets,
  credentials, cookies, private keys, raw PII, private URLs, or unrelated proprietary data.
- Codex owns implementation and acceptance. Pro output is a candidate, not environment
  evidence and not authorization for code, Git, deployment, publication, live-data writes,
  purchases, or outreach.
- One approved collaboration goal permits one bounded dispatch and necessary readback. Ask
  again only if the recipient, sensitivity, scope, or external effect changes materially.
- Respect `do not transmit`, `offline only`, and equivalent instructions as a hard stop.

- 跟随用户语言；只在用户明确要求时调用 Pro。
- 只发送完成目标所需的最小去敏内容，绝不发送秘密、凭证、Cookie、私钥、原始个人数据、
  私有链接或无关专有资料。
- Pro 的输出只是候选结果，不代表本地验证，也不授权代码、Git、部署、公开发布或真实数据写入。

## 1. Choose one lane / 选择一种协作路线

Choose by evidence need, not by apparent complexity:

1. **FAST_DELIVERY** — images, copy, document drafts, supplied-evidence synthesis, strategy,
   or lightweight expert review that needs no new external facts.
2. **RESEARCH_DELIVERY** — current or specialist external facts can materially change the
   decision. Require visible sources and dates.
3. **ENGINEERING_DELIVERY** — Codex expects source changes, file-specific review, test ideas,
   or runtime guidance. Supply only the narrow source and contracts needed for correctness.

If engineering evidence is incomplete, request `REVIEW_ONLY`; do not invite an exact patch
against files or APIs Pro could not inspect.

## 2. Build the smallest complete brief / 准备最小完整任务包

Every dispatch includes:

```text
Dispatch marker:
Goal:
Lane:
Evidence supplied:
Evidence not supplied:
Required output:
Hard constraints:
Acceptance criteria:
```

Keep a complete short brief inline. When detailed context is necessary, use one sanitized
Markdown attachment and a short instruction to read it; do not duplicate the full packet in
the message. Record the attachment filename, visible path scope, byte size, and SHA-256.

Read [references/briefs-and-acceptance.md](references/briefs-and-acceptance.md) for lane
templates and the acceptance checklist.

## 3. Select one available surface / 选择一个可用通道

Prefer the narrowest surface that can send and read the selected payload:

1. a dedicated ChatGPT task or conversation exposed by the current Codex environment;
2. the in-app browser when the ChatGPT webpage or visible attachment UI is required;
3. the user's Chrome session only when its existing login or extension state is necessary;
4. user copy-and-paste when no authorized direct channel is available.

Before declaring a surface unavailable, inspect the callable capabilities actually present.
When browser control is selected, load and follow its browser-control skill. Do not read,
request, or automate passwords, passkeys, CAPTCHA, or MFA; ask the user to complete login.

Use a new or marker-dedicated conversation for an independent first round. Reuse an existing
conversation only when the user explicitly asks to continue it or the history is bounded to
the same outcome.

## 4. Dispatch once and prove it / 单次发送并确认

- Put one unique marker in the request.
- Send once through the selected surface.
- A send receipt proves only acceptance by the transport. Confirm the marker is visible in
  the intended conversation before recording dispatch.
- If send status is ambiguous, read back the same conversation once. Never send the same
  packet to two surfaces or create duplicate conversations while the first may be active.
- Wait without repeatedly rereading the full conversation. Preserve the same marker and
  conversation for one correction round.

If no result can be read safely, stop with the exact transport state and give the user the
prepared sanitized brief for manual dispatch. Do not weaken privacy or evidence rules merely
to avoid a blocked outcome.

## 5. Require evidence-labelled output / 要求证据标签

Ask Pro to begin with the marker and an access declaration. Material claims use:

- `DIRECT` — supported by supplied or visibly inspected evidence;
- `INFERRED` — reasoned but not directly confirmed;
- `ILLUSTRATIVE` — example, concept, mockup, or pseudocode;
- `UNVERIFIED` — not confirmable from available evidence.

Release-blocking claims require `DIRECT` evidence. Pro must not claim it ran commands, opened
files, visited sources, or tested runtime behavior that it could not access.

## 6. Codex accepts, corrects, or rejects / Codex 独立验收

Codex independently checks the result against the user's goal and real local evidence:

```text
ACCEPTED_UNCHANGED
ACCEPTED_WITH_LOCAL_EDIT
RETURN_TO_PRO
REJECTED
UNVERIFIED
```

Fix small wording and integration details locally. If new reasoning is required, send one
delta correction in the same conversation containing the observed evidence, violated
constraint, and required correction. Do not resend accepted context. A further round requires
new material evidence or explicit user direction.

Never claim completion from Pro self-report alone. Run the repository, artifact, source, or
business checks appropriate to the actual deliverable.

## 7. Close at the authorized boundary / 按授权边界收尾

Report:

- requested outcome and selected lane;
- surface and conversation identifier or URL when available;
- sanitized evidence supplied;
- accepted, edited, rejected, and unverified content;
- Codex's independent checks;
- actual file, Git, publication, or release state;
- next action and owner when the requested outcome is not yet closed.

Do not publish, merge, deploy, message third parties, or perform a live write unless the
user's request separately authorizes that exact effect.
