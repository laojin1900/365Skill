#!/usr/bin/env node

import { access, mkdir, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  assertSameIds,
  copyPath,
  listDirectories,
  readPublicationPolicy,
  walkFiles,
} from "./publication-core.mjs";

function option(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : undefined;
}

const scriptRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const sourceRoot = path.resolve(option("--source") ?? scriptRoot);
const outputValue = option("--output");
if (!outputValue) throw new Error("PUBLICATION_OUTPUT_REQUIRED");
const outputRoot = path.resolve(outputValue);
const relativeOutput = path.relative(sourceRoot, outputRoot);
if (!relativeOutput || (!relativeOutput.startsWith("..") && !path.isAbsolute(relativeOutput))) {
  throw new Error("PUBLICATION_OUTPUT_MUST_BE_OUTSIDE_SOURCE");
}

try {
  await access(outputRoot);
  if ((await readdir(outputRoot)).length > 0) throw new Error("PUBLICATION_OUTPUT_NOT_EMPTY");
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
  await mkdir(outputRoot, { recursive: true });
}

const policy = await readPublicationPolicy(sourceRoot);
const sourceSkillIds = await listDirectories(path.join(sourceRoot, "skills"));
for (const skillId of policy.public_skill_ids) {
  if (!sourceSkillIds.includes(skillId)) throw new Error("PUBLICATION_ALLOWLIST_SKILL_MISSING");
}

for (const sharedPath of policy.shared_paths) {
  await copyPath(sourceRoot, outputRoot, sharedPath);
}
for (const skillId of policy.public_skill_ids) {
  await copyPath(sourceRoot, outputRoot, path.join("skills", skillId));
  const evalPath = path.join(sourceRoot, "evals", skillId);
  try {
    await access(evalPath);
    await copyPath(sourceRoot, outputRoot, path.join("evals", skillId));
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}

const privateSkillIds = sourceSkillIds.filter((id) => !policy.public_skill_ids.includes(id));
for (const file of await walkFiles(outputRoot)) {
  const content = await readFile(file);
  const text = content.toString("utf8");
  if (privateSkillIds.some((id) => text.includes(id))) {
    throw new Error("PUBLICATION_PRIVATE_SKILL_REFERENCE_DETECTED");
  }
}

const exportedSkillIds = await listDirectories(path.join(outputRoot, "skills"));
assertSameIds(exportedSkillIds, policy.public_skill_ids, "PUBLICATION_EXPORTED_SKILLS_MISMATCH");
process.stdout.write(`${JSON.stringify({
  marker: "PUBLIC_SKILL_EXPORT_V1",
  publicSkillIds: policy.public_skill_ids,
  exportedSkillCount: exportedSkillIds.length,
})}\n`);
