---
name: model-subscription-api-dual-channel
description: Design and implement a multi-channel model registry + smart sorting for any AI coding agent. Use when setting up a model catalog/model selector in a new agent, gateway, or frontend, or when the user wants to replicate Pi Web's "subscription vs pay-per-use API" dual-channel design and its usage-driven top-of-list sorting. Separates subscription-quota providers (google-vip / kimi-vip / xai-subscription) from pay-as-you-go API providers (google / deepseek / openrouter), unifies everything onto OpenAI-compatible endpoints, builds requests from per-vendor compat flags, and orders models by flag-vendor weight + local usage frequency + natural collation, grouped by provider with short badges. Skip for web-scraping/web-automation model channels (gweb) — those lack tool calling and collapse on long contexts.
version: 1
created: "2026-08-17"
updated: "2026-08-17"
---

# Model Subscription / API Dual-Channel Design & Smart Sorting

Reusable recipe for building a model registry and picker where **subscription-quota
models and pay-per-use API models live side by side but stay strictly separated**, and
where the model list is ordered by what the user actually runs.

This is the pattern used by Pi Web's model picker (ChatInput + models.json +
discover route + model-usage). The same contract can be re-implemented in any
agent, gateway, or frontend.

## When to Use

Use when you are:

1. Building a model catalog / model selector for any agent, gateway, or frontend,
2. asked to replicate Pi Web's "subscription vs API" dual-channel model design or its
   smart ordering,
3. integrating with a subscription gateway (OmniRoute / new-api / allmodelsapi.com)
   that exposes OpenAI-compatible endpoints,
4. deciding how to order models and show provider badges / quota.

Do **not** use this for web-scraping or browser-automation model channels (`gweb`,
Playwright-driven gemini.google.com): those have no tool-calling and collapse on long
context (repeated/degenerate output, 150w-token inputs). They are not a real API.

## Procedure

### 1. Define channels — one Provider per channel kind

One Provider instance per channel. **Never mix subscription and API models in the
same provider.**

- Subscription-quota providers get a `-vip` / `-subscription` suffix:
  `google-vip`, `kimi-vip`, `xai-subscription`.
- Pay-per-use API providers use a bare or `-api` name:
  `google`, `deepseek`, `openrouter`, `xai-api`.
- `openai-codex` (OAuth subscription), `omniroute` (smart gateway) are special.

Keep the IDs as the contract. The display name is resolved separately (see step 5).

### 2. Author models.json (credential-free)

```jsonc
{
  "providers": {
    "google-vip": {
      "baseUrl": "https://allmodelsapi.com/v1",
      "api": "openai-completions",
      "authHeader": true,
      "models": [
        {
          "id": "antigravity/gemini-3.5-flash-high",
          "name": "Gemini 3.5 Flash (High) (Google AI Pro订阅)",
          "reasoning": true,
          "input": ["text", "image"],
          "contextWindow": 1048576,
          "maxTokens": 65536,
          "compat": { "supportsDeveloperRole": false, "supportsReasoningEffort": false }
        }
      ]
    },
    "kimi-vip": {
      "baseUrl": "https://allmodelsapi.com/v1",
      "api": "openai-completions",
      "authHeader": true,
      "models": [
        {
          "id": "kimi-coding/k3",
          "name": "Kimi K3 (Kimi Coding订阅)",
          "reasoning": true,
          "input": ["text", "image"],
          "contextWindow": 1048576,
          "maxTokens": 131072,
          "compat": {
            "supportsDeveloperRole": false,
            "supportsReasoningEffort": true,
            "requiresReasoningContentOnAssistantMessages": true
          }
        }
      ]
    }
  }
}
```

Contract notes:

- `providers.<id>` — the channel identity; globally unique.
- `models[].id` **must include the gateway prefix** (`antigravity/`, `kimi-coding/`).
  This is what routes to the right upstream in OmniRoute/new-api.
- `reasoning`, `input`, `contextWindow`, `maxTokens` drive the picker (badges, filters,
  token budget).
- optional advanced fields: `thinkingLevelMap` (map `off/max` levels to vendor strings or
  `null`; drives reasoning depth — non-reasoning models are `["off"]` only, `xhigh/max` only if
  explicitly mapped), `cost` (per-1M-token `input/output/cacheRead/cacheWrite` + optional
  `tiers[]` for usage-based rate tiers; `calculateCost` picks the tier by input tokens and gives
  the session `$` cost), model-level `headers`/`api`/`baseUrl`/`apiKey` overrides.
