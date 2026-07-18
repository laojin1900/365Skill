import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function read(relativePath) {
  return readFile(path.join(skillRoot, relativePath), "utf8");
}

test("skill routes dynamic theme work through an executable settling gate", async () => {
  const skill = await read("SKILL.md");
  const stability = await read("references/dynamic-ui-stability.md");

  assert.match(skill, /change_class: <static-visual \/ structural-theme \/ dynamic-runtime>/u);
  assert.match(skill, /make every enhancement idempotent/u);
  assert.match(skill, /smallest stable container/u);
  assert.match(skill, /300 ms and 600 ms checkpoints/u);
  assert.match(skill, /exactly one additional\s+enhancement/u);
  assert.match(stability, /minimal synthetic page/u);
  assert.match(stability, /initial600\)\.toBe\(initial300\)/u);
  assert.match(stability, /mutation300\)\.toBe\(initial600 \+ 1\)/u);
  assert.match(stability, /mutation600\)\.toBe\(mutation300\)/u);
});

test("skill keeps draft mutation, publication, and project policy boundaries explicit", async () => {
  const skill = await read("SKILL.md");
  const handoff = await read("references/acceptance-and-handoff.md");

  assert.match(skill, /A draft-theme write is still a Shopify mutation/u);
  assert.match(skill, /Publish only after explicit Owner approval/u);
  assert.match(skill, /Project runbooks, target registries, protected-action gates/u);
  assert.match(skill, /For source-only work, remote-only fields may be `not-applicable`/u);
  assert.match(skill, /A narrow fix may list unrelated surfaces as `excluded`/u);
  assert.match(skill, /belong to Shopify Admin\/data operations/u);
  assert.match(skill, /Split mixed requests into separate/u);
  assert.match(skill, /project-neutral rules are extracted without store IDs/u);
  assert.match(handoff, /publish_state: not-published/u);
  assert.match(handoff, /dynamic_stability:/u);
});
