---
name: shopify-theme-delivery
description: Use when planning, building, migrating, validating, previewing, diagnosing, or releasing a Shopify Online Store 2.0 theme, including Liquid, JSON templates, sections, snippets, theme CSS or JavaScript, Theme Editor preservation, draft-theme writes, stale previews, dynamic DOM enhancements, or multi-page acceptance.
---

# Shopify Theme Delivery

## Overview

Treat a Shopify theme change as a versioned release package, not a sequence of
Theme Editor clicks. Freeze the desired state, edit the correct source layer,
write one bounded batch to one draft theme, prove remote identity and runtime
behavior, then leave publication to the Owner unless separately authorized.

Project runbooks, target registries, protected-action gates, and brand systems
override this portable skill when stricter.

## Required Entry Contract

For source-only work, remote-only fields may be `not-applicable`. Before any
remote read or write, every target and approval field must be known:

```text
SHOPIFY_THEME_DELIVERY
store: <store domain or registry key>
base_theme: <name and id>
target_draft: <name and id>
current_live: <name and id>
edit_scope: <routes / surfaces / files>
change_class: <static-visual / structural-theme / dynamic-runtime>
preserve: <merchant content, settings, app blocks, locales, integrations>
excluded: <checkout, data, publish, apps, other routes>
write_approval: <not-needed / pending / approved exact scope>
publish_approval: <not-requested / pending / approved exact scope>
acceptance: <routes, viewports, interactions, settling checks>
```

Never guess a store, theme ID, live state, resource assignment, preview URL, or
approval state. Prefer project registries and guarded scripts over remembered
IDs or raw commands. A local CSS/Liquid/test change may proceed without remote
identity; it must stop before remote inspection or mutation.

Requests whose primary object is product, inventory, collection, metafield,
customer, or order data belong to Shopify Admin/data operations. App and
extension deployment belongs to app delivery. Checkout logic belongs to its
own supported extension/function surface. Split mixed requests into separate
theme and non-theme scopes with independent approvals and acceptance.

## Classify the Change Before Coding

| Class | Typical work | Minimum proof |
| --- | --- | --- |
| Static visual | tokens, spacing, typography, responsive CSS | computed styles, desktop/mobile, overflow and focus |
| Structural theme | Liquid, schema, section composition, JSON templates | JSON/schema validation, section wiring, Theme Editor preservation |
| Dynamic runtime | search, filters, predictive results, sticky actions, DOM observers | idempotency, isolated settling test, one real mutation, live preview interaction |

Use the highest applicable class. A styling task that adds a MutationObserver
is a dynamic-runtime task.

## Freeze the Complete Desired State

Before editing, produce one owner-reviewable package scaled to the affected
surface. A narrow fix may list unrelated surfaces as `excluded`; a full-theme
replacement requires the complete store-wide matrix:

1. Brand system: tone, palette, typography, spacing, radii, surfaces, imagery,
   motion, accessibility, and responsive rules.
2. Surface matrix: global shell, homepage, collection, product, cart, search,
   content pages, account, localization/markets, and eligible checkout surface.
3. Ownership matrix:
   - source owns structure, shared components, tokens, CSS, and JavaScript;
   - Theme Editor owns exposed copy, images, menus, section settings, and order;
   - Shopify data owns products, collections, metafields, inventory, customers,
     and orders;
   - Owner alone publishes or rolls back unless separately authorized.
4. Preservation contract: existing section IDs, merchant content, settings,
   app blocks, localization, data bindings, and integrations to retain.
5. Definition of done: local validation, remote readback, preview routes,
   desktop/mobile checks, evidence, and explicit unpublished state.

Do not claim a complete theme when only the homepage or global CSS is covered.
Read `references/shopify-theme-delivery-standard.md` for the full checklist.

## Choose the Correct Edit Layer

| Change | Edit layer |
| --- | --- |
| Page composition, section order, defaults | `templates/*.json` |
| Rendered module and merchant-editable schema | `sections/*.liquid` |
| Shared markup or Liquid logic | `snippets/*` |
| Styling, behavior, static media | `assets/*` |
| Global shell or asset loading | `layout/theme.liquid` only when truly global |
| Theme-wide configurable settings | `config/settings_schema.json` |
| Current merchant values | Avoid `config/settings_data.json`; require explicit approval |

JSON templates are composition data. Never place Liquid, HTML, CSS, or
JavaScript in them. Preserve existing section IDs and settings unless migration
is explicit. Modern checkout is not a normal theme surface.

## Use One Bounded Approval Envelope

A draft-theme write is still a Shopify mutation. Request one compact approval
for the coherent batch, not one approval per file:

```text
Approve writing <manifest or N named files> to draft theme <id> on <store>,
followed by exact readback and preview-only browser acceptance; no publish,
live-theme change, data mutation, app deploy, or checkout mutation.
```