- `compat` drives request construction (see step 6).
- Keep the file **credential-free**; store keys separately in `auth.json`.

### 3. Model discovery — never fabricate prefixed IDs

For subscription channels, fetch the model list from the gateway catalog and filter by
the **exact prefix** of that provider. From `app/api/models-config/discover/route.ts`:

```
google-vip:  prefix = "antigravity/"   accept id starts "antigravity/gemini-"
                                       exclude "image", "agent", type image/embedding
kimi-vip:    prefix = "kimi-coding/"   accept id starts "kimi-coding/"
```

**Hard rule:** NEVER manufacture `antigravity/*` or `kimi-coding/*` IDs from a broad
`auto/*` gateway catalog or a general vendor list. Only accept prefixed IDs that came
from that provider's own catalog; otherwise the ID may route to the wrong vendor or
404 at runtime.

Newly-announced models appear only after they show up in the gateway's synced catalog
(OmniRoute `syncedAvailableModels` → `/v1/models`). Test a real completion
(`model_not_found`) rather than trusting marketing (e.g. `antigravity/gemini-3.7-flash`
is still 404 on Google's Antigravity developer endpoint even though the consumer API
has 3.7).

### 4. Build the smart sort (three-tier, usage-driven)

```
weight(modelId, provider) = baseWeight(flag-vendor weight table, take max)
                            + min(100, usageCount * 10)

sort desc by weight; tie-break with Intl.Collator(undefined,
    { numeric: true, sensitivity: "base" }) on name → provider → id.
```

`usageCount` = persisted per-`${provider}:${modelId}` count (e.g. `localStorage`
`pi-model-usage-counts`), incremented on every send, so the models you actually run
float to the top.

### 5. Group by provider + show badges

After sorting, group preserving insertion order, and attach a short provider label via
**one central map**:

```
google-vip       → "Google(订阅)"
google           → "Google(API)"
kimi-vip         → "Kimi(订阅)"
kimi-coding      → "Kimi(Coding)"
deepseek         → "DeepSeek"
openrouter       → "OpenRouter"
qwen-token-plan-cn → "Qwen(包月)"
qwen-dashscope-cn  → "Qwen(按量)"
openai-codex     → "ChatGPT"
```

Never scatter these labels across components — keep one `getProviderShortBadge()` /
`getProviderDisplayName()`.

### 6. Handle per-vendor compat in a request-adapter layer

Party `compat` differences in one adapter, not at every call site:

```
supportsDeveloperRole                    → use "developer" role else "system"
supportsReasoningEffort                  → send reasoning_effort or not
requiresReasoningContentOnAssistantMessages → Kimi: echo reasoning back
supportsThinkingAsText / thinkingFormat  → how thinking appears (deepseek/openai/qwen…)
supportsUsageInStreaming                 → parse usage from stream
maxTokensField                           → max_completion_tokens vs max_tokens
```

This is why `google-vip` (Antigravity) and `kimi-vip` (Kimi) can both run on
`openai-completions` while behaving differently.

### 7. Quota / usage visualization — differentiate by channel kind

- **Real balance** where a real endpoint exists: OpenAI Codex, Kimi, DeepSeek,
  OpenRouter.
- **Gateway subscription providers** (`google-vip`, `kimi-vip`, `omniroute`) with no
  read-only quota endpoint: show honest `unavailable` + a link. **Never fake a gateway
  token balance as a fixed subscription quota** — they are different things.

Tag every quota payload with an explicit **reliability** grade
(`official` / `provider_reported_private` / `gateway` / `none`) and carry it into the UI
so a tooltip can warn when an endpoint is provider-reported but not a stable public API.

Render **one quota badge per provider group header** (not per model row):

```
[● 93%        ]   ← pill: small colored dot + short text
```

- text short-hand: `93%`, `13.2M`, `余量不可查`, `额度…` (loading = gray),
  `凭证失效` (auth error = red).
