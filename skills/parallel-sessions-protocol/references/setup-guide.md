# Setup from zero (and the traps)

## 1. Prerequisites

- git ≥ 2.30 (worktree support matured)
- GitHub CLI: `brew install gh` (macOS) / see github.com/cli/cli for others
- A GitHub remote on the repository (`git remote -v` shows a github.com URL)

## 2. Authenticate `gh`

```bash
gh auth login        # choose GitHub.com → HTTPS → login with browser
gh auth status       # verify: must show "Logged in to github.com"
```

Trap: on a machine with multiple accounts, `gh` uses one active account per
host. `gh auth switch` changes it. A PR opened under the wrong account still
works but confuses the board's "who owns this track" reading.

## 3. Worktree basics

```bash
# create a worktree for a new track (from the repo root)
git worktree add ../my-track-wt -b feature/20260805/my-track origin/main

# list all worktrees (do this when debugging "branch is already checked out")
git worktree list

# remove when the track ends
git worktree remove ../my-track-wt
```

Traps learned in production:

- **Never leave a worktree checked out on `main`.** Git refuses to check out
  a branch that any worktree holds, so a worktree parked on main blocks
  every other session's `gh pr merge --delete-branch`, `git checkout main`,
  etc. If you hit `fatal: 'main' is already used by worktree at ...`, that
  is the cause — find it with `git worktree list`.
- Before removing a worktree that might not be yours: verify it is clean
  (`git -C <path> status --porcelain` prints nothing) and coordinate with
  its session or the owner first.
- A detached HEAD (`git checkout --detach origin/main`) is the polite way to
  park a checkout you are done with — it holds no branch hostage.

## 4. The MERGEABLE trap

`gh pr view N --json mergeable,mergeStateStatus` and the GitHub UI both
compute mergeability against a **cached** base. After main moves, a branch
that now conflicts can still show `MERGEABLE / CLEAN` for a while.

Always preview locally before requesting or performing a merge:

```bash
git fetch origin
git merge origin/main --no-commit --no-ff   # on your track branch
git merge --abort                            # if you only wanted the preview
```

If the preview conflicts on shared ledger files, resolve by **keeping both
sides in full**, never by picking one.

## 5. Force-push after rebase

Rebasing a pushed branch rewrites history; the next push is rejected as
non-fast-forward. Use:

```bash
git push --force-with-lease
```

`--force-with-lease` fails if the remote moved since your last fetch —
protecting a concurrent update — while bare `--force` would silently
destroy it.

## 6. Optional notification webhook

If the team wants merge announcements or CI alerts in chat (Feishu / Slack):

```bash
# put the webhook in a gitignored env file, never in the repo
echo 'NOTIFY_WEBHOOK_URL=<paste the webhook URL here>' >> .env.local
```

Feishu bots accept:

```bash
curl -X POST "$NOTIFY_WEBHOOK_URL" -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"<message>"}}'
```

Treat the URL as a credential (anyone holding it can post to the group).
Never commit it, never embed it in a skill, and rotate it via the chat
platform's bot settings if it leaks.
