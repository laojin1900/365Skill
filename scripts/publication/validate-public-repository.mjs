#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  assertSameIds,
  catalogSkillIds,
  listDirectories,
  readPublicationPolicy,
  walkFiles,
} from "./publication-core.mjs";

function option(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : undefined;
}

const scriptRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const root = path.resolve(option("--root") ?? scriptRoot);
const policy = await readPublicationPolicy(root);
const allowed = policy.public_skill_ids;

assertSameIds(
  await listDirectories(path.join(root, "skills")),
  allowed,
  "PUBLIC_REPOSITORY_SKILLS_NOT_ALLOWLISTED",
);
const evalIds = await listDirectories(path.join(root, "evals"));
if (evalIds.some((id) => !allowed.includes(id))) {
  throw new Error("PUBLIC_REPOSITORY_EVAL_NOT_ALLOWLISTED");
}
const catalog = await readFile(path.join(root, "catalog", "skills.yaml"), "utf8");
assertSameIds(catalogSkillIds(catalog), allowed, "PUBLIC_REPOSITORY_CATALOG_MISMATCH");

const referencePattern = /(?<![\/A-Za-z0-9_.-])(?:skills|evals)\/([a-z0-9]+(?:-[a-z0-9]+)*)/gu;
for (const file of await walkFiles(root)) {
  if (!/\.(?:json|md|mjs|py|txt|ya?ml)$/u.test(file)) continue;
  const content = await readFile(file, "utf8");
  for (const match of content.matchAll(referencePattern)) {
    if (!allowed.includes(match[1])) throw new Error("PUBLIC_REPOSITORY_REFERENCE_NOT_ALLOWLISTED");
  }
}

process.stdout.write(`${JSON.stringify({
  marker: "PUBLIC_SKILL_REPOSITORY_VALID_V1",
  publicSkillIds: allowed,
  skillCount: allowed.length,
})}\n`);