- colored green / amber / red by thresholds (the `modelUsageText` / `modelUsageColor` /
  `modelUsageTooltip` helpers in Pi Web's ChatInput).
- title-tooltip shows `source · plan`, per-metric remaining / used / percent, a message,
  and reliability.
- never show a number when a provider is `unavailable` — show `余量不可查` + link; and
  don't show the badge at all while the whole provider is still loading.

### 8. Collapse long model groups

When the picker is **not searching**, if a provider has more than **4** models, show
only the first 4 plus a header hint `前 4/N`, and render a full-width toggle:

```
[Google(订阅)      ● 93%            前 4/9]
  Gemini 3.5 Flash (High) (✓ 当前选择)   [Google(订阅)]
  Gemini 3.5 Flash (Low)                [Google(订阅)]
  Gemini 3.1 Flash Lite                 [Google(订阅)]
  Gemini 2.5 Pro                        [Google(订阅)]
[▼ 展开更多 (还有 5 个模型)]
```

Tapping expands to `▲ 折叠收起`; the per-provider expansion state resets to collapsed
when the dropdown reopens. When a search query is active, bypass collapsing — show all
matches (the filtered set already shrinks).

### 8.5 Vendor secondary-fold (extra-long providers)

When one provider carries **>= 24 models** (e.g. `openrouter` 271, `B-ai` 39), the simple
`前 4/N` fold is not enough — even expanded it dumps hundreds of rows. Add a **progressive
three-level** fold instead of dumping the vendor view immediately:

1. **Collapsed (default)**: the top **4 most-used models** directly — identical to the
   small-provider fold, nothing vendor-related visible. (`前 4/N` header, `▼ 展开更多
   (还有 N 个模型)` button.)
2. **Tap 展开更多** → switches to the vendor-grouped view: provider header becomes
   `N 个 · M 厂商`; each vendor renders as a **collapsed header row `▶ vendor N 个`**
   (name + count only, **no models**); only the first 6 vendors show, the rest behind
   `▼ 展开更多厂商 (还有 N 个)`.
3. **Tap a vendor header** → only then that vendor's models expand (`▶` rotates 90°,
   all its models render). Tapping the header again collapses it.

A `▲ 折叠收起 (回到常用 4 个)` button at the bottom of the vendor view collapses back to
level 1.

- Vendor derivation: first path segment of the model id
  (`ai21/jamba-*` → `ai21`, `antigravity/gemini-*` → `antigravity`, `kimi-coding/k3` →
  `kimi-coding`). For unprefixed ids fall back to the display-name family prefix
  (`claude-opus-5` → `claude`, `gpt-5.6-sol` → `gpt`, `gemini-3.1-pro` → `gemini`) so a
  mixed-vendor provider like `B-ai` (39 models across claude/gpt/gemini/kimi/glm/deepseek)
  splits into clean families.
- **Group with a Map keyed by vendor** — never merge only *consecutive* same-vendor rows:
  the usage-driven smart sort interleaves same-vendor models, so consecutive-only merging
  creates duplicate vendor groups (observed: `deepseek` appearing twice).
- Providers under the threshold keep the plain `前 4/N` fold — its expand shows ALL models
  flat with **no** vendor grouping; a search query bypasses both folds.
- State split: `expandedProviders[provider]` gates level 2 vs 1,
  `expandedVendors['provider/vendor']` gates level 3.

### 8.6 Design-evolution record (how this fold was iterated)

> Distilled from Pi Web's real iteration. Do not jump straight to the 3-level design —
> ship the simple version first, then converge per user feedback.

**v1 (initial): vendor groups shown immediately.** Extra-long providers (>= 24 models)
rendered the vendor-grouped view on open: each vendor header had a 3-model preview +
per-vendor "展开 N 个" button, header showed `N 个 · M 厂商`.

**Feedback 1**: don't show vendor groups on open. *"For OpenRouter, showing 4 models by
default is enough — the 4 most-used ones. Clicking 展开更多 shows the vendor-grouped
list. Clicking a vendor's list shows its common models."*

→ **v2 (current): progressive three levels.**

1. **Collapsed = top 4 most-used models** (identical `前 4/N` to small providers, no
   vendor traces);
2. **Tap 展开更多** → vendor-grouped view: header `N 个 · M 厂商`, each vendor a
   **collapsed header row `▶ vendor N 个`** (name + count only, models hidden), only the
   first 6 vendors + `▼ 展开更多厂商`;
3. **Tap a vendor header** → only then its models expand (▶ rotates 90°); tap again to
   collapse.

Bottom `▲ 折叠收起 (回到常用 4 个)` returns to level 1.

**UX principles distilled from this iteration:**

- **Information density follows usage frequency**: users switch among a few frequent
  models daily — the default view is always the *top-4 most-used*, never a structural
  view. Grouping/vendor/full list are only *drill-down paths*.
- **Each expand reveals exactly one layer**: fold → top 4; more → vendor list; tap a
  vendor → its models. Never dump everything at once (271 rows flat = failure).
