# Shopify Theme Delivery Standard

## Normative language

- **MUST** is required for reliable delivery.
- **SHOULD** is the default unless the project documents a reason otherwise.
- **MAY** is optional.
- Current user scope, platform limits, and maintained project classifiers,
  guarded operators, and runbooks take precedence over this portable fallback,
  including a narrower valid project route. Apply only the sections needed for
  the requested local, preview, preparation, or live delivery boundary.

## Scope and target identity

For local source work, record affected source and scope. For remote reads,
resolve exact identity and read scope without requiring write authorization.
Before remote mutation, establish applicable fields from current evidence:

- store domain or registry key;
- environment and credential source name, never secret values;
- base/source theme name and ID;
- exact target theme name, ID, role, and selected write mode;
- current live theme name and ID;
- rollback receipt/preimages or candidate, as selected by the operator;
- source repository and revision;
- allowed files and surfaces;
- prohibited writes;
- write and publish approval states.

Do not use “the open theme,” “the latest theme,” or a remembered ID as a target.
Read theme identity immediately before a write and again during readback.
Missing remote fields do not block local implementation or local verification.

## Desired-state package

Use existing user requirements and design decisions. A broad redesign needs the
promised surface matrix; a bounded change uses only affected parts of the
following checklist. Ask only about unresolved material choices.

### Brand foundation

- positioning and tone;
- primary, secondary, surface, text, border, success, warning, and error colors;
- heading and body fonts, weights, fixed type scale, and fallbacks;
- spacing scale, content width, grid, borders, radii, and shadows;
- icon and imagery direction;
- motion and reduced-motion behavior;
- focus, contrast, keyboard, zoom, and touch-target requirements.

### Component system

- announcement/top bar;
- header, navigation, search, account, cart badge, and mobile drawer;
- footer, newsletter, legal, social, localization, and contact blocks;
- buttons, inputs, badges, cards, price, product card, media, pagination,
  breadcrumbs, notices, and empty states;
- loading, error, disabled, selected, hover, focus, and out-of-stock states.

### Content hierarchy

Define required, optional, and excluded modules before implementation. Decide
promotions, editorial content, social proof, trust, buyer paths, and wholesale
paths before browser editing rather than adding them incrementally.

## Surface inventory

“Complete theme” means every promised surface is listed and accepted.

| Surface | Minimum coverage |
| --- | --- |
| Global shell | announcement, header, navigation, predictive search, cart drawer, footer, cookie/app overlays |
| Homepage | hero, categories, products, promotions, trust, business paths, optional editorial/blog |
| Collection | title/banner, filters, sort, grid, cards, pagination, empty state, mobile controls |
| Product | media, variants, price, availability, quantity/MOQ, add-to-cart, shipping, app blocks, sticky action |
| Cart | drawer/page, quantity, remove, notes, discount messaging, subtotal, checkout action, empty state |
| Search | predictive/results/no-results, filters where supported, stable dynamic enhancement |
| Content | standard page, contact, FAQ, blog index, article, policy pages, 404 |
| Customer | supported login/account/order surfaces |
| Markets/locales | language, currency/market, translated strings, long-copy resilience, RTL if required |
| Checkout | supported branding/editor/extension only; not ordinary theme Liquid |

For a narrow task, mark non-target surfaces “excluded,” not “complete.”

## Architecture and content ownership

- `layout/theme.liquid`: global document shell and asset loading.
- `templates/*.json`: section composition, IDs, order, and defaults.
- `sections/*.liquid`: rendered modules, schema, blocks, and presets.
- `snippets/*`: shared Liquid fragments.
- `assets/*`: CSS, JavaScript, images, and fonts.
- `config/settings_schema.json`: theme-wide editable setting definitions.
- `config/settings_data.json`: merchant values; protected by default.
- `locales/*`: translatable strings.

Source controls structure and reusable behavior. Theme Editor controls merchant
content exposed by schema. Products, collections, metafields, inventory,
customers, and orders are not theme files. Apps, extensions, and checkout use
separate deploy and approval boundaries.

## Implementation and preservation rules

MUST:

- map template section types to implementations before edits;
- keep merchant-editable content in schema settings/blocks;
- preserve section IDs where possible so saved content stays bound;
- preserve app blocks, dynamic sources, metafield bindings, localization keys,
  menu handles, selling plans, and integration hooks;
- keep JavaScript progressively enhanced, scoped, idempotent, and disposable;
- validate touched JSON/schema; theme JSON may contain comments and trailing
  commas, so use Theme Check or a JSONC-aware validator;
- verify the real cascade, computed styles, and responsive behavior.

MUST NOT:

- place raw Liquid/HTML/CSS/JavaScript inside JSON templates;
- hardcode merchant content merely to match a screenshot;
- remove blocks/settings without a migration decision;
- modify `settings_data.json` without an explicit reviewed reason;
- widen a single-route fix into unrelated routes;
- use `layout/theme.liquid` as a generic cache marker;
- claim checkout coverage from theme preview alone;
- accept observer-driven DOM code without a settling regression.

