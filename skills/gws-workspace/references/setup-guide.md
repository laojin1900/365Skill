# gws Setup Guide

From-zero install and OAuth configuration for the `gws` CLI
(`github.com/googleworkspace/cli`). Read this when `gws auth status` does not
report `oauth2`, or when the user asks to install gws.

Contents: Install → GCP project → Consent screen → Test users → OAuth client →
Login → Headless/CI → Verify.

## 1. Install

```bash
npm install -g @googleworkspace/cli   # prebuilt binaries, Node 18+
brew install googleworkspace-cli      # macOS/Linux Homebrew
```

Verify with `gws --version`.

## 2. GCP Project

gws needs a Google Cloud project to hold OAuth credentials. Create a dedicated
one (keeps the consent screen separate from other apps):

```bash
gcloud auth login                       # browser flow, once
gcloud projects create gws-cli-<name> --name="gws-cli"
gcloud config set project gws-cli-<name>
```

No `gcloud`? Create the project in the Cloud Console instead. `gws auth setup`
can automate API enablement but **cannot create the OAuth client** — Google
removed programmatic client creation, so the console steps below are always
required.

## 3. Consent Screen (Google Auth Platform)

Open `https://console.cloud.google.com/auth/overview?project=<PROJECT_ID>`:

1. **Get started** → App info: any app name (e.g. `gws CLI`), support email =
   the user's own address.
2. **Audience: External.** (Internal requires a Workspace org.)
3. **Contact info:** the user's email. This field is a *chip input* — type the
   address and press **Enter** so it becomes a chip, or validation fails.
4. Agree to the user data policy → **Create**.

## 4. Test Users (Required)

While the consent screen stays in **Testing** status, only listed test users
can authorize. Missing this step causes a generic `Access blocked` error at
login.

Go to **Audience** → **Add users**, add the Google account(s) that will use
gws (again a chip input — press Enter), and save.

## 5. OAuth Client — Secret Is Visible Only Once

1. Go to **Clients** → **Create client** → application type **Desktop app**;
   any name.
2. The creation dialog shows the client ID and a **Download JSON** button.
   **Download it immediately.** Since 2025 Google never shows or re-downloads
   a client secret after creation — the detail page masks it (`****-xxxx`).
3. If the secret was not captured, there is no recovery: **create a new
   Desktop client** and download the JSON at creation. (Adding a secret to an
   existing client also reveals it only at that moment.)
4. Install the file:

```bash
mkdir -p ~/.config/gws && chmod 700 ~/.config/gws
mv ~/Downloads/client_secret_*.json ~/.config/gws/client_secret.json
chmod 600 ~/.config/gws/client_secret.json
```

Equivalent: export `GOOGLE_WORKSPACE_CLI_CLIENT_ID` and
`GOOGLE_WORKSPACE_CLI_CLIENT_SECRET`.

## 6. Login

```bash
gws auth login
```

- Complete the browser flow with a test-user account.
- "Google hasn't verified this app" (testing mode) → **Continue**.
- If scope checkboxes appear, select the required scopes (or Select all).
- Start with read-oriented scopes; re-run `gws auth login` later to add more —
  grants are incremental.

Credentials are stored AES-256-GCM encrypted at
`~/.config/gws/credentials.enc` (key in the OS keyring on macOS/Windows; a
local `.encryption_key` fallback on headless Linux).

## 7. Headless / CI

Authenticate interactively once, then export and move the file:

```bash
gws auth export --unmasked > credentials.json   # protect this file
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/credentials.json
gws drive files list                            # works without a browser
```

For server-to-server inside a Workspace organization, use a service account
JSON with domain-wide delegation via the same
`GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` variable — no login needed.

## 8. Verify

```bash
gws auth status --format json                 # auth_method: oauth2
gws drive files list --params '{"pageSize": 1}'
gws calendar +agenda
```

New consent-screen/client settings can take ~5 minutes to propagate; retry
once before reconfiguring.