- **The vendor header itself is the toggle**: no "header + per-vendor expand button"
  two-control pattern; one clickable header row (▶/▼ affordance) is enough.
- **Every layer must be escapable**: the vendor view needs a bottom
  "折叠收起 (回到常用 4 个)" or the user is trapped deep in the tree.
- **Delete dead code on iteration**: v1's 3-model preview, per-vendor "展开 N 个"
  buttons and the `MODEL_VENDOR_SHOW_LIMIT` constant were all removed in v2 (the vendor
  header is the toggle). Clean up unused constants/controls as you iterate.

**Verification (Playwright assertions):**

- Collapsed: `前 4/39` present, `▶vendor N 个` absent.
- After expand: `39 个 · 8 厂商` present; vendor list is
  `▶deepseek2 个 / ▶kimi3 个 / ▶gemini5 个 / ▶claude10 个 / ▶glm3 个 / ▶gpt12 个`;
  model-row count = 0.
- After tapping `▶gemini`: gemini model rows = 5.
- After tapping "折叠收起": back to `前 4/39`, vendor view gone.

### 9. CLI / terminal variant

Pin the current model first, then `provider localeCompare`, then `model id`. Same
models.json, different render context.

### 10. Visibility filter + default-model memory

Persist two user-level bits outside the catalog: a **visible-models whitelist**
(`visibleModels: ["provider/model", ...]`, empty = show all) so users can hide models they do
not want, and the **last selected provider+model** as the default. Hard rule: the picker may
only surface models that `ModelRuntime.getAvailable()` can actually resolve — never inject a
UI-only model the runtime cannot `getModel()`, or selection will fail at send time.

### 11. UI contract notes (already in Pi Web — replicate, don't rebuild)

Two UIs already ship in Pi Web; copy the contracts rather than re-inventing:
- **Thinking-level selector**: level list `auto/off/minimal/low/medium/high/xhigh/max`; availability
  comes from `getSupportedThinkingLevels(model)` (non-reasoning → `["off"]`; `xhigh/max` only when
  `thinkingLevelMap` maps them). The dropdown shows the mapped vendor string when
  `thinkingLevelMap[lvl]` differs, and request-building maps `level → thinkingLevelMap[level]`
  (or the raw level when `auto`/no map).
- **Cost & usage display**: `cost.input/output/cacheRead/cacheWrite` per-1M-token (+ `tiers[]`)
  feeds `calculateCost()` for the session `$` cost; per-message `formatUsage` prints
  `"N in · M out · K cache · $X.XXXX"`; `formatUsageValue` handles `USD/CNY/requests/credits`.

Both are described in detail in `references/implementation-guide.md` §9.

## Pitfalls

- Do not put gweb / browser-automation channels in the main catalog: no tool calling,
  long contexts collapse and repeat, and Google developer-side models may 404.
- Never fabricate prefixed IDs from a broad `auto/*` catalog; only accept IDs from the
  provider's own catalog.
- Do not make one provider both subscription and API — it pollutes sort weights and
  quota display.
- Do not hardcode the flag-vendor weight table immutably; make it configurable since
  each agent's flagship models differ.
- `input: ["text","image"]` satisfies both text and image; use `["text"]` for
  text-only.
- When a model is missing from the catalog, test a real completion before assuming; a
  `model_not_found` / 404 is authoritative (catalog may be a stale cache).
- Do not render a quota badge on every model row — show one badge per provider group
  header; per-row badges clutter a large catalog.
- Never fabricate a number when a provider is `unavailable` — show `余量不可查` + a
  link; and skip the badge entirely while the whole provider is still loading.
- Keep the collapse limit and the quota badge as **UI concerns**, decoupled from the
  sort weights and the quota data-layer, so either can change independently.
- Never let the UI inject a model the runtime cannot resolve (`ModelRuntime.getAvailable()` / `getModel()` is the single source of truth); otherwise selecting it fails at send.

## Verification

1. `models.json` passes the schema (non-empty `id`, valid `compat` fields).
2. A real chat completion returns 200 for a registered prefixed ID
   (e.g. `antigravity/gemini-3.5-flash-high`) and `model_not_found` for an unregistered one
   — proves prefix routing.
3. Picker renders subscription providers as `Google(订阅)`/`Kimi(订阅)` and API
   providers as `Google(API)`/others, grouped by provider.
4. Frequent models + high-weight flagships surface above low-weight ones; ties fall
   back to natural collation.
5. Sends increment `pi-model-usage-counts`; the used provider/model climbs the list.
