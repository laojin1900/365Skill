---
name: shopify-theme-delivery
description: Use when planning, building, migrating, validating, previewing, diagnosing, or releasing a Shopify Online Store 2.0 theme, including Liquid, JSON templates, sections, snippets, theme CSS or JavaScript, Theme Editor preservation, draft-theme writes, stale previews, dynamic DOM enhancements, or multi-page acceptance.
---

# Shopify Theme Delivery

## Overview

Treat a Shopify theme change as a versioned source package. Match the requested
delivery boundary: local source, remote preview, release preparation, or live
release. Local source work closes with relevant local verification; remote
identity, write authorization, and release evidence apply when that boundary
requires them.

Use the current project's maintained theme route when one exists. Project
classifiers, runbooks, guarded operators, target registries, and brand systems
take precedence over this portable fallback, including a narrower valid route.
Do not layer a second draft-release workflow over the selected project route.
Preserve current user scope and authority; missing project evidence blocks the
affected remote action, not unrelated source work.

## Required Entry Contract

For source-only work, remote-only fields may be `not-applicable`. Before a
remote read, resolve the exact target and read scope; read access does not
require write or publish authorization. Before a remote write, establish the
applicable target, source, preservation, authorization, and acceptance fields:

```text
SHOPIFY_THEME_DELIVERY
store: <store domain or registry key>
base_theme: <name and id>
target_theme: <name, id and role>
target_draft: <name and id, or not-applicable for a live-file patch>
current_live: <name and id>
edit_scope: <routes / surfaces / files>
change_class: <static-visual / structural-theme / dynamic-runtime>
delivery_mode: <local-source / live-file-patch / stable-draft / role-transition>
preserve: <merchant content, settings, app blocks, locales, integrations>
excluded: <checkout, data, publish, apps, other routes>
write_approval: <not-needed / pending / approved exact scope>
publish_approval: <not-requested / pending / approved exact scope>
acceptance: <routes, viewports, interactions, settling checks>
```

Never guess a store, theme ID, live state, resource assignment, preview URL, or
approval state. Prefer project registries and guarded scripts over remembered
IDs or raw commands. A local CSS/Liquid/test change may proceed without remote
identity; resolve identity before remote inspection and the additional write
requirements before mutation.

Requests whose primary object is product, inventory, collection, metafield,
customer, or order data belong to Shopify Admin/data operations. App and
extension deployment belongs to app delivery. Checkout logic belongs to its
own supported extension/function surface. Split mixed requests into separate
theme and non-theme scopes with separately resolved authority and acceptance.

## Classify the Change Before Coding

| Class | Typical work | Minimum proof |
| --- | --- | --- |
| Static visual | copy, tokens, spacing, typography, responsive CSS | affected styles/content; viewport, overflow and focus checks when impacted |
| Structural theme | Liquid, schema, section composition, JSON templates | JSON/schema validation, section wiring, Theme Editor preservation |
| Dynamic runtime | search, filters, predictive results, sticky actions, DOM observers | idempotency, isolated settling test, one real mutation, affected interaction |

Use the highest applicable class. A styling task that adds a MutationObserver
is a dynamic-runtime task.

Verification depth and remote write mode are separate decisions. Use the
project's supported mode: exact files on the current live theme, its stable
draft slot, or an authorized theme-role transition. Dynamic runtime risk does
not by itself require a new draft or role transition. Broader verification
does not expand the allowed file manifest or remote effect.

Follow the selected operator's exact target, reviewed source revision, preimage,
rollback, and readback requirements. Do not impose a universal main-branch
equality rule or invalidate unchanged evidence for unrelated mainline commits.
If the project route is unavailable or unsupported, repair its evidence or
source path; do not switch to a broader write mode or an unguarded writer.
Without a project route, resolve a supported exact write mechanism before any
mutation. These mode descriptions do not grant authority.

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
   - publication and rollback follow the exact authorized effect and selected
     operator's contract.
4. Preservation contract: existing section IDs, merchant content, settings,
   app blocks, localization, data bindings, and integrations to retain.
5. Definition of done: local validation and, for remote delivery, exact readback,
   relevant route/viewport checks, evidence, and the requested draft/live state.

Do not claim a complete theme when only the homepage or global CSS is covered.
For a broad redesign or remote operation, read the matching sections of
`references/shopify-theme-delivery-standard.md`. A bounded change needs only
its affected surface, preservation intent, checks, and requested delivery state.

## Choose the Correct Edit Layer

| Change | Edit layer |
| --- | --- |
| Page composition, section order, defaults | `templates/*.json` |
| Rendered module and merchant-editable schema | `sections/*.liquid` |
| Shared markup or Liquid logic | `snippets/*` |
| Styling, behavior, static media | `assets/*` |
| Global shell or asset loading | `layout/theme.liquid` only when truly global |
| Theme-wide configurable settings | `config/settings_schema.json` |
| Current merchant values | Avoid `config/settings_data.json`; require authority for exact keys |

