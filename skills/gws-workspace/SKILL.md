---
name: gws-workspace
description: Operate Google Workspace — Gmail, Calendar, Drive, Sheets, Docs, Slides, Chat, Tasks — through the gws CLI (github.com/googleworkspace/cli) with read-by-default safety gates. Use when the user mentions gws, Gmail, email inbox/send/reply/triage, 邮件/收件箱/发邮件/未读邮件, Google Calendar, 日程/日历/创建会议, Google Drive, 谷歌网盘/上传 Drive, Google Sheets, 谷歌表格, Google Docs, 谷歌文档, or asks for Google Workspace automation such as daily/weekly mail+calendar digests (邮件汇总/日程周报). Also use when installing gws, configuring its OAuth client, or troubleshooting gws authentication errors.
---

# gws Workspace Operations

Operate a user's Google Workspace account through the `gws` CLI — one binary
covering every Workspace API, built dynamically from Google's Discovery
Service, with structured JSON output. It is open source (Apache-2.0) but **not
an officially supported Google product** and is pre-v1: expect breaking
changes and pin versions in production.

## Preflight

Before the first gws call in a session:

```bash
gws auth status --format json
```

- `auth_method: "oauth2"` or `service_account` → proceed.
- `auth_method: "none"` → stop. Follow `references/setup-guide.md` with the
  user to install gws and complete OAuth. Never invent client IDs, client
  secrets, or tokens; OAuth setup requires real user actions in the Google
  Cloud Console.
- `command not found` → install: `npm install -g @googleworkspace/cli`
  (alternatives: `brew install googleworkspace-cli`, cargo, nix).

The stderr line `Using keyring backend: keyring` is informational, not an
error. Parse stdout only.

## Command Model

Two surfaces; prefer helper commands when one fits.

**Helper commands (`+` prefix, hand-written):**

| Service | Command | Purpose |
| --- | --- | --- |
| gmail | `+send --to A --subject S --body B` | Send email |
| gmail | `+reply --message-id ID --body B` | Reply (threads automatically) |
| gmail | `+triage` | Unread inbox summary |
| gmail | `+watch` | Stream new mail as NDJSON |
| calendar | `+agenda [--today] [--timezone TZ]` | Upcoming events |
| calendar | `+insert` | Create an event |
| drive | `+upload ./file --name N` | Upload a file |
| sheets | `+read --spreadsheet ID` | Read values |
| sheets | `+append --spreadsheet ID --values "a,b"` | Append a row |
| docs | `+write` | Append text to a document |
| chat | `+send` | Message a space |
| workflow | `+standup-report`, `+weekly-digest`, `+meeting-prep` | Composite digests |

**Discovery commands (full API surface):**

```bash
gws <service> <resource> <method> --params '{"k":"v"}'   # query/path params
gws <service> <resource> <method> --json '{"k":"v"}'     # request body
gws schema gmail.users.messages.list                     # inspect any method
gws gmail --help                                         # live command list
```

- Message metadata: request `format: "metadata"` plus
  `metadataHeaders: ["Subject","From","Date"]`; body parts are base64url in
  `payload.body.data` / `payload.parts`.
- Gmail search uses standard `q` operators (`is:unread`, `newer_than:7d`,
  `after:2026/07/01 before:2026/07/08`).
- Useful flags: `--format json|table|yaml|csv`, `--page-all` (NDJSON
  pagination), `--output <path>` (binary download), `--upload <path>`.

## Safety Gates

- **Read freely.** list/get/triage/agenda/read need no confirmation.
- **Confirm externally visible actions.** Before `gmail +send/+reply/+forward`,
  `chat +send`, or creating calendar events that invite guests, restate the
  recipients, subject, and body summary; execute only after explicit approval.
- **Confirm destructive actions.** Deleting mail, Drive files, or events, and
  modifying existing events or documents, require explicit approval with the
  target ID shown.
- **Least privilege.** Request only the scopes the task needs during
  `gws auth login`; start read-only and expand. Never print credentials,
  tokens, or `~/.config/gws/` contents into chat output.
- Timezone: `+agenda` uses the Google account timezone; pass `--timezone`
  explicitly when the user expects another zone.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Access blocked` / `access_denied` | Consent screen in testing mode, account not a test user | Add the account under Google Auth Platform → Audience → Test users |
| Token refresh fails | Stale encrypted credentials | Delete `~/.config/gws/credentials.enc`, re-run `gws auth login` |
| Scope/permission errors | Scope not granted at login | Re-run `gws auth login` with the needed scopes (incremental) |
| Method not found | Discovery document cached or new API | `gws <service> --help`; commands are generated at runtime from the live Discovery Service |
| No OAuth client / lost secret | Google shows a client secret only once, at creation | Create a new Desktop client and download the JSON immediately — see `references/setup-guide.md` |

## References

- `references/setup-guide.md` — from-zero install and OAuth setup: GCP
  project, consent screen, Desktop client, the secret-visible-once policy,
  test users, headless/CI credentials, and service accounts. Read it whenever
  `gws auth status` is not `oauth2` or the user asks to install gws.