After approval, execute the unchanged envelope. Ask again only if the store,
target theme, manifest, protected surface, or publish boundary changes.

## Delivery Workflow

1. **Inventory** — Read theme identity, route/template assignments, active
   sections, shared assets, apps, locales, and baseline evidence.
2. **Design once** — Approve the desired state and surface matrix before code.
3. **Implement in source** — Use sections/snippets/assets; change templates
   only for composition. Keep merchant content configurable.
4. **Validate locally** — Run Theme Check and the bundled validator:

   ```bash
   node scripts/validate-theme-package.mjs \
     --theme /path/to/theme \
     --changed-files /path/to/changed-files.txt
   ```

   Resolve the script relative to this skill. Pass `--allow-settings-data`
   only after explicit approval. Run focused tests while iterating; run broad
   suites once on the frozen candidate revision.
5. **Prove dynamic stability when applicable** — Follow
   `references/dynamic-ui-stability.md`. The enhancer must settle after initial
   render and after one genuine external mutation.
6. **Write one draft batch** — Prefer project scripts or supported CLI/API.
   Specify the exact draft theme ID; never publish as a side effect.
7. **Read back remotely** — Compare the exact changed-file manifest, file
   count, content hashes/checksums, and release marker against the target draft.
8. **Accept in browser** — Use the preview URL for the same theme ID. Check the
   route matrix at desktop and mobile widths, interactions, console errors,
   horizontal overflow, focus, reduced motion, and responsive layout.
9. **Hand off** — Record source revision, draft/live/rollback IDs, changed
   files, readback, preview evidence, exclusions, and `not published` state.
10. **Publish separately** — Publish only after explicit Owner approval, then
    verify live identity, public routes, and the rollback candidate.

Use `references/acceptance-and-handoff.md` for the final acceptance matrix and
handoff block.

## Dynamic UI Stability Gate

For DOM-enhancing theme JavaScript:

- make every enhancement idempotent;
- observe the smallest stable container, not the whole document by default;
- avoid replacing children when the desired DOM already exists;
- filter, pause, or disconnect the observer around owned writes;
- coalesce mutation bursts into one scheduled enhancement;
- clean up observers, listeners, and scheduled work;
- prove repeated execution does not duplicate components or state;
- prove initial render settles: the scheduled-work count is unchanged between
  the 300 ms and 600 ms checkpoints;
- append one genuine external result mutation, prove exactly one additional
  enhancement, then prove the next 300 ms to 600 ms window is unchanged.

Use a minimal synthetic page first so unrelated theme animation frames do not
hide a feedback loop. Then verify the same behavior on the real draft preview.

## Release Markers and Stale Previews

Put a narrow marker in the target section or asset. Do not use
`layout/theme.liquid` as a routine marker for one route.

Diagnose a mismatch in this order:

1. store and target theme identity;
2. route/resource handle, ID, visibility, and `template_suffix`;
3. JSON template wiring and section type;
4. remote changed-file readback and checksum;
5. target marker in preview HTML;
6. loaded CSS/JavaScript URLs and runtime/cascade state;
7. private-session/mobile comparison;
8. bounded Shopify processing delay;
9. browser, CDN, or proxy cache.

Do not repush the whole theme or publish repeatedly to chase cache. Classify
the mismatch from evidence.

## Experience-to-Skill Learning Loop

A conversation summary is not learned behavior. Promote a lesson only when:

1. a minimal reproducer captures the failure;
2. an executable regression fails before the fix and passes after it;
3. the relevant skill instruction or reference is updated;
4. the skill package and target implementation both validate;
5. project-neutral rules are extracted without store IDs, credentials,
   internal approval mechanics, private paths, or company-only policy.

This process is deliberate and reviewable; the skill must not silently mutate
itself from chat history.

## Completion Gate

Do not report completion unless all applicable gates pass:

- exact draft and live identities recorded;
- changed files match approved scope;
- JSON/schema/Theme Check validation passes;
- dynamic-runtime settling regression passes when applicable;
- remote readback matches the local manifest;
- every promised surface has preview evidence;
- desktop and mobile acceptance passes;
- no unintended `settings_data.json`, Shopify data, app, checkout, or live-theme
  mutation occurred;
- publish state, rollback target, and next action are explicit.

## Red Flags

Stop when any of these appears:

- “Use whichever theme is open.”
- “Push the entire folder and see what changes.”
- “Use browser clicks to upload many source files.”
- “Change `settings_data.json` to make it match.”
- “The draft looks good, so call it published.”
- “The homepage is done, so the whole theme is done.”
- “The MutationObserver works, so performance is fine.”
- “Public HTML differs, therefore the source is wrong.”
