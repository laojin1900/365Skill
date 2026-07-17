import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { listDirectories, readPublicationPolicy, walkFiles } from "./publication-core.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

test("public export contains exactly allowlisted skills and no private skill identifiers", async () => {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), "365skill-public-export-"));
  const output = path.join(tempRoot, "repository");
  try {
    execFileSync(process.execPath, [
      path.join(repoRoot, "scripts/publication/export-public-repository.mjs"),
      "--source", repoRoot,
      "--output", output,
    ], { stdio: "pipe" });
    execFileSync(process.execPath, [
      path.join(output, "scripts/publication/validate-public-repository.mjs"),
      "--root", output,
    ], { stdio: "pipe" });

    const policy = await readPublicationPolicy(repoRoot);
    assert.deepEqual(await listDirectories(path.join(output, "skills")), policy.public_skill_ids);
    const privateIds = (await listDirectories(path.join(repoRoot, "skills")))
      .filter((id) => !policy.public_skill_ids.includes(id));
    const exportedText = (await Promise.all(
      (await walkFiles(output)).map(async (file) => (await readFile(file)).toString("utf8")),
    )).join("\n");
    for (const privateId of privateIds) assert.equal(exportedText.includes(privateId), false);
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});

test("validator ignores external skill URLs but rejects unlisted local skill paths", async () => {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), "365skill-public-validation-"));
  const output = path.join(tempRoot, "repository");
  try {
    execFileSync(process.execPath, [
      path.join(repoRoot, "scripts/publication/export-public-repository.mjs"),
      "--source", repoRoot,
      "--output", output,
    ], { stdio: "pipe" });
    const probe = path.join(output, "reference-probe.md");
    await writeFile(probe, `https://example.com/${"skills"}/external-reference\n`, "utf8");
    execFileSync(process.execPath, [
      path.join(output, "scripts/publication/validate-public-repository.mjs"),
      "--root", output,
    ], { stdio: "pipe" });

    await writeFile(probe, `Install ${"skills"}/not-allowlisted/SKILL.md\n`, "utf8");
    assert.throws(() => execFileSync(process.execPath, [
      path.join(output, "scripts/publication/validate-public-repository.mjs"),
      "--root", output,
    ], { stdio: "pipe" }));
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});
