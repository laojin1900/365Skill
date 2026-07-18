---
name: gws-weekly-digest
description: 生成每周邮件+日程晨报/周报：用 gws CLI（或等效邮件/日历命令行）汇总上一周的邮件（总量、未读、重点发件人、疑似待回复）和本周（今日起七天）的日历日程，输出结构化中文或英文 markdown 晨报，并给出本周关注建议。当用户说「周报」「晨报」「每周邮件汇总」「周一晨报」「帮我汇总上周邮件和本周日程」「weekly digest」「Monday briefing」「weekly email+calendar summary」「邮件日程周报」时触发；也用于搭建此类定时摘要自动化。不用于：发送邮件、修改日历、实时邮件处理、非 Google 系的邮件/日历系统（Outlook/Exchange 需另行适配）。
---

# gws Weekly Digest

Produce a recurring weekly briefing from a user's mailbox and calendar:
last week's mail statistics plus the next seven days of events, rendered as
a structured markdown digest with attention recommendations.

Default posture: **strictly read-only**. Never send, delete, or modify mail
or events while producing a digest.

## Prerequisites

- `gws` CLI installed and authenticated (`gws auth status` → `oauth2`).
  If not, stop and point the user to the gws setup; do not attempt OAuth
  yourself. The stderr line `Using keyring backend: keyring` is normal.
- A scheduler if the digest should recur (cron, an agent automation
  platform, or CI). This skill produces the digest; scheduling is the
  host environment's job.

## Data Collection

1. **Week boundaries first.** Compute from the run date in the user's
   timezone: last week = previous Monday 00:00 → this Monday 00:00;
   events window = today 00:00 → +7 days. State both windows in the output.
2. **Mail stats** (Gmail `q` operators):

   ```bash
   gws gmail users messages list --params '{"userId":"me","q":"after:YYYY/MM/DD before:YYYY/MM/DD","maxResults":100}'
   gws gmail users messages list --params '{"userId":"me","q":"after:YYYY/MM/DD before:YYYY/MM/DD is:unread","maxResults":100}'
   ```

   Sample up to ~30 messages (prioritize unread, skip noreply/newsletter
   senders) with `format: "metadata"` and
   `metadataHeaders: ["Subject","From","Date"]` for the reply-candidate list.
3. **Calendar**:

   ```bash
   gws calendar events list --params '{"calendarId":"primary","timeMin":"...","timeMax":"...","singleEvents":true,"orderBy":"startTime","maxResults":50}'
   ```

   Use RFC3339 timestamps with explicit offset. Group events by day.

## Output

Write the full digest to `weekly-digest/gws-<run-date>.md` under the current
workspace using the structure in `references/digest-template.md`:

1. mail overview (totals, unread share, top senders table)
2. reply candidates (≤5, with sender/subject/date and why it matters)
3. events grouped by day
4. cross-analysis: 1–3 attention items linking mail threads to upcoming
   events (e.g. a thread that should be answered before a meeting)

Then return a ≤15-line chat summary: key numbers, top reply candidates,
schedule highlights, recommendations. The markdown file is the durable
artifact; the chat reply is the glanceable layer.

## Recurrence Guidance

- Weekly cadence: Monday morning in the user's timezone. Avoid minute `:00`
  and `:30` for scheduled jobs; pick a stable off-peak minute (7–23 or
  37–53) unless the user asked for an exact time.
- If multiple Monday automations exist, stagger them by ≥30 minutes.
- A weekly digest pairs naturally with a completion notification; offer it,
  but only when the user wants one.

## Failure Handling

- Auth missing/expired → report and stop; never retry OAuth in the
  background.
- Empty calendar or zero mail → still write the digest and say so; an empty
  week is a valid result, not an error.
- Partial API failure → mark the affected section as unavailable, keep the
  rest, and note it in the summary.
