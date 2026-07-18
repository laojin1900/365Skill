# Shopify Theme Delivery Standard

## Normative language

- **MUST** is required for reliable delivery.
- **SHOULD** is the default unless the project documents a reason otherwise.
- **MAY** is optional.
- Project governance, platform limits, and explicit Owner instructions override
  this standard when stricter.

## Scope and target identity

Before edits, record:

- store domain or registry key;
- environment and credential source name, never secret values;
- base/source theme name and ID;
- exact target draft theme name and ID;
- current live theme name and ID;
- rollback candidate;
- source repository and revision;
- allowed files and surfaces;
- prohibited writes;
- write and publish approval states.

Do not use “the open theme,” “the latest theme,” or a remembered ID as a target.
Read theme identity immediately before a write and again during readback.

## Desired-state package

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

If `settings_data.json` must change, record exact keys, take a backup/readback,
exclude unrelated values, validate JSON, and obtain explicit approval.

## Draft write and remote readback

One approval SHOULD cover one coherent batch and state the store, exact draft
theme, manifest, write mechanism, readback/preview verification, and excluded
live publish, data, app, and checkout mutations.

Prefer project guard scripts. Otherwise use supported Shopify CLI/API with the
explicit theme ID. Use browser automation for inspection and acceptance, not as
the primary carrier for a multi-file source package. Never publish as a side
effect of a draft write.

After writing, prove:

- remote theme ID equals the approved draft;
- remote changed-file set equals the manifest;
- every remote file exists;
- local and remote checksums match;
- the release marker is in the intended section/asset;
- the live theme identity did not change.

File-count success without content comparison is insufficient.

## Browser acceptance

Use the exact preview URL for the target draft. At minimum check desktop and
mobile; add tablet for layout-sensitive work. For each promised route verify:

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

## Cache diagnosis

Check in order:

1. store and live/draft identity;
2. preview URL theme parameter;
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

## Publication and rollback

Draft acceptance is not publication. Publish only after separate explicit
approval identifying the target theme and accepted source revision. After
publication, verify live identity, representative public routes, interactions,
and the public release marker; record the prior live theme as rollback target.

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