If `settings_data.json` must change, bind authority to exact keys, exclude
unrelated values, and validate JSON. For a remote write, also preserve preimages
and verify readback. Do not repeat an existing authorization covering those keys.

## Selected write mode and remote readback

A current user request naming the operation, target, and intended effect supplies
authorization for that scope. If authority is missing, prepare a concrete target
and manifest before asking. One authorization SHOULD cover the coherent batch;
do not ask again per file or for a correction preserving the reviewed effect.
Reconfirm material changes to target, scope, effect, credential boundary, or
rollback method. A read request does not authorize mutation.

Risk sets verification depth; the project's supported mode sets the remote
effect. Exact live files, a stable draft slot, and a theme-role transition are
distinct effects. A dynamic change does not require a new candidate solely
because its checks are broader. Preserve the selected project route; do not
layer a heavier draft workflow over it.

Use the project's guarded writer, binding the reviewed source revision, exact
target, changed-file manifest, preimages, rollback, and readback. Revalidate
changed dependencies; unrelated mainline changes do not invalidate otherwise
current evidence. Never replace an unsupported guarded path with a raw writer.
Without a project route, resolve a supported exact write mechanism and target
before mutation. Use browser automation for inspection and acceptance, not as
the primary carrier for a multi-file source package. Never publish as a side
effect of a draft write; a live-file patch has no draft or promotion step.

After writing, prove:

- remote theme ID and role match the selected authorized target;
- remote changed-file set equals the manifest;
- every remote file exists;
- local and remote checksums match;
- the release marker is in the intended section/asset;
- the live identity is unchanged for a file patch or draft write, or matches
  the authorized role transition after promotion.

File-count success without content comparison is insufficient.

## Browser acceptance

Local source work closes with relevant local checks. Isolated copy/styling
does not require full browser acceptance; material interaction, navigation,
checkout, or responsive behavior does. Keep dynamic settling proof even for a
small change that introduces an observer.

For remote delivery, use the exact draft preview or public URL for the selected
live theme. Match coverage to affected behavior and the project risk route.
Broad redesigns cover all promised routes on desktop/mobile; bounded changes
use the required target viewports and checks. Add tablet when layout impact
warrants it. For the affected routes verify:

- correct resource and template assignment;
- target release marker in preview HTML;
- content/settings preservation;
- hierarchy, contrast, typography, images, and responsive behavior;
- target menus, drawers, variants, filters, quantities, and actions;
- keyboard/focus and reduced motion where applicable;
- no horizontal overflow or relevant console errors;
- loaded assets belong to the target revision;
- dynamic enhancements settle and do not duplicate.

Screenshots alone do not prove interactions, settling, or remote source identity.
Use target readiness rather than whole-page network idleness for bounded checks.

## Cache diagnosis

Check in order:

1. store and live/draft identity;
2. preview URL theme parameter or public live identity, according to the mode;
3. resource handle/ID and visibility;
4. assigned template or `template_suffix`;
5. JSON section wiring;
6. remote checksum and release marker;
7. marker in preview HTML;
8. loaded assets and cascade/runtime state;
9. private-session and mobile comparison;
10. bounded Shopify processing delay;
11. browser cache, outer CDN, or proxy.

Do not call a mismatch “cache-only” until steps 1–8 pass.
When exact remote readback matches but public delivery shows prior bytes during
bounded propagation, continue with read-only observation. Delay alone does not
authorize another write, candidate, publication, or automatic rollback. On an
uncertain write, reconcile the receipt and target state before any continuation.

## Publication and rollback

Draft acceptance does not authorize publication. Publish only when the selected
mode and user authorization cover the exact target and reviewed source; an
existing explicit publish request suffices without another confirmation.
Stable drafts remain unpublished; live-file patches have no promotion step.
After publication, verify live identity, representative public routes,
interactions, and the public release marker. Retain the rollback evidence
required by the selected operator: prior live identity for a role transition,
or exact preimages and receipt for a file patch.

Use the operator's conflict-safe rollback only for a verified failure under its
contract. Preserve concurrent third-party changes; propagation delay alone is
not a rollback trigger.

## Evidence hygiene

Durable evidence includes the desired-state/surface matrix, source revision,
manifest, validation result, remote checksum readback, browser acceptance,
theme identities, approval/publish state, and handoff. Keep raw API responses,
downloaded themes, duplicate screenshots, debug logs, and secret files in
temporary/output paths.

## Official references

- Theme architecture: <https://shopify.dev/docs/storefronts/themes/architecture>
- JSON templates: <https://shopify.dev/docs/storefronts/themes/architecture/templates/json-templates>
- Sections: <https://shopify.dev/docs/storefronts/themes/architecture/sections>
- Section schema: <https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema>
- Shopify CLI: <https://shopify.dev/docs/storefronts/themes/tools/cli>
- Theme Check: <https://shopify.dev/docs/storefronts/themes/tools/theme-check/index>
- Checkout customization: <https://shopify.dev/docs/apps/build/checkout/technologies>
