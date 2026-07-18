# Dynamic UI Stability

Use this reference when theme JavaScript enhances DOM that Shopify, predictive
search, filters, apps, sections, or other scripts may replace after load.

## Failure pattern

The dangerous loop is:

1. an observer sees a child-list change;
2. the enhancer replaces or appends DOM;
3. that owned write triggers the same observer;
4. another animation frame runs even though desired state is already present;
5. the page continues scheduling work indefinitely.

The interface may look correct while wasting CPU, causing delayed input,
draining mobile batteries, or amplifying unrelated rendering work.

## Implementation rules

### Make writes idempotent

Before changing DOM, compare the desired state with current state. Reuse
existing nodes when possible. Do not replace `children`, `innerHTML`, classes,
attributes, or text with an equivalent value.

### Scope observation

Observe the smallest stable container that owns the external changes. Avoid a
global `{ childList: true, subtree: true }` observer unless the page has no more
specific stable root and filtering is proven.

### Separate owned and external mutations

Use one or more of these patterns:

- disconnect before owned writes and reconnect after them;
- filter records whose target is inside an enhancer-owned node;
- tag owned nodes and ignore those records;
- render from a stable state comparison and return without writes when equal.

### Coalesce and clean up

Coalesce mutation bursts into one `requestAnimationFrame` or microtask. Keep at
most one scheduled enhancement. Cancel pending work and disconnect observers
when the owning section is removed or reinitialized.

## Isolated executable proof

Test the module on a minimal synthetic page before a live preview. This removes
noise from carousels, apps, and theme animations.

```js
import { test, expect } from "@playwright/test";

test("enhancement settles and reacts once", async ({ page }) => {
  await page.goto("https://example.com/search?q=red&type=product");
  await page.setContent(`
    <main class="template-search">
      <header class="template-search__header"><h1>Search</h1></header>
      <div data-external-results></div>
    </main>
  `);

  await page.evaluate(() => {
    window.__frames = 0;
    const nativeRaf = window.requestAnimationFrame.bind(window);
    window.requestAnimationFrame = (callback) => {
      window.__frames += 1;
      return nativeRaf(callback);
    };
  });

  await page.addScriptTag({
    path: "/absolute/path/to/theme-enhancer.mjs",
    type: "module",
  });

  await page.waitForTimeout(300);
  const initial300 = await page.evaluate(() => window.__frames);
  await page.waitForTimeout(300);
  const initial600 = await page.evaluate(() => window.__frames);
  expect(initial600).toBe(initial300);

  await page.evaluate(() => {
    const external = document.createElement("div");
    external.hidden = true;
    external.dataset.externalMutation = "true";
    document.querySelector("[data-external-results]").append(external);
  });

  await page.waitForTimeout(300);
  const mutation300 = await page.evaluate(() => window.__frames);
  expect(mutation300).toBe(initial600 + 1);
  await page.waitForTimeout(300);
  const mutation600 = await page.evaluate(() => window.__frames);
  expect(mutation600).toBe(mutation300);
});
```

Adapt selectors and the external mutation to the feature. If the implementation
uses a scheduler other than `requestAnimationFrame`, count that scheduler or an
explicit enhancement invocation instead. Do not add permanent debug hooks to
production solely for the test.

## Required regression cases

1. Initial render produces the desired component once.
2. A second enhancer call performs no DOM write and creates no duplicate.
3. No new scheduled work occurs between the 300 ms and 600 ms checkpoints.
4. One genuine external result mutation causes exactly one enhancement.
5. The next 300 ms to 600 ms window is stable.
6. Section replacement or teardown does not retain orphan observers/listeners.
7. The real draft preview still passes interaction, console, focus, mobile,
   reduced-motion, and horizontal-overflow checks.

## Acceptance record

Record:

```text
DYNAMIC_UI_STABILITY
module:
observed_root:
owned_dom_boundary:
idempotency_strategy:
scheduling_strategy:
cleanup_strategy:
initial_300_count:
initial_600_count:
external_mutation_count:
post_mutation_300_count:
post_mutation_600_count:
duplicate_dom_count:
preview_result:
```
