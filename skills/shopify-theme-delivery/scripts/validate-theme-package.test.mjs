import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { validateThemePackage } from "./validate-theme-package.mjs";

async function createThemeFixture() {
  const root = await mkdtemp(path.join(os.tmpdir(), "shopify-theme-delivery-"));

  await Promise.all([
    mkdir(path.join(root, "templates"), { recursive: true }),
    mkdir(path.join(root, "sections"), { recursive: true }),
    mkdir(path.join(root, "config"), { recursive: true }),
  ]);
  await writeFile(
    path.join(root, "templates", "index.json"),
    JSON.stringify({ sections: { hero: { type: "hero", settings: {} } }, order: ["hero"] }),
  );
  await writeFile(
    path.join(root, "sections", "hero.liquid"),
    '<section>Hero</section>\n{% schema %}{"name":"Hero","settings":[],"presets":[{"name":"Hero"}]}{% endschema %}\n',
  );
  await writeFile(path.join(root, "config", "settings_data.json"), "{}\n");

  return root;
}

test("accepts a structurally valid Online Store 2.0 theme package", async () => {
  const root = await createThemeFixture();

  try {
    const result = await validateThemePackage({ themeRoot: root });

    assert.equal(result.ok, true);
    assert.deepEqual(result.errors, []);
    assert.equal(result.counts.templates, 1);
    assert.equal(result.counts.sections, 1);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("accepts Shopify JSON comments and trailing commas", async () => {
  const root = await createThemeFixture();

  try {
    await writeFile(
      path.join(root, "templates", "index.json"),
      `{
        // Shopify theme JSON supports comments.
        "sections": {
          "hero": { "type": "hero", },
        },
        "order": ["hero",],
      }`,
    );
    await writeFile(
      path.join(root, "sections", "hero.liquid"),
      `<section>Hero</section>
      {% schema %}
      {
        /* Section schema can also use comments. */
        "name": "Hero",
        "settings": [],
        "presets": [{ "name": "Hero", }],
      }
      {% endschema %}
      `,
    );

    const result = await validateThemePackage({ themeRoot: root });

    assert.equal(result.ok, true, result.errors.join("\n"));
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("rejects broken template order and missing section implementations", async () => {
  const root = await createThemeFixture();

  try {
    await writeFile(
      path.join(root, "templates", "index.json"),
      JSON.stringify({ sections: { hero: { type: "missing-section" } }, order: ["unknown"] }),
    );

    const result = await validateThemePackage({ themeRoot: root });

    assert.equal(result.ok, false);
    assert(result.errors.some((value) => value.includes("order id 'unknown'")));
    assert(result.errors.some((value) => value.includes("sections/missing-section.liquid")));
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("blocks settings_data.json in a changed-file manifest unless explicitly allowed", async () => {
  const root = await createThemeFixture();

  try {
    const blocked = await validateThemePackage({
      changedFiles: ["config/settings_data.json"],
      themeRoot: root,
    });
    const allowed = await validateThemePackage({
      allowSettingsData: true,
      changedFiles: ["config/settings_data.json"],
      themeRoot: root,
    });

    assert.equal(blocked.ok, false);
    assert(blocked.errors.some((value) => value.includes("settings_data.json")));
    assert.equal(allowed.ok, true);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
