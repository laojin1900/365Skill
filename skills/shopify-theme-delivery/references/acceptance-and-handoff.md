# Acceptance and Handoff

## Changed-file manifest

Use theme-relative paths, one per line:

```text
assets/brand-system.css
assets/theme-interactions.js
sections/header.liquid
sections/footer.liquid
templates/index.json
```

Generate the manifest from the source diff. Do not include downloaded remote
files or transient evidence. Pass it to the bundled validator with
`--changed-files`.

## Acceptance matrix

Create one row per promised surface, not one row per screenshot.

| Surface | Route/resource | Template suffix | Target section/asset | Desktop | Mobile | Interaction | Marker | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Global shell | representative routes | n/a | header/footer assets | pass | pass | menus/search/cart | present | pass |
| Homepage | `/` | default | homepage sections | pass | pass | links/carousels | present | pass |
| Collection | `/collections/<handle>` | recorded | collection grid | pass | pass | filter/sort/page | present | pass |
| Product | `/products/<handle>` | recorded | main product | pass | pass | variants/quantity/cart | present | pass |
| Cart | `/cart` and drawer | default | cart section/assets | pass | pass | update/remove/checkout link | present | pass |

Use representative real resources and record excluded surfaces explicitly.
When the project provides no viewports, use desktop 1440 × 1000 and mobile
390 × 844, adding tablet 768 × 1024 for layout-sensitive work.

Record computed styles for CSS precedence, contrast, typography, visibility, or
responsive issues. Record console errors and horizontal overflow for every
viewport. Dynamic-runtime work must also record the isolated settling result.

## Browser evidence

Evidence must answer:

- Which draft theme rendered?
- Which route/resource and template rendered?
- Did the target section/asset revision render?
- Were content/settings preserved?
- Did required interactions work?
- Did desktop and mobile pass?
- Did dynamic enhancements settle without duplicate DOM or scheduled work?
- Were console errors or overflow present?

Store only final useful screenshots/traces. Near-identical screenshots are
debug output, not release evidence.

## Handoff block

```text
SHOPIFY_THEME_DELIVERY_BLOCK
task_id:
store:
source_repository:
source_revision:
change_class:
base_theme_name:
base_theme_id:
target_draft_name:
target_draft_id:
live_theme_id_before:
rollback_theme_id:
approved_write_scope:
changed_files:
settings_data_changed: no | approved exact keys
local_validation:
dynamic_stability: not-applicable | initial-settled / one-external-mutation-settled
remote_readback: <matched>/<expected> plus checksum result
preview_url_identity:
acceptance_matrix:
desktop_result:
mobile_result:
console_errors:
horizontal_overflow:
excluded_surfaces:
shopify_data_mutation: none | approved exact mutation
app_or_extension_deploy: none | approved exact deploy
checkout_mutation: none | approved exact mutation
publish_state: not-published | published with approval
publish_approval:
live_theme_id_after:
next_action:
```

For draft-only delivery, `publish_state` remains `not-published` and
`live_theme_id_after` is `unchanged/not-applicable`.