JSON templates are composition data. Never place Liquid, HTML, CSS, or
JavaScript in them. Preserve existing section IDs and settings unless migration
is explicit. Modern checkout is not a normal theme surface.

## Use One Bounded Authorization Envelope

A draft-theme write is still a Shopify mutation. A current explicit user request
that names the operation, target, and intended effect authorizes that scope;
do not ask for equivalent confirmation again. Read-only inspection does not
authorize a write. If write authority is missing, prepare the exact reviewable
manifest and target first, then request one compact authorization for the batch:

```text
Approve writing <manifest or N named files> to draft theme <id> on <store>,
followed by exact readback and preview-only browser acceptance; no publish,
live-theme change, data mutation, app deploy, or checkout mutation.
```

For a supported live-file patch, bind the exact live theme, named files, reviewed
revision, preimages, and receipt-based rollback; it has no draft or promotion
step. Ask again only when the target, scope, material effect, credential boundary,
or rollback method changes materially. A correction within the authorized
effect does not require another equivalent confirmation.

## Delivery Workflow

1. **Inventory** — Locate affected source, callers, and preservation constraints.
   Resolve remote identity and assignments when remote work is requested.
2. **Design** — Reuse existing requirements and design decisions. Establish a
   full surface matrix for a broad redesign; ask only about unresolved choices
   that materially change the outcome.
3. **Implement in source** — Use sections/snippets/assets; change templates
   only for composition. Keep merchant content configurable.
4. **Validate locally** — Use focused checks appropriate to the changed files.
   Run Theme Check for relevant Liquid/schema changes and the bundled validator
   when validating a theme package:

   ```bash
   node scripts/validate-theme-package.mjs \
     --theme /path/to/theme \
     --changed-files /path/to/changed-files.txt
   ```

   Resolve the script relative to this skill. Pass `--allow-settings-data`
   only when the user authorized those settings. Isolated copy/styling does not
   require full browser acceptance; material interaction, navigation, checkout,
   or responsive behavior does. Scale checks to affected behavior; repeat or
   broaden passing checks only for new changes, failures, or a concrete concern.
5. **Prove dynamic stability when applicable** — Follow
   `references/dynamic-ui-stability.md`. The enhancer must settle after initial
   render and after one genuine external mutation. Verify locally for local
   delivery; remote acceptance follows only when remote delivery is requested.
   Local source work ends after the applicable local checks.
6. **Execute the selected remote effect** — Only for authorized remote work,
   use the selected exact-file, stable-draft, or role-transition writer. Reuse
   the project draft slot when selected; never create a candidate solely
   because verification is broad. Never publish as a side effect of a draft write.
7. **Read back remotely** — Compare the exact changed-file manifest, file
   count, content hashes/checksums, and release marker against the selected target.
8. **Accept in browser** — Use the exact draft preview or public URL for the
   selected live theme. Check affected routes, viewports, interactions, console
   errors, overflow, focus, reduced motion, and dynamic settling as applicable.
   Broad redesigns cover all promised surfaces on desktop/mobile. Use target
   readiness rather than whole-page network idleness for bounded checks.
9. **Hand off** — Report the change, strongest relevant checks, actual delivery
   state, and remaining work. For remote work include exact identity, readback,
   rollback evidence, and applicable browser acceptance.
10. **Publish when selected and authorized** — An existing explicit publish
    request covering this target and effect suffices. Verify live identity,
    public routes, and the selected rollback evidence after publication.
    A live-file patch has no promotion step.

Use `references/acceptance-and-handoff.md` for remote acceptance or a structured
handoff when useful. Omit fields outside the requested delivery boundary.

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
hide a feedback loop. Then verify affected behavior in the local app or theme
fixture; for requested remote delivery, also verify the exact draft or live target.

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
the mismatch from evidence. When readback matches and public delivery still
shows exact prior bytes during bounded propagation, use read-only observation.
Propagation delay alone does not authorize another write, publication, new
candidate, or automatic rollback. Reconcile uncertain writes from receipts and
target readback before any serial continuation; never blind-retry.

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

Local source work closes after relevant local validation, including dynamic
settling when applicable. Remote identities, publication, and remote browser
evidence are not local completion gates. For remote delivery, apply only the
gates required by the selected effect:

- exact target and live identities recorded;
- changed files match approved scope;
- JSON/schema/Theme Check validation passes;
- dynamic-runtime settling regression passes when applicable;
- remote readback matches the local manifest;
- every promised surface has the required local, preview, or public evidence;
- affected viewport and interaction acceptance passes;
- no unintended `settings_data.json`, Shopify data, app, checkout, file, or
  theme-role mutation occurred;
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
