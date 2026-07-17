import { cp, lstat, mkdir, readFile, readdir } from "node:fs/promises";
import path from "node:path";

const SKILL_ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;

export async function readPublicationPolicy(root) {
  const file = path.join(root, "catalog", "publication-policy.json");
  const policy = JSON.parse(await readFile(file, "utf8"));
  if (policy.schema_version !== 1 || policy.default_visibility !== "private") {
    throw new Error("PUBLICATION_POLICY_INVALID");
  }
  if (!Array.isArray(policy.public_skill_ids) || !Array.isArray(policy.shared_paths)) {
    throw new Error("PUBLICATION_POLICY_INVALID");
  }
  const ids = policy.public_skill_ids;
  if (new Set(ids).size !== ids.length || ids.some((id) => !SKILL_ID.test(id))) {
    throw new Error("PUBLICATION_SKILL_ALLOWLIST_INVALID");
  }
  return { ...policy, public_skill_ids: [...ids].sort() };
}

export async function listDirectories(root) {
  try {
    const entries = await readdir(root, { withFileTypes: true });
    return entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
  } catch (error) {
    if (error?.code === "ENOENT") return [];
    throw error;
  }
}

export async function assertRegularTree(root) {
  const stat = await lstat(root);
  if (stat.isSymbolicLink()) throw new Error("PUBLICATION_SYMLINK_REJECTED");
  if (!stat.isDirectory()) return;
  for (const entry of await readdir(root)) {
    await assertRegularTree(path.join(root, entry));
  }
}

export async function copyPath(sourceRoot, outputRoot, relativePath) {
  if (path.isAbsolute(relativePath) || relativePath.split(path.sep).includes("..")) {
    throw new Error("PUBLICATION_SHARED_PATH_INVALID");
  }
  const source = path.join(sourceRoot, relativePath);
  await assertRegularTree(source);
  const destination = path.join(outputRoot, relativePath);
  await mkdir(path.dirname(destination), { recursive: true });
  await cp(source, destination, { recursive: true, errorOnExist: true, force: false });
}

export function catalogSkillIds(source) {
  return [...source.matchAll(/^  - id: ([a-z0-9]+(?:-[a-z0-9]+)*)$/gmu)]
    .map((match) => match[1])
    .sort();
}

export function assertSameIds(actual, expected, errorCode) {
  if (JSON.stringify([...actual].sort()) !== JSON.stringify([...expected].sort())) {
    throw new Error(errorCode);
  }
}

export async function walkFiles(root) {
  const files = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    if (entry.name === ".git") continue;
    const absolute = path.join(root, entry.name);
    if (entry.isSymbolicLink()) throw new Error("PUBLICATION_SYMLINK_REJECTED");
    if (entry.isDirectory()) files.push(...await walkFiles(absolute));
    if (entry.isFile()) files.push(absolute);
  }
  return files;
}
